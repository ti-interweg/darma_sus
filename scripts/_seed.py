# -*- coding: utf-8 -*-
"""Gera os JSONs iniciais (snapshot capturado em 28/08/2026) na pasta data/.
Depois da primeira execucao do workflow, quem atualiza esses arquivos e o coletar.py."""
import json, os, datetime

BASE = os.path.join(os.path.dirname(__file__), "..", "data")
os.makedirs(BASE, exist_ok=True)

MESES = "01/25,02/25,03/25,04/25,05/25,06/25,07/25,08/25,09/25,10/25,11/25,12/25,01/26,02/26,03/26,04/26,05/26,06/26,07/26,08/26".split(",")

SUB = """Consultas / Atendimentos / Acompanhamentos;0,0,6,47,41,74,517,527,467,475,328,2535,19308,28668,35340,26378,28995,28237,33616,28916
Diagnóstico por tomografia;3705,3776,3426,3800,4251,3653,4524,4191,4202,4035,4062,3898,4332,4118,5439,4399,4709,6234,5996,5847
Diagnóstico por ultrasonografia;1,8,2,0,3,0,0,0,0,0,108,1558,7554,9843,12937,9330,10479,10066,13602,11310
Diagnóstico por radiologia;909,1096,1067,1208,1261,1196,1516,1353,1270,1302,1080,1315,3596,5050,7297,5217,5965,5592,7279,6415
Diagnóstico por ressonância magnética;2235,2583,2230,2541,2907,2506,3187,2782,3014,2972,2890,2583,2534,2635,4087,3071,3404,2985,4098,4007
Métodos diagnósticos em especialidades;120,108,106,93,142,118,159,117,120,155,427,752,2821,3668,4195,2971,3786,3236,4026,3325
Tratamento em nefrologia;1106,932,922,1097,1048,854,1055,946,949,1145,960,1024,1085,963,1188,1122,868,1047,973,1031
Diagnóstico por medicina nuclear in vivo;874,977,736,891,871,778,1039,910,959,1020,745,824,894,756,1288,916,978,966,1109,972
Diagnóstico por endoscopia;0,0,0,0,0,0,0,0,0,0,2,270,1396,1888,2684,1904,2453,2294,2569,2219
Fisioterapia;0,0,0,0,0,0,0,0,0,0,0,182,971,1047,1299,1047,1087,1065,1236,1082
Diagnóstico por anatomia patológica e citopatologia;0,0,0,0,0,0,0,0,0,0,0,36,940,1521,0,3,19,24,54,744
Terapias especializadas;79,110,120,134,132,107,126,121,160,142,116,127,101,123,179,143,237,199,247,210
Cirurgia em nefrologia;126,129,113,169,129,118,123,159,155,127,128,136,136,104,147,134,146,98,156,103
Coleta de material;0,0,0,0,0,0,0,0,0,0,2,40,246,257,321,292,296,310,413,342
Vigilância em saúde;0,0,0,0,0,0,0,0,0,0,0,8,94,272,698,528,454,153,155,141
Diagnóstico por radiologia intervencionista;0,0,0,0,0,0,0,0,0,0,151,124,177,147,164,236,156,198,261,251
Ações coletivas/individuais em saúde;0,0,0,0,0,0,0,0,0,0,1,45,279,291,435,245,173,103,144,72
Diagnóstico em laboratório clínico;0,0,0,0,0,0,0,0,0,0,0,33,286,163,189,104,143,206,273,200
Tratamentos clínicos (outras especialidades);12,7,8,9,9,9,8,10,8,8,7,12,62,104,135,105,135,168,142,153
Atenção em Oncologia;0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,5,8,9,764
Atenção em Saúde Mulher;0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,418
Cirurgia do aparelho da visão;0,0,0,0,0,0,0,0,0,0,0,0,0,1,111,32,0,0,0,0
Atenção em Cardiologia;0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,21,0,45,53
Pequenas cirurgias e cirurgias de pele, tecido subcutâneo e mucosa;0,0,0,0,0,0,0,0,0,0,0,0,0,11,35,37,10,0,0,0
Cirurgia do aparelho digestivo, orgãos anexos e parede abdominal;0,0,0,0,0,0,0,0,0,0,0,0,0,7,19,4,2,0,0,0
Bucomaxilofacial;0,0,0,0,0,0,0,0,0,0,0,0,0,16,11,2,2,0,0,0
Cirurgia das vias aéreas superiores, da face, da cabeça e do pescoço;0,0,0,0,0,0,0,0,0,0,0,0,0,3,1,5,1,0,0,0
Tratamento em oncologia;0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,10,0,0,0
Cirurgia do aparelho geniturinário;0,0,0,0,0,0,0,0,0,0,0,0,0,3,5,0,1,0,0,0"""

MUN_MENSAL = open(os.path.join(os.path.dirname(__file__), "_mun_mensal.txt"), encoding="utf-8").read()

CANCEL = [
    ("2.8 - OUTROS MOTIVOS", 16545), ("1.8 - ALTA POR OUTROS MOTIVOS", 5563),
    ("5.1 - ENCERRAMENTO ADMINISTRATIVO", 2971), ("1.4 - ALTA A PEDIDO", 1280),
    ("1.2 - ALTA MELHORADO", 658), ("3.1 - TRANSFERIDO PARA OUTRO ESTABELECIMENTO", 520),
    ("2.6 - POR MUDANÇA DE PROCEDIMENTO", 470),
    ("4.1 - COM DECLARAÇÃO DE ÓBITO FORNECIDA PELO MÉDICO ASSISTENTE", 370),
    ("1.6 - ALTA POR EVASÃO", 235), ("2.2 - POR INTERCORRÊNCIA", 220),
]

PROCS = [
    ("406020566", "TRATAMENTO (demais procedimentos)", 3348),
    ("407030026", "COLECISTECTOMIA", 2721),
    ("0211040045", "HISTEROSCOPIA (DIAGNÓSTICA)", 2216),
    ("401010074", "EXÉRESE DE TUMOR DE PELE", 2079),
    ("409060135", "HISTERECTOMIA TOTAL", 1447),
    ("405050372", "FACOEMULSIFICAÇÃO (catarata)", 1391),
    ("410010073", "PLÁSTICA MAMÁRIA", 1266),
    ("407040129", "HERNIOPLASTIA UMBILICAL", 1193),
    ("409060194", "MIOMECTOMIA", 1025),
    ("407030034", "COLECISTECTOMIA VIDEOLAPAROSCÓPICA", 835),
]

HOSP = [
    ("SAÚDE DE TODOS - CLÍNICA MÉDICA", 17000), ("HOSPITAL REGIONAL LINDOLFO GOMES VIDAL", 15000),
    ("HOSPITAL REGIONAL DE JOÃO CÂMARA", 13000), ("HOSPITAL DR MARIANO COELHO", 12000),
    ("HOSPITAL REGIONAL NELSON INÁCIO DOS SANTOS", 11000),
    ("HOSPITAL UNIVERSITÁRIO ANA BEZERRA (HUAB)", 11000),
    ("HOSPITAL DR JOSÉ PEDRO BEZERRA", 8000),
    ("SECRETARIA MUNICIPAL DE SAÚDE DE SANTA CRUZ", 6000),
    ("HOSPITAL CENTRAL CORONEL PEDRO GERMANO", 5000),
    ("HOSPITAL MATERNIDADE BELARMINO AMORIM", 5000),
]

subgrupos = []
for line in SUB.strip().split("\n"):
    nome, dados = line.split(";")
    serie = [int(x) for x in dados.split(",")]
    subgrupos.append({"nome": nome, "data": serie, "total": sum(serie)})

municipios = []
for line in MUN_MENSAL.strip().split("\n"):
    ibge, nome, dados = line.split("|")
    serie = [int(x) for x in dados.split(",")]
    municipios.append({"ibge": ibge, "nome": nome, "data": serie, "total": sum(serie)})
municipios.sort(key=lambda m: -m["total"])

agora = "2026-08-28T21:40:00-03:00"

amb = {
    "atualizado_em": agora,
    "fonte": "Regula RN / SESAP-RN — api.ambulatorial.lais.ufrn.br",
    "periodo_serie": {"de": "01/01/2025", "ate": "28/08/2026"},
    "periodo_municipios": {"de": "01/01/2025", "ate": "28/08/2026"},
    "meses": MESES,
    "subgrupos": subgrupos,
    "municipios": municipios,
    "motivos_cancelamento": [{"nome": n, "qtd": q} for n, q in CANCEL],
}

fila = {
    "atualizado_em": agora,
    "fonte": "Painel Regula Cirurgias — SESAP-RN / POLI (atualizado a cada 2h)",
    "situacao": "Pendente",
    "total_lista": 47703,
    "agendas": 17240,
    "vagas_ofertadas": 159536,
    "ranking_procedimentos": [{"codigo": c, "nome": n, "qtd": q} for c, n, q in PROCS],
    "ranking_estabelecimentos": [{"nome": n, "qtd": q} for n, q in HOSP],
    "observacao": "Valores do ranking de estabelecimentos sao aproximados (o painel os exibe arredondados em milhares).",
}

agenda = {
    "atualizado_em": agora,
    "observacao": "Lista mantida a mao. Cada item: {data:'AAAA-MM-DD', ate:'AAAA-MM-DD' (opcional), titulo, local, fonte (url)}.",
    "eventos": [],
}

for nome, obj in (("ambulatorial.json", amb), ("fila_cirurgias.json", fila), ("agenda.json", agenda)):
    with open(os.path.join(BASE, nome), "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=1)
    print("escrito", nome)
