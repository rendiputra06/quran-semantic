from apps.search import blueprint
from flask import render_template, request, jsonify, json
from flask_login import login_required
from jinja2 import TemplateNotFound
from apps.home.models import db, Category, Ayat, Surat
from sqlalchemy import or_
from apps.search.prediksi import semantikSearch


@blueprint.route('/search/')
# @login_required
def search():
    categories = Category.query.all()
    return render_template('search/search.html', categories=categories)


@blueprint.route('/api/cari/<words>', methods=['GET'])
def cari(words):
    """
    Search in verses using insensitive contains.
    Return all verses with given words and join with Surat table.
    """
    try:
        words = words.lower()  # Mengubah kata kunci pencarian menjadi huruf kecil
        search = "%{}%".format(words)

        # Join Ayat dengan Surat berdasarkan surah_id
        verses = db.session.query(Ayat, Surat).join(Surat, Ayat.surah_id == Surat.id).filter(
            or_(
                Ayat.isi_ayat.ilike(search),
                Ayat.isi_ayat_tanpa_tashkeel.ilike(search),
                Ayat.ayat_indo.ilike(search)
            )
        ).all()

        # Memformat data untuk JSON response
        data = [
            {
                'nomor_ayat': ayat.Ayat.nomor_ayat,
                'isi_ayat': ayat.Ayat.isi_ayat,
                'ayat_indo': ayat.Ayat.ayat_indo,
                'surah': ayat.Surat.nama,
                'nama_latin': ayat.Surat.nama_latin,
                'surah_id': ayat.Ayat.surah_id,
                'nomor_di_surah': ayat.Ayat.nomor_di_surah,
                'nomor_di_alquran': ayat.Ayat.nomor_di_alquran,
                'quran_format': convert_to_quran_format(ayat.Ayat.nomor_ayat),
                'breadcrumb': find_ayat_breadcrumb(ayat.Ayat.nomor_ayat)
            }
            for ayat in verses
        ]

        return jsonify({'length': len(data), 'data': data})

    except Exception as e:
        return jsonify(error=str(e)), 400


def convert_to_quran_format(input_string):
    """
    Mengubah format string input menjadi format "QS. x:y"
    """
    # Memisahkan nomor surat dan nomor ayat dari inputString
    surah_number = int(input_string[1:4])
    ayah_number = int(input_string[5:])

    # Membuat format "QS. x:y" dari nomor surat dan nomor ayat
    result = f"Qs.{surah_number}:{ayah_number}"

    return result


def find_ayat_breadcrumb(nomor_ayat):
    search_ayat = convert_to_quran_format(nomor_ayat)
    # Mencari semua kategori yang memiliki ayat tertentu
    categories = db.session.query(Category).filter(
        Category.list_ayat.contains(f'"{search_ayat}"')).all()
    results = []

    def get_parents(category):
        # Mengumpulkan breadcrumb dari kategori saat ini ke puncak
        breadcrumb = [category.name]
        while category.parent_id:
            # Mengambil objek Category berdasarkan parent_id
            category = db.session.query(Category).get(category.parent_id)
            breadcrumb.append(category.name)
        return ' > '.join(reversed(breadcrumb))

    # Mengumpulkan semua jalur hirarki untuk kategori yang ditemukan
    for category in categories:
        breadcrumb = get_parents(category)
        results.append(breadcrumb)

    return results


@blueprint.route('/api/semantik/<words>', methods=['GET'])
def semantik(words):
    try:
        result = semantikSearch(words)
        verse_ids = result['data']
        verses = db.session.query(Ayat, Surat).join(Surat, Ayat.surah_id == Surat.id).filter(
            Ayat.nomor_di_alquran.in_(verse_ids)).all()
        formatted_verses = [
            {
                'nomor_ayat': verse.Ayat.nomor_ayat,
                'isi_ayat': verse.Ayat.isi_ayat,
                'ayat_indo': verse.Ayat.ayat_indo,
                'surah': verse.Surat.nama,
                'nama_latin': verse.Surat.nama_latin,
                'surah_id': verse.Ayat.surah_id,
                'nomor_di_surah': verse.Ayat.nomor_di_surah,
                'nomor_di_alquran': verse.Ayat.nomor_di_alquran,
                'quran_format': convert_to_quran_format(verse.Ayat.nomor_ayat),
                'breadcrumb': find_ayat_breadcrumb(verse.Ayat.nomor_ayat)
            }
            for verse in verses
        ]
        result['data'] = formatted_verses
        return jsonify(result)
    except Exception as e:
        return jsonify(error=str(e)), 400
