
const predefinedOffices = [
  {
      id: "1",
      name: "Office of the VC",
      head: "Rev. Fr. Prof. Hycinth E Ichoku",
      phone: "09160937525",
      image: "/static/images/vice_chancellor.jpg",
  },
  {
      id: "2",
      name: "Office of the Registrar",
      head: "Dr. Stella Chizoba Okonkwo",
      phone: "09160937525",
      image: "/static/images/registrar.png",
  },
  {
      id: "3",
      name: "Office of the Deputy VC",
      head: "Rev. Prof. Sasa Micheal Sunday",
      phone: "09160937525",
      image: "/static/images/sasa.jpg",
  },
  {
      id: "4",
      name: "Office of the Bursar",
      head: "Mrs. Margaret Ejima Akoje",
      phone: "09160937525",
      image: "/static/images/bursar.jpg",
  },
  {
      id: "5",
      name: "Office of the SRA",
      head: "SRA",
      phone: "09160937525",
      image: "/static/images/Sra.jpeg",
  },
];

function initializeOffices() {
  try {
      if (!localStorage.getItem("offices")) {
          localStorage.setItem("offices", JSON.stringify(predefinedOffices));
      }
  } catch (error) {
      console.error("Error initializing offices in localStorage:", error);
  }
}

function getOffices() {
  try {
      const offices = localStorage.getItem("offices");
      return offices ? JSON.parse(offices) : [];
  } catch (error) {
      console.error("Error retrieving offices from localStorage:", error);
      return [];
  }
}

function createOfficeElement(office) {
  const officeItem = document.createElement("div");
  officeItem.className = "office";

  officeItem.innerHTML = `
      <img src="${office.image}" alt="${office.name}" class="office-img" />
      <div class="office_info">
          <span>${office.head}</span>
          <p>${office.name}</p>
      </div>
      <div class="view">
          <button data-office-id="${office.id}">Send Message</button>
      </div>
  `;

  return officeItem;
}

function attachOfficeButtonListeners() {
  const buttons = document.querySelectorAll(".office button");
  buttons.forEach((button) => {
      button.addEventListener("click", (event) => {
          const officeId = event.target.getAttribute("data-office-id");
          viewOfficeDetails(officeId);
      });
  });
}

function renderOffices() {
  const officeContainer = document.querySelector(".offices");
  if (!officeContainer) {
      console.error("Office container not found!");
      return;
  }

  officeContainer.innerHTML = ""; // Clear existing content

  const offices = getOffices();
  offices.forEach((office) => {
      const officeItem = createOfficeElement(office);
      officeContainer.appendChild(officeItem);
  });

  attachOfficeButtonListeners();
}

function viewOfficeDetails(officeId) {
  try {
      const offices = getOffices();
      const office = offices.find((o) => o.id === officeId);

      if (office) {
          const officeQuery = encodeURIComponent(JSON.stringify(office));
          window.location.href = `/send_msg?office=${officeQuery}`;
      } else {
          console.error("Office not found:", officeId);
          alert("Office not found. Please try again.");
      }
  } catch (error) {
      console.error("Error viewing office details:", error);
      alert("An error occurred. Please try again.");
  }
}



// Initialize and render offices
console.log("Offices Data from Local Storage:", getOffices());
localStorage.removeItem("offices");
console.log("Offices Data from Local Storage:", getOffices());
initializeOffices();
renderOffices();