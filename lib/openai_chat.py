"""Open AI Chat"""
import openai


class OpenAIChat:
    """Open AI Chat class"""

    def __init__(self, model):
        """Init chat"""
        self.chat_responses = []
        response = self.chat = openai.ChatCompletion.create(
            model=model,
            messages=[
                {"role": "system", "content": "Welcome to Post IT AI."},
            ],
        )
        self.chat_responses.append(response)

    @staticmethod
    def create_message_payload(messages, system=False):
        """Create message payload"""
        role = "system" if system else "user"
        payload_message = [
            {
                "role": role,
                "content": message
            } for message in messages
        ]
        return payload_message

    def chat(self, messages):
        """Chat class"""
        formatted_messages = self.create_message_payload(messages)
        chat_response = self.chat.append(formatted_messages)
        self.chat_responses.append(chat_response)
        return chat_response

    def get_latest_response(self) -> object | None:
        """Get the latest response"""
        latest_response = None
        if len(self.chat_responses) > 0:
            latest_response = self.chat_responses[-1]
        return latest_response

    def get_responses(self):
        """Get responses for the class"""
        return self.chat_responses


if __name__ == "__main__":
    from util.get_config import Config
    cfg = Config().get_config()
    chat_model = cfg.get("CHAT_GPT_MODEL")
    open_ai_chat = OpenAIChat(chat_model)
    response = open_ai_chat.chat("Tell me a fairy tale story for my kid")
    print(response)
