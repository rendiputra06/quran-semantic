from .preprocess import *
import random

quran_clean_text = get_quran_indo_clean_text()


def get_verse_max_score(query_word, verse_text, model):
    
    maxi = -1.0
    for verse_word in verse_text:
        if query_word not in model or verse_word not in model:
            continue
        score = model.similarity(query_word, verse_word)
        maxi = max(score, maxi)

    return max(0.0, maxi)


def search_by_word(query_word, model, method):
   

    verse_props, verse_id = [], 0

    query_word = clean(query_word)
    if len(query_word):
        query_word = query_word[0]
    else:
        query_word = ''

    for verse in quran_clean_text:
        # Tokenizing and cleaning are made only once here :)
        score = method(query_word, verse, model)
        verse_props.append((score, verse_id))
        verse_id += 1

    verse_props.sort(reverse=True)

    # Return at most 50 verses
    max_out_length = min(len(verse_props), 50)
    most_similar_verses = [(score, verse_id, quran_clean_text[verse_id])
                           for score, verse_id in verse_props[:max_out_length]]
    return most_similar_verses


def search_by_sentence(query_text, model, method):
    
    query_text = preprocess(query_text)
    verse2score = {}
    for i in range(len(query_text)):
        most_similar_verses1 = search_by_word(query_text[i], model, method)
        for score, verse_id, verse in most_similar_verses1:
            # Doubling the score for the frequent results
            verse_tuple = tuple(verse)
            if (verse_id, verse_tuple) in verse2score:
                verse2score[(verse_id, verse_tuple)] += score
            else:
                verse2score[(verse_id, verse_tuple)] = score

    best_verses = [(score, verse_id, verse)
                   for (verse_id, verse), score in verse2score.items()]
    best_verses.sort(reverse=True)

    # Return at most 50 verses
    max_out_length = min(len(best_verses), 20)
    return best_verses[:max_out_length]


def search_similar_word(sentence, model):
    # tokenize the sentence into words
    words = preprocess(sentence)
    # initialize an empty list to store the generated words
    generated_words = []
    # loop through each word in the sentence
    for word in words:
        # get the most similar words to the word using the model
        similar_words = model.most_similar(word)
        # choose 10 random words from the similar words
        random_words = random.sample(similar_words, 5)
        # extract only the words from the tuples
        random_words = [w[0] for w in random_words]
        # append the random words to the generated words list
        generated_words.extend(random_words)
    return generated_words

def search_similar_word_with_scores(sentence, model):
    # tokenize the sentence into words
    words = preprocess(sentence)
    # initialize a list to store generated word-score pairs
    generated_data = []

    # loop through each word in the sentence
    for word in words:
        # get the most similar words and scores using the model
        similar_words_and_scores = model.most_similar(word, topn=10)
        # extract similar words and scores from the tuples
        similar_data = [{'word': w[0], 'score': w[1]}
                        for w in similar_words_and_scores]
        # append the similar words and scores to the generated data list
        generated_data.extend(similar_data)

    # Sort the generated data based on scores in descending order
    generated_data.sort(key=lambda x: x['score'], reverse=True)

    return generated_data
