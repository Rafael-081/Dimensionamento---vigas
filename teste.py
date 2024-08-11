import streamlit as st
import math

# Cabeçalho
st.markdown("""
    <div style='text-align: center; margin-bottom: 20px;'>
        <h1>Universidade Federal de Pernambuco</h1>
        <h5>Engenharia Civil</h5>
        <p>Disciplina: Concreto 1</p>
        <p>Aluno: Edmilson Ferreira</p>
    </div>
""", unsafe_allow_html=True)

# Título do aplicativo
st.title("Calculadora de Área de Aço em Vigas Sujeitas à Flexão Simples")

# Entrada de dados
d = st.number_input("Digite o valor de d (altura útil da seção em cm):", min_value=0.0, step=1.0)
fsd1 = st.number_input("Digite o valor da tensão de escoamento do aço em MPa:", min_value=0.0, step=1.0)
bw = st.number_input("Digite o valor de bw (largura da alma em cm):", min_value=0.0, step=1.0)
fck = st.number_input("Digite o valor de fck (resistência característica do concreto em MPa):", min_value=0.0, step=1.0)
MDe = st.number_input("Digite o valor de MD (momento de cálculo em KN.m):", min_value=0.0, step=1.0)
b1 = st.number_input("Digite o valor de b1 (largura da aba 1 da mesa  em cm em cm):", min_value=0.0, step=1.0)
b3 = st.number_input("Digite o valor de b3 (largura da aba 3 da mesa  em cm):", min_value=0.0, step=1.0)
h_aba = st.number_input("Digite o valor de h_aba (altura da mesa da seção T em cm):", min_value=0.0, step=1.0)

# Botão de cálculo
if st.button("CALCULAR"):
    fsd = fsd1 / 10
    MD = MDe * 100
    bf = b1 + b3 + bw
    
    aux = bf * 0.8 * 0.85 * (fck / 14)
    a = aux * -0.4
    b = aux * d
    c = -MD
    w = d

    def solver_positivo_menor_que_w(a, b, c, w):
        delta = b**2 - 4*a*c

        if delta < 0:
            x = []
        elif delta == 0:
            raiz = -b / (2*a)
            x = [raiz] if 0 < raiz < w else []
        else:
            raiz1 = (-b + math.sqrt(delta)) / (2*a)
            raiz2 = (-b - math.sqrt(delta)) / (2*a)
            x = [raiz for raiz in [raiz1, raiz2] if 0 < raiz < w]
        
        return x

    x = solver_positivo_menor_que_w(a, b, c, w)

    if b1 == b3 == 0:
        if x and x[0] / d < 0.45:
            As = MD / ((fsd / 1.15) * (d - 0.4 * x[0]))
            st.success(f"A área de aço inferior As é: {As:.2f} cm²")
        else:
            x0 = 0.45 * d
            MD1 = 0.85 * (fck / 14) * 0.8 * bw * x0 * (d - 0.4 * x0)
            As = MD1 / ((fsd / 1.15) * (d - 0.4 * x0)) + (MD - MD1) / ((fsd / 1.15) * (d - 0.1 * d))
            Asinf = (MD - MD1) / ((fsd / 1.15) * (d - 0.1 * d))
            st.success(f"A área de aço inferior As é: {As:.2f} cm²")
            st.success(f"A área de aço superior As,inf é: {Asinf:.2f} cm²")
    else:
        if x and 0.8 * x[0] < h_aba:
            As = MD / ((fsd / 1.15) * (d - 0.4 * x[0]))
            st.success(f"A área de aço inferior As é: {As:.2f} cm²")
        else:
            MD_ABA = (bf - bw) * h_aba * 0.85 * (fck / 14) * (d - h_aba / 2)
            aux = bw * 0.8 * 0.85 * (fck / 14)
            a = aux * -0.4
            b = aux * d
            c = -(MD - MD_ABA)
            y = solver_positivo_menor_que_w(a, b, c, w)
            
            if y:
                if x and y[0] / d < 0.45:
                    MD_ABA = (bf - bw) * h_aba * 0.85 * (fck / 14) * (d - h_aba / 2)
                    As_aba = MD_ABA / ((fsd / 1.15) * (d - h_aba / 2))
                    As = (MD - MD_ABA) / ((fsd / 1.15) * (d - 0.4 * y[0]))
                    Ast = As + As_aba
                    st.success(f"A área de aço inferior As é: {Ast:.2f} cm²")
                else:
                    x0 = 0.45 * d
                    MD_ABA = (bf - bw) * h_aba * 0.85 * (fck / 14) * (d - h_aba / 2)
                    As_aba = MD_ABA / ((fsd / 1.15) * (d - h_aba / 2))
                    MD_ALMA = MD - MD_ABA
                    MD1 = 0.85 * (fck / 14) * 0.8 * bw * x0 * (d - 0.4 * x0)
                    As = MD1 / ((fsd / 1.15) * (d - 0.4 * x0)) + (MD_ALMA - MD1) / ((fsd / 1.15) * (d - 0.1 * d)) + As_aba
                    Asinf = (MD_ALMA - MD1) / ((fsd / 1.15) * (d - 0.1 * d))
                    st.success(f"A área de aço inferior As é: {As:.2f} cm²")
                    st.success(f"A área de aço superior As,sup é: {Asinf:.2f} cm²")
            else:
                st.error("Não foi possível calcular a nova linha neutra e a área de aço.")
