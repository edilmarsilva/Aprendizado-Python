import re
import html as html_lib
import shutil
from pathlib import Path
from html import escape

from bs4 import BeautifulSoup


# ============================================================
# CONFIGURAÇÃO
# ============================================================

PASTA_ORIGEM = Path(
    r"C:\Users\Fiscal\Desktop\1 XML E PDF EDILMAR\FTP"
)

PASTA_DESTINO = Path(
    r"C:\Users\Fiscal\Desktop\1 XML E PDF EDILMAR\FTP 2.0"
)


ARQUIVOS_ESPECIAIS = {
    "trefita08972jkjk098080546543211222hkjfk23123k56s5gdj5412kk44k55332kk66h5421k_2":
        "Trefita - Estoque",

    "acovisa0898095278916771yiuy98978jhgnmbjkhfdahfa98371987132bbnbnbbbb2":
        "Acovisa - Estoque",

    "acoforte78788798708972jkjk098080546543211222hkjfk23123k56s5gdj5412kk44k55332kk66h5421k_2":
        "Acoforte - Estoque",
}


HEADERS = [
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


# ============================================================
# LEITURA DO ARQUIVO
# ============================================================

def ler_arquivo_como_texto(caminho):
    """
    Lê arquivos antigos normalmente salvos em Windows-1252.
    Depois converte tags escritas como <table> em tags HTML reais.
    """

    caminho = Path(caminho)

    if not caminho.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {caminho}")

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
                errors="strict"
            ) as arquivo:
                texto = arquivo.read()
            break
        except UnicodeDecodeError:
            continue

    if texto is None:
        with open(
            caminho,
            "r",
            encoding="cp1252",
            errors="replace"
        ) as arquivo:
            texto = arquivo.read()

    # Alguns arquivos chegam com o HTML inteiro escapado:
    # <table>, <tr>, <th> etc.
    anterior = None

    while texto != anterior:
        anterior = texto
        texto = html_lib.unescape(texto)

    return texto


# ============================================================
# FUNÇÕES AUXILIARES
# ============================================================

def limpar_texto(valor):
    """
    Remove espaços e tags internas, mantendo o texto da célula.
    """

    if valor is None:
        return ""

    valor = html_lib.unescape(str(valor))
    valor = re.sub(r"<[^>]+>", " ", valor)
    valor = re.sub(r"\s+", " ", valor)

    return valor.strip()


def normalizar_nome(nome):
    """
    Normaliza o nome para comparação, removendo extensão,
    espaços e diferenças entre maiúsculas/minúsculas.
    """

    nome = Path(nome).stem
    return nome.strip().lower()


def encontrar_arquivo_especial(nome_base):
    """
    Procura o arquivo pelo nome informado, aceitando:
    - .htm
    - .HTM
    - arquivo sem extensão
    """

    nome_base_normalizado = normalizar_nome(nome_base)

    if not PASTA_ORIGEM.exists():
        return None

    for item in PASTA_ORIGEM.iterdir():
        if not item.is_file():
            continue

        if normalizar_nome(item.name) == nome_base_normalizado:
            return item

    return None


def extrair_data(texto):
    """
    Extrai data e hora do texto original.
    """

    texto_limpo = limpar_texto(texto)

    padrao = re.search(
        r"atualizada\s+em\s+"
        r"(\d{1,2}/\d{1,2}/\d{4})"
        r".{0,100}?"
        r"(\d{1,2}:\d{2}:\d{2})",
        texto_limpo,
        re.IGNORECASE | re.DOTALL
    )

    if padrao:
        return f"{padrao.group(1)} às {padrao.group(2)}"

    return "Data não disponível"


def converter_numero_brasileiro(valor):
    """
    Converte números como:

    1.480  -> 1480
    35.812 -> 35812
    900    -> 900
    """

    if valor is None:
        return 0

    valor = limpar_texto(valor)
    valor = valor.replace("KGS", "")
    valor = valor.replace("KG", "")
    valor = valor.strip()

    # Para os arquivos de estoque, o ponto é separador de milhar.
    valor = valor.replace(".", "")
    valor = valor.replace(",", "")

    somente_numeros = re.sub(r"[^\d]", "", valor)

    if not somente_numeros:
        return 0

    return int(somente_numeros)


def formatar_numero(valor):
    """
    Formata 154189 como 154.189.
    """

    return f"{int(valor):,}".replace(",", ".")


def extrair_totais(texto):
    """
    Extrai os totais do rodapé do arquivo.
    """

    texto_limpo = limpar_texto(texto)

    total_estoque = 0
    total_processo = 0

    padrao_estoque = re.search(
        r"Total\s+de\s+Materiais\s+em\s+estoque\s*:?\s*"
        r"([\d\.,]+)",
        texto_limpo,
        re.IGNORECASE
    )

    padrao_processo = re.search(
        r"Total\s+de\s+Materiais\s+em\s+processo\s*:?\s*"
        r"([\d\.,]+)",
        texto_limpo,
        re.IGNORECASE
    )

    if padrao_estoque:
        total_estoque = converter_numero_brasileiro(
            padrao_estoque.group(1)
        )

    if padrao_processo:
        total_processo = converter_numero_brasileiro(
            padrao_processo.group(1)
        )

    return {
        "estoque": total_estoque,
        "processo": total_processo,
    }


def classe_status(status):
    status_normalizado = limpar_texto(status).upper()

    if status_normalizado == "OK":
        return "ok"

    if status_normalizado == "VENCIDA":
        return "vencida"

    return "outro"


# ============================================================
# EXTRAÇÃO DAS LINHAS (TODAS, NÃO SOMENTE A PRIMEIRA)
# ============================================================

def extrair_registros(texto):
    """
    Estrutura dos arquivos especiais:

    Cliente | Tipo Aço | Pf | Bitola | Acab | Lote | Qtde |
    NF | Corrida | Em Prod. | Contábil

    Percorre TODAS as linhas <tr> do arquivo, usando apenas as
    células que pertencem diretamente a cada linha (recursive=False),
    evitando misturar tabelas aninhadas e perder registros.
    """

    soup = BeautifulSoup(texto, "html.parser")

    registros = []

    for tr in soup.find_all("tr"):

        # Pega apenas as células diretamente filhas desta linha.
        celulas = tr.find_all(
            ["th", "td"],
            recursive=False
        )

        # Fallback: se não achou o suficiente, tenta recursivo
        # apenas dentro desta linha específica.
        if len(celulas) < 11:
            celulas = tr.find_all(
                ["th", "td"],
                recursive=True
            )

        if len(celulas) < 11:
            continue

        valores = [
            limpar_texto(celula.get_text(" ", strip=True))
            for celula in celulas
        ]

        # Ignora a linha de cabeçalho.
        primeiro_valor = valores[0].lower()

        if primeiro_valor in {
            "cliente",
            "tipo aço",
            "tipo aco",
        }:
            continue

        if len(valores) < 11:
            continue

        # Mantém somente as 11 colunas previstas, mesmo que
        # existam células extras por HTML quebrado.
        valores = valores[:11]

        cliente = valores[0]

        if not cliente:
            continue

        registro = {
            "Cliente": cliente,
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

            "QtdeNum": converter_numero_brasileiro(
                valores[6]
            ),

            "EmProdNum": converter_numero_brasileiro(
                valores[9]
            ),

            "Status": valores[10],
            "StatusClasse": classe_status(valores[10]),
        }

        registros.append(registro)

    return registros


# ============================================================
# GERAÇÃO DO HTML
# ============================================================

def gerar_linha_html(registro):
    status = escape(registro["Status"])
    status_classe = registro["StatusClasse"]

    status_html = (
        f'<span class="status {status_classe}">'
        f'{status}'
        f'</span>'
    )

    return f"""
<tr
    data-status="{escape(registro['Status'])}"
    data-qtde="{registro['QtdeNum']}"
    data-em-prod="{registro['EmProdNum']}"
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
    <td>{status_html}</td>
</tr>
"""


def gerar_html(titulo, data, registros, totais):
    linhas_html = "\n".join(
        gerar_linha_html(registro)
        for registro in registros
    )

    cabecalho_html = "".join(
        f"<th>{escape(cabecalho)}</th>"
        for cabecalho in HEADERS
    )

    total_estoque_original = totais["estoque"]
    total_processo_original = totais["processo"]

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
    background: #f4f7f5;
    color: #202820;
    font-family: Arial, Helvetica, sans-serif;
    font-size: 14px;
}}

.wrap {{
    width: 100%;
    max-width: 1600px;
    margin: 20px auto;
    padding: 0 12px;
}}

.head,
.controls-box,
.table-box,
.card {{
    background: #ffffff;
    border-radius: 12px;
    box-shadow: 0 4px 18px #0001;
}}

.head {{
    padding: 20px;
    margin-bottom: 14px;
}}

.head h1 {{
    margin: 0;
    color: #176b28;
    font-size: 28px;
}}

.head small {{
    display: block;
    margin-top: 6px;
    color: #667;
    font-size: 13px;
}}

.controls-box {{
    padding: 14px;
    margin-bottom: 14px;
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
    border: 1px solid #d8e0da;
    border-radius: 8px;
    background: #ffffff;
    font-size: 14px;
}}

.controls input {{
    flex: 1;
    min-width: 250px;
}}

.controls button {{
    border: none;
    background: #176b28;
    color: #ffffff;
    cursor: pointer;
    font-weight: bold;
}}

.controls button:hover {{
    background: #135620;
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
    min-width: 1100px;
    border-collapse: collapse;
    text-align: center;
}}

th,
td {{
    padding: 11px 9px;
    border-bottom: 1px solid #e1e6e2;
    white-space: nowrap;
}}

th {{
    position: sticky;
    top: 0;
    z-index: 2;
    background: #eaffea;
    color: #155c22;
    cursor: pointer;
    font-weight: bold;
}}

tbody tr:hover td {{
    background: #f4fff4;
}}

.status {{
    display: inline-block;
    min-width: 58px;
    padding: 5px 10px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: bold;
}}

.status.ok {{
    background: #dcfce7;
    color: #166534;
}}

.status.vencida {{
    background: #fecaca;
    color: #991b1b;
}}

.status.outro {{
    background: #e5e7eb;
    color: #374151;
}}

.summary {{
    display: grid;
    grid-template-columns: repeat(
        auto-fit,
        minmax(220px, 1fr)
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
    color: #667;
    font-size: 12px;
}}

.card b {{
    display: block;
    margin-top: 8px;
    color: #176b28;
    font-size: 24px;
}}

.footer-info {{
    padding: 10px;
    color: #667;
}}

@media (max-width: 600px) {{
    .controls {{
        flex-direction: column;
        align-items: stretch;
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

    <div class="head">
        <h1>{escape(titulo)}</h1>
        <small>
            Listagem atualizada em {escape(data)}
        </small>
    </div>

    <div class="controls-box">
        <div class="controls">
            <input
                id="campoPesquisa"
                type="text"
                placeholder="Pesquisar em todas as colunas"
            >

            <select id="campoStatus">
                <option value="">Todos os status</option>
                <option value="OK">OK</option>
                <option value="VENCIDA">VENCIDA</option>
            </select>

            <button type="button" onclick="limparFiltros()">
                Limpar filtros
            </button>

            <button type="button" onclick="exportarCSV()">
                Exportar CSV
            </button>
        </div>
    </div>

    <div class="table-box">
        <div class="scroll">
            <table id="tabela">
                <thead>
                    <tr>
                        {cabecalho_html}
                    </tr>
                </thead>

                <tbody>
                    {linhas_html}
                </tbody>
            </table>
        </div>

        <div class="footer-info" id="contador">
            {len(registros)} registro(s) exibido(s)
        </div>
    </div>

    <div class="summary" id="resumo">
        <div class="card">
            <small>Total de materiais em estoque</small>
            <b id="totalEstoque">
                {formatar_numero(total_estoque_original)} KG
            </b>
        </div>

        <div class="card">
            <small>Total de materiais em processo</small>
            <b id="totalProcesso">
                {formatar_numero(total_processo_original)} KG
            </b>
        </div>
    </div>

</div>

<script>
const campoPesquisa = document.querySelector("#campoPesquisa");
const campoStatus = document.querySelector("#campoStatus");
const linhas = [
    ...document.querySelectorAll("#tabela tbody tr")
];

const totalEstoqueOriginal = {total_estoque_original};
const totalProcessoOriginal = {total_processo_original};

function converterNumero(valor) {{
    return Number(valor || 0);
}}

function formatarKg(valor) {{
    return Math.round(valor)
        .toLocaleString("pt-BR") + " KG";
}}

function obterLinhasVisiveis() {{
    return linhas.filter(linha => !linha.hidden);
}}

function atualizarResumo() {{
    const linhasVisiveis = obterLinhasVisiveis();

    let totalEstoque = 0;
    let totalProcesso = 0;

    linhasVisiveis.forEach(linha => {{
        totalEstoque += converterNumero(
            linha.dataset.qtde
        );

        totalProcesso += converterNumero(
            linha.dataset.emProd
        );
    }});

    const existePesquisa =
        campoPesquisa.value.trim() !== "";

    const existeStatus =
        campoStatus.value !== "";

    if (!existePesquisa && !existeStatus) {{
        document.querySelector("#totalEstoque").textContent =
            formatarKg(totalEstoqueOriginal);

        document.querySelector("#totalProcesso").textContent =
            formatarKg(totalProcessoOriginal);
    }} else {{
        document.querySelector("#totalEstoque").textContent =
            formatarKg(totalEstoque);

        document.querySelector("#totalProcesso").textContent =
            formatarKg(totalProcesso);
    }}
}}

function aplicarFiltros() {{
    const pesquisa = campoPesquisa.value
        .toLowerCase()
        .trim();

    const statusSelecionado = campoStatus.value;

    let quantidadeVisivel = 0;

    linhas.forEach(linha => {{
        const textoLinha = linha.innerText.toLowerCase();
        const statusLinha = linha.dataset.status || "";

        const passouPesquisa =
            !pesquisa ||
            textoLinha.includes(pesquisa);

        const passouStatus =
            !statusSelecionado ||
            statusLinha === statusSelecionado;

        const mostrar =
            passouPesquisa && passouStatus;

        linha.hidden = !mostrar;

        if (mostrar) {{
            quantidadeVisivel++;
        }}
    }});

    document.querySelector("#contador").textContent =
        quantidadeVisivel +
        " registro(s) exibido(s)";

    atualizarResumo();
}}

function limparFiltros() {{
    campoPesquisa.value = "";
    campoStatus.value = "";
    aplicarFiltros();
}}

campoPesquisa.addEventListener(
    "input",
    aplicarFiltros
);

campoStatus.addEventListener(
    "change",
    aplicarFiltros
);

document.querySelectorAll("#tabela th").forEach(
    (cabecalho, indice) => {{
        cabecalho.addEventListener(
            "click",
            () => ordenarTabela(indice)
        );
    }}
);

function ordenarTabela(indice) {{
    const tbody = document.querySelector(
        "#tabela tbody"
    );

    const ordemAtual =
        tbody.dataset.ordem === "asc"
            ? "desc"
            : "asc";

    tbody.dataset.ordem = ordemAtual;

    const ordenadas = [...linhas].sort(
        (a, b) => {{
            const valorA =
                a.cells[indice].innerText.trim();

            const valorB =
                b.cells[indice].innerText.trim();

            const comparacao =
                valorA.localeCompare(
                    valorB,
                    "pt-BR",
                    {{
                        numeric: true,
                        sensitivity: "base"
                    }}
                );

            return ordemAtual === "asc"
                ? comparacao
                : -comparacao;
        }}
    );

    ordenadas.forEach(linha => tbody.appendChild(linha));
}}

function escaparCSV(valor) {{
    return '"' +
        valor.replaceAll('"', '""') +
        '"';
}}

function exportarCSV() {{
    const linhasVisiveis = obterLinhasVisiveis();

    const cabecalhos = [
        ...document.querySelectorAll("#tabela thead th")
    ].map(celula => celula.innerText.trim());

    const dados = linhasVisiveis.map(linha => [
        ...linha.cells
    ].map(celula => celula.innerText.trim()));

    const conteudo = [
        cabecalhos,
        ...dados
    ]
        .map(linha => linha.map(escaparCSV).join(";"))
        .join("\\n");

    const arquivo = new Blob(
        ["\\ufeff" + conteudo],
        {{ type: "text/csv;charset=utf-8" }}
    );

    const link = document.createElement("a");

    link.href = URL.createObjectURL(arquivo);
    link.download = "{escape(titulo)}.csv";
    link.click();

    URL.revokeObjectURL(link.href);
}}

atualizarResumo();
</script>

</body>
</html>
"""


# ============================================================
# PROCESSAMENTO DE UM ARQUIVO ESPECIAL
# ============================================================

def processar_arquivo_especial(
    caminho_origem,
    caminho_destino,
    titulo
):
    print(f"\n🔄 Processando: {caminho_origem.name}")

    texto = ler_arquivo_como_texto(caminho_origem)

    data = extrair_data(texto)
    totais = extrair_totais(texto)
    registros = extrair_registros(texto)

    print(f"   Registros encontrados: {len(registros)}")
    for indice, registro in enumerate(registros, start=1):
        print(
            f"   {indice:03d} - Cliente: {registro['Cliente']} | "
            f"Lote: {registro['Lote']} | Qtde: {registro['Qtde']} | "
            f"Status: {registro['Status']}"
        )

    html_final = gerar_html(
        titulo=titulo,
        data=data,
        registros=registros,
        totais=totais
    )

    caminho_destino.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(
        caminho_destino,
        "w",
        encoding="utf-8"
    ) as arquivo:
        arquivo.write(html_final)

    print(f"\n   ✅ Título: {titulo}")
    print(f"   ✅ Registros: {len(registros)}")
    print(
        f"   ✅ Total estoque: "
        f"{formatar_numero(totais['estoque'])} KG"
    )
    print(
        f"   ✅ Total processo: "
        f"{formatar_numero(totais['processo'])} KG"
    )
    print(f"   ✅ Gerado: {caminho_destino.name}")


# ============================================================
# EXECUÇÃO PRINCIPAL
# ============================================================

def processar():
    print("=" * 75)
    print("TRATAMENTO DOS 3 ARQUIVOS ESPECIAIS DE ESTOQUE")
    print("=" * 75)

    if not PASTA_ORIGEM.exists():
        print(f"\n❌ Pasta de origem não encontrada:")
        print(PASTA_ORIGEM)
        input("\nPressione ENTER para fechar...")
        return

    # Cria ou sobrescreve completamente a pasta de destino.
    if PASTA_DESTINO.exists():
        print(f"\n🗑️ Removendo pasta existente:")
        print(PASTA_DESTINO)
        shutil.rmtree(PASTA_DESTINO)

    PASTA_DESTINO.mkdir(
        parents=True,
        exist_ok=True
    )

    processados = 0
    nao_encontrados = 0
    erros = 0

    for nome_base, titulo in ARQUIVOS_ESPECIAIS.items():
        try:
            arquivo_origem = encontrar_arquivo_especial(nome_base)

            if arquivo_origem is None:
                print(f"\n❌ Não encontrado: {nome_base}")
                nao_encontrados += 1
                continue

            # Mantém o nome original e usa .htm no destino.
            arquivo_destino = (
                PASTA_DESTINO /
                f"{arquivo_origem.stem}.htm"
            )

            processar_arquivo_especial(
                caminho_origem=arquivo_origem,
                caminho_destino=arquivo_destino,
                titulo=titulo
            )

            processados += 1

        except Exception as erro:
            erros += 1

            print(
                f"\n❌ Erro ao processar "
                f"{nome_base}:"
            )
            print(f"   {erro}")

    print("\n" + "=" * 75)
    print("PROCESSAMENTO CONCLUÍDO")
    print("=" * 75)
    print(f"✅ Arquivos processados: {processados}")
    print(f"⚠️ Arquivos não encontrados: {nao_encontrados}")
    print(f"❌ Erros: {erros}")
    print(f"\n📂 Pasta de saída:")
    print(PASTA_DESTINO)

    input("\nPressione ENTER para fechar...")


if __name__ == "__main__":
    processar()
