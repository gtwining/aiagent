import os
import sys
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt
from call_function import available_functions, call_function

# Load environment variables
load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
if api_key is None:
    raise RuntimeError("API Key Not Found")

model_name = "gemini-2.0-flash"

# Setup CLI Arguments
parser = argparse.ArgumentParser(description="Chatbot")
parser.add_argument("user_prompt", type=str, help="User prompt")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()

# Initialize Client
client = genai.Client(api_key=api_key)

# Initialize Conversation History
messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

if args.verbose:
    print(f"Starting agent loop for prompt: {args.user_prompt}")

# --- THE AGENT LOOP ---
MAX_ITERATIONS = 20

for i in range(MAX_ITERATIONS):
    # 1. Call the model
    response = client.models.generate_content(
        model=model_name,
        contents=messages,
        config=types.GenerateContentConfig(
            system_instruction=system_prompt,
            tools=[available_functions]
        ),
    )

    if response.usage_metadata is None:
        raise RuntimeError("API request failed: usage_metadata is missing.")

    if args.verbose:
        print(f"\n--- Iteration {i+1} ---")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

    # 2. Update History: Add the model's response (thoughts/tool calls)
    # The model needs to see what it just said/asked for in the next turn
    if response.candidates:
        for candidate in response.candidates:
            messages.append(candidate.content)

    # 3. Handle Function Calls (The "Act" Phase)
    if response.function_calls:
        function_results_parts = []
        
        # Execute each function requested by the model
        for function_call in response.function_calls:
            # Run the tool
            call_result = call_function(function_call, verbose=args.verbose)
            
            # Validation (as implemented previously)
            if not call_result.parts:
                raise RuntimeError("Error: Function call result contains no parts.")
            
            # Collect the result part
            function_results_parts.append(call_result.parts[0])

            # Optional: Verbose logging of the result content
            if args.verbose:
                f_response = call_result.parts[0].function_response
                print(f"-> Result: {f_response.response}")

        # 4. Update History: Add tool results
        # We package all tool results into a single "user" message for the model to observe
        messages.append(types.Content(role="user", parts=function_results_parts))
        
        # Continue to the next iteration so the model can read these results
        continue

    # 5. Handle Text Response (The "Final Answer" Phase)
    # If the model didn't ask for a tool, it's talking to the user.
    elif response.text:
        print(f"Response: \n{response.text}")
        sys.exit(0) # Success! Exit the program.

    else:
        # Edge case: No text and no function calls
        print("Response: [No content or function calls returned]")
        sys.exit(1)

# If we fall out of the loop, we ran out of turns
print(f"Error: Max iterations ({MAX_ITERATIONS}) reached without a final response.")
sys.exit(1)