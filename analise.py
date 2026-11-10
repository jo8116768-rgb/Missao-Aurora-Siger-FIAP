# Funcao desse arquivo: Analisar o uso de energia, comparar GERACAO, CONSUMO e (se houver) RESERVA e gerar uma acao simples.

# Regras:
#   consumo > geracao  -> risco  -> "ALERTA: consumo maior que geracao"
#   geracao > consumo  -> sobra  -> "SUGESTAO: armazenar energia excedente"

# Unidades: geracao e consumo em kW; reserva em kWh.

# Este arquivo so ANALISA. Quem desliga equipamentos é decisoes.py.
 
 
def analisar(geracao, consumo, reserva=0.0):
    """
    Compara geração e consumo e devolve uma mensagem (texto).
 
    Parâmetros:
        geracao: energia gerada no momento (kW).
        consumo: energia consumida no momento (kW).
        reserva: energia armazenada (kWh). Opcional: se nao for informada,
                 vale 0.0 (ou seja, "sem reserva").
    """
    # Caso 1: consumo maior que a geracao -> falta energia (risco)
    if consumo > geracao:
        deficit = consumo - geracao  # quanto falta, em kW
 
        # Se a reserva for pelo menos igual ao deficit, ela segura a
        # situacao (por cerca de 1 hora ou mais). Entao avisamos disso.
        if reserva >= deficit:
            return "ALERTA: consumo maior que geração (reserva cobre o deficit)"
 
        # Sem reserva suficiente, o alerta e o simples do enunciado.
        return "ALERTA: consumo maior que geração"
 
    # Caso 2: geracao maior que o consumo -> sobra energia (possivel desperdicio)
    if geracao > consumo:
        return "SUGESTÃO: armazenar energia excedente"
 
    # Caso 3: se chegou aqui, nao e maior nem menor, entao e igual.
    return "EQUILÍBRIO: geração igual ao consumo"

 
# TESTE LOCAL: so roda com "python analise.py".
# Quando o main.py importa este arquivo, este bloco e ignorado.
 

if __name__ == "__main__":
    print("=== TESTE DE ANALISE ===")
    print(analisar(40, 70))       # exemplo 1 do enunciado -> ALERTA
    print(analisar(80, 30))       # exemplo 2 do enunciado -> SUGESTAO
    print(analisar(50, 50))       # empate -> EQUILIBRIO
    print(analisar(40, 70, 100))  # deficit de 30 kW, reserva de 100 cobre
 