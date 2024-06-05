from requests import get
from flask import jsonify, make_response
from flask_restful import Resource
from gensim.models.fasttext import load_facebook_model
from gensim.models import Word2Vec
from .preprocess import *
from .fungsi_semantik import *
from .pooling import *

# model_tw = Word2Vec.load('././models/full_grams_cbow_100_twitter.mdl').wv
# model_wiki = Word2Vec.load("././models/indonesia/wiki.id.case.model").wv
# model_pakai = load_facebook_model('././models/fasttext/wiki.id.bin').wv
model_pakai = Word2Vec.load(
    '././models/word2vec/idwiki/idwiki_word2vec_200_new_lower.model').wv


quran_clean_text = get_quran_indo_clean_text()


def fetch(verse_ids):
    output = []
    for id in verse_ids:
        url = f"http://localhost:8000/api/lexical/verse-in-quran/{id}"
        headers = {'content-type': 'application/json'}
        results = get(url, headers=headers)
        results = results.json()
        output.append(results['data'])
    return output



def semantikSearch(query):

    results = search_by_sentence(query, model_pakai, get_verse_max_score)
    # kata = search_by_word(query, model_pakai, get_verse_max_score)
    # kata = search_similar_word(query, model_pakai)
    kata = search_similar_word_with_scores(query, model_pakai)
    # Fixing: TypeError(Object of type float32 is not JSON serializable)
    for idx, (score, verse_id, verse) in enumerate(results):
        tmp = (float(score), verse_id, verse)
        results[idx] = tmp

    print(kata)

    results = [verse_id+1 for score, verse_id, verse in results]
    # results = fetch(results)

    return {'length': len(results), 'data': results, 'kata': kata}
