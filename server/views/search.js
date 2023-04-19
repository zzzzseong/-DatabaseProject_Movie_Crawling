const form = document.querySelector(".js-searchForm");
const input = form.querySelector("input");
const select = form.querySelector("select");
const movieList = document.querySelector(".js-movieList");
const result = document.querySelector(".js-result");

const page = document.querySelector(".page");
const sForm = document.querySelector(".js-sortForm");
const sButton = document.querySelector(".sortButton");
const sSelect = sForm.querySelector("select");

const prev = document.querySelector(".prev");
const next = document.querySelector(".next");

var word = "";
var pageCount;
let sortKey = "title_movie";

function handleSubmit(event) {
  event.preventDefault();
  if (!input.value) {
    return alert("please input keyword");
  }
  pageCount = 1;
  const option = select.querySelector("option:checked");
  result.innerText = `${input.value}(${option.value})에 대한 영화 검색 결과입니다.`;

  page.style.display = "block";
  sForm.style.display = "block";

  if (option.value === "제목") {
    word = "title";
  } else if (option.value === "배우") {
    word = "actor";
  } else if (option.value === "감독") {
    word = "director";
  } else if (option.value === "장르") {
    word = "genre";
  } else {
    word = "country";
  }
  getMovieData(1);
  initHandelPage();
}

const getMovieData = async (num) => {
  const movies = getMovies(num);
};
const getMovies = async (num) => {
  try {
    return axios({
      method: "get",
      url: `http://localhost:8000/${word}/${input.value}/${num}/${sortKey}`, //search option - search input - page number
    })
      .then((res) => {
        while (movieList.hasChildNodes()) {
          movieList.removeChild(movieList.firstChild);
        }
        for (let i = 0; i < res.data.length; i++) {
          const li = document.createElement("li");
          const img = document.createElement("img");
          img.setAttribute("src", `${res.data[i].image_movie}`); //추가
          img.style.float = "left";
          img.style.height = "100px";
          img.style.marginRight = "20px";
          const div = document.createElement("div");
          const a = document.createElement("a");
          a.innerText = `${res.data[i].title_movie}`;
          a.addEventListener("click", function () {
            localStorage.setItem("moviecode", res.data[i].moviecode);
            location.href = "./movieinfo.html";
          });
          a.style.fontSize = "22px";
          div.style.marginBottom = "20px";
          div.appendChild(a);

          const div2 = document.createElement("div");
          const div3 = document.createElement("div");
          div2.innerText = `제작년도: ${res.data[i].opening_date}`;
          div2.style.marginBottom = "10px";
          div3.innerText = `평점: ${res.data[i].audience_rate}`; //추가

          li.appendChild(img);
          li.appendChild(div);
          li.appendChild(div2);
          li.appendChild(div3);
          movieList.appendChild(li);
        }
      })
      .catch((err) => {
        console.error(err);
      });
  } catch (error) {
    console.error(error);
  }
};

function initHandelPage() {
  prev.addEventListener("click", function () {
    if (pageCount === 1) {
      return 0;
    } else {
      getMovieData(--pageCount);
    }
  });
  next.addEventListener("click", function () {
    getMovieData(++pageCount);
  });
}

function sortSubmit() {
  const sort = sSelect.querySelector("option:checked");
  if (sort.value === "가나다 정렬") {
    sortKey = "title_movie";
    pageCount = 1;
    getMovieData(pageCount);
  }
  if (sort.value === "년도 정렬") {
    sortKey = "opening_date";
    pageCount = 1;
    getMovieData(pageCount);
  }
  if (sort.value === "평점 정렬") {
    sortKey = "audience_rate";
    pageCount = 1;
    getMovieData(pageCount);
  }
}

function init() {
  form.addEventListener("submit", handleSubmit);
  sButton.addEventListener("click", sortSubmit);
}

init();
