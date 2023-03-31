const openModalBtn = document.getElementById('addUser');
const closeModalBtn = document.getElementById('userModalClose');
const modal = document.getElementById('userModal');
const modalWrapper = document.getElementById('userModalWrapper');
const modalContent = document.getElementById('userModalContent');

function addShowHideModal() {
  openModalBtn.onclick = function(event) {
    modal.style.display = "block";
    // console.log("Modal shown");
  }

  window.onclick = function(event) {
    // Close the modal if the backdrop is clicked
    // Excluding button prevents an open and immediate close when clicking 
    target = event.target;

    // console.log(event.target);
    if (
      target == modal | target == closeModalBtn | target == modalWrapper && 
      target != openModalBtn && modal.style.display != "none"
    ) {
      modal.style.display = "none";

      // console.log("Modal hidden");
    }
  }
}
