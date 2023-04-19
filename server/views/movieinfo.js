let moviecode;

/**/
const main_score = document.querySelector(".main-score");
const movie_name = document.querySelector(".movie_name");
const poster = document.querySelector(".poster");
const step1 = document.querySelector(".step1");
const step2 = document.querySelector(".step2");
const step3 = document.querySelector(".step3");
const step4 = document.querySelector(".step4");
const actorPane = document.querySelector(".actorPane");
const photoPane = document.querySelector(".wrapper");
const reviewList = document.querySelector(".reviewList");
const review_count = document.querySelector(".review_count");
const lineList = document.querySelector(".lineList");
/**/

window.onload = function () {
  getMovieData();
};

function init() {}

const getMovieData = async () => {
  const movies = getMovie();
  const actors = getActor();
  const photos = getPhoto();
  const reviews = getReview();
  const lines = getLine();
};

const getMovie = async () => {
  try {
    if (localStorage.getItem("moviecode")) {
      moviecode = localStorage.getItem("moviecode");
    }

    return axios({
      method: "get",
      url: `http://localhost:8000/movie/${moviecode}`,
    })
      .then((res) => {
        //title
        movie_name.innerText = `${res.data[0].title_movie}`;
        //image
        poster.setAttribute("src", `${res.data[0].image_movie}`);
        //socreboard
        const main_score_h3_1 = document.createElement("h3");
        main_score_h3_1.innerText = `관람객`;
        const main_score1 = document.createElement("div");
        main_score1.innerText = `${Math.ceil(res.data[0].audience_rate)}`;
        const main_score_h3_2 = document.createElement("h3");
        main_score_h3_2.innerText = `기자/평론가`;
        const main_score2 = document.createElement("div");
        main_score2.innerText = `${Math.ceil(res.data[0].journalist_rate)}`;
        const main_score_h3_3 = document.createElement("h3");
        main_score_h3_3.innerText = `네티즌`;
        const main_score3 = document.createElement("div");
        main_score3.innerText = `${Math.ceil(res.data[0].netizen_rate)}`;

        main_score.appendChild(main_score_h3_1);
        main_score.appendChild(main_score1);
        main_score.appendChild(main_score_h3_2);
        main_score.appendChild(main_score2);
        main_score.appendChild(main_score_h3_3);
        main_score.appendChild(main_score3);
        //info-spec
        let str = "";
        if (res.data.length < 3) {
        } else {
          for (let i = 0; i < 3; i++) {
            if (res.data[i].genre_movie === null) {
              break;
            }
            if (i === 0) {
              str += res.data[i].genre_movie;
            } else {
              str += `, ${res.data[i].genre_movie}`;
            }
          }
        }
        const info_spec_step1_span1 = document.createElement("span");
        info_spec_step1_span1.innerText = `${str} | `;
        const info_spec_step1_span2 = document.createElement("span");
        info_spec_step1_span2.innerText = ` ${res.data[0].country_movie} |`;
        const info_spec_step1_span3 = document.createElement("span");
        info_spec_step1_span3.innerText = ` ${res.data[0].playing_time} |`;
        const info_spec_step1_span4 = document.createElement("span");
        info_spec_step1_span4.innerText = ` ${res.data[0].opening_date}`;
        step1.appendChild(info_spec_step1_span1);
        step1.appendChild(info_spec_step1_span2);
        step1.appendChild(info_spec_step1_span3);
        step1.appendChild(info_spec_step1_span4);

        step2.innerText = `${res.data[0].name_director}`;

        str = "";
        let first = "";
        let check = "";
        for (let i = 0; i < res.data.length; i++) {
          if (res.data[i].name_actor === null) {
            break;
          }
          if (i !== 0 && res.data[i].name_actor === first) {
            break;
          }
          if (i !== 0 && check === res.data[i].name_actor) {
          } else {
            if (i === 0) {
              str += res.data[i].name_actor;
              check = res.data[i].name_actor;
              first = res.data[i].name_actor;
            } else {
              str += `, ${res.data[i].name_actor}`;
              check = res.data[i].name_actor;
            }
          }
        }
        step3.innerText = `${str}`;
        step4.innerText = `${res.data[0].movie_rate}`;
      })
      .catch((err) => {
        console.error(err);
      });
  } catch (error) {
    console.error(error);
  }
};

const getActor = async () => {
  try {
    if (localStorage.getItem("moviecode")) {
      moviecode = localStorage.getItem("moviecode");
    }

    return axios({
      method: "get",
      url: `http://localhost:8000/movie/${moviecode}/actor`,
    })
      .then((res) => {
        //배우 표시
        for (let i = 0; i < res.data.length; i++) {
          if (res.data[i].name_actor === null) {
            break;
          }
          const actorInfo = document.createElement("div");
          actorInfo.style.float = "left";
          actorInfo.style.width = "440px";
          actorInfo.style.margin = "20px 0";

          const actorImg = document.createElement("img");
          actorImg.setAttribute("src", `${res.data[i].image_actor}`);
          actorInfo.appendChild(actorImg);

          const actorName = document.createElement("h3");
          actorName.innerText = `${res.data[i].name_actor}`;
          actorInfo.appendChild(actorName);

          actorPane.appendChild(actorInfo);
        }
      })
      .catch((err) => {
        console.error(err);
      });
  } catch (error) {
    console.error(error);
  }
};
const getPhoto = async () => {
  try {
    if (localStorage.getItem("moviecode")) {
      moviecode = localStorage.getItem("moviecode");
    }
    return axios({
      method: "get",
      url: `http://localhost:8000/movie/${moviecode}/photo`,
    })
      .then((res) => {
        //포토
        for (let i = 0; i < res.data.length; i++) {
          if (res.data[i].length === null) {
            break;
          }
          const img = document.createElement("img");
          img.setAttribute("src", `${res.data[i].image_photo}`);
          img.style.padding = "10px";
          photoPane.appendChild(img);
        }
      })
      .catch((err) => {
        console.error(err);
      });
  } catch (error) {
    console.error(error);
  }
};
const getReview = async () => {
  try {
    if (localStorage.getItem("moviecode")) {
      moviecode = localStorage.getItem("moviecode");
    }

    return axios({
      method: "get",
      url: `http://localhost:8000/movie/${moviecode}/review`,
    })
      .then((res) => {
        //리뷰
        console.log(res.data[0]);
        review_count.innerText = res.data[0].reviewkey;
        for (let i = 0; i < res.data.length; i++) {
          if (res.data[i].title_review === null) {
            break;
          }
          const li = document.createElement("li");
          const review_title = document.createElement("div");
          review_title.style.marginBottom = "10px";
          const review_span = document.createElement("span");
          review_span.innerText = `${res.data[i].title_review}`;
          review_span.style.fontSize = "20px";
          review_title.appendChild(review_span);

          const review_right = document.createElement("div");
          review_right.style.float = "right";
          review_right.style.display = "inline";
          review_right.style.marginRight = "10px";
          const review_right_span1 = document.createElement("span");
          review_right_span1.innerText = `${res.data[i].writer_review} |`;
          review_right_span1.style.fontSize = "10px";
          const review_right_span2 = document.createElement("span");
          review_right_span2.innerText = ` ${res.data[i].makingdate_review} | `;
          review_right_span2.style.fontSize = "10px";
          const review_right_span3 = document.createElement("span");
          review_right_span3.innerText = `${res.data[i].hits}`;
          review_right_span3.style.fontSize = "10px";
          review_right.appendChild(review_right_span1);
          review_right.appendChild(review_right_span2);
          review_right.appendChild(review_right_span3);
          review_title.appendChild(review_right);

          const review_text = document.createElement("div");
          review_text.innerText = `${res.data[0].content}`;
          li.appendChild(review_title);
          li.appendChild(review_text);
          reviewList.appendChild(li);
        }
      })
      .catch((err) => {
        console.error(err);
      });
  } catch (error) {
    console.error(error);
  }
};
const getLine = async () => {
  try {
    if (localStorage.getItem("moviecode")) {
      moviecode = localStorage.getItem("moviecode");
    }

    return axios({
      method: "get",
      url: `http://localhost:8000/movie/${moviecode}/line`,
    })
      .then((res) => {
        //명대사
        for (let i = 0; i < res.data.length; i++) {
          if (res.data[i].bestline === null) {
            break;
          }
          const li = document.createElement("li");
          const lineList_div = document.createElement("div");
          const lineImg = document.createElement("img");
          lineImg.setAttribute("src", `${res.data[i].image_line}`);
          lineImg.style.float = "left";
          lineImg.style.marginRight = "20px";
          lineList_div.appendChild(lineImg);
          const line_title = document.createElement("h4");
          lineList_div.appendChild(line_title);
          line_title.innerText = `${res.data[i].bestline}`;
          const div1 = document.createElement("div");
          div1.style.marginBottom = "20px;";
          const lineSpan1 = document.createElement("span");
          lineSpan1.innerText = `${res.data[i].part_line} | `;
          const lineSpan2 = document.createElement("span");
          lineSpan2.innerText = `${res.data[i].name_line}`;
          div1.appendChild(lineSpan1);
          div1.appendChild(lineSpan2);
          lineList_div.appendChild(div1);

          const line_right = document.createElement("div");
          line_right.style.float = "right";
          line_right.style.display = "inline";
          line_right.style.marginRight = "10px";
          const right_span1 = document.createElement("span");
          right_span1.innerText = `${res.data[i].writer_line} | `;
          right_span1.style.fontSize = "10px";
          const right_span2 = document.createElement("span");
          right_span2.innerText = `${res.data[i].makingdate_line} | `;
          right_span2.style.fontSize = "10px";
          const right_span3 = document.createElement("span");
          right_span3.innerText = `${res.data[i].likecnt}`;
          right_span3.style.fontSize = "10px";
          line_right.appendChild(right_span1);
          line_right.appendChild(right_span2);
          line_right.appendChild(right_span3);
          li.appendChild(lineList_div);
          li.appendChild(line_right);
          lineList.appendChild(li);
        }
      })
      .catch((err) => {
        console.error(err);
      });
  } catch (error) {
    console.error(error);
  }
};
