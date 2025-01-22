document.addEventListener("DOMContentLoaded", () => {
  const office = JSON.parse(sessionStorage.getItem("selectedOffice"));

  if (office) {
    document.querySelector(".head_text").textContent = office.name;
    document.querySelector(".view_img").src = office.image;
    document.querySelector(".name").textContent = office.head;
  } else {
    alert("Office data not found!");
    window.location.href = "/";
  }
});

let send = document.getElementById("send");

  view_btns.onclick = function () {
    window.location.href = "/success";
  };
