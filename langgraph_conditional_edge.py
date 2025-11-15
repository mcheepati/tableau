"""
LangGraph Conditional Edge Implementation

This module demonstrates the use of conditional edges in LangGraph.
Conditional edges allow dynamic routing in a state graph based on the 
current state and custom logic.
"""

from typing import TypedDict, Literal
from langgraph.graph import StateGraph, END


class GraphState(TypedDict):
    """State for the graph with user data."""
    user: str
    score: int
    domain: str
    status: str


def process_user_node(state: GraphState) -> GraphState:
    """
    Process user data node.
    
    Args:
        state: Current graph state
        
    Returns:
        Updated state with processing status
    """
    print(f"Processing user: {state['user']}")
    state["status"] = "processed"
    return state


def validate_score_node(state: GraphState) -> GraphState:
    """
    Validate user score node.
    
    Args:
        state: Current graph state
        
    Returns:
        Updated state with validation status
    """
    print(f"Validating score: {state['score']} for user: {state['user']}")
    if state["score"] >= 5:
        state["status"] = "high_score"
    else:
        state["status"] = "low_score"
    return state


def high_score_handler(state: GraphState) -> GraphState:
    """
    Handler for high score users.
    
    Args:
        state: Current graph state
        
    Returns:
        Updated state with high score handling
    """
    print(f"High score detected for user: {state['user']}")
    state["status"] = "high_score_processed"
    return state


def low_score_handler(state: GraphState) -> GraphState:
    """
    Handler for low score users.
    
    Args:
        state: Current graph state
        
    Returns:
        Updated state with low score handling
    """
    print(f"Low score detected for user: {state['user']}")
    state["status"] = "low_score_processed"
    return state


def score_router(state: GraphState) -> Literal["high_score", "low_score"]:
    """
    Conditional edge router function.
    Routes to different nodes based on score validation status.
    
    Args:
        state: Current graph state
        
    Returns:
        Next node name to route to
    """
    if state.get("status") == "high_score":
        return "high_score"
    else:
        return "low_score"


def create_conditional_graph() -> StateGraph:
    """
    Create a LangGraph with conditional edges.
    
    Returns:
        Compiled state graph with conditional routing
    """
    # Initialize the graph
    workflow = StateGraph(GraphState)
    
    # Add nodes
    workflow.add_node("process_user", process_user_node)
    workflow.add_node("validate_score", validate_score_node)
    workflow.add_node("high_score", high_score_handler)
    workflow.add_node("low_score", low_score_handler)
    
    # Set entry point
    workflow.set_entry_point("process_user")
    
    # Add regular edge
    workflow.add_edge("process_user", "validate_score")
    
    # Add conditional edge - this is the key feature
    workflow.add_conditional_edges(
        "validate_score",
        score_router,
        {
            "high_score": "high_score",
            "low_score": "low_score"
        }
    )
    
    # Add edges to end
    workflow.add_edge("high_score", END)
    workflow.add_edge("low_score", END)
    
    # Compile the graph
    return workflow.compile()


def run_graph_example(user_data: dict) -> GraphState:
    """
    Run the graph with example user data.
    
    Args:
        user_data: Dictionary containing user, score, and domain
        
    Returns:
        Final state after graph execution
    """
    app = create_conditional_graph()
    
    # Create initial state
    initial_state: GraphState = {
        "user": user_data.get("user", "unknown"),
        "score": user_data.get("score", 0),
        "domain": user_data.get("domain", "unknown"),
        "status": "initial"
    }
    
    print(f"\n{'='*50}")
    print(f"Running graph for: {initial_state['user']}")
    print(f"{'='*50}")
    
    # Execute the graph
    result = app.invoke(initial_state)
    
    print(f"\nFinal status: {result['status']}")
    print(f"{'='*50}\n")
    
    return result


if __name__ == "__main__":
    # Example usage with different scores to demonstrate conditional routing
    test_users = [
        {"user": "madhu", "score": 6, "domain": "mx"},
        {"user": "john", "score": 3, "domain": "us"},
        {"user": "alice", "score": 8, "domain": "uk"},
    ]
    
    print("LangGraph Conditional Edge Demo")
    print("================================\n")
    
    for user_data in test_users:
        result = run_graph_example(user_data)
