import streamlit as st
import pandas as pd
import urllib.parse

# Configuração da página para aproveitar toda a largura da tela
st.set_page_config(page_title="Dashboard EP - Bauru", layout="wide", initial_sidebar_state="expanded")

# ==========================================
# CONFIGURAÇÃO DO LINK (GOOGLE SHEETS)
LINK_GOOGLE_SHEETS = "https://docs.google.com/spreadsheets/d/1yGdTyQWTTYOTEpzJqzu3M5KG1dv9Y7uEc-NbPedPNGU/export?format=xlsx"
# ==========================================

@st.cache_data(ttl=60)
def carregar_dados(url):
    df = pd.read_excel(url, engine='openpyxl')
    return df

# Cabeçalho do Dashboard
st.title("📊 Painel de Indicadores - Educação Permanente")
st.markdown("Análise visual de engajamento e carga horária da ESF.")

# Botão de atualização
if st.sidebar.button("🔄 Atualizar Base de Dados"):
    st.cache_data.clear()
    st.rerun()

try:
    with st.spinner('Sincronizando com a planilha...'):
        df = carregar_dados(LINK_GOOGLE_SHEETS)
        
    # --- PROCESSAMENTO DOS DADOS ---
    df.columns = df.columns.str.strip().str.upper()
    
    # 1. UNIFICAÇÃO INTELIGENTE DE COLUNAS DE NOME
    # Procuramos todas as colunas que contenham "NOME" e "COMPLETO"
    colunas_nome = [c for c in df.columns if 'NOME' in c and 'COMPLETO' in c]
    if colunas_nome:
        # Mesclamos as colunas: onde a primeira estiver vazia, pegamos o dado da segunda
        df['NOME COMPLETO'] = df[colunas_nome].bfill(axis=1).iloc[:, 0]
    
    # Identificação das colunas de tempo
    col_inicio = 'HORÁRIO INICIAL' if 'HORÁRIO INICIAL' in df.columns else 'HORARIO INICIAL'
    col_fim = 'HORÁRIO FINAL' if 'HORÁRIO FINAL' in df.columns else 'HORARIO FINAL'
    col_data = 'DATA DA ATIVIDADE' if 'DATA DA ATIVIDADE' in df.columns else 'CARIMBO DE DATA/HORA'

    # 2. Tratamento de Horas e Carga Horária
    inicio_dt = pd.to_datetime(df[col_inicio].astype(str), errors='coerce')
    fim_dt = pd.to_datetime(df[col_fim].astype(str), errors='coerce')
    df['CH_CALCULADA'] = (fim_dt - inicio_dt).dt.total_seconds() / 3600
    df['CH_CALCULADA'] = df['CH_CALCULADA'].fillna(0).apply(lambda x: max(0, x))

    # 3. Tratamento de Datas e Extração do Mês
    df['DATA_DT'] = pd.to_datetime(df[col_data], errors='coerce')
    df['MÊS'] = df['DATA_DT'].dt.strftime('%m - %b')
    df = df.sort_values('DATA_DT')

    # --- BARRA LATERAL: FILTROS AVANÇADOS ---
    st.sidebar.header("🔍 Filtros de Análise")
    
    meses = sorted(df['MÊS'].dropna().unique().tolist())
    unidades = sorted(df['LOTAÇÃO'].dropna().unique().tolist())
    profissionais = sorted(df['NOME COMPLETO'].dropna().unique().tolist())
    categorias = sorted(df['CATEGORIA PROFISSIONAL'].dropna().unique().tolist())

    f_mes = st.sidebar.multiselect("📅 Selecione o Mês:", meses)
    f_unidade = st.sidebar.multiselect("📍 Unidade (Lotação):", unidades)
    f_categoria = st.sidebar.multiselect("⚕️ Categoria Profissional:", categorias)
    f_nome = st.sidebar.multiselect("👤 Nome do Profissional:", profissionais)

    # Aplicação da Lógica de Filtro
    df_f = df.copy()
    if f_mes: df_f = df_f[df_f['MÊS'].isin(f_mes)]
    if f_unidade: df_f = df_f[df_f['LOTAÇÃO'].isin(f_unidade)]
    if f_categoria: df_f = df_f[df_f['CATEGORIA PROFISSIONAL'].isin(f_categoria)]
    if f_nome: df_f = df_f[df_f['NOME COMPLETO'].isin(f_nome)]

    if df_f.empty:
        st.warning("⚠️ Nenhum dado encontrado para os filtros aplicados.")
    else:
        # --- BLOCO 1: MÉTRICAS GERAIS ---
        m1, m2, m3 = st.columns(3)
        m1.metric("Total de Capacitações", len(df_f))
        m2.metric("Horas Totais Formativas", f"{df_f['CH_CALCULADA'].sum():.1f} h")
        m3.metric("Média de Horas/Atividade", f"{(df_f['CH_CALCULADA'].mean()):.1f} h")

        st.markdown("---")

        # --- BLOCO 2: GRÁFICOS VISUAIS ---
        col_esq, col_dir = st.columns(2)

        with col_esq:
            st.subheader("📈 Ranking de Registros por Unidade")
            chart_registros = df_f['LOTAÇÃO'].value_counts().sort_values(ascending=True)
            st.bar_chart(chart_registros, color="#29b5e8")

        with col_dir:
            st.subheader("⏱️ Carga Horária Total por Unidade")
            chart_horas = df_f.groupby('LOTAÇÃO')['CH_CALCULADA'].sum().sort_values(ascending=True)
            st.bar_chart(chart_horas, color="#ff4b4b")

        st.markdown("---")

        # --- BLOCO 3: ANÁLISE DETALHADA ---
        c1, c2 = st.columns([1, 1.5])
        
        with c1:
            st.subheader("🏆 Destaque Profissional por Unidade")
            destaque = df_f.groupby(['LOTAÇÃO', 'CATEGORIA PROFISSIONAL']).size().reset_index(name='Qtd')
            idx = destaque.groupby('LOTAÇÃO')['Qtd'].idxmax()
            st.dataframe(destaque.loc[idx, ['LOTAÇÃO', 'CATEGORIA PROFISSIONAL', 'Qtd']], use_container_width=True, hide_index=True)

        with c2:
            st.subheader("📋 Resumo de Temas por Categoria")
            resumo = df_f.groupby('CATEGORIA PROFISSIONAL').agg({
                'DESCRIÇÃO BREVE DA ATIVIDADE': lambda x: ' | '.join(x.dropna().astype(str).unique()),
                'CH_CALCULADA': 'sum'
            }).reset_index()
            resumo.columns = ['CATEGORIA', 'TEMAS TRABALHADOS', 'TOTAL HORAS']
            resumo['TOTAL HORAS'] = resumo['TOTAL HORAS'].round(1).astype(str) + " h"
            st.dataframe(resumo, use_container_width=True, hide_index=True)

        # Tabela Bruta (Expansível)
        with st.expander("🔍 Ver todos os detalhes dos profissionais filtrados"):
            st.write(df_f[['DATA DA ATIVIDADE', 'NOME COMPLETO', 'LOTAÇÃO', 'CATEGORIA PROFISSIONAL', 'CH_CALCULADA']])

        # --- BLOCO 4: GERADOR DE INFORME PARA WHATSAPP ---
        st.markdown("---")
        st.subheader("📱 Informe para WhatsApp")
        st.markdown("Revise o resumo automático das atividades filtradas e compartilhe com as equipes.")

        unidades_texto = ", ".join(f_unidade) if f_unidade else "Toda a Rede"
        meses_texto = ", ".join(f_mes) if f_mes else "Período Geral"
        total_horas = f"{df_f['CH_CALCULADA'].sum():.1f}"
        total_capacitacoes = len(df_f)

        mensagem = f"🏥 *Informe de Educação Permanente*\n"
        mensagem += f"📍 *Unidade(s):* {unidades_texto}\n"
        mensagem += f"📅 *Referência:* {meses_texto}\n\n"
        mensagem += f"✅ *Atividades Registradas:* {total_capacitacoes}\n"
        mensagem += f"⏳ *Carga Horária Total:* {total_horas}h\n\n"

        if 'TIPO DE ATIVIDADE REALIZADA' in df_f.columns:
            temas_comuns = df_f['TIPO DE ATIVIDADE REALIZADA'].value_counts().head(3).index.tolist()
            if temas_comuns:
                mensagem += f"📌 *Principais Focos Trabalhados:*\n"
                for tema in temas_comuns:
                    mensagem += f"- {tema}\n"

        mensagem += f"\nParabéns a todos pelo excelente engajamento e vamos juntos planejar os próximos passos! 💪"

        texto_editavel = st.text_area("Edite a mensagem abaixo se necessário antes de enviar:", value=mensagem, height=250)

        texto_formatado_url = urllib.parse.quote(texto_editavel)
        
        link_web = f"https://web.whatsapp.com/send?text={texto_formatado_url}"
        link_app = f"https://wa.me/?text={texto_formatado_url}"

        col_w1, col_w2 = st.columns(2)
        with col_w1:
            st.link_button("🌐 Enviar pelo WhatsApp WEB", link_web, type="primary", use_container_width=True)
        with col_w2:
            st.link_button("📱 Enviar pelo Aplicativo", link_app, use_container_width=True)
            
        st.caption("💡 **Dica:** Se os botões falharem, basta clicar no texto acima, apertar Ctrl+A e Ctrl+C para copiar!")

except Exception as e:
    st.error(f"Erro ao processar dados: {e}")
