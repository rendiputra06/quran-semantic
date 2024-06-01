from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship

# Setup database connection and model
Base = declarative_base()
engine = create_engine('sqlite:///../../apps/db.sqlite')
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

def delete_category_and_children(category_id):
    category = session.query(Category).get(category_id)
    if category:
        session.delete(category)
        session.commit()
    else:
        print(f"Category with ID {category_id} not found.")

# Contoh penggunaan untuk menghapus entri dengan ID tertentu
delete_category_and_children(5)
