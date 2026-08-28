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

MUN = """2408102|Natal|295126
2403251|Parnamirim|8000
2408003|Mossoró|7391
2402006|Caicó|5859
2407104|Macaíba|5143
2412005|São Gonçalo do Amarante|5072
2400208|Açu|5064
2411205|Santa Cruz|4758
2407203|Macau|4652
2414803|Vera Cruz|4575
2410405|Pureza|3768
2408300|Nova Cruz|3257
2411502|Santo Antônio|3249
2407807|Monte Alegre|3238
2414407|Touros|3212
2404507|Guamaré|3185
2412906|São Tomé|3092
2401404|Baía Formosa|3057
2407500|Maxaranguape|3057
2404606|Ielmo Marinho|2941
2405801|João Câmara|2873
2402600|Ceará-Mirim|2847
2403509|Espírito Santo|2843
2403608|Extremoz|2796
2412203|São José de Mipibu|2716
2408953|Rio do Fogo|2651
2400307|Afonso Bezerra|2618
2404705|Ipanguaçu|2596
2408201|Nísia Floresta|2594
2414209|Tibau do Sul|2590
2403103|Currais Novos|2567
2401701|Bom Jesus|2553
2413904|Taipu|2551
2407708|Montanhas|2492
2401602|Bento Fernandes|2416
2410108|Poço Branco|2382
2414001|Tangará|2369
2402204|Canguaretama|2346
2406601|Lagoa Salgada|2305
2412609|São Paulo do Potengi|2261
2413102|Senador Elói de Souza|2155
2401206|Arês|2058
2409100|Passa e Fica|2027
2413508|Serrinha|2002
2404200|Goianinha|1978
2406502|Lagoa Nova|1968
2400802|Angicos|1965
2406304|Lagoa de Pedras|1917
2405405|Japi|1772
2412559|São Miguel do Gostoso|1760
2402105|Campo Redondo|1713
2400703|Alto do Rodrigues|1656
2405306|Januário Cicco|1602
2411403|Santana do Matos|1570
2406700|Lajes|1519
2409803|Pedro Velho|1514
2402808|Coronel Ezequiel|1465
2406809|Lajes Pintadas|1446
2410306|Serra Caiada|1445
2409704|Pedro Avelino|1397
2401909|Caiçara do Rio do Vento|1370
2406155|Jundiá|1333
2409407|Pau dos Ferros|1221
2401859|Caiçara do Norte|1202
2402709|Cerro Corá|1198
2410900|Riachuelo|1163
2406205|Lagoa d'Anta|1133
2408805|Parazinho|1072
2401503|Barcelona|1036
2405009|Jaçanã|1029
2402303|Caraúbas|1025
2409902|Pendências|995
2412807|São Rafael|959
2402501|Carnaubais|948
2412500|São Miguel|943
2412302|São José do Campestre|934
2409209|Passagem|928
2409605|Pedra Preta|887
2414704|Várzea|885
2403400|Equador|841
2401800|Brejinho|823
2404853|Itajá|815
2413359|Serra do Mel|807
2406106|Jucurutu|798
2401008|Apodi|794
2401453|Baraúna|781
2413706|Sítio Novo|766
2401107|Areia Branca|731
2412708|São Pedro|712
2413557|Serrinha dos Pintos|707
2403004|Cruzeta|702
2403202|Doutor Severiano|696
2405603|Jardim de Piranhas|689
2403806|Florânia|679
2405702|Jardim do Seridó|667
2411700|São Bento do Trairí|664
2409332|Santa Maria|640
2405504|Jardim de Angicos|634
2411106|Ruy Barbosa|624
2400109|Acari|613
2413201|Senador Georgino Avelino|586
2413300|Serra de São Bento|573
2413003|São Vicente|557
2400505|Alexandria|550
2402402|Carnaúba dos Dantas|541
2404101|Galinhos|519
2409308|Patu|514
2408904|Parelhas|509
2414506|Umarizal|508
2415008|Vila Flor|481
2414456|Triunfo Potiguar|479
2414605|Upanema|460
2413409|Serra Negra do Norte|447
2403707|Felipe Guerra|445
2414159|Tenente Laurentino Cruz|437
2406403|Lagoa de Velhos|427
2401305|Campo Grande|395
2408409|Olho d'Água do Borges|381
2409506|Pedra Grande|380
2414100|Tenente Ananias|368
2407906|Monte das Gameleiras|367
2411007|Rodolfo Fernandes|363
2407401|Martins|359
2411601|São Bento do Norte|347
2408508|Ouro Branco|339
2412104|São João do Sabugi|337
2405207|Janduís|336
2410702|Riacho da Cruz|312
2410603|Rafael Godeiro|291
2404408|Grossos|275
2403756|Fernando Pedroza|262
2402907|Coronel João Pessoa|235
2405108|Jandaíra|228
2411809|São Fernando|222
2404002|Frutuoso Gomes|196
2410256|Porto do Mangue|194
2412401|São José do Seridó|191
2410009|Pilões|187
2406007|José da Penha|185
2400604|Almino Afonso|184
2407005|Luís Gomes|179
2408706|Paraú|173
2407252|Major Sales|172
2400901|Antônio Martins|162
2404309|Governador Dix-Sept Rosado|159
2414753|Venha-Ver|155
2411908|São Francisco do Oeste|144
2411429|Santana do Seridó|142
2404804|Ipueira|142
2414308|Timbaúba dos Batistas|139
2413607|Severiano Melo|136
2403301|Encanto|129
2401651|Bodó|125
2408607|Paraná|117
2406908|Lucrécia|105
2404903|Itaú|104
2410207|Portalegre|100
2403905|Francisco Dantas|99
2414902|Viçosa|96
2407302|Marcelino Vieira|95
2407609|Messias Targino|93
2411056|Tibau|87
2413805|Taboleiro Grande|73
2410801|Riacho de Santana|71
2410504|Rafael Fernandes|68
2400406|Água Nova|68
2405900|João Dias|67"""

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
for line in MUN.strip().split("\n"):
    ibge, nome, total = line.split("|")
    municipios.append({"ibge": ibge, "nome": nome, "total": int(total)})

agora = "2026-08-28T21:40:00-03:00"

amb = {
    "atualizado_em": agora,
    "fonte": "Regula RN / SESAP-RN — api.ambulatorial.lais.ufrn.br",
    "periodo_serie": {"de": "01/01/2025", "ate": "28/08/2026"},
    "periodo_municipios": {"de": "01/01/2026", "ate": "28/08/2026"},
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

for nome, obj in (("ambulatorial.json", amb), ("fila_cirurgias.json", fila)):
    with open(os.path.join(BASE, nome), "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=1)
    print("escrito", nome)
