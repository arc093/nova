import base64
import os
import platform
import re
from typing import Optional, Tuple
import csv

from talon import actions, app, clip, settings

from .novaTypes import Data, Headers, Tool


def notify(message: str):
    """Send a notification to the user. Defaults the Andreas' notification system if you have it installed"""
    try:
        actions.user.notify(message)
    except Exception:
        app.notify(message)
    # Log in case notifications are disabled
    print(message)


def get_token() -> str:
    """Get the OpenAI API key from the environment"""
    try:
        return os.environ["OPENAI_API_KEY"]
    except KeyError:
        message = "GPT Failure: env var OPENAI_API_KEY is not set."
        notify(message)
        raise Exception(message)


def generate_payload(
    prompt: str, content: str, tools: Optional[list[Tool]] = None
) -> Tuple[Headers, Data]:
    """Generate the headers and data for the OpenAI API GPT request.
    Does not return the URL given the fact not all openai-compatible endpoints support new features like tools
    """
    #notify("GPT Task Started")

    TOKEN = get_token()

    language = actions.code.language()
    additional_context = (
        f"\nThe user is currently in a code editor for {language}."
        if language != ""
        else ""
    )

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {TOKEN}",
    }

    data = {
        "messages": [
            {
                "role": "system",
                "content": settings.get("user.nova_model_system_prompt")
                + additional_context,
            },
            {"role": "user", "content": f"{prompt}:\n{content}"},
        ],
        "max_tokens": 2024,
        "temperature": settings.get("user.nova_model_temperature"),
        "n": 1,
        "stop": None,
        "model": settings.get("user.nova_openai_model"),
    }

    if tools is not None:
        data["tools"] = tools

    return headers, data


def remove_wrapper(text: str):
    """Remove the string wrapper from the str representation of a command"""
    # different command wrapper for Linux.
    if platform.system() == "Linux":
        regex = r"^.*?'(.*?)'.*?$"
    else:
        # TODO condense these regexes. Hard to test between platforms
        # since the wrapper is slightly different
        regex = r'[^"]+"([^"]+)"'
    match = re.search(regex, text)
    return match.group(1) if match else text

def log_to_csv(textToProcess: str, response: str):
    csv_file_path = "api_requests_log.csv"
    is_new_file = not os.path.exists(csv_file_path)
    with open(csv_file_path, mode='a', newline='') as file:
        writer = csv.writer(file)
        if is_new_file:
            writer.writerow(["User Text", "GPT Response"])
        writer.writerow([textToProcess, response])

log_to_csv('hi','123')
notify(os.getcwd())