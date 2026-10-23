from supervisor_hitl.agents.supervisor_agent import SupervisorAgent
from supervisor_hitl.workflows.trip_planning.states import ExecutionState, OutputState

class TripPlanningNodes():
    def end(self, state: ExecutionState) -> OutputState:
        try:
            return state.messages
        except Exception:
            raise
