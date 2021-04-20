import streamlit as st
import streamlit.components.v1 as components
import theme
import pandas as pd
import numpy as np


## EVERYTHING FROM HERE DOWN IS JUST EXAMPLES!

sidebar, main = st.beta_columns((1,4))

chart_data = pd.DataFrame(
     np.random.randn(20, 3),
     columns=['a', 'b', 'c'])

df = pd.read_csv('./assets/data/stormofswords.csv')
dl_link = theme.download_link(df, "test.csv", "Download", "right")

with sidebar:
    st.header("Data Inputs")
    st.markdown("Regular content that's not in an accordion or card looks like this")
    st.text("text text text")
    text_side = st.text_input('Text Input', 'Placeholder')

    select_side = st.selectbox('Dropdown Select', ('Option 1', 'Option 2','Option 3'))
    test_sel = st.radio('Show Data', ('Yes', 'No')) 
    check_test = st.checkbox('Show line chart')
    st.markdown(dl_link, unsafe_allow_html=True)


with main:
    st.title(theme.title_string)
    
    expander1 = st.beta_expander("Accordion title", expanded=False)
    with expander1:
        st.markdown(theme.get_accordion("Hidden accordion content"),unsafe_allow_html=True)
    expander2 = st.beta_expander("Accordion title", expanded=True)
    with expander2:
        st.markdown("<p class='card'>The content within an accordion panel could include a variety of content types. The content can be – a long paragraph of description text, structured content, unordered lists, images with captions, simple or complex tables, data visualizations and a lot more.The content within an accordion panel could include a variety of content types. The content can be – a long paragraph of description text, structured content, unordered lists, images with captions, simple or complex tables, data visualizations and a lot more.</p>", unsafe_allow_html=True)

    st.markdown(theme.get_card("Cool card title","Lots of card content and stuff<br><br>tincidunt sit amet nibh ut imperdiet. Suspendisse dictum finibus velit, in ullamcorper nibh efficitur non. Pellentesque aliquet quam in lorem viverra, et condimentum nunc fringilla. Morbi non tempus leo. Curabitur eget velit risus. Quisque dictum risus ut mattis semper. Ut semper nulla luctus, rutrum elit a, iaculis neque. Integer malesuada sollicitudin risus, sed pulvinar justo volutpat pretium. Sed fermentum scelerisque diam fermentum congue. Maecenas non est ante. Proin eu ex ante.","right"),unsafe_allow_html=True)

    if test_sel == 'Yes':
        st.dataframe(df)

    if check_test:
        st.line_chart(chart_data)

    st.button('ST Button')
    st.multiselect('Multiselect', [1,2,3])
    st.slider('Slide me', min_value=0, max_value=10)
    st.select_slider('Slide to select', options=[1,'2'])
    st.number_input('Enter a number')
    st.text_area('Area for textual entry')
    st.date_input('Date input')
    st.time_input('Time entry')
    st.file_uploader('File uploader')
    st.color_picker('Pick a color')