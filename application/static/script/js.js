const predefinedOffices = [
  {
    id: "1",
    name: "Office of the VC",
    head: "Rev. Fr. Prof. Hycinth E Ichoku",
    phone: "09160937525",
    image: "/static/images/vice_chancellor.jpg",  },
  {
    id: "2",
    name: "Office of the Registrar",
    head: "Dr. Stella Chizoba Okonkwo",
    phone: "09160937525",
    image: "{{ url_for('static', filename='images/registrar.png') }}",
  },
  {
    id: "3",
    name: "Office of the Deputy VC",
    head: "Rev. Prof. Sasa Micheal Sunday",
    phone: "09160937525",
    image: "{{ url_for('static', filename='images/sasa.jpg') }}",
  },
  {
    id: "4",
    name: "Office of the Bursar",
    head: "Mrs. Margaret Ejima Akoje",
    phone: "09160937525",
    image: "{{ url_for('static', filename='images/bursar.jpg') }}",
  },
  {
    id: "5",
    name: "Office of the SRA",
    head: "SRA",
    phone: "09160937525",
    image: "{{ url_for('static', filename='images/Sra.jpeg') }}",
  },
];


function initializeOffices() {
  if (!localStorage.getItem("offices")) {
    localStorage.setItem("offices", JSON.stringify(predefinedOffices));
  }
}

function getOffices() {
  const offices = localStorage.getItem("offices");
  return offices ? JSON.parse(offices) : [];
}

function renderOffices() {
  const officeContainer = document.querySelector(".offices");
  officeContainer.innerHTML = ""; 

  const offices = getOffices();
  offices.forEach((office) => {
    const officeItem = document.createElement("div");
    officeItem.className = "office";

    officeItem.innerHTML = `
      <img src="${office.image}" alt="${office.name}" />
      <div class="office_info">
        <span>${office.head}</span>
        <p>${office.name}</p>
      </div>
      <div class="view">
        <button onclick="viewOfficeDetails('${office.id}')">View more</button>
      </div>
    `;

    officeContainer.appendChild(officeItem);
  });
}

function viewOfficeDetails(officeId) {
  const offices = getOffices();
  const office = offices.find((o) => o.id === officeId);

  if (office) {
    sessionStorage.setItem("selectedOffice", JSON.stringify(office));
    window.location.href = "/view_more";
  }
}


initializeOffices();
renderOffices();

