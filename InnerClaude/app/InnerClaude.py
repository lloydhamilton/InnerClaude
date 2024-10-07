import os

import streamlit as st
from anthropic import Anthropic
from anthropic._streaming import Stream
from anthropic.types.raw_message_stream_event import RawMessageStreamEvent
from dotenv import load_dotenv


class InnerClaude:
    """InnerClaude class."""

    def __init__(self, session_state: st.session_state) -> None:
        """Initialise the InnerClaude class.

        Args:
            session_state: The session state of the current streamlit app.

        """
        self.__api_key = None
        self.load_envars()
        self.selected_model = None
        self.session_state = self.check_session_state(session_state)
        self._model_options = {
            "claude-3-5-sonnet-20240620": "Claude 3 Sonnet",
            "claude-3-opus-20240229": "Claude 3 Opus",
            "claude-3-haiku-20240307": "Claude 3 Haiku",
        }

    @property
    def model_options(self) -> dict:
        """Get the model options."""
        return self._model_options

    @property
    def api_key(self) -> str:
        """Get the api key."""
        return self.__api_key

    def load_envars(self) -> None:
        """Loads the api key from the .env file."""
        load_dotenv()
        api_key = os.getenv("API_KEY")
        self.__api_key = api_key
        if self.__api_key is None:
            st.info("Please configure your API key in the project. See README.md")
            st.stop()

    def anthropic_client(self) -> Anthropic:
        """Initialise the Anthropic client.

        If the client does not exist, initialise it. Otherwise, return the existing
        client.
        """
        if self.session_state.anthropic_client is None:
            client = Anthropic(api_key=self.api_key)
            self.session_state.anthropic_client = client
        return self.session_state.anthropic_client

    def configure_sidebar(self) -> str:
        """Configure the sidebar.

        The sidebar contains the model selection.
        """
        with st.sidebar:
            st.title("⚙️ Settings")
            selected_model = st.selectbox(
                "Select a model",
                options=list(self.model_options.keys()),
                format_func=lambda index: self.model_options[index],
                index=0,
                help="Select a model to chat with.",
            )

        self.selected_model = selected_model

        return selected_model

    @staticmethod
    def check_session_state(session_state: st.session_state) -> st.session_state:
        """Check the session state.

        If the session state does not contain the messages key, initialise it.

        Args:
            session_state: The session state of the current streamlit app.
        """
        if "messages" not in session_state:
            session_state["messages"] = []
        if "anthropic_client" not in session_state:
            session_state["anthropic_client"] = None
        return session_state

    def title(self, title: str) -> None:
        """Set the title of the app.

        Args:
            title: The title of the app.
        """
        st.title(title)
        st.subheader(f"Powered by Anthropic {self.model_options[self.selected_model]}")

    def update_chat_context(self) -> None:
        """Update the chat context.

        This method updates the chat context with the messages from the session state.
        """
        for msg in self.session_state.messages:
            st.chat_message(msg["role"]).write(msg["content"])

    def process_prompt(self) -> None:
        """Process the user prompt."""
        if prompt := st.chat_input():
            client = self.anthropic_client()
            self.session_state.messages.append({"role": "user", "content": prompt})
            st.chat_message("user").write(prompt)
            try:
                response = client.messages.create(
                    model=self.selected_model,
                    max_tokens=1000,
                    messages=self.trim_context_window(self.session_state.messages),
                    stream=True,
                )
            except Exception as e:
                error_message = f"Oh no! We encountered an error: {e}"
                st.chat_message("assistant").write(error_message)
                self.append_message("assistant", error_message)
                st.stop()

            st.chat_message("assistant").write_stream(self.process_stream(response))

    def append_message(self, role: str, content: str) -> None:
        """Append a message to the session state.

        Args:
            role: The role of the message.
            content: The content of the message.
        """
        self.session_state.messages.append({"role": role, "content": content})

    def process_stream(self, message: Stream[RawMessageStreamEvent]) -> str:
        """Custom stream processor."""
        output = ""
        for msg in message:
            if msg.type in ["content_block_delta"]:
                output += msg.delta.text
                yield msg.delta.text
        self.append_message("assistant", output)

    @staticmethod
    def trim_context_window(message: list[dict], window: int = 10) -> list[dict]:
        """Trim the context window of the message.

        Args:
            message (list[dict]): The message to be trimmed.
            window (int): The window size to trim the message.

        Returns:
            list[dict]: The trimmed message.
        """
        msg = None

        # return only the first element if there is only one element
        if len(message) <= window:
            msg = message

        # return the last five elements if there are more than five elements
        if len(message) > window:
            msg = message[-window:]

        # if the first element is an assistant message, remove it
        message_type = [item["role"] for item in msg]
        if message_type[0] == "assistant":
            msg = msg[1:]

        return msg

    def start(self) -> str:
        """Start the app."""
        model = self.configure_sidebar()
        self.title("💬 Claude AI Personal Chatbot")
        st.chat_message("assistant").write("How can I help you?")
        self.update_chat_context()
        self.process_prompt()

        return model
