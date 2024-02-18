const form = document.querySelector("form"),
fileInput = document.querySelector(".file-input"),
progressArea = document.querySelector(".progress-area"),
uploadedArea = document.querySelector(".uploaded-area");
arxivLinkInput = document.getElementById("arxivLink"),
resultDiv = document.getElementById("result");
form.addEventListener("click", () =>{
  fileInput.click();
});

fileInput.onchange = ({target})=>{
  let file = target.files[0];
  if(file){
    let fileName = file.name;
    if(fileName.length >= 12){
      let splitName = fileName.split('.');
      fileName = splitName[0].substring(0, 13) + "... ." + splitName[1];
    }
    uploadFile(fileName);
  }
}

function uploadFile(name){
  let xhr = new XMLHttpRequest();
  xhr.open("POST", "php/upload.php");
  xhr.upload.addEventListener("progress", ({loaded, total}) =>{
    let fileLoaded = Math.floor((loaded / total) * 100);
    let fileTotal = Math.floor(total / 1000);
    let fileSize;
    (fileTotal < 1024) ? fileSize = fileTotal + " KB" : fileSize = (loaded / (1024*1024)).toFixed(2) + " MB";
    let progressHTML = `<li class="row">
                          <i class="fas fa-file-alt"></i>
                          <div class="content">
                            <div class="details">
                              <span class="name">${name} • Uploading</span>
                              <span class="percent">${fileLoaded}%</span>
                            </div>
                            <div class="progress-bar">
                              <div class="progress" style="width: ${fileLoaded}%"></div>
                            </div>
                          </div>
                        </li>`;
    uploadedArea.classList.add("onprogress");
    progressArea.innerHTML = progressHTML;
    if(loaded == total){
      progressArea.innerHTML = "";
      let uploadedHTML = `<li class="row">
                            <div class="content upload">
                              <i class="fas fa-file-alt"></i>
                              <div class="details">
                                <span class="name">${name} • Uploaded</span>
                                <span class="size">${fileSize}</span>
                              </div>
                            </div>
                            <i class="fas fa-check"></i>
                          </li>`;
      uploadedArea.classList.remove("onprogress");
      uploadedArea.insertAdjacentHTML("afterbegin", uploadedHTML);
    }
  });
  let data = new FormData(form);
  xhr.send(data);
}

function validateLink() {
  var input = arxivLinkInput.value;

  // Regular expression to check if the input is a valid arXiv link
  var arxivRegex = /^https:\/\/arxiv\.org\/abs\/\d{4}\.\d{5}$/;

  if (arxivRegex.test(input)) {
    // Valid arXiv link
    resultDiv.innerHTML = '<p id="success">Valid arXiv link!</p>';

    // Redirect to the specified URL
    window.location.href = 'http://127.0.0.1:8000/get_data_from_url';
  } else {
    // Invalid arXiv link
    resultDiv.innerHTML = '<p id="error">Invalid arXiv link. Please provide a valid link.</p>';
  }
}









const form1 = document.getElementById('check');
const userInputField = document.getElementById('arxivLink');

form1.addEventListener('submit', (event) => {
  const userInput = userInputField.value.trim(); // Trim extra spaces

  // Validate user input if necessary (e.g., check for invalid characters)

  // Determine the appropriate action URL based on user input
 
   // Set the form's action attribute to the chosen URL
   form1.action = "http://127.0.0.1:8000/get_data_from_url?arxiv_url="+userInput;

   // Optionally, prevent default form submission to allow further processing
   // if needed (e.g., for AJAX requests)
   // event.preventDefault();
 });

//  function openNav() {
//   document.getElementById("mySidenav").style.width = "250px";
//   document.getElementById("main").style.marginLeft = "250px";
// }

// function closeNav() {
//   document.getElementById("mySidenav").style.width = "0";
//   document.getElementById("main").style.marginLeft= "0";
// }
function openNav() {
  document.getElementById("mySidenav").style.width = "100%"; // Set width to 100% to cover the whole webpage
  document.getElementById("mySidenav").style.height = "98vh"; // Set height to 90% of viewport height
}

function closeNav() {
  document.getElementById("mySidenav").style.width = "0"; // Set width to 0 to close the side navigation
}
