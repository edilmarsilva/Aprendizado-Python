import re
import shutil
import unicodedata

from datetime import datetime
from html import escape, unescape
from html.parser import HTMLParser
from pathlib import Path

from bs4 import BeautifulSoup


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
</tr>
"""


def gerar_html_estoque(titulo, data, registros, totais):
    cabecalhos_html = "".join(f"<th>{escape(c)}</th>" for c in COLUNAS_ESTOQUE)
    linhas_html = "".join(gerar_linha_html_estoque(r) for r in registros)

    total_estoque_formatado = formatar_kg(totais["estoque"])
    total_processo_formatado = formatar_kg(totais["processo"])

    return f"""<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{escape(titulo)}</title>
<style>
* {{ box-sizing: border-box; }}
body {{ margin: 0; background: #f2f6f3; color: #172019; font-family: Arial, Helvetica, sans-serif; font-size: 14px; }}
.wrap {{ width: 100%; max-width: 1600px; margin: 0 auto; }}
.header, .controls-box, .table-box, .card {{ background: #ffffff; border-radius: 12px; box-shadow: 0 4px 18px #0001; }}
.header {{ margin-bottom: 14px; padding: 20px; }}
.header h1 {{ margin: 0; color: #08712c; font-size: 29px; }}
.header p {{ margin: 8px 0 0; color: #52635a; }}
.controls-box {{ margin-bottom: 14px; padding: 14px; }}
.controls {{ display: flex; align-items: center; gap: 8px; flex-wrap: wrap; }}
.controls input, .controls select, .controls button {{ min-height: 40px; padding: 10px 12px; border: 1px solid #d5dfd8; border-radius: 8px; font-size: 14px; }}
.controls input {{ flex: 1; min-width: 260px; }}
.controls button {{ border: none; background: #11742d; color: #ffffff; cursor: pointer; font-weight: bold; }}
.controls button:hover {{ background: #095520; }}
.table-box {{ overflow: hidden; }}
.scroll {{ width: 100%; overflow-x: auto; }}
table {{ width: 100%; min-width: 1150px; border-collapse: collapse; text-align: center; }}
th, td {{ padding: 11px 10px; border-bottom: 1px solid #e1e8e3; white-space: nowrap; }}
th {{ position: sticky; top: 0; z-index: 2; background: #e8ffe9; color: #086b2b; cursor: pointer; font-weight: bold; }}
tbody tr:hover td {{ background: #f3fff4; }}
.status {{ display: inline-block; min-width: 58px; padding: 5px 11px; border-radius: 20px; font-size: 12px; font-weight: bold; }}
.status.ok {{ background: #d9fbe7; color: #176b3a; }}
.status.vencida {{ background: #ffd0d0; color: #a01818; }}
.status.outro {{ background: #e7ebea; color: #37423c; }}
.contador {{ padding: 11px 8px; color: #52635a; }}
.resumo {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(230px, 1fr)); gap: 12px; margin-top: 14px; }}
.card {{ padding: 18px; text-align: center; }}
.card small {{ display: block; color: #52635a; }}
.card strong {{ display: block; margin-top: 8px; color: #08702a; font-size: 25px; }}
@media (max-width: 650px) {{
    .controls {{ align-items: stretch; flex-direction: column; }}
    .controls input, .controls select, .controls button {{ width: 100%; }}
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
            <input id="pesquisa" type="text" placeholder="Pesquisar em todas as colunas">
            <select id="filtroStatus">
                <option value="">Todos os status</option>
                <option value="OK">OK</option>
                <option value="VENCIDA">VENCIDA</option>
                <option value="AGUARDANDO_ORDEM">Aguardando Ordem</option>
            </select>
            <button type="button" onclick="limparFiltros()">Limpar filtros</button>
            <button type="button" onclick="exportarCSV()">Exportar CSV</button>
        </div>
    </div>

    <div class="table-box">
        <div class="scroll">
            <table id="tabela">
                <thead><tr>{cabecalhos_html}</tr></thead>
                <tbody>{linhas_html}</tbody>
            </table>
        </div>
        <div class="contador" id="contador">{len(registros)} registro(s) exibido(s)</div>
    </div>

    <div class="resumo">
        <div class="card">
            <small>Total de materiais em estoque</small>
            <strong id="totalEstoque">{total_estoque_formatado}</strong>
        </div>
        <div class="card">
            <small>Total de materiais em processo</small>
            <strong id="totalProcesso">{total_processo_formatado}</strong>
        </div>
    </div>

</div>

<script>
const pesquisa = document.querySelector('#pesquisa');
const filtroStatus = document.querySelector('#filtroStatus');
const linhas = [...document.querySelectorAll('#tabela tbody tr')];

function atualizarResumo() {{
    const visiveis = linhas.filter(l => !l.hidden);
    let totalEstoque = 0;
    let totalProcesso = 0;

    visiveis.forEach(l => {{
        totalEstoque += Number(l.dataset.qtde || 0);
        totalProcesso += Number(l.dataset.emProd || 0);
    }});

    document.querySelector('#totalEstoque').textContent = Math.round(totalEstoque).toLocaleString('pt-BR') + ' KG';
    document.querySelector('#totalProcesso').textContent = Math.round(totalProcesso).toLocaleString('pt-BR') + ' KG';
}}

function aplicarFiltros() {{
    const texto = pesquisa.value.toLowerCase().trim();
    const status = filtroStatus.value;
    let contador = 0;

    linhas.forEach(l => {{
        const textoLinha = l.innerText.toLowerCase();
        const statusLinha = l.dataset.status || "";
        const aguardando = l.dataset.aguardando === "true";

        let passaStatus = !status;

        if (status === "AGUARDANDO_ORDEM") {{
            passaStatus = aguardando;
        }} else if (status) {{
            passaStatus = statusLinha === status;
        }}

        const passaTexto = !texto || textoLinha.includes(texto);
        const mostrar = passaTexto && passaStatus;

        l.hidden = !mostrar;
        if (mostrar) contador++;
    }});

    document.querySelector('#contador').textContent = contador + " registro(s) exibido(s)";
    atualizarResumo();
}}

function limparFiltros() {{
    pesquisa.value = "";
    filtroStatus.value = "";
    aplicarFiltros();
}}

pesquisa.addEventListener('input', aplicarFiltros);
filtroStatus.addEventListener('change', aplicarFiltros);

document.querySelectorAll('#tabela thead th').forEach((th, i) => {{
    th.addEventListener('click', () => {{
        const tbody = document.querySelector('#tabela tbody');
        const ordem = tbody.dataset.ordem === "asc" ? "desc" : "asc";
        tbody.dataset.ordem = ordem;

        const ordenadas = [...linhas].sort((a, b) => {{
            const va = a.cells[i].innerText.trim();
            const vb = b.cells[i].innerText.trim();
            const cmp = va.localeCompare(vb, "pt-BR", {{ numeric: true, sensitivity: "base" }});
            return ordem === "asc" ? cmp : -cmp;
        }});

        ordenadas.forEach(l => tbody.appendChild(l));
    }});
}});

function escapeCSV(v) {{ return '"' + v.replaceAll('"', '""') + '"'; }}

function exportarCSV() {{
    const visiveis = linhas.filter(l => !l.hidden);
    const cabecalhos = [...document.querySelectorAll('#tabela thead th')].map(th => th.innerText.trim());
    const dados = visiveis.map(l => [...l.cells].map(c => c.innerText.trim()));
    const conteudo = [cabecalhos, ...dados].map(l => l.map(escapeCSV).join(";")).join("\\n");
    const blob = new Blob(["\\ufeff" + conteudo], {{ type: "text/csv;charset=utf-8" }});
    const link = document.createElement("a");
    link.href = URL.createObjectURL(blob);
    link.download = "{escape(titulo)}.csv";
    link.click();
    URL.revokeObjectURL(link.href);
}}

atualizarResumo();
</script>
</body>
</html>"""


def processar_arquivo_estoque(caminho_origem, caminho_destino, titulo):
    print()
    print("=" * 80)
    print(f"[ESTOQUE] Processando: {caminho_origem.name}")
    print(f"Título: {titulo}")
    print("=" * 80)

    texto = ler_arquivo(caminho_origem)
    data = extrair_data_estoque(texto)
    totais = extrair_totais_estoque(texto)
    registros = extrair_registros_estoque(texto)

    print(f"✅ Total de registros: {len(registros)}")

    html_final = gerar_html_estoque(titulo=titulo, data=data, registros=registros, totais=totais)

    caminho_destino.parent.mkdir(parents=True, exist_ok=True)

    with open(caminho_destino, "w", encoding="utf-8") as arquivo:
        arquivo.write(html_final)

    print(f"✅ Arquivo gerado em: {caminho_destino}")


# ============================================================
# MOTOR 2 — TRATAMENTO DE PRODUÇÃO (demais .htm)
# ============================================================

def status_da_imagem(src):
    up = (src or "").upper()

    if "SEPARADO.GIF" in up:
        return "SEPARADO", "sep"
    if "PONTEADO.GIF" in up:
        return "PONTEADO", "pon"
    if "AGUARDASEPARAR" in up:
        return "AGUARDANDO SEPARAÇÃO", "agu"
    if "LIBERADO.GIF" in up:
        return "LIBERADO", "lib"
    if "DECAPADO.GIF" in up:
        return "DECAPADO", "dec"
    if "SERRADO.GIF" in up:
        return "SERRADO", "ser"
    if "TREFILADO.GIF" in up:
        return "TREFILADO", "tre"
    if "ENDIREITADO" in up:
        return "ENDIREITADO", "tre"
    if "ESPECIAL" in up:
        return "ESPECIAL", "esp"

    return "", ""


def extrair_data_producao(texto):
    m = re.search(
        r"atualizada\s+em\s*(\d{2}/\d{2}/\d{4}).{0,60}?(\d{2}:\d{2}:\d{2})",
        texto, re.IGNORECASE | re.DOTALL,
    )

    if m:
        return f"{m.group(1)} às {m.group(2)}"

    return datetime.now().strftime("%d/%m/%Y às %H:%M:%S")


def extrair_registros_producao(html_bruto):
    """
    Extrai os registros da tabela de produção.

    A leitura usa primeiro somente as células diretamente existentes
    dentro de cada <tr>. Isso evita que células mal fechadas do HTML
    sejam incorporadas ao campo Aço ou às colunas seguintes.
    """

    soup = BeautifulSoup(html_bruto, "html.parser")
    linhas_tr = soup.find_all("tr")

    print(f"   Linhas <tr> identificadas: {len(linhas_tr)}")

    registros = []

    for tr in linhas_tr:
        # Primeiro tenta somente as células diretas da linha.
        celulas = tr.find_all(["th", "td"], recursive=False)

        # Fallback para alguns HTML antigos que possuem <td> aninhado.
        if len(celulas) < 14:
            celulas = tr.find_all(["th", "td"], recursive=True)

        # Se ainda não houver células suficientes, pula esta linha.
        if len(celulas) < 14: # Mantido 14 como um limite mínimo razoável
            continue

        def texto_da_celula(celula):
            """
            Extrai apenas o texto da célula.
            Imagens não substituem o conteúdo textual.
            """
            return limpar_texto(celula.get_text(" ", strip=True))

        valores_extraidos = [texto_da_celula(celula) for celula in celulas]

        # A primeira coluna precisa ser a Ordem de Produção.
        # Verifica se o primeiro valor é um número de ordem de produção válido.
        primeiro_texto = normalizar_texto(valores_extraidos[0])
        primeiro_sem_espacos = re.sub(r"\s+", "", primeiro_texto)

        if not re.fullmatch(r"\d{5,}", primeiro_sem_espacos):
            continue

        # Procura o status somente pelas imagens da linha.
        status_txt = ""
        status_cls = ""

        for img in tr.find_all("img"):
            status_txt, status_cls = status_da_imagem(
                img.get("src", "")
            )

            if status_txt:
                break

        # Garante que temos exatamente 15 posições para desempacotar,
        # preenchendo com strings vazias se houver menos, ou agrupando
        # o excesso na observação se houver mais.
        valores = valores_extraidos[:] # Copia para não modificar a lista original

        # Se houver mais de 15 células, as excedentes pertencem
        # ao conteúdo final da observação.
        if len(valores) > 15:
            observacao_extra = " ".join(
                valor for valor in valores[14:] if valor
            )
            valores = valores[:14] + [observacao_extra]
        # Garante pelo menos 15 posições, conforme HEADERS_PRODUCAO.
        while len(valores) < 15:
            valores.append("")

        (
            o_pr,
            lote,
            pf_l,
            bit_l,
            aco, # <-- AQUI ESTÁ A COLUNA AÇO
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

        # Apenas limpa o texto, sem tentar separar.
        # O valor de 'aco' já deve ser o conteúdo da 5ª célula.
        aco = limpar_texto(aco)

        # A quantidade pode vir como 1.234,56 ou 1234.
        qtde_limpa = limpar_texto(qtde)
        qtde_numero = re.sub(r"[^\d]", "", qtde_limpa)
        qtde_num = int(qtde_numero) if qtde_numero else 0

        # O status visual encontrado na imagem tem prioridade.
        # Se não houver imagem, aproveita o texto da coluna Status.
        if not status_txt and status_coluna:
            status_txt = limpar_texto(status_coluna)
            status_cls = ""

        registros.append({
            "O.Pr.": o_pr,
            "Lote": lote,
            "Pf.L": pf_l,
            "Bit.L": bit_l,
            "Aço": aco,
            "Pf": pf,
            "Ac": ac,
            "Bit.": bit_,
            "Tol.": tol,
            "Cliente": cliente,
            "Qtde": qtde,
            "Prazo Dado": prazo,

            # Conforme o padrão solicitado:
            # PCP fica vazio.
            "P.C.P": "",

            "Status": status_txt,
            "StatusClasse": status_cls,
            "Observações": observacoes,
            "QtdeNum": qtde_num,
        })

    print(f"   Registros aproveitados: {len(registros)}")

    return registros


    for tr in linhas_tr:
        # Primeiro tenta somente as células diretas da linha.
        celulas = tr.find_all(["th", "td"], recursive=False)

        # Fallback para alguns HTML antigos que possuem <td> aninhado.
        if len(celulas) < 14:
            celulas = tr.find_all(["th", "td"], recursive=True)

        if len(celulas) < 14:
            continue

        def texto_da_celula(celula):
            """
            Extrai apenas o texto da célula.
            Imagens não substituem o conteúdo textual.
            """
            return limpar_texto(celula.get_text(" ", strip=True))

        valores = [texto_da_celula(celula) for celula in celulas]

        # A primeira coluna precisa ser a Ordem de Produção.
        primeiro_texto = normalizar_texto(valores[0])

        # Remove espaços que possam existir em números.
        primeiro_sem_espacos = re.sub(r"\s+", "", primeiro_texto)

        if not re.fullmatch(r"\d{5,}", primeiro_sem_espacos):
            continue

        # Procura o status somente pelas imagens da linha.
        status_txt = ""
        status_cls = ""

        for img in tr.find_all("img"):
            status_txt, status_cls = status_da_imagem(
                img.get("src", "")
            )

            if status_txt:
                break

        # Garante pelo menos 15 posições, conforme HEADERS_PRODUCAO.
        while len(valores) < 15:
            valores.append("")

        # Se houver mais de 15 células, as excedentes pertencem
        # ao conteúdo final da observação.
        if len(valores) > 15:
            observacao_extra = " ".join(
                valor for valor in valores[14:] if valor
            )
            valores = valores[:14] + [observacao_extra]

        (
            o_pr,
            lote,
            pf_l,
            bit_l,
            aco,
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

        # Correção da coluna Aço:
        # Quando o HTML vem malformado, a quinta célula pode conter
        # também os valores das colunas seguintes.
        # Neste relatório, o valor do aço é o primeiro item da célula.

        aco = limpar_texto(aco)

        if aco:
            aco = aco.split(maxsplit=1)[0].strip()

        # A quantidade pode vir como 1.234,56 ou 1234.
        qtde_limpa = limpar_texto(qtde)
        qtde_numero = re.sub(r"[^\d]", "", qtde_limpa)
        qtde_num = int(qtde_numero) if qtde_numero else 0

        # O status visual encontrado na imagem tem prioridade.
        # Se não houver imagem, aproveita o texto da coluna Status.
        if not status_txt and status_coluna:
            status_txt = limpar_texto(status_coluna)
            status_cls = ""

        registros.append({
            "O.Pr.": o_pr,
            "Lote": lote,
            "Pf.L": pf_l,
            "Bit.L": bit_l,
            "Aço": aco,
            "Pf": pf,
            "Ac": ac,
            "Bit.": bit_,
            "Tol.": tol,
            "Cliente": cliente,
            "Qtde": qtde,
            "Prazo Dado": prazo,

            # Conforme o padrão solicitado:
            # PCP fica vazio.
            "P.C.P": "",

            "Status": status_txt,
            "StatusClasse": status_cls,
            "Observações": observacoes,
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
