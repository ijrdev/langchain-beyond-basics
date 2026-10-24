from langgraph.graph import StateGraph

from supervisor_hitl.agents.supervisor_agent import SupervisorAgent
from supervisor_hitl.workflows.trip_planning.nodes import TripPlanningNodes
from supervisor_hitl.workflows.trip_planning.states import InputState, ExecutionState, OutputState

class TripPlanningWorkflow():
    def __init__(self):
        self.builder: StateGraph = StateGraph(ExecutionState, input_schema=InputState, output_schema=OutputState)
        self.trip_planning_nodes: TripPlanningNodes = TripPlanningNodes()
        self.supervisor_agent: SupervisorAgent = SupervisorAgent()
        
    def build(self):
        try:
            self.builder.set_entry_point("agent")
            self.builder.set_finish_point("end")
            
            self.builder.add_node("agent", self.supervisor_agent.agent)
            self.builder.add_node("end", self.trip_planning_nodes.end)
            
            self.builder.add_edge("agent", "end")

            return self.builder.compile()
        except Exception:
            raise
            