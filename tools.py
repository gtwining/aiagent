# In main.py
from tools import get_files_info_tool

# Register the tool
config = types.GenerateContentConfig(
    system_instruction=system_prompt,
    tools=[types.Tool(function_declarations=[get_files_info_tool])]
)
