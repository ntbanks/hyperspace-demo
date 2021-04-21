# Streamlit Theme
## Install
> pip install streamlit

## Running
There are two example versions of a streamlit app using the theme.\
The first 90 or so lines are necessary for the theme, and the rest is just examples of using the components.

### app.py 
Set up with inputs on a left "sidebar" and the data displays/text in a main section.
> streamlit run app.py

### app-no-sidebar.py 
Set up with inputs at the top and the data displays/text below.
> streamlit run app-no-sidebar.py

Both can accept a theme argument with either "light" or "dark" as options:
> streamlit run app.py -- --theme light

dark is the default\
\
The extra set of "--" is so that streamlit ignores all of the args and they get passed straight to python.\
If the streamlit app needs an argument, like port, this will need to be removed and the theme will need to be set manually.

## Theming
All of the streamlit interactive input componenets and most text options are automatically formatted. Below is the list of formatted text options:\
st.title() - title of the app (RS21 DS Prototype)\
st.header() - section headings (Data Inputs)\
st.subheader() - the same as st.header() but smaller\
st.markdown() - all body text\
st.text() - this is designed by streamlit as a fixed width text display and will force a scroll bar if the text is too long. use markdown\

### Accordion:
The title bar of the accordion is styled automatically but the content needs to be wrapped in a paragraph tag like this:
```
expander1 = st.beta_expander("Accordion title", expanded=False)
with expander1:
    st.markdown("<p class='card'>Hidden accordion content</p>",unsafe_allow_html=True)
```
OR\
there is a "get_accordion()" function that takes a string and returns the string wrapped in the tag
```
expander1 = st.beta_expander("Accordion title", expanded=False)
with expander1:
    st.markdown(get_accordion("Hidden accordion content"),unsafe_allow_html=True)
```

### Cards:
There is a "get_card()" function that takes two args (title, content) and wraps them in the necessary html tags and returns the full html needed for the card.\
get_card() has a third optional argument "align" that allows you to pass the string "right" to align the card on the right side of the screen.
```
st.markdown(get_card("title","content"), unsafe_allow_html=True)
```

### Download link:
There is a download_link() function that returns the html for a download button.\
download_link has the same optional argument "align" that allows you to align the button on the right side of the screen.
```
download_html = download_link(df, filename, 'EXPORT DATA')
st.markdown(download_html, unsafe_allow_html=True)
```
