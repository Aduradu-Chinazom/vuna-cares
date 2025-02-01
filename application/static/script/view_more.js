document.addEventListener("DOMContentLoaded", () => {
  try {
      const officeData = sessionStorage.getItem("selectedOffice");
      const office = officeData ? JSON.parse(officeData) : null;

      if (office && typeof office === "object") {
          document.querySelector(".head_text").textContent = office.name;
          document.querySelector(".view_img").src = office.image;
          document.querySelector(".name").textContent = office.head || "Unknown Head";
      } else {
          alert("Office data not found!");
          window.location.href = "/";
      }
  } catch (error) {
      console.error("Error retrieving office data:", error);
      alert("An error occurred while loading the office details.");
      window.location.href = "/";
  }
});

const send = document.getElementById("send");

if (send) {
  send.addEventListener("click", (event) => {
      event.preventDefault();

      const name = document.getElementById("name").value.trim();
      const matric = document.getElementById("matric_number").value.trim();
      const message = document.getElementById("message").value.trim();

      if (!name || !matric || !message) {
          alert("Please fill in all fields before sending!");
          return;
      }

      try {
          let messages = localStorage.getItem("messages");
          messages = messages ? JSON.parse(messages) : [];

          const officeData = sessionStorage.getItem("selectedOffice");
          const office = officeData ? JSON.parse(officeData) : {};

          const newMessage = {
              name: name,
              matric: matric,
              message: message,
              office_name: office.name || "Unknown Office",
              office_phone: office.phone || "No Phone Available",
          };

          messages.push(newMessage);
          localStorage.setItem("messages", JSON.stringify(messages));
          window.location.href = "/success";
      } catch (error) {
          console.error("Error saving message:", error);
          alert("An error occurred while sending the message. Please try again.");
      }
  });
} else {
  console.warn("Send button not found on the page.");
}
