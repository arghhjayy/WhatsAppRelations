# WhatsApp relations 👫

Do you know how much information your WhatsApp group chats hold? That's a very open ended question. We as humans can read through the texts and infer a lot. We can infer about the relationships among the group members which consists of answering questions like

- With whom does this person interact with the most?
- What phrase does this person use the most?
- What is his/her/their nickname?

But, for a computer to learn about these relationships is difficult. In this project, I try applying a method called [Word2Vec word embeddings](https://arxiv.org/abs/1301.3781) which is widely used in the world of NLP to understand text data.

## But what are word embeddings?

Word embeddings or word vectors are numerical representations of words using x numbers. This "x" is called the dimension of the word vectors. To know more about word embeddings, you can refer to [this article](https://jalammar.github.io/illustrated-word2vec/)

## What do I do in this project?

I read the WhatsApp chat file, preprocess it and feed it to the Word2Vec model which computes the word embeddings for the words that occur more than 30 times in the file. This 30, along with many others is a variable that I played around for a bit. I settled for variables for which the results to me were satisfactory.The project uses [Gensim](https://radimrehurek.com/gensim/) to calculate these vectors. Here are the variable values that I have used:

- `size=50`
- `window=10`
- `min_count=30`

For more on this, refer to the official [Gensim Word2Vec documentation](https://radimrehurek.com/gensim/models/word2vec.html)

## What do I analyze?

From the calculated word vectors, these are the tasks that are performed:

1) Word similarity: given a word, I find the most similar 5 words using [cosine similarity](https://en.wikipedia.org/wiki/Cosine_similarity).

2) Word analogies: given three words, I find the fourth word that would fit the most. For more info, [check this out](https://examples.yourdictionary.com/analogy-ex.html)

## Understood, but...why?

1) Word similarity tells us what are the most associated words with the given word. For example, if we're looking at a WhatsApp group of current friends, we can give a friend's name as input and the most similar words would be the person's address, lane number, nickname, most used phrase, etc.
2) For word analogies, if we use a similar friends WhatsApp group example, if we're given "person1_name": "person1_nickname" :: "person2_name" : ?. This should output person2's nickname. 