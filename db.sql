set sql_safe_updates=0;

create database navermovie;
use navermovie;
create table movie(
   moviecode integer,
   title_movie varchar(100),
    movie_rate varchar(100),
    audience_rate varchar(50),
    audience_count varchar(50),
    netizen_rate varchar(50),
    netizen_count varchar(50),
    journalist_rate varchar(50),
    journalist_count varchar(50),
    totalaudience varchar(50),
    playing_time varchar(50),
    opening_date varchar(50),
    image_movie varchar(100),
    enter_date datetime default now(),
    primary key (moviecode)
);
select count(*) from movie;

create table genre(
   moviecode integer not null,
   genre_movie varchar(20),
   primary key (genre_movie, moviecode),
   foreign key (moviecode) references movie(moviecode)
);   
select * from genre;

create table country(
   moviecode integer not null,
   country_movie varchar(20),
    primary key (country_movie, moviecode),
    foreign key (moviecode) references movie(moviecode)
);
select * from country;

create table director(
   directorcode integer not null,
    moviecode integer not null,
    name_director varchar(50),
    image_director varchar(500),
    primary key(directorcode, moviecode),
    foreign key (moviecode) references movie(moviecode)
);
select * from director;

create table actor(
   actorcode varchar(50),
    moviecode integer not null,
    name_actor varchar(50),
    image_actor varchar(500),
    primary key(actorcode, moviecode),
    foreign key (moviecode) references movie(moviecode)
);
select * from actor;
#insert into actor(actorcode,moviecode,name_actor,image_actor)
#values ('7184', 191613, '놈 맥도널드', 'https://search.pstatic.net/common/?src=http%3A%2F%2Fimgmovie.naver.net%2Fmdi%2Fpi%2F000000071%2FPM7184_162330_000.jpg&type=u111_139&quality=95');

create table review(
   reviewkey integer auto_increment,
    moviecode integer not null,
    title_review varchar(100),
    writer_review varchar(30),
    makingdate_review varchar(30),
    hits varchar(10),
    content text,
    primary key(reviewkey, moviecode),
    foreign key (moviecode) references movie(moviecode)
);
select * from review;

create table photo(
   photokey integer auto_increment,
   moviecode integer not null,
   image_photo varchar(500),
   primary key(photokey, moviecode),
   foreign key (moviecode) references movie(moviecode)
);
select * from photo;

create table line(
   linekey integer auto_increment,
   moviecode integer not null,
   image_line varchar(500), /*명대사 사진*/
   bestline text, /*명대사 대사*/
   part_line varchar(30), /*명대사 극중 이름personaName*/
   name_line varchar(30), /*명대사 배우 이름actorName*/
   writer_line varchar(30), /*작성자*/
   likecnt varchar(10), /*추천수*/
   makingdate_line varchar(30), /*작성 날짜*/
   primary key(linekey, moviecode),
   foreign key (moviecode) references movie(moviecode)
);
select * from line;

create table persona(
   personakey integer auto_increment,
    moviecode integer not null,
    image_persona varchar(500),
    star varchar(10),
    name_persona varchar(30),   
    part_persona varchar(30),
    primary key(personakey,moviecode),
    foreign key (moviecode) references movie(moviecode)
);
select * from persona;

create index idx_genre_movie on genre(genre_movie, moviecode);
create index idx_aname_movie on actor(name_actor, moviecode);
create index idx_dname_movie on director(name_director, moviecode);
create index idx_title on movie(title_movie);