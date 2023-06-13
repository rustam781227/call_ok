create database music_storage;

comment on database music_storage is 'База данных для музыкального сервиса';

create schema common;

comment on schema common is 'Схема для хранения информации о песнях';



create table common.songs
(
    id_song  integer      not null
        constraint songs_pk
            primary key,
    name     varchar(256) not null,
    artist   varchar(256) not null,
    genre    varchar(128) not null,
    duration integer      not null,
    album varchar(256) not null
);

comment on table common.songs is 'Таблица для хранения песен';

comment on column common.songs.id_song is 'ИД Песни';

comment on column common.songs.name is 'Название песни';

comment on column common.songs.artist is 'Исполнитель';

comment on column common.songs.genre is 'Жанр';

comment on column common.songs.duration is 'Длительность';

comment on column common.songs.album is 'Альбом';

create table common.playlist
(
    id_playlist integer      not null
        constraint playlist_pk
            primary key,
    name        varchar(128) not null,
    id_user     integer      not null,
    constraint ak_playlist
        unique (name, id_user)
);

comment on table common.playlist is 'Таблица хранения плейлистов';

comment on column common.playlist.name is 'Название плейлиста';

comment on column common.playlist.id_user is 'ИД пользователя, создавшего плейлист';

create table common.songs_in_playlist
(
    id_song     integer not null,
    id_playlist integer not null,
    constraint ak_song_in_playlist
        unique (id_song, id_playlist),
    constraint fk_songs_in_playlist_ref_song
        foreign key (id_song) references common.songs (id_song),
       constraint fk_songs_in_playlist_ref_playlists
        foreign key (id_playlist) references common.playlist (id_playlist)
);

comment on table common.songs_in_playlist is 'Таблица для хранения песен в плейлистах';

comment on column common.songs_in_playlist.id_song is 'Ид песни';

comment on column common.songs_in_playlist.id_playlist is 'ИД Плейлиста';

create table common.users
(
    id_user     integer not null,
    username varchar(128) not null,
    password varchar(256) not null,
    constraint ak_user unique (username)
);

comment on column common.users.id_user is 'ИД Пользователя';

comment on column common.users.username is 'Имя пользователя';

comment on column common.users.password is 'Пароль';


create table common.song_rating
(
    id_song_rating integer not null
        constraint song_rating_pks
            primary key,
    rating         integer not null,
    id_user        integer,
    constraint fk_song_rating_ref_user
        foreign key (id_user) references common.users (id_user)
);

comment on table common.song_rating is 'Таблица для хранения рейтинга песен';

comment on column common.song_rating.id_song_rating is 'ИД рейтинга песни';

comment on column common.song_rating.rating is 'Рейтинг';

comment on column common.song_rating.id_user is 'Ид оценившего пользователя';

create sequence common.create_id_playlist minvalue 1;
alter table common.playlist alter column id_playlist set default nextval('common.create_id_playlist'::regclass);
create sequence common.create_id_song_rating minvalue 1;
alter table common.song_rating alter column id_song_rating set default nextval('common.create_id_song_rating'::regclass);
create sequence common.create_id_song minvalue 1;
alter table common.songs alter column id_song set default nextval('common.create_id_song'::regclass);
create sequence common.create_id_song_in_playlist minvalue 1;
alter table common.songs_in_playlist alter column id_song_in_playlist set default nextval('common.create_id_song_in_playlist'::regclass);
create sequence common.create_id_user minvalue 1;
alter table common.users alter column id_user set default nextval('common.create_id_user'::regclass)


alter table common.song_rating
    add id_song integer;

alter table common.song_rating
    add constraint fk_song_rating_ref_song
        foreign key (id_song) references common.songs
            on update cascade on delete cascade;

