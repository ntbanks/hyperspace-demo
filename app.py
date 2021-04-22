import streamlit as st
import streamlit.components.v1 as components
import base64
import pandas as pd
import numpy as np
import argparse
import sys
import matplotlib.pyplot as plt
import sqlite3
import pickle
from pickle import load
from keras.models import load_model
import keras
from sklearn.preprocessing import StandardScaler
from collections import deque
from time import sleep
import matplotlib.pyplot as plt
import altair as alt



def local_css(file_name):
    with open(file_name) as f:
        st.markdown('<style>{}</style>'.format(f.read()), unsafe_allow_html=True)

def load_image(path):
    with open(path,"rb") as img:
        return base64.b64encode(img.read()).decode()

def download_link(object_to_download, download_filename, download_link_text, align="left"):
    """
    Generates a link to download the given object_to_download.
    object_to_download (str, pd.DataFrame):  The object to be downloaded.
    download_filename (str): filename and extension of file. e.g. mydata.csv, some_txt_output.txt
    download_link_text (str): Text to display for download link.
    align (str): optional "right" or "left" argument to align the button on the right. left is default
    Examples:
        download_link(YOUR_DF, 'YOUR_DF.csv', 'Click here to download data!')
        download_link(YOUR_STRING, 'YOUR_STRING.txt', 'Click here to download your text!')
    """
    if isinstance(object_to_download,pd.DataFrame):
        object_to_download = object_to_download.to_csv(index=False)
        # some strings <-> bytes conversions necessary here
        b64 = base64.b64encode(object_to_download.encode()).decode()
        return f'<a class="downloadlink f{align}" href="data:file/txt;base64,{b64}" download="{download_filename}">{download_link_text}</a>'

def get_card(title, content, align="left"):
    """
    Generate the html to build a "card".
    title (str): the title of the card
    content (str): the content of the card
    align (str): optional "right" or "left" argument to align card on the right. left is default

    """
    return f"<div class='card  f{align}'><h2 class=card-title>{title}</h2><p class='card'>{content}</p></div>"

def get_accordion(content):
    return f"<p class='card'>{content}</p>"

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

# sets widescreen and the page_icon and title that show up in the tab

title_string = 'RS21 DS Prototype'
st.set_page_config(layout="wide", page_title=title_string, page_icon=icon_url)

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




@st.cache
def get_dfval_frame():
    with sqlite3.connect('turbofandata.db') as connection:
        dfval_new = pd.read_sql('SELECT * from dfval_notime', connection)
        return dfval_new
    
@st.cache
def load_saved_model():
    model = load_model('model_notime.h5')
    
    
@st.cache
def load_scaler():
    scaler_xtrain = load(open('scaler_xtrain_notime.pkl','rb'))
    


def get_single_hazard(params:dict,
                     scaler_xtrain, clf, b, survival_curve):
    """takes a single sample of data in the form of a dictionary and 
    returns the hazard function predicted by the model clf."""
    db = pd.DataFrame(params.values(), index=b.keys()).T[input_cols]
    X = scaler_xtrain.transform(db.to_numpy())
    hazard = clf.predict(X)
    survival_curve.append(survival_curve[-1]*(1 - hazard[0][0]))
    return hazard




    
dfval = get_dfval_frame()
#model = load_saved_model()
model = load_model('model_notime.h5')
#scaler_xtrain = load_scaler()
scaler_xtrain = load(open('scaler_xtrain_notime.pkl','rb'))
#st.write(f'{type(model)} : {type(dfval)} : {type(scaler_xtrain)}')
input_cols = ['setting_1', 'setting_2', 'setting_3', 's_1', 
              's_2', 's_3', 's_4', 's_5', 's_6', 's_7', 's_8',
              's_9', 's_10', 's_11', 's_12', 's_13', 's_14',
              's_15', 's_16', 's_17', 's_18', 's_19', 's_20', 's_21']



sats = tuple(dfval['id'].unique())
freq = st.sidebar.slider('Update Cycles per Second', min_value=1, max_value=3000)
sat = st.sidebar.selectbox('Select Satellite', sats)
start_monitoring = st.button('Start Monitoring')


#survival_curve = [1]
#last_rows = np.random.randn(1, 1)
#chart = st.line_chart(last_rows)

#for i in range(1, 101):
#    new_rows = last_rows[-1, :] + np.random.randn(5, 1).cumsum(axis=0)
#    status_text.text("%i%% Complete" % i)
#    chart.add_rows(new_rows)
#    progress_bar.progress(i)
#    last_rows = new_rows
#    time.sleep(0.05)

def other_monitor(sat):
    dfsat = dfval[dfval['id']==sat]
    dfsat.reset_index(inplace=True)
    survival_curve = [1.0000]
    start_row = [[1.000]]
    #chart = st.line_chart(np.array(survival_curve).reshape(len(survival_curve), -1))
    chart = st.line_chart(start_row)
    
    for i in dfsat.index:
        b = dfsat.iloc[i].to_dict()
        h = get_single_hazard(b, scaler_xtrain, model, b, survival_curve)
        print(h)
        new_row = start_row*([[1.0]] - h)
        chart.add_rows(new_row)
        start_row = new_row
        sleep(1./freq)
    


def stream_sat(sat):
    dfsat = dfval[dfval['id']==sat]
    dfsat.reset_index(inplace=True)
    fig, ax = plt.subplots()
    max_samples = 100
    max_x = max_samples
    x = np.arange(0, max_x)
    y = deque(np.zeros(max_samples), max_samples)
    #y = deque(np.ones(2), max_samples)
    ax .set_ylim(0, 1.2)
    line, = ax.plot(x, np.array(y))
    the_plot = st.pyplot(plt)
    #chart = st.line_chart(x,y)
    #survival_curve = [1]
    #chart = st.line_chart(np.array(survival_curve).reshape(len(survival_curve), -1))
    

        
    def animate():
        line.set_ydata(np.array(y))
        the_plot.pyplot(plt)
        y.append(survival_curve[-1])
    
    for i in dfsat.index:
        b = dfsat.iloc[i].to_dict()
        h = get_single_hazard(b, scaler_xtrain, model, b, survival_curve)
        #st.write(survival_curve[-1])
        animate()
        sleep(1./freq)
    
    
    
    
if start_monitoring:
    #stream_sat(sat)
    other_monitor(sat)


## EVERYTHING FROM HERE DOWN IS JUST EXAMPLES!

#sidebar, main = st.beta_columns((1,4))

#chart_data = pd.DataFrame(
#     np.random.randn(20, 3),
#     columns=['a', 'b', 'c'])

#df = pd.read_csv('./assets/data/stormofswords.csv')
#dl_link = download_link(df, "test.csv", "Download", "right")

#with sidebar:
#    st.header("Data Inputs")
#    st.markdown("Regular content that's not in an accordion or card looks like this")
#    st.text("text text text")
#    text_side = st.text_input('Text Input', 'Placeholder')

#    select_side = st.selectbox('Dropdown Select', ('Option 1', 'Option 2','Option 3'))
#    test_sel = st.radio('Show Data', ('Yes', 'No')) 
#    check_test = st.checkbox('Show line chart')
#    st.markdown(dl_link, unsafe_allow_html=True)


#with main:
#    st.title(title_string)
    
#    expander1 = st.beta_expander("Accordion title", expanded=False)
#    with expander1:
#        st.markdown(get_accordion("Hidden accordion content"),unsafe_allow_html=True)
#    expander2 = st.beta_expander("Accordion title", expanded=True)
#    with expander2:
#        st.markdown("<p class='card'>The content within an accordion panel could include a variety of content types. The content can be – a long paragraph of description text, structured content, unordered lists, images with captions, simple or complex tables, data visualizations and a lot more.The content within an accordion panel could include a variety of content types. The content can be – a long paragraph of description text, structured content, unordered lists, images with captions, simple or complex tables, data visualizations and a lot more.</p>", unsafe_allow_html=True)

#    st.markdown(get_card("Cool card title","Lots of card content and stuff<br><br>tincidunt sit amet nibh ut imperdiet. Suspendisse dictum finibus velit, in ullamcorper nibh efficitur non. Pellentesque aliquet quam in lorem viverra, et condimentum nunc fringilla. Morbi non tempus leo. Curabitur eget velit risus. Quisque dictum risus ut mattis semper. Ut semper nulla luctus, rutrum elit a, iaculis neque. Integer malesuada sollicitudin risus, sed pulvinar justo volutpat pretium. Sed fermentum scelerisque diam fermentum congue. Maecenas non est ante. Proin eu ex ante.","right"),unsafe_allow_html=True)

#    if test_sel == 'Yes':
#        st.dataframe(df)

#    if check_test:
#        st.line_chart(chart_data)

#    st.button('ST Button')
#    st.multiselect('Multiselect', [1,2,3])
#    st.slider('Slide me', min_value=0, max_value=10)
#    st.select_slider('Slide to select', options=[1,'2'])
#    st.number_input('Enter a number')
#    st.text_area('Area for textual entry')
#    st.date_input('Date input')
#    st.time_input('Time entry')
#    st.file_uploader('File uploader')
#    st.color_picker('Pick a color')