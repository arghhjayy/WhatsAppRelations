import emoji
import pandas as pd
from gensim.models import Word2Vec
import re
import string
import warnings
from flask import Flask, jsonify, request
warnings.filterwarnings('ignore')

app = Flask(__name__)

with open('../assets/stop_hinglish.txt', 'r') as f:
	STOPWORDS = f.read().split('\n')


def remove_emoji(text):
	return emoji.replace_emoji(text, replace='')


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

	# final cleanup, check if strings are empty
	lines = [line for line in lines if line != '']
	lines = [line.lower() for line in lines]
	return lines


def prepare_model(data, n_iters):
	lines = data.read().decode('utf-8')

	lines = lines.split('\n')

	cleaned_lines = clean_lines(lines)

	word2vec_input = [cleaned_lines[i].split() for i in range(len(cleaned_lines))]

	model = Word2Vec(vector_size=50, window=10, min_count=1)

	model.build_vocab(word2vec_input)

	model.train(word2vec_input, total_examples=len(cleaned_lines), epochs=n_iters)

	print(model)

	model.save("saved_model.model")


def load_saved_model():
	try:
		model = Word2Vec.load("saved_model.model")
		return model
	except:
		return None


@app.route("/health", methods=["GET"])
def health_check():
	return jsonify("Healthy")


@app.route("/make_embeddings", methods=["POST"])
def make_model():
	data_file = request.files["data_file"]
	n_iters = 300
	prepare_model(data_file, n_iters)
	return jsonify("Done")


@app.route("/top_n_similar", methods=["POST"])
def top_n_similar():
	model = load_saved_model()

	if model is None:
		return jsonify("Model loading failed")

	# print(model.wv.index_to_key)

	req_data = request.get_json()
	word = req_data['word']
	n = req_data['n']
	try:
		res = model.wv.most_similar(word, topn=n)
		return jsonify(res)
	except Exception as e:
		print(e)
		return jsonify('Word is either not entered or does not exist in dictionary')


@app.route("/word_analogies", methods=["POST"])
def word_analogies():
	model = load_saved_model()

	if model is None:
		return jsonify("Model loading failed")

	word1 = request.post['word_1']
	word2 = request.post['word_2']
	word3 = request.post['word_3']

	try:
		res = model.wv.most_similar(positive=[word3, word2], negative=[word1])
		res = pd.DataFrame(res, columns=['word', 'similarity score'])
		return jsonify(dict(res))
	except:
		return jsonify('At least one of the three word above does not exist in the dictionary')

if __name__ == "__main__":
	app.run(debug=True, host="0.0.0.0")
