# MGPEB - Módulo de Gerenciamento de Pouso e Estabilização de Base
> **Missão Aurora Siger** | Controle de tráfego orbital, autorização de pouso e gestão energética inteligente em Marte

---

## Documentação Completa

O relatório acadêmico e técnico detalhado do projeto (incluindo modelagem matemática, análise ESG e histórico computacional) pode ser acessado no link abaixo:

**[Acessar Relatório Completo do Projeto](https://1drv.ms/w/c/795ed93c519cc49d/IQBBZ2CzEfzPR6WL85Ynqp-0ATGO4qSNvQN1AeUynNbUmvo?e=ZyNp68)**

---

## Fase 2 — Controle de Tráfego Orbital e Pouso (`Fase_2_Pouso`)

### Visão Geral do Projeto
A base **Aurora Siger** encontra-se em fase inicial de instalação no solo marciano. Com apenas uma área de pouso disponível e cinco módulos em órbita aguardando autorização para descida, o **MGPEB** atua no controle crítico do fluxo operacional, garantindo a integridade dos módulos e a sobrevivência da colônia.

### Módulos em Órbita

| Módulo | Chegada | Massa | Combustível | Criticidade | Prioridade | Função Primária |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| **Energia** | 08:00 | 9 t | 55% | Alta | Alta | Fornecimento elétrico para a infraestrutura |
| **Habitação** | 08:30 | 12 t | 70% | Alta | Alta | Abrigo da tripulação em condições controladas |
| **Comunicações** | 09:00 | 4 t | 25% | Alta | Média | Enlace de contato com a Terra |
| **Estufa** | 09:30 | 8 t | 40% | Média | Baixa | Produção alimentar local |
| **Suporte Médico** | 10:00 | 5 t | 35% | Alta | Alta | Cuidados de saúde da tripulação |

### Estruturas de Dados Utilizadas
* **Fila de Espera Orbital (`QueueFIFO`):** Organiza a fila de espera (`fila_pouso`), assegurando processamento estritamente sequencial.
* **Lista Linear (`List`):** Registra a base permanente de dados dos módulos já estabilizados em solo (`modulos_pousados`).
* **Pilha de Alertas (`StackLIFO`):** Rastreia incidentes e falhas operacionais (`pilha_alertas`), priorizando na interface a notificação mais recente.

### Regras Lógicas de Decisão
O algoritmo avalia quatro variáveis booleanas de telemetria: `Combustivel_OK` (> 30%), `Sensores_OK`, `Clima_Favoravel` e `Pista_Livre`.

1. **Pouso Padrão (Porta AND):**
   `Pouso_Padrao = Combustivel_OK AND Sensores_OK AND Clima_Favoravel AND Pista_Livre`

### Código Fonte (Fase 2)
* O algoritmo completo e implementado está disponível no arquivo: [`Fase_2_Pouso/mgpeb.py`](./Fase_2_Pouso/mgpeb.py)

---

## Fase 3 — Sistema Integrado de Funcionamento Inteligente da Colônia (`Fase 3`)

### Visão Geral
Após a estabilização dos módulos em solo, o sistema integrado da **Fase 3** gerencia de forma inteligente os recursos energéticos da colônia. O sistema organiza os subsistemas de forma hierárquica, prevê a geração de energia eólica com base no clima marciano usando regressão linear, analisa o balanço energético e toma decisões automáticas priorizando o suporte à vida.

### 1. Organização Hierárquica dos Dados (`dados.py`)
Os setores da colônia são armazenados em uma estrutura de dicionário hierárquico (`colonia`), dividindo os módulos entre geração, suporte à vida e sistemas auxiliares:

| Módulo / Setor | Componente | Status Inicial | Potência / Gasto | Carga Essencial? |
| :--- | :--- | :---: | :---: | :---: |
| **Energético** | Solar (Painéis) | Ativo | 50.0 kW (Capacidade) | Sim (`True`) |
| **Energético** | Eólico (Turbinas) | Ativo | 30.0 kW (Capacidade) | Sim (`True`) |
| **Suporte à Vida** | Oxigênio (Gerador O₂) | Ativo | 20.0 kW (Consumo) | Sim (`True`) |
| **Suporte à Vida** | Aquecimento (Térmico) | Ativo | 15.0 kW (Consumo) | Sim (`True`) |
| **Módulos Auxiliares** | Iluminação Externa | Ativo | 5.0 kW (Consumo) | Não (`False`) |
| **Módulos Auxiliares** | Laboratório de Pesquisa | Ativo | 12.0 kW (Consumo) | Não (`False`) |

* **Funções de Mapeamento:**
  * `geracao_total(colonia_dados)`: Filtra o módulo energético e soma a capacidade (kW) das fontes ativas.
  * `consumo_total(colonia_dados)`: Soma o gasto (kW) de todos os componentes ativos de suporte à vida e módulos auxiliares.

### 2. Previsão de Energia Eólica com Regressão Linear (`previsao.py`)
Utiliza as listas históricas de medições para ajustar uma reta pelo método dos mínimos quadrados (`ajustar_reta()`) e estimar a geração futura (`prever()`):
* **`historico_vento` (m/s):** `[5.0, 7.5, 9.0, 11.0, 12.5, 14.0]`
* **`historico_energia` (kW):** `[12.0, 18.0, 22.0, 27.0, 31.0, 35.0]`
* **Equação Ajustada:** `energia = 2.5602 * vento - 1.0090`

### 3. Análise Energética e Regras de Decisão (`analise.py` e `decisoes.py`)
* **Análise (`analisar()`):** Compara a geração total com o consumo e verifica a existência de reservas de bateria:
  * `Consumo > Geração` → Emite alerta de déficit energético (e verifica se a reserva cobre a diferença).
  * `Geração > Consumo` → Sugere armazenar a energia excedente.
* **Tomada de Decisão (`decidir()` e `desligar_nao_essenciais()`):**
  * Se a energia gerada for insuficiente para a demanda, o sistema ativa o modo de economia e **desliga automaticamente os sistemas não essenciais** (Iluminação Externa e Laboratório de Pesquisa), preservando os sistemas críticos de **Suporte à Vida** (Oxigênio e Aquecimento).

---

### Exemplos de Entrada e Saída (Cenários de Teste — `main.py`)

#### Exemplo 1: Previsão de Energia Eólica (Regressão)
* **Entrada:** `vento = 11` (m/s)
* **Saída:** `Previsão de energia eólica ≈ 27.15 kW`

#### Exemplo 2: Cenário 1 — Operação Normal com Excedente
* **Entrada:** `vento = 11 m/s` | Painel Solar `Ativo` (50.0 kW) | Todos os módulos ligados (`Consumo = 52.0 kW`)
* **Processamento:** Geração Total = `50.0 + 27.15 = 77.15 kW`
* **Saída:**
  ```text
  Geração prevista: 77.2 kW | Consumo atual: 52.0 kW
  SUGESTÃO: armazenar energia excedente (25.2 kW disponíveis).
  STATUS: Operação normal mantida. Todos os sistemas ativos.
