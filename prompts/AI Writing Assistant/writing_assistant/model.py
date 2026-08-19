"""Live model construction for the (non-demo) pipeline."""

from __future__ import annotations

import os
from typing import Any

import streamlit as st

from . import config


def has_groq_key() -> bool:
    return bool(os.environ.get("GROQ_API_KEY"))


@st.cache_resource(show_spinner=False)
def create_model(temperature: float) -> Any:
    if not has_groq_key():
        raise RuntimeError(
            "GROQ_API_KEY is not set. Add it to a .env file, or switch on "
            "Demo mode in the sidebar to try the app without an API key."
        )
    from langchain_groq import ChatGroq

    return ChatGroq(model=config.GROQ_MODEL, temperature=temperature)