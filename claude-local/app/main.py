import streamlit as st
from anthropic import Anthropic
from anthropic._streaming import Stream
from anthropic.types.raw_message_stream_event import RawMessageStreamEvent
from config_env import config_env
from trim_context import trim_context_window


def main() -> None:
    """Main entry point of the app."""
    api_key = config_env()
    with st.sidebar:
        "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"
        "[View the source code](https://github.com/streamlit/llm-examples/blob/main/Chatbot.py)"
        "[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/streamlit/llm-examples?quickstart=1)"

    st.title("💬 Claude AI Personal Chatbot")

    if "messages" not in st.session_state:
        st.session_state["messages"] = [
            {"role": "assistant", "content": "How can I help you?"}
        ]

    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

    if prompt := st.chat_input():
        if not api_key:
            st.info("Please add your API key to continue.")
            st.stop()

        client = Anthropic(api_key=api_key)
        st.session_state.messages.append({"role": "user", "content": prompt})
        # print(len(trim_context_window(st.session_state.messages)))
        st.chat_message("user").write(prompt)
        response = client.messages.create(
            model="claude-3-5-sonnet-20240620",
            max_tokens=1000,
            # messages=trim_context_window(st.session_state.messages),
            messages=[{"role": "user", "content": prompt}],
            stream=True,
        )
        st.chat_message("assistant").write_stream(process_stream(response))


def process_stream(message: Stream[RawMessageStreamEvent]) -> str:
    """Custom stream processor."""
    for msg in message:
        if msg.type in ["content_block_delta"]:
            yield msg.delta.text


# TODO: need to fix context window issue, only sending the prompt message to the model
# TODO: need to fix context window not being printed to window when new message is sent

if __name__ == "__main__":
    main()
