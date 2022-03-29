import streamlit as st

from PIL import Image


st.title("Give Me The Odds")

top_column_left, top_column_right = st.columns(2)
top_column_left.subheader("Instructions")
top_column_left.write("To get the odds of the Millennium Falcon reaching Endor in time and saving the galaxy, upload a JSON file containing the data intercepted by the rebels.")
top_column_left.write("You can read more about the challenge [here](https://github.com/dataiku/millenium-falcon-challenge)")

image = Image.open('static/c3po.png')
top_column_right.image(image)

mid_column_left, mid_column_right = st.columns(2)
mid_column_left.header("ODDS (%):")


def uploader_callback():
    if uploaded_file is None:
        mid_column_right.header("Calculating...")
    else:
        mid_column_right.header("")


uploaded_file = st.file_uploader(label="Upload a JSON file containing the data intercepted by the rebels below",
                                 type=["json"],
                                 on_change=uploader_callback,
                                 key="file_uploader",
                                 help="Expand the 'Show hints' section to learn more about the expected file format")


with st.expander("Show hints"):
    st.write("An example of the expected file format can be seen below.")
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
