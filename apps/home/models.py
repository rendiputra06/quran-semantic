from apps import db


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    parent_id = db.Column(db.Integer, db.ForeignKey(
        'category.id'), nullable=True)
    children = db.relationship(
        'Category', backref=db.backref('parent', remote_side=[id]))

    def __repr__(self):
        return f'<Category {self.name}>'


class Surat(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nama = db.Column(db.String(100), nullable=False)
    nama_latin = db.Column(db.String(100), nullable=False)
    nama_tanpa_tashkeel = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<Surat {self.nama}>'


class Ayat(db.Model):
    nomor_ayat = db.Column(db.String, primary_key=True)
    halaman = db.Column(db.Integer, nullable=False)
    kuarterHizb = db.Column(db.Integer, nullable=False)
    juz = db.Column(db.Integer, nullable=False)
    surah_id = db.Column(db.Integer, db.ForeignKey('surat.id'), nullable=False)
    isi_ayat = db.Column(db.Text, nullable=False)
    isi_ayat_tanpa_tashkeel = db.Column(db.Text, nullable=False)
    ayat_indo = db.Column(db.Text, nullable=False)
    nomor_di_surah = db.Column(db.Integer, nullable=False)
    nomor_di_alquran = db.Column(db.Integer, nullable=False)
    sajda = db.Column(db.Boolean, nullable=False)

    def __repr__(self):
        return f'<SearchAyat {self.nomor_ayat}>'
