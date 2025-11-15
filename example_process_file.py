"""
Example script that processes data from testsata.jason file
using the LangGraph conditional edge implementation.
"""

import json
from langgraph_conditional_edge import run_graph_example


def process_data_file(filename: str = "testsata.jason"):
    """
    Process user data from JSON file using the conditional edge graph.
    
    Args:
        filename: Path to the JSON data file
    """
    print("="*60)
    print("Processing Data File with LangGraph Conditional Edges")
    print("="*60)
    
    try:
        # Read the JSON file
        with open(filename, 'r') as f:
            content = f.read()
        
        # Parse JSON (handling potential format issues)
        # Fix common JSON issues:
        # 1. Remove trailing comma before ]
        # 2. Quote unquoted string values
        content = content.strip()
        
        # Fix unquoted domain values
        import re
        content = re.sub(r':(\w+)([,}])', r':"\1"\2', content)
        
        # Remove trailing comma before closing bracket
        content = re.sub(r',(\s*\])', r'\1', content)
        
        # Parse the data
        users = json.loads(content)
        
        print(f"\nFound {len(users)} users in {filename}\n")
        
        # Process each user through the graph
        results = []
        for user_data in users:
            # Ensure score is an integer
            if 'score' in user_data:
                user_data['score'] = int(user_data['score'])
            result = run_graph_example(user_data)
            results.append(result)
        
        # Summary
        print("\n" + "="*60)
        print("SUMMARY")
        print("="*60)
        high_scores = sum(1 for r in results if r['status'] == 'high_score_processed')
        low_scores = sum(1 for r in results if r['status'] == 'low_score_processed')
        
        print(f"Total users processed: {len(results)}")
        print(f"High score users (score >= 5): {high_scores}")
        print(f"Low score users (score < 5): {low_scores}")
        print("="*60)
        
    except FileNotFoundError:
        print(f"Error: Could not find file '{filename}'")
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")


if __name__ == "__main__":
    process_data_file()
