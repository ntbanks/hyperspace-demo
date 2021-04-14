import streamlit as st
import streamlit.components.v1 as components
import base64
import pandas as pd
import numpy as np

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
        return f'<a class=downloadlink href="data:file/txt;base64,{b64}" download="{download_filename}">{download_link_text}</a>'

icon_url = f"data:image/png;base64,{load_image('./assets/static/logo.png')}"
title_string = 'RS21 DS Prototype'
#title_string = ''

top_logo_html=f"""
    <div class="topdiv">
        <img class="toplogo" src={icon_url}>
        <div class="toptext">{title_string}</div>
    </div>
    """

# sets widescreen and the page_icon and title that show up in the tab
st.set_page_config(layout="wide", page_title=title_string, page_icon=icon_url)

# load in .css file. right now, main.css is dark theme
local_css('./assets/css/main.css')
# Open Sans font
st.markdown("<link rel=\"stylesheet\" type=\"text/css\" href=\"//fonts.googleapis.com/css?family=Open+Sans\" />", unsafe_allow_html=True)
# writes the logo and title into the header
st.markdown(top_logo_html, unsafe_allow_html=True)  














## EVERYTHING FROM HERE DOWN IS JUST EXAMPLES!

sidebar, main = st.beta_columns((1,4))

chart_data = pd.DataFrame(
     np.random.randn(20, 3),
     columns=['a', 'b', 'c'])

df = pd.read_csv('./assets/data/stormofswords.csv')
dl_link = download_link(df, "test.csv", "Download")

with sidebar:
    st.markdown("<p class='section-title'>Data Inputs</p>",unsafe_allow_html=True)
    st.markdown("<p class='content'>Regular content that's not in an accordion or card looks like this</p>", unsafe_allow_html=True)
    text_side = st.text_input('Text Input', 'Placeholder')

    select_side = st.selectbox('Dropdown Select', ('Option 1', 'Option 2','Option 3'))
    test_sel = st.radio('Show Data', ('Yes', 'No')) 
    check_test = st.checkbox('Show line chart')
    st.markdown(dl_link, unsafe_allow_html=True)


with main:
    st.markdown(f"<p class='title'>{title_string}</p>",unsafe_allow_html=True)
    
    expander1 = st.beta_expander("Accordion title", expanded=False)
    with expander1:
        st.markdown("<p class='content2'>Hidden accordion content</p>",unsafe_allow_html=True)
    expander2 = st.beta_expander("Accordion title", expanded=True)
    with expander2:
        st.markdown("<p class='content2'>The content within an accordion panel could include a variety of content types. The content can be – a long paragraph of description text, structured content, unordered lists, images with captions, simple or complex tables, data visualizations and a lot more.The content within an accordion panel could include a variety of content types. The content can be – a long paragraph of description text, structured content, unordered lists, images with captions, simple or complex tables, data visualizations and a lot more.</p>", unsafe_allow_html=True);

    st.markdown("<div class='card'><p class='card-title'>Cool card title<p class='content2'>Lots of card content and stuff<br><br>tincidunt sit amet nibh ut imperdiet. Suspendisse dictum finibus velit, in ullamcorper nibh efficitur non. Pellentesque aliquet quam in lorem viverra, et condimentum nunc fringilla. Morbi non tempus leo. Curabitur eget velit risus. Quisque dictum risus ut mattis semper. Ut semper nulla luctus, rutrum elit a, iaculis neque. Integer malesuada sollicitudin risus, sed pulvinar justo volutpat pretium. Sed fermentum scelerisque diam fermentum congue. Maecenas non est ante. Proin eu ex ante.</p></div>",unsafe_allow_html=True);

    if test_sel == 'Yes':
        st.dataframe(df)

    if check_test:
        st.line_chart(chart_data)