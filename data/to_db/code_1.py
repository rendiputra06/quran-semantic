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


Base.metadata.create_all(engine)


def delete_hierarchy_by_id(category_id):
    def delete_category_and_children(category):
        for child in category.children:
            delete_category_and_children(child)
        session.delete(category)

    category_to_delete = session.query(Category).get(category_id)
    if category_to_delete:
        delete_category_and_children(category_to_delete)
        session.commit()


# Contoh penggunaan untuk menghapus data dengan ID tertentu
delete_hierarchy_by_id(3)
