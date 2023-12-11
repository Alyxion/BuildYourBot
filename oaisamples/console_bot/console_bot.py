import os
from typing import Literal

from pydantic import BaseModel

from oaisamples.easy_bot.easy_bot import gpt_model, EasyChatbot

PROMPT_DIR = os.path.dirname(__file__) + "/../prompts"
costs_per_1k_in = float(os.getenv("OPENAI_COSTS_PER_1K_IN", "0.001"))
costs_per_1k_out = float(os.getenv("OPENAI_COSTS_PER_1K_OUT", "0.002"))

if __name__ == "__main__":
    rel_path = os.path.dirname(__file__) + "/../config"
    os.makedirs(rel_path, exist_ok=True)
    HISTORY_FILENAME = f"{rel_path}/chat_history.txt"

    prompt = open(PROMPT_DIR + "/teacher_walter.txt", "r").read()

    ascii_colors_supported = False
    # check if the terminal supports colors
    escape_code_user = "\033[34m"
    escape_code_bot = "\033[32m"
    escape_code_default = "\033[39m"

    chat_bot = EasyChatbot(prompt=prompt)

    print(f"Chat conversation using {gpt_model}")
    print(f"Token limit: {chat_bot.max_tokens}")
    print("Say Hi to start, say Bye to end the conversation.\n")
    print("-----------------------------------------------------\n")

    # ask if the user wants to restore the history
    if os.path.exists(HISTORY_FILENAME):
        restore = input("Do you want to restore the chat history? (y/n) ")
        if restore.lower() == "y":
            chat_bot.restore_history(HISTORY_FILENAME)

    while True:
        user_input = input(f"{escape_code_user}You: {escape_code_default}")
        print(escape_code_default, end="")
        bot_response = chat_bot.add_message(user_input)
        print(f"{escape_code_bot}Bot: {escape_code_default}{bot_response}")
        if "bye" in user_input.lower():
            break
        chat_bot.store_history(HISTORY_FILENAME)

    print("\n-----------------------------------------------------\n")

    print("Total costs:")
    costs_in = chat_bot.input_tokens_usage / 1000 * costs_per_1k_in
    costs_out = chat_bot.output_token_usage / 1000 * costs_per_1k_out
    print(f"Input: {chat_bot.input_tokens_usage} tokens, ${costs_in}")
    print(f"Output: {chat_bot.output_token_usage} tokens, ${costs_out}")
    print(f"Total: ${costs_in + costs_out}")

    if chat_bot.response_count > 0:
        print(
            f"Average response time: {chat_bot.total_response_time / chat_bot.response_count}"
        )
