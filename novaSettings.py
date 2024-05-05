from typing import Literal

from talon import Context, Module

mod = Module()
ctx = Context()


mod.setting(
    "nova_openai_model", type=Literal["gpt-3.5-turbo", "gpt-4"], default="gpt-3.5-turbo"
)

mod.setting(
    "nova_model_temperature",
    type=float,
    default=0.6,
    desc="The temperature of the model. Higher values make the model more creative.",
)

mod.setting(
    "nova_model_endpoint",
    type=str,
    default="https://api.openai.com/v1/chat/completions",
    desc="The endpoint to send the model requests to",
)

mod.setting(
    "nova_model_system_prompt",
    type=str,
    default="You are an assistant helping an office worker to be more productive. Output just the response to the request and no additional content. Do not generate any markdown formatting such as backticks for programming languages unless it is explicitly requested.",
    desc="The default system prompt that informs the way the model should behave at a high level",
)

mod.setting(
    "nova_model_shell_default",
    type=str,
    default="bash",
    desc="The default shell for outputting model shell commands",
)


