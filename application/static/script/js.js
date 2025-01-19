let view_btns = document.getElementsByClassName("view_btn");

for (let i = 0; i < view_btns.length; i++) {
  view_btns[i].onclick = function () {
    window.location.href = "/view_more";
  };
}
document.querySelectorAll('.pages a').forEach(link => {
  link.addEventListener('click', event => {
      event.preventDefault();
      const targetId = link.getAttribute('href').substring(1);
      document.getElementById(targetId).scrollIntoView({ behavior: 'smooth' });
  });
});
