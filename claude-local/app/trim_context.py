def trim_context_window(message: list[dict], window: int = 3) -> list[dict]:
    """Trim the context window of the message.

    Args:
        message (list[dict]): The message to be trimmed.
        window (int): The window size to trim the message.

    Returns:
        list[dict]: The trimmed message.
    """
    msg = None

    # return only the first element if there is only one element
    if len(message[1:]) < window:
        msg = message[1:]

    # return the last five elements if there are more than five elements
    if len(message[1:]) > window:
        msg = message[-5:]

    # if the first element is an assistant message, remove it
    message_type = [item["role"] for item in msg]
    if message_type[0] == "assistant":
        msg = msg[1:]

    return msg
