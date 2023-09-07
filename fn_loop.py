import openai
import json

def save_messages(filename, content):
    filename += '.md'
    content = json.loads(json.dumps(content))
    with open(filename,'w') as file:
        for message in content:
            role = message.get('role', '')
            content = message.get('content', '')
            function_call = message.get('function_call', '')
            file.write('# ' + role.capitalize() + '\n```\nContent: ' +  str(content))
            if function_call:
                arguments = json.loads(function_call['arguments'])
                function_call['arguments'] = arguments
                file.write('\nFunction call: ' + json.dumps(function_call, indent=4))
            file.write('\n```\n')

def run_conversation(system_message, user_message, gpt_functions, model="gpt-4"):
    messages = [{"role": "system", "content": system_message}, {"role": "user", "content": user_message}]
    functions = [func['def'] for func in gpt_functions.values()]
    available_functions = {func_name: func['fn'] for func_name, func in gpt_functions.items()}

    while True:
        print("Starting a new iteration of the loop...")
        response = openai.ChatCompletion.create(
            model=model,
            messages=messages,
            functions=functions,
            function_call="auto",
        )
        print("Response received from OpenAI API.")
        
        response_message = response["choices"][0]["message"]
        
        if response_message.get("function_call"):
            messages.append(response_message)
            save_messages('mod-messages', messages)
            
            if response_message["content"] is not None:
                print('Response from AI:\n' + response_message["content"])
            
            function_name = response_message["function_call"]["name"]
            function_to_call = available_functions[function_name]
            try:
                function_args = json.loads(response_message["function_call"]["arguments"])
            except json.decoder.JSONDecodeError:
                print("JSONDecodeError: Could not decode arguments for function call.")
                print(response_message["function_call"]["arguments"])
            function_response = function_to_call(**function_args)
            
            messages.append(
                {
                    "role": "function",
                    "name": function_name,
                    "content": str(function_response),
                }
            )
            save_messages('mod-messages', messages)
        else:
            messages.append(response_message)
            save_messages('mod-messages', messages)

            last_message = response_message["content"]
            return last_message

if __name__ == "__main__":
    from gpt_functions import get_gpt_functions 
    system_message = "You are a helpful assistant."
    user_message = "Create an md file that tells a 3-sentence story about a cat."
    gpt_functions = get_gpt_functions()

    last_message = run_conversation(system_message=system_message, user_message=user_message, gpt_functions=gpt_functions)
    print(f"Conversation ended. Last message from assistant: {last_message}")
