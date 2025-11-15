# LangGraph Conditional Edge Implementation

This project demonstrates the implementation of conditional edges in LangGraph, a framework for building stateful, multi-actor applications with language models.

## Overview

Conditional edges in LangGraph allow you to create dynamic routing in state graphs based on the current state and custom logic. This is useful for building complex workflows where the next step depends on the results of previous operations.

## Features

- **Conditional Routing**: Routes graph execution to different nodes based on state conditions
- **State Management**: Manages graph state using TypedDict for type safety
- **Modular Design**: Separate nodes for different processing stages
- **Comprehensive Tests**: Full test coverage for all components

## Project Structure

```
tableau/
├── langgraph_conditional_edge.py    # Main implementation
├── test_langgraph_conditional_edge.py  # Test suite
├── requirements.txt                 # Python dependencies
├── testsata.jason                   # Sample data file
└── README.md                        # This file
```

## Installation

1. Install Python 3.8 or higher
2. Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

### Running the Example

```bash
python langgraph_conditional_edge.py
```

This will demonstrate the conditional edge functionality with sample user data.

### Import in Your Code

```python
from langgraph_conditional_edge import create_conditional_graph, run_graph_example

# Run with custom user data
user_data = {"user": "alice", "score": 8, "domain": "us"}
result = run_graph_example(user_data)
print(f"Final status: {result['status']}")
```

## How It Works

### Graph Structure

The graph consists of the following nodes:

1. **process_user**: Initial processing of user data
2. **validate_score**: Validates the user's score
3. **high_score**: Handles users with scores >= 5
4. **low_score**: Handles users with scores < 5

### Conditional Edge Logic

The key feature is the `add_conditional_edges()` method:

```python
workflow.add_conditional_edges(
    "validate_score",     # Source node
    score_router,         # Router function
    {
        "high_score": "high_score",    # Mapping of router output to target nodes
        "low_score": "low_score"
    }
)
```

The `score_router()` function examines the state and returns either "high_score" or "low_score", which determines which node executes next.

### State Flow

```
START
  ↓
process_user
  ↓
validate_score
  ↓
score_router (conditional)
  ├─→ high_score (if score >= 5)
  └─→ low_score (if score < 5)
  ↓
END
```

## Running Tests

Run the test suite with pytest:

```bash
pytest test_langgraph_conditional_edge.py -v
```

Or run all tests:

```bash
pytest -v
```

## Test Coverage

The test suite includes:

- Unit tests for individual node functions
- Tests for the conditional router logic
- Integration tests for full graph execution
- Edge case and boundary testing

## Key Concepts

### GraphState

A TypedDict that defines the state structure:

```python
class GraphState(TypedDict):
    user: str
    score: int
    domain: str
    status: str
```

### Node Functions

Each node is a function that takes and returns a `GraphState`:

```python
def node_function(state: GraphState) -> GraphState:
    # Process state
    state["status"] = "updated"
    return state
```

### Router Function

The router function determines the next node based on state:

```python
def score_router(state: GraphState) -> Literal["high_score", "low_score"]:
    if state.get("status") == "high_score":
        return "high_score"
    else:
        return "low_score"
```

## Use Cases

This pattern is useful for:

- User workflow routing based on attributes
- Decision trees in automated processes
- Multi-stage validation with different outcomes
- Dynamic content generation pipelines
- Approval workflows with conditional logic

## Dependencies

- `langgraph`: Core LangGraph library
- `langchain`: LangChain framework
- `langchain-core`: Core LangChain components
- `typing-extensions`: Extended typing support

## Contributing

Feel free to submit issues or pull requests to improve this implementation.

## License

This project is provided as-is for educational and demonstration purposes.
