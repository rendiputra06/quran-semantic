from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship

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
    children = relationship('Category', backref='parent', remote_side=[id], cascade='all,delete')

    def __repr__(self):
        return f'<Category {self.name}>'

Base.metadata.create_all(engine)

def delete_all_except_one():
    try:
        category_id_to_keep = int(input("Masukkan ID kategori yang ingin Anda pertahankan: "))
    except ValueError:
        print("ID kategori harus berupa angka.")
        return

    session.query(Category).filter(Category.id != category_id_to_keep).delete()
    session.commit()

# Contoh penggunaan untuk menghapus semua kategori kecuali satu ID tertentu
delete_all_except_one()