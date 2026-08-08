from langfuse.langchain import CallbackHandler


def get_langfuse_handler():
    return CallbackHandler()