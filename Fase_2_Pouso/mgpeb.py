# MGPEB - Módulo de Gerenciamento de Pouso e Estabilização de Base
# Missão Aurora Siger
#
# Constante global definindo o limite mínimo de combustível para operação segura
LIMITE_COMBUSTIVEL = 30

# Estrutura de Fila (FIFO) pré-populada com os dados oficiais da missão
fila_pouso = [
    {"nome": "Energia", "prioridade": "Alta", "combustivel": 55.0, "massa": 9.0, "criticidade": "Alta", "horario_chegada": "08:00"},
    {"nome": "Habitação", "prioridade": "Alta", "combustivel": 70.0, "massa": 12.0, "criticidade": "Alta", "horario_chegada": "08:30"},
    {"nome": "Comunicações", "prioridade": "Média", "combustivel": 25.0, "massa": 4.0, "criticidade": "Alta", "horario_chegada": "09:00"},
    {"nome": "Estufa", "prioridade": "Baixa", "combustivel": 40.0, "massa": 8.0, "criticidade": "Média", "horario_chegada": "09:30"},
    {"nome": "Suporte Médico", "prioridade": "Alta", "combustivel": 35.0, "massa": 5.0, "criticidade": "Alta", "horario_chegada": "10:00"}
]

# Lista linear para armazenamento de módulos já estabilizados em solo
modulos_pousados = []

# Estrutura de Pilha (LIFO) para controle de alertas do sistema
pilha_alertas = []


def cadastrar_modulo():
    """Realiza a entrada manual de novos módulos validando tipos e prevenindo duplicatas."""
    print("\n--- CADASTRO DE NOVO MÓDULO (MANUAL) ---")
    nome = input("Digite o nome do módulo: ").strip()

    # Verificação de duplicata usando busca sequencial
    for m in fila_pouso + modulos_pousados:
        if m["nome"].lower() == nome.lower():
            print("[ERRO] Já existe um módulo com esse nome no sistema.")
            return

    while True:
        prioridade = input("Digite a prioridade do módulo (Baixa/Média/Alta): ").strip().capitalize()
        if prioridade in ["Baixa", "Média", "Alta", "Media"]:
            if prioridade == "Media": 
                prioridade = "Média" 
            break
        print("[ERRO] Opção inválida! Digite apenas Baixa, Média ou Alta.")

    while True:
        try:
            combustivel = float(input("Digite o nível de combustível (%): "))
            if 0 <= combustivel <= 100:
                break
            print("[ERRO] O combustível deve ser um valor entre 0 e 100.")
        except ValueError:
            print("[ERRO] Digite apenas números! Não use letras ou símbolos.")

    while True:
        try:
            massa = float(input("Digite a massa do módulo (Toneladas): "))
            if massa > 0:
                break
            print("[ERRO] A massa não pode ser zero ou negativa.")
        except ValueError:
            print("[ERRO] Digite apenas números para a massa.")

    while True:
        criticidade = input("Digite a criticidade da carga (Baixa/Média/Alta): ").strip().capitalize()
        if criticidade in ["Baixa", "Média", "Alta", "Media"]:
            if criticidade == "Media":
                criticidade = "Média"
            break
        print("[ERRO] Opção inválida! Digite apenas Baixa, Média ou Alta.")

    horario_chegada = input("Digite o horário estimado de chegada (ex: 08:30): ").strip()

    # Instanciação do dicionário do novo módulo
    modulo = {
        "nome": nome,
        "prioridade": prioridade,
        "combustivel": combustivel,
        "massa": massa,
        "criticidade": criticidade,
        "horario_chegada": horario_chegada
    }

    fila_pouso.append(modulo) # Enfileiramento padrão (FIFO)
    print("\n Módulo cadastrado com sucesso!")


def visualizar_fila():
    """Exibe os módulos em órbita aguardando processamento."""
    if len(fila_pouso) == 0:
        print("\nA fila de pouso está vazia.")
    else:
        print("\n=== FILA DE POUSO ===")
        for i, modulo in enumerate(fila_pouso):
            print(f"\n{i+1}º da Fila - Nome: {modulo['nome']}")
            print(f"Prioridade: {modulo['prioridade']} | Combustível: {modulo['combustivel']}%")
            print(f"Massa: {modulo['massa']} t | Criticidade: {modulo['criticidade']} | Horário: {modulo['horario_chegada']}")


def processar_pouso():
    """Analisa as condições do primeiro elemento da fila (FIFO) e define a autorização booleana."""
    if len(fila_pouso) == 0:
        print("\nNão há módulos aguardando pouso.")
        return

    # Acessa o primeiro da fila
    modulo = fila_pouso[0]

    print("\n=== ANÁLISE DE POUSO ===")
    print(f"Módulo: {modulo['nome']} (Combustível: {modulo['combustivel']}%)")

    # Coleta de variáveis ambientais
    while True:
        sensores = input("Os sensores estão funcionando? (sim/não): ").strip().lower()
        if sensores in ["sim", "não", "nao"]:
            sensores_ok = (sensores == "sim")
            break
        print("[ERRO] Responda apenas com 'sim' ou 'não'.")

    while True:
        clima = input("Qual o clima? (Ideal/Médio/Ruim): ").strip().capitalize()
        if clima in ["Ideal", "Médio", "Medio", "Ruim"]:
            if clima == "Medio": clima = "Médio"
            clima_favoravel = (clima in ["Ideal", "Médio"])
            break
        print("[ERRO] Responda apenas com 'Ideal', 'Médio' ou 'Ruim'.")

    while True:
        pista = input("A pista está livre? (sim/não): ").strip().lower()
        if pista in ["sim", "não", "nao"]:
            pista_livre = (pista == "sim")
            break
        print("[ERRO] Responda apenas com 'sim' ou 'não'.")
    
    # Aplicação das Regras Lógicas
    combustivel_ok = modulo["combustivel"] > LIMITE_COMBUSTIVEL
    
    pouso_padrao = combustivel_ok and sensores_ok and clima_favoravel and pista_livre
    pouso_emergencia = (not combustivel_ok) and sensores_ok and pista_livre
    
    # Variável unificadora de autorização
    autoriza = pouso_padrao or pouso_emergencia
    
    if autoriza:
        if pouso_padrao:
            modulo["tipo_pouso"] = "Padrão"
            print("\n POUSO PADRÃO CONCLUÍDO")
        elif pouso_emergencia:
            modulo["tipo_pouso"] = "Emergência"
            print("\n POUSO DE EMERGÊNCIA CONCLUÍDO")
            
        # Remove do topo da fila (pop) e adiciona na lista de pousados
        modulos_pousados.append(fila_pouso.pop(0))
        
    else:
        # Lógica de diagnóstico de falhas
        motivos = []
        if not pista_livre: motivos.append("Pista obstruída")
        if not sensores_ok: motivos.append("Falha nos sensores")
        if pista_livre and sensores_ok and combustivel_ok and not clima_favoravel:
            motivos.append("Clima ruim (há combustível de sobra, aguardar melhora)")
            
        texto_motivo = " e ".join(motivos)
        alerta = f"NÃO POUSAR ({modulo['nome']}): {texto_motivo}"
        
        pilha_alertas.append(alerta) # Empilha o alerta (LIFO)
        
        # Move o módulo bloqueado para o final da fila para testar os próximos
        fila_pouso.append(fila_pouso.pop(0))
        
        print(f"\n NÃO POUSAR")
        print(f"Motivo: {texto_motivo}")
        print(f"O módulo {modulo['nome']} foi movido para o FINAL da fila.")


def visualizar_pousados():
    """Percorre a lista linear de módulos estabilizados."""
    if len(modulos_pousados) == 0:
        print("\nNenhum módulo pousou ainda.")
    else:
        print("\n=== MÓDULOS POUSADOS ===")
        for modulo in modulos_pousados:
            print(f"\nNome: {modulo['nome']}")
            print(f"Tipo de Pouso Realizado: {modulo.get('tipo_pouso', 'Desconhecido')}")
            print(f"Prioridade: {modulo['prioridade']} | Combustível Restante: {modulo['combustivel']}%")
            print(f"Massa: {modulo['massa']} t | Criticidade: {modulo['criticidade']} | Horário Original: {modulo['horario_chegada']}")


def visualizar_alertas():
    """Exibe os elementos da pilha respeitando a ordem LIFO (Last In, First Out)."""
    if len(pilha_alertas) == 0:
        print("\nNenhum alerta registrado.")
    else:
        print("\n=== PILHA DE ALERTAS ===")
        # reversed() apenas inverte a visualização sem alterar a estrutura da pilha
        for alerta in reversed(pilha_alertas):
            print(alerta)


def desempilhar_alerta():
    """Remove e resolve o alerta mais recente do topo da pilha."""
    if len(pilha_alertas) == 0:
        print("\nA pilha já está vazia. Nenhum alerta para resolver.")
    else:
        # pop() em uma lista atua perfeitamente como o desempilhamento padrão LIFO
        alerta_resolvido = pilha_alertas.pop()
        print(f"\n Alerta resolvido e retirado da pilha: \n'{alerta_resolvido}'")


def buscar_modulo():
    """Algoritmos de busca para recuperar informações dos módulos."""
    if len(fila_pouso) == 0 and len(modulos_pousados) == 0:
        print("\n Não há módulos cadastrados no sistema.")
        return

    print("\n=== MENU DE BUSCA ===")
    print("1 - Buscar por Nome")
    print("2 - Buscar módulo com MENOR combustível (Busca Sequencial)")
    print("3 - Buscar módulos de MAIOR Prioridade (Alta)")
    print("4 - Buscar por Criticidade da Carga")
    opcao_busca = input("Escolha uma opção: ")

    todos_modulos = fila_pouso + modulos_pousados

    if opcao_busca == "1":
        nome_busca = input("Digite o nome: ").strip().lower()
        for m in todos_modulos:
            if m["nome"].strip().lower() == nome_busca:
                status = "Aguardando Pouso" if m in fila_pouso else "Pousado na Base"
                print(f"\nEncontrado: {m['nome']} | Status: {status} | Combustível: {m['combustivel']}%")
                return
        print("\nMódulo não encontrado.")

    elif opcao_busca == "2":
        # Implementação de Busca Sequencial Clássica
        menor = todos_modulos[0]
        for m in todos_modulos:
            if m["combustivel"] < menor["combustivel"]:
                menor = m
                
        status = "Aguardando Pouso" if menor in fila_pouso else "Pousado na Base"
        print(f"\nMódulo com MENOR combustível: {menor['nome']} com {menor['combustivel']}% (Status: {status})")

    elif opcao_busca == "3":
        print("\n--- Módulos de ALTA Prioridade ---")
        achou = False
        for m in todos_modulos:
            if m["prioridade"] == "Alta":
                status = "Aguardando" if m in fila_pouso else "Pousado"
                print(f"- {m['nome']} ({status})")
                achou = True
        if not achou: print("Nenhum módulo de prioridade alta encontrado.")

    elif opcao_busca == "4":
        crit_busca = input("Qual criticidade deseja buscar (Baixa/Média/Alta)? ").strip().capitalize()
        if crit_busca == "Media": crit_busca = "Média"
        print(f"\n--- Módulos com Carga de Criticidade {crit_busca} ---")
        achou = False
        for m in todos_modulos:
            if m["criticidade"] == crit_busca:
                status = "Aguardando" if m in fila_pouso else "Pousado"
                print(f"- {m['nome']} ({status})")
                achou = True
        if not achou: print("Nenhum módulo com essa criticidade encontrado.")
    else:
        print("Opção de busca inválida.")


def reordenar_fila():
    """Aplica o algoritmo clássico Bubble Sort para reorganizar a fila baseada em múltiplos critérios."""
    n = len(fila_pouso)
    if n < 2:
        print("\nNão há módulos suficientes na fila para reordenar.")
        return

    print("\n=== OPÇÕES DE ORDENAÇÃO (Bubble Sort) ===")
    print("1 - Por Menor Combustível (Situação de Emergência)")
    print("2 - Por Prioridade (Desempate por Horário de Chegada)")
    print("3 - Apenas por Horário de Chegada")
    escolha = input("Escolha como deseja reordenar a fila: ")

    if escolha == "1":
        # Bubble Sort: Menor combustível borbulha para o topo
        for i in range(n):
            for j in range(0, n - i - 1):
                if fila_pouso[j]["combustivel"] > fila_pouso[j + 1]["combustivel"]:
                    # Swap manual
                    fila_pouso[j], fila_pouso[j + 1] = fila_pouso[j + 1], fila_pouso[j]
        print("\n Fila reordenada! Módulos com MENOS combustível estão no topo.")

    elif escolha == "2":
        pesos = {"Alta": 1, "Média": 2, "Baixa": 3}
        # Bubble Sort com múltiplos critérios (Peso > Horário)
        for i in range(n):
            for j in range(0, n - i - 1):
                peso_atual = pesos.get(fila_pouso[j]["prioridade"], 4)
                peso_prox = pesos.get(fila_pouso[j + 1]["prioridade"], 4)
                
                hora_atual = fila_pouso[j]["horario_chegada"]
                hora_prox = fila_pouso[j + 1]["horario_chegada"]

                # Condição de troca: Se o peso numérico for maior OU (se pesos iguais, a hora for mais tarde)
                if peso_atual > peso_prox or (peso_atual == peso_prox and hora_atual > hora_prox):
                    fila_pouso[j], fila_pouso[j + 1] = fila_pouso[j + 1], fila_pouso[j]
        print("\n Fila reordenada! Prioridades respeitadas com horários servindo de desempate.")
        
    elif escolha == "3":
        # Bubble Sort puramente cronológico
        for i in range(n):
            for j in range(0, n - i - 1):
                if fila_pouso[j]["horario_chegada"] > fila_pouso[j + 1]["horario_chegada"]:
                    fila_pouso[j], fila_pouso[j + 1] = fila_pouso[j + 1], fila_pouso[j]
        print("\n Fila reordenada em ordem cronológica de chegada.")

    else:
        print("\nOpção inválida.")


# Loop de controle do software
while True:
    print("\n=== MGPEB - AURORA SIGER ===")
    print("1 - Cadastrar novo módulo (Opcional)")
    print("2 - Visualizar fila de pouso")
    print("3 - Processar próximo pouso")
    print("4 - Visualizar módulos pousados")
    print("5 - Visualizar pilha de alertas")
    print("6 - Buscar módulos")         
    print("7 - Reordenar fila de pouso") 
    print("8 - Resolver último alerta (Desempilhar)")
    print("0 - Sair")

    opcao = input("Escolha uma opção: ")
    
    if opcao == "1": cadastrar_modulo()
    elif opcao == "2": visualizar_fila()
    elif opcao == "3": processar_pouso()
    elif opcao == "4": visualizar_pousados()
    elif opcao == "5": visualizar_alertas()
    elif opcao == "6": buscar_modulo()
    elif opcao == "7": reordenar_fila()
    elif opcao == "8": desempilhar_alerta()
    elif opcao == "0":
        print("Encerrando o sistema MGPEB...")
        break
    else:
        print("Opção inválida!")
