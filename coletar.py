# -*- coding: utf-8 -*-
"""
Coletor do DARMA SUS.

Roda no GitHub Actions (ou local) e grava em data/:
  - ambulatorial.json      solicitacoes do Regula RN (API publica, sem token)
  - fila_cirurgias.json    fila de cirurgias eletivas (painel Power BI da SESAP)
  - historico.csv          uma linha por coleta, para montar serie historica

Por que raspar o Power BI: o painel da fila cirurgica nao tem API. O endpoint
interno do Power BI ate existe, mas exige montar consultas DAX e quebra a cada
mudanca do relatorio. Ler o texto renderizado e mais simples e mais estavel.
"""

import csv
import json
import os
import re
import sys
from datetime import date, datetime, timezone, timedelta

import requests

API = "https://api.ambulatorial.lais.ufrn.br/api"
POWERBI_FILA = (
    "https://app.powerbi.com/view?r=eyJrIjoiNWUwOGNlZmEtOGQ4NC00N2Y1LTkzODQt"
    "MTYxOTcyM2RiNDU5IiwidCI6Ijk5YjA1YzllLWE3NjUtNDAwYy1iYTA3LTMzYmIxMGU5YjJiMiJ9"
)
DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data")
BRT = timezone(timedelta(hours=-3))
INICIO_SERIE = "01/01/2025"
TIMEOUT = 60


def agora():
    return datetime.now(BRT).replace(microsecond=0).isoformat()


def br(d):
    return d.strftime("%d/%m/%Y")


# --------------------------------------------------------------------------- #
# 1. Regula RN — API publica
# --------------------------------------------------------------------------- #
def api(rota, de, ate):
    r = requests.get(f"{API}/transparencia/{rota}", params={"de": de, "ate": ate}, timeout=TIMEOUT)
    r.raise_for_status()
    return r.json()


def nomes_municipios():
    """Mapa codigo IBGE (6 digitos) -> nome. Tenta o IBGE; cai para o proprio Regula."""
    try:
        r = requests.get(
            "https://servicosdados.ibge.gov.br/api/v1/localidades/estados/24/municipios",
            timeout=TIMEOUT,
        )
        r.raise_for_status()
        return {str(m["id"])[:6]: m["nome"] for m in r.json()}
    except Exception as e:  # noqa: BLE001
        print(f"  IBGE indisponivel ({e}); usando /integracoes/municipio", file=sys.stderr)

    # O endpoint do Regula devolve no maximo 10 itens por chamada: varremos prefixos.
    letras = "abcdefghijklmnopqrstuvwxyz"
    mapa = {}
    for a in letras:
        for b in letras + " ":
            try:
                r = requests.get(f"{API}/integracoes/municipio", params={"q": a + b}, timeout=TIMEOUT)
                for m in r.json() or []:
                    mapa[m["ibge"]] = m["name"]
            except Exception:  # noqa: BLE001
                continue
    return mapa


def coletar_ambulatorial():
    hoje = date.today()
    inicio_ano = date(hoje.year, 1, 1)

    serie = api("solicitacoes_por_subgrupo", INICIO_SERIE, br(hoje))
    municipios = api("solicitacoes_municipios", br(inicio_ano), br(hoje))
    cancel = api("motivos_cancelamento_pie", br(inicio_ano), br(hoje))

    mapa = nomes_municipios()
    muns = sorted(
        (
            {"ibge": str(c), "nome": mapa.get(str(c)[:6], "Municipio " + str(c)), "total": v}
            for c, v in municipios
        ),
        key=lambda m: -m["total"],
    )

    subgrupos = sorted(
        ({"nome": g["nome"], "data": g["data"], "total": g["total"]} for g in serie["grupos"]),
        key=lambda g: -g["total"],
    )

    motivos = sorted(
        ({"nome": m["name"], "qtd": m["y"]} for m in cancel), key=lambda m: -m["qtd"]
    )[:12]

    return {
        "atualizado_em": agora(),
        "fonte": "Regula RN / SESAP-RN — api.ambulatorial.lais.ufrn.br",
        "periodo_serie": {"de": INICIO_SERIE, "ate": br(hoje)},
        "periodo_municipios": {"de": br(inicio_ano), "ate": br(hoje)},
        "meses": serie["meses"],
        "subgrupos": subgrupos,
        "municipios": muns,
        "motivos_cancelamento": motivos,
    }


# --------------------------------------------------------------------------- #
# 2. Fila de cirurgias eletivas — painel Power BI
# --------------------------------------------------------------------------- #
def _num(txt):
    """'17,24 Mil' -> 17240 ; '47703' -> 47703 ; '1.391' -> 1391"""
    txt = txt.strip()
    mult = 1000 if re.search(r"\bmil\b", txt, re.I) else 1
    txt = re.sub(r"\bmil\b", "", txt, flags=re.I).strip()
    txt = txt.replace(".", "").replace(",", ".")
    try:
        return int(round(float(txt) * mult))
    except ValueError:
        return None


def coletar_fila():
    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        nav = p.chromium.launch()
        pag = nav.new_page(viewport={"width": 1600, "height": 1200})
        pag.goto(POWERBI_FILA, wait_until="networkidle", timeout=120_000)
        pag.wait_for_timeout(20_000)  # os visuais carregam depois do networkidle
        texto = pag.inner_text("body")
        nav.close()

    linhas = [l.strip() for l in texto.split("\n") if l.strip()]

    def depois_de(rotulo):
        """No Power BI o valor de um cartao aparece imediatamente antes ou depois do rotulo."""
        for i, l in enumerate(linhas):
            if rotulo.lower() in l.lower():
                for j in (i - 1, i + 1, i + 2):
                    if 0 <= j < len(linhas):
                        v = _num(linhas[j])
                        if v:
                            return v
        return None

    procs, hosps = [], []
    padrao_proc = re.compile(r"^(\d{9,10})\s+(.+?)\s*$")
    # O ranking vem como blocos de rotulos seguidos dos respectivos valores.
    rotulos_proc = [m.groups() for l in linhas if (m := padrao_proc.match(l))]
    valores = [v for l in linhas if (v := _num(l)) and v > 50]
    for (cod, nome), qtd in zip(rotulos_proc, valores[-len(rotulos_proc):] if rotulos_proc else []):
        procs.append({"codigo": cod, "nome": nome.strip(" .…"), "qtd": qtd})

    return {
        "atualizado_em": agora(),
        "fonte": "Painel Regula Cirurgias — SESAP-RN / POLI (atualizado a cada 2h)",
        "situacao": "Pendente",
        "total_lista": depois_de("Quantidade de pacientes em Lista"),
        "agendas": depois_de("Agendas"),
        "vagas_ofertadas": depois_de("Vagas Ofertadas"),
        "ranking_procedimentos": procs[:10],
        "ranking_estabelecimentos": hosps,
        "texto_bruto": texto[:4000],  # ajuda a depurar quando o layout do painel muda
    }


# --------------------------------------------------------------------------- #
def escrever(nome, obj):
    caminho = os.path.join(DATA, nome)
    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=1)
    print(f"  gravado {nome}")


def anexar_historico(amb, fila):
    caminho = os.path.join(DATA, "historico.csv")
    novo = not os.path.exists(caminho)
    with open(caminho, "a", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        if novo:
            w.writerow(["data", "fila_cirurgias", "solicitacoes_ano", "municipios_com_dado"])
        w.writerow([
            date.today().isoformat(),
            (fila or {}).get("total_lista") or "",
            sum(m["total"] for m in amb["municipios"]) if amb else "",
            len(amb["municipios"]) if amb else "",
        ])


def main():
    os.makedirs(DATA, exist_ok=True)
    falhas = []

    print("Regula RN (ambulatorial)...")
    amb = None
    try:
        amb = coletar_ambulatorial()
        escrever("ambulatorial.json", amb)
    except Exception as e:  # noqa: BLE001
        falhas.append(f"ambulatorial: {e}")
        print(f"  FALHOU: {e}", file=sys.stderr)

    print("Fila de cirurgias (Power BI)...")
    fila = None
    try:
        fila = coletar_fila()
        if not fila.get("total_lista"):
            raise RuntimeError("painel carregou mas nao achei o total da lista")
        escrever("fila_cirurgias.json", fila)
    except Exception as e:  # noqa: BLE001
        falhas.append(f"fila: {e}")
        print(f"  FALHOU: {e}", file=sys.stderr)

    if amb:
        anexar_historico(amb, fila)

    # Uma fonte pode cair sem derrubar a outra; o site segue com o dado anterior.
    if len(falhas) == 2:
        print("As duas coletas falharam.", file=sys.stderr)
        sys.exit(1)
    if falhas:
        print("Coleta parcial: " + "; ".join(falhas), file=sys.stderr)


if __name__ == "__main__":
    main()
