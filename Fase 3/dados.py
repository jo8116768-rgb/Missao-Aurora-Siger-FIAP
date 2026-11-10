# ==============================================================================
# 1. ESTRUTURA PRINCIPAL DA COLÔNIA
# Dicionário aninhado que organiza os módulos em categorias (energético, suporte, etc).
# Cada componente possui chaves de status ('ativo'/'inativo'), potência e prioridade.
# ==============================================================================
colonia = {
    # Módulo responsável pela produção de eletricidade da colônia
    "energético": {
        "solar": {
            "status": "ativo",
            "capacidade_kw": 50.0,  # Produção máxima em kW dos painéis solares
            "essencial": True       # Fonte primária, não pode ser desligada
        },
        "eolico": {
            "status": "ativo",
            "capacidade_kw": 30.0,  # Produção máxima em kW das turbinas eólicas
            "essencial": True       # Fonte secundária
        }
    },
    # Módulo de sistemas vitais para os tripulantes
    "suporte_vida": {
        "oxigenio": {
            "status": "ativo",
            "consumo_kw": 20.0,     # Gasto energético constante de O2
            "essencial": True       # Crítico: NUNCA deve ser desligado pelas regras
        },
        "aquecimento": {
            "status": "ativo",
            "consumo_kw": 15.0,     # Controle térmico dos habitats
            "essencial": True       # Crítico para sobrevivência
        }
    },
    # Módulos secundários que podem sofrer corte de energia em emergências
    "modulos_auxiliares": {
        "iluminacao_externa": {
            "status": "ativo",
            "consumo_kw": 5.0,      # Iluminação dos pátios de pouso/carga
            "essencial": False      # Não essencial: pode ser desligado se faltar energia
        },
        "laboratorio_pesquisa": {
            "status": "ativo",
            "consumo_kw": 12.0,     # Experimentos e processamento de dados
            "essencial": False      # Não essencial: desativado em racionamentos
        }
    }
}

# ==============================================================================
# 2. HISTÓRICOS PARA O MÓDULO DE PREVISÃO
# Listas pareadas que correlacionam a velocidade do vento com a energia gerada.
# ==============================================================================

historico_vento = [5.0, 7.5, 9.0, 11.0, 12.5, 14.0]      # Velocidade medida em m/s
historico_energia = [12.0, 18.0, 22.0, 27.0, 31.0, 35.0]  # Geração correspondente em kW

# ==============================================================================
# 3. FUNÇÕES DE CÁLCULO ENERGÉTICO
# ==============================================================================

def geracao_total(colonia_dados: dict) -> float:
    """
    Soma a capacidade em kW de todos os geradores ativos no módulo 'energético'.
    Retorna o valor total de energia disponível.
    """
    total = 0.0
    # Acessa com segurança o módulo energético do dicionário
    modulo_energetico = colonia_dados.get("energético", {})
    
    # Percorre cada gerador (ex: 'solar', 'eolico') e suas propriedades
    for gerador, info in modulo_energetico.items():
        # Só soma a capacidade se o gerador estiver ligado/ativo
        if info.get("status") == "ativo":
            total += info.get("capacidade_kw", 0.0)
            
    return total


def consumo_total(colonia_dados: dict) -> float:
    """
    Soma o consumo em kW de todos os componentes ativos que consomem energia
    (ignorando os geradores do módulo 'energético').
    """
    total = 0.0
    
    # Percorre os módulos da colônia (suporte_vida, modulos_auxiliares, etc.)
    for modulo, componentes in colonia_dados.items():
        # Pula o setor de geração, pois ele produz energia em vez de consumir
        if modulo == "energético":
            continue
        
        # Percorre cada equipamento dentro do módulo atual
        for comp, info in componentes.items():
            # Só contabiliza o gasto se o equipamento estiver 'ativo'
            if info.get("status") == "ativo":
                total += info.get("consumo_kw", 0.0)
                
    return total


# 4. BLOCO DE VERIFICAÇÃO LOCAL
# Este bloco só executa se você rodar 'python dados.py' diretamente no terminal.
# Quando este arquivo for importado no main.py esse bloco é ignorado.

if __name__ == "__main__":
    print("=== TESTE DE VALIDAÇÃO (DADOS.PY) ===")
    g_total = geracao_total(colonia)
    c_total = consumo_total(colonia)
    
    print(f"Geração total ativa : {g_total} kW")
    print(f"Consumo total ativo  : {c_total} kW")
    print(f"Balanço (Sobra/Falta): {g_total - c_total:.2f} kW")