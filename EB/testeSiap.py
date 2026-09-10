import re
import shutil
import unicodedata

from datetime import datetime
from html import escape, unescape
from html.parser import HTMLParser
from pathlib import Path
from bs4 import BeautifulSoup

# Configuração dos caminhos para o ambiente de homologação/produção
PASTA_ORIGEM = Path(r"C:\FTP")
PASTA_DESTINO = Path(r"C:\FTP 2.0")

# Caminhos específicos para o estoquelam.htm
CAMINHO_ESTOQUELAM_ORIGEM = Path(r"C:\z\estoquelam.htm")
CAMINHO_ESTOQUELAM_DESTINO = PASTA_DESTINO / "estoquelam.htm"

NOME_LOGO_EMBRACO = "logo_embo_new.png"

ARQUIVOS_ESTOQUE = {
    "acoforte78788798708972jkjk098080546543211222hkjfk23123k56s5gdj5412kk44k55332kk66h5421k_2":
        "Acoforte - Estoque",

    "acovisa0898095278916771yiuy98978jhgnmbjkhfdahfa98371987132bbnbnbbbb2":
        "Acovisa - Estoque",

    "trefita08972jkjk098080546543211222hkjfk23123k56s5gdj5412kk44k55332kk66h5421k_2":
        "Trefita - Estoque",

    "estoquelam":
        "Estoque Geral - Laminação",
}

ARQUIVOS_ESTOQUE_CLIENTES = {
    "ACOFORTE": (
        "Acoforte",
        "https://www.embo.com.br/logon/usuarios/acoforte78788798708972jkjk098080546543211222hkjfk23123k56s5gdj5412kk44k55332kk66h5421k_2.htm",
    ),
    "ACOVISA": (
        "Acovisa",
        "https://www.embo.com.br/logon/usuarios/acovisa0898095278916771yiuy98978jhgnmbjkhfdahfa98371987132bbnbnbbbb2.htm",
    ),
    "TREFITA": (
        "Trefita",
        "https://www.embo.com.br/logon/usuarios/trefita08972jkjk098080546543211222hkjfk23123k56s5gdj5412kk44k55332kk66h5421k_2.htm",
    ),
}

COLUNAS_ESTOQUE = [
    "Cliente", "Tipo Aço", "Pf", "Bitola", "Acab",
    "Lote", "Qtde", "NF", "Corrida", "Em Prod.", "Contábil",
]

CABECALHO_NORMALIZADO_ESTOQUE = [
    "CLIENTE", "TIPO ACO", "PF", "BITOLA", "ACAB",
    "LOTE", "QTDE", "NF", "CORRIDA", "EM PROD.", "CONTABIL",
]

HEADERS_PRODUCAO = [
    "O.Pr.", "Lote", "Formato", "Bitola Laminado", "Aço", "Perfil",
    "Acabamento", "Bitola Final", "Tolerância", "Cliente", "Qtde",
    "Prazo Dado", "P.C.P", "Status do Processo", "Observações",
]

DIRETORIA_STEM = "diretoria98841101651222hkjfk23123k56s5gdj5412kk44k55332kk66h5421k"


# ============================================================
# FUNÇÕES COMUNS
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


def normalizar_nome_arquivo(nome):
    return Path(nome).stem.strip().lower()


def converter_numero(valor):
    valor = limpar_texto(valor).upper()
    valor = valor.replace("KGS", "").replace("KG", "").strip()
    valor = valor.replace(".", "").replace(",", "")
    numeros = re.sub(r"[^\d]", "", valor)
    return int(numeros) if numeros else 0


def formatar_kg(valor):
    return f"{int(valor):,}".replace(",", ".") + " KG"


def formatar_lote_exibicao(valor):
    valor = limpar_texto(valor)
    if valor.isdigit():
        return valor.lstrip("0") or "0"
    return valor


def limpar_nome_arquivo(nome):
    nome = re.sub(r'[^a-zA-Z0-9._-]', '', nome)
    nome = re.sub(r'\.+', '.', nome)
    return nome if nome else 'arquivo.htm'


def renomear_corrompidos(pasta):
    pasta_path = Path(pasta)
    if not pasta_path.exists():
        return 0
    contador = 0
    for item in pasta_path.iterdir():
        if item.is_file() and item.suffix.lower() == ".htm":
            nome_limpo = limpar_nome_arquivo(item.name)
            if item.name != nome_limpo:
                novo = item.parent / nome_limpo
                if novo.exists():
                    base, ext = (
                        nome_limpo.rsplit('.', 1)
                        if '.' in nome_limpo
                        else (nome_limpo, 'htm')
                    )
                    i = 1
                    while (item.parent / f"{base}_{i}.{ext}").exists():
                        i += 1
                    novo = item.parent / f"{base}_{i}.{ext}"
                item.rename(novo)
                contador += 1
    return contador


def extrair_titulo_do_nome_arquivo(caminho_arquivo):
    nome = Path(caminho_arquivo).stem
    nome_normalizado = normalizar_texto(nome)
    if nome_normalizado.startswith("ACOFORTE"):
        return "Acoforte"
    correspondencia = re.match(r"^([A-Za-zÀ-ÖØ-öø-ÿ]+)", nome)
    if correspondencia:
        prefixo = correspondencia.group(1)
        return prefixo[:1].upper() + prefixo[1:].lower()
    return nome if nome else "Relatório"


def copiar_logo_embraco():
    caminho_origem_logo = PASTA_ORIGEM / NOME_LOGO_EMBRACO
    caminho_destino_logo = PASTA_DESTINO / NOME_LOGO_EMBRACO
    if caminho_origem_logo.exists():
        try:
            shutil.copy2(caminho_origem_logo, caminho_destino_logo)
            print(f"✅ Logo '{NOME_LOGO_EMBRACO}' copiado para '{PASTA_DESTINO}'")
        except Exception as e:
            print(f"❌ Erro ao copiar o logo '{NOME_LOGO_EMBRACO}': {e}")
    else:
        print(f"⚠️ Logo '{NOME_LOGO_EMBRACO}' não encontrado em '{PASTA_ORIGEM}'.")


# ============================================================
# MOTOR 1 — TRATAMENTO EXCLUSIVO DE ESTOQUE
# ============================================================

class TabelaHTMLParser(HTMLParser):
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
        elif tag in {"td", "th"}:
            self.iniciar_celula(tag)

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
    return normalizar_texto(valores[0]) == "CLIENTE" or normalizar_texto(valores[1]) == "TIPO ACO"


def linha_eh_total_estoque(valores):
    texto = " ".join(normalizar_texto(v) for v in valores)
    return "TOTAL DE MATERIAIS" in texto or "TOTAL MATERIAIS" in texto


def linha_tem_dados_estoque(valores):
    if len(valores) < 11 or not limpar_texto(valores[0]):
        return False
    return not linha_eh_cabecalho_estoque(valores) and not linha_eh_total_estoque(valores)


def ajustar_linha_estoque(valores):
    return valores[:11] if len(valores) >= 11 else None


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
        if not encontrou_cabecalho or not linha_tem_dados_estoque(valores):
            continue
        valores = ajustar_linha_estoque(valores)
        if valores is None:
            continue

        registro = {
            "Cliente": valores[0], "Tipo Aço": valores[1], "Pf": valores[2],
            "Bitola": valores[3], "Acab": valores[4], "Lote": str(valores[5]),
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
    return f"{padrao.group(1)} às {padrao.group(2)}" if padrao else "Data não disponível"


def extrair_totais_estoque(texto):
    texto_limpo = limpar_texto(re.sub(r"<[^>]+>", " ", texto, flags=re.IGNORECASE))
    total_estoque = 0
    total_processo = 0
    padrao_estoque = re.search(r"Total\s+de\s+Materiais\s+em\s+estoque\s*:?\s*([\d\.,]+)", texto_limpo,
                               flags=re.IGNORECASE)
    padrao_processo = re.search(r"Total\s+de\s+Materiais\s+em\s+processo\s*:?\s*([\d\.,]+)", texto_limpo,
                                flags=re.IGNORECASE)
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
<tr data-qtde="{registro['QtdeNum']}" data-em-prod="{registro['EmProdNum']}" data-status="{status}" data-aguardando="{aguardando}">
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
    <td><span class="status {classe}">{status}</span></td>
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
.brand{{display:flex;align-items:center;gap:14px;margin-bottom:10px}}
.brand-logo{{width:58px;height:58px;object-fit:contain;display:block}}
.brand-text{{display:flex;flex-direction:column;justify-content:center;line-height:1.15}}
.brand-name{{display:block;color:#20208f;font-size:22px;font-weight:bold;letter-spacing:1px}}
.brand-subtitle{{display:block;color:#f58200;font-size:12px;font-weight:bold;letter-spacing:.35px;margin-top:4px}}
.head h1{{margin:0;color:#176b28;font-size:28px;line-height:1.15}}
.head small{{color:#667}}
.controls{{display:flex;gap:8px;flex-wrap:wrap;margin-top:14px}}
.controls input,.controls select,.controls button{{padding:10px;border:1px solid #d8e0da;border-radius:8px;background:white;font-size:15px}}
.controls input{{flex:1;min-width:230px}}
.controls button{{background:#176b28;color:white;cursor:pointer;border:none;font-weight:bold;padding:10px 20px}}
.controls button:hover{{background:#135620}}
.box{{overflow:hidden}}
.scroll{{overflow-x:auto}}
table{{width:100%;border-collapse:collapse;text-align:center}}
th,td{{padding:13px;border-bottom:1px solid #e1e6e2;white-space:nowrap;font-weight:bold}}
th{{background:#eaffea;color:#155c22;cursor:pointer;position:sticky;top:0;font-weight:bold;line-height:1.15}}
tr:hover td{{background:#f4fff4}}
.status{{padding:6px 12px;border-radius:20px;font-weight:bold;font-size:12px;display:inline-block}}
.ok{{background:#dcfce7;color:#166534}}
.vencida{{background:#fef3c7;color:#92400e}}
.outro{{background:#e0f2fe;color:#0c4a6e}}
.summary{{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:12px;margin-top:14px}}
.card{{padding:15px;text-align:center}}
.card small{{color:#667;font-size:12px;display:block}}
.card b{{display:block;font-size:22px;margin-top:8px;color:#176b28;font-weight:bold}}
</style>
</head>
<body>
<div class="wrap">
<div class="head">
    <div class="brand">
        <img class="brand-logo" src="logo_embo_new.png" alt="Logo EMBRACO">
        <div class="brand-text">
            <strong class="brand-name">SIAPE</strong>
            <span class="brand-subtitle">Sistema Integrado de Acompanhamento de Produção EMBRACO</span>
        </div>
    </div>
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
const totalItensEl = document.querySelector('#total-itens');

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
    if (totalItensEl) {{
        totalItensEl.textContent = count;
    }}
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


def processar_arquivo_estoque(caminho_origem, caminho_destino, titulo):
    print()
    print("=" * 80)
    print(f"[ESTOQUE] Processando: {caminho_origem.name}")
    print("=" * 80)

    texto = ler_arquivo(caminho_origem)
    data = extrair_data_estoque(texto)
    registros = extrair_registros_estoque(texto)
    totais = extrair_totais_estoque(texto)

    print(f"Título: {titulo}")
    print(f"✅ Total de registros: {len(registros)}")

    html_final = gerar_html_estoque(titulo=titulo, data=data, registros=registros, totais=totais)
    caminho_destino.parent.mkdir(parents=True, exist_ok=True)

    with open(caminho_destino, "w", encoding="utf-8") as arquivo:
        arquivo.write(html_final)

    print(f"✅ Arquivo gerado em: {caminho_destino}")


# ============================================================
# MOTOR 2 — TRATAMENTO DE PRODUÇÃO (demais .htm)
# ============================================================

def extrair_data_producao(texto):
    texto_limpo = limpar_texto(re.sub(r"<[^>]+>", " ", texto, flags=re.IGNORECASE))
    padrao = re.search(
        r"atualizada\s+em\s+(\d{1,2}/\d{1,2}/\d{4}).{0,150}?(\d{1,2}:\d{2}:\d{2})",
        texto_limpo, flags=re.IGNORECASE | re.DOTALL,
    )
    return f"{padrao.group(1)} às {padrao.group(2)}" if padrao else "Data não disponível"


def status_da_imagem(src, alt="", title=""):
    texto = " ".join(limpar_texto(v) for v in (src, alt, title) if limpar_texto(v))
    up = normalizar_texto(texto)

    if "LIBERADO" in up:
        return "LIBERADO", "lib"
    if "PONTEADO" in up:
        return "PONTEADO", "pon"
    if (
            "AGUARDANDO" in up
            or "AGUARDA SEPARACAO" in up
            or "AGUARDA SEPARAR" in up
            or "AGUARDA" in up and "SEPAR" in up
            or "AGUARDA SEPAR" in up
    ):
        return "AGUARDANDO SEPARAÇÃO", "agu"
    if "SEPARADO" in up:
        return "SEPARADO", "sep"
    if "DECAPADO" in up:
        return "DECAPADO", "dec"
    if "SERRADO" in up:
        return "SERRADO", "ser"
    if "TREFILADO" in up:
        return "TREFILADO", "tre"
    if "ENDIREITADO" in up:
        return "ENDIREITADO", "end"
    if "ESPECIAL" in up:
        return "ESPECIAL", "esp"
    return "", ""


def classe_status_producao(valor):
    valor = normalizar_texto(valor)
    if "LIBERADO" in valor:
        return "lib"
    if "SEPARADO" in valor:
        return "sep"
    if "PONTEADO" in valor:
        return "pon"
    if "AGUARDANDO SEPARAÇÃO" in valor or "AGUARDANDO SEPARACAO" in valor:
        return "agu"
    if "DECAPADO" in valor:
        return "dec"
    if "SERRADO" in valor:
        return "ser"
    if "TREFILADO" in valor:
        return "tre"
    if "ENDIREITADO" in valor:
        return "end"
    if "ESPECIAL" in valor:
        return "esp"
    return ""


def linha_eh_registro_producao(valores):
    if len(valores) < 5:
        return False
    valores_limpos = [limpar_texto(valor) for valor in valores]
    if not any(valores_limpos):
        return False
    texto_linha = normalizar_texto(" ".join(valores_limpos))
    palavras_invalidas = {
        "MENU", "INICIO", "INÍCIO", "SAIR", "VOLTAR", "RELATORIO",
        "RELATORIO DE PRODUCAO", "PRODUCAO", "ORDEM DE PRODUCAO", "O.PR.",
        "LOTE", "ACO", "STATUS", "OBSERVACOES", "PF.L", "BIT.L", "PF",
        "AC", "BIT.", "TOL.", "CLIENTE", "QTDE", "PRAZO DADO", "P.C.P",
    }
    if texto_linha in palavras_invalidas or normalizar_texto(valores_limpos[0]) in palavras_invalidas:
        return False

    ordem_producao = re.sub(r"\s+", "", valores_limpos[0])
    if not re.fullmatch(r"\d{4,}", ordem_producao):
        return False

    lote = re.sub(r"\s+", "", valores_limpos[1])
    if not re.fullmatch(r"[A-Za-z0-9]{3,}", lote):
        return False

    return bool(valores_limpos[2] or valores_limpos[3] or valores_limpos[4])


def extrair_registros_producao(html_bruto):
    if not html_bruto.rstrip().endswith(">"):
        html_bruto += "</th></tr></table>"
    elif "</tr>" not in html_bruto.lower()[-50:]:
        html_bruto += "</tr></table>"

    soup = BeautifulSoup(html_bruto, "html.parser")
    linhas_tr = soup.find_all("tr")
    print(f"   Linhas <tr> identificadas: {len(linhas_tr)}")
    registros = []

    for tr in linhas_tr:
        celulas = tr.find_all(["th", "td"], recursive=False)
        if len(celulas) < 5:
            celulas = tr.find_all(["th", "td"], recursive=True)

        valores = [limpar_texto(celula.get_text(" ", strip=True)) for celula in celulas]
        observacao_celula_original = ""
        if len(celulas) >= 15:
            raw_tr = str(tr)
            encontrados_obs = re.findall(
                r'<th[^>]*\bwidth\s*=\s*["\']?120["\']?[^>]*>(.*?)</th>',
                raw_tr, flags=re.IGNORECASE | re.DOTALL,
            )
            if encontrados_obs:
                observacao_celula_original = limpar_texto(
                    BeautifulSoup(encontrados_obs[-1], "html.parser").get_text(" ", strip=True)
                )

            if not observacao_celula_original:
                observacao_celula_original = limpar_texto(celulas[14].get_text(" ", strip=True))

            if not observacao_celula_original:
                textos = [limpar_texto(no) for no in celulas[14].find_all(string=True) if limpar_texto(no)]
                observacao_celula_original = " ".join(dict.fromkeys(textos))

        if not linha_eh_registro_producao(valores):
            continue

        status_txt = ""
        status_cls = ""

        for img in tr.find_all("img"):
            status_txt, status_cls = status_da_imagem(
                img.get("src", ""), img.get("alt", ""), img.get("title", ""),
            )
            if status_txt:
                break

        while len(valores) < 15:
            valores.append("")

        if len(valores) > 15:
            observacao_extra = " ".join(valor for valor in valores[14:] if valor)
            valores = valores[:14] + [observacao_extra]

        aco_content_in_cell = limpar_texto(valores[4])
        if aco_content_in_cell and " " in aco_content_in_cell and not any(valores[i].strip() for i in range(5, 12)):
            parts = aco_content_in_cell.split()

            def eh_data_pt_br(s):
                return bool(re.fullmatch(r"\d{2}/\d{2}/\d{4}", s))

            def eh_quantidade(s):
                return bool(re.fullmatch(r"\d{1,3}(?:\.\d{3})*|\d+", s))

            def eh_numero_decimal(s):
                return bool(re.fullmatch(r"\d+(?:[.,]\d+)", s))

            def eh_tol(s):
                return bool(re.fullmatch(r"H-\d+(?:[.,]\d+)?", s.upper()) or eh_numero_decimal(s))

            def eh_codigo_curto(s):
                return bool(re.fullmatch(r"[A-Za-zÀ-ÿ]{1,4}", s))

            indice_data = next((i for i in range(len(parts) - 1, -1, -1) if eh_data_pt_br(parts[i])), None)

            if indice_data is not None and indice_data >= 2:
                valores[11] = parts[indice_data]
                indice_qtde = indice_data - 1

                if eh_quantidade(parts[indice_qtde]):
                    valores[10] = parts[indice_qtde]
                    indice_bit = None
                    indice_pf = None

                    for i in range(2, indice_qtde):
                        if (eh_numero_decimal(parts[i]) and eh_codigo_curto(parts[i - 1]) and eh_codigo_curto(
                                parts[i - 2])):
                            indice_bit = i
                            indice_pf = i - 2
                            break

                    if indice_bit is not None:
                        valores[4] = " ".join(parts[:indice_pf])
                        valores[5] = parts[indice_pf]
                        valores[6] = parts[indice_pf + 1]
                        valores[7] = parts[indice_bit]

                        entre = parts[indice_bit + 1:indice_qtde]
                        if not entre:
                            valores[8] = ""
                            valores[9] = ""
                        elif len(entre) == 1:
                            valores[8] = ""
                            valores[9] = entre[0]
                        elif eh_tol(entre[0]):
                            valores[8] = entre[0]
                            valores[9] = " ".join(entre[1:])
                        else:
                            valores[8] = ""
                            valores[9] = " ".join(entre)
                    else:
                        valores[4] = parts[0]
                        for offset, valor in enumerate(parts[1:8]):
                            valores[5 + offset] = valor
                else:
                    valores[4] = parts[0]
                    for offset, valor in enumerate(parts[1:8]):
                        valores[5 + offset] = valor

            valores = (valores + [""] * 15)[:15]

        (
            o_pr, lote, pf_l, bit_l, aco, pf, ac, bit_, tol,
            cliente, qtde, prazo, pcp, status_coluna, observacoes,
        ) = valores[:15]

        observacoes = limpar_texto(observacoes)
        if not observacoes and observacao_celula_original:
            observacoes = limpar_texto(observacao_celula_original)

        padrao_data_observacao = re.match(r"^(\d{2}/\d{2}/\d{4})(?:\s+(.*))?$", observacoes)
        if padrao_data_observacao:
            data_obs = padrao_data_observacao.group(1)
            resto_obs = limpar_texto(padrao_data_observacao.group(2) or "")
            if not re.fullmatch(r"\d{2}/\d{2}/\d{4}", limpar_texto(prazo)):
                prazo = data_obs
            observacoes = resto_obs

        if not observacoes and len(celulas) > 15:
            observacoes = limpar_texto(
                " ".join(
                    limpar_texto(c.get_text(" ", strip=True))
                    for c in celulas[15:] if limpar_texto(c.get_text(" ", strip=True))
                )
            )

        if not observacoes:
            raw_tr = str(tr)
            encontrados_obs = re.findall(
                r'<th[^>]*\bwidth\s*=\s*["\']?120["\']?[^>]*>(.*?)</th>',
                raw_tr, flags=re.IGNORECASE | re.DOTALL,
            )
            if encontrados_obs:
                observacoes = limpar_texto(
                    BeautifulSoup(encontrados_obs[-1], "html.parser").get_text(" ", strip=True)
                )

        qtde_limpa = limpar_texto(qtde)
        qtde_numero = re.sub(r"[^\d]", "", qtde_limpa)
        qtde_num = int(qtde_numero) if qtde_numero else 0

        if not status_txt and status_coluna:
            status_txt = limpar_texto(status_coluna)
            status_cls = classe_status_producao(status_txt)

        registros.append({
            "O.Pr.": limpar_texto(o_pr),
            "Lote": str(limpar_texto(lote)),
            "Pf.L": limpar_texto(pf_l),
            "Bit.L": limpar_texto(bit_l),
            "Aço": limpar_texto(aco),
            "Pf": limpar_texto(pf),
            "Ac": limpar_texto(ac),
            "Bit.": limpar_texto(bit_),
            "Tol.": limpar_texto(tol),
            "Cliente": limpar_texto(cliente),
            "Qtde": limpar_texto(qtde),
            "Prazo Dado": limpar_texto(prazo),
            "P.C.P": "",
            "Status": status_txt,
            "StatusClasse": status_cls,
            "Observações": limpar_texto(observacoes),
            "QtdeNum": qtde_num,
        })

    print(f"   Registros aproveitados: {len(registros)}")
    return registros


def gerar_linha_producao(r):
    status_html = (
        f'<span class="st {r["StatusClasse"]}">{escape(r["Status"])}</span>'
        if r["Status"] else ""
    )

    return f"""<tr data-status="{escape(r['Status'])}" data-qtde="{r['QtdeNum']}" data-prazo="{escape(r['Prazo Dado'] or '')}">
<td>{escape(r['O.Pr.'] or '')}</td><td>{escape(formatar_lote_exibicao(r['Lote']))}</td><td>{escape(r['Pf.L'] or '')}</td><td>{escape(r['Bit.L'] or '')}</td>
<td>{escape(r['Aço'] or '')}</td><td>{escape(r['Pf'] or '')}</td><td>{escape(r['Ac'] or '')}</td><td>{escape(r['Bit.'] or '')}</td>
<td>{escape(r['Tol.'] or '')}</td><td>{escape(r['Cliente'] or '')}</td><td>{escape(r['Qtde'] or '')}</td><td class="col-prazo">{escape(r['Prazo Dado'] or '')}</td>
<td>{escape(r['P.C.P'] or '')}</td><td data-s="{escape(r['Status'])}">{status_html}</td><td>{escape(r['Observações'] or '')}</td>
</tr>"""


def chave_cliente(valor):
    valor = normalizar_texto(valor)
    return re.sub(r"[^A-Z0-9]", "", valor)


def obter_links_estoque_producao(registros, titulo_pagina=""):
    clientes_presentes = {
        chave_cliente(r.get("Cliente", ""))
        for r in registros if limpar_texto(r.get("Cliente", ""))
    }
    encontrados = []

    for chave, (nome, arquivo) in ARQUIVOS_ESTOQUE_CLIENTES.items():
        chave_normalizada = chave_cliente(chave)
        cliente_identificado = any(
            cliente == chave_normalizada or cliente.startswith(chave_normalizada) or chave_normalizada in cliente
            for cliente in clientes_presentes
        )

        titulo_normalizado = chave_cliente(titulo_pagina)
        if chave_normalizada == "ACOFORTE" and titulo_normalizado.startswith("ACOFORTE"):
            cliente_identificado = True

        if cliente_identificado:
            encontrados.append((nome, arquivo))

    return encontrados


def gerar_botoes_estoque_producao(registros, titulo_pagina="", caminho_origem=None):
    if caminho_origem and Path(caminho_origem).stem.lower() == DIRETORIA_STEM:
        return '<a class="btn-estoque" href="estoquelam.htm" target="_blank" rel="noopener noreferrer">📦 Estoque Geral</a>'

    botoes = []
    for nome, url in obter_links_estoque_producao(registros, titulo_pagina):
        botoes.append(
            f'<a class="btn-estoque" href="{escape(url, quote=True)}" '
            f'target="_blank" rel="noopener noreferrer">📦 Estoque — {escape(nome)}</a>'
        )
    return "".join(botoes)


def gerar_html_producao(titulo, data, registros, caminho_origem=None):
    linhas = "\n".join(gerar_linha_producao(r) for r in registros)

    def formatar_header_producao(h):
        quebras = {
            "Bitola Laminado": "Bitola<br>Laminado",
            "Bitola Final": "Bitola<br>Final",
            "Status do Processo": "Status do<br>Processo",
            "Prazo Dado": "Prazo<br>Dado",
        }
        return quebras.get(h, escape(h))

    headers_html = "".join(f'<th>{formatar_header_producao(h)}</th>' for h in HEADERS_PRODUCAO)
    botoes_estoque = gerar_botoes_estoque_producao(registros, titulo, caminho_origem)

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
.head,.box,.card,.dash-card{{background:white;border-radius:12px;box-shadow:0 4px 18px #0001}}
.head{{padding:18px 20px;margin-bottom:14px}}
.brand{{display:flex;align-items:center;gap:14px;margin-bottom:10px}}
.brand-logo{{width:58px;height:58px;object-fit:contain;display:block}}
.brand-text{{display:flex;flex-direction:column;justify-content:center;line-height:1.15}}
.brand-name{{display:block;color:#20208f;font-size:22px;font-weight:bold;letter-spacing:1px}}
.brand-subtitle{{display:block;color:#f58200;font-size:12px;font-weight:bold;letter-spacing:.35px;margin-top:4px}}
.head h1{{margin:0;color:#176b28;font-size:28px;line-height:1.15}}
.head small{{color:#667}}

/* STYLES DO DASHBOARD */
.dash-container{{margin-bottom:14px}}
.dash-kpis{{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:12px;margin-bottom:14px}}
.dash-card{{padding:16px;border-left:5px solid #176b28;display:flex;flex-direction:column;justify-content:center}}
.dash-card small{{color:#556;font-size:12px;font-weight:bold;text-transform:uppercase;letter-spacing:0.5px}}
.dash-card b{{font-size:24px;color:#176b28;margin-top:6px;font-weight:bold;line-height:1.2}}
.dash-card-atraso{{border-left-color:#dc2626 !important;background:#fff5f5}}
.dash-card-atraso b{{color:#dc2626 !important}}

.dash-status-section{{background:white;border-radius:12px;box-shadow:0 4px 18px #0001;padding:18px;margin-bottom:14px}}
.dash-status-title{{font-size:15px;font-weight:bold;color:#176b28;margin-bottom:12px;text-transform:uppercase;letter-spacing:0.5px}}
.dash-grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:12px}}

.dash-status-item{{
    background:#f8faf8;
    padding:10px 12px;
    border-radius:8px;
    border:1px solid #e1e6e2;
    cursor:pointer;
    transition:all 0.2s ease;
    user-select:none;
}}
.dash-status-item:hover{{
    background:#eaffea;
    border-color:#176b28;
    transform:translateY(-2px);
    box-shadow:0 4px 10px #0001;
}}
.dash-status-item:active{{
    transform:translateY(0);
}}

.dash-status-head{{display:flex;justify-content:space-between;align-items:center;margin-bottom:6px;font-size:13px}}
.dash-status-name{{font-weight:bold;display:flex;align-items:center;gap:6px}}
.dash-status-metrics{{color:#445;font-weight:bold}}
.dash-progress-bg{{height:8px;background:#e2e8e3;border-radius:4px;overflow:hidden}}
.dash-progress-bar{{height:100%;background:#176b28;width:0%;transition:width 0.3s ease}}

.controls{{display:flex;gap:8px;flex-wrap:wrap;margin-top:14px;align-items:center}}
.controls input,.controls select,.controls button{{padding:10px;border:1px solid #d8e0da;border-radius:8px;background:white;font-size:14px}}
.controls input[type="text"]{{flex:1;min-width:200px}}
.controls input[type="date"]{{min-width:130px;color:#333;font-weight:bold;font-family:inherit}}
.controls button,.controls .btn-estoque{{background:#176b28;color:white;cursor:pointer;border:none;font-weight:bold;padding:10px 20px;border-radius:8px;font-size:15px;box-sizing:border-box;font-family:inherit}}
.controls button:hover,.controls .btn-estoque:hover{{background:#135620}}
.controls .btn-estoque{{display:inline-flex;align-items:center;justify-content:center;text-decoration:none;white-space:nowrap}}
.date-filter-group{{display:inline-flex;align-items:center;gap:6px;background:#eaffea;padding:4px 8px;border-radius:8px;border:1px solid #cce8d0}}
.date-filter-group span{{font-size:12px;font-weight:bold;color:#176b28}}

.box{{overflow:hidden}}
.scroll{{overflow-x:auto}}
table{{width:100%;min-width:1450px;border-collapse:collapse;text-align:center}}

/* TODAS AS CÉLULAS DA TABELA EM NEGRITO */
th,td{{padding:12px;border-bottom:1px solid #e1e6e2;white-space:nowrap;font-weight:bold;}}
th{{background:#eaffea;color:#155c22;cursor:pointer;position:relative;font-weight:bold}}
tr:hover td{{background:#f4fff4}}
#stickyHeader{{display:none;position:fixed;top:0;z-index:1000;overflow:hidden;background:white;box-shadow:0 3px 10px #0002}}
#stickyHeader table{{margin:0;border-collapse:collapse;table-layout:auto}}
#stickyHeader th{{background:#eaffea;color:#155c22;cursor:pointer;white-space:nowrap}}

/* DESTAQUE APENAS PARA O PRAZO DA LINHA EM ATRASO */
tr.linha-atrasada td.col-prazo {{
    color: #dc2626 !important;
    background-color: #fee2e2 !important;
    border-radius: 4px;
}}
.st-atraso {{
    background: #fee2e2;
    color: #991b1b;
    border: 1px solid #fca5a5;
}}

.st{{padding:6px 12px;border-radius:20px;font-weight:bold;font-size:12px;display:inline-block}}
.lib{{background:#dcfce7;color:#166534}}
.sep{{background:#fef3c7;color:#92400e}}
.pon{{background:#dbeafe;color:#1e40af}}
.agu{{background:#fde68a;color:#92400e}}
.dec{{background:#fecaca;color:#991b1b}}
.ser{{background:#fed7aa;color:#92400e}}
.tre{{background:#c7d2fe;color:#1e40af}}
.end{{background:#e0f2fe;color:#0c4a6e}}
.esp{{background:#f3e8ff;color:#6b21a8}}

.summary{{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:12px;margin-top:14px}}
.card{{padding:15px;text-align:center}}
.card small{{color:#667;font-size:12px;display:block}}
.card b{{display:block;font-size:22px;margin-top:8px;color:#176b28;font-weight:bold}}
.btn-print{{background:#176b28 !important;color:white !important}}

@media print{{
@page{{size:A4 landscape;margin:8mm}}
html,body{{background:white !important;margin:0 !important;padding:0 !important}}
body{{font-size:8pt}}
.wrap{{max-width:none;margin:0;padding:0}}
.controls-box,#stickyHeader,.dash-container{{display:none !important}}
.box{{box-shadow:none;border-radius:0;overflow:visible !important}}
.scroll{{overflow:visible !important}}
table{{width:100%;min-width:0;font-size:7pt}}
th,td{{padding:4px 3px}}
th{{position:static !important;cursor:default}}
.summary{{display:none !important}}
tr[hidden]{{display:none !important}}
}}
</style>
</head>
<body>
<div class="wrap">
<div class="head">
    <div class="brand">
        <img class="brand-logo" src="logo_embo_new.png" alt="Logo EMBRACO">
        <div class="brand-text">
            <strong class="brand-name">SIAPE</strong>
            <span class="brand-subtitle">Sistema Integrado de Acompanhamento de Produção EMBRACO</span>
        </div>
    </div>
<h1>{escape(titulo)}</h1>
<small>Listagem atualizada em {escape(data)}</small>
</div>

<!-- DASHBOARD DE INDICADORES -->
<div class="dash-container" id="dashContainer">
    <div class="dash-kpis">
        <div class="dash-card"><small>Total de Ordens</small><b id="dashOrdens">0</b></div>
        <div class="dash-card"><small>Total em KG</small><b id="dashKg">0 KG</b></div>
        <div class="dash-card"><small>Em Produção</small><b id="dashEmProd">0 KG</b></div>
        <div class="dash-card"><small>Prontos p/ Retirada</small><b id="dashProntos">0 KG</b></div>
        <div class="dash-card"><small>Aguardando Separação</small><b id="dashAguardando">0 KG</b></div>
        <div class="dash-card dash-card-atraso"><small>⚠️ Em Atraso</small><b id="dashAtrasados">0 KG</b></div>
    </div>

    <div class="dash-status-section">
        <div class="dash-status-title">Resumo por Status (Clique para filtrar)</div>
        <div class="dash-grid" id="dashStatusGrid">
            <!-- Gerado Dinamicamente via JS -->
        </div>
    </div>
</div>

<div class="box controls-box" style="padding:14px;margin-bottom:14px">
<div class="controls">
<input id="q" type="text" placeholder="🔎 Pesquisar em todas as colunas">
<select id="st">
<option value="">Todos os status</option>
<option value="ATRASADO">⚠️ EM ATRASO</option>
<option>LIBERADO</option>
<option>SEPARADO</option>
<option>PONTEADO</option>
<option>AGUARDANDO SEPARAÇÃO</option>
<option>DECAPADO</option>
<option>SERRADO</option>
<option>TREFILADO</option>
<option>ENDIREITADO</option>
<option>ESPECIAL</option>
</select>

<!-- FILTRO POR DATA INICIAL E FINAL -->
<div class="date-filter-group">
    <span>De:</span>
    <input type="date" id="dtIni" title="Data Inicial Prazo">
    <span>Até:</span>
    <input type="date" id="dtFin" title="Data Final Prazo">
</div>

<button onclick="clearF()">Limpar filtros</button>
<button onclick="csv()">Exportar CSV</button>
<button type="button" class="btn-print" onclick="window.print()">🖨️ Imprimir / PDF</button>
{botoes_estoque}
</div>
</div>

<div class="box">
<div class="scroll" id="tableScroll">
<table id="t">
<thead><tr>{headers_html}</tr></thead>
<tbody>
{linhas}
</tbody>
</table>
</div>
<div style="padding:10px;color:#667" id="count">{len(registros)} registros exibidos</div>
</div>
<div id="stickyHeader" aria-hidden="true"></div>

<div class="summary" id="summary">
<div class="card"><small>Total em processamento</small><b id="total">0 KG</b></div>
<div class="card"><small>Prontos para retirada</small><b id="prontos">0 KG</b></div>
</div>
</div>

<script>
const q = document.querySelector('#q');
const st = document.querySelector('#st');
const dtIni = document.querySelector('#dtIni');
const dtFin = document.querySelector('#dtFin');
const rows = [...document.querySelectorAll('#t tbody tr')];

const ALL_STATUSES = [
    {{ name: "EM ATRASO", cls: "st-atraso", key: "ATRASADO" }},
    {{ name: "LIBERADO", cls: "lib", key: "LIBERADO" }},
    {{ name: "SEPARADO", cls: "sep", key: "SEPARADO" }},
    {{ name: "PONTEADO", cls: "pon", key: "PONTEADO" }},
    {{ name: "AGUARDANDO SEPARAÇÃO", cls: "agu", key: "AGUARDANDO SEPARAÇÃO" }},
    {{ name: "DECAPADO", cls: "dec", key: "DECAPADO" }},
    {{ name: "SERRADO", cls: "ser", key: "SERRADO" }},
    {{ name: "TREFILADO", cls: "tre", key: "TREFILADO" }},
    {{ name: "ENDIREITADO", cls: "end", key: "ENDIREITADO" }},
    {{ name: "ESPECIAL", cls: "esp", key: "ESPECIAL" }}
];

function fmt(v) {{ return Math.round(v).toLocaleString('pt-BR') + ' KG'; }}

// LÓGICA DE DETECÇÃO DE ATRASO
const hoje = new Date();
hoje.setHours(0, 0, 0, 0);

function parseDataPtBr(dtStr) {{
    if (!dtStr) return null;
    const partes = dtStr.trim().split('/');
    if (partes.length === 3) {{
        const d = new Date(partes[2], partes[1] - 1, partes[0]);
        d.setHours(0, 0, 0, 0);
        return d;
    }}
    return null;
}}

function verificarEmarcarAtrasos() {{
    rows.forEach(r => {{
        const prazoTxt = (r.dataset.prazo || "").trim();
        const status = r.dataset.status || "";

        if (prazoTxt && status !== "LIBERADO") {{
            const dataPrazo = parseDataPtBr(prazoTxt);
            if (dataPrazo && dataPrazo < hoje) {{
                r.classList.add('linha-atrasada');
                r.dataset.atrasado = "true";
            }}
        }}
    }});
}}

function filtrarPorStatus(nomeStatus) {{
    const selectStatus = document.querySelector('#st');
    if (selectStatus) {{
        selectStatus.value = nomeStatus;
        applyFilters();
        document.querySelector('.controls-box').scrollIntoView({{ behavior: 'smooth' }});
    }}
}}

function updateDashboard(visibleRows) {{
    let totalOrdens = visibleRows.length;
    let totalKg = 0;
    let prontosKg = 0;
    let aguardandoKg = 0;
    let atrasadosKg = 0;

    const statusCounts = {{}};
    const statusKg = {{}};

    ALL_STATUSES.forEach(s => {{
        statusCounts[s.name] = 0;
        statusKg[s.name] = 0;
    }});

    visibleRows.forEach(r => {{
        const qtde = Number(r.dataset.qtde || 0);
        const status = r.dataset.status || "";
        const ehAtrasado = r.dataset.atrasado === "true";

        totalKg += qtde;

        if (status === "LIBERADO") {{
            prontosKg += qtde;
        }} else if (status === "AGUARDANDO SEPARAÇÃO") {{
            aguardandoKg += qtde;
        }}

        if (ehAtrasado) {{
            atrasadosKg += qtde;
            statusCounts["EM ATRASO"]++;
            statusKg["EM ATRASO"] += qtde;
        }}

        if (statusCounts[status] !== undefined) {{
            statusCounts[status]++;
            statusKg[status] += qtde;
        }}
    }});

    const emProdKg = totalKg - prontosKg;

    document.querySelector('#dashOrdens').textContent = totalOrdens.toLocaleString('pt-BR');
    document.querySelector('#dashKg').textContent = fmt(totalKg);
    document.querySelector('#dashEmProd').textContent = fmt(emProdKg);
    document.querySelector('#dashProntos').textContent = fmt(prontosKg);
    document.querySelector('#dashAguardando').textContent = fmt(aguardandoKg);
    document.querySelector('#dashAtrasados').textContent = fmt(atrasadosKg);

    const grid = document.querySelector('#dashStatusGrid');
    grid.innerHTML = '';

    ALL_STATUSES.forEach(s => {{
        const count = statusCounts[s.name] || 0;
        const kg = statusKg[s.name] || 0;
        const pct = totalKg > 0 ? ((kg / totalKg) * 100).toFixed(1) : "0.0";

        const item = document.createElement('div');
        item.className = 'dash-status-item';
        item.onclick = () => filtrarPorStatus(s.key);

        item.innerHTML = `
            <div class="dash-status-head">
                <span class="dash-status-name">
                    <span class="st ${{s.cls}}" style="padding:2px 8px;font-size:10px;">${{s.name}}</span>
                </span>
                <span class="dash-status-metrics">${{count}} ordens | ${{fmt(kg)}} (${{pct}}%)</span>
            </div>
            <div class="dash-progress-bg">
                <div class="dash-progress-bar" style="width: ${{pct}}%;"></div>
            </div>
        `;
        grid.appendChild(item);
    }});
}}

function updateSummary() {{
    const visible = rows.filter(r => !r.hidden);
    let total = 0;
    let prontos = 0;

    visible.forEach(r => {{
        const qtde = Number(r.dataset.qtde || 0);
        total += qtde;
        if (r.dataset.status === "LIBERADO") {{
            prontos += qtde;
        }}
    }});

    document.querySelector('#total').textContent = fmt(total);
    document.querySelector('#prontos').textContent = fmt(prontos);

    updateDashboard(visible);
}}

function applyFilters() {{
    const texto = q.value.toLowerCase().trim();
    const status = st.value;

    const valIni = dtIni.value ? new Date(dtIni.value + 'T00:00:00') : null;
    const valFin = dtFin.value ? new Date(dtFin.value + 'T23:59:59') : null;

    let count = 0;

    rows.forEach(r => {{
        const textoLinha = r.innerText.toLowerCase();
        const statusLinha = r.dataset.status || "";
        const ehAtrasado = r.dataset.atrasado === "true";
        const prazoTxt = r.dataset.prazo || "";
        const dtPrazo = parseDataPtBr(prazoTxt);

        const passaTexto = !texto || textoLinha.includes(texto);
        let passaStatus = !status || statusLinha === status;

        if (status === "ATRASADO") {{
            passaStatus = ehAtrasado;
        }}

        let passaData = true;
        if (valIni || valFin) {{
            if (!dtPrazo) {{
                passaData = false;
            }} else {{
                if (valIni && dtPrazo < valIni) passaData = false;
                if (valFin && dtPrazo > valFin) passaData = false;
            }}
        }}

        const mostrar = passaTexto && passaStatus && passaData;

        r.hidden = !mostrar;
        if (mostrar) count++;
    }});

    document.querySelector('#count').textContent = count + " registros exibidos";
    updateSummary();
}}

function clearF() {{
    q.value = "";
    st.value = "";
    dtIni.value = "";
    dtFin.value = "";
    applyFilters();
}}

q.addEventListener('input', applyFilters);
st.addEventListener('change', applyFilters);
dtIni.addEventListener('change', applyFilters);
dtFin.addEventListener('change', applyFilters);

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

const tableScroll = document.getElementById("tableScroll");
const table = document.getElementById("t");
const stickyHeader = document.getElementById("stickyHeader");
let stickyTable = null;

function atualizarCabecalhoFixo() {{
    if (!table || !tableScroll || !stickyHeader) return;
    const tableRect = table.getBoundingClientRect();
    const scrollRect = tableScroll.getBoundingClientRect();
    const headerHeight = table.tHead ? table.tHead.getBoundingClientRect().height : 0;
    const deveMostrar = tableRect.top < 0 && tableRect.bottom > headerHeight;
    if (!deveMostrar) {{ stickyHeader.style.display = "none"; return; }}
    if (!stickyTable) {{
        stickyTable = table.cloneNode(false);
        stickyTable.appendChild(table.tHead.cloneNode(true));
        stickyTable.querySelectorAll("th").forEach((th, i) => {{
            th.addEventListener("click", () => {{
                const original = table.tHead.querySelectorAll("th")[i];
                if (original) original.click();
            }});
        }});
        stickyHeader.appendChild(stickyTable);
    }}
    stickyHeader.style.display = "block";
    stickyHeader.style.left = scrollRect.left + "px";
    stickyHeader.style.width = scrollRect.width + "px";
    stickyHeader.style.height = headerHeight + "px";
    stickyTable.style.width = table.scrollWidth + "px";
    stickyTable.style.transform = "translateX(" + (-tableScroll.scrollLeft) + "px)";
    const originalCells = table.tHead.querySelectorAll("th");
    const stickyCells = stickyTable.querySelectorAll("th");
    originalCells.forEach((cell, i) => {{
        if (stickyCells[i]) {{
            const largura = cell.getBoundingClientRect().width;
            stickyCells[i].style.width = largura + "px";
            stickyCells[i].style.minWidth = largura + "px";
        }}
    }});
}}

window.addEventListener("scroll", atualizarCabecalhoFixo, {{ passive: true }});
window.addEventListener("resize", atualizarCabecalhoFixo);
tableScroll.addEventListener("scroll", atualizarCabecalhoFixo, {{ passive: true }});

verificarEmarcarAtrasos();
applyFilters();
atualizarCabecalhoFixo();
</script>
</body>
</html>"""


def processar_arquivo_producao(caminho_origem, caminho_destino):
    print()
    print("=" * 80)
    print(f"[PRODUÇÃO] Processando: {caminho_origem.name}")
    print("=" * 80)

    texto = ler_arquivo(caminho_origem)
    titulo = extrair_titulo_do_nome_arquivo(caminho_origem)
    data = extrair_data_producao(texto)
    registros = extrair_registros_producao(texto)

    print(f"Título: {titulo}")
    print(f"✅ Total de registros: {len(registros)}")

    html_final = gerar_html_producao(titulo=titulo, data=data, registros=registros, caminho_origem=caminho_origem)
    caminho_destino.parent.mkdir(parents=True, exist_ok=True)

    with open(caminho_destino, "w", encoding="utf-8") as arquivo:
        arquivo.write(html_final)

    print(f"✅ Arquivo gerado em: {caminho_destino}")


# ============================================================
# EXECUÇÃO PRINCIPAL
# ============================================================

def processar():
    print("=" * 80)
    print("PROCESSAMENTO SIAP V9.0: ESTOQUE GERAL E AJUSTE DE DIRETORIA")
    print("=" * 80)

    if not PASTA_ORIGEM.exists():
        print("❌ Pasta de origem não encontrada:")
        print(PASTA_ORIGEM)
        input("\nPressione ENTER para fechar...")
        return

    print()
    print("🧹 Verificando nomes de arquivos .htm corrompidos...")
    renomeados = renomear_corrompidos(PASTA_ORIGEM)
    print(f"   Arquivos renomeados: {renomeados}")

    if PASTA_DESTINO.exists():
        print()
        print("🗑️ Sobrescrevendo a pasta de destino...")
        shutil.rmtree(PASTA_DESTINO)

    PASTA_DESTINO.mkdir(parents=True, exist_ok=True)

    copiar_logo_embraco()

    todos_arquivos = [a for a in PASTA_ORIGEM.iterdir() if a.is_file()]
    todos_htm = [a for a in todos_arquivos if a.suffix.lower() == ".htm"]

    nomes_estoque_normalizados = {
        normalizar_nome_arquivo(nome): titulo
        for nome, titulo in ARQUIVOS_ESTOQUE.items()
    }

    arquivos_estoque_encontrados = {}
    for arquivo in todos_htm:
        nome_normalizado = normalizar_nome_arquivo(arquivo.name)
        if nome_normalizado in nomes_estoque_normalizados:
            arquivos_estoque_encontrados[nome_normalizado] = arquivo

    processados_estoque = 0
    nao_encontrados_estoque = 0
    processados_producao = 0
    copiados = 0
    erros = 0

    print()
    print("=" * 80)
    print("ETAPA 1 — TRATAMENTO EXCLUSIVO DE ESTOQUE")
    print("=" * 80)

    for nome_exato, titulo in ARQUIVOS_ESTOQUE.items():
        nome_normalizado = normalizar_nome_arquivo(nome_exato)

        if nome_normalizado == "estoquelam":
            arquivo_origem = CAMINHO_ESTOQUELAM_ORIGEM
            arquivo_destino = CAMINHO_ESTOQUELAM_DESTINO
        else:
            arquivo_origem = arquivos_estoque_encontrados.get(nome_normalizado)
            if arquivo_origem is None:
                print()
                print(f"❌ Arquivo de estoque não encontrado: {nome_exato}")
                nao_encontrados_estoque += 1
                continue
            arquivo_destino = PASTA_DESTINO / arquivo_origem.name

        try:
            processar_arquivo_estoque(
                caminho_origem=arquivo_origem,
                caminho_destino=arquivo_destino,
                titulo=titulo,
            )
            processados_estoque += 1
        except Exception as erro:
            erros += 1
            print()
            print(f"❌ Erro ao processar (estoque) {nome_exato}: {erro}")

    print()
    print("=" * 80)
    print("ETAPA 2 — TRATAMENTO DE PRODUÇÃO")
    print("=" * 80)

    for arquivo in todos_htm:
        nome_normalizado = normalizar_nome_arquivo(arquivo.name)

        if nome_normalizado in nomes_estoque_normalizados or nome_normalizado == "estoquelam":
            continue

        arquivo_destino = PASTA_DESTINO / arquivo.name

        try:
            processar_arquivo_producao(
                caminho_origem=arquivo,
                caminho_destino=arquivo_destino,
            )
            processados_producao += 1
        except Exception as erro:
            erros += 1
            print()
            print(f"❌ Erro ao processar (produção) {arquivo.name}: {erro}")

    print()
    print("=" * 80)
    print("ETAPA 3 — CÓPIA DE ARQUIVOS NÃO-.HTM (INTACTOS)")
    print("=" * 80)

    for arquivo in todos_arquivos:
        if arquivo.suffix.lower() == ".htm":
            continue
        if arquivo.name.lower() == NOME_LOGO_EMBRACO.lower():
            continue

        arquivo_destino = PASTA_DESTINO / arquivo.name

        try:
            shutil.copy2(arquivo, arquivo_destino)
            copiados += 1
            print(f"📄 Copiado intacto: {arquivo.name}")
        except Exception as erro:
            erros += 1
            print(f"❌ Erro ao copiar {arquivo.name}: {erro}")

    print()
    print("=" * 80)
    print("PROCESSAMENTO CONCLUÍDO")
    print("=" * 80)
    print(f"✅ Arquivos de ESTOQUE processados: {processados_estoque}")
    print(f"⚠️ Arquivos de ESTOQUE não encontrados: {nao_encontrados_estoque}")
    print(f"✅ Arquivos de PRODUÇÃO processados: {processados_producao}")
    print(f"📄 Arquivos não-.htm copiados intactos: {copiados}")
    print(f"❌ Erros: {erros}")
    print()
    print("📂 Pasta criada/sobrescrita:")
    print(PASTA_DESTINO)

    input("\nPressione ENTER para fechar...")


if __name__ == "__main__":
    processar()
