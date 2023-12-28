'''

'''

import importlib
import os
from typing import Literal
import discord
import discord.ext

CMD_FOLDER_NAME = "commands"

def apply(client:discord.Client):
    for file in os.listdir(os.path.dirname(__file__) + "/" + CMD_FOLDER_NAME):
        if file == "__pycache__":
            continue
        file = file[:-3]
        importlib.import_module('.' + CMD_FOLDER_NAME + '.' + file, package="teinou")