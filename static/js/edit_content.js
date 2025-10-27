// const editButtons = document.getElementsByClassName("btn-edit");
// const commentText = document.getElementById("id_body");
// const commentForm = document.getElementById("commentForm");
// const submitButton = document.getElementById("submitButton");

const deleteModal = new bootstrap.Modal(document.getElementById("deleteModal"));
const deletePostButtons = document.getElementsByClassName("delete-post-button");
const deleteCommentButtons = document.getElementsByClassName("delete-comment-button");
const deleteConfirm = document.getElementById("deleteConfirm");
const deleteModalLabel = document.getElementById("deleteModalLabel");
const deleteModalBody = document.getElementById("deleteModalBody");

/**
* Initializes edit functionality for the provided edit buttons.
* 
* For each button in the `editButtons` collection:
* - Retrieves the associated comment's ID upon click.
* - Fetches the content of the corresponding comment.
* - Populates the `commentText` input/textarea with the comment's content for editing.
* - Updates the submit button's text to "Update".
* - Sets the form's action attribute to the `edit_comment/{commentId}` endpoint.
*
for (let button of editButtons) {
  button.addEventListener("click", (e) => {
    let commentId = e.target.getAttribute("comment_id");
    let commentContent = document.getElementById(`comment${commentId}`).innerText;
    commentText.value = commentContent;
    submitButton.innerText = "Update";
    commentForm.setAttribute("action", `edit_comment/${commentId}`);
  });
}
*/

/**
* Initializes deletion functionality for the provided delete buttons.
* 
* For each button in the `deleteButtons` collection:
* - Retrieves the associated comment's ID upon click.
* - Updates the `deleteConfirm` link's href to point to the 
* deletion endpoint for the specific comment.
* - Displays a confirmation modal (`deleteModal`) to prompt 
* the user for confirmation before deletion.
*/

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
  deleteConfirm.href = `delete-${contentType}/${contentId}`;
}