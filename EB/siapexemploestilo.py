import re
import shutil
import unicodedata

from datetime import datetime
from html import escape, unescape
from html.parser import HTMLParser
from pathlib import Path

from bs4 import BeautifulSoup

# ============================================================
# V8.5 — DASHBOARD E INDICADORES
# ============================================================
# CONFIGURAÇÃO
# ============================================================

PASTA_ORIGEM = Path(r"C:\Users\Fiscal\Desktop\1 XML E PDF EDILMAR\FTP")
PASTA_DESTINO = Path(r"C:\Users\Fiscal\Desktop\1 XML E PDF EDILMAR\FTP 2.0")

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

# Arquivos de ESTOQUE correspondentes a cada cliente.
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

# ============================================================
# FUNÇÕES COMUNS
# ============================================================

def ler_arquivo(caminho):
    codificacoes = ["cp1252", "latin-1", "utf-8"]
    texto = None

    for codificacao in codificacoes:
        try:
            with open(
                caminho,
                "r",
                encoding=codificacao,
                errors="strict",
            ) as arquivo:
                texto = arquivo.read()
            break
        except UnicodeDecodeError:
            texto = None

    if texto is None:
        with open(
            caminho,
            "r",
            encoding="cp1252",
            errors="replace",
        ) as arquivo:
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
    valor = "".join(
        c for c in valor
        if unicodedata.category(c) != "Mn"
    )

    return re.sub(r"\s+", " ", valor).strip()


def normalizar_nome_arquivo(nome):
    return Path(nome).stem.strip().lower()


def converter_numero(valor):
    valor = limpar_texto(valor).upper()
    valor = valor.replace("KGS", "")
    valor = valor.replace("KG", "")
    valor = valor.strip()

    valor = valor.replace(".", "")
    valor = valor.replace(",", "")

    numeros = re.sub(r"[^\d]", "", valor)

    return int(numeros) if numeros else 0


def formatar_kg(valor):
    return f"{int(valor):,}".replace(",", ".") + " KG"


def formatar_lote_exibicao(valor):
    """Remove zeros à esquerda somente na apresentação do Lote."""
    valor = limpar_texto(valor)

    if valor.isdigit():
        return valor.lstrip("0") or "0"

    return valor


# ============================================================
# LIMPEZA DE NOMES CORROMPIDOS
# ============================================================

def limpar_nome_arquivo(nome):
    nome = re.sub(r"[^a-zA-Z0-9._-]", "", nome)
    nome = re.sub(r"\.+", ".", nome)

    return nome if nome else "arquivo.htm"


def renomear_corrompidos(pasta):
    pasta_path = Path(pasta)

    if not pasta_path.exists():
        return 0

    contador = 0

    for item in pasta_path.iterdir():
        if not item.is_file():
            continue

        if item.suffix.lower() != ".htm":
            continue

        nome_limpo = limpar_nome_arquivo(item.name)

        if item.name == nome_limpo:
            continue

        novo = item.parent / nome_limpo

        if novo.exists():
            if "." in nome_limpo:
                base, ext = nome_limpo.rsplit(".", 1)
            else:
                base, ext = nome_limpo, "htm"

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

    # Corrige nomes como Acofortegdg para Acoforte.
    if nome_normalizado.startswith("ACOFORTE"):
        return "Acoforte"

    correspondencia = re.match(
        r"^([A-Za-zÀ-ÖØ-öø-ÿ]+)",
        nome,
    )

    if correspondencia:
        prefixo = correspondencia.group(1)
        return prefixo[:1].upper() + prefixo[1:].lower()

    return nome if nome else "Relatório"


# ============================================================
# MOTOR 1 — TRATAMENTO EXCLUSIVO DE ESTOQUE
# ============================================================

class ParserEstoque(HTMLParser):
    def __init__(self):
        super().__init__()
        self.em_td = False
        self.em_th = False
        self.linha_atual = []
        self.linhas = []
        self.texto_atual = []

    def handle_starttag(self, tag, attrs):
        tag = tag.lower()

        if tag == "tr":
            self.linha_atual = []

        elif tag == "td":
            self.em_td = True
            self.texto_atual = []

        elif tag == "th":
            self.em_th = True
            self.texto_atual = []

    def handle_endtag(self, tag):
        tag = tag.lower()

        if tag in ("td", "th"):
            texto = limpar_texto(" ".join(self.texto_atual))
            self.linha_atual.append(texto)
            self.texto_atual = []
            self.em_td = False
            self.em_th = False

        elif tag == "tr":
            if self.linha_atual:
                self.linhas.append(self.linha_atual)

            self.linha_atual = []

    def handle_data(self, data):
        if self.em_td or self.em_th:
            self.texto_atual.append(data)


def encontrar_tabela_estoque(texto):
    soup = BeautifulSoup(texto, "html.parser")
    tabelas = soup.find_all("table")

    melhor_tabela = None
    melhor_pontuacao = -1

    for tabela in tabelas:
        texto_tabela = normalizar_texto(tabela.get_text(" "))

        pontuacao = 0

        for cabecalho in CABECALHO_NORMALIZADO_ESTOQUE:
            if cabecalho in texto_tabela:
                pontuacao += 1

        if pontuacao > melhor_pontuacao:
            melhor_pontuacao = pontuacao
            melhor_tabela = tabela

    return melhor_tabela


def extrair_registros_estoque(texto, titulo):
    tabela = encontrar_tabela_estoque(texto)

    if tabela is None:
        return []

    registros = []

    linhas = tabela.find_all("tr")

    for linha in linhas:
        celulas = linha.find_all(["td", "th"])

        valores = [
            limpar_texto(celula.get_text(" "))
            for celula in celulas
        ]

        if not valores:
            continue

        normalizados = [
            normalizar_texto(valor)
            for valor in valores
        ]

        if any(
            cabecalho in normalizados
            for cabecalho in CABECALHO_NORMALIZADO_ESTOQUE
        ):
            continue

        if len(valores) < len(COLUNAS_ESTOQUE):
            valores += [""] * (
                len(COLUNAS_ESTOQUE) - len(valores)
            )

        valores = valores[:len(COLUNAS_ESTOQUE)]

        registro = dict(
            zip(COLUNAS_ESTOQUE, valores)
        )

        registro["Cliente"] = (
            registro.get("Cliente")
            or titulo
        )

        registros.append(registro)

    return registros


def gerar_html_estoque(titulo, registros):
    data_atualizacao = datetime.now().strftime(
        "%d/%m/%Y às %H:%M:%S"
    )

    linhas_html = []

    for registro in registros:
        celulas = []

        for coluna in COLUNAS_ESTOQUE:
            valor = registro.get(coluna, "")

            if coluna == "Lote":
                valor = formatar_lote_exibicao(valor)

            celulas.append(
                f"<td>{escape(str(valor))}</td>"
            )

        linhas_html.append(
            "<tr>" + "".join(celulas) + "</tr>"
        )

    tabela_html = "\n".join(linhas_html)

    cabecalho_html = "".join(
        f"<th>{escape(coluna)}</th>"
        for coluna in COLUNAS_ESTOQUE
    )

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
.head,.box{{background:white;border-radius:12px;box-shadow:0 4px 18px #0001}}
.head{{padding:18px 20px;margin-bottom:14px}}
.brand{{display:flex;align-items:center;gap:12px;margin-bottom:10px}}
.brand-mark{{width:38px;height:38px;border-radius:10px;background:#176b28;color:white;display:flex;align-items:center;justify-content:center;font-weight:bold;font-size:18px}}
.brand-text{{font-size:12px;font-weight:bold;letter-spacing:1.2px;color:#176b28;text-transform:uppercase}}
.head h1{{margin:0;color:#176b28;font-size:28px;line-height:1.15}}
.head small{{color:#667}}
.box{{overflow:hidden}}
.scroll{{overflow-x:auto}}
table{{width:100%;min-width:1000px;border-collapse:collapse;text-align:center}}
th,td{{padding:12px;border-bottom:1px solid #e1e6e2;white-space:nowrap}}
th{{background:#eaffea;color:#155c22;font-weight:bold}}
tr:hover td{{background:#f4fff4}}
</style>
</head>
<body>
<div class="wrap">
<div class="head">
<div class="brand">
<div class="brand-mark">P</div>
<div class="brand-text">Portal de Produção</div>
</div>
<h1>{escape(titulo)}</h1>
<small>Listagem atualizada em {data_atualizacao}</small>
</div>

<div class="box">
<div class="scroll">
<table>
<thead>
<tr>{cabecalho_html}</tr>
</thead>
<tbody>
{tabela_html}
</tbody>
</table>
</div>
</div>
</div>
</body>
</html>"""


def processar_arquivo_estoque(
    caminho_origem,
    caminho_destino,
    titulo,
):
    print()
    print("=" * 80)
    print(f"[ESTOQUE] Processando: {caminho_origem.name}")
    print("=" * 80)

    texto = ler_arquivo(caminho_origem)
    registros = extrair_registros_estoque(texto, titulo)

    html_final = gerar_html_estoque(
        titulo=titulo,
        registros=registros,
    )

    caminho_destino.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with open(
        caminho_destino,
        "w",
        encoding="utf-8",
    ) as arquivo:
        arquivo.write(html_final)

    print(f"✅ Registros encontrados: {len(registros)}")
    print(f"✅ Arquivo gerado em: {caminho_destino}")


# ============================================================
# MOTOR 2 — TRATAMENTO DE PRODUÇÃO
# ============================================================

def extrair_data_producao(texto):
    correspondencia = re.search(
        r"(\d{2}/\d{2}/\d{4}).*?(\d{2}:\d{2}:\d{2})",
        texto,
        flags=re.IGNORECASE | re.DOTALL,
    )

    if correspondencia:
        return (
            f"{correspondencia.group(1)} "
            f"às {correspondencia.group(2)}"
        )

    return datetime.now().strftime(
        "%d/%m/%Y às %H:%M:%S"
    )


def localizar_tabela_producao(texto):
    soup = BeautifulSoup(texto, "html.parser")

    tabelas = soup.find_all("table")

    melhor_tabela = None
    melhor_pontuacao = -1

    cabecalhos_procurados = [
        normalizar_texto(cabecalho)
        for cabecalho in HEADERS_PRODUCAO
    ]

    for tabela in tabelas:
        primeira_linha = tabela.find("tr")

        if primeira_linha is None:
            continue

        celulas = primeira_linha.find_all(
            ["td", "th"]
        )

        cabecalhos = [
            normalizar_texto(
                celula.get_text(" ")
            )
            for celula in celulas
        ]

        pontuacao = 0

        for cabecalho in cabecalhos_procurados:
            if cabecalho in cabecalhos:
                pontuacao += 1

        if pontuacao > melhor_pontuacao:
            melhor_pontuacao = pontuacao
            melhor_tabela = tabela

    return melhor_tabela


def extrair_registros_producao(texto):
    tabela = localizar_tabela_producao(texto)

    if tabela is None:
        return []

    registros = []

    linhas = tabela.find_all("tr")

    for linha in linhas:
        celulas = linha.find_all(["td", "th"])

        valores = [
            limpar_texto(celula.get_text(" "))
            for celula in celulas
        ]

        if not valores:
            continue

        normalizados = [
            normalizar_texto(valor)
            for valor in valores
        ]

        if any(
            normalizado in [
                normalizar_texto(cabecalho)
                for cabecalho in HEADERS_PRODUCAO
            ]
            for normalizado in normalizados
        ):
            if any(
                normalizar_texto(cabecalho) in normalizados
                for cabecalho in HEADERS_PRODUCAO
            ):
                continue

        if len(valores) < len(HEADERS_PRODUCAO):
            valores += [""] * (
                len(HEADERS_PRODUCAO) - len(valores)
            )

        valores = valores[:len(HEADERS_PRODUCAO)]

        registro = dict(
            zip(HEADERS_PRODUCAO, valores)
        )

        registro["Qtde_num"] = converter_numero(
            registro.get("Qtde", "")
        )

        registro["Status do Processo"] = normalizar_texto(
            registro.get("Status do Processo", "")
        )

        registros.append(registro)

    return registros


# ============================================================
# HTML DE PRODUÇÃO
# ============================================================

def gerar_html_producao(titulo, data, registros):
    linhas_html = []

    for registro in registros:
        status = normalizar_texto(
            registro.get("Status do Processo", "")
        )

        qtde_num = registro.get("Qtde_num", 0)

        classe_status = {
            "LIBERADO": "lib",
            "SEPARADO": "sep",
            "PONTEADO": "pon",
            "AGUARDANDO SEPARAÇÃO": "agu",
            "DECAPADO": "dec",
            "SERRADO": "ser",
            "TREFILADO": "tre",
            "ENDIREITADO": "end",
            "ESPECIAL": "esp",
        }.get(status, "")

        valores_linha = []

        for cabecalho in HEADERS_PRODUCAO:
            valor = registro.get(cabecalho, "")

            if cabecalho == "Lote":
                valor = formatar_lote_exibicao(valor)

            if cabecalho == "Status do Processo":
                valor = (
                    f'<span class="st {classe_status}">'
                    f"{escape(str(valor))}"
                    "</span>"
                )

            valores_linha.append(
                f"<td>{valor}</td>"
            )

        linhas_html.append(
            "<tr "
            f'data-status="{escape(status)}" '
            f'data-qtde="{qtde_num}">'
            + "".join(valores_linha)
            + "</tr>"
        )

    tabela_html = "\n".join(linhas_html)

    cabecalho_html = "".join(
        f"<th>{escape(cabecalho)}</th>"
        for cabecalho in HEADERS_PRODUCAO
    )

    status_cards = [
        ("lib", "Liberado", "✓"),
        ("sep", "Separado", "⇢"),
        ("pon", "Ponteado", "•"),
        ("agu", "Aguardando separação", "◷"),
        ("dec", "Decapado", "◆"),
        ("ser", "Serrado", "▰"),
        ("tre", "Trefilado", "↗"),
        ("end", "Endireitado", "↔"),
        ("esp", "Especial", "★"),
    ]

    cards_html = []

    for classe, nome, icone in status_cards:
        cards_html.append(
            f"""
<div class="status-card status-{classe}">
    <div class="status-card-top">
        <div class="status-icon">{icone}</div>
        <div class="status-name">{escape(nome)}</div>
    </div>

    <div class="status-card-main">
        <strong id="status-{classe}">0</strong>
        <span>ordens</span>
    </div>

    <div class="status-card-kg">
        <strong id="kg-{classe}">0 KG</strong>
        <span>quantidade</span>
    </div>

    <div class="status-progress">
        <div id="bar-{classe}"></div>
    </div>

    <div class="status-card-percent">
        <span>participação nas ordens</span>
        <strong id="pct-{classe}">0%</strong>
    </div>
</div>
"""
        )

    cards_html = "".join(cards_html)

    return f"""<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{escape(titulo)}</title>

<style>
* {{
    box-sizing: border-box;
}}

body {{
    margin: 0;
    background:
        linear-gradient(180deg, #f3f8f4 0%, #f7faf8 100%);
    font: 15px Arial, sans-serif;
    color: #202820;
}}

.wrap {{
    max-width: 1500px;
    margin: 20px auto;
    padding: 0 12px;
}}

.head,
.box,
.card,
.status-dashboard {{
    background: white;
    border-radius: 14px;
    box-shadow: 0 5px 22px rgba(24, 72, 39, .08);
}}

.head {{
    padding: 20px 22px;
    margin-bottom: 14px;
    border: 1px solid #e6eee8;
}}

.brand {{
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 10px;
}}

.brand-mark {{
    width: 40px;
    height: 40px;
    border-radius: 12px;
    background: #176b28;
    color: white;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: bold;
    font-size: 18px;
    box-shadow: 0 4px 10px rgba(23, 107, 40, .25);
}}

.brand-text {{
    font-size: 12px;
    font-weight: bold;
    letter-spacing: 1.2px;
    color: #176b28;
    text-transform: uppercase;
}}

.head h1 {{
    margin: 0;
    color: #176b28;
    font-size: 28px;
    line-height: 1.15;
}}

.head small {{
    display: block;
    color: #667;
    margin-top: 5px;
}}

.controls {{
    display: flex;
    gap: 8px;
    flex-wrap: wrap;
    margin-top: 14px;
}}

.controls input,
.controls select,
.controls button {{
    padding: 10px;
    border: 1px solid #d8e0da;
    border-radius: 8px;
    background: white;
    font-size: 14px;
}}

.controls input {{
    flex: 1;
    min-width: 230px;
}}

.controls button,
.controls .btn-estoque {{
    background: #176b28;
    color: white;
    cursor: pointer;
    border: none;
    font-weight: bold;
    padding: 10px 20px;
    border-radius: 8px;
    font-size: 15px;
    box-sizing: border-box;
    font-family: inherit;
}}

.controls button:hover,
.controls .btn-estoque:hover {{
    background: #135620;
}}

.controls .btn-estoque {{
    display: inline-flex;
    align-items: center;
    justify-content: center;
    text-decoration: none;
    white-space: nowrap;
}}

.box {{
    overflow: hidden;
    border: 1px solid #e6eee8;
}}

.scroll {{
    overflow-x: auto;
}}

table {{
    width: 100%;
    min-width: 1450px;
    border-collapse: collapse;
    text-align: center;
}}

th,
td {{
    padding: 12px;
    border-bottom: 1px solid #e1e6e2;
    white-space: nowrap;
}}

th {{
    background: #eaffea;
    color: #155c22;
    cursor: pointer;
    position: relative;
    font-weight: bold;
}}

tr:hover td {{
    background: #f4fff4;
}}

#stickyHeader {{
    display: none;
    position: fixed;
    top: 0;
    z-index: 1000;
    overflow: hidden;
    background: white;
    box-shadow: 0 3px 10px #0002;
}}

#stickyHeader table {{
    margin: 0;
    border-collapse: collapse;
    table-layout: auto;
}}

#stickyHeader th {{
    background: #eaffea;
    color: #155c22;
    cursor: pointer;
    white-space: nowrap;
}}

.st {{
    padding: 6px 12px;
    border-radius: 20px;
    font-weight: bold;
    font-size: 12px;
    display: inline-block;
}}

.lib {{
    background: #dcfce7;
    color: #166534;
}}

.sep {{
    background: #fef3c7;
    color: #92400e;
}}

.pon {{
    background: #dbeafe;
    color: #1e40af;
}}

.agu {{
    background: #fde68a;
    color: #92400e;
}}

.dec {{
    background: #fecaca;
    color: #991b1b;
}}

.ser {{
    background: #fed7aa;
    color: #92400e;
}}

.tre {{
    background: #c7d2fe;
    color: #1e40af;
}}

.end {{
    background: #e0f2fe;
    color: #0c4a6e;
}}

.esp {{
    background: #f3e8ff;
    color: #6b21a8;
}}

.summary {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 12px;
    margin-top: 14px;
}}

.card {{
    padding: 16px;
    text-align: center;
    border: 1px solid #e6eee8;
}}

.card small {{
    color: #667;
    font-size: 12px;
    display: block;
}}

.card b {{
    display: block;
    font-size: 22px;
    margin-top: 8px;
    color: #176b28;
    font-weight: bold;
}}

.card.accent {{
    border-top: 4px solid #176b28;
}}

.btn-print {{
    background: #176b28 !important;
    color: white !important;
}}

/* ============================================================
   NOVO RESUMO POR STATUS
   ============================================================ */

.status-dashboard {{
    margin-top: 16px;
    padding: 20px;
    border: 1px solid #e1ebe3;
    overflow: hidden;
}}

.status-dashboard-header {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 20px;
    margin-bottom: 18px;
    padding-bottom: 15px;
    border-bottom: 1px solid #e5ece7;
}}

.dashboard-kicker {{
    color: #559064;
    font-size: 11px;
    font-weight: bold;
    letter-spacing: 1.3px;
    text-transform: uppercase;
    margin-bottom: 5px;
}}

.dashboard-title {{
    color: #174d24;
    font-size: 22px;
    font-weight: bold;
}}

.dashboard-subtitle {{
    color: #718078;
    font-size: 13px;
    margin-top: 4px;
}}

.dashboard-total {{
    min-width: 145px;
    padding: 12px 16px;
    text-align: right;
    border-radius: 12px;
    background: #eff9f1;
    border: 1px solid #d9eddd;
}}

.dashboard-total-label {{
    display: block;
    color: #62806a;
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: .5px;
}}

.dashboard-total strong {{
    display: block;
    color: #176b28;
    font-size: 24px;
    margin-top: 3px;
}}

.status-grid {{
    display: grid;
    grid-template-columns: repeat(3, minmax(0, 1fr));
    gap: 14px;
}}

.status-card {{
    position: relative;
    min-height: 185px;
    padding: 17px;
    overflow: hidden;
    border: 1px solid #e4ebe6;
    border-radius: 14px;
    background: #fff;
    transition:
        transform .18s ease,
        box-shadow .18s ease;
}}

.status-card::before {{
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 5px;
    background: var(--status-color);
}}

.status-card:hover {{
    transform: translateY(-3px);
    box-shadow: 0 8px 22px rgba(30, 80, 43, .13);
}}

.status-card-top {{
    display: flex;
    align-items: center;
    gap: 9px;
    min-height: 29px;
}}

.status-icon {{
    width: 27px;
    height: 27px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 50%;
    color: white;
    background: var(--status-color);
    font-size: 15px;
    font-weight: bold;
}}

.status-name {{
    color: #35443a;
    font-size: 14px;
    font-weight: bold;
    line-height: 1.2;
}}

.status-card-main {{
    display: flex;
    align-items: baseline;
    gap: 8px;
    margin-top: 17px;
}}

.status-card-main strong {{
    color: var(--status-color);
    font-size: 34px;
    line-height: 1;
}}

.status-card-main span {{
    color: #7b877e;
    font-size: 12px;
}}

.status-card-kg {{
    display: flex;
    align-items: baseline;
    gap: 7px;
    margin-top: 10px;
}}

.status-card-kg strong {{
    color: #28372c;
    font-size: 17px;
}}

.status-card-kg span {{
    color: #89938c;
    font-size: 11px;
}}

.status-progress {{
    height: 7px;
    margin-top: 17px;
    overflow: hidden;
    border-radius: 10px;
    background: #edf1ee;
}}

.status-progress div {{
    width: 0;
    height: 100%;
    border-radius: inherit;
    background: var(--status-color);
    transition: width .35s ease;
}}

.status-card-percent {{
    display: flex;
    justify-content: space-between;
    gap: 10px;
    margin-top: 7px;
    color: #89938c;
    font-size: 10px;
}}

.status-card-percent strong {{
    color: var(--status-color);
    font-size: 11px;
}}

.status-lib {{
    --status-color: #16a34a;
    --status-soft: #eaf8ee;
}}

.status-sep {{
    --status-color: #d28a00;
    --status-soft: #fff8e5;
}}

.status-pon {{
    --status-color: #2563eb;
    --status-soft: #edf4ff;
}}

.status-agu {{
    --status-color: #d97706;
    --status-soft: #fff5df;
}}

.status-dec {{
    --status-color: #dc2626;
    --status-soft: #fff0f0;
}}

.status-ser {{
    --status-color: #ea580c;
    --status-soft: #fff1e9;
}}

.status-tre {{
    --status-color: #4f46e5;
    --status-soft: #f0efff;
}}

.status-end {{
    --status-color: #0284c7;
    --status-soft: #ecf8ff;
}}

.status-esp {{
    --status-color: #9333ea;
    --status-soft: #faf0ff;
}}

@media (max-width: 1050px) {{
    .status-grid {{
        grid-template-columns: repeat(2, minmax(0, 1fr));
    }}
}}

@media (max-width: 650px) {{
    .status-dashboard {{
        padding: 14px;
    }}

    .status-dashboard-header {{
        align-items: flex-start;
        flex-direction: column;
    }}

    .dashboard-total {{
        width: 100%;
        text-align: left;
    }}

    .status-grid {{
        grid-template-columns: 1fr;
    }}
}}

@media print {{
    @page {{
        size: A4 landscape;
        margin: 8mm;
    }}

    html,
    body {{
        background: white !important;
        margin: 0 !important;
        padding: 0 !important;
    }}

    body {{
        font-size: 8pt;
    }}

    .wrap {{
        max-width: none;
        margin: 0;
        padding: 0;
    }}

    .controls-box,
    #stickyHeader {{
        display: none !important;
    }}

    .box {{
        box-shadow: none;
        border-radius: 0;
        overflow: visible !important;
    }}

    .scroll {{
        overflow: visible !important;
    }}

    table {{
        width: 100%;
        min-width: 0;
        font-size: 7pt;
    }}

    th,
    td {{
        padding: 4px 3px;
    }}

    th {{
        position: static !important;
        cursor: default;
    }}

    .summary,
    .status-dashboard {{
        display: none !important;
    }}

    tr[hidden] {{
        display: none !important;
    }}
}}
</style>
</head>

<body>
<div class="wrap">

<div class="head">
    <div class="brand">
        <div class="brand-mark">P</div>
        <div class="brand-text">Portal de Produção</div>
    </div>

    <h1>{escape(titulo)}</h1>
    <small>
        Listagem atualizada em {escape(data)}
    </small>
</div>

<div class="box controls-box" style="padding:14px;margin-bottom:14px">
    <div class="controls">
        <input
            id="q"
            placeholder="🔎 Pesquisar em todas as colunas"
        >

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

        <button type="button" onclick="clearF()">
            Limpar filtros
        </button>

        <button type="button" onclick="csv()">
            Exportar CSV
        </button>

        <button
            type="button"
            class="btn-print"
            onclick="window.print()"
        >
            🖨️ Imprimir / PDF
        </button>
    </div>
</div>

<div class="box" style="padding:14px;margin-bottom:14px">
    <div class="controls">
        <a
            class="btn-estoque"
            href="{ARQUIVOS_ESTOQUE_CLIENTES['ACOFORTE'][1]}"
            target="_blank"
        >
            📦 Estoque — Acoforte
        </a>

        <a
            class="btn-estoque"
            href="{ARQUIVOS_ESTOQUE_CLIENTES['ACOVISA'][1]}"
            target="_blank"
        >
            📦 Estoque — Acovisa
        </a>

        <a
            class="btn-estoque"
            href="{ARQUIVOS_ESTOQUE_CLIENTES['TREFITA'][1]}"
            target="_blank"
        >
            📦 Estoque — Trefita
        </a>
    </div>
</div>

<div class="box">
    <div class="scroll" id="tableScroll">
        <table id="t">
            <thead>
                <tr>{cabecalho_html}</tr>
            </thead>
            <tbody>
                {tabela_html}
            </tbody>
        </table>
    </div>

    <div
        id="count"
        style="padding:12px 14px;color:#667"
    >
        {len(registros)} registros exibidos
    </div>
</div>

<div id="stickyHeader" aria-hidden="true"></div>

<div class="summary" id="summary">
    <div class="card accent">
        <small>Ordens exibidas</small>
        <b id="total-ordens">0</b>
    </div>

    <div class="card accent">
        <small>Quantidade total</small>
        <b id="total">0 KG</b>
    </div>

    <div class="card">
        <small>Em produção</small>
        <b id="em-producao">0 KG</b>
    </div>

    <div class="card">
        <small>Prontos para retirada</small>
        <b id="prontos">0 KG</b>
    </div>

    <div class="card">
        <small>Aguardando separação</small>
        <b id="aguardando-kg">0 KG</b>
    </div>
</div>

<div class="status-dashboard" id="status-dashboard">
    <div class="status-dashboard-header">
        <div>
            <div class="dashboard-kicker">
                ACOMPANHAMENTO OPERACIONAL
            </div>

            <div class="dashboard-title">
                Resumo por status
            </div>

            <div class="dashboard-subtitle">
                Ordens e quantidade conforme os filtros aplicados
            </div>
        </div>

        <div class="dashboard-total">
            <span class="dashboard-total-label">
                Ordens visíveis
            </span>

            <strong id="status-total-ordens">0</strong>
        </div>
    </div>

    <div class="status-grid">
        {cards_html}
    </div>
</div>

</div>

<script>
const q = document.querySelector('#q');
const st = document.querySelector('#st');
const rows = [...document.querySelectorAll('#t tbody tr')];

function fmt(v) {{
    return Math.round(v).toLocaleString('pt-BR') + ' KG';
}}

function updateSummary() {{
    const visible = rows.filter(r => !r.hidden);

    let total = 0;
    let prontos = 0;
    let emProducao = 0;
    let aguardandoKg = 0;

    const statusData = {{
        "LIBERADO": ["lib", 0, 0],
        "SEPARADO": ["sep", 0, 0],
        "PONTEADO": ["pon", 0, 0],
        "AGUARDANDO SEPARAÇÃO": ["agu", 0, 0],
        "DECAPADO": ["dec", 0, 0],
        "SERRADO": ["ser", 0, 0],
        "TREFILADO": ["tre", 0, 0],
        "ENDIREITADO": ["end", 0, 0],
        "ESPECIAL": ["esp", 0, 0]
    }};

    visible.forEach(r => {{
        const qtde = Number(r.dataset.qtde || 0);
        const status = r.dataset.status || "";

        total += qtde;

        // Somente LIBERADO entra em "Prontos para retirada".
        if (status === "LIBERADO") {{
            prontos += qtde;
        }} else {{
            emProducao += qtde;
        }}

        if (status === "AGUARDANDO SEPARAÇÃO") {{
            aguardandoKg += qtde;
        }}

        if (statusData[status]) {{
            statusData[status][1] += 1;
            statusData[status][2] += qtde;
        }}
    }});

    document.querySelector('#total-ordens').textContent =
        visible.length.toLocaleString('pt-BR');

    document.querySelector('#status-total-ordens').textContent =
        visible.length.toLocaleString('pt-BR');

    document.querySelector('#total').textContent = fmt(total);
    document.querySelector('#em-producao').textContent = fmt(emProducao);
    document.querySelector('#prontos').textContent = fmt(prontos);
    document.querySelector('#aguardando-kg').textContent =
        fmt(aguardandoKg);

    Object.values(statusData).forEach(
        ([classe, quantidade, kg]) => {{
            const percentual = visible.length
                ? (quantidade / visible.length) * 100
                : 0;

            const statusElement = document.querySelector(
                '#status-' + classe
            );

            const kgElement = document.querySelector(
                '#kg-' + classe
            );

            const percentualElement = document.querySelector(
                '#pct-' + classe
            );

            const barraElement = document.querySelector(
                '#bar-' + classe
            );

            if (statusElement) {{
                statusElement.textContent =
                    quantidade.toLocaleString('pt-BR');
            }}

            if (kgElement) {{
                kgElement.textContent = fmt(kg);
            }}

            if (percentualElement) {{
                percentualElement.textContent =
                    percentual.toLocaleString(
                        'pt-BR',
                        {{
                            minimumFractionDigits: 1,
                            maximumFractionDigits: 1
                        }}
                    ) + '%';
            }}

            if (barraElement) {{
                barraElement.style.width =
                    percentual.toFixed(2) + '%';
            }}
        }}
    );
}}

function applyFilters() {{
    const texto = q.value.toLowerCase().trim();
    const status = st.value;
    let count = 0;

    rows.forEach(r => {{
        const textoLinha = r.innerText.toLowerCase();
        const statusLinha = r.dataset.status || "";

        const passaTexto =
            !texto || textoLinha.includes(texto);

        const passaStatus =
            !status || statusLinha === status;

        const mostrar =
            passaTexto && passaStatus;

        r.hidden = !mostrar;

        if (mostrar) {{
            count++;
        }}
    }});

    document.querySelector('#count').textContent =
        count + " registros exibidos";

    updateSummary();
}}

function clearF() {{
    q.value = "";
    st.value = "";
    applyFilters();
}}

q.addEventListener('input', applyFilters);
st.addEventListener('change', applyFilters);

document.querySelectorAll('#t thead th').forEach(
    (th, i) => {{
        th.addEventListener('click', () => {{
            const tbody = document.querySelector('#t tbody');

            const order =
                tbody.dataset.order === "asc"
                    ? "desc"
                    : "asc";

            tbody.dataset.order = order;

            const sorted = [...rows].sort((a, b) => {{
                const va = a.cells[i].innerText.trim();
                const vb = b.cells[i].innerText.trim();

                const cmp = va.localeCompare(
                    vb,
                    "pt-BR",
                    {{
                        numeric: true,
                        sensitivity: "base"
                    }}
                );

                return order === "asc" ? cmp : -cmp;
            }});

            sorted.forEach(r => tbody.appendChild(r));
        }});
    }}
);

function escapeCSV(v) {{
    return '"' + v.replaceAll('"', '""') + '"';
}}

function csv() {{
    const visible = rows.filter(r => !r.hidden);

    const headers = [
        ...document.querySelectorAll('#t thead th')
    ].map(th => th.innerText.trim());

    const data = visible.map(
        r => [...r.cells].map(
            c => c.innerText.trim()
        )
    );

    const content = [headers, ...data]
        .map(l => l.map(escapeCSV).join(";"))
        .join("\\n");

    const blob = new Blob(
        ["\\ufeff" + content],
        {{
            type: "text/csv;charset=utf-8"
        }}
    );

    const link = document.createElement("a");

    link.href = URL.createObjectURL(blob);
    link.download = "{escape(titulo)}.csv";
    link.click();

    URL.revokeObjectURL(link.href);
}}

const tableScroll =
    document.getElementById("tableScroll");

const table =
    document.getElementById("t");

const stickyHeader =
    document.getElementById("stickyHeader");

let stickyTable = null;

function atualizarCabecalhoFixo() {{
    if (!table || !tableScroll || !stickyHeader) {{
        return;
    }}

    const tableRect =
        table.getBoundingClientRect();

    const scrollRect =
        tableScroll.getBoundingClientRect();

    const headerHeight =
        table.tHead
            ? table.tHead.getBoundingClientRect().height
            : 0;

    const deveMostrar =
        tableRect.top < 0 &&
        tableRect.bottom > headerHeight;

    if (!deveMostrar) {{
        stickyHeader.style.display = "none";
        return;
    }}

    if (!stickyTable) {{
        stickyTable = table.cloneNode(false);

        stickyTable.appendChild(
            table.tHead.cloneNode(true)
        );

        stickyTable
            .querySelectorAll("th")
            .forEach((th, i) => {{
                th.addEventListener("click", () => {{
                    const original =
                        table.tHead.querySelectorAll("th")[i];

                    if (original) {{
                        original.click();
                    }}
                }});
            }});

        stickyHeader.appendChild(stickyTable);
    }}

    stickyHeader.style.display = "block";
    stickyHeader.style.left = scrollRect.left + "px";
    stickyHeader.style.width = scrollRect.width + "px";
    stickyHeader.style.height = headerHeight + "px";

    stickyTable.style.width =
        table.scrollWidth + "px";

    stickyTable.style.transform =
        "translateX(" +
        (-tableScroll.scrollLeft) +
        "px)";

    const originalCells =
        table.tHead.querySelectorAll("th");

    const stickyCells =
        stickyTable.querySelectorAll("th");

    originalCells.forEach((cell, i) => {{
        if (stickyCells[i]) {{
            const largura =
                cell.getBoundingClientRect().width;

            stickyCells[i].style.width =
                largura + "px";

            stickyCells[i].style.minWidth =
                largura + "px";
        }}
    }});
}}

window.addEventListener(
    "scroll",
    atualizarCabecalhoFixo,
    {{ passive: true }}
);

window.addEventListener(
    "resize",
    atualizarCabecalhoFixo
);

tableScroll.addEventListener(
    "scroll",
    atualizarCabecalhoFixo,
    {{ passive: true }}
);

updateSummary();
atualizarCabecalhoFixo();
</script>
</body>
</html>"""


def processar_arquivo_producao(
    caminho_origem,
    caminho_destino,
):
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

    html_final = gerar_html_producao(
        titulo=titulo,
        data=data,
        registros=registros,
    )

    caminho_destino.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with open(
        caminho_destino,
        "w",
        encoding="utf-8",
    ) as arquivo:
        arquivo.write(html_final)

    print(f"✅ Arquivo gerado em: {caminho_destino}")


# ============================================================
# EXECUÇÃO PRINCIPAL
# ============================================================

def processar():
    print("=" * 80)
    print(
        "PROCESSAMENTO: ESTOQUE (3 exclusivos) + "
        "PRODUÇÃO (demais .htm) + CÓPIA (outros)"
    )
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

    PASTA_DESTINO.mkdir(
        parents=True,
        exist_ok=True,
    )

    todos_arquivos = [
        arquivo
        for arquivo in PASTA_ORIGEM.iterdir()
        if arquivo.is_file()
    ]

    todos_htm = [
        arquivo
        for arquivo in todos_arquivos
        if arquivo.suffix.lower() == ".htm"
    ]

    nomes_estoque_normalizados = {
        normalizar_nome_arquivo(nome): titulo
        for nome, titulo in ARQUIVOS_ESTOQUE.items()
    }

    arquivos_estoque_encontrados = {}

    for arquivo in todos_htm:
        nome_normalizado = normalizar_nome_arquivo(
            arquivo.name
        )

        if nome_normalizado in nomes_estoque_normalizados:
            arquivos_estoque_encontrados[
                nome_normalizado
            ] = arquivo

    processados_estoque = 0
    nao_encontrados_estoque = 0
    processados_producao = 0
    copiados = 0
    erros = 0

    print()
    print("=" * 80)
    print(
        "ETAPA 1 — TRATAMENTO EXCLUSIVO DE ESTOQUE "
        "(ignorando os demais .htm por enquanto)"
    )
    print("=" * 80)

    for nome_exato, titulo in ARQUIVOS_ESTOQUE.items():
        nome_normalizado = normalizar_nome_arquivo(
            nome_exato
        )

        arquivo_origem = arquivos_estoque_encontrados.get(
            nome_normalizado
        )

        if arquivo_origem is None:
            print()
            print(
                f"❌ Arquivo de estoque não encontrado: "
                f"{nome_exato}"
            )

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
            print(
                f"❌ Erro ao processar (estoque) "
                f"{arquivo_origem.name}: {erro}"
            )

    print()
    print("=" * 80)
    print(
        "ETAPA 2 — TRATAMENTO DE PRODUÇÃO "
        "(todos os .htm, exceto os 3 de estoque)"
    )
    print("=" * 80)

    for arquivo in todos_htm:
        nome_normalizado = normalizar_nome_arquivo(
            arquivo.name
        )

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
            print(
                f"❌ Erro ao processar (produção) "
                f"{arquivo.name}: {erro}"
            )

    print()
    print("=" * 80)
    print(
        "ETAPA 3 — CÓPIA DE ARQUIVOS NÃO-.HTM "
        "(INTACTOS)"
    )
    print("=" * 80)

    for arquivo in todos_arquivos:
        if arquivo.suffix.lower() == ".htm":
            continue

        arquivo_destino = PASTA_DESTINO / arquivo.name

        try:
            shutil.copy2(
                arquivo,
                arquivo_destino,
            )

            copiados += 1
            print(
                f"📄 Copiado intacto: {arquivo.name}"
            )

        except Exception as erro:
            erros += 1

            print(
                f"❌ Erro ao copiar "
                f"{arquivo.name}: {erro}"
            )

    print()
    print("=" * 80)
    print("PROCESSAMENTO CONCLUÍDO")
    print("=" * 80)
    print(
        f"✅ Arquivos de ESTOQUE processados: "
        f"{processados_estoque}"
    )
    print(
        f"⚠️ Arquivos de ESTOQUE não encontrados: "
        f"{nao_encontrados_estoque}"
    )
    print(
        f"✅ Arquivos de PRODUÇÃO processados: "
        f"{processados_producao}"
    )
    print(
        f"📄 Arquivos não-.htm copiados intactos: "
        f"{copiados}"
    )
    print(f"❌ Erros: {erros}")
    print()
    print("📂 Pasta criada/sobrescrita:")
    print(PASTA_DESTINO)

    input("\nPressione ENTER para fechar...")


if __name__ == "__main__":
    processar()
