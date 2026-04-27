import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from collections import Counter
import re

# Configuração da página
st.set_page_config(page_title="Gestão EP - Bauru", layout="wide", initial_sidebar_state="expanded")

# ==========================================
# 1. LISTA MESTRA DE COLABORADORES (379 NOMES)
# ==========================================
LISTA_MESTRA_NOMES = [
    "ADRIANA CRISTINA DOS SANTOS", "ADRIANA SANTOS DE ARAUJO", "ADRIEL LUCAS COSTA CUNHA", 
    "AIELLY CRISTINA DOS SANTOS COU", "AKIMI ADACHI", "ALESSANDRA REGINA DA SILVA", 
    "ALESSANDRA TEIXEIRA AFFONSO", "ALEXSANDRA AFFONSO", "ALINE APARECIDA DE SOUZA", 
    "ALINE ERIKA FERREIRA DE LIMA", "AMANDA GABRIELA DOS SANTOS CONSTANTINO", 
    "AMANDA RODRIGUES ALVES NUNES", "AMANDRA GONCALVES CRIPPA", "ANA BEATRIZ CORPASSI", 
    "ANA CAROLINA CONDI DA MATA", "ANA CAROLINA DA SILVA", "ANA CAROLINA FERRAZ PANUCCI", 
    "ANA CAROLINA LOPES MATSUMOTO", "ANA CECILIA DE CAMPOS GALICIA", "ANA CRISTINA DE CAMPOS", 
    "ANA GABRIELA LEITE CAMPOS", "ANA JULIA CAMARGO DOS SANTOS", "ANA LAURA ALMERIN TRABUCO", 
    "ANA LUCIA CUSTODIO LEME", "ANA LUCIA RAIMUNDO", "ANA NERY MUNUERA NOGUEIRA", 
    "ANA PATRICIA VIEIRA", "ANA PAULA ALVES DOS SANTOS", "ANA PAULA BAPTISTA SALERNO", 
    "ANA PAULA DE MATOS MILESKI", "ANA PAULA SANTANA DOS REIS", "ANA PAULA VIOTTO", 
    "ANA RAFAELA MORENO DUTRA", "ANDERSON MICHEL DOS REIS", "ANDRE VINICIUS RIBEIRO", 
    "ANDRESSA APARECIDA PEREIRA GOES PESUTO", "ANDRESSA SOARES JOBSTRAIBIZER", 
    "ANDREZA RODRIGUES SUPRIANO", "ANGELITA GOMES BORGES GONÇALVES", "ANNA LUIZA AMARANTE DA SILVA", 
    "ANTONIA KAUANE AMARANTE MORAIS", "APARECIDA KINUIO HIRATA HUKUCHIMA", "ARIANE KEVLIN RODRIGUES", 
    "ARIANE VARGAS DA SILVA", "BARBARA ARRABAL BARROS FERREIRA", "BARBARA BIANCHI DIAS", 
    "BARBARA DE FATIMA RODRIGUES", "BARBARA LETICIA CHINALLI FERNANDES SANTOS", "BARBARA RAMOS MARQUES", 
    "BEATRIZ BARRETO DE OLIVEIRA", "BEATRIZ FERREIRA BORGES", "BEATRIZ NAVARRO SANCHES", 
    "BEATRIZ PEREIRA CAMPOS", "BEATRIZ SILVEIRA SILVERIO", "BIANCA DOS SANTOS CAETANO", 
    "BRENA PAMELA EGLESIAS FRANCO", "BRUNA CRISTINA GOMES CAMPOS BENTO", "BRUNA FERNANDA DOS SANTOS", 
    "BRUNA LACERDA DA SILVA", "BRUNA SILVERIO FORTUNATO", "BRUNA VICENTINI SIQUEIRA CRUZ", 
    "BRUNO DE SOUZA MAZZUIA", "CAIO FARIA DE MORAES", "CARLA CRISTINA GONCALO", 
    "CARLA MARIA PEREIRA DA SILVA", "CARMEN LUCIA ZUQUIERI", "CAROLINA CRISTINA BERGAMASCHI DA SILVA", 
    "CATARINA AGUIAR FERREIRA LIMA", "CELESTE LUZIA CHRISOSTOMO DOS SANTOS", "CELIA APARECIDA CAMARGO LOPES", 
    "CELIA MARIA FRANCISCO DA SILVA", "CHARLES VINICIUS ALVES VASQUE", "CLAUDIA DE QUEIROZ MARTINS RABAQUINI", 
    "CLAUDIA FERNANDES NOGUEIRA", "CLEBER ROGERIO ESTRUQUE", "CRISTIANE DE CASSIA SOARES BRAZ", 
    "CRISTIANE PEREIRA REINALDO", "CRISTILAYNE MATIAS DE LIMA", "DAIZE MANOEL DOS SONTOS", 
    "DAMARIS VASCONI DA SILVA", "DANIEL APARECIDO MARASSATTI", "DANIEL AUGUSTO ADAMI", 
    "DANIELI DA SILVA RAMOS", "DANIELLE GOMES DUARTE", "DAPHYNE YACHEL CHAVES", 
    "DAVID LEE BARBOSA MANTOVANI", "DAVYD AUGUSTO CASTELLI DE SOUZA", "DAYANE FERNANDA LIMA DA SILVA", 
    "DAYANE RAFAELA FARIAS FERREIRA TOMAZ", "DEBORA ALESSANDRA PERGER RODRIGUES", 
    "DEBORA APARECIDA PACCOLA REZENDE", "DEBORA LONGO MIYASHITA", "DEBORAH EVELYN CANDIDO ZANOTT", 
    "DEBORAH TORREZAN MARQUES", "DENIA CELESTINA ARAUJO SOUZA", "DEVLYN PICOLOTO SHIL", 
    "DJEINE GONÇALVES DOS SANTOS", "DJULIEL GLEYCSON DA SILVA", "DOUGLAS ARAUJO PEDROLONGO", 
    "DRIELLE LUCIA BASTOS DA SILVA", "EDSON ALVES DE PORTUGAL", "EDSON MURILO DE OLIVEIRA", 
    "ELAINE APARECIDA DE SOUZA", "ELAINE CRISTINA FIRMINO", "ELAINE DO CARMO ROCHA", 
    "ELEN CRIS FRANCO DUARTE", "ELIANA PATRICIA PINTO FERNANDES", "ELIANE MARQUES FERREIRA", 
    "ELIDA ESTEFANIA ALVES TOMAZ", "ELISANGELA APARECIDA LOPES", "ELIZABETH DA SILVA LEMES", 
    "ELLEN APARECIDA COSTA", "EMANUELLI GIGLIOLI OLIVATTO", "EMYLLY YARA TEODORO DOS SANTOS", 
    "ERICA CRISTINA MACHADO DA", "ERICA RODRIGUES CAETANO PEROTA", "EVERTON APARECIDO GARCIA LEAL", 
    "FABIANA JORGE DA SILVA", "FABIANA PRADO DA SILVA", "FABIANO AZEVEDO SERAFIM", 
    "FABIOLA GOMES DOS SANTOS", "FATIMA APARECIDA DE ASSIS", "FERNANDA CRISTINA TERECIANO", 
    "FERNANDA DE SOUZA FERREIRA", "FERNANDA MARQUES YUI", "FERNANDA PARINI NUNES", 
    "FERNANDA SAN JULIANO PEREIRA PAULON", "FILIPE SAN JULIANO PEREIRA", "FLAVIO LIBOIO", 
    "FRANCIELEN DA SILVA RIBEIRO", "FRANCINE APARECIDA K FRANCEZ", "FRANCINE AROTEIA CAPONE", 
    "FRANCINE RODRIGUES DO NASCIMENTO", "FRANKLIN ABNER DE LIMA SANTOS", "GABRIEL BARBOSA SACCARDO", 
    "GABRIEL FERNANDO ROSA ALDIGUERES", "GABRIEL HELENO LUIS", "GABRIELA BENJAMIN TOGASHI", 
    "GABRIELA BERNARDINO MARTINS", "GABRIELA CRISTINA SCHWETER ALBANEZ", "GABRIELA GARCIA", 
    "GABRIELA KRONKA BARBOZA", "GABRIELLY TEOFILO RAMOS MENEGHELLO", "GEOVANA FERREIRA BRANDAO", 
    "GILSIANDRA DA SILVA CAETANO", "GIORDANA DE FREITAS COLACINO MENDES", "GIOVANA ALQUATI DE ALMEIDA", 
    "GIOVANA GONÇALVES COSTA ARAUJO", "GIOVANA GONÇALVES DA SILVA", "GIOVANA RENATA RECUCHE", 
    "GIOVANA SASSO JONAS", "GIOVANNA GALASSO PANNUNZIO", "GISELE ALVES DE MIRA SOUZA", 
    "GISELE ASSIS RIBEIRO TAVARES", "GISELE HERNANDES GONCALVES", "GISELE LIPE BAUTZ", 
    "GISLAINE CRISTINA GUIMARÃES JA", "GIULIA AGUIAR CAMARGO", "GIULIA NARCIZO GARCIA", 
    "GIZELE ARAUJO VALADAO GOMES", "GLAUCIA APARECIDA DE JESUS COLOMBO VIEIRA", 
    "GUILHERME FERNANDO MACIEL PRUDENTE", "GUSTAVO NARDI NOGUEIRA", "IEDA PAPILLE DOS SANTOS", 
    "ISABEL CRISTINA FRANÇA DE OLIVEIRA DA SILVA", "ISABELA APARECIDA RODRIGUES DA CRUZ JERONIMO", 
    "ISABELA CHAVES DE OLIVEIRA", "ISABELA CRISTINA FLORENTINO", "ISABELA DE OLIVEIRA ALVES", 
    "ISABELA INACIO DE CASTRO", "ISABELA MORENO AYRES", "ISABELA POSSIGNOLLO DA SILVA", 
    "ISRAEL MESSIAS GUARDIA", "IVAN VARAS CARDOSO", "IVANA FERREIRA DO NASCIMENTO", 
    "IVY CAROLINA CORREA SANTIAGO S", "IZABELA FERREIRA DE CASTRO BATISTA", "JAMILLE ALESSANDRA LEITE", 
    "JANAINA DE CARVALHO QUEIROGA", "JANETE VICTOR MANGA", "JAQUELINE PEREIRA DE SOUZA", 
    "JEAN CARLO PEREIRA DOS SANTOS", "JESSICA ARIELE GUIMARAES CORTE", "JESSICA CARVALHO DE SOUZA", 
    "JESSICA CRISTINE LEITE", "JESSICA ELLEN LINDOLPHO CREMON", "JESSICA FARIA BARBOSA", 
    "JESSICA WATANABE CONCEICAO", "JHENIFER VITÓRIA DA SILVA MARTINS", "JOAO GABRIEL DA SILVA FREITAS", 
    "JOÃO PEDRO PONCE LOPES", "JOAO VITOR RINALDO DE SOUSA", "JOICE CASTELLI PATROCINIO", 
    "JOSE CARLOS SALVADOR", "JOSELAINE REGIANI RAMOS", "JOSIANE CRISTINA GOMES SEBASTIÃO", 
    "JOSIANE REGO", "JOSIANE SOARES DE SOUZA SANTOS", "JUCILENE MARIA COSTA", "JUCINEIA DOS SANTOS", 
    "JULIA FICHIO MIYAHARA", "JULIA SANCHES DE SOUZA", "JULIA SILVA PEREIRA", "JULIA TELLES PASCON", 
    "JULIANA APARECIDA SCANTIMBURGO MANSO", "JULIANA DA SILVA BUENO", "JULIANA DE FATIMA RIBEIRO", 
    "JULIANA DE OLIVEIRA JUMONJI", "JULIANA MOREIRA LOPES", "JULIANA ORTIZ DA SILVA", 
    "JULIANE MACEGOZA DO AMARAL", "JULIANE PANDOLFI BUENO DE SOUZA ANTONIO", "JULIO CESAR TAVARES", 
    "KARINA MONTEIRO BATISTA", "KARLA RAISSA BELINI BALDONI", "KATHLEEN RUFINO DA SILVA", 
    "KEDMA CASTILHO DE LIMA LUNA", "KESLEY GARCIA IVASSAKI", "KETURI GABRIELA ALVES DA SILVA", 
    "LARA GARCIA DE OLIVEIRA", "LARISSA PEREIRA GONCALVES", "LEANDRO ACACIO DOS SANTOS", 
    "LEANDRO DAVANÇO FREIRE", "LEILANE SIQUEIRA DE GOIS MATHEUS", "LEONARDO AMARAL DE PAULA DA SILVA", 
    "LEONARDO HORNE GOMES", "LEONARDO PEREIRA GOMES", "LEONARDO RICARDO DA SILVA", 
    "LETICIA ALVES FERREIRA", "LETICIA BONAFIM PELLOSO FURTADO", "LETICIA DA SILVA REDECOPA", 
    "LETICIA RUZZON CONEGLIAN", "LIDIANE HELOISA JODAR", "LIGIA MARIA FERREIRA DO CARMO", 
    "LISANDRA DA SILVA RODRIGUES", "LIVIA MOZARDO CASTIGLIOLI", "ANA KARINA BENEDITO PEREIRA", 
    "LORRAYNE FARIAS DOS SANTOS", "LUCIANA ALVES DOS SANTOS", "LUCIANA APARECIDA DA SILVA", 
    "LUCIANA APARECIDA VICENTINI CA", "LUCIANE CRISTINA MAIA DE OLIVEIRA", "LUCIMAR DOS SANTOS CAETANO", 
    "LUCIMARA CARVALHO DE BRITO", "LUIDGI AGNNO ZELNYS CARLOS", "LUIS FELIPE LIZI JORGE", 
    "MAIARA APARECIDA FRANCO DA SILVEIRA", "MAILON LESSA", "MARCELLA CARDOSO GONÇALVES", 
    "MARCELLA MONTOVANELLI MENECHELLI", "MARCELLY CRISTHINE DA SILVA", "MARCELO ANDRADE FERREIRA", 
    "MARCELO JORGE GOMES", "MARIA APARECIDA MARTINS ROSA", "MARIA CAROLINA URSULINO BURATTO FRANCO", 
    "MARIA FERNANDA FRANCISCA PAULA", "MARIA ISABEL DA COSTA", "MARIA LYANDRA CARVALHO", 
    "MARIANA BERTUCCO BAZAN", "MARIANA MAGRO REINATO", "MARIANA PERES FATORI", "MARIANE ALVES JATOBA", 
    "MARISA CRISTINA PRUDENTE RIBEIRO", "MARIUZA GONCALVES VIEIRA", "MARLI GONÇALVES CARNIATO", 
    "MATHEUS CAMARGO MARCIANO", "MATHEUS SILVA ANTONIO", "MAYARA ANDRESSA BRUNA DOS SANTOS", 
    "MAYARA GODOY PANUNTO", "MAYARA MONTOVANI DE OLIVEIRA", "MAYRA DINIZ WASHINGTON", 
    "MELINA RODRIGUES", "MILENA NORONHA MUNHOZ", "MIQUE ERIC GIMENES", "MIRIAM CHRISTINELLI", 
    "MIRIAN HELEN CARNEIRO DE SOUZA", "MIRYELLI CAROLINE MACIEL", "NATALIA ALVES TOSTA OCANHA", 
    "NATALIA CAVALHERI DE SOUZA GUERRERO", "NATALIA CRISTINA DOS SANTOS", "NATALIA FIDENCIO NASCIMENTO", 
    "NATHALIA APAREC B.SOUZA", "NATHALIA DO CARMO LEME INACIO", 
    "NATHALIA GONÇALVES COSTA CASAGRANDE BERNARDO", "NATHALY MARTINUCCI", 
    "NAYANE MARIA DE MELO ALEXANDRINO", "NAYARA COLEONE MUSTACIO ZANELI", "NAYARA SOBRINHO LEITE", 
    "NAYARA TOMAZI BATISTA", "NELI DE FATIMA DANIEL SANTOS", "NEYLA IVETTE YUTRONIC SERRANO", 
    "NEYLOR JOSE ANTUNES DOS SANTOS", "NIELY RAÍSSA LIMA GUIMARÃES", "PAMELA CRISTINA KURIO", 
    "PAMELA LARISSA FRANCO DA CRUZ ALVES", "PAMELLA THAYARA DOS SANTOS", 
    "PATRICIA ALINE RODRIGUES DE SOUZA", "PATRICIA LIZANDRA MORETTI CRUZ", "PATRICIA MIRELI SILVA", 
    "PAULO HENRIQUE MANGILI SERESUELA", "PAULO RICARDO SOLANA", "POLLIANY DO MONTE LANCA", 
    "PRISCILA CALIGARIS CAGI", "PRISCILA DOS SANTOS TRINDADE", "RAFAELA FERNANDA RODRIGUES FAUSTINO", 
    "RAFAELA LOPES ALVES", "RAI SAIKA PINTON", "RAPHAELA GIOVANA ALVES CALVO", 
    "RAQUEL PEREIRA DA CONCEICAO", "RAQUEL PEREIRA DA SILVA", "RAYANE ISABELLE TURKOCIO FERRAREZI", 
    "REGINALDO CAETANO", "RENATA DE PAULA SOARES", "RENATA DI PAULA COSTA", "RICARDO QUIRINO FONSECA", 
    "RICARDO RUIVO BUSCH", "RICHELE BOICO DE SOUZA BARBOSA", "ROBSON LUIZ PEREIRA", 
    "RODRIGO SANTOS SANTANA", "ROSIELI DE CARVALHO", "ROSIMEIRE APARECIDA GARCIA DA SILVA OLIVEIRA", 
    "SABRINA ALBANEZ OLIVIER", "SAMARA MOREIRA INACIO", "SANDRA CRISTINA DIAS CAMARGO MARTINS", 
    "SARA LEONCIO DE MELO GARCIA", "SELMA MARIA DA SILVA", "SHIRLEI APARECIDA PRONUNCIATE GUIMARÃES", 
    "SILVANA APARECIDA STEKER PACHECO", "SILVIA APARECIDA DE SOUZA SANTANA DO NASCIMENTO", 
    "SILVIA HELENA FERNANDES", "SILVIA REGINA CELESTINO", "SILVIA SAYURI YATSU TAHARA", 
    "SIMONE MONTEIRO DA SILVA LOPES", "SIMONE REGINA FARINHA", "SOLANGE CASTILHO", "SOLANGE ESGOTI", 
    "SONIA APARECIDA FAGNANI", "SUELLEN SIMONE GONZALES BERRO", "SUSAN NAWALY GONCALVES SANDOLI", 
    "TAIENE DA SILVA MORETTO", "TAIS DIAS CESARIO", "TALITA CRISTINA DA SILVA RIBEIRO", 
    "TANIA REINALDO MARINS", "TATIANE BAZOTTI COSTA", "TAYOANA CAROLINA SILVA", 
    "THAINA OLIVEIRA FELICIO OLIVATTI", "THAIS CARDOSO DA SILVA SILVIERO", "THAIS CRISTINA ALVES PINTO", 
    "THAIS NAYRA MACHADO", "THAIS OTAVIANA PEREIRA PARDINO", "THAISE MARTINS SANTOS SANTANA", 
    "THALIA MOREIRA MANZUTI GARCIA", "THATIANE FRANCINI DA SILVA FERREIRA", 
    "THIAGO HENRIQUE CHANQUINI FRANCISCO", "TIAGO PEREIRA ALEXANDRE", "TIENE ARCANJO DE OLIVEIRA", 
    "TIFANY DA SILVA TORRES", "VALDINEIA NERIS DE SOUSA", "VALERIA DE MIRANDA", 
    "VANESSA DOMINGOS BARBOSA", "VANESSA FRACALOSSI", "VANUZA BARBOSA LEITE", 
    "VERA LUCIA ALVES DA SILVA", "VICTOR FERREIRA RAMOS COLASSO", 
    "VITÓRIA GABRIELLE RODRIGUES DOS SANTOS", "VIVIAN MARTINS GOMES", "VIVIANI MAXIMINO BAPTISTA BUENO", 
    "VYVIAN KELLEY ALVES CASTILHO", "WANESSA VIEIRA CASTELO RODRIGUES", "WENDLER VINICIUS DA PAIXAO", 
    "WESLEY DOS SANTOS CASTILHO RODRIGUES", "WILLIAM AUGUSTO GRANDO", "YASMIM VITORIA DA SILVA SOUZA", 
    "YURI HOLLANDER", "ZENAIDE BARBOSA HONORATO", "THALES CABRAL BENINI FELISBERTO", 
    "MARIA FERNANDA LOSSILA", "ELIZABETH CRISTINA BATISTA", "REGINA APARECIDA DE FREITAS DOS SANTOS"
]

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
st.caption("Atenção Primária à Saúde - Monitoramento Estratégico")
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
    colunas_nome = [c for c in df.columns if 'NOME' in c and 'COMPLETO' in c]
    if colunas_nome:
        df['NOME COMPLETO'] = df[colunas_nome].bfill(axis=1).iloc[:, 0].str.strip().str.upper()
    
    col_inicio = 'HORÁRIO INICIAL' if 'HORÁRIO INICIAL' in df.columns else 'HORARIO INICIAL'
    col_fim = 'HORÁRIO FINAL' if 'HORÁRIO FINAL' in df.columns else 'HORARIO FINAL'
    col_data = 'DATA DA ATIVIDADE' if 'DATA DA ATIVIDADE' in df.columns else 'CARIMBO DE DATA/HORA'
    col_tema = 'DESCRIÇÃO BREVE DA ATIVIDADE' if 'DESCRIÇÃO BREVE DA ATIVIDADE' in df.columns else df.columns[-1]

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
        m1.metric("Registros", len(df_f))
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

        # --- RESTAURADO: DESTAQUE E TEMAS POR CATEGORIA ---
        c_t1, c_t2 = st.columns([1, 1.5])
        with c_t1:
            st.subheader("Destaques por Unidade")
            destaque = df_f.groupby(['LOTAÇÃO', 'CATEGORIA PROFISSIONAL']).size().reset_index(name='Qtd')
            idx = destaque.groupby('LOTAÇÃO')['Qtd'].idxmax()
            st.dataframe(destaque.loc[idx], use_container_width=True, hide_index=True)
        
        with c_t2:
            st.subheader("Carga Horária e Temas por Categoria")
            resumo = df_f.groupby('CATEGORIA PROFISSIONAL').agg({
                col_tema: lambda x: ' | '.join(x.dropna().astype(str).unique()[:3]) + '...', # Mostra apenas os 3 primeiros para não poluir
                'CH_CALCULADA': 'sum'
            }).reset_index()
            resumo.columns = ['Categoria', 'Exemplos de Temas', 'Total Horas']
            st.dataframe(resumo, use_container_width=True, hide_index=True)

        st.divider()

        # --- ÁREA DA COORDENAÇÃO ---
        st.header("Coordenação | Business Intelligence")
        with st.expander("Autenticação Necessária"):
            senha = st.text_input("Senha de acesso", type="password", key="sec")
            if senha == "bauru2024":
                
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

                # 4. Monitoramento de Gestão
                c_gest1, c_gest2 = st.columns(2)
                with c_gest1:
                    st.subheader("Ranking Individual")
                    st.dataframe(df_f.groupby(['NOME COMPLETO', 'LOTAÇÃO'])['CH_CALCULADA'].sum().sort_values(ascending=False).reset_index(), hide_index=True)
                with c_gest2:
                    st.subheader("Busca Ativa (Zero Horas)")
                    df_mestra = pd.DataFrame({'NOME COMPLETO': [n.upper() for n in LISTA_MESTRA_NOMES]})
                    faltantes = df_mestra[~df_mestra['NOME COMPLETO'].isin(df_f['NOME COMPLETO'].unique())]
                    st.dataframe(faltantes, hide_index=True)
            elif senha:
                st.error("Senha incorreta.")

except Exception as e:
    st.error(f"Erro no processamento: {e}")
