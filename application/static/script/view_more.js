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

  const messageBox = document.getElementById("message");
  const message = messageBox.value.trim();
  if (message) {
      window.location.href = "/success";
  } else {
      alert("Please fill in the message box before sending!");
  }
});
