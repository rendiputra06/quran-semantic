# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from apps.home import blueprint
from flask import render_template, request, jsonify, json
from flask_login import login_required, current_user
from jinja2 import TemplateNotFound
from apps.home.models import db, Category, Ayat, Surat, Evaluation


@blueprint.route('/index')
# @login_required
def index():

    categories = Category.query.all()
    # print(categories)
    print(current_user)
    if(current_user.is_authenticated ):
        print('saya sudah login')
        return render_template('crud/index.html', segment='index')
    else:
        # Ambil parameter "view" dari URL (default-nya 'default')
        view = request.args.get('view', 'default')
        if view == 'default' :
            return render_template('crud/versi_1.html', segment='index')
        elif view == 'v2' :
            return render_template('crud/versi_2.html', segment='index')
        elif view == 'v3' :
            return render_template('crud/versi_3.html', segment='index')
        elif view == 'table' :
            return render_template('crud/table.html', segment='index')
        elif view == 'ontologi' :
            return render_template('crud/ontologi.html', segment='index')
        print('saya tidak login')


@blueprint.route('/kategori')
@login_required
def kategori():
    categories = Category.query.all()
    return render_template('crud/kategori.html', categories=categories)


@blueprint.route('/view_kategori/', methods=['GET'])
def api_kategori():
    categories = Category.query.filter_by(parent_id=None).all()
    categories_list = []
    for category in categories:
        categories_list.append([category.id, category.name])
    return jsonify(records=categories_list)


@blueprint.route('/edit_kategori/', methods=['GET'])
def edit_kategori():
    category_id = request.args.get('id')
    category = Category.query.get(category_id)
    if category:
        parent_id = category.parent_id if category.parent_id else None
        category_data = [category.id, category.name, parent_id]
    else:
        category_data = "Kategori tidak ditemukan"
    return jsonify(records=category_data)


@blueprint.route('/add_kategori/', methods=['POST'])
def add_kategori():
    if request.method == "POST":
        mode = request.form['mode']
        if mode == 'add':
            msg = None
            name = request.form['name']
            parent_id = request.form.get('parent_id') or None
            new_category = Category(name=name, parent_id=parent_id)
            db.session.add(new_category)
            db.session.commit()
            msg = "Record successfully added."
            return jsonify(msg=msg)
        elif mode == 'update':
            msg = None
            category_id = request.form['id']
            category = Category.query.get(category_id)
            if category:
                category.name = request.form['name']
                category.parent_id = request.form.get('parent_id')
                db.session.commit()
                msg = "Record successfully updated."
            else:
                msg = "Kategori tidak ditemukan"
            return jsonify(msg=msg)


@blueprint.route('/delete_kategori/', methods=['POST'])
def delete_kategori():
    msg = None
    try:
        category_id = request.form['id']
        category = Category.query.get(category_id)
        if category:
            # Cek apakah ada data yang memakai category ini sebagai parent_id
            subcategories = Category.query.filter_by(
                parent_id=category_id).all()
            if subcategories:
                msg = "Tidak bisa menghapus kategori karena ada subkategori yang terkait."
            else:
                db.session.delete(category)
                db.session.commit()
                msg = "Record successfully deleted."
        else:
            msg = "Kategori tidak ditemukan"
    except Exception as e:
        db.session.rollback()
        msg = "Error occurred: " + str(e)
    finally:
        return jsonify(msg=msg)


@blueprint.route('/view_subkategori/', methods=['GET'])
def view_subkategori():
    parent_id = request.args.get('parent_id')
    subcategories = Category.query.filter_by(parent_id=parent_id).all()
    subcategories_list = []

    if subcategories:
        for subcategory in subcategories:
            subcategories_list.append([subcategory.id, subcategory.name])
    else:
        parent_category = Category.query.get(parent_id)
        if parent_category and parent_category.list_ayat:
            list_ayat = json.loads(parent_category.list_ayat)
            return jsonify(records=list_ayat, ayat=True)

    return jsonify(records=subcategories_list)

@blueprint.route('/view_ayat/', methods=['GET'])
def view_ayat():
    value = request.args.get('value')
    
    if value:
        try:
            # Parsing value in the format Qs.1:11
            surah_num, ayat_num = value.split(':')
            surah_num = surah_num.replace('Qs.', '').strip()
            ayat_num = ayat_num.strip()
            
            ayat = Ayat.query.filter_by(surah_id=surah_num, nomor_di_surah=ayat_num).first()
            
            if ayat:
                surah = Surat.query.filter_by(id=ayat.surah_id).first()
                ayat_data = {
                    'nomor_ayat': ayat.nomor_ayat,
                    'surah_id': ayat.surah_id,
                    'isi_ayat': ayat.isi_ayat,
                    'ayat_indo': ayat.ayat_indo,
                    'nomor_di_surah': ayat.nomor_di_surah,
                    'nomor_di_alquran': ayat.nomor_di_alquran,
                    'surah_nama' : surah.nama,
                    'surah_nama_latin' : surah.nama_latin
                }
                return jsonify(records=[ayat_data])
            else:
                return jsonify(records=[]), 404
        
        except Exception as e:
            return jsonify(error=str(e)), 400
    return jsonify(records=[]), 400

# Endpoint untuk mendapatkan semua evaluasi
def serialize_evaluation(evaluation):
    return {
        'id': evaluation.id,
        'query': evaluation.query,
        'tipe': evaluation.tipe,
        'precision': evaluation.precision_final,
        'recall': evaluation.recall_final,
        'f1_score': evaluation.f1_score_final,
        'map': evaluation.map,
        'ndcg': evaluation.ndcg
    }

@blueprint.route('/index/get_evaluations', methods=['GET'])
def get_evaluations():
    evaluations = db.session.query(Evaluation).all()
    serialized = [serialize_evaluation(evaluation) for evaluation in evaluations]
    return jsonify(serialized)

# Endpoint untuk menghapus satu evaluasi berdasarkan ID
@blueprint.route('/index/delete_evaluation/<int:id>', methods=['DELETE'])
def delete_evaluation(id):
    # evaluation = Evaluation.query.get(id)
    evaluation = db.session.query(Evaluation).get(id)
    if not evaluation:
        return jsonify({'message': 'Evaluation not found'}), 404

    db.session.delete(evaluation)
    db.session.commit()
    return jsonify({'message': 'Evaluation deleted successfully'})

# Endpoint untuk menghapus beberapa evaluasi berdasarkan ID
@blueprint.route('/index/delete_selected', methods=['POST'])
def delete_selected():
    data = request.get_json()
    ids = data.get('ids', [])

    if not ids:
        return jsonify({'message': 'No IDs provided'}), 400

    evaluations = db.session.query(Evaluation).filter(Evaluation.id.in_(ids)).all()
    if not evaluations:
        return jsonify({'message': 'No evaluations found for the given IDs'}), 404

    for evaluation in evaluations:
        db.session.delete(evaluation)
    db.session.commit()

    return jsonify({'message': f'{len(evaluations)} evaluations deleted successfully'})

@blueprint.route('/<template>')
@login_required
def route_template(template):
    print('i still running the template')
    try:

        if not template.endswith('.html'):
            template += '.html'

        # Detect the current page
        segment = get_segment(request)

        # Serve the file (if exists) from app/templates/home/FILE.html
        return render_template("home/" + template, segment=segment)

    except TemplateNotFound:
        return render_template('home/page-404.html'), 404

    except:
        return render_template('home/page-500.html'), 500


# Helper - Extract current page name from request
def get_segment(request):

    try:

        segment = request.path.split('/')[-1]

        if segment == '':
            segment = 'index'

        return segment

    except:
        return None
