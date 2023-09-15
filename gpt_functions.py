import os
# Purpose: Functions that can be called by the GPT-3 chatbot

def propose_file_operations(proposed_file_operations):
    result = {
        'status': 'success',
        'message': '',
    }
    for operation in proposed_file_operations:
        operation_type = operation['operation_type']
        src_path = operation['src_path']
        
        if operation_type == 'create-or-replace-file':
            full_contents = operation['full_contents']
            try:
                dir_path = os.path.dirname(src_path)
                if len(dir_path) > 0:
                    os.makedirs(dir_path, exist_ok=True)
                with open(src_path, 'w') as file:
                    file.write(full_contents)
            except PermissionError:
                result['status'] = 'error'
                result['message'] += f"You do not have permission to write to {src_path}.\n"
                continue
        elif operation_type == 'partial-file-replace':
            find = operation['find']
            replace_with = operation['replace_with']
            try:
                with open(src_path, 'r') as file:
                    contents = file.read()
                if find in contents:
                    replaced_contents = contents.replace(find, replace_with)
                    if contents == replaced_contents:
                        result['status'] = 'error'
                        result['message'] += f'The replacement did not produce a change in {src_path}.\n'
                        continue
                    with open(src_path, 'w') as file:
                        file.write(replaced_contents)
            except FileNotFoundError:
                result['status'] = 'error'
                result['message'] += f"File {src_path} not found.\n"
                continue
            except PermissionError:
                result['status'] = 'error'
                result['message'] += f"You do not have permission to read or write to {src_path}.\n"
                continue
    return result

gpt_functions = {
    'propose_file_operations': {
        'fn': propose_file_operations,
        'def': {
            "name": "propose_file_operations",
            "description": "Performs proposed file operations and returns an object containing a status and a possible message string containing any errors.",
            "parameters": {
                "type": "object",
                "properties": {
                    "proposed_file_operations": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "operation_type": { "type": "string" },
                                "src_path": { "type": "string" },
                                "full_contents": { "type": "string" },
                                "find": { "type": "string" },
                                "replace_with": { "type": "string" },
                            },
                        },
                        "description": "An array of objects that specify the file operations to perform. " \
                        "Each object has an operation_type that is either 'create-or-replace-file' or 'partial-file-replace'. " \
                        "If operation_type is 'create-or-replace-file', then the object has src_path and full_contents fields. " \
                        "If operation_type is 'partial-file-replace', then the object has src_path, find, and replace_with fields. " \
                        "This array can contain multiple 'partial-file-replace' operations for the same file if needed."
                    },
                },
                "required": ["proposed_file_operations"],
            },
        },
    },
}

def get_gpt_functions(included_functions=None):
    if included_functions is None:
        return gpt_functions
    else:
        return {fn: gpt_functions[fn] for fn in included_functions if fn in gpt_functions}