import streamlit as st
import streamlit.components.v1 as components
import base64
import pandas as pd


def local_css(file_name):
    with open(file_name) as f:
        st.markdown('<style>{}</style>'.format(f.read()), unsafe_allow_html=True)

def load_image(path):
    with open(path,"rb") as img:
        return base64.b64encode(img.read()).decode()

def download_link(object_to_download, download_filename, download_link_text):
    """
    Generates a link to download the given object_to_download.
    object_to_download (str, pd.DataFrame):  The object to be downloaded.
    download_filename (str): filename and extension of file. e.g. mydata.csv, some_txt_output.txt
    download_link_text (str): Text to display for download link.
    Examples:
        download_link(YOUR_DF, 'YOUR_DF.csv', 'Click here to download data!')
        download_link(YOUR_STRING, 'YOUR_STRING.txt', 'Click here to download your text!')
    """
    if isinstance(object_to_download,pd.DataFrame):
        object_to_download = object_to_download.to_csv(index=False)
        # some strings <-> bytes conversions necessary here
        b64 = base64.b64encode(object_to_download.encode()).decode()
        return f'<a class="downloadlink" href="data:file/txt;base64,{b64}" download="{download_filename}">{download_link_text}</a>'

icon_url = f"data:image/png;base64,{load_image('./assets/static/logo.png')}"

title_string = 'RS21 DS Prototype'

top_logo_html=f"""
    <div style="z-index: 101; display:inline-block; position: fixed; left: 0; top: 0;">
        <img style="padding-left:15px; padding-right: 10px; padding-bottom: 8px; display:inline-block;" src={icon_url}>
        <h2 style="display: inline-block;">{title_string}</h2>
    </div>
    """

st.set_page_config(layout="wide", page_title=title_string, page_icon=icon_url)
local_css('./assets/css/main.css')
st.markdown(top_logo_html, unsafe_allow_html=True)
