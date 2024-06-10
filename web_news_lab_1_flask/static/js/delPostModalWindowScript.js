let modalDelPostConfimWindow_varr = document.getElementById(
  "ModalDelPostConfimWindow"
);

let deleteButtons = document.querySelectorAll(".button.delete");

let modalDelPostConfimWindowConfirmBtn = document.getElementById("confirmBtn");
let modalDelPostConfimWindowConfirmBtnCancelBtn =
  document.getElementById("cancelBtn");

let modalDelPostConfimWindowSpan = document.getElementsByClassName("close")[0];

let postIdToDelete = null;

deleteButtons.forEach((button) => {
  button.onclick = function () {
    postIdToDelete = button.getAttribute("data-post-id");
    modalDelPostConfimWindow_varr.style.display = "block";
  };
});

modalDelPostConfimWindowSpan.onclick = function () {
  modalDelPostConfimWindow_varr.style.display = "none";
};

window.onclick = function (event) {
  if (event.target == modalDelPostConfimWindow_varr) {
    modalDelPostConfimWindow_varr.style.display = "none";
  }
};

modalDelPostConfimWindowConfirmBtn.onclick = function () {
  if (postIdToDelete) {
    //  запит POST на сервер для видалення поста
    fetch(`/post/delete/${postIdToDelete}`, {
      method: "POST",
    });

    modalDelPostConfimWindow_varr.style.display = "none";
  }
  window.location.reload();
};

modalDelPostConfimWindowConfirmBtnCancelBtn.onclick = function () {
  modalDelPostConfimWindow_varr.style.display = "none";
};
