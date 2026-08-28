# DARMA SUS

Consulta pública às filas do SUS no Rio Grande do Norte: a lista de cirurgias eletivas do estado e as
solicitações de consultas e exames especializados, município por município.

Site estático (GitHub Pages) + um workflow que copia os dados oficiais uma vez por dia. Nenhum
servidor, nenhum banco.

## Por que existe

O RN publica esses números, mas em dois lugares que não conversam entre si e não guardam histórico:
uma API de transparência que alimenta a Sala de Situação do Regula RN, e um painel Power BI com a
fila cirúrgica. Este projeto lê os dois, guarda uma cópia diária e apresenta o resultado numa página
que qualquer pessoa entende.

**O que estes dados não são:** tempo de espera em dias. Nenhuma das duas fontes publica há quanto
tempo cada pessoa aguarda — apenas quantas estão na lista e quantos pedidos entram por mês. Para o
tempo real seria preciso pedir, via LAI, a extração com data da solicitação e data do atendimento.

## Fontes

| Fonte | O que dá | Como é lida |
|---|---|---|
| [Regula RN](https://ambulatorial.saude.rn.gov.br/sala-situacao) (SESAP-RN / LAIS-UFRN) | solicitações de consultas e exames por subgrupo, por município e motivos de cancelamento | API REST pública, sem autenticação |
| [Painel Fila de Cirurgias Eletivas](https://poli.control.rn.gov.br/monitoramento/saude/fila-cirurgias-eletivas/) (SESAP-RN / POLI) | total de pacientes na lista e ranking de procedimentos | não tem API — leitura do painel Power BI com Playwright |

### A API do Regula RN

Base: `https://api.ambulatorial.lais.ufrn.br/api`. Datas no formato `dd/mm/aaaa`.

```
GET /transparencia/solicitacoes_por_subgrupo?de=01/01/2026&ate=31/12/2026
GET /transparencia/solicitacoes_municipios?de=…&ate=…
GET /transparencia/motivos_cancelamento_pie?de=…&ate=…
GET /transparencia/motivos_cancelamento_rank_solicitantes?de=…&ate=…
GET /transparencia/solicitacoes_municipios_excel?de=…&ate=…          (microdados)
GET /integracoes/municipio?q=natal                                    (10 itens por chamada)
GET /integracoes/regiao_saude
```

As rotas `/procedimentos/*` exigem login e retornam 401 — por isso o filtro por procedimento
específico não existe aqui, só por subgrupo.

**A API não envia cabeçalhos CORS para origens externas.** Uma página estática não consegue chamá-la
direto do navegador; daí a coleta rodar no GitHub Actions e o site ler apenas arquivos do próprio
repositório.

## Estrutura

```
index.html                     o site inteiro (sem dependências externas)
data/ambulatorial.json         série mensal por subgrupo e por município, cancelamentos
data/fila_cirurgias.json       total na fila e ranking de procedimentos
data/historico.csv             uma linha por coleta — a série histórica que os painéis não guardam
data/agenda.json               mutirões e ações marcadas (mantido à mão; ver abaixo)
scripts/coletar.py             o coletor
scripts/_seed.py               gera o snapshot inicial (só precisou rodar uma vez)
.github/workflows/coleta.yml   coleta diária às 6h de Natal
.github/workflows/pages.yml    publica a raiz do repo no Pages, sem Jekyll
```

### O filtro de período

A barra no topo do site cobre qualquer intervalo de meses entre jan/2025 e o mês atual. Os números
de consultas e exames — tiles, gráfico, tabela e resposta da busca — respondem a ela. A fila
cirúrgica não: ela é uma foto do momento, não um acumulado, então o número segue sendo o da leitura
mais recente qualquer que seja o período.

Para isso funcionar sem chamar a API ao vivo (ela não manda CORS), o coletor busca o total de cada
município **mês a mês** — uma requisição por mês — e grava a série em `data/ambulatorial.json`.

### Mutirões (`data/agenda.json`)

Não sai de API nenhuma: é uma lista mantida à mão. Cada item:

```json
{"data": "2026-09-14", "ate": "2026-09-16", "titulo": "Mutirão de catarata",
 "local": "Hospital Regional de João Câmara", "fonte": "https://..."}
```

`ate` é opcional. Eventos com data passada somem sozinhos, e a seção inteira fica oculta enquanto a
lista estiver vazia — então não há risco de o site anunciar um mutirão que já aconteceu.

## Como publicar

1. **Settings → Pages → Source: Deploy from a branch**, branch `main`, pasta `/ (root)`.
2. **Settings → Actions → General → Workflow permissions:** marcar *Read and write permissions*
   (o workflow comita os dados de volta no repositório).
   Se preferir publicar sem Jekyll, troque *Source* para **GitHub Actions** — o `pages.yml` cuida do resto.
3. **Actions → Coleta diária → Run workflow** para a primeira coleta real. Depois disso ela roda
   sozinha todo dia às 09:00 UTC (06:00 em Natal).

O site já sobe funcionando: os JSONs em `data/` trazem um snapshot de 28/08/2026.

## Rodar local

```bash
pip install -r requirements.txt
python -m playwright install chromium
python scripts/coletar.py      # regrava data/
python -m http.server 8000     # abre em http://localhost:8000
```

## Manutenção

O ponto frágil é a leitura do Power BI: se a SESAP mudar o layout do painel, o coletor para de achar
os números. Ele foi escrito para falhar de forma parcial — a coleta ambulatorial continua, o site
segue com o último dado da fila, e o campo `texto_bruto` em `fila_cirurgias.json` guarda o texto lido
para facilitar o conserto.

## Licença e ressalvas

Dados públicos da SESAP-RN, reproduzidos com indicação de fonte. Este projeto não é um canal oficial
da secretaria, não agenda atendimentos e não consulta a posição individual de ninguém na fila — para
isso, procure a unidade de saúde ou a central de regulação do seu município.
