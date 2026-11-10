
# Mantenha este arquivo na mesma pasta que Dados.py.
# Os historicos sao importados diretamente de Dados.py para evitar duplicacao.

from dados import historico_vento, historico_energia


def ajustar_reta(ventos, energias):
    """
    Calcula os coeficientes a e b da reta de regressão linear y = a*x + b.

    Parâmetros:
        ventos: lista com velocidades do vento (m/s).
        energias: lista com as geracoes eolicas correspondentes (kW).

    Retorno:
        Uma tupla (a, b), em que:
        a = inclinação da reta;
        b = ponto em que a reta cruza o eixo y.
    """
    if len(ventos) != len(energias):
        raise ValueError("As listas de vento e energia devem ter o mesmo tamanho.")

    if len(ventos) < 2:
        raise ValueError("São necessários pelo menos dois pares de dados.")

    quantidade = len(ventos)

    media_vento = sum(ventos) / quantidade
    media_energia = sum(energias) / quantidade

    numerador = 0.0
    denominador = 0.0

    for i in range(quantidade):
        numerador += (ventos[i] - media_vento) * (energias[i] - media_energia)
        denominador += (ventos[i] - media_vento) ** 2

    if denominador == 0:
        raise ValueError("Não é possível ajustar a reta: todas as velocidades são iguais.")

    a = numerador / denominador
    b = media_energia - (a * media_vento)

    return a, b


def prever(vento, a, b):
    """
    Estima a geracao eólica para uma velocidade de vento informada.

    Parâmetros:
        vento: velocidade do vento em m/s.
        a: inclinação calculada por ajustar_reta().
        b: intercepto calculado por ajustar_reta().

    Retorno:
        Energia estimada em kW (sem arredondamento interno).
    """
    energia_prevista = a * vento + b
    return energia_prevista


# Teste independente: executa somente quando este arquivo e rodado diretamente.
# Quando outro arquivo importar estas funcoes, os testes nao serao executados.
if __name__ == "__main__":
    a, b = ajustar_reta(historico_vento, historico_energia)
    resultado = prever(11.0, a, b)

    print("=== TESTE DO MODELO DE PREVISAO EOLICA ===")
    print(f"Inclinação da reta (a): {a:.4f}")
    print(f"Intercepto da reta (b): {b:.4f}")
    print(f"Previsão para vento de 11 m/s: {resultado:.2f} kW")
