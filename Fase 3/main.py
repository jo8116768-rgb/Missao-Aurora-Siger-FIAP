# MGCE - Sistema de gerenciamento inteligente da colonia


# ARQUIVO: main.py (programa principal)

# Esse arquivo nao cria regras nem formulas novas: ele só chama e usa, na ordem
# certa as funcoes dos outros arquivos:

#   dados.py = organiza os dados da colonia (dicionarios, listas, hierarquia)
#   previsao.py = regressao linear: vento -> energia eolica
#   analise.py = compara geracao x consumo (x reserva)
#   decisoes.py = regras de prioridade e desligamento de nao essenciais

# Fluxo de cada cenario:  PREVER -> ANALISAR -> DECIDIR
# Assim o sistema deixa de so reagir e reage ao problema,
# usando o vento previsto (sistema preditivo).

# Para rodar: python main.py  (todos os arquivos na MESMA pasta)
 
# deepcopy copia um dicionario inteiro (inclusive os de dentro). Precisamos
# disso porque decidir() ALTERA os dados ao desligar equipamentos.

from copy import deepcopy
 
from dados import (colonia, historico_vento, historico_energia,
                   geracao_total, consumo_total)
from previsao import ajustar_reta, prever
from analise import analisar
from decisoes import decidir
 
 
def simular_cenario(nome, vento, solar_ativo, a, b, reserva=0.0):
    """
    Roda o sistema para um cenario.
 
    Parâmetros:
        nome: título mostrado na tela.
        vento: velocidade do vento (m/s).
        solar_ativo: True se o painel solar funciona, False se esta fora.
        a, b: coeficientes da reta de previsao (calculados uma vez no main).
        reserva: energia armazenada em kWh (opcional).
    """
    print("\n" + "=" * 55)
    print(f"CENÁRIO: {nome}")
    print("=" * 55)
 
    # Trabalha numa COPIA. Sem isso, o que um cenario desliga (ex.: laboratorio)
    # continuaria desligado nos cenarios seguintes.
    copia = deepcopy(colonia)
 
    # previsao: estima a energia eolica a partir do vento
    capacidade = copia["energético"]["eolico"]["capacidade_kw"]
    eolica = prever(vento, a, b)
 
    # A reta e so uma estimativa e nao conhece limites fisicos da turbina:
    # min() corta o que passa da capacidade; max() evita energia negativa.
    eolica = max(0.0, min(eolica, capacidade))
 
    # Troca a capacidade do eolico (na copia) pelo valor PREVISTO. Assim a
    # funcao geracao_total() de dados.py ja soma a energia prevista.
    copia["energético"]["eolico"]["capacidade_kw"] = eolica
 
    # Simula falha do painel solar (geracao_total ignora geradores "inativo")
    if not solar_ativo:
        copia["energético"]["solar"]["status"] = "inativo"
 
    print(f"Entrada: vento = {vento} m/s | solar = {'ativo' if solar_ativo else 'FORA'}")
    print(f"Previsão de energia eólica: {eolica:.1f} kW")
 
    # analise: compara geracao x consumo
    geracao = geracao_total(copia)
    consumo = consumo_total(copia)
    print(f"Geração: {geracao:.1f} kW | Consumo: {consumo:.1f} kW")
    print(analisar(geracao, consumo, reserva))
 
    # decisao: aplica as regras e desliga os nao essenciais
    decidir(copia)
 
 
def main():
    print("-------- MGCE - GERENCIAMENTO INTELIGENTE DA COLONIA --------")

    # Treina o modelo uma vez com os historicos de dados.py.
    # a = inclinacao da reta; b = ponto onde ela cruza o eixo y.
    a, b = ajustar_reta(historico_vento, historico_energia)
    print(f"Modelo de previsão: energia = {a:.4f} * vento + ({b:.4f})")

    # Teste rapido do modelo: para vento = 11 m/s, a previsao fica perto de 27 kW.
    print(f"Previsão de teste: vento = 11 m/s -- {prever(11.0, a, b):.1f} kW")

    # Tres cenarios: normal, critico sem reserva e critico com reserva
    simular_cenario("Dia normal", 11.0, True, a, b)
    simular_cenario("Vento fraco e painel solar fora", 4.0, False, a, b)
    simular_cenario("Mesmo cenário, com reserva de 100 kWh", 4.0, False, a, b, reserva=100.0)
 
 
# So executa main() quando o arquivo e rodado direto (python main.py).
if __name__ == "__main__":
    main()
 