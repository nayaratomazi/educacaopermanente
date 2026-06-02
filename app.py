import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from collections import Counter
import re

# Configuração da página
st.set_page_config(page_title="Educação Permanente - ESF", layout="wide", initial_sidebar_state="expanded")

# ==========================================
# 1. LISTA MESTRA DE COLABORADORES (379 NOMES)
# ==========================================
LISTA_MESTRA_NOMES = [
    ["ADRIANA CRISTINA DOS SANTOS", "USF JARDIM GODOY/APOIO"],
    ["ADRIANA SANTOS DE ARAUJO", "USF SANTA EDWIRGES/503"],
    ["AIELLY CRISTINA DOS SANTOS COU", "EMULTI 02"],
    ["AKIMI ADACHI", "USF SANTA EDWIRGES/502"],
    ["ALESSANDRA TEIXEIRA AFFONSO", "USF VARGEM LIMPA"],
    ["ALEXSANDRA AFFONSO", "USF SANTA EDWIRGES/501"],
    ["ALINE ERIKA FERREIRA DE LIMA", "EQUIPE SUBSTITUTA"],
    ["AMANDA GABRIELA DOS SANTOS CONSTANTINO", "EMULTI 03"],
    ["AMANDA RODRIGUES ALVES NUNES", "EQUIPE SUBSTITUTA"],
    ["AMANDRA GONCALVES CRIPPA", "USF VILA SÃO PAULO/702"],
    ["ANA CAROLINA FERRAZ PANUCCI", "USF NOVA BAURU / USF NOVE DE JULHO"],
    ["ANA CECILIA DE CAMPOS GALICIA", "EMULTI 01"],
    ["ANA CRISTINA DE CAMPOS", "EQUIPE SUBSTITUTA"],
    ["ANA GABRIELA LEITE CAMPOS", "USF SANTA EDWIRGES/101"],
    ["ANA JULIA CAMARGO DOS SANTOS", "EQUIPE SUBSTITUTA"],
    ["ANA LUCIA CUSTODIO LEME", "USF JARDIM GODOY/APOIO"],
    ["ANA LUCIA RAIMUNDO", "USF VARGEM LIMPA/APOIO"],
    ["ANA NERY MUNUERA NOGUEIRA", "USF JARDIM GODOY/201"],
    ["ANA PATRICIA VIEIRA", "USF VARGEM LIMPA/APOIO"],
    ["ANA PAULA ALVES DOS SANTOS", "USF SANTA EDWIRGES/503"],
    ["ANA PAULA BAPTISTA SALERNO", "USF NOVA BAURU/COORD"],
    ["ANA PAULA SANTANA DOS REIS", "USF VARGEM LIMPA/APOIO"],
    ["ANA PAULA VIOTTO", "EMULTI 03"],
    ["ANA RAFAELA MORENO DUTRA", "USF TIBIRIÇÁ/APOIO"],
    ["ANDERSON MICHEL DOS REIS", "EMULTI 01"],
    ["ANDRE VINICIUS RIBEIRO", "USF VILA SÃO PAULO/APOIO"],
    ["ANDRESSA SOARES JOBSTRAIBIZER", "USF NOVE DE JULHO/601"],
    ["ANDREZA RODRIGUES SUPRIANO", "USF VILA DUTRA/72"],
    ["ANGELITA GOMES BORGES GONÇALVES", "USF SANTA EDWIRGES/APOIO"],
    ["ANTONIA KAUANE AMARANTE MORAIS", "USF VARGEM LIMPA"],
    ["APARECIDA KINUIO HIRATA HUKUCHIMA", "USF SANTA EDWIRGES/502"],
    ["ARIANE VARGAS DA SILVA", "USF POUSADA II/APOIO"],
    ["BARBARA ARRABAL BARROS FERREIRA", "USF SANTA EDWIRGES/101"],
    ["BARBARA BIANCHI DIAS", "EMULTI 01"],
    ["BARBARA DE FATIMA RODRIGUES", "EMULTI 01"],
    ["BEATRIZ FERREIRA BORGES", "USF POUSADA II / USF NOVE DE JULHO"],
    ["BEATRIZ NAVARRO SANCHES", "USF VARGEM LIMPA"],
    ["BIANCA DOS SANTOS CAETANO", "USF NOVE DE JULHO/APOIO"],
    ["BRENA PAMELA EGLESIAS FRANCO", "USF VILA SÃO PAULO/APOIO"],
    ["BRUNA CRISTINA GOMES CAMPOS BENTO", "USF VARGEM LIMPA/APOIO"],
    ["BRUNA FERNANDA DOS SANTOS", "USF SANTA EDWIRGES/502"],
    ["BRUNA LACERDA DA SILVA", "USF JARDIM GODOY/21"],
    ["BRUNA SILVERIO FORTUNATO", "USF TIBIRIÇÁ/APOIO"],
    ["BRUNA VICENTINI SIQUEIRA CRUZ", "EMULTI 02"],
    ["BRUNO DE SOUZA MAZZUIA", "USF VILA DUTRA/71"],
    ["CAIO FARIA DE MORAES", "USF JARDIM GODOY/201"],
    ["CARLA CRISTINA GONCALO", "USF TIBIRIÇÁ/APOIO"],
    ["CARMEN LUCIA ZUQUIERI", "USF POUSADA II/APOIO"],
    ["CATARINA AGUIAR FERREIRA LIMA", "EMULTI 02"],
    ["CELIA APARECIDA CAMARGO LOPES", "USF NOVA BAURU/APOIO"],
    ["CELIA MARIA FRANCISCO DA SILVA", "USF TIBIRIÇA/APOIO"],
    ["CLAUDIA DE QUEIROZ MARTINS RABAQUINI", "USF VILA DUTRA/71"],
    ["CLAUDIA FERNANDES NOGUEIRA", "USF JARDIM GODOY/200"],
    ["CLEBER ROGERIO ESTRUQUE", "USF VILA SÃO PAULO/702"],
    ["CRISTIANE DE CASSIA SOARES BRAZ", "USF VARGEM LIMPA"],
    ["CRISTIANE PEREIRA REINALDO", "USF SANTA EDWIRGES/501"],
    ["CRISTILAYNE MATIAS DE LIMA", "USF JARDIM GODOY/APOIO"],
    ["DANIEL AUGUSTO ADAMI", "USF VILA SÃO PAULO/APOIO"],
    ["DANIEL SOJO DO NASCIMENTO", "EQUIPE SUBSTITUTA"],
    ["DANIELI DA SILVA RAMOS", "USF VILA DUTRA/76"],
    ["DANIELLE GOMES DUARTE", "USF SANTA EDWIRGES/503"],
    ["DAPHYNE YACHEL CHAVES", "EQUIPE SUBSTITUTA"],
    ["DAVID LEE BARBOSA MANTOVANI", "EQUIPE SUBSTITUTA"],
    ["DEBORA ALESSANDRA PERGER RODRIGUES", "USF NOVE DE JULHO/301"],
    ["DEBORA APARECIDA PACCOLA REZENDE", "EMULTI 01"],
    ["DEBORA LONGO MIYASHITA", "USF VILA SÃO PAULO/701"],
    ["DEBORAH EVELYN CANDIDO ZANOTT", "USF VL SÃO PAULO/COORD"],
    ["DEBORAH TORREZAN MARQUES", "EQUIPE SUBSTITUTA"],
    ["DENIA CELESTINA ARAUJO SOUZA", "USF JARDIM GODOY/APOIO"],
    ["DEVLYN PICOLOTO SHIL", "USF JARDIM GODOY/APOIO"],
    ["DJULIEL GLEYCSON DA SILVA", "USF VILA SÃO PAULO/APOIO"],
    ["DOUGLAS ARAUJO PEDROLONGO", "USF VILA SÃO PAULO/702"],
    ["DRIELLE LUCIA BASTOS DA SILVA", "EQUIPE SUBSTITUTA"],
    ["EDSON ALVES DE PORTUGAL", "USF TIBIRIÇÁ/25"],
    ["EDSON MURILO DE OLIVEIRA", "USF VILA DUTRA/76"],
    ["ELAINE APARECIDA DE SOUZA", "USF SANTA EDWIRGES/APOIO"],
    ["ELAINE CRISTINA FIRMINO", "USF NOVE DE JULHO/APOIO"],
    ["ELAINE DO CARMO ROCHA", "USF VARGEM LIMPA/COORD"],
    ["ELEN CRIS FRANCO DUARTE", "USF VILA SÃO PAULO/701"],
    ["ELIANE MARQUES FERREIRA", "USF VILA SÃO PAULO/401"],
    ["ELIDA ESTEFANIA ALVES TOMAZ", "USF VILA DUTRA/APOIO"],
    ["ELISANGELA APARECIDA LOPES", "USF VILA DUTRA/72"],
    ["ELIZABETH CRISTINA BATISTA", "USF POUSADA II/801"],
    ["ELLEN APARECIDA COSTA", "USF SANTA EDWIRGES/501"],
    ["EMANUELLI GIGLIOLI OLIVATTO", "USF NOVA BAURU/901"],
    ["EMYLLY YARA TEODORO DOS SANTOS", "EQUIPE SUBSTITUTA"],
    ["ENARA DE CASTRO DINIZ", "EMULTI 2"],
    ["ERICA CRISTINA MACHADO DA", "EMULTI 01"],
    ["ERICA RODRIGUES CAETANO PEROTA", "USF SANTA EDWIRGES/APOIO"],
    ["FABIANO AZEVEDO SERAFIM", "USF VILA DUTRA/71"],
    ["FABIOLA GOMES DOS SANTOS", "USF VILA SÃO PAULO/APOIO"],
    ["FERNANDA MARQUES YUI", "USF NOVE DE JULHO/601"],
    ["FERNANDA PARINI NUNES", "USF NOVE DE JULHO/301"],
    ["FRANCINE APARECIDA K FRANCEZ", "USF SANTA EDWIRGES/502"],
    ["FRANCINE AROTEIA CAPONE", "USF VILA SÃO PAULO/401"],
    ["FRANCINE RODRIGUES DO NASCIMENTO", "USF VILA DUTRA/76"],
    ["GABRIEL BARBOSA SACCARDO", "USF NOVE DE JULHO/601"],
    ["GABRIEL FERNANDO ROSA ALDIGUERES", "USF NOVE DE JULHO/301"],
    ["GABRIEL HELENO LUIS", "USF VILA SÃO PAULO/701"],
    ["GABRIELA BENJAMIN TOGASHI", "ESF - SUPERVISÃO"],
    ["GABRIELA BERNARDINO MARTINS", "USF POUSADA II/APOIO"],
    ["GABRIELA CRISTINA SCHWETER ALBANEZ", "USF VILA DUTRA/APOIO"],
    ["GABRIELA GARCIA", "USF VILA DUTRA/76"],
    ["GABRIELA KRONKA BARBOZA", "USF NOVA BAURU/901"],
    ["GABRIELA ZERLIN CRISTOVAO", "EQUIPE SUBSTITUTA"],
    ["GABRIELLY TEOFILO RAMOS MENEGHELLO", "USF VILA SÃO PAULO/702"],
    ["GEOVANA FERREIRA BRANDAO", "EQUIPE SUBSTITUTA"],
    ["GIOVANA ALQUATI DE ALMEIDA", "EQUIPE SUBSTITUTA"],
    ["GIOVANA SASSO JONAS", "USF NOVE DE JULHO/301"],
    ["GIOVANNA GALASSO PANNUNZIO", "EMULTI 03"],
    ["GISELE ASSIS RIBEIRO TAVARES", "USF JARDIM GODOY/APOIO"],
    ["GISELE HERNANDES GONCALVES", "USF TIBIRIÇÁ/25"],
    ["GISLAINE CRISTINA GUIMARÃES JA", "USF TIBIRIÇÁ/25"],
    ["GIULIA AGUIAR CAMARGO", "USF NOVE DE JULHO/301"],
    ["GIZELE ARAUJO VALADAO GOMES", "EMULTI 01"],
    ["GUSTAVO NARDI NOGUEIRA", "USF VILA DUTRA/COORD"],
    ["IEDA PAPILLE DOS SANTOS", "EMULTI 01"],
    ["ISABEL CRISTINA FRANÇA DE OLIVEIRA DA SILVA", "USF VARGEM LIMPA/APOIO"],
    ["ISABELA INACIO DE CASTRO", "USF JARDIM GODOY/200"],
    ["ISABELA MORENO AYRES", "EQUIPE SUBSTITUTA"],
    ["ISABELA POSSIGNOLLO DA SILVA", "EMULTI 03"],
    ["ISRAEL MESSIAS GUARDIA", "USF TIBIRIÇÁ/25"],
    ["IVANA FERREIRA DO NASCIMENTO", "USF VILA SAO PAULO/401"],
    ["IVY CAROLINA CORREA SANTIAGO S", "USF VILA DUTRA/76"],
    ["IZABELA FERREIRA DE CASTRO BATISTA", "USF SANTA EDWIRGES"],
    ["JANETE VICTOR MANGA", "EQUIPE SUBSTITUTA"],
    ["JEAN CARLO PEREIRA DOS SANTOS", "USF SANTA EDWIRGES/101"],
    ["JESSICA ARIELE GUIMARAES CORTE", "USF VILA DUTRA/APOIO"],
    ["JESSICA ELLEN LINDOLPHO CREMON", "EQUIPE SUBSTITUTA"],
    ["JESSICA FARIA BARBOSA", "ESF - SUPERVISÃO"],
    ["JESSICA WATANABE CONCEICAO", "USF JARDIM GODOY/200"],
    ["JHENIFER VITÓRIA DA SILVA MARTINS", "USF VILA SÃO PAULO/APOIO"],
    ["JOÃO PEDRO PONCE LOPES", "EQUIPE SUBSTITUTA"],
    ["JOICE CASTELLI PATROCINIO", "EQUIPE SUBSTITUTA"],
    ["JOSE CARLOS SALVADOR", "USF POUSADA II / USF NOVA BAURU"],
    ["JOSELAINE REGIANI RAMOS", "USF NOVA BAURU/901"],
    ["JOSIANE CRISTINA GOMES SEBASTIÃO", "USF SANTA EDWIRGES/APOIO"],
    ["JOSIANE REGO", "USF JARDIM GODOY/COORD"],
    ["JUCILENE MARIA COSTA", "USF JARDIM GODOY/APOIO"],
    ["JULIA FICHIO MIYAHARA", "USF POUSADA II/801"],
    ["JULIA SANCHES DE SOUZA", "USF VILA DUTRA/72"],
    ["JULIA SILVA PEREIRA", "USF JARDIM GODOY/200"],
    ["JULIA TELLES PASCON", "USF POUSADA II/801"],
    ["JULIANA APARECIDA SCANTIMBURGO MANSO", "USF TIBIRIÇA/25"],
    ["JULIANA DA SILVA BUENO", "USF NOVA BAURU/APOIO"],
    ["JULIANE PANDOLFI BUENO DE SOUZA ANTONIO", "USF VILA SÃO PAULO/401"],
    ["JULIO CESAR TAVARES", "EQUIPE SUBSTITUTA"],
    ["KAIELLY GAIDO CORREIA", "EQUIPE SUBSTITUTA"],
    ["KARLA RAISSA BELINI BALDONI", "EQUIPE SUBSTITUTA"],
    ["KAROLYN SALES FIORAVANTI", "USF SANTA EDWIRGES/SUB"],
    ["KARYN CARREGA RODRIGUES", "ESF - SUPERVISÃO"],
    ["KATHLEEN RUFINO DA SILVA", "EMULTI 02"],
    ["KEDMA CASTILHO DE LIMA LUNA", "EMULTI 03"],
    ["KETURI GABRIELA ALVES DA SILVA", "EQUIPE SUBSTITUTA"],
    ["LARA GARCIA DE OLIVEIRA", "USF JARDIM GODOY/200"],
    ["LARISSA PEREIRA GONCALVES", "EMULTI 02"],
    ["LARISSA SOUTO DOS SANTOS", "EQUIPE SUBSTITUTA"],
    ["LEILANE SIQUEIRA DE GOIS MATHEUS", "USF TIBIRIÇÁ/APOIO"],
    ["LEONARDO AMARAL DE PAULA DA SILVA", "USF TIBIRIÇA/25"],
    ["LEONARDO PEREIRA GOMES", "USF JARDIM GODOY/21"],
    ["LETICIA BONAFIM PELLOSO FURTADO", "USF JARDIM GODOY/201"],
    ["LETICIA DA SILVA REDECOPA", "USF VARGEM LIMPA/APOIO FIXO"],
    ["LETICIA FERNANDA GUASTALA", "USF VILA SÃO PAULO/702"],
    ["LETICIA RUZZON CONEGLIAN", "USF VILA SÃO PAULO/APOIO"],
    ["LIDIANE HELOISA JODAR", "USF VILA DUTRA/72"],
    ["LIGIA MARIA FERREIRA DO CARMO", "USF VILA SÃO PAULO / USF NOVA BAURU"],
    ["LISANDRA DA SILVA RODRIGUES", "USF VILA DUTRA/APOIO"],
    ["LIVIA MOZARDO CASTIGLIO", "USF NOVA BAURU/901"],
    ["LOANA KARINA BENEDITO PEREIRA", "USF JARDIM GODOY/APOIO"],
    ["LORRAYNE FARIAS DOS SANTOS", "USF VILA SÃO PAULO/701"],
    ["LUCAS MATHEUS RIBEIRO", "ESF - SANTA EDWIRGES/APOIO"],
    ["LUCIANA ALVES DOS SANTOS", "USF POUSADA II/801"],
    ["LUCIANA APARECIDA DA SILVA", "EQUIPE SUBSTITUTA"],
    ["LUCIANA APARECIDA VICENTINI CA", "USF JARDIM GODOY/21"],
    ["LUCIMAR DOS SANTOS CAETANO", "USF SANTA EDWIRGES/APOIO"],
    ["LUCIMARA CARVALHO DE BRITO", "USF JARDIM GODOY/21"],
    ["LUIS FELIPE LIZI JORGE", "USF SANTA EDWIRGES/503"],
    ["MAILON LESSA", "USF JARDIM GODOY/APOIO"],
    ["MARCELLA CARDOSO GONÇALVES", "USF SANTA EDWIRGES/101"],
    ["MARCELLA MONTOVANELLI MENECHELLI", "USF SANTA EDWIRGES/502"],
    ["MARCELLY CRISTHINE DA SILVA", "USF VILA SÃO PAULO/702"],
    ["MARCELO ANDRADE FERREIRA", "USF JARDIM GODOY/201"],
    ["MARCELO JORGE GOMES", "USF NOVA BAURU/901"],
    ["MARIA APARECIDA MARTINS ROSA", "USF VILA SÃO PAULO/APOIO"],
    ["MARIA CAROLINA URSULINO BURATTO FRANCO", "USF VILA SÃO PAULO/701"],
    ["MARIA FERNANDA FRANCISCA PAULA", "USF NOVE DE JULHO/APOIO"],
    ["MARIA FERNANDA LOSSILA", "EQUIPE SUBSTITUTA"],
    ["MARIA ISABEL DA COSTA", "USF VILA SÃO PAULO/401"],
    ["MARIA LYANDRA CARVALHO", "USF NOVE DE JULHO/601"],
    ["MARIANA BERTUCCO BAZAN", "USF POUSADA II/801"],
    ["MARIANA MAGRO REINATO", "USF VILA DUTRA/76"],
    ["MARIANA PERES FATORI", "USF VILA SÃO PAULO/401"],
    ["MARIANE ALVES JATOBA", "USF SANTA EDWIRGES/101"],
    ["MARIUZA GONCALVES VIEIRA", "USF SANTA EDWIRGES/501"],
    ["MARLI GONÇALVES CARNIATO", "USF SANTA EDWIRGES"],
    ["MATHEUS CAMARGO MARCIANO", "USF VILA DUTRA/71"],
    ["MATHEUS SILVA ANTONIO", "USF VILA DUTRA/72"],
    ["MAYARA GODOY PANUNTO", "USF VILA DUTRA/71"],
    ["MAYARA MONTOVANI DE OLIVEIRA", "USF JARDIM GODOY/200"],
    ["MAYRA DINIZ WASHINGTON", "EMULTI 03"],
    ["MILENA NORONHA MUNHOZ", "USF SANTA EDWIRGES/503"],
    ["MIRIAM CHRISTINELLI", "USF VILA SÃO PAULO/APOIO"],
    ["MIRYELLI CAROLINE MACIEL", "EQUIPE SUBSTITUTA"],
    ["NATALIA ALVES TOSTA OCANHA", "USF POUSADA II/APOIO FIXO"],
    ["NATALIA CAVALHERI DE SOUZA GUERRERO", "USF VARGEM LIMPA / USF POUSADA II"],
    ["NATALIA CRISTINA DOS SANTOS FLORIANO", "USF TIBIRIÇÁ/APOIO FIXO"],
    ["NATALIA FIDENCIO NASCIMENTO", "USF JARDIM GODOY/21"],
    ["NATHALY MARTINUCCI", "USF VARGEM LIMPA"],
    ["NAYANE MARIA DE MELO ALEXANDRINO", "USF SANTA EDWIRGES/501"],
    ["NAYARA COLEONE MUSTACIO ZANELI", "USF SANTA EDWIRGES/COORD"],
    ["NAYARA SOBRINHO LEITE", "USF VARGEM LIMPA / USF TIBIRIÇÁ"],
    ["NAYARA TOMAZI BATISTA", "EQUIPE EDUCAÇÃO PERMANENTE"],
    ["NELI DE FATIMA DANIEL SANTOS", "USF NOVA BAURU/APOIO FIXO"],
    ["NEYLA IVETTE YUTRONIC SERRANO", "EQUIPE EDUCAÇÃO PERMANENTE"],
    ["NIELY RAÍSSA LIMA GUIMARÃES", "USF VILA DUTRA/APOIO"],
    ["PATRICIA APARECIDA OLIVEIRA", "USF VILA DUTRA/APOIO"],
    ["POLLIANY DO MONTE LANCA", "EMULTI 03"],
    ["PRISCILA CALIGARIS CAGI", "USF VARGEM LIMPA"],
    ["PRISCILA DOS SANTOS TRINDADE", "USF VILA DUTRA/APOIO"],
    ["RAFAELA FERNANDA RODRIGUES FAUSTINO", "USF TIBIRIÇÁ/COORD"],
    ["RAFAELA LOPES ALVES", "USF SANTA EDWIRGES/APOIO"],
    ["RAI SAIKA PINTON", "USF SANTA EDWIRGES/APOIO"],
    ["RAQUEL PEREIRA DA CONCEICAO", "USF VILA DUTRA/APOIO"],
    ["RAQUEL PEREIRA DA SILVA", "USF TIBIRIÇÁ"],
    ["RAYANE ISABELLE TURKOCIO FERRAREZI", "USF POUSADA II/APOIO"],
    ["REGINA APARECIDA DE FREITAS DOS SANTOS", "EQUIPE SUBSTITUTA"],
    ["REGINALDO CAETANO", "USF TIBIRIÇÁ/25"],
    ["RENATA DE PAULA SOARES", "USF VILA DUTRA/APOIO"],
    ["RENATA DI PAULA COSTA", "USF SANTA EDWIRGES/101"],
    ["RICARDO QUIRINO FONSECA", "USF VILA SÃO PAULO/701"],
    ["RICHELE BOICO DE SOUZA BARBOSA", "USF NOVA BAURU/APOIO"],
    ["ROSIMEIRE APARECIDA GARCIA DA SILVA OLIVEIRA", "USF NOVE DE JULHO/601"],
    ["SABRINA ALBANEZ OLIVIER", "USF TIBIRIÇÁ/APOIO"],
    ["SANDRA CRISTINA DIAS CAMARGO MARTINS", "USF VILA DUTRA/72"],
    ["SARA LEONCIO DE MELO GARCIA", "USF JARDIM GODOY/201"],
    ["SELMA MARIA DA SILVA", "USF SANTA EDWIRGES/502"],
    ["SHIRLEI APARECIDA PRONUNCIATE GUIMARÃES", "EQUIPE SUBSTITUTA"],
    ["SILVANA APARECIDA STEKER PACHECO", "USF POUSADA II/801"],
    ["SILVIA APARECIDA DE SOUZA SANTANA DO NASCIMENTO", "USF VILA DUTRA/APOIO"],
    ["SILVIA HELENA FERNANDES", "USF POUSADA II/COORD"],
    ["SIMONE MONTEIRO DA SILVA LOPES", "USF SANTA EDWIRGES/APOIO"],
    ["SIMONE REGINA FARINHA", "USF VARGEM LIMPA/APOIO"],
    ["SOLANGE CASTILHO", "USF NOVE DE JULHO/301"],
    ["SOLANGE ESGOTI", "EQUIPE SUBSTITUTA"],
    ["SUELLEN SIMONE GONZALES BERRO", "EMULTI 02"],
    ["SUSAN NAWALY GONCALVES SANDOLI", "EMULTI 02"],
    ["TAIENE DA SILVA MORETTO", "USF JARDIM GODOY/201"],
    ["TAIS DIAS CESARIO", "USF JARDIM GODOY/21"],
    ["TALITA CRISTINA DA SILVA RIBEIRO", "USF VILA DUTRA/71"],
    ["TANIA REINALDO MARINS", "USF VILA DUTRA/APOIO"],
    ["TATIANE BAZOTTI COSTA", "EQUIPE EDUCAÇÃO PERMANENTE"],
    ["THAINA OLIVEIRA FELICIO OLIVATTI", "EMULTI 02"],
    ["THAIS CRISTINA ALVES PINTO", "USF NOVA BAURU/901"],
    ["THAIS NAYRA MACHADO", "USF NOVE DE JULHO/601"],
    ["THAIS OTAVIANA PEREIRA PARDINO", "USF VARGEM LIMPA/APOIO"],
    ["THAISE MARTINS SANTOS SANTANA", "EMULTI 03"],
    ["THALES CABRAL BENINI FELISBERTO", "USF SANTA EDWIRGES/101"],
    ["THALIA MOREIRA MANZUTI GARCIA", "USF VILA DUTRA/APOIO"],
    ["THATIANE FRANCINI DA SILVA FERREIRA", "USF SANTA EDWIRGES/501"],
    ["TIENE ARCANJO DE OLIVEIRA", "EQUIPE SUBSTITUTA"],
    ["VALDINEIA NERIS DE SOUSA", "USF NOVE DE JULHO/COORD"],
    ["VALERIA DE MIRANDA", "USF JARDIM GODOY/APOIO"],
    ["VANUZA BARBOSA LEITE", "EQUIPE SUBSTITUTA"],
    ["VERA LUCIA ALVES DA SILVA", "USF POUSADA II/APOIO"],
    ["VICTOR FERREIRA RAMOS COLASSO", "USF SANTA EDWIRGES/501"],
    ["VITÓRIA GABRIELLE RODRIGUES DOS SANTOS", "EQUIPE SUBSTITUTA"],
    ["VIVIAN MARTINS GOMES", "USF TIBIRIÇÁ"],
    ["VIVIANI MAXIMINO BAPTISTA BUENO", "USF POUSADA II/801"],
    ["VYVIAN KELLEY ALVES CASTILHO", "USF SANTA EDWIRGES/APOIO"],
    ["WANESSA VIEIRA CASTELO RODRIGUES", "USF NOVE DE JULHO/APOIO"],
    ["WENDLER VINICIUS DA PAIXAO", "USF SANTA EDWIRGES/APOIO"],
    ["WESLEY DOS SANTOS CASTILHO RODRIGUES", "ACS - UNIDADE NÃO DEFINIDA"],
    ["WILLIAM AUGUSTO GRANDO", "USF SANTA EDWIRGES/503"],
    ["YASMIM VITORIA DA SILVA SOUZA", "EQUIPE SUBSTITUTA"],
    ["ZENAIDE BARBOSA HONORATO", "USF POUSADA II/801"],
    ["ALESSANDRA REGINA DA SILVA", "ACS - UNIDADE NÃO DEFINIDA"],
    ["ALINE APARECIDA DE SOUZA", "ACS - UNIDADE NÃO DEFINIDA"],
    ["ANA BEATRIZ CORPASSI", "ACS - UNIDADE NÃO DEFINIDA"],
    ["ANA CAROLINA CONDI DA MATA", "ACS - UNIDADE NÃO DEFINIDA"],
    ["ANA CAROLINA DA SILVA", "ACS - UNIDADE NÃO DEFINIDA"],
    ["ANA CAROLINA LOPES MATSUMOTO", "ACS - UNIDADE NÃO DEFINIDA"],
    ["ANA LAURA ALMERIN TRABUCO", "ACS - UNIDADE NÃO DEFINIDA"],
    ["ANA PAULA DE MATOS MILESKI", "ACS - UNIDADE NÃO DEFINIDA"],
    ["ANDRESSA APARECIDA PEREIRA GOES PESUTO", "ACS - UNIDADE NÃO DEFINIDA"],
    ["ANNA LUIZA AMARANTE DA SILVA", "ACS - UNIDADE NÃO DEFINIDA"],
    ["ARIANE KEVLIN RODRIGUES", "ACS - UNIDADE NÃO DEFINIDA"],
    ["BARBARA LETICIA CHINALLI FERNANDES SANTOS", "ACS - UNIDADE NÃO DEFINIDA"],
    ["BARBARA RAMOS MARQUES", "ACS - UNIDADE NÃO DEFINIDA"],
    ["BEATRIZ BARRETO DE OLIVEIRA", "ACS - UNIDADE NÃO DEFINIDA"],
    ["BEATRIZ PEREIRA CAMPOS", "ACS - UNIDADE NÃO DEFINIDA"],
    ["BEATRIZ SILVEIRA SILVERIO", "ACS - UNIDADE NÃO DEFINIDA"],
    ["CARLA MARIA PEREIRA DA SILVA", "ACS - UNIDADE NÃO DEFINIDA"],
    ["CAROLINA CRISTINA BERGAMASCHI DA SILVA", "ACS - UNIDADE NÃO DEFINIDA"],
    ["CELESTE LUZIA CHRISOSTOMO DOS SANTOS", "ACS - UNIDADE NÃO DEFINIDA"],
    ["CHARLES VINICIUS ALVES VASQUE", "ACS - UNIDADE NÃO DEFINIDA"],
    ["DAIZE MANOEL DOS SONTOS", "ACS - UNIDADE NÃO DEFINIDA"],
    ["DAMARIS VASCONI DA SILVA", "ACS - UNIDADE NÃO DEFINIDA"],
    ["DANIEL APARECIDO MARASSATTI", "ACS - UNIDADE NÃO DEFINIDA"],
    ["DAVYD AUGUSTO CASTELLI DE SOUZA", "ACS - UNIDADE NÃO DEFINIDA"],
    ["DAYANE FERNANDA LIMA DA SILVA", "ACS - UNIDADE NÃO DEFINIDA"],
    ["DAYANE RAFAELA FARIAS FERREIRA TOMAZ", "ACS - UNIDADE NÃO DEFINIDA"],
    ["DJEINE GONÇALVES DOS SANTOS", "ACS - UNIDADE NÃO DEFINIDA"],
    ["ELIANA PATRICIA PINTO FERNANDES", "ACS - UNIDADE NÃO DEFINIDA"],
    ["ELIZABETH DA SILVA LEMES", "ACS - UNIDADE NÃO DEFINIDA"],
    ["EVERTON APARECIDO GARCIA LEAL", "ACS - UNIDADE NÃO DEFINIDA"],
    ["FABIANA JORGE DA SILVA", "ACS - UNIDADE NÃO DEFINIDA"],
    ["FABIANA PRADO DA SILVA", "ACS - UNIDADE NÃO DEFINIDA"],
    ["FATIMA APARECIDA DE ASSIS", "ACS - UNIDADE NÃO DEFINIDA"],
    ["FERNANDA CRISTINA TERECIANO", "ACS - UNIDADE NÃO DEFINIDA"],
    ["FERNANDA DE SOUZA FERREIRA", "ACS - UNIDADE NÃO DEFINIDA"],
    ["FERNANDA SAN JULIANO PEREIRA PAULON", "ACS - UNIDADE NÃO DEFINIDA"],
    ["FILIPE SAN JULIANO PEREIRA", "ACS - UNIDADE NÃO DEFINIDA"],
    ["FLAVIO LIBOIO", "ACS - UNIDADE NÃO DEFINIDA"],
    ["FRANCIELEN DA SILVA RIBEIRO", "ACS - UNIDADE NÃO DEFINIDA"],
    ["FRANKLIN ABNER DE LIMA SANTOS", "ACS - UNIDADE NÃO DEFINIDA"],
    ["GILSIANDRA DA SILVA CAETANO", "ACS - UNIDADE NÃO DEFINIDA"],
    ["GIORDANA DE FREITAS COLACINO MENDES", "ACS - UNIDADE NÃO DEFINIDA"],
    ["GIOVANA GONÇALVES COSTA ARAUJO", "ACS - UNIDADE NÃO DEFINIDA"],
    ["GIOVANA GONÇALVES DA SILVA", "ACS - UNIDADE NÃO DEFINIDA"],
    ["GIOVANA RENATA RECUCHE", "ACS - UNIDADE NÃO DEFINIDA"],
    ["GISELE ALVES DE MIRA SOUZA", "ACS - UNIDADE NÃO DEFINIDA"],
    ["GISELE LIPE BAUTZ", "ACS - UNIDADE NÃO DEFINIDA"],
    ["GIULIA NARCIZO GARCIA", "ACS - UNIDADE NÃO DEFINIDA"],
    ["GLAUCIA APARECIDA DE JESUS COLOMBO VIEIRA", "ACS - UNIDADE NÃO DEFINIDA"],
    ["GUILHERME FERNANDO MACIEL PRUDENTE", "ACS - UNIDADE NÃO DEFINIDA"],
    ["ISABELA APARECIDA RODRIGUES DA CRUZ JERONIMO", "ACS - UNIDADE NÃO DEFINIDA"],
    ["ISABELA CHAVES DE OLIVEIRA", "ACS - UNIDADE NÃO DEFINIDA"],
    ["ISABELA CRISTINA FLORENTINO", "ACS - UNIDADE NÃO DEFINIDA"],
    ["ISABELA DE OLIVEIRA ALVES", "ACS - UNIDADE NÃO DEFINIDA"],
    ["IVAN VARAS CARDOSO", "ACS - UNIDADE NÃO DEFINIDA"],
    ["JAMILLE ALESSANDRA LEITE", "ACS - UNIDADE NÃO DEFINIDA"],
    ["JANAINA DE CARVALHO QUEIROGA", "ACS - UNIDADE NÃO DEFINIDA"],
    ["JAQUELINE PEREIRA DE SOUZA", "ACS - UNIDADE NÃO DEFINIDA"],
    ["JESSICA CARVALHO DE SOUZA", "ACS - UNIDADE NÃO DEFINIDA"],
    ["JESSICA CRISTINE LEITE", "ACS - UNIDADE NÃO DEFINIDA"],
    ["JOAO GABRIEL DA SILVA FREITAS", "ACS - UNIDADE NÃO DEFINIDA"],
    ["JOAO VITOR RINALDO DE SOUSA", "ACS - UNIDADE NÃO DEFINIDA"],
    ["JOSIANE SOARES DE SOUZA SANTOS", "ACS - UNIDADE NÃO DEFINIDA"],
    ["JUCINEIA DOS SANTOS", "ACS - UNIDADE NÃO DEFINIDA"],
    ["JULIANA DE FATIMA RIBEIRO", "ACS - UNIDADE NÃO DEFINIDA"],
    ["JULIANA DE OLIVEIRA JUMONJI", "ACS - UNIDADE NÃO DEFINIDA"],
    ["JULIANA MOREIRA LOPES", "ACS - UNIDADE NÃO DEFINIDA"],
    ["JULIANA ORTIZ DA SILVA", "ACS - UNIDADE NÃO DEFINIDA"],
    ["JULIANE MACEGOZA DO AMARAL", "ACS - UNIDADE NÃO DEFINIDA"],
    ["KARINA MONTEIRO BATISTA", "ACS - UNIDADE NÃO DEFINIDA"],
    ["KESLEY GARCIA IVASSAKI", "ACS - UNIDADE NÃO DEFINIDA"],
    ["LEANDRO ACACIO DOS SANTOS", "ACS - UNIDADE NÃO DEFINIDA"],
    ["LEANDRO DAVANÇO FREIRE", "ACS - UNIDADE NÃO DEFINIDA"],
    ["LEONARDO HORNE GOMES", "ACS - UNIDADE NÃO DEFINIDA"],
    ["LEONARDO RICARDO DA SILVA", "ACS - UNIDADE NÃO DEFINIDA"],
    ["LETICIA ALVES FERREIRA", "ACS - UNIDADE NÃO DEFINIDA"],
    ["LUCIANE CRISTINA MAIA DE OLIVEIRA", "ACS - UNIDADE NÃO DEFINIDA"],
    ["LUIDGI AGNNO ZELNYS CARLOS", "ACS - UNIDADE NÃO DEFINIDA"],
    ["MAIARA APARECIDA FRANCO DA SILVEIRA", "ACS - UNIDADE NÃO DEFINIDA"],
    ["MARISA CRISTINA PRUDENTE RIBEIRO", "ACS - UNIDADE NÃO DEFINIDA"],
    ["MAYARA ANDRESSA BRUNA DOS SANTOS", "ACS - UNIDADE NÃO DEFINIDA"],
    ["MELINA RODRIGUES", "ACS - UNIDADE NÃO DEFINIDA"],
    ["MIQUE ERIC GIMENES", "ACS - UNIDADE NÃO DEFINIDA"],
    ["MIRIAN HELEN CARNEIRO DE SOUZA", "ACS - UNIDADE NÃO DEFINIDA"],
    ["NATALIA CRISTINA DOS SANTOS", "ACS - UNIDADE NÃO DEFINIDA"],
    ["NATHALIA APAREC B.SOUZA", "ACS - UNIDADE NÃO DEFINIDA"],
    ["NATHALIA DO CARMO LEME INACIO", "ACS - UNIDADE NÃO DEFINIDA"],
    ["NATHALIA GONÇALVES COSTA CASAGRANDE BERNARDO", "ACS - UNIDADE NÃO DEFINIDA"],
    ["NEYLOR JOSE ANTUNES DOS SANTOS", "ACS - UNIDADE NÃO DEFINIDA"],
    ["PAMELA CRISTINA KURIO", "ACS - UNIDADE NÃO DEFINIDA"],
    ["PAMELA LARISSA FRANCO DA CRUZ ALVES", "ACS - UNIDADE NÃO DEFINIDA"],
    ["PAMELLA THAYARA DOS SANTOS", "ACS - UNIDADE NÃO DEFINIDA"],
    ["PATRICIA ALINE RODRIGUES DE SOUZA", "ACS - UNIDADE NÃO DEFINIDA"],
    ["PATRICIA LIZANDRA MORETTI CRUZ", "ACS - UNIDADE NÃO DEFINIDA"],
    ["PATRICIA MIRELI SILVA", "ACS - UNIDADE NÃO DEFINIDA"],
    ["PAULO HENRIQUE MANGILI SERESUELA", "ACS - UNIDADE NÃO DEFINIDA"],
    ["PAULO RICARDO SOLANA", "ACS - UNIDADE NÃO DEFINIDA"],
    ["RAPHAELA GIOVANA ALVES CALVO", "ACS - UNIDADE NÃO DEFINIDA"],
    ["RICARDO RUIVO BUSCH", "ACS - UNIDADE NÃO DEFINIDA"],
    ["ROBSON LUIZ PEREIRA", "ACS - UNIDADE NÃO DEFINIDA"],
    ["RODRIGO SANTOS SANTANA", "ACS - UNIDADE NÃO DEFINIDA"],
    ["ROSIELI DE CARVALHO", "ACS - UNIDADE NÃO DEFINIDA"],
    ["SAMARA MOREIRA INACIO", "ACS - UNIDADE NÃO DEFINIDA"],
    ["SILVIA REGINA CELESTINO", "ACS - UNIDADE NÃO DEFINIDA"],
    ["SILVIA SAYURI YATSU TAHARA", "ACS - UNIDADE NÃO DEFINIDA"],
    ["SONIA APARECIDA FAGNANI", "USF SANTA EDWIRGES/SUB"],
    ["TAYOANA CAROLINA SILVA", "ACS - UNIDADE NÃO DEFINIDA"],
    ["THAIS CARDOSO DA SILVA SILVIERO", "ACS - UNIDADE NÃO DEFINIDA"],
    ["THIAGO HENRIQUE CHANQUINI FRANCISCO", "ACS - UNIDADE NÃO DEFINIDA"],
    ["TIAGO PEREIRA ALEXANDRE", "ACS - UNIDADE NÃO DEFINIDA"],
    ["TIFANY DA SILVA TORRES", "ACS - UNIDADE NÃO DEFINIDA"],
    ["VANESSA DOMINGOS BARBOSA", "ACS - UNIDADE NÃO DEFINIDA"],
    ["VANESSA FRACALOSSI", "ACS - UNIDADE NÃO DEFINIDA"],
    ["WESLEY DOS SANTOS CASTILHO RODRIGUES", "ACS - UNIDADE NÃO DEFINIDA"],
    ["YURI HOLLANDER", "ACS - UNIDADE NÃO DEFINIDA"]
]

# ==========================================
# 2. SISTEMA DE MONITORAMENTO INTELIGENTE (BI)
# ==========================================

def padronizar_unidade(x):
    """Filtra e consolida as strings pelo nome antes da barra."""
    if not isinstance(x, str):
        return "NÃO INFORMADA"
    val = x.upper().strip()
    if "ACS" in val and "NÃO DEFINIDA" in val:
        return "ACS - UNIDADE NÃO DEFINIDA"
    # Corta a string na barra e pega apenas a primeira parte
    return val.split('/')[0].strip()

# CONFIGURAÇÃO DO LINK (GOOGLE SHEETS)
LINK_GOOGLE_SHEETS = "https://docs.google.com/spreadsheets/d/1yGdTyQWTTYOTEpzJqzu3M5KG1dv9Y7uEc-NbPedPNGU/export?format=xlsx"

@st.cache_data(ttl=60)
def carregar_dados(url):
    df = pd.read_excel(url, engine='openpyxl')
    return df

def extrair_temas_inteligentes(textos):
    """Função simples para identificar palavras-chave mais comuns em temas."""
    stop_words = ['DA', 'DE', 'DO', 'E', 'O', 'A', 'PARA', 'COM', 'EM', 'UM', 'UMA', 'SOBRE']
    palavras = []
    for t in textos:
        if isinstance(t, str):
            # Limpa caracteres especiais e divide por palavras
            pals = re.findall(r'\w+', t.upper())
            palavras.extend([p for p in pals if p not in stop_words and len(p) > 3])
    return Counter(palavras).most_common(10)

# Interface Principal
st.title("Painel de Gestão | Educação Permanente")
st.caption("Acompanhamento de atividades educativas")
st.divider()

# Sidebar
st.sidebar.header("Configurações")
if st.sidebar.button("Atualizar Dados"):
    st.cache_data.clear()
    st.rerun()

try:
    with st.spinner('Sincronizando base de dados...'):
        df = carregar_dados(LINK_GOOGLE_SHEETS)
    
    # Processamento
    df.columns = df.columns.str.strip().str.upper()
    
    # --- PREENCHIMENTO DE NULOS (A Trava Matemática) ---
    # Isso garante que se um profissional não preencheu a Unidade ou a Categoria, 
    # ele não seja ignorado na hora de somar, fazendo os totais baterem perfeitamente.
    # Aplica o padrão "antes da barra" logo no início para uso no painel inteiro
    if 'LOTAÇÃO' in df.columns:
        df['LOTAÇÃO'] = df['LOTAÇÃO'].fillna('NÃO INFORMADA').astype(str)
        df['LOTAÇÃO'] = df['LOTAÇÃO'].apply(padronizar_unidade)
        
    if 'CATEGORIA PROFISSIONAL' in df.columns:
        df['CATEGORIA PROFISSIONAL'] = df['CATEGORIA PROFISSIONAL'].fillna('NÃO INFORMADA')
    # ----------------------------------------------------

    colunas_nome = [c for c in df.columns if 'NOME' in c and 'COMPLETO' in c]
    if colunas_nome:
        df['NOME COMPLETO'] = df[colunas_nome].bfill(axis=1).iloc[:, 0].str.strip().str.upper()
        df['NOME COMPLETO'] = df['NOME COMPLETO'].fillna('NÃO INFORMADO') # Trava para Nome
    
    col_inicio = 'HORÁRIO INICIAL' if 'HORÁRIO INICIAL' in df.columns else 'HORARIO INICIAL'
    col_fim = 'HORÁRIO FINAL' if 'HORÁRIO FINAL' in df.columns else 'HORARIO FINAL'
    col_data = 'DATA DA ATIVIDADE' if 'DATA DA ATIVIDADE' in df.columns else 'CARIMBO DE DATA/HORA'
    col_tema = 'DESCRIÇÃO BREVE DA ATIVIDADE' if 'DESCRIÇÃO BREVE DA ATIVIDADE' in df.columns else df.columns[-1]

    # Trava de tema vazio
    if col_tema in df.columns:
        df[col_tema] = df[col_tema].fillna('NÃO INFORMADO')

    df['CH_CALCULADA'] = (pd.to_datetime(df[col_fim].astype(str), errors='coerce') - 
                         pd.to_datetime(df[col_inicio].astype(str), errors='coerce')).dt.total_seconds() / 3600
    df['CH_CALCULADA'] = df['CH_CALCULADA'].fillna(0).apply(lambda x: max(0, x))
    
    df['DATA_DT'] = pd.to_datetime(df[col_data], errors='coerce')
    df['MÊS'] = df['DATA_DT'].dt.strftime('%m - %b')
    df['ANO'] = df['DATA_DT'].dt.year.astype(str)
    df['PERIODO'] = df['DATA_DT'].dt.strftime('%Y-%m')

    # Filtros
    st.sidebar.subheader("Filtros")
    f_ano = st.sidebar.multiselect("Ano", sorted(df['ANO'].dropna().unique()))
    f_mes = st.sidebar.multiselect("Mês", sorted(df['MÊS'].dropna().unique()))
    f_unidade = st.sidebar.multiselect("Unidade", sorted(df['LOTAÇÃO'].dropna().unique()))
    f_cat = st.sidebar.multiselect("Categoria", sorted(df['CATEGORIA PROFISSIONAL'].dropna().unique()))
    f_nome = st.sidebar.multiselect("Nome do Profissional", sorted(df['NOME COMPLETO'].dropna().unique()))

    df_f = df.copy()
    if f_ano: df_f = df_f[df_f['ANO'].isin(f_ano)]
    if f_mes: df_f = df_f[df_f['MÊS'].isin(f_mes)]
    if f_unidade: df_f = df_f[df_f['LOTAÇÃO'].isin(f_unidade)]
    if f_cat: df_f = df_f[df_f['CATEGORIA PROFISSIONAL'].isin(f_cat)]
    if f_nome: df_f = df_f[df_f['NOME COMPLETO'].isin(f_nome)]

    if df_f.empty:
        st.info("Aguardando seleção de dados nos filtros.")
    else:
        # --- VISÃO PÚBLICA ---
        m1, m2, m3 = st.columns(3)
        m1.metric("Registros (Total)", len(df_f))
        m2.metric("Total Horas", f"{df_f['CH_CALCULADA'].sum():.1f}h")
        m3.metric("Média/Atividade", f"{(df_f['CH_CALCULADA'].mean()):.1f}h")
        
        st.divider()

        # Gráficos Principais
        c_g1, c_g2 = st.columns(2)
        with c_g1:
            st.subheader("Registros por Unidade")
            st.bar_chart(df_f['LOTAÇÃO'].value_counts(), color="#29b5e8")
        with c_g2:
            st.subheader("Carga Horária por Unidade")
            st.bar_chart(df_f.groupby('LOTAÇÃO')['CH_CALCULADA'].sum(), color="#ff4b4b")

        st.divider()

        # --- DESTAQUES E ANÁLISES POR CATEGORIA ---
        c_t1, c_t2 = st.columns([1, 1.5])
        
        with c_t1:
            st.subheader("Destaques por Unidade")
            destaque = df_f.groupby(['LOTAÇÃO', 'CATEGORIA PROFISSIONAL']).size().reset_index(name='Qtd')
            idx = destaque.groupby('LOTAÇÃO')['Qtd'].idxmax()
            st.dataframe(destaque.loc[idx], use_container_width=True, hide_index=True)
            
            # Nova Tabela Adicionada: Atividades e CH por Categoria
            st.subheader("Atividades e CH por Categoria")
            resumo_cat = df_f.groupby('CATEGORIA PROFISSIONAL').agg(
                Atividades=('CATEGORIA PROFISSIONAL', 'count'),
                CH_Total=('CH_CALCULADA', 'sum')
            ).reset_index()
            resumo_cat['CH_Total'] = resumo_cat['CH_Total'].round(1).astype(str) + 'h'
            st.dataframe(resumo_cat, use_container_width=True, hide_index=True)
        
        with c_t2:
            # Nova Tabela Adicionada: Categoria e Tema da Atividade
            st.subheader("Relação: Categoria Profissional e Tema")
            relacao_tema = df_f[['CATEGORIA PROFISSIONAL', col_tema]].drop_duplicates().sort_values(by='CATEGORIA PROFISSIONAL')
            relacao_tema.columns = ['Categoria', 'Tema da Atividade']
            st.dataframe(relacao_tema, use_container_width=True, hide_index=True)
            
            st.subheader("Carga Horária e Resumo de Temas por Categoria")
            resumo = df_f.groupby('CATEGORIA PROFISSIONAL').agg({
                col_tema: lambda x: ' | '.join(x.dropna().astype(str).unique()[:3]) + '...', 
                'CH_CALCULADA': 'sum'
            }).reset_index()
            resumo.columns = ['Categoria', 'Exemplos de Temas', 'Total Horas']
            st.dataframe(resumo, use_container_width=True, hide_index=True)

        st.divider()

        # --- ÁREA DA COORDENAÇÃO ---
        st.header("Coordenação")
        with st.expander("Autenticação Necessária"):
            senha = st.text_input("Senha de acesso", type="password", key="sec")
            if senha == "eps2026_esf":
                
                # 1. Deltas de Tendência
                st.subheader("Tendência Mensal")
                periodos = sorted(df_f['PERIODO'].unique())
                if len(periodos) >= 2:
                    curr, prev = periodos[-1], periodos[-2]
                    h_curr = df_f[df_f['PERIODO'] == curr]['CH_CALCULADA'].sum()
                    h_prev = df_f[df_f['PERIODO'] == prev]['CH_CALCULADA'].sum()
                    delta = ((h_curr - h_prev) / h_prev) * 100 if h_prev > 0 else 0
                    st.metric(f"Horas em {curr}", f"{h_curr:.1f}h", f"{delta:.1f}% vs {prev}")
                
                # 2. Gráfico de Evolução Interativo (Plotly)
                st.subheader("Evolução Temporal do Engajamento")
                df_evol = df_f.groupby(['PERIODO', 'LOTAÇÃO'])['CH_CALCULADA'].sum().reset_index()
                fig_line = px.line(df_evol, x='PERIODO', y='CH_CALCULADA', color='LOTAÇÃO', markers=True, template="plotly_white")
                st.plotly_chart(fig_line, use_container_width=True)

                st.divider()

                # 3. Análise Inteligente de Temas e Radar
                c_bi1, c_bi2 = st.columns(2)
                with c_bi1:
                    st.subheader("Temas mais Abordados (Agrupados)")
                    nuvem = extrair_temas_inteligentes(df_f[col_tema])
                    df_nuvem = pd.DataFrame(nuvem, columns=['Termo', 'Frequência'])
                    fig_tema = px.bar(df_nuvem, x='Frequência', y='Termo', orientation='h', color='Frequência', color_continuous_scale="Blues")
                    st.plotly_chart(fig_tema, use_container_width=True)
                
                with c_bi2:
                    st.subheader("Equilíbrio por Categoria (Radar)")
                    df_radar = df_f.groupby('CATEGORIA PROFISSIONAL')['CH_CALCULADA'].sum().reset_index()
                    fig_radar = go.Figure(data=go.Scatterpolar(r=df_radar['CH_CALCULADA'], theta=df_radar['CATEGORIA PROFISSIONAL'], fill='toself'))
                    st.plotly_chart(fig_radar, use_container_width=True)

                st.divider()

                # 4. Monitoramento de Gestão e Metas (16h)
                st.subheader("Monitoramento de Gestão e Metas (16h)")
                
                # --- BASE PARA METAS E BUSCA ATIVA (Lista Mestra) ---
                df_mestra = pd.DataFrame(LISTA_MESTRA_NOMES, columns=['NOME COMPLETO', 'UNIDADE REGISTRADA'])
                df_mestra['NOME COMPLETO'] = df_mestra['NOME COMPLETO'].str.strip().str.upper()
                df_mestra['UNIDADE REGISTRADA'] = df_mestra['UNIDADE REGISTRADA'].apply(padronizar_unidade)
                
                if f_unidade:
                    df_mestra = df_mestra[df_mestra['UNIDADE REGISTRADA'].isin(f_unidade)]
                
                horas_prof = df_f.groupby('NOME COMPLETO')['CH_CALCULADA'].sum().reset_index()
                gestao = pd.merge(df_mestra, horas_prof, on='NOME COMPLETO', how='left').fillna(0)
                
                c_gest1, c_gest2 = st.columns(2)
                
                with c_gest1:
                    st.markdown("**Desempenho: Meta de 16h por Unidade Unificada**")
                    gestao['ATINGIU META'] = gestao['CH_CALCULADA'] >= 16
                    resumo_meta = gestao.groupby('UNIDADE REGISTRADA').agg(
                        Profissionais=('NOME COMPLETO', 'count'),
                        Atingiram=('ATINGIU META', 'sum')
                    ).reset_index()
                    resumo_meta['% Sucesso'] = resumo_meta.apply(
                        lambda r: f"{(r['Atingiram'] / r['Profissionais'] * 100):.1f}%" if r['Profissionais'] > 0 else "0.0%", axis=1
                    )
                    st.dataframe(resumo_meta.sort_values('Atingiram', ascending=False), hide_index=True)
                    
                    st.markdown("**Ranking Individual Completo**")
                    # RANKING APENAS DE QUEM LANÇOU ATIVIDADE (DIRETO DO DF_F)
                    if not df_f.empty:
                        ranking_ind = df_f.groupby(['NOME COMPLETO', 'LOTAÇÃO']).agg(
                            Carga_Horaria=('CH_CALCULADA', 'sum'),
                            Atividades_Lancadas=('CH_CALCULADA', 'count')
                        ).reset_index()
                        ranking_ind.columns = ['Nome do Profissional', 'Unidade', 'Carga Horária (h)', 'Atividades Lançadas']
                        ranking_ind = ranking_ind.sort_values(by=['Carga Horária (h)', 'Atividades Lançadas'], ascending=[False, False])
                        st.dataframe(ranking_ind, hide_index=True)
                    else:
                        st.info("Nenhum lançamento no período filtrado.")

                with c_gest2:
                    st.markdown("**Busca Ativa: Ausência de Lançamentos (Por Unidade Unificada)**")
                    faltantes = gestao[gestao['CH_CALCULADA'] == 0][['NOME COMPLETO', 'UNIDADE REGISTRADA']]
                    st.dataframe(faltantes.sort_values('UNIDADE REGISTRADA'), hide_index=True)

            elif senha:
                st.error("Senha incorreta.")

except Exception as e:
    st.error(f"Erro no processamento: {e}")
