# --- BLOCO 4: GERADOR DE INFORME PARA WHATSAPP ---
        st.markdown("---")
        st.subheader("📱 Informe para WhatsApp")
        st.markdown("Revise o resumo automático das atividades filtradas e compartilhe com as equipes.")

        # Montando as variáveis do texto
        unidades_texto = ", ".join(f_unidade) if f_unidade else "Toda a Rede"
        meses_texto = ", ".join(f_mes) if f_mes else "Período Geral"
        total_horas = f"{df_f['CH_CALCULADA'].sum():.1f}"
        total_capacitacoes = len(df_f)

        # Escrevendo a mensagem formatada para o WhatsApp
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

        # Caixa de texto para edição
        texto_editavel = st.text_area("Edite a mensagem abaixo se necessário:", value=mensagem, height=250)

        # Codificando o texto para link
        texto_formatado_url = urllib.parse.quote(texto_editavel)
        
        # Link 1: Força abrir no WhatsApp Web (Navegador) - Costuma falhar menos no PC
        link_web = f"https://web.whatsapp.com/send?text={texto_formatado_url}"
        
        # Link 2: O formato curto oficial (wa.me) para o aplicativo
        link_app = f"https://wa.me/?text={texto_formatado_url}"

        col_w1, col_w2 = st.columns(2)
        with col_w1:
            st.link_button("🌐 Enviar pelo WhatsApp WEB", link_web, type="primary", use_container_width=True)
        with col_w2:
            st.link_button("📱 Enviar pelo Aplicativo", link_app, use_container_width=True)
            
        st.caption("💡 **Dica:** Se os botões falharem devido ao bloqueio do computador, basta clicar dentro da caixa de texto acima, apertar **Ctrl+A** (selecionar tudo), depois **Ctrl+C** (copiar) e colar direto na sua conversa!")
