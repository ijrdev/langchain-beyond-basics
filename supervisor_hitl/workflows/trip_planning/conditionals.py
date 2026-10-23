from langgraph.graph import StateGraph
from pydantic import BaseModel

class TripState(BaseModel):
    request: dict
    attractions: dict
    lodging: dict
    logistics: dict
    draft: dict
    human_decision: dict
    final_plan: dict


class TripPlanningWorkflow():
    def __init__(self, attractions_agent, lodging_agent, logistics_agent):
        self.attractions_agent = attractions_agent
        self.lodging_agent = lodging_agent
        self.logistics_agent = logistics_agent

        builder = StateGraph(TripState)

        builder.add_node("attractions", self._research_attractions)
        builder.add_node("lodging", self._research_lodging)
        builder.add_node("logistics", self._research_logistics)
        builder.add_node("assemble", self._assemble_plan)
        builder.add_node("human_review", self._human_review)
        builder.add_node("apply_decision", self._apply_decision)

        builder.set_entry_point("attractions")
        builder.add_edge("attractions", "lodging")
        builder.add_edge("lodging", "logistics")
        builder.add_edge("logistics", "assemble")
        builder.add_edge("assemble", "human_review")
        builder.add_edge("human_review", "apply_decision")

        self.graph = builder.compile(checkpointer=...)