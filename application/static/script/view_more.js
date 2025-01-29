document.addEventListener("DOMContentLoaded", () => {
  let send = document.getElementById("send");

  send.addEventListener("click", (event) => {
    event.preventDefault();

    const name = document.getElementById("name").value.trim();
    const matric = document.getElementById("matric_number").value.trim();
    const message = document.getElementById("message").value.trim();

    if (!name || !matric || !message) {
      alert("Please fill in all fields before sending!");
      return;
    }

    let messages = localStorage.getItem("messages");
    messages = messages ? JSON.parse(messages) : [];

    const newMessage = {
      name: name,
      matric: matric,
      message: message,
      timestamp: new Date().toLocaleString(),
    };

    messages.push(newMessage);

    localStorage.setItem("messages", JSON.stringify(messages));
   
    window.location.href = "/success"; 
  });
});
