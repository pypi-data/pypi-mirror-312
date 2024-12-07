from toolmate import config

import os, shutil, argparse, pyperclip, subprocess
from pathlib import Path

from toolmate import updateApp, configFile, getOllamaServerClient
from toolmate.utils.assistant import ToolMate
from prompt_toolkit.shortcuts import set_title, clear_title


def main():
    print(f"Setting up {config.toolMateAIName} ...")

    # Create the parser
    parser = argparse.ArgumentParser(description="ToolMate AI cli options")
    # Add arguments
    parser.add_argument('-a', '--apikeys', action='store', dest='apikeys', help="configure API keys; true / false")
    parser.add_argument('-b', '--model', action='store', dest='model', help="configure AI backend and models; true / false")
    # Parse arguments
    args = parser.parse_args()
    # Check what kind of arguments were provided and perform actions accordingly

    # update to the latest version
    config.tempInterface = ""
    config.custom_config = ""
    config.initialCompletionCheck = False
    config.includeIpInDeviceInfoTemp = False
    config.defaultEntry = ""
    config.accept_default = False

    # set window title
    set_title(config.toolMateAIName)

    config.toolmate = ToolMate()

    if args.apikeys and args.apikeys.lower() == "true":
        config.toolmate.changeAPIkeys()
    if args.model and args.model.lower() == "true":
        config.toolmate.setLlmModel()

    # unload llama.cpp model to free VRAM
    try:
        config.llamacppToolModel.close()
        print("Llama.cpp model unloaded!")
    except:
        pass
    if config.llmInterface == "ollama":
        getOllamaServerClient().generate(model=config.ollamaToolModel, keep_alive=0, stream=False,)
        print(f"Ollama model '{config.ollamaToolModel}' unloaded!")
    if hasattr(config, "llamacppToolModel"):
        del config.llamacppToolModel

    # delete temporary content
    try:
        tempFolder = os.path.join(config.toolMateAIFolder, "temp")
        shutil.rmtree(tempFolder, ignore_errors=True)
        Path(tempFolder).mkdir(parents=True, exist_ok=True)
    except:
        pass

    # backup configurations
    config.saveConfig()
    if os.path.isdir(config.localStorage):
        shutil.copy(configFile, os.path.join(config.localStorage, "config_lite_backup.py" if config.isLite else "config_backup.py"))

    # clear title
    clear_title()

if __name__ == "__main__":
    main()
