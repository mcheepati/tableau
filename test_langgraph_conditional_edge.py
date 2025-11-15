"""
Tests for LangGraph Conditional Edge Implementation
"""

import pytest
from langgraph_conditional_edge import (
    GraphState,
    process_user_node,
    validate_score_node,
    high_score_handler,
    low_score_handler,
    score_router,
    create_conditional_graph,
    run_graph_example
)


class TestNodes:
    """Test individual node functions."""
    
    def test_process_user_node(self):
        """Test process_user_node updates status correctly."""
        state: GraphState = {
            "user": "test_user",
            "score": 5,
            "domain": "test",
            "status": "initial"
        }
        result = process_user_node(state)
        assert result["status"] == "processed"
        assert result["user"] == "test_user"
    
    def test_validate_score_node_high_score(self):
        """Test validate_score_node with high score."""
        state: GraphState = {
            "user": "test_user",
            "score": 7,
            "domain": "test",
            "status": "processed"
        }
        result = validate_score_node(state)
        assert result["status"] == "high_score"
    
    def test_validate_score_node_low_score(self):
        """Test validate_score_node with low score."""
        state: GraphState = {
            "user": "test_user",
            "score": 3,
            "domain": "test",
            "status": "processed"
        }
        result = validate_score_node(state)
        assert result["status"] == "low_score"
    
    def test_validate_score_node_boundary(self):
        """Test validate_score_node at boundary (score = 5)."""
        state: GraphState = {
            "user": "test_user",
            "score": 5,
            "domain": "test",
            "status": "processed"
        }
        result = validate_score_node(state)
        assert result["status"] == "high_score"
    
    def test_high_score_handler(self):
        """Test high_score_handler updates status correctly."""
        state: GraphState = {
            "user": "test_user",
            "score": 8,
            "domain": "test",
            "status": "high_score"
        }
        result = high_score_handler(state)
        assert result["status"] == "high_score_processed"
    
    def test_low_score_handler(self):
        """Test low_score_handler updates status correctly."""
        state: GraphState = {
            "user": "test_user",
            "score": 2,
            "domain": "test",
            "status": "low_score"
        }
        result = low_score_handler(state)
        assert result["status"] == "low_score_processed"


class TestConditionalRouter:
    """Test the conditional router function."""
    
    def test_score_router_high_score(self):
        """Test score_router returns high_score path."""
        state: GraphState = {
            "user": "test_user",
            "score": 8,
            "domain": "test",
            "status": "high_score"
        }
        result = score_router(state)
        assert result == "high_score"
    
    def test_score_router_low_score(self):
        """Test score_router returns low_score path."""
        state: GraphState = {
            "user": "test_user",
            "score": 3,
            "domain": "test",
            "status": "low_score"
        }
        result = score_router(state)
        assert result == "low_score"
    
    def test_score_router_no_status(self):
        """Test score_router with missing status defaults to low_score."""
        state: GraphState = {
            "user": "test_user",
            "score": 3,
            "domain": "test",
            "status": "unknown"
        }
        result = score_router(state)
        assert result == "low_score"


class TestGraphExecution:
    """Test the full graph execution."""
    
    def test_graph_creation(self):
        """Test that graph can be created successfully."""
        graph = create_conditional_graph()
        assert graph is not None
    
    def test_run_graph_high_score(self):
        """Test graph execution with high score user."""
        user_data = {"user": "madhu", "score": 6, "domain": "mx"}
        result = run_graph_example(user_data)
        assert result["status"] == "high_score_processed"
        assert result["user"] == "madhu"
        assert result["score"] == 6
        assert result["domain"] == "mx"
    
    def test_run_graph_low_score(self):
        """Test graph execution with low score user."""
        user_data = {"user": "john", "score": 3, "domain": "us"}
        result = run_graph_example(user_data)
        assert result["status"] == "low_score_processed"
        assert result["user"] == "john"
        assert result["score"] == 3
        assert result["domain"] == "us"
    
    def test_run_graph_boundary_score(self):
        """Test graph execution with boundary score (5)."""
        user_data = {"user": "alice", "score": 5, "domain": "uk"}
        result = run_graph_example(user_data)
        assert result["status"] == "high_score_processed"
        assert result["user"] == "alice"
    
    def test_run_graph_default_values(self):
        """Test graph execution with missing data (uses defaults)."""
        user_data = {}
        result = run_graph_example(user_data)
        assert result["status"] == "low_score_processed"
        assert result["user"] == "unknown"
        assert result["score"] == 0
        assert result["domain"] == "unknown"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
