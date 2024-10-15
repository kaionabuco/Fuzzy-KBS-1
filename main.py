import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

# ENGENHO DE INFERÊNCIA
historico_credito = ctrl.Antecedent(np.arange(0, 12, 1), 'historico_credito')
divida = ctrl.Antecedent(np.arange(0, 11, 1), 'divida')
renda_mensal = ctrl.Antecedent(np.arange(0, 100001, 1), 'renda_mensal')
risco = ctrl.Consequent(np.arange(0, 11, 1), 'risco')

historico_credito['ruim'] = fuzz.trimf(historico_credito.universe, [0, 0, 6])
historico_credito['bom'] = fuzz.trimf(historico_credito.universe, [4, 10, 10])
historico_credito['desconhecido'] = fuzz.trimf(historico_credito.universe, [11, 11, 11])
# Valor 11 em histórico de crédito representa "desconhecido"
divida['baixa'] = fuzz.trimf(divida.universe, [0, 0, 6])
divida['alta'] = fuzz.trimf(divida.universe, [4, 10, 10])

renda_mensal['baixa'] = fuzz.trimf(renda_mensal.universe, [0, 0, 1000])
renda_mensal['media'] = fuzz.trimf(renda_mensal.universe, [7500, 15000, 30000])
renda_mensal['alta'] = fuzz.trapmf(renda_mensal.universe, [1500, 35000, 100000, 100000])

risco['baixo'] = fuzz.trimf(risco.universe, [0, 0, 4])
risco['medio'] = fuzz.trimf(risco.universe, [3, 5, 7])
risco['alto'] = fuzz.trimf(risco.universe, [6, 10, 10])

# BASE DE CONHECIMENTO
# Árvore de decisão gerada por C4.5, tirada diretamente da Lista 1, desconsiderando variável "Garantia"
rule1 = ctrl.Rule(renda_mensal['alta'] & historico_credito['desconhecido'] & divida['baixa'], risco['baixo'])
rule2 = ctrl.Rule(renda_mensal['alta'] & historico_credito['desconhecido'] & divida['alta'], risco['medio'])
rule3 = ctrl.Rule(renda_mensal['alta'] & historico_credito['bom'], risco['baixo'])
rule4 = ctrl.Rule(renda_mensal['alta'] & historico_credito['ruim'], risco['medio'])
rule5 = ctrl.Rule(renda_mensal['media'] & historico_credito['desconhecido'] & divida['alta'], risco['alto'])
rule6 = ctrl.Rule(renda_mensal['media'] & historico_credito['bom'] & divida['alta'], risco['medio'])
rule7 = ctrl.Rule(renda_mensal['media'] & historico_credito['ruim'] & divida['alta'], risco['alto'])
rule8 = ctrl.Rule(renda_mensal['baixa'], risco['alto'])

sistema_risco_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8])
sistema_risco = ctrl.ControlSystemSimulation(sistema_risco_ctrl)


# INTERFACE
# Interface de usuário em linha de comando
def avaliar_risco():
    print("Sistema de Avaliação de Risco - Empréstimo")

    try:
        hist_credito = input("O quão bom é o histórico de crédito do cliente, de 0 a 10? "
                             "Insira 'desconhecido' se a informação não estiver disponível.\n")
        if hist_credito == 'desconhecido':
            hist_credito = 11  # Usamos 11 para mapear ao histórico 'desconhecido'
        else:
            hist_credito = float(hist_credito)

        divida_user = float(input("O quão alta é a dívida do cliente, de 0 a 10?\n"))
        renda_user = float(input("Informe a renda mensal do cliente (em R$):\n"))
    except ValueError:
        print("Por favor, insira valores válidos.")
        return

    sistema_risco.input['historico_credito'] = hist_credito
    sistema_risco.input['divida'] = divida_user
    sistema_risco.input['renda_mensal'] = renda_user

    sistema_risco.compute()
    risco_calculado = sistema_risco.output['risco']

    # EXPLICABILIDADE
    if risco_calculado < 4:
        explicacao = "Baixo risco -- Histórico de crédito bom ou renda alta compensam o valor da dívida."
    elif 4 <= risco_calculado < 7:
        explicacao = "Médio risco -- Dívida e histórico moderados, com renda na faixa intermediária."
    else:
        explicacao = "Alto risco -- Alto valor de dívida, histórico de crédito ruim ou baixa renda aumentam o risco."

    print(f"Resultado: Risco calculado = {risco_calculado:.2f} (de 10)")
    print(f"Explicação: {explicacao}")


if __name__ == "__main__":
    while True:
        avaliar_risco()
        continuar = input("Deseja realizar outra avaliação? (s/n): ").strip().lower()
        if continuar != 's':
            break
