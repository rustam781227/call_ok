from sqlalchemy import UniqueConstraint, Column, String, Integer, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()
metadata = Base.metadata


class Playlist(Base):
    __tablename__ = 'playlist'
    __table_args__ = (
        UniqueConstraint('name', 'id_user'),
        {'schema': 'common', 'comment': 'Таблица хранения плейлистов'}
    )

    id_playlist = Column(Integer, primary_key=True)
    name = Column(String(128), nullable=False, comment='Название плейлиста')
    id_user = Column(Integer, nullable=False, comment='ИД пользователя, создавшего плейлист')

    songs = relationship('Song', secondary='common.songs_in_playlist')


class Song(Base):
    __tablename__ = 'songs'
    __table_args__ = {'schema': 'common', 'comment': 'Таблица для хранения песен'}

    id_song = Column(Integer, primary_key=True, comment='ИД Песни')
    name = Column(String(256), nullable=False, comment='Название песни')
    artist = Column(String(256), nullable=False, comment='Исполнитель')
    genre = Column(String(128), nullable=False, comment='Жанр')
    duration = Column(Integer, nullable=False, comment='Длительность')
    album = Column(String(256), nullable=False, comment='Альбом')


class User(Base):
    __tablename__ = 'users'
    __table_args__ = {'schema': 'common'}

    id_user = Column(Integer, primary_key=True, comment='ИД Пользователя')
    username = Column(String(128), nullable=False, unique=True, comment='Имя пользователя')
    password = Column(String(256), nullable=False, comment='Пароль')


class SongRating(Base):
    __tablename__ = 'song_rating'
    __table_args__ = {'schema': 'common', 'comment': 'Таблица для хранения рейтинга песен'}

    id_song_rating = Column(Integer, primary_key=True, comment='ИД рейтинга песни')
    id_song = Column(ForeignKey('common.songs.id_song', ondelete='CASCADE', onupdate='CASCADE'))
    rating = Column(Integer, nullable=False, comment='Рейтинг')
    id_user = Column(ForeignKey('common.users.id_user'), comment='Ид оценившего пользователя')

    user = relationship('User')


class SongInPlaylist(Base):
    __tablename__ = 'songs_in_playlist'
    __table_args__ = (
        UniqueConstraint('id_song', 'id_playlist'),
        {'schema': 'common', 'comment': 'Таблица для хранения песен в плейлистах'}
    )
    id_song_in_playlist = Column(Integer, primary_key=True, comment='ИД песни в плейлисте')
    id_song = Column(ForeignKey('common.songs.id_song'), nullable=False, comment='Ид песни')
    id_playlist = Column(ForeignKey('common.playlist.id_playlist'), nullable=False, comment='ИД Плейлиста')
