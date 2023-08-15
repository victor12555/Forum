from sqlalchemy import Column,Integer,String,DateTime,ForeignKey,Text,MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.orm import relationship
from datetime import datetime
from time import sleep
from comunidadeimpressionadora import login_manager
from flask_login import UserMixin

Base = declarative_base()

metadata = MetaData()

@login_manager.user_loader
def load_usuario(id_usuario):
    return session.get(Usuario,id_usuario)


class Usuario(Base,UserMixin):
    __tablename__ = 'usuario'
    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    senha = Column(String, nullable=False)
    foto_perfil = Column(String, default='default.jpg')
    posts = relationship('Post', backref='autor', lazy=True)
    cursos = Column(String, nullable=False, default='Não informado')

    def contar_posts(self):
        return len(self.posts)


class Post(Base):
    __tablename__ = 'post'
    id = Column(Integer, primary_key=True)
    titulo = Column(String, nullable=False)
    corpo = Column(Text, nullable=False)
    data_criacao = Column(DateTime, nullable=False, default=datetime.utcnow)
    id_usuario = Column(Integer, ForeignKey('usuario.id'), nullable=False)

sleep(5)
engine = create_engine("sqlite:///comunidadeimpressionadora//site.db")
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()
# novo_usuario = Usuario(username="Lira",email="Lira@gmail.com",senha="123456")
# novo_usuario2 = Usuario(username="Joao",email="joao@gmail.com1",senha="123456")
# novo_usuario3 = Usuario(username="Victor",email="alvesvictor125@gmail.com",senha="123456")
# session.add(novo_usuario)
# session.add(novo_usuario2)
# session.add(novo_usuario3)
# session.commit()
# session.close()
