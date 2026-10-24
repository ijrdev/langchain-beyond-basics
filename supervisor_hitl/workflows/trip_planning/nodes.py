from supervisor_hitl.workflows.trip_planning.states import ExecutionState, OutputState

class TripPlanningNodes():
    def end(self, state: ExecutionState) -> OutputState:
        try:
            return {"messages": state.messages}
        except Exception:
            raise
