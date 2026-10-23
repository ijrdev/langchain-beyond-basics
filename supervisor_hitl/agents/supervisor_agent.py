import os

from langgraph.graph.state import StateGraph
from langchain.chat_models import init_chat_model
from langgraph_supervisor import create_supervisor

from supervisor_hitl.agents.destination_research_agent import DestinationResearchAgent
from supervisor_hitl.agents.activity_planner_agent import ActivityPlannerAgent
from supervisor_hitl.agents.budget_agent import BudgetAgent

class SupervisorAgent():
    def __init__(self):
        self.agent: StateGraph = create_supervisor(
            [DestinationResearchAgent().agent, ActivityPlannerAgent().agent, BudgetAgent().agent],
            supervisor_name="supervisor_agent",
            parallel_tool_calls=True,
            output_mode="last_message",
            add_handoff_messages=False,
            add_handoff_back_messages=False,
            model=init_chat_model(
                model= f"{os.getenv('PROVIDER')}:{os.getenv('MODEL')}",
                api_key=os.getenv("API_KEY"),
                reasoning_effort=os.getenv("REASONING_EFFORT"),
            ),
            prompt="""
                Você é o supervisor de um planejador de viagens conversacional.

                Seu trabalho é:
                1. Entender o pedido e o contexto da conversa.
                2. Perguntar apenas informações essenciais que estiverem faltando, como destino,
                período ou duração, cidade de saída, número de viajantes e orçamento.
                3. Quando houver dados suficientes, delegar:
                - pesquisa do destino para DestinationResearchAgent;
                - organização dos dias para ActivityPlannerAgent;
                - estimativa de custos para BudgetAgent.
                4. Consolidar as respostas em um rascunho claro de viagem.

                Regras:
                - Não invente atrações, horários, preços, disponibilidade ou regras de entrada.
                - Diferencie fatos encontrados, estimativas e sugestões.
                - Preserve as preferências e restrições informadas pelo usuário.
                - Se os agentes trouxerem dados conflitantes ou insuficientes, indique isso no rascunho.
                - Não afirme que reservas foram feitas.
                - Não aprove nem rejeite o plano. A decisão será solicitada pelo workflow em uma
                etapa separada de revisão humana.
                - Se receber feedback de edição, ajuste o rascunho e solicite nova revisão humana.

                Apresente o rascunho com:
                - resumo da viagem;
                - roteiro por dia;
                - estimativa de orçamento;
                - premissas e informações ainda não confirmadas;
                - fontes consultadas.
            """,
        )