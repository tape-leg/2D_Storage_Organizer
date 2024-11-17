const DropArea = document.getElementById("drop-area");
const inputFile = document.getElementById("input-file");
const imageView = document.getElementById("img-view");

inputFile.addEventListener("change", uploadImage);

function uploadImage(){
    let imgLink = URL.createObjectURL(inputFile.files[0]);
    imageView.style.backgroundImage = `url(${imgLink})`;
    imageView.textContent = "";
    imageView.style.border = 0;

}
DropArea.addEventListener("dragover", function(e){
    e.preventDefault();
});
DropArea.addEventListener("dragover", function(e){
    e.preventDefault();
    inputFile.files = e.dataTransfer.files;
    
});