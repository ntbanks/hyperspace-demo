import streamlit as st
import streamlit.components.v1 as components
import theme
import pandas as pd
import numpy as np

## EVERYTHING FROM HERE DOWN IS JUST EXAMPLES!

st.markdown("<style>section.main{padding-left: 12%; padding-right: 12%;}</style>", unsafe_allow_html=True)

chart_data = pd.DataFrame(
     np.random.randn(20, 3),
     columns=['a', 'b', 'c'])

df = pd.read_csv('./assets/data/stormofswords.csv')

download_link = theme.download_link(df, "test.csv", "Download")

st.title(theme.title_string)
st.header("Data Inputs")

first,second = st.beta_columns(2)

with first:
    text_side = st.text_input('Text Input', 'Placeholder')
    test_sel = st.radio('Show Data', ('Yes', 'No')) 
    
with second:
    select_side = st.selectbox('Dropdown Select', ('Option 1', 'Option 2','Option 3'))
    check_test = st.checkbox('Show line chart')

st.header("Information Display")
st.markdown("Regular content that's not in an accordion or card looks like this", unsafe_allow_html=True)
st.markdown("A streamlit data frame looks like this", unsafe_allow_html=True)
if test_sel == 'Yes':
    st.dataframe(df)
    st.markdown(download_link, unsafe_allow_html=True)

expander1 = st.beta_expander("Accordion title", expanded=False)
with expander1:
    st.markdown(theme.get_accordion("Hidden accordion content"),unsafe_allow_html=True)
expander2 = st.beta_expander("Accordion title", expanded=True)
with expander2:
    st.markdown("<p class='card'>The content within an accordion panel could include a variety of content types. The content can be – a long paragraph of description text, structured content, unordered lists, images with captions, simple or complex tables, data visualizations and a lot more.The content within an accordion panel could include a variety of content types. The content can be – a long paragraph of description text, structured content, unordered lists, images with captions, simple or complex tables, data visualizations and a lot more.</p>", unsafe_allow_html=True);

st.markdown(theme.get_card("Cool card title","Lots of card content and stuff<br><br>tincidunt sit amet nibh ut imperdiet. Suspendisse dictum finibus velit, in ullamcorper nibh efficitur non. Pellentesque aliquet quam in lorem viverra, et condimentum nunc fringilla. Morbi non tempus leo. Curabitur eget velit risus. Quisque dictum risus ut mattis semper. Ut semper nulla luctus, rutrum elit a, iaculis neque. Integer malesuada sollicitudin risus, sed pulvinar justo volutpat pretium. Sed fermentum scelerisque diam fermentum congue. Maecenas non est ante. Proin eu ex ante."),unsafe_allow_html=True);

if check_test:
    st.line_chart(chart_data)