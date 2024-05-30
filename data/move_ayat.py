import sqlite3
import pandas as pd

# Menghubungkan ke database Quran lama
quran_db = sqlite3.connect('quran.db')
quran_cr = quran_db.cursor()


# Path ke file Excel dengan data translate Al-Quran Bahasa Indonesia
excel_file_path = 'quran_indo.xlsx'

# Baca file Excel
df = pd.read_excel(excel_file_path)

# for i in range(1, 6237):
for i in range(1, 6237):
    id = i
    excel = df.iloc[id - 1]
    # Ambil data dari tabel lama (verses)
    quran_cr.execute(f'SELECT * FROM verses WHERE id == {id}')
    row = quran_cr.fetchone()

    if row:
        page = row[2]
        hizb_quarter = row[3]
        juz = row[4]
        surah = row[5]
        verse = row[6]
        verse_without_tashkeel = row[7]
        number_in_surah = row[8]
        number_in_quran = row[9]
        sajda = row[13]
        ayat_indo = excel[4]
        # page, hizb_quarter, juz, surah, verse, verse_without_tashkeel, number_in_surah, number_in_quran, sajda = row
        verse_pk = f'S{str(surah).zfill(3)}V{str(number_in_surah).zfill(3)}'

        django_db = sqlite3.connect('../apps/db.sqlite3')
        cr = django_db.cursor()
        cr.execute(
            '''INSERT INTO ayat
            (nomor_ayat, halaman, kuarterHizb, juz, surah_id, isi_ayat, isi_ayat_tanpa_tashkeel, ayat_indo, nomor_di_surah, nomor_di_alquran, sajda) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
            (verse_pk, page, hizb_quarter, juz, surah, verse, verse_without_tashkeel,
             ayat_indo, number_in_surah, number_in_quran, sajda)
        )

        django_db.commit()

        print('=' * 50)
        print(verse_pk, '|', page, '|', hizb_quarter, '|', ayat_indo)
        # print(verse_pk, '|', page, '|', hizb_quarter, '|', juz, '|', surah, '|', verse, '|', verse_without_tashkeel, '|', number_in_surah, '|', number_in_quran, '|', sajda)

# Tutup koneksi ke database Quran lama
quran_db.close()
