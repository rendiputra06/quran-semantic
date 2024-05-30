# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from apps.home import blueprint
from flask import render_template, request, jsonify
from flask_login import login_required
from jinja2 import TemplateNotFound
from apps.home.models import db, Category, Ayat


@blueprint.route('/index')
@login_required
def index():

    categories = Category.query.all()
    print(categories)
    return render_template('crud/index.html', segment='index')


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
        category_data = [category.id, category.name, category.parent_id]
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
    for subcategory in subcategories:
        subcategories_list.append([subcategory.id, subcategory.name])
    return jsonify(records=subcategories_list)


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
