import streamlit as st
import time

def autorefresh(interval=2000, key=None):
    """
    Automatically refresh the Streamlit app at the specified interval.

    Args:
        interval (int): Refresh interval in milliseconds. Default is 2000ms (2 seconds).
        key (str): Unique key for the refresh counter (optional).
    """
    if interval <= 0:
        raise ValueError("Interval must be a positive integer in milliseconds.")

    if key is None:
        key = f"autorefresh-{interval}"

    # Initialize or increment the refresh counter in session state
    if key not in st.session_state:
        st.session_state[key] = 0
    st.session_state[key] += 1

    # Trigger refresh
    time.sleep(interval / 1000)  # Convert milliseconds to seconds
    st.experimental_rerun()

# Attach autorefresh to the Streamlit namespace
st.autorefresh = autorefresh