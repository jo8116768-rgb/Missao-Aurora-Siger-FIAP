# MGCE - Sistema de gerenciamento inteligente da colonia
# Parte de Pedro Scabio: regras de decisao e desligamento de sistemas nao essenciais.
# Manter este arquivo na mesma pasta que Dados.py.

from Dados import colonia, geracao_total, consumo_total

# Limite adotado para considerar a potencia disponivel baixa.
# O enunciado apresenta 50 como exemplo; aqui usamos 50 kW.
LIMITE_GERACAO_KW = 50.0


def desligar_nao_essenciais(colonia_dados):
    """Desliga equipamentos nao essenciais e informa o que foi desligado."""
    desligados = []

    # Primeiro, desliga apenas equipamentos nao essenciais que estejam ativos.
    for setor, componentes in colonia_dados.items():
        if setor == "energético":
            continue

        for nome, info in componentes.items():
            if info.get("essencial") == False and info.get("status") == "ativo":
                info["status"] = "inativo"
                desligados.append(nome)

    return desligados


def decidir(colonia_dados):
    """Analisa a situacao e aplica as regras por ordem de prioridade."""
    geracao = geracao_total(colonia_dados)
    consumo = consumo_total(colonia_dados)
    geracao_baixa = geracao < LIMITE_GERACAO_KW
    consumo_alto = consumo > geracao

    print("\n=== ANALISE ENERGETICA DA COLONIA ===")
    print(f"Geracao disponivel: {geracao:.1f} kW")
    print(f"Consumo atual: {consumo:.1f} kW")
    print(f"Balanco: {geracao - consumo:.1f} kW")

    # Prioridade 1: duas condicoes criticas ao mesmo tempo.
    if geracao_baixa and consumo_alto:
        print("ALERTA CRITICO: geracao baixa e consumo maior que a geracao!")
        print("ACAO: ativar modo de economia e preservar suporte a vida.")
        desligados = desligar_nao_essenciais(colonia_dados)

    # Prioridade 2: consumo acima da geracao, mesmo sem geracao baixa.
    elif consumo_alto:
        print("ALERTA: consumo maior que a geracao!")
        print("ACAO: reduzir consumo desligando sistemas nao essenciais.")
        desligados = desligar_nao_essenciais(colonia_dados)

    # Prioridade 3: geracao baixa, mesmo que ainda cubra o consumo.
    elif geracao_baixa:
        print("ATENCAO: geracao abaixo de 50 kW.")
        print("ACAO: economizar energia e manter sistemas essenciais.")
        desligados = desligar_nao_essenciais(colonia_dados)

    # Prioridade 4: operacao normal.
    else:
        print("STATUS: operacao normal. Geracao suficiente.")
        print("SUGESTAO: armazenar eventual excedente, se houver reserva disponivel.")
        desligados = []

    if desligados:
        print("Equipamentos desligados:", ", ".join(desligados))
    elif geracao_baixa or consumo_alto:
        print("Nenhum equipamento nao essencial ativo para desligar.")

    # Recalcula o consumo apos os desligamentos.
    consumo_final = consumo_total(colonia_dados)
    print(f"Consumo apos decisao: {consumo_final:.1f} kW")
    print(f"Balanco apos decisao: {geracao - consumo_final:.1f} kW")

    # Aviso importante: o sistema nunca desliga componentes essenciais.
    if consumo_final > geracao:
        print("ALERTA: ainda ha deficit! Os sistemas essenciais foram preservados.")

    return {
        "geracao_kw": geracao,
        "consumo_inicial_kw": consumo,
        "consumo_final_kw": consumo_final,
        "desligados": desligados
    }


# Testes independentes: cada cenario usa uma copia dos dados originais.
if __name__ == "__main__":
    from copy import deepcopy

    print("\nTESTE 1 - Operacao normal")
    teste1 = deepcopy(colonia)
    decidir(teste1)

    print("\nTESTE 2 - Geracao baixa")
    teste2 = deepcopy(colonia)
    teste2["energético"]["solar"]["status"] = "inativo"
    decidir(teste2)

    print("\nTESTE 3 - Consumo alto")
    teste3 = deepcopy(colonia)
    teste3["modulos_auxiliares"]["laboratorio_pesquisa"]["consumo_kw"] = 70.0
    decidir(teste3)

    print("\nTESTE 4 - Geracao baixa E consumo alto")
    teste4 = deepcopy(colonia)
    teste4["energético"]["solar"]["status"] = "inativo"
    teste4["modulos_auxiliares"]["laboratorio_pesquisa"]["consumo_kw"] = 70.0
    decidir(teste4)
