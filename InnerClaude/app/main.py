import streamlit as st

from InnerClaude import InnerClaude


def main() -> None:
    """Main entry point of the app."""
    inner_claude = InnerClaude(session_state=st.session_state)
    inner_claude.start()


if __name__ == "__main__":
    main()
