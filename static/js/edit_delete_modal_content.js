const deleteModal = new bootstrap.Modal(document.getElementById("deleteModal"));
const deletePostButtons = document.getElementsByClassName("delete-post-button");
const deleteCommentButtons = document.getElementsByClassName("delete-comment-button");
const deleteConfirm = document.getElementById("deleteConfirm");
const deleteModalLabel = document.getElementById("deleteModalLabel");
const deleteModalBody = document.getElementById("deleteModalBody");

for (let button of deletePostButtons) {
  button.addEventListener("click", (e) => {
    updateModal(e, "post")
    deleteModal.show();
  });
}

for (let button of deleteCommentButtons) {
  button.addEventListener("click", (e) => {
    updateModal(e, "comment")
    deleteModal.show();
  });
}

function updateModal(e, contentType) {
  let content_id = `${contentType}_id`
  let contentId = e.target.getAttribute(content_id);
  deleteModalLabel.innerText = `Delete ${contentType}?`
  deleteModalBody.innerText = `Are you sure you want to delete your ${contentType}? This action cannot be undone.`
  deleteConfirm.href = `/delete-${contentType}/${contentId}`;
}