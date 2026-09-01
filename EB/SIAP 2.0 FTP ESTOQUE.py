import re
import shutil
import unicodedata

from html import escape, unescape
from html.parser import HTMLParser
from pathlib import Path


# ============================================================
# CONFIGURAÇÃO
# ============================================================

PASTA_ORIGEM = Path(
    r"C:\Users\Fiscal\Desktop\1 XML E PDF EDILMAR\FTP"
)

PASTA_DESTINO = Path(
    r"C:\Users\Fiscal\Desktop\1 XML E PDF EDILMAR\FTP 2.0"
)


# Nomes EXATOS (sem extensão) dos três arquivos a processar.
ARQUIVOS_PERMITIDOS = {
    "acoforte78788798708972jkjk098080546543211222hkjfk23123k56s5gdj5412kk44k55332kk66h5421k_2":
        "Acoforte - Estoque",

    "acovisa0898095278916771yiuy98978jhgnmbjkhfdahfa98371987132bbnbnbbbb2":
        "Acovisa - Estoque",

    "trefita08972jkjk098080546543211222hkjfk23123k56s5gdj5412kk44k55332kk66h5421k_2":
        "Trefita - Estoque",
}


COLUNAS = [
    "Cliente",
    "Tipo Aço",
    "Pf",
    "Bitola",
    "Acab",
    "Lote",
    "Qtde",
    "NF",
    "Corrida",
    "Em Prod.",
    "Contábil",
]


CABECALHO_NORMALIZADO = [
    "CLIENTE",
    "TIPO ACO",
    "PF",
    "BITOLA",
    "ACAB",
    "LOTE",
    "QTDE",
    "NF",
    "CORRIDA",
    "EM PROD.",
    "CONTABIL",
]


# ============================================================
# LEITURA DO ARQUIVO
# ============================================================

def ler_arquivo(caminho):
    """
    Lê o arquivo usando as codificações mais comuns.
    """

    codificacoes = [
        "cp1252",
        "latin-1",
        "utf-8",
    ]

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


# ============================================================
# FUNÇÕES DE TEXTO
# ============================================================

def limpar_texto(valor):
    """
    Remove espaços, quebras de linha e entidades HTML.
    """

    if valor is None:
        return ""

    valor = unescape(str(valor))

    valor = re.sub(
        r"\s+",
        " ",
        valor,
    )

    return valor.strip()


def normalizar_texto(valor):
    """
    Normaliza texto para comparações, removendo acentos.
    """

    valor = limpar_texto(valor).upper()

    valor = unicodedata.normalize(
        "NFD",
        valor,
    )

    valor = "".join(
        caractere
        for caractere in valor
        if unicodedata.category(caractere) != "Mn"
    )

    valor = re.sub(
        r"\s+",
        " ",
        valor,
    )

    return valor.strip()


def normalizar_nome_arquivo(nome):
    return Path(nome).stem.strip().lower()


# ============================================================
# LOCALIZAÇÃO EXATA DOS ARQUIVOS
# ============================================================

def localizar_arquivos():
    """
    Localiza os arquivos comparando o nome (sem extensão) contra
    o nome EXATO informado em ARQUIVOS_PERMITIDOS. Sem prefixo,
    sem ordenação alfabética e sem escolha de arquivo parecido.
    """

    encontrados = {}

    if not PASTA_ORIGEM.exists():
        return encontrados

    arquivos = [
        arquivo
        for arquivo in PASTA_ORIGEM.iterdir()
        if arquivo.is_file()
        and arquivo.suffix.lower() == ".htm"
    ]

    for nome_exato in ARQUIVOS_PERMITIDOS:
        nome_exato_normalizado = normalizar_nome_arquivo(
            nome_exato
        )

        correspondencias = [
            arquivo
            for arquivo in arquivos
            if normalizar_nome_arquivo(arquivo.name) == nome_exato_normalizado
        ]

        if correspondencias:
            encontrados[nome_exato] = correspondencias[0]

            if len(correspondencias) > 1:
                print()
                print(
                    f"⚠️ Mais de um arquivo com o nome exato "
                    f"'{nome_exato}'."
                )
                print(
                    f"Será usado somente: "
                    f"{correspondencias[0].name}"
                )

    return encontrados


# ============================================================
# PARSER HTML ROBUSTO
# ============================================================

class TabelaHTMLParser(HTMLParser):
    """
    Leitor tolerante para HTML antigo ou malformado.

    Uma nova tag <td> ou <th> sempre inicia uma nova célula,
    mesmo que o arquivo anterior não tenha fechado corretamente
    a célula anterior. Da mesma forma, uma nova tag <tr> encerra
    a linha anterior.
    """

    def __init__(self):
        super().__init__(
            convert_charrefs=True
        )

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

        texto = limpar_texto(
            "".join(self.celula_atual)
        )

        self.linha_atual.append(
            {
                "tipo": self.tipo_celula_atual,
                "valor": texto,
            }
        )

        self.celula_atual = None
        self.tipo_celula_atual = None

    def iniciar_linha(self):
        self.finalizar_linha()

        self.linha_atual = []

    def finalizar_linha(self):
        self.finalizar_celula()

        if self.linha_atual:
            self.linhas.append(
                self.linha_atual
            )

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


# ============================================================
# IDENTIFICAÇÃO E LIMPEZA DAS LINHAS
# ============================================================

def valores_da_linha(linha):
    return [
        limpar_texto(celula["valor"])
        for celula in linha
    ]


def linha_eh_cabecalho(valores):
    if len(valores) < 11:
        return False

    primeiros = [
        normalizar_texto(valor)
        for valor in valores[:11]
    ]

    if primeiros == CABECALHO_NORMALIZADO:
        return True

    primeiro = normalizar_texto(valores[0])
    segundo = normalizar_texto(valores[1])

    if primeiro == "CLIENTE":
        return True

    if segundo == "TIPO ACO":
        return True

    return False


def linha_eh_total(valores):
    texto = " ".join(
        normalizar_texto(valor)
        for valor in valores
    )

    return (
        "TOTAL DE MATERIAIS" in texto
        or "TOTAL MATERIAIS" in texto
    )


def linha_tem_dados(valores):
    if len(valores) < 11:
        return False

    cliente = limpar_texto(
        valores[0]
    )

    if not cliente:
        return False

    if linha_eh_cabecalho(valores):
        return False

    if linha_eh_total(valores):
        return False

    return True


def ajustar_linha(valores):
    if len(valores) < 11:
        return None

    if len(valores) == 11:
        return valores

    return valores[:11]


# ============================================================
# EXTRAÇÃO DOS REGISTROS
# ============================================================

def extrair_registros(texto):
    """
    Extrai todos os registros, linha por linha.

    0  Cliente
    1  Tipo Aço
    2  Pf
    3  Bitola
    4  Acab
    5  Lote
    6  Qtde
    7  NF
    8  Corrida
    9  Em Prod.
    10 Contábil
    """

    linhas = extrair_linhas_html(
        texto
    )

    print(
        f"   Linhas HTML identificadas: "
        f"{len(linhas)}"
    )

    registros = []
    encontrou_cabecalho = False

    for numero_linha, linha in enumerate(
        linhas,
        start=1,
    ):
        valores = valores_da_linha(
            linha
        )

        if len(valores) < 11:
            continue

        if linha_eh_cabecalho(valores):
            encontrou_cabecalho = True
            continue

        if not encontrou_cabecalho:
            continue

        if not linha_tem_dados(valores):
            continue

        valores = ajustar_linha(
            valores
        )

        if valores is None:
            continue

        registro = {
            "Cliente": valores[0],
            "Tipo Aço": valores[1],
            "Pf": valores[2],
            "Bitola": valores[3],
            "Acab": valores[4],
            "Lote": valores[5],
            "Qtde": valores[6],
            "NF": valores[7],
            "Corrida": valores[8],
            "Em Prod.": valores[9],
            "Contábil": valores[10],
        }

        registro["QtdeNum"] = converter_numero(
            registro["Qtde"]
        )

        registro["EmProdNum"] = converter_numero(
            registro["Em Prod."]
        )

        registro["Status"] = registro["Contábil"]
        registro["StatusClasse"] = classe_status(
            registro["Contábil"]
        )

        # ------------------------------------------------------
        # NOVO: Aguardando Ordem
        # Qtde - Em Prod. > 0
        # ------------------------------------------------------
        registro["AguardandoOrdem"] = (
            registro["QtdeNum"] - registro["EmProdNum"]
        ) > 0

        registros.append(
            registro
        )

    print(
        f"   Registros aproveitados: "
        f"{len(registros)}"
    )

    return registros


# ============================================================
# DATA, NÚMEROS E TOTAIS
# ============================================================

def extrair_data(texto):
    texto_limpo = limpar_texto(
        re.sub(
            r"<[^>]+>",
            " ",
            texto,
            flags=re.IGNORECASE,
        )
    )

    padrao = re.search(
        r"atualizada\s+em\s+"
        r"(\d{1,2}/\d{1,2}/\d{4})"
        r".{0,150}?"
        r"(\d{1,2}:\d{2}:\d{2})",
        texto_limpo,
        flags=re.IGNORECASE | re.DOTALL,
    )

    if padrao:
        return (
            f"{padrao.group(1)} às "
            f"{padrao.group(2)}"
        )

    return "Data não disponível"


def converter_numero(valor):
    valor = limpar_texto(
        valor
    ).upper()

    valor = valor.replace("KGS", "")
    valor = valor.replace("KG", "")
    valor = valor.strip()

    valor = valor.replace(".", "")
    valor = valor.replace(",", "")

    numeros = re.sub(
        r"[^\d]",
        "",
        valor,
    )

    if not numeros:
        return 0

    return int(numeros)


def formatar_kg(valor):
    return (
        f"{int(valor):,}".replace(
            ",",
            ".",
        )
        + " KG"
    )


def extrair_totais(texto):
    texto_limpo = limpar_texto(
        re.sub(
            r"<[^>]+>",
            " ",
            texto,
            flags=re.IGNORECASE,
        )
    )

    total_estoque = 0
    total_processo = 0

    padrao_estoque = re.search(
        r"Total\s+de\s+Materiais\s+em\s+estoque"
        r"\s*:?\s*([\d\.,]+)",
        texto_limpo,
        flags=re.IGNORECASE,
    )

    padrao_processo = re.search(
        r"Total\s+de\s+Materiais\s+em\s+processo"
        r"\s*:?\s*([\d\.,]+)",
        texto_limpo,
        flags=re.IGNORECASE,
    )

    if padrao_estoque:
        total_estoque = converter_numero(
            padrao_estoque.group(1)
        )

    if padrao_processo:
        total_processo = converter_numero(
            padrao_processo.group(1)
        )

    return {
        "estoque": total_estoque,
        "processo": total_processo,
    }


def classe_status(valor):
    valor = normalizar_texto(
        valor
    )

    if valor == "OK":
        return "ok"

    if valor == "VENCIDA":
        return "vencida"

    return "outro"


# ============================================================
# GERAÇÃO DO HTML
# ============================================================

def gerar_linha_html(registro):
    status = escape(
        registro["Contábil"]
    )

    classe = registro[
        "StatusClasse"
    ]

    aguardando = (
        "true"
        if registro["AguardandoOrdem"]
        else "false"
    )

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
</tr>
"""


def gerar_html(
    titulo,
    data,
    registros,
    totais,
):
    cabecalhos_html = "".join(
        f"<th>{escape(coluna)}</th>"
        for coluna in COLUNAS
    )

    linhas_html = "".join(
        gerar_linha_html(registro)
        for registro in registros
    )

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
    background: #f2f6f3;
    color: #172019;
    font-family: Arial, Helvetica, sans-serif;
    font-size: 14px;
}}

.wrap {{
    width: 100%;
    max-width: 1600px;
    margin: 0 auto;
}}

.header,
.controls-box,
.table-box,
.card {{
    background: #ffffff;
    border-radius: 12px;
    box-shadow: 0 4px 18px #0001;
}}

.header {{
    margin-bottom: 14px;
    padding: 20px;
}}

.header h1 {{
    margin: 0;
    color: #08712c;
    font-size: 29px;
}}

.header p {{
    margin: 8px 0 0;
    color: #52635a;
}}

.controls-box {{
    margin-bottom: 14px;
    padding: 14px;
}}

.controls {{
    display: flex;
    align-items: center;
    gap: 8px;
    flex-wrap: wrap;
}}

.controls input,
.controls select,
.controls button {{
    min-height: 40px;
    padding: 10px 12px;
    border: 1px solid #d5dfd8;
    border-radius: 8px;
    font-size: 14px;
}}

.controls input {{
    flex: 1;
    min-width: 260px;
}}

.controls button {{
    border: none;
    background: #11742d;
    color: #ffffff;
    cursor: pointer;
    font-weight: bold;
}}

.controls button:hover {{
    background: #095520;
}}

.table-box {{
    overflow: hidden;
}}

.scroll {{
    width: 100%;
    overflow-x: auto;
}}

table {{
    width: 100%;
    min-width: 1150px;
    border-collapse: collapse;
    text-align: center;
}}

th,
td {{
    padding: 11px 10px;
    border-bottom: 1px solid #e1e8e3;
    white-space: nowrap;
}}

th {{
    position: sticky;
    top: 0;
    z-index: 2;
    background: #e8ffe9;
    color: #086b2b;
    cursor: pointer;
    font-weight: bold;
}}

tbody tr:hover td {{
    background: #f3fff4;
}}

.status {{
    display: inline-block;
    min-width: 58px;
    padding: 5px 11px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: bold;
}}

.status.ok {{
    background: #d9fbe7;
    color: #176b3a;
}}

.status.vencida {{
    background: #ffd0d0;
    color: #a01818;
}}

.status.outro {{
    background: #e7ebea;
    color: #37423c;
}}

.contador {{
    padding: 11px 8px;
    color: #52635a;
}}

.resumo {{
    display: grid;
    grid-template-columns: repeat(
        auto-fit,
        minmax(230px, 1fr)
    );
    gap: 12px;
    margin-top: 14px;
}}

.card {{
    padding: 18px;
    text-align: center;
}}

.card small {{
    display: block;
    color: #52635a;
}}

.card strong {{
    display: block;
    margin-top: 8px;
    color: #08702a;
    font-size: 25px;
}}

@media (max-width: 650px) {{
    .controls {{
        align-items: stretch;
        flex-direction: column;
    }}

    .controls input,
    .controls select,
    .controls button {{
        width: 100%;
    }}
}}
</style>
</head>

<body>
<div class="wrap">

    <div class="header">
        <h1>{escape(titulo)}</h1>
        <p>Listagem atualizada em {escape(data)}</p>
    </div>

    <div class="controls-box">
        <div class="controls">

            <input
                id="pesquisa"
                type="text"
                placeholder="Pesquisar em todas as colunas"
            >

            <select id="filtroStatus">
                <option value="">Todos os status</option>
                <option value="OK">OK</option>
                <option value="VENCIDA">VENCIDA</option>
                <option value="AGUARDANDO_ORDEM">Aguardando Ordem</option>
            </select>

            <button
                type="button"
                onclick="limparFiltros()"
            >
                Limpar filtros
            </button>

            <button
                type="button"
                onclick="exportarCSV()"
            >
                Exportar CSV
            </button>

        </div>
    </div>

    <div class="table-box">
        <div class="scroll">

            <table id="tabela">
                <thead>
                    <tr>
                        {cabecalhos_html}
                    </tr>
                </thead>

                <tbody>
                    {linhas_html}
                </tbody>
            </table>

        </div>

        <div
            class="contador"
            id="contador"
        >
            {len(registros)} registro(s) exibido(s)
        </div>
    </div>

    <div class="resumo">

        <div class="card">
            <small>Total de materiais em estoque</small>
            <strong id="totalEstoque">
                {formatar_kg(totais["estoque"])}
            </strong>
        </div>

        <div class="card">
            <small>Total de materiais em processo</small>
            <strong id="totalProcesso">
                {formatar_kg(totais["processo"])}
            </strong>
        </div>

    </div>

</div>

<script>
const pesquisa =
    document.querySelector("#pesquisa");

const filtroStatus =
    document.querySelector("#filtroStatus");

const linhas = [
    ...document.querySelectorAll(
        "#tabela tbody tr"
    )
];

const estoqueOriginal =
    {totais["estoque"]};

const processoOriginal =
    {totais["processo"]};


function formatarKg(valor) {{
    return Math.round(valor)
        .toLocaleString("pt-BR") + " KG";
}}


function obterLinhasVisiveis() {{
    return linhas.filter(
        linha => !linha.hidden
    );
}}


function atualizarResumo() {{
    const visiveis =
        obterLinhasVisiveis();

    const possuiFiltro =
        pesquisa.value.trim() !== "" ||
        filtroStatus.value !== "";

    let estoque = 0;
    let processo = 0;

    visiveis.forEach(linha => {{
        estoque += Number(
            linha.dataset.qtde || 0
        );

        processo += Number(
            linha.dataset.emProd || 0
        );
    }});

    document.querySelector(
        "#totalEstoque"
    ).textContent = formatarKg(
        possuiFiltro
            ? estoque
            : estoqueOriginal
    );

    document.querySelector(
        "#totalProcesso"
    ).textContent = formatarKg(
        possuiFiltro
            ? processo
            : processoOriginal
    );
}}


function aplicarFiltros() {{
    const texto =
        pesquisa.value
            .toLowerCase()
            .trim();

    const statusSelecionado =
        filtroStatus.value;

    let quantidade = 0;

    linhas.forEach(linha => {{
        const textoLinha =
            linha.innerText.toLowerCase();

        const statusLinha =
            linha.dataset.status || "";

        const aguardandoOrdem =
            linha.dataset.aguardando === "true";

        const passouTexto =
            !texto ||
            textoLinha.includes(texto);

        let passouStatus = true;

        if (statusSelecionado === "AGUARDANDO_ORDEM") {{
            passouStatus = aguardandoOrdem;
        }} else if (statusSelecionado) {{
            passouStatus =
                statusLinha === statusSelecionado;
        }}

        const mostrar =
            passouTexto &&
            passouStatus;

        linha.hidden = !mostrar;

        if (mostrar) {{
            quantidade++;
        }}
    }});

    document.querySelector(
        "#contador"
    ).textContent =
        quantidade +
        " registro(s) exibido(s)";

    atualizarResumo();
}}


function limparFiltros() {{
    pesquisa.value = "";
    filtroStatus.value = "";
    aplicarFiltros();
}}


pesquisa.addEventListener(
    "input",
    aplicarFiltros
);

filtroStatus.addEventListener(
    "change",
    aplicarFiltros
);


function ordenarTabela(indice) {{
    const tbody =
        document.querySelector(
            "#tabela tbody"
        );

    const ordemAtual =
        tbody.dataset.ordem || "desc";

    const novaOrdem =
        ordemAtual === "asc"
            ? "desc"
            : "asc";

    tbody.dataset.ordem = novaOrdem;

    const ordenadas =
        [...linhas].sort((a, b) => {{
            const valorA =
                a.cells[indice]
                    .innerText
                    .trim();

            const valorB =
                b.cells[indice]
                    .innerText
                    .trim();

            const comparacao =
                valorA.localeCompare(
                    valorB,
                    "pt-BR",
                    {{
                        numeric: true,
                        sensitivity: "base"
                    }}
                );

            return novaOrdem === "asc"
                ? comparacao
                : -comparacao;
        }});

    ordenadas.forEach(linha => {{
        tbody.appendChild(linha);
    }});
}}


document.querySelectorAll(
    "#tabela thead th"
).forEach((cabecalho, indice) => {{
    cabecalho.addEventListener(
        "click",
        () => ordenarTabela(indice)
    );
}});


function escaparCSV(valor) {{
    return '"' +
        valor.replaceAll('"', '""') +
        '"';
}}


function exportarCSV() {{
    const visiveis =
        obterLinhasVisiveis();

    const cabecalhos = [
        ...document.querySelectorAll(
            "#tabela thead th"
        )
    ].map(
        celula => celula.innerText.trim()
    );

    const dados = visiveis.map(linha => [
        ...linha.cells
    ].map(
        celula => celula.innerText.trim()
    ));

    const conteudo = [
        cabecalhos,
        ...dados
    ]
        .map(linha =>
            linha.map(escaparCSV).join(";")
        )
        .join("\\n");

    const arquivo = new Blob(
        ["\\ufeff" + conteudo],
        {{
            type: "text/csv;charset=utf-8"
        }}
    );

    const link =
        document.createElement("a");

    link.href =
        URL.createObjectURL(arquivo);

    link.download =
        "{escape(titulo)}.csv";

    link.click();

    URL.revokeObjectURL(link.href);
}}


atualizarResumo();
</script>

</body>
</html>
"""


# ============================================================
# PROCESSAMENTO DE UM ARQUIVO
# ============================================================

def processar_arquivo(
    caminho_origem,
    caminho_destino,
    titulo,
):
    print()
    print("=" * 80)
    print(f"Processando: {caminho_origem.name}")
    print(f"Título: {titulo}")
    print("=" * 80)

    texto = ler_arquivo(
        caminho_origem
    )

    data = extrair_data(
        texto
    )

    totais = extrair_totais(
        texto
    )

    registros = extrair_registros(
        texto
    )

    print()
    print(
        f"✅ Total de registros: "
        f"{len(registros)}"
    )

    for indice, registro in enumerate(
        registros,
        start=1,
    ):
        print(
            f"{indice:04d} | "
            f"Cliente: {registro['Cliente']} | "
            f"Tipo Aço: {registro['Tipo Aço']} | "
            f"Pf: {registro['Pf']} | "
            f"Bitola: {registro['Bitola']} | "
            f"Acab: {registro['Acab']} | "
            f"Lote: {registro['Lote']} | "
            f"Qtde: {registro['Qtde']} | "
            f"NF: {registro['NF']} | "
            f"Corrida: {registro['Corrida']} | "
            f"Em Prod.: {registro['Em Prod.']} | "
            f"Contábil: {registro['Contábil']} | "
            f"AguardandoOrdem: {registro['AguardandoOrdem']}"
        )

    html_final = gerar_html(
        titulo=titulo,
        data=data,
        registros=registros,
        totais=totais,
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

    print()
    print(
        f"✅ Arquivo gerado em:"
    )
    print(caminho_destino)


# ============================================================
# EXECUÇÃO PRINCIPAL
# ============================================================

def processar():
    print("=" * 80)
    print("TRATAMENTO EXCLUSIVO DE TREFITA, ACOVISA E ACOFORTE")
    print("=" * 80)

    if not PASTA_ORIGEM.exists():
        print("❌ Pasta de origem não encontrada:")
        print(PASTA_ORIGEM)
        input("\nPressione ENTER para fechar...")
        return

    if PASTA_DESTINO.exists():
        print("🗑️ Sobrescrevendo a pasta FTP 2.0...")
        shutil.rmtree(PASTA_DESTINO)

    PASTA_DESTINO.mkdir(
        parents=True,
        exist_ok=True,
    )

    arquivos = localizar_arquivos()

    processados = 0
    nao_encontrados = 0
    erros = 0

    for nome_exato, titulo in ARQUIVOS_PERMITIDOS.items():
        arquivo_origem = arquivos.get(
            nome_exato
        )

        if arquivo_origem is None:
            print()
            print(
                f"❌ Arquivo não encontrado: "
                f"{nome_exato}"
            )
            nao_encontrados += 1
            continue

        arquivo_destino = (
            PASTA_DESTINO /
            arquivo_origem.name
        )

        try:
            processar_arquivo(
                caminho_origem=arquivo_origem,
                caminho_destino=arquivo_destino,
                titulo=titulo,
            )

            processados += 1

        except Exception as erro:
            erros += 1

            print()
            print(
                f"❌ Erro ao processar "
                f"{arquivo_origem.name}:"
            )
            print(erro)

    print()
    print("=" * 80)
    print("PROCESSAMENTO CONCLUÍDO")
    print("=" * 80)
    print(
        f"✅ Arquivos processados: "
        f"{processados}"
    )
    print(
        f"⚠️ Arquivos não encontrados: "
        f"{nao_encontrados}"
    )
    print(
        f"❌ Erros: "
        f"{erros}"
    )
    print()
    print(
        "📂 Pasta criada/sobrescrita:"
    )
    print(PASTA_DESTINO)

    input("\nPressione ENTER para fechar...")


if __name__ == "__main__":
    processar()