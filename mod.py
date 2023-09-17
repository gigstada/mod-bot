#!/usr/bin/env python3

# Shiver me timbers, here be module imports from the standard library ye scurvy dog
import os
import sys
import glob
import argparse
import shutil

# Arr, haul in these third-party modules, ye scallywags
import openai
import yaml
from fn_loop import run_conversation
from gpt_functions import get_gpt_functions 
import json_file_serializer
import simple_file_serializer

dir_path = os.path.dirname(os.path.realpath(__file__))

# Get the path components of the current file
current_file_path = os.path.realpath(__file__)
current_directory = os.path.dirname(current_file_path)
python_server_path = os.path.join(current_directory, "../python-server")
# Add the python-server directory to the system path
sys.path.append(python_server_path)

# Hoist the OpenAI API key from the environment variable, ye mateys
openai.api_key = os.getenv('OPENAI_API_KEY')

# Batten down the hatches and prepare ye dictionary, mapping shortcut strings to the full model name
MODEL_MAP = {
    "4": "gpt-4",
    "3": "gpt-3.5-turbo",
    "3l": "gpt-3.5-turbo-16k",
}

# Here be a function to get the model name based on the shortcut, savvy?
def get_model_name_from_shortcut(shortcut):
    model = MODEL_MAP.get(shortcut)
    print(f'Using AI model: {model}')
    return model



# Avast ye! Here be the main function
if __name__ == "__main__":
    # Parse the arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", help="Path to the yaml config file.", default=None)
    parser.add_argument("--gen-config", help="Generate a config file in the current working directory.", nargs='?', const='config.tmp.yaml')
    args = parser.parse_args()

    # Check if --config or --gen-config arg is supplied
    if not any([args.config, args.gen_config]):
        raise ValueError('At least one of the arguments --config or --gen-config must be provided.')
    elif args.gen_config:
        shutil.copyfile(os.path.join(dir_path, 'config_sample.yaml'), args.gen_config)
        print(f"Config file copied to {args.gen_config}")
        exit(0)

    # Load the configuration data from the file specified by the --config argument
    with open(args.config, 'r') as config_file:
        config = yaml.safe_load(config_file)

    # Check if config 'dumb' is True or False
    dumb = config.get('dumb', False)
    get_file_contents_string = simple_file_serializer.get_file_contents_string if dumb else json_file_serializer.get_file_contents_string

    # Use config file's directory as current working directory, if specified in the config
    if config.get('use_config_for_cwd', False):
        os.chdir(os.path.dirname(os.path.realpath(args.config)))

    # Get the instructions, source paths and model from the config
    instructions = config.get('instructions')
    src_paths = config.get('src_paths', [])
    if isinstance(src_paths, str):
        raise ValueError("src_paths should be an array, not a string.")
    glob_string = config.get('glob', "")
    glob_exclude = config.get('glob_exclude', "")
    log_perf = config.get('log_perf', False)
    if glob_string:
        glob_paths = glob.glob(glob_string)
        if glob_exclude:
            glob_exclude_paths = glob.glob(glob_exclude)
            glob_paths = [path for path in glob_paths if path not in glob_exclude_paths]
        src_paths.extend(glob_paths)
    model_shortcut = str(config.get('model', '4'))
    model_name = get_model_name_from_shortcut(model_shortcut)

    # Get the file contents
    if isinstance(src_paths, list) and len(src_paths) > 0:
        file_contents = get_file_contents_string(src_paths)
    else:
        file_contents = []

    # Load the system prompt from the file
    with open(os.path.join(dir_path, 'system_prompt.md'), 'r') as file:
        system_prompt = file.read()

    user_message = instructions + "\n Here are the file contents you can use:\n" + file_contents

    gpt_functions = get_gpt_functions() if not dumb else None

    last_message = run_conversation(system_message=system_prompt, user_message=user_message, gpt_functions=gpt_functions, model=model_name)
    print(f'Conversation has ended. Final message from the assistant:\n\n{last_message}')