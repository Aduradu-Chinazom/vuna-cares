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

send.addEventListener("click", (event) => {
  event.preventDefault();

  const nameBox = document.getElementById("name");
  const matricBox = document.getElementById("matric_number");
  const messageBox = document.getElementById("message");

  const name = nameBox.value.trim();
  const matric = matricBox.value.trim();
  const message = messageBox.value.trim();

  if (!name || !matric || !message) {
      alert("Please fill in all fields before sending!");
  } else {
      window.location.href = "/success";
  }
});
