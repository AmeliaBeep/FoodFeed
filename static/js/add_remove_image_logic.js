/**
 * Adds event listeners relating to the confirmation of 
 * profile image deletion.
 * 
 * First the delete_image_toggle checkbox input is updated
 * so checking it reveals a confirm deletion modal.
 * 
 * Then the 'Undo Removal' button is updated, so that 
 * clicking it unchecks the delete_image_toggle input. 
 */
let removeImageInput = document.querySelector('#delete_image_toggle');
const deleteModal = new bootstrap.Modal(document.getElementById("deleteModal"));
const deleteUndoButton = document.getElementById("deleteUndo");

removeImageInput.addEventListener("click", (e) => {
    if (e.target.checked == true) {
        deleteModal.show();
    };
});

deleteUndoButton.addEventListener("click", () => {
    let removeImageInput = document.querySelector('#delete_image_toggle');
    removeImageInput.checked = false;
    deleteModal.hide()
});