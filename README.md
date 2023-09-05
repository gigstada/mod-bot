# Mod Bot AI
An AI file updater.

Note: This project is for research and messing around only. The author is not responsible for collossal messes you make when using this script. Use at your own risk.

## Overview
This project uses OpenAI's GPT 3/4 API for suggesting updates to files or creating new ones. The AI can read files or parts of files you share with it and can change those files or create new ones.

## Installation

1. Clone the repository to your local machine.
1. Set the `OPENAI_API_KEY` environment variable
   This can be done by adding the following line to your `.bashrc` or `.zshrc` file:

    ```
    export OPENAI_API_KEY=your-api-key
    ```

    Replace `your-api-key` with the actual OpenAI API key you've set up on your [OpenAI account page](https://platform.openai.com/account/api-keys).
1. Run `pip install -r requirements.txt` in the cloned folder to install the required python packages.
1. Make the script available globally on your machine by adding it to your system's PATH. You can do so my creating a symbolic link to the `mod.py` script in a directory that is included in your system's PATH.

    Example for Unix-like systems:

    ```
    ln -s /path/to/mod.py /usr/local/bin/mod
    ```

    Replace `/path/to/mod.py` with the absolute path to the `mod.py` script. Then, you can run the program from anywhere by just typing `mod`.

## Configuration
The script requires a YAML configuration file which you can provide via the `--config` argument. The AI uses this configuration file to know which files to modify and what changes to make. A sample configuration is available in 'config_sample.yaml'.

## Usage

After installing and making the command available globally using the instructions above, your workflow will look something like this:

1. `cd` into the directory where you want to make changes.
1. Make sure you've committed all your current changes to git or other VCS so you can easily see what changes the AI makes when you run the script.
1. Run `mod --gen-config` to create a sample config file in the current directory. 
1. Edit the generated 'config.tmp.yaml' config file to describe your desired changes.
1. Run `mod --config config.tmp.yaml` to make the changes.
1. Inspect and commit or revert the changes using your dev tools of choice.


## Examples
See the examples folder for some very basic examples of how this tool works. You can run all the examples to see the changes they produce by running `./run_examples.sh` from the root of the project.

## Tips
- The AI can't read your mind and is also sometimes dumb, so be very specific about what you want.
- Make changes incrementally to increase the chances of the AI understanding what you want. 
  For example, if you want to convert a JS file to Python and then use it in another Python file, do it in two runs of the script. The first run would convert the JS file to Python and the second run would import the new Python file into your other Python file and use it in an existing function.
- Use the Python slice notation on your src_paths in the config file to prevent the AI from reading the entire file. See the comments in the generated config file to see how to express this. Note that the cost of using the GPT-4 API can add up quickly this helps limit the amount of text we're sending to the AI API.

## GPT-3 vs GPT-4
The script can use either GPT-3 or GPT-4. GPT-4 is much more powerful and can do more complex tasks, but it's also much more expensive. You can choose which version to use in the config file. If you don't specify a version, the script will use GPT-4 by default.
