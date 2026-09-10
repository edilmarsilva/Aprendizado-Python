import re
import shutil
import unicodedata

from datetime import datetime
from html import escape, unescape
from html.parser import HTMLParser
from pathlib import Path

from bs4 import BeautifulSoup

# =========================
# CONFIGURAÇÕES
# =========================

PASTA_ORIGEM = Path(r"C:\FTP")
PASTA_DESTINO = Path(r"C:\FTP 2.0")

# Nomes EXATOS (sem extensão) dos três arquivos com tratamento
# exclusivo de ESTOQUE. Qualquer outro .htm usa o tratamento de
# PRODUÇÃO. Qualquer arquivo que não seja .htm é copiado intacto.
ARQUIVOS_ESTOQUE = {
    "acoforte78788798708972jkjk098080546543211222hkjfk23123k56s5gdj5412kk44k55332kk66h5421k_2":
        "Acoforte - Estoque",

    "acovisa0898095278916771yiuy98978jhgnmbjkhfdahfa98371987132bbnbnbbbb2":
        "Acovisa - Estoque",

    "trefita08972jkjk098080546543211222hkjfk23123k56s5gdj5412kk44k55332kk66h5421k_2":
        "Trefita - Estoque",
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
    "O.Pr.", "Lote", "Pf.L", "Bit.L", "Aço", "Pf", "Ac", "Bit.", "Tol.",
    "Cliente", "Qtde", "Prazo Dado", "P.C.P", "Status", "Observações",
]

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

# ============================================================
# LIMPEZA DE NOMES CORROMPIDOS
# ============================================================

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

    correspondencia = re.match(r"^([A-Za-zÀ-ÖØ-öø-ÿ]+)", nome)

    if correspondencia:
        prefixo = correspondencia.group(1)
        return prefixo[:1].upper() + prefixo[1:].lower()

    return nome if nome else "Relatório"

# ============================================================
# MOTOR 1 — TRATAMENTO EXCLUSIVO DE ESTOQUE
# (Acoforte / Acovisa / Trefita)
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
body{{margin:0;background:#f4f7f5;font:14px Arial;color:#202820}}
.wrap{{max-width:1500px;margin:20px auto;padding:0 12px}}
.head,.box,.card{{background:white;border-radius:12px;box-shadow:0 4px 18px #0001}}
.head{{padding:18px;margin-bottom:14px}}
.head h1{{margin:0;color:#176b28;font-size:28px}}
.head small{{color:#667}}
.controls{{display:flex;gap:8px;flex-wrap:wrap;margin-top:14px}}
.controls input,.controls select,.controls button{{padding:10px;border:1px solid #d8e0da;border-radius:8px;background:white;font-size:14px}}
.controls input{{flex:1;min-width:230px}}
.controls button{{background:#176b28;color:white;cursor:pointer;border:none;font-weight:bold;padding:10px 20px}}
.controls button:hover{{background:#135620}}
.box{{overflow:hidden}}
.scroll{{overflow-x:auto}}
table{{width:100%;border-collapse:collapse;text-align:center}}
th,td{{padding:12px;border-bottom:1px solid #e1e6e2;white-space:nowrap}}
th{{background:#eaffea;color:#155c22;cursor:pointer;position:sticky;top:0;font-weight:bold}}
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

    if padrao:
        return f"{padrao.group(1)} às {padrao.group(2)}"

    return "Data não disponível"

def conteudo_celula_completo(celula):
    """
    Extrai o conteúdo de uma célula mesmo quando a informação não está
    disponível como texto normal. Alguns relatórios antigos colocam
    observações em IMG/GIF, ALT, TITLE, VALUE ou até no caminho do arquivo.
    """
    partes = []

    texto = limpar_texto(celula.get_text(" ", strip=True))
    if texto:
        partes.append(texto)

    for tag in celula.find_all(True):
        for atributo in ("alt", "title", "value", "src", "data-original", "data-src"):
            valor = limpar_texto(tag.get(atributo, ""))
            if valor:
                partes.append(valor)

        # Alguns HTMLs antigos guardam a imagem em background-image.
        estilo = limpar_texto(tag.get("style", ""))
        if estilo and "background" in normalizar_texto(estilo):
            partes.append(estilo)

    # Também considera atributos da própria célula.
    for atributo in ("alt", "title", "value", "src", "data-original", "data-src"):
        valor = limpar_texto(celula.get(atributo, ""))
        if valor:
            partes.append(valor)

    # Remove duplicidades preservando a ordem.
    return " ".join(dict.fromkeys(partes))


def status_da_imagem(src, alt="", title=""):
    """
    Identifica o status a partir do nome/caminho da imagem GIF, ALT ou TITLE.

    Alguns relatórios antigos usam uma imagem com nome/texto semelhante a
    "Aguarda Separação Lam". Mesmo que o GIF esteja corrompido ou o texto
    visível não seja extraído pelo BeautifulSoup, o nome do arquivo, ALT ou
    TITLE pode preservar a indicação do status.
    """
    texto = " ".join(
        limpar_texto(v) for v in (src, alt, title) if limpar_texto(v)
    )
    up = normalizar_texto(texto)

    if "LIBERADO" in up:
        return "LIBERADO", "lib"
    if "PONTEADO" in up:
        return "PONTEADO", "pon"

    # Variações encontradas em relatórios antigos: "AGUARDA",
    # "AGUARDANDO", "AGUARDA SEPARACAO", "AGUARDA SEPARAÇÃO LAM", etc.
    # Todas devem resultar no mesmo status usado no filtro da página.
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
    if "AGUARDANDO SEPARACAO" in valor:
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
    """
    Confirma se a linha realmente contém um registro de produção.
    Impede que linhas do menu, cabeçalhos ou textos auxiliares
    sejam transformados em registros.
    """

    if len(valores) < 5: # Precisa ter pelo menos as 5 primeiras colunas para ser um registro válido
        return False

    valores_limpos = [limpar_texto(valor) for valor in valores]

    # Ignora linha completamente vazia
    if not any(valores_limpos):
        return False

    texto_linha = normalizar_texto(" ".join(valores_limpos))

    # Palavras comuns encontradas em menus e cabeçalhos
    palavras_invalidas = {
        "MENU",
        "INICIO",
        "INÍCIO",
        "SAIR",
        "VOLTAR",
        "RELATORIO",
        "RELATORIO DE PRODUCAO",
        "PRODUCAO",
        "ORDEM DE PRODUCAO",
        "O.PR.",
        "LOTE",
        "ACO",
        "STATUS",
        "OBSERVACOES",
        "PF.L",
        "BIT.L",
        "PF",
        "AC",
        "BIT.",
        "TOL.",
        "CLIENTE",
        "QTDE",
        "PRAZO DADO",
        "P.C.P",
    }

    # Se a linha inteira (ou uma parte significativa) for uma palavra inválida, descarta
    if texto_linha in palavras_invalidas:
        return False

    # Impede que uma linha cujo primeiro campo seja claramente um menu ou cabeçalho
    # seja aceita como registro.
    primeiro = normalizar_texto(valores_limpos[0])

    if primeiro in palavras_invalidas:
        return False

    # A Ordem de Produção (primeira coluna) deve conter apenas números e ter pelo menos 4 dígitos.
    ordem_producao = re.sub(r"\s+", "", valores_limpos[0])
    if not re.fullmatch(r"\d{4,}", ordem_producao):
        return False

    # O Lote (segunda coluna) também deve ser numérico e ter pelo menos 4 dígitos.
    lote = re.sub(r"\s+", "", valores_limpos[1])
    if not re.fullmatch(r"\d{4,}", lote):
        return False

    # Pelo menos uma das colunas Pf.L, Bit.L ou Aço deve estar preenchida.
    if not (valores_limpos[2] or valores_limpos[3] or valores_limpos[4]):
        return False

    return True

def extrair_registros_producao(html_bruto):
    """
    Extrai os registros da tabela de produção.
    Ajustado para redistribuir conteúdo da coluna 'Aço' se houver concatenação
    e para filtrar linhas inválidas.
    """

    soup = BeautifulSoup(html_bruto, "html.parser")
    linhas_tr = soup.find_all("tr")

    print(f"   Linhas <tr> identificadas: {len(linhas_tr)}")

    registros = []

    for tr in linhas_tr:
        # Primeiro tenta somente as células diretas da linha.
        celulas = tr.find_all(["th", "td"], recursive=False)

        # Fallback para alguns HTML antigos que possuem <td> aninhado.
        # Se a primeira tentativa não encontrar células suficientes, tenta recursivamente.
        # Um registro válido precisa de pelo menos 5 colunas (O.Pr. a Aço).
        if len(celulas) < 5:
            celulas = tr.find_all(["th", "td"], recursive=True)

        # Extrai os valores das células. Para a observação, não usamos
        # somente get_text(), pois relatórios antigos podem guardar a
        # informação em IMG/GIF, ALT, TITLE, VALUE, SRC ou background-image.
        valores = [limpar_texto(celula.get_text(" ", strip=True)) for celula in celulas]

        # A 15ª coluna é Observações.
        #
        # ATENÇÃO: os relatórios antigos possuem HTML MALFORMADO: a célula do
        # Status contém <form>/<label>/<img> e, em seguida, abre a célula da
        # Observação sem fechar corretamente a anterior. O BeautifulSoup pode,
        # então, considerar a imagem do Status como parte da 15ª célula.
        #
        # Por isso, para Observações usamos PRIMEIRO somente texto real da
        # célula, ignorando completamente src/alt/title de imagens. Isso evita
        # que "SEPARADO.GIF", "endireitado.GIF", etc. sejam anexados à
        # Observação.
        observacao_celula_original = ""
        if len(celulas) >= 15:
            # PRIMEIRA tentativa: recupera a observação diretamente do HTML
            # bruto da <tr>. Nos arquivos antigos, a marcação é inválida e o
            # BeautifulSoup pode aninhar a célula da observação dentro da
            # célula do Status. O padrão width="120" identifica a célula real
            # de Observações nesses relatórios.
            raw_tr = str(tr)
            encontrados_obs = re.findall(
                r'<th[^>]*\bwidth\s*=\s*["\']?120["\']?[^>]*>(.*?)</th>',
                raw_tr,
                flags=re.IGNORECASE | re.DOTALL,
            )
            if encontrados_obs:
                observacao_celula_original = limpar_texto(
                    BeautifulSoup(encontrados_obs[-1], "html.parser").get_text(
                        " ", strip=True
                    )
                )

            # SEGUNDA tentativa: texto da 15ª célula, sem atributos de imagem.
            if not observacao_celula_original:
                observacao_celula_original = limpar_texto(
                    celulas[14].get_text(" ", strip=True)
                )

            # TERCEIRA tentativa: nós textuais da própria célula.
            if not observacao_celula_original:
                textos = []
                for no in celulas[14].find_all(string=True):
                    texto_no = limpar_texto(str(no))
                    if texto_no:
                        textos.append(texto_no)
                observacao_celula_original = " ".join(dict.fromkeys(textos))

        # Filtra linhas que não são registros de produção válidos
        if not linha_eh_registro_producao(valores):
            continue

        # Procura o status somente pelas imagens da linha.
        status_txt = ""
        status_cls = ""

        for img in tr.find_all("img"):
            status_txt, status_cls = status_da_imagem(
                img.get("src", ""),
                img.get("alt", ""),
                img.get("title", ""),
            )
            if status_txt:
                break

        # Garante pelo menos 15 posições, conforme HEADERS_PRODUCAO.
        # Isso é importante para o desempacotamento e para garantir que todas as colunas existam.
        while len(valores) < 15:
            valores.append("")

        # Se houver mais de 15 células, as excedentes pertencem
        # ao conteúdo final da observação.
        if len(valores) > 15:
            observacao_extra = " ".join(
                valor for valor in valores[14:] if valor
            )
            valores = valores[:14] + [observacao_extra]

        # --- TRATAMENTO PARA COLUNAS CONCATENADAS NO CAMPO 'Aço' ---
        # Reconstrói registros concatenados sem deslocar campos quando Aço ou
        # Cliente possuem espaços (ex.: "MR 250", "TENAX 2", "SIMEC 2").
        # Tol. também pode estar vazia e, nesse caso, permanece vazia.
        aco_content_in_cell = limpar_texto(valores[4])

        if aco_content_in_cell and " " in aco_content_in_cell and not any(
            valores[i].strip() for i in range(5, 12)
        ):
            parts = aco_content_in_cell.split()

            def eh_data_pt_br(s):
                return bool(re.fullmatch(r"\d{2}/\d{2}/\d{4}", s))

            def eh_quantidade(s):
                return bool(re.fullmatch(r"\d{1,3}(?:\.\d{3})*|\d+", s))

            def eh_numero_decimal(s):
                return bool(re.fullmatch(r"\d+(?:[.,]\d+)", s))

            def eh_tol(s):
                return bool(
                    re.fullmatch(r"H-\d+(?:[.,]\d+)?", s.upper())
                    or eh_numero_decimal(s)
                )

            def eh_codigo_curto(s):
                return bool(re.fullmatch(r"[A-Za-zÀ-ÿ]{1,4}", s))

            # A estrutura é identificada de trás para frente:
            # Prazo = data; Qtde = número imediatamente anterior à data.
            indice_data = None
            for i in range(len(parts) - 1, -1, -1):
                if eh_data_pt_br(parts[i]):
                    indice_data = i
                    break

            if indice_data is not None and indice_data >= 2:
                valores[11] = parts[indice_data]
                indice_qtde = indice_data - 1

                if eh_quantidade(parts[indice_qtde]):
                    valores[10] = parts[indice_qtde]

                    # Procura Pf + Ac + Bit. A partir daí, tudo antes da
                    # Qtde pertence a Tol. + Cliente.
                    indice_bit = None
                    indice_pf = None
                    for i in range(2, indice_qtde):
                        if (
                            eh_numero_decimal(parts[i])
                            and eh_codigo_curto(parts[i - 1])
                            and eh_codigo_curto(parts[i - 2])
                        ):
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
                            # Não há Tol.: o único campo é Cliente.
                            valores[8] = ""
                            valores[9] = entre[0]
                        elif eh_tol(entre[0]):
                            valores[8] = entre[0]
                            valores[9] = " ".join(entre[1:])
                        else:
                            # Primeiro campo não parece Tol.; portanto todos
                            # os campos formam o Cliente.
                            valores[8] = ""
                            valores[9] = " ".join(entre)
                    else:
                        # Fallback conservador para estruturas não reconhecidas.
                        valores[4] = parts[0]
                        for offset, valor in enumerate(parts[1:8]):
                            valores[5 + offset] = valor
                else:
                    valores[4] = parts[0]
                    for offset, valor in enumerate(parts[1:8]):
                        valores[5 + offset] = valor
            else:
                valores[4] = parts[0]
                for offset, valor in enumerate(parts[1:8]):
                    valores[5 + offset] = valor

            valores = (valores + [""] * 15)[:15]
        # --- FIM DO TRATAMENTO ---

        # Desempacota os valores para as variáveis nomeadas
        (
            o_pr,
            lote,
            pf_l,
            bit_l,
            aco, # Este 'aco' já foi processado pelo bloco acima
            pf,
            ac,
            bit_,
            tol,
            cliente,
            qtde,
            prazo,
            pcp,
            status_coluna,
            observacoes,
        ) = valores[:15]

        # --- TRATAMENTO DA COLUNA OBSERVAÇÕES ---
        # Alguns arquivos antigos colocam a data do Prazo junto com a
        # observação (ex.: "21/08/2026 NF 21982"). A data pertence a
        # "Prazo Dado" e o restante pertence a "Observações".
        # Também preservamos qualquer conteúdo existente nas células
        # posteriores ao Status, evitando que a observação seja perdida.
        observacoes = limpar_texto(observacoes)

        # Se get_text() não encontrou nada, recupera o conteúdo bruto da
        # célula original de Observações (inclusive IMG/GIF e atributos).
        if not observacoes and observacao_celula_original:
            observacoes = limpar_texto(observacao_celula_original)

        padrao_data_observacao = re.match(
            r"^(\d{2}/\d{2}/\d{4})(?:\s+(.*))?$", observacoes
        )
        if padrao_data_observacao:
            data_obs = padrao_data_observacao.group(1)
            resto_obs = limpar_texto(padrao_data_observacao.group(2) or "")

            # Só preenche o prazo com a data da observação se ele ainda
            # estiver vazio ou não contiver uma data válida.
            if not re.fullmatch(r"\d{2}/\d{2}/\d{4}", limpar_texto(prazo)):
                prazo = data_obs

            observacoes = resto_obs

        # Se por algum motivo a célula 15 estiver vazia, procura conteúdo
        # de observação nas células excedentes do <tr>.
        if not observacoes and len(celulas) > 15:
            observacoes = limpar_texto(
                " ".join(
                    limpar_texto(c.get_text(" ", strip=True))
                    for c in celulas[15:]
                    if limpar_texto(c.get_text(" ", strip=True))
                )
            )

        # Fallback final: procura novamente a célula width="120" diretamente
        # no HTML da linha. Isso resolve os casos em que o HTML antigo é
        # malformado e a árvore criada pelo BeautifulSoup mistura as células.
        if not observacoes:
            raw_tr = str(tr)
            encontrados_obs = re.findall(
                r'<th[^>]*\bwidth\s*=\s*["\']?120["\']?[^>]*>(.*?)</th>',
                raw_tr,
                flags=re.IGNORECASE | re.DOTALL,
            )
            if encontrados_obs:
                observacoes = limpar_texto(
                    BeautifulSoup(encontrados_obs[-1], "html.parser").get_text(
                        " ", strip=True
                    )
                )
        # --- FIM DO TRATAMENTO DA COLUNA OBSERVAÇÕES ---

        # Quantidade numérica para os totais do rodapé.
        qtde_limpa = limpar_texto(qtde)
        qtde_numero = re.sub(r"[^\d]", "", qtde_limpa)
        qtde_num = int(qtde_numero) if qtde_numero else 0

        # O status encontrado na imagem tem prioridade.
        if not status_txt and status_coluna:
            status_txt = limpar_texto(status_coluna)
            status_cls = classe_status_producao(status_txt)

        registros.append({
            "O.Pr.": limpar_texto(o_pr),
            "Lote": limpar_texto(lote),
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

            # Conforme definido, PCP permanece vazio.
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

    return f"""<tr data-status="{escape(r['Status'])}" data-qtde="{r['QtdeNum']}">
<td>{escape(r['O.Pr.'] or '')}</td><td>{escape(r['Lote'] or '')}</td><td>{escape(r['Pf.L'] or '')}</td><td>{escape(r['Bit.L'] or '')}</td>
<td>{escape(r['Aço'] or '')}</td><td>{escape(r['Pf'] or '')}</td><td>{escape(r['Ac'] or '')}</td><td>{escape(r['Bit.'] or '')}</td>
<td>{escape(r['Tol.'] or '')}</td><td>{escape(r['Cliente'] or '')}</td><td>{escape(r['Qtde'] or '')}</td><td>{escape(r['Prazo Dado'] or '')}</td>
<td>{escape(r['P.C.P'] or '')}</td><td data-s="{escape(r['Status'])}">{status_html}</td><td>{escape(r['Observações'] or '')}</td>
</tr>"""

def gerar_html_producao(titulo, data, registros):
    linhas = "\n".join(gerar_linha_producao(r) for r in registros)
    headers_html = "".join(f"<th>{h}</th>" for h in HEADERS_PRODUCAO)

    return f"""<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{escape(titulo)}</title>
<style>
*{{box-sizing:border-box}}
body{{margin:0;background:#f4f7f5;font:14px Arial;color:#202820}}
.wrap{{max-width:1500px;margin:20px auto;padding:0 12px}}
.head,.box,.card{{background:white;border-radius:12px;box-shadow:0 4px 18px #0001}}
.head{{padding:18px;margin-bottom:14px}}
.head h1{{margin:0;color:#176b28;font-size:28px}}
.head small{{color:#667}}
.controls{{display:flex;gap:8px;flex-wrap:wrap;margin-top:14px}}
.controls input,.controls select,.controls button{{padding:10px;border:1px solid #d8e0da;border-radius:8px;background:white;font-size:14px}}
.controls input{{flex:1;min-width:230px}}
.controls button{{background:#176b28;color:white;cursor:pointer;border:none;font-weight:bold;padding:10px 20px}}
.controls button:hover{{background:#135620}}
.box{{overflow:hidden}}
.scroll{{overflow-x:auto}}
table{{width:100%;border-collapse:collapse;text-align:center}}
th,td{{padding:12px;border-bottom:1px solid #e1e6e2;white-space:nowrap}}
th{{background:#eaffea;color:#155c22;cursor:pointer;position:sticky;top:0;font-weight:bold}}
tr:hover td{{background:#f4fff4}}
.st{{padding:6px 12px;border-radius:20px;font-weight:bold;font-size:12px;display:inline-block}}
.lib{{background:#dcfce7;color:#166534}}
.sep{{background:#fef3c7;color:#92400e}}
.pon{{background:#dbeafe;color:#1e40af}}
.agu{{background:#fde68a;color:#92400e}}
.dec{{background:#fecaca;color:#991b1b}}
.ser{{background:#fed7aa;color:#92400e}}
.tre{{background:#c7d2fe;color:#1e40af}}
.end{{background:#e0f2fe;color:#0c4a6e}} /* Adicionado estilo para Endireitado */
.esp{{background:#f3e8ff;color:#6b21a8}}
.summary{{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:12px;margin-top:14px}}
.card{{padding:15px;text-align:center}}
.card small{{color:#667;font-size:12px;display:block}}
.card b{{display:block;font-size:22px;margin-top:8px;color:#176b28;font-weight:bold}}
</style>
</head>
<body>
<div class="wrap">
<div class="head">
<h1>{escape(titulo)}</h1>
<small>Listagem atualizada em {escape(data)}</small>
</div>

<div class="box" style="padding:14px;margin-bottom:14px">
<div class="controls">
<input id="q" placeholder="🔎 Pesquisar em todas as colunas">
<select id="st">
<option value="">Todos os status</option>
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
<div class="card"><small>Total em processamento</small><b id="total">0 KG</b></div>
<div class="card"><small>Prontos para retirada</small><b id="prontos">0 KG</b></div>
</div>
</div>

<script>
const q = document.querySelector('#q');
const st = document.querySelector('#st');
const rows = [...document.querySelectorAll('#t tbody tr')];

function fmt(v) {{ return Math.round(v).toLocaleString('pt-BR') + ' KG'; }}

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
}}

function applyFilters() {{
    const texto = q.value.toLowerCase().trim();
    const status = st.value;
    let count = 0;

    rows.forEach(r => {{
        const textoLinha = r.innerText.toLowerCase();
        const statusLinha = r.dataset.status || "";
        const passaTexto = !texto || textoLinha.includes(texto);
        const passaStatus = !status || statusLinha === status;
        const mostrar = passaTexto && passaStatus;

        r.hidden = !mostrar;
        if (mostrar) count++;
    }});

    document.querySelector('#count').textContent = count + " registros exibidos";
    updateSummary();
}}

function clearF() {{
    q.value = "";
    st.value = "";
    applyFilters();
}}

q.addEventListener('input', applyFilters);
st.addEventListener('change', applyFilters);

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

updateSummary();
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

    html_final = gerar_html_producao(titulo=titulo, data=data, registros=registros)

    caminho_destino.parent.mkdir(parents=True, exist_ok=True)

    with open(caminho_destino, "w", encoding="utf-8") as arquivo:
        arquivo.write(html_final)

    print(f"✅ Arquivo gerado em: {caminho_destino}")

# ============================================================
# EXECUÇÃO PRINCIPAL
# ============================================================

def processar():
    print("=" * 80)
    print("PROCESSAMENTO: ESTOQUE (3 exclusivos) + PRODUÇÃO (demais .htm) + CÓPIA (outros)")
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
    print("ETAPA 1 — TRATAMENTO EXCLUSIVO DE ESTOQUE (ignorando os demais .htm por enquanto)")
    print("=" * 80)

    for nome_exato, titulo in ARQUIVOS_ESTOQUE.items():
        nome_normalizado = normalizar_nome_arquivo(nome_exato)
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
            print(f"❌ Erro ao processar (estoque) {arquivo_origem.name}: {erro}")

    print()
    print("=" * 80)
    print("ETAPA 2 — TRATAMENTO DE PRODUÇÃO (todos os .htm, exceto os 3 de estoque)")
    print("=" * 80)

    for arquivo in todos_htm:
        nome_normalizado = normalizar_nome_arquivo(arquivo.name)

        if nome_normalizado in nomes_estoque_normalizados:
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
