import math
import streamlit as st

# Cabeçalho da aplicação
st.markdown("<h4 style='text-align: center; margin-bottom: 10px;'>Universidade Federal de Pernambuco</h4>", unsafe_allow_html=True)
st.markdown("<h5 style='text-align: center; margin-top: -10px;'>Aluno: Edmilson Ferreira</h5>", unsafe_allow_html=True)

# Título da aplicação
st.title("Calculadora de Área de Aço em Vigas Sujeitas à Flexão Simples")

# Mensagem informativa
st.info("Os valores padrão abaixo são apenas exemplos. Altere-os conforme necessário.")

# Entradas do usuário
st.header("Insira os valores abaixo:")

d = st.number_input("Valor da altura útil da viga (cm)", value=36.0)
fsd1 = st.number_input("Valor da tensão de escoamento do aço (MPa)", value=500.0)
bw = st.number_input("Valor da largura da alma (cm)", value=14.0)
fck = st.number_input("Valor de fck do concreto (MPa)", value=25.0)
MDe = st.number_input("Valor do momento de cálculo (kN.m)", value=89.69)
b1 = st.number_input("Valor do comprimento da aba lateral b1 (cm)", value=0.0)
b3 = st.number_input("Valor do comprimento da aba lateral b3 (cm)", value=0.0)
h_aba = st.number_input("Valor da altura da mesa (cm)", value=0.0)

# Botão para calcular
if st.button("Calcular"):
    # Cálculos iniciais
    fsd = fsd1 / 10
    MD = MDe * 100
    bf = b1 + b3 + bw
    aux = bf * 0.8 * 0.85 * (fck / 14)
    a = aux * -0.4
    b = aux * d
    c = -MD
    w = d

    x = solver_positivo_menor_que_w(a, b, c, w)

    # Exibição dos resultados
    if b1 == b3 == 0:
        if x and x[0] / d < 0.45:
            As = MD / ((fsd / 1.15) * (d - 0.4 * x[0]))
            st.write(f"A área de aço inferior As é: {As:.2f} cm²")
        else:
            x0 = 0.45 * d
            MD1 = 0.85 * (fck / 14) * 0.8 * bw * x0 * (d - 0.4 * x0)
            As = MD1 / ((fsd / 1.15) * (d - 0.4 * x0)) + (MD - MD1) / ((fsd / 1.15) * (d - 0.1 * d))
            Asinf = (MD - MD1) / ((fsd / 1.15) * (d - 0.1 * d))
            As1 = MD1 / ((fsd / 1.15) * (d - 0.4 * x0))
            st.write(f"A parcela As1 da área inferior de aço é: {As1:.2f} cm²")
            st.write(f"A área total inferior de aço inferior As é: {As:.2f} cm²")
            st.write(f"A área superior de aço é: {Asinf:.2f} cm²")
    else:
        if x and 0.8 * x[0] < h_aba:
            As = MD / ((fsd / 1.15) * (d - 0.4 * x[0]))
            st.write(f"A área de aço inferior As é: {As:.2f} cm²")
        else:
            MD_ABA = (bf - bw) * h_aba * 0.85 * (fck / 14) * (d - h_aba / 2)
            aux = bw * 0.8 * 0.85 * (fck / 14)
            a = aux * -0.4
            b = aux * d
            c = -(MD - MD_ABA)
            w = d
            y = solver_positivo_menor_que_w(a, b, c, w)
        
            if y:
                if x and y[0] / d < 0.45:
                    MD_ABA = (bf - bw) * h_aba * 0.85 * (fck / 14) * (d - h_aba / 2)
                    As_aba = MD_ABA / ((fsd / 1.15) * (d - h_aba / 2))
                    As = (MD - MD_ABA) / ((fsd / 1.15) * (d - 0.4 * y[0]))
                    Ast = As + As_aba
                    st.write(f"A área inferior de aço para o momento resistido pelas abas é: {As_aba:.2f} cm²")
                    st.write(f"A área inferior de aço para o momento resistido pela alma é: {As:.2f} cm²")
                    st.write(f"A área de aço inferior As é: {Ast:.2f} cm²")
                else:
                    x0 = 0.45 * d
                    MD_ABA = (bf - bw) * h_aba * 0.85 * (fck / 14) * (d - h_aba / 2)
                    As_aba = MD_ABA / ((fsd / 1.15) * (d - h_aba / 2))
                    MD_ALMA = MD - MD_ABA
                    MD1 = 0.85 * (fck / 14) * 0.8 * bw * x0 * (d - 0.4 * x0)
                    As = MD1 / ((fsd / 1.15) * (d - 0.4 * x0)) + (MD_ALMA - MD1) / ((fsd / 1.15) * (d - 0.1 * d)) + As_aba
                    Asinf = ( (MD - MD_ABA) - MD1) / ((fsd / 1.15) * (d - 0.1 * d))
                    As_alma = MD1 / ((fsd / 1.15) * (d - 0.4 * x0))
                    st.write(f"A área inferior de aço para o momento resistido pelas abas é: {As_aba:.2f} cm²")
                    st.write(f"A área inferior de aço para o momento resistido pela alma é: {As_alma:.2f} cm²")
                    st.write(f"A área inferior total de aço (As) é: {As:.2f} cm²")
                    st.write(f"A área superior de aço (As,sup) é: {Asinf:.2f} cm²")
            else:
                st.write("Não foi possível calcular a área de aço.")
