from enum import Enum
from dataclasses import dataclass
import openai
from typing import Optional, List
import discord
from Ai.AiBase import Message, Prompt, Conversation
from Ai.AiUtils import split_into_shorter_messages, logger
from Ai.AiTrainer import *
import random
api_keys = [] # Use apikey as a list (you add more api key for no limit)



class CompletionResult(Enum):
    OK = 0
    TOO_LONG = 1
    INVALID_REQUEST = 2
    OTHER_ERROR = 3


@dataclass
class CompletionData:
    status: CompletionResult
    reply_text: Optional[str]
    status_text: Optional[str]


async def generate_completion_response(
    messages: List[Message], user: str
) -> CompletionData:
    openai.api_key = random.choice(api_keys)
    SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
    CONFIG: Config = dacite.from_dict(
        Config, yaml.safe_load(open(SCRIPT_DIR + os.sep + os.pardir +"/config.yaml", "r", encoding='utf-8'))
    )

    BOT_NAME = CONFIG.name
    BOT_INSTRUCTIONS = CONFIG.instructions
    EXAMPLE_CONVOS = CONFIG.example_conversations


    try:
        
        prompt = Prompt(
            header=Message(
                "System", f"Instructions for {BOT_NAME}: {BOT_INSTRUCTIONS}"
            ),
            examples=EXAMPLE_CONVOS,
            convo=Conversation(messages + [Message(BOT_NAME)]),
        )
        rendered = prompt.render()
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": rendered}],
        )
        reply = response.choices[0].message.content.strip()

        return CompletionData(
            status=CompletionResult.OK, reply_text=reply, status_text=None
        )
    except openai.error.InvalidRequestError as e:
        if "This model's maximum context length" in e.user_message:
            return CompletionData(
                status=CompletionResult.TOO_LONG, reply_text=None, status_text=str(e)
            )
        else:
            logger.exception(e)
            return CompletionData(
                status=CompletionResult.INVALID_REQUEST,
                reply_text=None,
                status_text=str(e),
            )
    except Exception as e:
        logger.exception(e)
        return CompletionData(
            status=CompletionResult.OTHER_ERROR, reply_text=None, status_text=str(e)
        )


