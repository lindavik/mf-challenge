import streamlit as st


st.title("Give Me The Odds")

placeholder = st.empty()
placeholder.text("POTATO")


def uploader_callback():
    placeholder.text("42%")


uploaded_file = st.file_uploader(label="A way to upload a JSON file containing the data intercepted by the rebels.",
                 type=["json"], on_change=uploader_callback, key='file_uploader')


with st.expander("Show hints"):
    st.text("An example of the expected file format can be seen below.")
    sample_file_content = '''
    {
      "countdown": 6,
      "bounty_hunters": [
        {"planet": "Tatooine", "day": 4 },
        {"planet": "Dagobah", "day": 5 }
      ]
    }
    '''
    st.code(sample_file_content, language='json')