let view_btns = document.getElementsByClassName("view_btn");

for (let i = 0; i < view_btns.length; i++) {
  view_btns[i].onclick = function () {
    window.location.href = "/view_more";
  };
}
