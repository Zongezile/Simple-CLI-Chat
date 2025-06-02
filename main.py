from openai import OpenAI
from dotenv import load_dotenv
import json

load_dotenv(dotenv_path=".....")

client = OpenAI()

def end_interaction():
    return

functions_list=[
    {
        "type": "function",
        "function": {
            "name": "end_interaction",
            "description": "Ends the current conversation with the user",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    }
]

function_implementations = {
    "end_interaction": end_interaction
}

def get_chat_completion(messages, tools=None, tool_choice="auto"):
    return client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        tools=tools,
        tool_choice=tool_choice
    )

def calculate_token_costs():
    prompt_tokens = response.usage.prompt_tokens
    completion_tokens = response.usage.completion_tokens

    COST_PER_1K_PROMPT = 0.005
    COST_PER_1K_COMPLETION = 0.015

    interaction_cost = (prompt_tokens * COST_PER_1K_PROMPT + completion_tokens * COST_PER_1K_COMPLETION) / 1000

    print(f"Cost: ${interaction_cost:.8f}")

while True:
    quest = input('Enter a message: ')
    print(f"You: {quest}")

    messages = [
        {"role": "system", "content": "You are a helpful assistant for a simple CLI chat. "
                                      "Only respond with text messages. Get creative with the answers!"},
        {"role": "user", "content": quest}
    ]

    response = get_chat_completion(messages, tools=functions_list)
    reply = response.choices[0].message.content

    if reply is None:
        tool_calls = response.choices[0].message.tool_calls
        for tool_call in tool_calls:
            function_id = tool_call.id
            function_name = tool_call.function.name
            function_args = json.loads(tool_call.function.arguments)
            function_to_call = function_implementations.get(function_name)
            if function_to_call:
                function_to_call(**function_args)

        print(f"{function_id}\nAssistant: {reply}")
        calculate_token_costs()
        break
    else:
        print(f"Assistant: {reply}")
        calculate_token_costs()
