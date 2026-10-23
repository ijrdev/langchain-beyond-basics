from langgraph.graph.state import CompiledStateGraph

from supervisor_hitl.workflows.trip_planning.graphs import TripPlanningWorkflow

trip_planning_workflow: TripPlanningWorkflow = TripPlanningWorkflow()

compiled_state_graph: CompiledStateGraph = trip_planning_workflow.build()