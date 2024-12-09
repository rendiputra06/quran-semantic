import pandas as pd
import json
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

# Setup database connection and model
Base = declarative_base()
engine = create_engine('sqlite:///../../apps/db.sqlite3')
Session = sessionmaker(bind=engine)
session = Session()


class Category(Base):
    __tablename__ = 'category'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    parent_id = Column(Integer, ForeignKey('category.id'), nullable=True)
    children = relationship('Category', backref='parent', remote_side=[id])
    list_ayat = Column(Text, nullable=True)  # Menambahkan field list_ayat

    def __repr__(self):
        return f'<Category {self.name}>'

# Base.metadata.create_all(engine)


def excel_to_hierarchy_db(file_path, sheet_name):
    # Membaca seluruh sheet dari file Excel
    df = pd.read_excel(file_path, sheet_name=sheet_name, header=None)

    # Membuat sub-dataframe yang dimulai dari kolom B dan melewati dua baris pertama
    df = df.iloc[2:, 1:]

    ayat_data = {}

    def build_hierarchy(df, parent_main_id):
        def add_children(df, parent_row, level, parent_id):
            if level > 5:
                return
            i = parent_row + 1
            while i < len(df) and pd.isna(df.iloc[i, level - 1]):
                if pd.notna(df.iloc[i, level]):
                    name = df.iloc[i, level]
                    child = Category(name=name, parent_id=parent_id)
                    session.add(child)
                    session.flush()  # Menyimpan child untuk mendapatkan id
                    ayat_data[child.id] = extract_special_data(i, child.id)
                    add_children(df, i, level + 1, child.id)
                i += 1

        i = 0
        while i < len(df):
            if pd.notna(df.iloc[i, 0]):
                name = df.iloc[i, 0]
                root = Category(name=name, parent_id=parent_main_id)
                session.add(root)
                session.flush()  # Menyimpan root untuk mendapatkan id
                add_children(df, i, 1, root.id)
            i += 1
        session.commit()

    def extract_special_data(posisi, id):
        special_data = []
        row = df.iloc[posisi]
        for col in range(6, len(row)):  # Mulai dari kolom ketujuh (index 6)
            if pd.notna(row[col]):
                special_data.append(row[col])
                print('baris dengan id = ', id, 'memiliki data', row[col])
        return special_data

    # Build hierarchy from DataFrame
    build_hierarchy(df, 8)

    # Update list_ayat in database
    for node_id, ayat_list in ayat_data.items():
        category = session.get(Category, node_id)
        if category:
            if ayat_list:
                category.list_ayat = json.dumps(ayat_list)
            else:
                category.list_ayat = None
    session.commit()


# Contoh penggunaan
excel_to_hierarchy_db('../indeks-quran-tercanggih.xls',
                      "MAKANAN & MINUMAN")
