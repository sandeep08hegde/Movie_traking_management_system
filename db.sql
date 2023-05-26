create table rating(
    bluff_val INTEGER PRIMARY KEY
);
create table completed(
    movie_id varchar(20),
    movie_name varchar(500),
    user_rating INTEGER,
    date_of_completion date,
    author varchar(120),
    FOREIGN KEY(user_rating) REFERENCES rating(bluff_val)
);

create table favorites(
    movie_id VARCHAR(20),
    movie_name varchar(500),
    user_rating INTEGER,
    author varchar(120),
    FOREIGN KEY(user_rating) REFERENCES rating(bluff_val) 
);

create table plan_to_watch(
    movie_id VARCHAR(20),
    movie_name varchar(500),
    author varchar(120)
);

create table genre(
    genre_id VARCHAR(10) primary key,
    avail_genre VARCHAR(20)
);

create table my_fav_genre(
    genre_id varchar(10),
    foreign key(genre_id) REFERENCES genre(genre_id),
    user_genre VARCHAR(20),
    author varchar(120)
);

insertion statements

INSERT INTO rating values(1);
INSERT INTO rating values(2);
INSERT INTO rating values(3);
INSERT INTO rating values(4);
INSERT INTO rating values(5);


