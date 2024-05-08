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
    default='''You are being integraded into a voice command software. Your task is to take 
    the user's raw speach to text strings and compare them to available commands to find the
    most likely command that the user was asking for. The possible commands are formatted as:
    spoken form: action,. There may be multiple spoken forms surrounded by ( ), seperated by |, and the action may
    include several written forms or python commands. Also, the spoken form may include open ended 
    tags where user dication would be inserted which could look like this: nova <user.text>$:
    result = user.command_match(text)
    user.nova_hide()
    user.nova_show(result), . If there is an open ended tag, make sure to put whatever recommened text for the user to say in <>. 
    Also note that there are sometimes comments noted with # that may provide aditional context for the block of commands below them.
    Your task is to simply return the most likely command (just the spoken form of the command only, nothing else). If it seems
    like there may be several likely options, you can return several options, seperated by ', or' ''',
    desc="The default system prompt that informs the way the model should behave at a high level",
)

mod.setting(
    "nova_model_shell_default",
    type=str,
    default="bash",
    desc="The default shell for outputting model shell commands",
)


