from utils.llm import ask_llm
import json

def format_response(query: str, steps: list, results: list) -> str:
    """
    Take raw tool results and turn them into a natural language response.
    This is what the user actually sees.
    """
    
    # Summarize what happened
    results_text = ""
    for i, (step, result) in enumerate(zip(steps, results)):
        results_text += f"Step {i+1} ({step['action']}): {json.dumps(result, default=str)[:300]}\n"
    
    prompt = f"""You are a helpful assistant. A user asked a question and the system executed some actions.
Summarize the results in a clear, friendly way.

User question: "{query}"

Results:
{results_text}

Write a brief, helpful response to the user based on these results. 
Be concise. If there's an error, explain it simply.
Response:"""
    
    return ask_llm(prompt)