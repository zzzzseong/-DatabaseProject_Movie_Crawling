const express = require("express");
const app = express();
const mysql = require("mysql");
const path = require("path");
const PORT = 8000;

const db = mysql.createConnection({
  host: "localhost",
  user: "root",
  password: "11111111",
  database: "navermovie",
});
db.connect((err) => {
  if (err) return console.log(err.message);
});

app.set("views", path.join(__dirname, "views"));
app.set("view engine", "html");
app.engine("html", require("ejs").renderFile);

app.use(express.json());
app.use(express.static(path.join(__dirname, "views")));
app.use(express.urlencoded({ extended: true }));

app.get("/", (req, res) => {
  res.render("main");
});

/* API 시작*/

// 영화를 눌렀을 때 해당 영화에 대한 자세한 정보를 가져오기
app.get("/movie/:moviecode", (req, res) => {
  console.log(req.params.moviecode);
  let query =
    "SELECT m.title_movie, g.genre_movie, m.movie_rate, m.image_movie, m.audience_rate, m.journalist_rate, m.netizen_rate, c.country_movie, m.playing_time, m.opening_date, d.name_director, a.name_actor FROM movie AS m, genre AS g, country AS c, director AS d, actor AS a WHERE m.moviecode=g.moviecode AND m.moviecode=c.moviecode AND m.moviecode=d.moviecode AND m.moviecode=a.moviecode AND m.moviecode=?";
  db.query(query, [req.params.moviecode], (err, results) => {
    if (err) console.error(err);
    if (results[0] === undefined) {
      query =
        "SELECT m.title_movie, g.genre_movie, m.movie_rate, m.image_movie, m.audience_rate, m.journalist_rate, m.netizen_rate, c.country_movie, m.playing_time, m.opening_date, d.name_director FROM movie AS m, genre AS g, country AS c, director AS d WHERE m.moviecode=g.moviecode AND m.moviecode=c.moviecode AND m.moviecode=d.moviecode AND m.moviecode=?";
      db.query(query, [req.params.moviecode], (err2, results2) => {
        if (err2) console.error(err2);
        res.send(results2);
      });
    } else {
      res.send(results);
    }
  });
});

app.get("/movie/:moviecode/actor", (req, res) => {
  let query =
    "SELECT a.image_actor, a.name_actor FROM movie AS m, actor AS a WHERE m.moviecode=a.moviecode AND m.moviecode=?";
  db.query(query, [req.params.moviecode], (err, results) => {
    if (err) console.error(err);
    res.send(results);
  });
});

app.get("/movie/:moviecode/photo", (req, res) => {
  let query =
    "SELECT p.image_photo FROM movie AS m, photo AS p WHERE m.moviecode=p.moviecode AND m.moviecode=?";
  db.query(query, [req.params.moviecode], (err, results) => {
    if (err) console.error(err);
    res.send(results);
  });
});

app.get("/movie/:moviecode/review", (req, res) => {
  let query =
    "SELECT r.reviewkey, r.title_review, r.writer_review, r.makingdate_review, r.hits, r.content FROM movie AS m, review AS r WHERE m.moviecode=r.moviecode AND m.moviecode=?";
  db.query(query, [req.params.moviecode], (err, results) => {
    if (err) console.error(err);
    //console.log(results);
    res.send(results);
  });
});

app.get("/movie/:moviecode/line", (req, res) => {
  let query =
    "SELECT l.image_line, l.bestline, l.part_line, l.name_line, l.writer_line, l.makingdate_line, l.likecnt FROM movie AS m, line AS l WHERE m.moviecode=l.moviecode AND m.moviecode=?";
  db.query(query, [req.params.moviecode], (err, results) => {
    if (err) console.error(err);
    res.send(results);
  });
});

// 장르를 선택하고 검색했을 때 영화 목록들을 ㄱㄴㄷ(abc) 순으로 order해서 10개씩 출력
app.get("/genre/:genre/:page/:sort", (req, res) => {
  let query = "";
  if (req.params.sort === "title_movie") {
    query = `SELECT * FROM movie AS m JOIN genre AS g ON m.moviecode=g.moviecode WHERE g.genre_movie like '%${req.params.genre}' or g.genre_movie like '%${req.params.genre}' or g.genre_movie like '%${req.params.genre}%' ORDER BY ${req.params.sort} LIMIT 10 OFFSET ?`;
  } else {
    query = `SELECT * FROM movie AS m JOIN genre AS g ON m.moviecode=g.moviecode WHERE g.genre_movie like '%${req.params.genre}' or g.genre_movie like '%${req.params.genre}' or g.genre_movie like '%${req.params.genre}%' ORDER BY ${req.params.sort} DESC LIMIT 10 OFFSET ?`;
  }
  db.query(query, [(req.params.page - 1) * 10], (err, results) => {
    if (err) console.error(err);
    //console.log(req.params.sort);
    res.send(results);
  });
});

// 감독을 선택하고 검색했을 때 영화 목록들 ㄱㄴㄷ(abc) 순으로 order해서 10개씩 출력
app.get("/director/:name_director/:page/:sort", (req, res) => {
  let query = "";
  if (req.params.sort === "title_movie") {
    query = `SELECT * FROM movie AS m JOIN director AS d ON m.moviecode=d.moviecode WHERE d.name_director like '%${req.params.name_director}' or d.name_director like '%${req.params.name_director}' or d.name_director like '%${req.params.name_director}%' ORDER BY ${req.params.sort} LIMIT 10 OFFSET ?`;
  } else {
    query = `SELECT * FROM movie AS m JOIN director AS d ON m.moviecode=d.moviecode WHERE d.name_director like '%${req.params.name_director}' or d.name_director like '%${req.params.name_director}' or d.name_director like '%${req.params.name_director}%' ORDER BY DESC ${req.params.sort} LIMIT 10 OFFSET ?`;
  }
  db.query(query, [(req.params.page - 1) * 10], (err, results) => {
    if (err) console.error(err);
    //console.log(results);
    res.send(results);
  });
});

// 배우를 선택하고 검색했을 때 영화 목록들 ㄱㄴㄷ(abc) 순으로 order해서 10개씩 출력
app.get("/actor/:name_actor/:page/:sort", (req, res) => {
  let query = "";
  if (req.params.sort === "title_movie") {
    query = `SELECT * FROM movie AS m JOIN actor AS a ON m.moviecode=a.moviecode WHERE a.name_actor like '%${req.params.name_actor}' or a.name_actor like '%${req.params.name_actor}' or a.name_actor like '%${req.params.name_actor}%' ORDER BY ${req.params.sort} LIMIT 10 OFFSET ?`;
  } else {
    query = `SELECT * FROM movie AS m JOIN actor AS a ON m.moviecode=a.moviecode WHERE a.name_actor like '%${req.params.name_actor}' or a.name_actor like '%${req.params.name_actor}' or a.name_actor like '%${req.params.name_actor}%' ORDER BY ${req.params.sort} DESC LIMIT 10 OFFSET ?`;
  }
  db.query(query, [(req.params.page - 1) * 10], (err, results) => {
    if (err) console.error(err);
    //console.log(results);
    res.send(results);
  });
});

// 제목을 선택하고 검색했을 때 영화 목록들 ㄱㄴㄷ(abc) 순으로 order해서 10개씩 출력
app.get("/title/:title/:page/:sort", (req, res) => {
  let query = "";
  if (req.params.sort === "title_movie") {
    query = `SELECT * FROM movie WHERE title_movie like '%${req.params.title}' or title_movie like '%${req.params.title}' or title_movie like '%${req.params.title}%' ORDER BY ${req.params.sort} LIMIT 10 OFFSET ?`;
  } else {
    query = `SELECT * FROM movie WHERE title_movie like '%${req.params.title}' or title_movie like '%${req.params.title}' or title_movie like '%${req.params.title}%' ORDER BY ${req.params.sort} DESC LIMIT 10 OFFSET ?`;
  }
  db.query(query, [(req.params.page - 1) * 10], (err, results) => {
    if (err) console.error(err);
    //console.log(results);
    res.send(results);
  });
});

// 국가를 선택하고 검색했을 때 영화 목록들 ㄱㄴㄷ(abc) 순으로 order해서 10개씩 출력
app.get("/country/:country/:page/:sort", (req, res) => {
  let query = "";
  if (req.params.sort === "title_movie") {
    query = `SELECT * FROM movie AS m JOIN country AS c ON m.moviecode=c.moviecode WHERE c.country_movie like '%${req.params.country}' or c.country_movie like '%${req.params.country}' or c.country_movie like '%${req.params.country}%' ORDER BY ${req.params.sort} LIMIT 10 OFFSET ?`;
  } else {
    query = `SELECT * FROM movie AS m JOIN country AS c ON m.moviecode=c.moviecode WHERE c.country_movie like '%${req.params.country}' or c.country_movie like '%${req.params.country}' or c.country_movie like '%${req.params.country}%' ORDER BY ${req.params.sort} DESC LIMIT 10 OFFSET ?`;
  }

  db.query(query, [(req.params.page - 1) * 10], (err, results) => {
    if (err) console.error(err);
    console.log(results);
    res.send(results);
  });
});

/* API 끝*/

app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT} `);
});
