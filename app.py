import emoji
import pandas as pd
from gensim.models import Word2Vec
import re
import string
import warnings
import streamlit as st
from io import StringIO
warnings.filterwarnings('ignore')

@st.cache(suppress_st_warning=True, allow_output_mutation=True, show_spinner=False)
def read_stopwords():
	with open('stop_hinglish.txt', 'r') as f:
	    STOPWORDS = f.read().split('\n')
	return STOPWORDS

STOPWORDS = read_stopwords()

def remove_emoji(text):
    return emoji.get_emoji_regexp().sub(u'', text)

def remove_timestamp_chats(text):
    re_str = r'\d+\/\d+\/\d+, \d+:\d+ (AM|PM) - .+: '
    return re.sub(re_str, '', text)

def remove_punctuation(text):
    return text.translate(str.maketrans('', '', string.punctuation))

def remove_media_chats(text):
    if text == '<Media omitted>':
        return ''
    else:
        return text

def remove_group_change_chats(text):
    re_str = r'.+ changed .+'
    return re.sub(re_str, '', text)

def remove_URL(text):
    return re.sub(r"http\S+", "", text)

def remove_mobile_nos(text):
    return re.sub(r'\d+', '', text)

def remove_stopwords(text):
    return ' '.join([word for word in text.split() if word not in STOPWORDS])

def clean_lines(lines):
    lines = [remove_timestamp_chats(line) for line in lines]
    lines = [remove_URL(line) for line in lines]
    lines = [remove_media_chats(line) for line in lines]
    lines = [remove_group_change_chats(line) for line in lines]
    lines = [remove_emoji(line) for line in lines]
    lines = [remove_punctuation(line) for line in lines]
    lines = [remove_mobile_nos(line) for line in lines]
    lines = [remove_stopwords(line) for line in lines]
    lines = [line.strip() for line in lines]

    #final cleanup, check if strings are empty
    lines = [line for line in lines if line != '']
    lines = [line.lower() for line in lines]
    return lines

st.set_page_config(page_title='WhatsApp Relations!')

st.title('WhatsApp relations 👫')
st.write('What is hidden in your WhatsApp chats? 🤔')

@st.cache(suppress_st_warning=True, allow_output_mutation=True, show_spinner=False)
def prepare_model(data, n_iters, save_wv):
	lines = data.read().decode('utf-8')

	lines = lines.split('\n')

	lines_ = clean_lines(lines)

	word2vec_input = [lines_[i].split() for i in range(len(lines_))]

	model = Word2Vec(sentences=word2vec_input, 
	                 size=50, window=10, 
	                 min_count=30, iter=n_iters)

	if save_wv:
		model.save('saved_model.model')

	return model

data = st.file_uploader('Upload your WhatsApp exported chat file', type=['txt'])

if data is not None:
	n_iters = st.slider('Number of iterations', 50, 10000, value=100)

	save_wv = st.checkbox('Save word vectors?')

	with st.spinner(f'Analyzing your data, please wait...'):
		model = prepare_model(data, n_iters, save_wv)
	st.success('Finished building model!')

	st.title('Word similarity:')

	word = st.text_input('Enter word here')
	try:
		res = model.most_similar(word, topn=5)
		st.write(f'5 most similar words to {word}:')
		res = pd.DataFrame(res, columns=['word', 'similarity score'])
		st.write(res)
	except:
		st.write('Word is either not entered or does not exist in dictionary')

	st.title('Word analogies:')

	word1 = st.text_input('Word 1')
	word2 = st.text_input('Word 2')
	word3 = st.text_input('Word 3')

	try:
		res = model.wv.most_similar(positive=[word3, word2], negative=[word1])
		res = pd.DataFrame(res, columns=['word', 'similarity score'])
		st.write(f'{word1} : {word2} :: {word3} : ?')
		st.write(res)
	except:
		st.write('At least one of the three word above does not exist in the dictionary')
else:
	pass