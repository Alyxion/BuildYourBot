import os
import time

import openai
import tiktoken
from dotenv import load_dotenv
from openai import OpenAI
from openai.lib.azure import AzureOpenAI

from .history_entry import HistoryEntry

# fetch credentials from environment
load_dotenv(os.path.dirname(__file__) + "/../../.env")

api_key = os.getenv("OPENAI_KEY")
azure_endpoint = os.getenv("OPENAI_AZURE_ENDPOINT", None)
api_version = os.getenv("OPENAI_API_VERSION")
gpt_model = os.getenv("OPENAI_BASE_MODEL")

# define directories
PROMPT_DIR = os.path.dirname(__file__) + "/../prompts"


class EasyChatbot:
    """A very simple chatbot that uses OpenAI's API to generate responses,
    keeps track of the history and summarizes it if necessary"""

    def __init__(self, prompt):
        """Initialize the chatbot

        :param prompt: The system prompt to use"""
        self.client = None
        if azure_endpoint is not None:
            self.client = AzureOpenAI(
                api_key=api_key, azure_endpoint=azure_endpoint, api_version=api_version
            )
        else:
            openai.api_version = api_version
            self.client = OpenAI(api_key=api_key)
        self.message_history: list[HistoryEntry] = []
        """The history of the chatbot"""
        self.max_response_tokens = 400
        """Maximum number of tokens the chatbot can generate"""
        self.max_user_tokens = 200
        """Maximum number of tokens the user can input"""
        self.max_history_tokens = self.max_response_tokens * 2
        """Maximum number of tokens the chatbot can generate"""
        self.max_summary_length = self.max_history_tokens * 2 // 3
        """Maximum number of tokens the chatbot can generate for the summary"""
        self.old_history = ""
        """The old history of the chatbot"""
        self.model = gpt_model
        """The model to use"""
        self.tokenizer = tiktoken.get_encoding("cl100k_base")
        """The tokenizer to use to count the tokens"""
        self.input_tokens_usage = 0
        """The number of tokens the user input and prompt generated"""
        self.output_token_usage = 0
        """The number of tokens the chatbot generated"""
        self.system_prompt = (
            f"{prompt}\nBelow you can find the history of our previous"
            "conversation:\n"
            ""
        )
        """Maximum number of tokens the user can input"""
        self.max_tokens = (
                self.max_history_tokens
                + self.max_user_tokens
                + len(self.tokenizer.encode(self.system_prompt))
        )
        """Maximum number of tokens for the chatbot to generate"""
        self.response_count = 0
        """Total count of responses"""
        self.total_response_time: float = 0.0
        """Total response time"""

    def history_as_string(self, include_old_history: bool = True) -> str:
        """Get the chat history as a string

        :param include_old_history: Whether to include the old history
        :return: The chat history as a string
        """
        history = "\n".join(
            [f"{entry.user_type}: {entry.message}" for entry in self.message_history]
        )
        if include_old_history:
            history = f"{self.old_history}\n{history}"
        return history

    def summarize_history(self):
        """Summarize the chat history to a short version"""
        prompt = open(PROMPT_DIR + "/basic_summary.txt", "r").read()
        history = self.history_as_string(include_old_history=True)
        completion = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "system", "content": prompt + history}],
            temperature=0.0,
            max_tokens=self.max_history_tokens + len(self.tokenizer.encode(prompt)) + 5,
            top_p=1,
        )
        # count costs
        self.input_tokens_usage += completion.usage.prompt_tokens
        self.output_token_usage += completion.usage.completion_tokens
        # check if an error occurred
        if completion.choices[0].finish_reason != "stop":
            raise Exception(completion.choices[0].error)
        self.message_history = []
        self.old_history = completion.choices[0].message.content

    def cleanup_history(self):
        """Verify that the history is not too long and summarize it if necessary"""
        hist_string = self.history_as_string(include_old_history=True)
        cur_tokens = self.tokenizer.encode(hist_string)
        if len(cur_tokens) > self.max_history_tokens:
            self.summarize_history()
            new_tokens = self.tokenizer.encode(self.history_as_string())
            print(self.old_history)
            print(
                f"Summarized history. Previous: {len(cur_tokens)} Now: {len(new_tokens)}"
            )

    def add_message(self, message: str) -> str:
        """Send a message to OpenAI including the system prompt and the chat history
        and return the response

        :param message: The message to send
        :return: The response of the chatbot"""
        history: list[dict] = []
        for element in self.message_history:
            history.append({"role": element.user_type, "content": element.message})
        conv_history = (  # construct the conversation history
                [
                    {
                        "role": "system",
                        "content": self.system_prompt + self.old_history,
                    }
                ] + history + [
                    {
                        "role": "user",
                        "content": message,
                    }
                ]
        )
        start_time = time.time()
        # Call the OpenAI API interface
        completion = self.client.chat.completions.create(
            model=self.model,
            messages=conv_history,
            temperature=0.5,
            max_tokens=self.max_tokens,
            top_p=1,
        )
        self.total_response_time += time.time() - start_time
        self.response_count += 1
        # count costs
        self.input_tokens_usage += completion.usage.prompt_tokens
        self.output_token_usage += completion.usage.completion_tokens
        self.message_history.append(HistoryEntry(user_type="user", message=message))
        answer = completion.choices[0].message.content
        self.message_history.append(HistoryEntry(user_type="assistant", message=answer))
        self.cleanup_history()
        return answer

    def store_history(self, filename: str):
        """Store the history to a file

        :param filename: The filename to store to"""
        with open(filename, "w") as f:
            f.write(self.history_as_string(include_old_history=True))

    def restore_history(self, filename: str):
        """Restore the history from a file

        :param filename: The filename to restore from"""
        if os.path.exists(filename):
            with open(filename, "r") as f:
                self.old_history = f.read()
                self.cleanup_history()
