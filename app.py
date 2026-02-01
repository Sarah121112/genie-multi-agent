import uuid
import streamlit as st
from agents.coordinator import build_coordinator
from utils.retry import retry_call

st.set_page_config(page_title="Genie Multi-Agent", layout="centered")

if "agent" not in st.session_state:
    st.session_state.agent = build_coordinator()

if "thread_id" not in st.session_state:
    st.session_state.thread_id = "case-study-thread"

if "messages" not in st.session_state:
    st.session_state.messages = []

config = {"configurable": {"thread_id": st.session_state.thread_id}}

st.title("Genie Multi-Agent")
st.caption(f"thread_id: {st.session_state.thread_id}")

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

prompt = st.chat_input("Ask about sales, customers, or inventory...")
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            ok, result, err, attempts = retry_call(
                lambda: st.session_state.agent.invoke(
                    {"messages": [("user", prompt)]},
                    config=config,
                ),
                retries=2,
                base_delay=1.0,
                max_delay=6.0,
            )

            if not ok:
                reply = (
                    "⚠️ I couldn’t connect to the language model right now.\n\n"
                    "Please try again in a few seconds.\n\n"
                    f"Attempts: {attempts}\n"
                    f"Error: {err}"
                )
            else:
                messages = result.get("messages", [])
                reply = messages[-1].content if messages else "(no response)"

            st.markdown(reply)

    st.session_state.messages.append({"role": "assistant", "content": reply})

col1, col2 = st.columns(2)
with col1:
    if st.button("New conversation"):
        st.session_state.thread_id = str(uuid.uuid4())
        st.session_state.messages = []
        st.rerun()

with col2:
    if st.button("Clear chat (keep memory)"):
        st.session_state.messages = []
        st.rerun()
