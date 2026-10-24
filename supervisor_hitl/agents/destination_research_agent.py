import os

from deepagents.middleware.subagents import CompiledSubAgent
from langchain.agents import create_agent
from langgraph.graph.state import CompiledStateGraph
from langchain.chat_models import init_chat_model

class DestinationResearchAgent():
    def __init__(self):
        self.name: str = "destination_research_agent"
        self.description: str = "Pesquisa o destino em fontes oficiais e retorna achados relevantes com URLs, separando fatos confirmados de informações pendentes."

        self.agent: CompiledStateGraph = create_agent(
            name=self.name,
            model=init_chat_model(
                model= f"{os.getenv('PROVIDER')}:{os.getenv('MODEL')}",
                api_key=os.getenv("API_KEY"),
                reasoning_effort=os.getenv("REASONING_EFFORT"),
            ),
            system_prompt="""
                Você é um agente de pesquisa de destinos para um planejador de viagens.

                Pesquise informações úteis sobre o destino solicitado, priorizando fontes oficiais:
                sites de turismo, atrações, museus, parques, órgãos públicos e operadores responsáveis.

                Investigue apenas o que for relevante para o pedido:
                - atrações e experiências;
                - localização e informações práticas;
                - sazonalidade ou restrições relevantes, quando houver fonte confiável;
                - links oficiais para consulta.

                Regras:
                - Use as ferramentas de pesquisa disponíveis; não responda como se tivesse pesquisado
                quando não tiver consultado fontes.
                - Para cada informação factual, inclua a URL da fonte.
                - Separe fatos encontrados de sugestões.
                - Não invente horários, preços, disponibilidade, condições de entrada ou segurança.
                - Se não encontrar uma informação, marque como "não confirmado".
                - Não monte o roteiro completo nem faça reservas.

                Retorne:
                - destino pesquisado;
                - achados, cada um com descrição e URL da fonte;
                - informações não encontradas ou não confirmadas;
                - observações úteis para o agente que montará o roteiro.
            """,
        )

    def as_subagent(self) -> CompiledSubAgent:
        try:
            return CompiledSubAgent(
                name = self.name,
                description = self.description,
                runnable = self.agent,
                mode = "isolated"
            )
        except Exception:
            raise
