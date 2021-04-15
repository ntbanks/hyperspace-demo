import streamlit as st
import streamlit.components.v1 as components
import base64
import pandas as pd
import numpy as np
import argparse
import sys

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

def parse_args(args):
    parser = argparse.ArgumentParser('DS POC')
    parser.add_argument('--theme', help='Theme: dark or light', default='dark', required=False)
    return parser.parse_args(args)

args = parse_args(sys.argv[1:])
cust_theme = args.theme

# load in .css file/logo and write to the config.toml logo based on theme choice

if cust_theme == "light":
    icon_url = f"data:image/png;base64,{load_image('./assets/static/logo-light.png')}"
    css_file = ('./assets/css/light.css')
    f = open("./.streamlit/config.toml", "w")
    toml_txt = "[theme]\nprimaryColor='#908F8F'\nbackgroundColor='#E8E8F0'\nsecondaryBackgroundColor='#F8F8F8'\ntextColor='#23242B'\nfont='sans serif'"
    f.write(toml_txt)
    f.close()
else:
    icon_url = f"data:image/png;base64,{load_image('./assets/static/logo-dark.png')}"
    css_file = ('./assets/css/dark.css')
    f = open("./.streamlit/config.toml", "w")
    toml_txt = "[theme]\nprimaryColor='#908F8F'\nbackgroundColor='#0e1117'\nsecondaryBackgroundColor='#23242B'\ntextColor='#fafafa'\nfont='sans serif'"
    f.write(toml_txt)
    f.close()


title_string = 'RS21 DS Prototype'
st.set_page_config(layout="wide", page_title=title_string, page_icon=icon_url)
# keeps this from going full full screen and looking ridiculous
st.markdown("<style>section.main{padding-left: 12%; padding-right: 12%;}</style>", unsafe_allow_html=True)

local_css(css_file)
local_css('./assets/css/main.css')

# Open Sans font
st.markdown("<link rel=\"stylesheet\" type=\"text/css\" href=\"//fonts.googleapis.com/css?family=Open+Sans\" />", unsafe_allow_html=True)

top_logo_html=f"""
    <div class="topdiv">
        <img class="toplogo" src={icon_url}>
        <div class="toptext">{title_string}</div>
    </div>
    """

# writes the logo and title into the header
st.markdown(top_logo_html, unsafe_allow_html=True)  














## EVERYTHING FROM HERE DOWN IS JUST EXAMPLES!

chart_data = pd.DataFrame(
     np.random.randn(20, 3),
     columns=['a', 'b', 'c'])

df = pd.read_csv('./assets/data/stormofswords.csv')

download_link = download_link(df, "test.csv", "Download")

st.title(title_string)
st.header("Data Inputs")

first,second = st.beta_columns(2)

with first:
    text_side = st.text_input('Text Input', 'Placeholder')
    test_sel = st.radio('Show Data', ('Yes', 'No')) 
    
with second:
    select_side = st.selectbox('Dropdown Select', ('Option 1', 'Option 2','Option 3'))
    check_test = st.checkbox('Show line chart')

st.header("Information Display")
st.markdown("<p>Regular content that's not in an accordion or card looks like this</p>", unsafe_allow_html=True)
st.markdown("<p>A streamlit data frame looks like this</p>", unsafe_allow_html=True)
if test_sel == 'Yes':
    st.dataframe(df)
    st.markdown(download_link, unsafe_allow_html=True)

expander1 = st.beta_expander("Accordion title", expanded=False)
with expander1:
    st.markdown("<p class='card'>Hidden accordion content</p>",unsafe_allow_html=True)
expander2 = st.beta_expander("Accordion title", expanded=True)
with expander2:
    st.markdown("<p class='card'>The content within an accordion panel could include a variety of content types. The content can be – a long paragraph of description text, structured content, unordered lists, images with captions, simple or complex tables, data visualizations and a lot more.The content within an accordion panel could include a variety of content types. The content can be – a long paragraph of description text, structured content, unordered lists, images with captions, simple or complex tables, data visualizations and a lot more.</p>", unsafe_allow_html=True);

st.markdown("<div class='card'><h3>Cool card title</h3><p class='card'>Lots of card content and stuff<br><br>tincidunt sit amet nibh ut imperdiet. Suspendisse dictum finibus velit, in ullamcorper nibh efficitur non. Pellentesque aliquet quam in lorem viverra, et condimentum nunc fringilla. Morbi non tempus leo. Curabitur eget velit risus. Quisque dictum risus ut mattis semper. Ut semper nulla luctus, rutrum elit a, iaculis neque. Integer malesuada sollicitudin risus, sed pulvinar justo volutpat pretium. Sed fermentum scelerisque diam fermentum congue. Maecenas non est ante. Proin eu ex ante.</p></div>",unsafe_allow_html=True);


if check_test:
    st.line_chart(chart_data)