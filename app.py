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

def get_label(text, section):
    """
    Adds a class to labels to allow custom coloring based on the section.
    text (str): label to be displayed
    section (str): one of "main" or "sidebar"
    ex: get_label("label", "main")
    """
    if section == "main":
        return f'<p class=\'main-label\'>{text}</p>';
    elif section == "sidebar":
        return f'<p class=\'sidebar-label\'>{text}</p>';


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
    <div class="topdiv">
        <img class="toplogo" src={icon_url}>
        <div class="toptext">{title_string}</div>
    </div>
    """

st.set_page_config(layout="wide", page_title=title_string, page_icon=icon_url)
local_css('./assets/css/main.css')
st.markdown(top_logo_html, unsafe_allow_html=True)
st.sidebar.header("hey")
st.markdown("<h2 class='title'>hey again</h2>",unsafe_allow_html=True)

st.sidebar.markdown(get_label('first label', 'sidebar'),unsafe_allow_html=True)
option = st.sidebar.selectbox('', ('Something 1', 'Something 2'))


st.sidebar.markdown(get_label('second label', 'sidebar'),unsafe_allow_html=True)
options = st.sidebar.multiselect('', ['green','yellow', 'blue', 'red'],['yellow','blue'])

st.markdown(get_label('main label', 'main'),unsafe_allow_html=True)
option_main = st.selectbox('', ('something', 'something else'))

