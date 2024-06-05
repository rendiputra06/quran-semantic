from apps.search import blueprint
from flask import render_template, request, jsonify, json
from flask_login import login_required
from jinja2 import TemplateNotFound
from apps.home.models import db, Category, Ayat, Surat
from sqlalchemy import or_
from prediksi import semantikSearch

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
                'halaman': ayat.Ayat.halaman,
                'kuarterHizb': ayat.Ayat.kuarterHizb,
                'juz': ayat.Ayat.juz,
                'surah_id': ayat.Ayat.surah_id,
                'isi_ayat': ayat.Ayat.isi_ayat,
                'isi_ayat_tanpa_tashkeel': ayat.Ayat.isi_ayat_tanpa_tashkeel,
                'ayat_indo': ayat.Ayat.ayat_indo,
                'nomor_di_surah': ayat.Ayat.nomor_di_surah,
                'nomor_di_alquran': ayat.Ayat.nomor_di_alquran,
                'sajda': ayat.Ayat.sajda,
                'surah_nama': ayat.Surat.nama,
                'surah_nama_latin': ayat.Surat.nama_latin,
                'surah_nama_tanpa_tashkeel': ayat.Surat.nama_tanpa_tashkeel
            }
            for ayat in verses
        ]

        return jsonify({'length': len(data), 'data': data})

    except Exception as e:
        return jsonify(error=str(e)), 400

# @blueprint.route('/api/semantik/<words>', methods=['GET'])
# def semantik(words):
