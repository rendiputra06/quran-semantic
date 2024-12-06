from .preprocess import *
import random
from multiprocessing import Pool

quran_clean_text = get_quran_indo_clean_text()


def get_verse_max_score(query_word, verse_text, model):

    maxi = -1.0
    for verse_word in verse_text:
        if query_word not in model or verse_word not in model:
            continue
        score = model.similarity(query_word, verse_word)
        maxi = max(score, maxi)

    return max(0.0, maxi)


def cari_kata(query_word, model, method):

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


def search_by_word_parallel(args):
    word, model, method = args
    return cari_kata(word, model, method)


def cari_kalimat(query_text, model, method):
    query_text = preprocess(query_text)
    verse2score = {}

    with Pool() as pool:
        results = pool.map(search_by_word_parallel, [
                           (word, model, method) for word in query_text])

    for most_similar_verses1 in results:
        for score, verse_id, verse in most_similar_verses1:
            verse_tuple = tuple(verse)
            if (verse_id, verse_tuple) in verse2score:
                verse2score[(verse_id, verse_tuple)] += score
            else:
                verse2score[(verse_id, verse_tuple)] = score

    best_verses = [(score, verse_id, verse)
                   for (verse_id, verse), score in verse2score.items()]
    best_verses.sort(reverse=True)
    max_out_length = min(len(best_verses), 20)
    return best_verses[:max_out_length]
