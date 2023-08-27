"""Open AI Chat"""
import openai
from openai.error import RateLimitError
from exceptions import OpenAIError, NoResponseError
from util.get_config import Config


class OpenAIChat:
    """Open AI Chat class"""

    def __init__(self, model):
        """Init chat"""
        self._messages = [
            {"role": "system", "content": "Welcome to Post IT AI."},
        ]
        self.chat_responses = []
        self.errors = []
        self.model = model
        self.cfg = Config().get_config()
        openai.api_key = self.cfg.get("OPENAI_API_KEY")
        try:
            chat_response = openai.ChatCompletion.create(
                model=model,
                messages=self._messages,
            )
            self.chat_responses.append(chat_response)
        except RateLimitError:
            self.errors.append(OpenAIError)

    @staticmethod
    def create_message_payload(messages, system=False):
        """Create message payload"""
        role = "system" if system else "user"
        if type(messages) == list:
            payload_message = [
                {"role": role, "content": message} for message in messages
            ]
        else:
            payload_message = [{"role": role, "content": messages}]
        return payload_message

    def chat(self, messages):
        """Chat method"""
        formatted_messages = self.create_message_payload(messages)
        chat_response = openai.ChatCompletion.create(
            model=self.model, messages=formatted_messages
        )
        self.chat_responses.append(chat_response)
        return self.get_choices_from_response(chat_response)

    def get_latest_response(self) -> object | None:
        """Get the latest response"""
        latest_response = None
        if len(self.chat_responses) > 0:
            latest_response = self.chat_responses[-1]
        return latest_response

    def get_responses(self):
        """Get responses for the class"""
        return self.chat_responses

    def get_choices_from_response(self, chat_gpt_response):
        """Get choice content"""
        if not chat_gpt_response:
            raise NoResponseError
        choices = chat_gpt_response.get("choices")
        chat_gpt_messages = []
        for choice in choices:
            message = choice.message.content
            role = choice.message.role
            self._messages.append(
                {
                    "role": role,
                    "content": message,
                }
            )
            chat_gpt_messages.append(message)
        return chat_gpt_messages


if __name__ == "__main__":
    cfg = Config().get_config()
    chat_model = cfg.get("CHAT_GPT_MODEL")
    open_ai_chat = OpenAIChat(chat_model)
    responses = open_ai_chat.chat("Tell me a fairy tale story for my kid")
    print(responses)
