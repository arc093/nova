import json
import os
from concurrent.futures import ThreadPoolExecutor
from typing import Any, ClassVar, Literal

import requests
from talon import Module, actions, clip, imgui, registry, settings


from .novaHelpers import generate_payload, notify, remove_wrapper

mod = Module()


def gpt_query(prompt: str, content: str) -> str:
    url = settings.get("user.nova_model_endpoint")

    headers, data = generate_payload(prompt, content)

    response = requests.post(url, headers=headers, data=json.dumps(data))

    match response.status_code:
        case 200:
            #notify("GPT Task Completed")
            return response.json()["choices"][0]["message"]["content"].strip()
        case _:
            notify("GPT Failure: Check the Talon Log")
            raise Exception(response.json())


@mod.action_class
class UserActions:
    def gpt_answer_question(text_to_process: str) -> str:
        """Answer an arbitrary question"""
        prompt = """
        The input is natural language the user has spoken, that should line up to a command for a computer voice control software. Respond with the most likely command. Here is a list of the possible commands: focus code, focus chrome, focus safari, focus notes, help active
        """
        return gpt_query(prompt, text_to_process)
    def nova_show(text: str):
        """Shows nova window"""
        global model_output
        model_output = text
        gui.show()
    def nova_hide():
        """Hides nova window"""

        gui.hide()
    

@imgui.open()
def gui(gui: imgui.GUI):
    gui.text("Try this command: ")
    gui.line()
    gui.text(model_output)

    gui.spacer()
    if gui.button("nova close"):
        actions.user.ai_window_hide()