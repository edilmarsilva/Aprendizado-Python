import re
import shutil
from pathlib import Path
from datetime import datetime
from bs4 import BeautifulSoup

# ================== CONFIGURAÇÃO ==================
PASTA_ORIGEM = r"C:\FTP"
PASTA_DESTINO = r"C:\FTP 2.0"

HEADERS = ["O.Pr.", "Lote", "Pf.L", "Bit.L", "Aço", "Pf", "Ac", "Bit.", "Tol.",
           "Cliente", "Qtde", "Prazo Dado", "P.C.P", "Status", "Observações"]

# ================== LIMPEZA DE NOMES CORROMPIDOS ==================
def limpar_nome_arquivo(nome):
    nome = re.sub(r'[^a-zA-Z0-9._-]', '', nome)
    nome = re.sub(r'\.+', '.', nome)
    return nome if nome else 'arquivo.htm'

def renomear_corrompidos(pasta):
    pasta_path = Path(pasta)
    if not pasta_path.exists():
        return 0
    contador = 0
    for item in pasta_path.rglob('*'):
        if item.is_file():
            nome_limpo = limpar_nome_arquivo(item.name)
            if item.name != nome_limpo:
                novo = item.parent / nome_limpo
                if novo.exists():
                    base, ext = nome_limpo.rsplit('.', 1) if '.' in nome_limpo else (nome_limpo, 'htm')
                    i = 1
                    while (item.parent / f"{base}_{i}.{ext}").exists():
                        i += 1
                    novo = item.parent / f"{base}_{i}.{ext}"
                item.rename(novo)
                contador += 1
    return contador

# ================== LEITURA ==================
def ler_arquivo_como_texto(caminho):
    caminho = Path(caminho)
    if not caminho.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {caminho}")
    for enc in ("cp1252", "latin-1", "utf-8"):
        try:
            with open(caminho, "r", encoding=enc, errors="strict") as f:
                return f.read()
        except UnicodeDecodeError:
            continue
    with open(caminho, "r", encoding="utf-8", errors="replace") as f:
        return f.read()

# ================== TÍTULO A PARTIR DO NOME DO ARQUIVO ==================
def extrair_titulo_do_nome_arquivo(caminho_arquivo):
    """
    O <title> do HTML original vem corrompido e repetido em vários
    arquivos diferentes (ex: "Açofera" em todos). Por isso o título da
    listagem passa a ser extraído do próprio nome do arquivo, pegando a
    parte alfabética inicial (antes do primeiro número), que é onde fica
    o nome real de cada relatório.
    """
    nome = Path(caminho_arquivo).stem
    m = re.match(r"^([A-Za-zÀ-ÖØ-öø-ÿ]+)", nome)
    if m:
        prefixo = m.group(1)
        return prefixo[:1].upper() + prefixo[1:].lower()
    return nome if nome else "Relatório"

# ================== EXTRAÇÃO ==================
def extrair_data(texto):
    m = re.search(r"atualizada\s+em\s*(\d{2}/\d{2}/\d{4}).{0,60}?(\d{2}:\d{2}:\d{2})",
                  texto, re.IGNORECASE | re.DOTALL)
    if m:
        return f"{m.group(1)} às {m.group(2)}"
    return datetime.now().strftime("%d/%m/%Y às %H:%M:%S")

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

def extrair_registros(html_bruto):
    """
    Usa BeautifulSoup (tolerante a HTML malformado) para pegar TODAS as
    linhas <tr> do documento, extrai as células de cada uma individualmente
    e filtra apenas as linhas cuja primeira célula é numérica com 5+ dígitos
    (identifica linha de dado real, ignorando cabeçalho e ruído estrutural).
    Se o arquivo não tiver nenhuma linha de dado, retorna lista vazia — e
    a estrutura HTML é gerada mesmo assim, apenas sem registros na tabela.
    """
    soup = BeautifulSoup(html_bruto, "html.parser")
    linhas_tr = soup.find_all("tr")

    registros = []
    for tr in linhas_tr:
        celulas = tr.find_all(["th", "td"], recursive=True)
        if len(celulas) < 14:
            continue

        primeiro_texto = celulas[0].get_text(strip=True)
        if not re.match(r"^\d{5,}$", primeiro_texto):
            continue

        valores = []
        status_txt, status_cls = "", ""
        for c in celulas:
            img = c.find("img")
            if img:
                status_txt, status_cls = status_da_imagem(img.get("src", ""))
                valores.append(None)
            else:
                valores.append(c.get_text(strip=True))

        if len(valores) < 14:
            continue

        o_pr, lote, pf_l, bit_l, aco, pf, ac, bit_, tol, cliente, qtde, prazo = valores[0:12]
        observacoes = valores[-1] if valores[-1] is not None else ""

        qtde_num = re.sub(r"[.\s]", "", qtde or "").replace(",", "")
        qtde_num = int(qtde_num) if qtde_num.isdigit() else 0

        registros.append({
            "O.Pr.": o_pr, "Lote": lote, "Pf.L": pf_l, "Bit.L": bit_l, "Aço": aco,
            "Pf": pf, "Ac": ac, "Bit.": bit_, "Tol.": tol, "Cliente": cliente,
            "Qtde": qtde, "Prazo Dado": prazo, "P.C.P": "",
            "Status": status_txt, "StatusClasse": status_cls,
            "Observações": observacoes, "QtdeNum": qtde_num
        })

    return registros

# ================== GERAÇÃO DO HTML ==================
def gerar_linha(r):
    status_html = f'<span class="st {r["StatusClasse"]}">{r["Status"]}</span>' if r["Status"] else ""
    return f"""<tr data-status="{r['Status']}" data-qtde="{r['QtdeNum']}">
<td>{r['O.Pr.']}</td><td>{r['Lote']}</td><td>{r['Pf.L']}</td><td>{r['Bit.L']}</td>
<td>{r['Aço']}</td><td>{r['Pf']}</td><td>{r['Ac']}</td><td>{r['Bit.']}</td>
<td>{r['Tol.']}</td><td>{r['Cliente']}</td><td>{r['Qtde']}</td><td>{r['Prazo Dado']}</td>
<td>{r['P.C.P']}</td><td data-s="{r['Status']}">{status_html}</td><td>{r['Observações']}</td>
</tr>"""

def gerar_html(titulo, data, registros):
    linhas = "\n".join(gerar_linha(r) for r in registros)
    headers_html = "".join(f"<th>{h}</th>" for h in HEADERS)

    return f"""<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{titulo}</title>
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
<h1>{titulo}</h1>
<small>Listagem atualizada em {data}</small>
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

function fmt(v) {{ return (v/1000).toFixed(3).replace('.', ',') + ' KG'; }}

function somas() {{
  let total = 0, prontos = 0, filtroTxt = st.value, filtroSoma = 0;
  rows.forEach(r => {{
    if (!r.hidden) {{
      const qtde = parseFloat(r.getAttribute('data-qtde')) || 0;
      const status = r.getAttribute('data-status') || '';
      total += qtde;
      if (status === 'LIBERADO') prontos += qtde;
      if (filtroTxt && status === filtroTxt) filtroSoma += qtde;
    }}
  }});
  const s = document.querySelector('#summary');
  s.innerHTML = '';
  s.innerHTML += `<div class="card"><small>Total em processamento</small><b>${{fmt(total)}}</b></div>`;
  s.innerHTML += `<div class="card"><small>Prontos para retirada</small><b>${{fmt(prontos)}}</b></div>`;
  if (filtroTxt) s.innerHTML += `<div class="card"><small>${{filtroTxt}}</small><b>${{fmt(filtroSoma)}}</b></div>`;
}}

function filtrar() {{
  let n = 0;
  rows.forEach(r => {{
    const ok = (!q.value || r.innerText.toLowerCase().includes(q.value.toLowerCase())) &&
               (!st.value || r.getAttribute('data-status') === st.value);
    r.hidden = !ok;
    if (ok) n++;
  }});
  document.querySelector('#count').textContent = n + ' registro' + (n === 1 ? '' : 's') + ' exibido' + (n === 1 ? '' : 's');
  somas();
}}

q.oninput = st.onchange = filtrar;

function clearF() {{ q.value = ''; st.value = ''; filtrar(); }}

function csv() {{
  const rs = rows.filter(r => !r.hidden);
  const heads = [...document.querySelectorAll('th')].map(x => x.innerText);
  const out = [heads, ...rs.map(r => [...r.cells].map(c => c.innerText.trim()))]
    .map(a => a.map(x => '"' + x.replaceAll('"', '""') + '"').join(';')).join('\\n');
  const a = document.createElement('a');
  a.href = URL.createObjectURL(new Blob(['\\ufeff' + out], {{type:'text/csv'}}));
  a.download = '{titulo}.csv';
  a.click();
}}

somas();
</script>
</body>
</html>"""

# ================== PROCESSAMENTO DE UM ARQUIVO ==================
def processar_arquivo_htm(caminho_origem, caminho_destino):
    """
    Sempre gera a estrutura aprimorada para arquivos .htm, mesmo quando
    nenhum registro é encontrado — nesse caso, a tabela aparece vazia,
    mas com o layout, cabeçalhos, filtros e somas normais.
    """
    texto = ler_arquivo_como_texto(caminho_origem)
    titulo = extrair_titulo_do_nome_arquivo(caminho_origem)
    data = extrair_data(texto)
    registros = extrair_registros(texto)

    html_final = gerar_html(titulo, data, registros)
    with open(caminho_destino, "w", encoding="utf-8") as f:
        f.write(html_final)

    return len(registros)

# ================== EXECUÇÃO PRINCIPAL ==================
def processar():
    origem = Path(PASTA_ORIGEM)
    destino = Path(PASTA_DESTINO)

    print("\n" + "=" * 70)
    print("🔧 ETAPA 1: LIMPANDO NOMES CORROMPIDOS")
    print("=" * 70 + "\n")

    if not origem.exists():
        print(f"❌ Pasta de origem não encontrada: {origem}")
        input("\nPressione ENTER para sair...")
        return

    renomeados = renomear_corrompidos(origem)
    print(f"✅ Total renomeado: {renomeados}\n")

    print("=" * 70)
    print("📂 ETAPA 2: PROCESSANDO ARQUIVOS")
    print("=" * 70 + "\n")

    # Sobrescreve a pasta de destino se já existir
    if destino.exists():
        shutil.rmtree(destino)
    destino.mkdir(parents=True, exist_ok=True)

    processados = 0
    sem_registros = 0
    copiados = 0
    falhas = 0

    for item in sorted(origem.rglob('*')):
        rel = item.relative_to(origem)
        dest = destino / rel

        if item.is_dir():
            dest.mkdir(parents=True, exist_ok=True)
            continue

        if item.suffix.lower() == '.htm':
            try:
                print(f"🔄 {item.name}")
                n = processar_arquivo_htm(item, dest)
                if n > 0:
                    print(f"   ✅ {n} registros extraídos\n")
                    processados += 1
                else:
                    print(f"   ⚠️ Estrutura gerada, mas sem registros encontrados\n")
                    sem_registros += 1
            except Exception as e:
                print(f"   ❌ Erro ao processar, copiado original: {e}\n")
                shutil.copy2(item, dest)
                falhas += 1
        else:
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(item, dest)
            copiados += 1

    print("=" * 70)
    print("✨ CONCLUÍDO!")
    print("=" * 70)
    print(f"✅ Processados com registros: {processados}")
    print(f"⚠️ Processados sem registros (estrutura gerada mesmo assim): {sem_registros}")
    print(f"📄 Copiados (outros): {copiados}")
    if falhas:
        print(f"❌ Falhas: {falhas}")
    print(f"\n📂 Verifique: {destino}\n")

if __name__ == "__main__":
    try:
        processar()
    except Exception as e:
        print(f"\n❌ Erro inesperado: {e}")
    input("\nPressione ENTER para fechar...")
