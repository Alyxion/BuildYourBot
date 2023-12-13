import os
import time

import streamlit as st
from oaisamples.easy_bot import EasyChatbot

PROMPT_DIR = os.path.dirname(__file__) + "/../prompts"  # The directory where the prompts are stored
PROMPT_SOURCES = ["teacher_walter.txt"]  # The prompts to use, will be concatenated
BOT_NAME = "Walter"  # The name of the chatbot


class StreamlitChatbot:
    """A very simple chatbot that uses OpenAI's API to generate responses
    and Streamlit to render the chatbot conversation"""

    def __init__(self):
        """Initialize the chatbot"""
        if "bot" not in st.session_state:
            st.session_state["bot"] = self.create_new_instance()
        self.bot = st.session_state.bot
        """The chatbot instance"""
        self.max_history = 20
        """Maximum number of recent messages to show"""
        self.min_response_time = 1.5
        """The minimum response time in seconds to make the bot seem more human"""

    @classmethod
    def create_new_instance(cls) -> EasyChatbot:
        """Creates a new chatbot instance"""
        prompt = "\n".join([open(f"{PROMPT_DIR}/{cur_prompt}", "r").read() for cur_prompt in PROMPT_SOURCES])
        bot = EasyChatbot(prompt)
        return bot

    def render_page(self):
        """Renders the chatbot page"""
        recent_conversation = self.bot.message_history[-self.max_history:]
        if len(recent_conversation) == 0:
            st.title("Streamlit Chatbot Demo")
            st.markdown("---")
            st.write("Say Hi to start the conversation.")
        for cur_message in recent_conversation:
            name = BOT_NAME if cur_message.user_type == "assistant" else "You"
            with st.chat_message(name, avatar=cur_message.user_type):
                st.markdown(cur_message.message)
        si = st.chat_input('Type a message...')
        if si:
            text = str(si)
            with st.chat_message("You", avatar="user"):
                st.markdown(text)
            with st.chat_message(BOT_NAME, avatar="assistant"):
                with st.spinner(f"{BOT_NAME} is thinking..."):
                    start_time = time.time()
                    self.bot.add_message(text)
                    cur_time = time.time()
                    if cur_time - start_time < self.min_response_time:
                        # if the answer was too fast, wait a bit, Microsoft-style
                        time.sleep(self.min_response_time - (cur_time - start_time))

            st.rerun()


if __name__ == '__main__':
    st.set_page_config(page_title="Streamlit Chatbot", page_icon="🤖")
    # disable magic commands
    chatbot = StreamlitChatbot()
    chatbot.render_page()
