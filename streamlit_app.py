import streamlit as st
from openai import OpenAI

# Set custom page config for colors and emoji favicon
st.set_page_config(page_title="Gardener Chatbot", page_icon="🌱", layout="centered", initial_sidebar_state="auto")

# Add custom CSS for a richer green background and more readable text
st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(135deg, #388e3c 0%, #81c784 100%) !important;
        min-height: 100vh;
        color: #fff !important;
    }
    .stMarkdown, .stTextInput, .stChatInput, .stCaption, .stTitle, .stInfo, .stAlert, .stChatMessage {
        color: #fff !important;
    }
    .leaf {
        position: fixed;
        z-index: 0;
        width: 80px;
        opacity: 0.18;
    }
    .leaf.top-left { top: 10px; left: 10px; transform: rotate(-20deg); }
    .leaf.top-right { top: 10px; right: 10px; transform: rotate(20deg) scaleX(-1); }
    .leaf.bottom-left { bottom: 10px; left: 10px; transform: rotate(15deg); }
    .leaf.bottom-right { bottom: 10px; right: 10px; transform: rotate(-15deg) scaleX(-1); }
    </style>
    <img src="https://cdn.pixabay.com/photo/2013/07/12/13/57/leaf-147280_1280.png" class="leaf top-left" />
    <img src="https://cdn.pixabay.com/photo/2013/07/12/13/57/leaf-147280_1280.png" class="leaf top-right" />
    <img src="https://cdn.pixabay.com/photo/2013/07/12/13/57/leaf-147280_1280.png" class="leaf bottom-left" />
    <img src="https://cdn.pixabay.com/photo/2013/07/12/13/57/leaf-147280_1280.png" class="leaf bottom-right" />
    """,
    unsafe_allow_html=True
)

# Show title and description.
st.title("Gardener Chatbot 🌱")
st.caption("\"To plant a garden is to believe in tomorrow.\" – Audrey Hepburn")
st.write("This is a simple chatbot that uses the OpenAI API to answer gardening questions.")
st.write("Howdy there, sprout! I'm your gardener grandpa—ready to help your plants grow tall and your thumbs turn green. Ask me anything about gardening, and I'll throw in a joke or two—just to keep things fertile!")

# Ask user for their OpenAI API key via `st.text_input`.
# Alternatively, you can store the API key in `./.streamlit/secrets.toml` and access it
# via `st.secrets`, see https://docs.streamlit.io/develop/concepts/connections/secrets-management
openai_api_key = st.text_input("OpenAI API Key", type="password")
if not openai_api_key:
    st.info("Please add your OpenAI API key to continue.", icon="🗝️")
else:

    # Create an OpenAI client.
    client = OpenAI(api_key=openai_api_key)

    # Create a session state variable to store the chat messages. This ensures that the
    # messages persist across reruns.
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display the existing chat messages via `st.chat_message`.
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Create a chat input field to allow the user to enter a message. This will display
    # automatically at the bottom of the page.
    if prompt := st.chat_input("Ask grandpa gardener anything about your plant or gardening!"):

        # Store and display the current prompt.
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Build system prompt for grandpa gardener persona
        system_prompt = (
            "You are a friendly, wise, and humorous old gardener grandpa. "
            "When the user asks about a plant, always give detailed information about the plant, how to cultivate and care for it, "
            "and make occasional gardening puns and grandpa jokes. "
            "Make sure to include at least one funny gardening joke in every answer. "
            "Keep your tone warm, encouraging, and a bit playful."
        )

        # Prepare messages for OpenAI API
        messages = [
            {"role": "system", "content": system_prompt},
        ] + [
            {"role": m["role"], "content": m["content"]}
            for m in st.session_state.messages
        ]

        # Generate a response using the OpenAI API.
        stream = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            stream=True,
        )

        # Stream the response to the chat using `st.write_stream`, then store it in 
        # session state.
        with st.chat_message("assistant"):
            response = st.write_stream(stream)
        st.session_state.messages.append({"role": "assistant", "content": response})
