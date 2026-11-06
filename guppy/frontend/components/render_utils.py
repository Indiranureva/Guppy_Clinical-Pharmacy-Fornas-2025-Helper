"""HTML Rendering Utilities for Guppy Frontend.

Guarantees clean HTML injection without markdown code-block indentation bugs.
"""

import textwrap
import streamlit as st


def render_html(html_str: str):
    """Safely render HTML without any markdown parser interpreting indentation as code blocks.
    
    Uses Streamlit's native st.html if available, or dedented st.markdown with unsafe_allow_html.
    """
    clean_html = textwrap.dedent(html_str).strip()
    if hasattr(st, "html"):
        st.html(clean_html)
    else:
        st.markdown(clean_html, unsafe_allow_html=True)
