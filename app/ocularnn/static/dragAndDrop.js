/* Drag and drop functionality with files requires use of event handler functions
 * for the drop and dragover events. drag events hold a read-only attribute
 * called dataTransfer. This holds the drag event's data through a DataTransfer
 * object. Each DataTransfer object contains a list of DataTransferItems, which
 * represents our files. We can use this to parse through dragged files when they 
 * are placed in the drop zone. */

const preview = document.getElementById('uploadPreview');

function previewImage(files) {
  /* Allows for the display of a thumbnail of the image uploaded by the user*/
  for (let i = 0; i < files.length; i++) {
    const file = files[i];

    const img = document.createElement('img');
    img.classList.add("obj");
    img.file = file;

    preview.appendChild(img);

    const reader = new FileReader();
    reader.onload = (function(uploadedImg) {
      return function(event) {uploadedImg.src = event.target.result; }; })(img);

    reader.readAsDataURL(file);
  }

}

function dropHandler(event) {
  /* This function triggers when files have been dropped to the drop zone. This
   * will be used to process the data from the drag event */

  // prevents default browser behaviour which is to open the file in a new tab
  event.preventDefault(); 
  const dt = event.dataTransfer;
  let dtItems = dt.items;
  const files = [];

  if (dt != null) {
    for (let i = 0; i < Math.min(2, dtItems.length); i++) {
      if (dtItems[i].kind == "file") {
        const f = dtItems[i].getAsFile();

        // Only add files if they are of type image
        if (f.type.startsWith('image/')) {
          files.push(f);
        }
      }
    }
  }
  previewImage(files);
}

function dragOverHandler(event) {
  event.preventDefault();
}
