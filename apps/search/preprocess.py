import nltk, re
import string
import pandas as pd

# Define function to preprocess text
# jalankan secara manual di command line
nltk.download('punkt')
nltk.download('stopwords')
stop_words = set(nltk.corpus.stopwords.words('indonesian'))

def clean(text):
    '''
    Membersihkan teks dengan menghapus karakter yang tidak diperlukan, tanda baca,
    dan mengubah semua huruf menjadi huruf kecil.

    @param text: teks yang akan dibersihkan
    @type text: str
    @return: teks yang telah dibersihkan
    @rtype: list of str
    '''
    # Menghapus angka dan karakter khusus
    text = re.sub(r'\d+', '', text)
    text = re.sub(r'[{}]'.format(re.escape(string.punctuation)), '', text)

    # Mengubah semua huruf menjadi huruf kecil
    text = text.lower()

    # Tokenize teks menjadi kata-kata
    words = text.split()

    # Menghapus kata-kata yang pendek (opsional)
    words = [word for word in words if len(word) > 1]

    return words

def preprocess(text):
    # Remove special characters and digits
    text = re.sub(r'[^\w\s]', '', text)
    text = re.sub(r'\d+', '', text)
    tokens = nltk.word_tokenize(text)
    stemmed_tokens = [nltk.stem.PorterStemmer().stem(token) for token in tokens]
    filtered_tokens = [token for token in stemmed_tokens if token not in stop_words]
    return filtered_tokens

def get_quran_indo_clean_text():
    df = pd.read_csv('./data/external/alquran-data.csv')
    # Preprocess text in Tanzil dataset
    return df['text'].apply(preprocess)
