import re
import shutil
import unicodedata

from datetime import datetime
from html import escape, unescape
from html.parser import HTMLParser
from pathlib import Path

from bs4 import BeautifulSoup

# ============================================================
# CONFIGURAÇÃO ESPECÍFICA PARA ESTOQUELAM.HTM
# ============================================================

ARQUIVO_ORIGEM_ESTOQUELAM = Path(r"\\server-embraco\c\z\estoquelam.htm")

# Colunas esperadas para o arquivo de estoque
COLUNAS_ESTOQUE = [
    "Cliente", "Tipo Aço", "Pf", "Bitola", "Acab",
    "Lote", "Qtde", "NF", "Corrida", "Em Prod.", "Contábil",
]

# Cabeçalho normalizado para identificação (se necessário)
CABECALHO_NORMALIZADO_ESTOQUE = [
    "CLIENTE", "TIPO ACO", "PF", "BITOLA", "ACAB",
    "LOTE", "QTDE", "NF", "CORRIDA", "EM PROD.", "CONTABIL",
]

# ============================================================
# FUNÇÕES COMUNS (COPIADAS DO SIAPV85.PY)
# ============================================================

def ler_arquivo(caminho):
    codificacoes = ["cp1252", "latin-1", "utf-8"]
    texto = None

    for codificacao in codificacoes:
        try:
            with open(caminho, "r", encoding=codificacao, errors="strict") as arquivo:
                texto = arquivo.read()
            break
        except UnicodeDecodeError:
            texto = None

    if texto is None:
        with open(caminho, "r", encoding="cp1252", errors="replace") as arquivo:
            texto = arquivo.read()

    anterior = None
    while texto != anterior:
        anterior = texto
        texto = unescape(texto)

    return texto

def limpar_texto(valor):
    if valor is None:
        return ""

    valor = unescape(str(valor))
    valor = re.sub(r"\s+", " ", valor)

    return valor.strip()

def normalizar_texto(valor):
    valor = limpar_texto(valor).upper()
    valor = unicodedata.normalize("NFD", valor)
    valor = "".join(c for c in valor if unicodedata.category(c) != "Mn")

    return re.sub(r"\s+", " ", valor).strip()

def converter_numero(valor):
    valor = limpar_texto(valor).upper()
    valor = valor.replace("KGS", "").replace("KG", "").strip()
    valor = valor.replace(".", "").replace(",", "")

    numeros = re.sub(r"[^\d]", "", valor)

    return int(numeros) if numeros else 0

def formatar_kg(valor):
    return f"{int(valor):,}".replace(",", ".") + " KG"

def extrair_titulo_do_nome_arquivo(caminho_arquivo):
    nome = Path(caminho_arquivo).stem
    nome_normalizado = normalizar_texto(nome)

    correspondencia = re.match(r"^([A-Za-zÀ-ÖØ-öø-ÿ]+)", nome)

    if correspondencia:
        prefixo = correspondencia.group(1)
        return prefixo[:1].upper() + prefixo[1:].lower()

    return nome if nome else "Relatório"

# ============================================================
# FUNÇÕES DE PARSE E GERAÇÃO DE HTML (COPIADAS DO SIAPV85.PY)
# ============================================================

class TabelaHTMLParser(HTMLParser):
    """
    Leitor tolerante para HTML antigo ou malformado.
    """

    def __init__(self):
        super().__init__(convert_charrefs=True)

        self.linhas = []
        self.linha_atual = None
        self.celula_atual = None
        self.tipo_celula_atual = None

    def iniciar_celula(self, tipo):
        self.finalizar_celula()

        if self.linha_atual is None:
            self.linha_atual = []

        self.celula_atual = []
        self.tipo_celula_atual = tipo

    def finalizar_celula(self):
        if self.celula_atual is None:
            return

        texto = limpar_texto("".join(self.celula_atual))

        self.linha_atual.append({
            "tipo": self.tipo_celula_atual,
            "valor": texto,
        })

        self.celula_atual = None
        self.tipo_celula_atual = None

    def iniciar_linha(self):
        self.finalizar_linha()
        self.linha_atual = []

    def finalizar_linha(self):
        self.finalizar_celula()

        if self.linha_atual:
            self.linhas.append(self.linha_atual)

        self.linha_atual = None

    def handle_starttag(self, tag, attrs):
        tag = tag.lower()

        if tag == "tr":
            self.iniciar_linha()
        elif tag == "td":
            self.iniciar_celula("td")
        elif tag == "th":
            self.iniciar_celula("th")

    def handle_startendtag(self, tag, attrs):
        tag = tag.lower()

        if tag in {"td", "th"}:
            self.iniciar_celula(tag)
            self.finalizar_celula()

    def handle_endtag(self, tag):
        tag = tag.lower()

        if tag in {"td", "th"}:
            self.finalizar_celula()
        elif tag == "tr":
            self.finalizar_linha()

    def handle_data(self, data):
        if self.celula_atual is not None:
            self.celula_atual.append(data)

    def finalizar(self):
        self.finalizar_linha()

def extrair_linhas_html(texto):
    parser = TabelaHTMLParser()
    parser.feed(texto)
    parser.close()
    parser.finalizar()

    return parser.linhas

def valores_da_linha(linha):
    return [limpar_texto(celula["valor"]) for celula in linha]

def linha_eh_cabecalho_estoque(valores):
    if len(valores) < 11:
        return False

    primeiros = [normalizar_texto(v) for v in valores[:11]]

    if primeiros == CABECALHO_NORMALIZADO_ESTOQUE:
        return True

    primeiro = normalizar_texto(valores[0])
    segundo = normalizar_texto(valores[1])

    if primeiro == "CLIENTE":
        return True

    if segundo == "TIPO ACO":
        return True

    return False

def linha_eh_total_estoque(valores):
    texto = " ".join(normalizar_texto(v) for v in valores)

    return "TOTAL DE MATERIAIS" in texto or "TOTAL MATERIAIS" in texto

def linha_tem_dados_estoque(valores):
    if len(valores) < 11:
        return False

    cliente = limpar_texto(valores[0])

    if not cliente:
        return False

    if linha_eh_cabecalho_estoque(valores):
        return False

    if linha_eh_total_estoque(valores):
        return False

    return True

def ajustar_linha_estoque(valores):
    if len(valores) < 11:
        return None

    if len(valores) == 11:
        return valores

    return valores[:11]

def classe_status_estoque(valor):
    valor = normalizar_texto(valor)

    if valor == "OK":
        return "ok"

    if valor == "VENCIDA":
        return "vencida"

    return "outro"

def extrair_registros_estoque(texto):
    linhas = extrair_linhas_html(texto)

    print(f"   Linhas HTML identificadas: {len(linhas)}")

    registros = []
    encontrou_cabecalho = False

    for linha in linhas:
        valores = valores_da_linha(linha)

        if len(valores) < 11:
            continue

        if linha_eh_cabecalho_estoque(valores):
            encontrou_cabecalho = True
            continue

        if not encontrou_cabecalho:
            continue

        if not linha_tem_dados_estoque(valores):
            continue

        valores = ajustar_linha_estoque(valores)

        if valores is None:
            continue

        registro = {
            "Cliente": valores[0], "Tipo Aço": valores[1], "Pf": valores[2],
            "Bitola": valores[3], "Acab": valores[4], "Lote": valores[5],
            "Qtde": valores[6], "NF": valores[7], "Corrida": valores[8],
            "Em Prod.": valores[9], "Contábil": valores[10],
        }

        registro["QtdeNum"] = converter_numero(registro["Qtde"])
        registro["EmProdNum"] = converter_numero(registro["Em Prod."])
        registro["Status"] = registro["Contábil"]
        registro["StatusClasse"] = classe_status_estoque(registro["Contábil"])
        registro["AguardandoOrdem"] = (registro["QtdeNum"] - registro["EmProdNum"]) > 0

        registros.append(registro)

    print(f"   Registros aproveitados: {len(registros)}")

    return registros

def extrair_data_estoque(texto):
    texto_limpo = limpar_texto(re.sub(r"<[^>]+>", " ", texto, flags=re.IGNORECASE))

    padrao = re.search(
        r"atualizada\s+em\s+(\d{1,2}/\d{1,2}/\d{4}).{0,150}?(\d{1,2}:\d{2}:\d{2})",
        texto_limpo, flags=re.IGNORECASE | re.DOTALL,
    )

    if padrao:
        return f"{padrao.group(1)} às {padrao.group(2)}"

    return "Data não disponível"

def extrair_totais_estoque(texto):
    texto_limpo = limpar_texto(re.sub(r"<[^>]+>", " ", texto, flags=re.IGNORECASE))

    total_estoque = 0
    total_processo = 0

    padrao_estoque = re.search(
        r"Total\s+de\s+Materiais\s+em\s+estoque\s*:?\s*([\d\.,]+)",
        texto_limpo, flags=re.IGNORECASE,
    )

    padrao_processo = re.search(
        r"Total\s+de\s+Materiais\s+em\s+processo\s*:?\s*([\d\.,]+)",
        texto_limpo, flags=re.IGNORECASE,
    )

    if padrao_estoque:
        total_estoque = converter_numero(padrao_estoque.group(1))

    if padrao_processo:
        total_processo = converter_numero(padrao_processo.group(1))

    return {"estoque": total_estoque, "processo": total_processo}

def gerar_linha_html_estoque(registro):
    status = escape(registro["Contábil"])
    classe = registro["StatusClasse"]
    aguardando = "true" if registro["AguardandoOrdem"] else "false"

    return f"""
<tr
    data-qtde="{registro['QtdeNum']}"
    data-em-prod="{registro['EmProdNum']}"
    data-status="{status}"
    data-aguardando="{aguardando}"
>
    <td>{escape(registro['Cliente'])}</td>
    <td>{escape(registro['Tipo Aço'])}</td>
    <td>{escape(registro['Pf'])}</td>
    <td>{escape(registro['Bitola'])}</td>
    <td>{escape(registro['Acab'])}</td>
    <td>{escape(registro['Lote'])}</td>
    <td>{escape(registro['Qtde'])}</td>
    <td>{escape(registro['NF'])}</td>
    <td>{escape(registro['Corrida'])}</td>
    <td>{escape(registro['Em Prod.'])}</td>
    <td>
        <span class="status {classe}">
            {status}
        </span>
    </td>
</tr>"""

def gerar_html_estoque(titulo, data, registros, totais):
    linhas = "\n".join(gerar_linha_html_estoque(r) for r in registros)
    headers_html = "".join(f"<th>{h}</th>" for h in COLUNAS_ESTOQUE)

    return f"""<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{escape(titulo)}</title>
<style>
*{{box-sizing:border-box}}
body{{margin:0;background:#f4f7f5;font:15px Arial;color:#202820}}
.wrap{{max-width:1500px;margin:20px auto;padding:0 12px}}
.head,.box,.card{{background:white;border-radius:12px;box-shadow:0 4px 18px #0001}}
.head{{padding:18px 20px;margin-bottom:14px}}
.brand{{display:flex;align-items:center;gap:12px;margin-bottom:10px}}
.brand-mark{{width:38px;height:38px;border-radius:10px;background:#176b28;color:white;display:flex;align-items:center;justify-content:center;font-weight:bold;font-size:18px;box-shadow:0 3px 8px #0002}}
.brand-text{{font-size:12px;font-weight:bold;letter-spacing:1.2px;color:#176b28;text-transform:uppercase}}
.head h1{{margin:0;color:#176b28;font-size:28px;line-height:1.15}}
.head small{{color:#667}}
.controls{{display:flex;gap:8px;flex-wrap:wrap;margin-top:14px}}
.controls input,.controls select,.controls button{{padding:10px;border:1px solid #d8e0da;border-radius:8px;background:white;font-size:15px}}
.controls input{{flex:1;min-width:230px}}
.controls button{{background:#176b28;color:white;cursor:pointer;border:none;font-weight:bold;padding:10px 20px}}
.controls button:hover{{background:#135620}}
.controls .btn-estoque{{display:inline-flex;align-items:center;justify-content:center;padding:10px 20px;border:1px solid #d8e0da;border-radius:8px;background:#176b28;color:white;text-decoration:none;font-size:14px;font-weight:bold;white-space:nowrap;cursor:pointer}}
.controls .btn-estoque:hover{{background:#135620}}
.controls .btn-estoque{{display:inline-flex;align-items:center;justify-content:center;padding:10px 20px;border:1px solid #d8e0da;border-radius:8px;background:#176b28;color:white;text-decoration:none;font-size:14px;font-weight:bold;white-space:nowrap;cursor:pointer}}
.controls .btn-estoque:hover{{background:#135620}}
.box{{overflow:hidden}}
.scroll{{overflow-x:auto}}
table{{width:100%;border-collapse:collapse;text-align:center}}
th,td{{padding:13px;border-bottom:1px solid #e1e6e2;white-space:nowrap}}
th{{background:#eaffea;color:#155c22;cursor:pointer;position:sticky;top:0;font-weight:bold;line-height:1.15}}
tr:hover td{{background:#f4fff4}}
.status{{padding:6px 12px;border-radius:20px;font-weight:bold;font-size:12px;display:inline-block}}
.ok{{background:#dcfce7;color:#166534}}
.vencida{{background:#fef3c7;color:#92400e}}
.outro{{background:#e0f2fe;color:#0c4a6e}}
.summary{{display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:10px;margin-top:14px}}
.card{{padding:14px;text-align:center;min-height:92px}}
.card small{{color:#667;font-size:12px;display:block}}
.card b{{display:block;font-size:21px;margin-top:7px;color:#176b28;font-weight:bold}}
.card.accent{{border-top:4px solid #176b28}}
.status-dashboard{{margin-top:18px;padding:18px;background:#f8faf8;border:1px solid #e3e9e4;border-radius:14px}}
.status-dashboard-header{{display:flex;align-items:center;justify-content:space-between;gap:12px;margin-bottom:14px}}
.dashboard-title{{color:#176b28;font-size:15px;font-weight:bold;letter-spacing:.2px}}
.dashboard-subtitle{{color:#718078;font-size:12px}}
.status-grid{{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px}}
.status-card{{background:white;border:1px solid #e2e8e3;border-radius:12px;padding:13px 14px;min-height:92px;box-shadow:0 2px 8px #0000000a;transition:transform .15s,box-shadow .15s}}
.status-card:hover{{transform:translateY(-1px);box-shadow:0 5px 14px #00000012}}
.status-name{{display:flex;align-items:center;gap:8px;font-size:12px;font-weight:bold;color:#35413a;margin-bottom:11px}}
.status-dot{{width:9px;height:9px;border-radius:50%;flex:0 0 9px;background:#9aa59e}}
.status-card.status-lib .status-dot{{background:#22c55e}}
.status-card.status-sep .status-dot{{background:#f59e0b}}
.status-card.status-pon .status-dot{{background:#3b82f6}}
.status-card.status-agu .status-dot{{background:#eab308}}
.status-card.status-dec .status-dot{{background:#ef4444}}
.status-card.status-ser .status-dot{{background:#f97316}}
.status-card.status-tre .status-dot{{background:#6366f1}}
.status-card.status-end .status-dot{{background:#0ea5e9}}
.status-card.status-esp .status-dot{{background:#a855f7}}
.status-values{{display:flex;align-items:flex-end;gap:16px}}
.status-main{{font-size:21px;font-weight:bold;color:#176b28;line-height:1}}
.status-label{{display:block;margin-top:4px;color:#7a857e;font-size:10px}}
.status-kg{{font-size:13px;font-weight:bold;color:#46534b;line-height:1.1}}
.status-kg-label{{display:block;margin-top:4px;color:#7a857e;font-size:10px}}
@media (max-width:900px){{.status-grid{{grid-template-columns:repeat(2,minmax(0,1fr))}}}}
@media (max-width:560px){{.status-grid{{grid-template-columns:1fr}}.status-dashboard-header{{align-items:flex-start;flex-direction:column;gap:4px}}}}
</style>
</head>
<body>
<div class="wrap">
<div class="head">
<div class="brand"><div class="brand-mark">P</div><div class="brand-text">Portal de Produção</div></div>
<h1>{escape(titulo)}</h1>
<small>Listagem atualizada em {escape(data)}</small>
</div>

<div class="box" style="padding:14px;margin-bottom:14px">
<div class="controls">
<input id="q" placeholder="🔎 Pesquisar em todas as colunas">
<select id="st">
<option value="">Todos os status</option>
<option>OK</option>
<option>VENCIDA</option>
<option>OUTRO</option>
</select>
<select id="aguardando">
<option value="">Todos os itens</option>
<option value="true">Aguardando Ordem</option>
</select>
<button onclick="clearF()">Limpar filtros</button>
<button onclick="csv()">Exportar CSV</button>
</div>
</div>

<div class="box">
<div class="scroll">
<table id="t">
<thead><tr>{headers_html}</tr></thead>
<tbody>
{linhas}
</tbody>
</table>
</div>
<div style="padding:10px;color:#667" id="count">{len(registros)} registros exibidos</div>
</div>

<div class="summary" id="summary">
<div class="card"><small>Total em estoque</small><b id="total-estoque">{formatar_kg(totais['estoque'])}</b></div>
<div class="card"><small>Total em processo</small><b id="total-processo">{formatar_kg(totais['processo'])}</b></div>
<div class="card"><small>Total de itens</small><b id="total-itens">{len(registros)}</b></div>
</div>
</div>

<script>
const q = document.querySelector('#q');
const st = document.querySelector('#st');
const aguardando = document.querySelector('#aguardando');
const rows = [...document.querySelectorAll('#t tbody tr')];

function applyFilters() {{
    const texto = q.value.toLowerCase().trim();
    const status = st.value;
    const aguardandoOrdem = aguardando.value;
    let count = 0;

    rows.forEach(r => {{
        const textoLinha = r.innerText.toLowerCase();
        const statusLinha = r.dataset.status || "";
        const aguardandoLinha = r.dataset.aguardando || "";

        const passaTexto = !texto || textoLinha.includes(texto);
        const passaStatus = !status || statusLinha === status;
        const passaAguardando = !aguardandoOrdem || aguardandoLinha === aguardandoOrdem;

        const mostrar = passaTexto && passaStatus && passaAguardando;

        r.hidden = !mostrar;
        if (mostrar) count++;
    }});

    document.querySelector('#count').textContent = count + " registros exibidos";
}}

function clearF() {{
    q.value = "";
    st.value = "";
    aguardando.value = "";
    applyFilters();
}}

q.addEventListener('input', applyFilters);
st.addEventListener('change', applyFilters);
aguardando.addEventListener('change', applyFilters);

document.querySelectorAll('#t thead th').forEach((th, i) => {{
    th.addEventListener('click', () => {{
        const tbody = document.querySelector('#t tbody');
        const order = tbody.dataset.order === "asc" ? "desc" : "asc";
        tbody.dataset.order = order;

        const sorted = [...rows].sort((a, b) => {{
            const va = a.cells[i].innerText.trim();
            const vb = b.cells[i].innerText.trim();
            const cmp = va.localeCompare(vb, "pt-BR", {{ numeric: true, sensitivity: "base" }});
            return order === "asc" ? cmp : -cmp;
        }});

        sorted.forEach(r => tbody.appendChild(r));
    }});
}});

function escapeCSV(v) {{ return '"' + v.replaceAll('"', '""') + '"'; }}

function csv() {{
    const visible = rows.filter(r => !r.hidden);
    const headers = [...document.querySelectorAll('#t thead th')].map(th => th.innerText.trim());
    const data = visible.map(r => [...r.cells].map(c => c.innerText.trim()));
    const content = [headers, ...data].map(l => l.map(escapeCSV).join(";")).join("\\n");
    const blob = new Blob(["\\ufeff" + content], {{ type: "text/csv;charset=utf-8" }});
    const link = document.createElement("a");
    link.href = URL.createObjectURL(blob);
    link.download = "{escape(titulo)}.csv";
    link.click();
    URL.revokeObjectURL(link.href);
}}

applyFilters();
</script>
</body>
</html>"""

# ============================================================
# EXECUÇÃO PRINCIPAL DO NOVO SCRIPT
# ============================================================

def processar_estoquelam_especifico():
    print("=" * 80)
    print(f"PROCESSANDO ARQUIVO ESPECÍFICO: {ARQUIVO_ORIGEM_ESTOQUELAM.name}")
    print("=" * 80)

    if not ARQUIVO_ORIGEM_ESTOQUELAM.exists():
        print(f"❌ Erro: Arquivo não encontrado em {ARQUIVO_ORIGEM_ESTOQUELAM}")
        return

    # Define o caminho de destino com "_v2"
    nome_base = ARQUIVO_ORIGEM_ESTOQUELAM.stem
    extensao = ARQUIVO_ORIGEM_ESTOQUELAM.suffix
    caminho_destino = ARQUIVO_ORIGEM_ESTOQUELAM.parent / f"{nome_base}_v2{extensao}"

    try:
        texto = ler_arquivo(ARQUIVO_ORIGEM_ESTOQUELAM)
        titulo = extrair_titulo_do_nome_arquivo(ARQUIVO_ORIGEM_ESTOQUELAM)
        data = extrair_data_estoque(texto)
        registros = extrair_registros_estoque(texto)
        totais = extrair_totais_estoque(texto)

        print(f"Título do relatório: {titulo}")
        print(f"✅ Total de registros extraídos: {len(registros)}")

        html_final = gerar_html_estoque(titulo=titulo, data=data, registros=registros, totais=totais)

        with open(caminho_destino, "w", encoding="utf-8") as arquivo:
            arquivo.write(html_final)

        print(f"✅ Arquivo melhorado gerado em: {caminho_destino}")

    except Exception as e:
        print(f"❌ Erro ao processar o arquivo {ARQUIVO_ORIGEM_ESTOQUELAM.name}: {e}")

if __name__ == "__main__":
    processar_estoquelam_especifico()