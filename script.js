const form = document.querySelector("form"),
  fileInput = document.querySelector(".file-input"),
  progressArea = document.querySelector(".progress-area"),
  uploadedArea = document.querySelector(".uploaded-area");
(arxivLinkInput = document.getElementById("arxivLink")),
  (resultDiv = document.getElementById("result"));
const fileUploader = document.getElementById("file-uploader");
const fileUploader1 = document.getElementById("file-uploader1");
const linkVerifier = document.getElementById("link-verifier");
const switchToFileUploaderButton = document.getElementById(
  "switch-to-file-uploader"
);
const switchToLinkVerifierButton = document.getElementById(
  "switch-to-link-verifier"
);

form.addEventListener("click", () => {
  fileInput.click();
});
switchToLinkVerifierButton.addEventListener("click", () => {
  fileUploader.classList.add("inactive-section");
  fileUploader.classList.remove("active-section");
  fileUploader1.classList.add("inactive-section");
  fileUploader1.classList.remove("active-section");
  linkVerifier.classList.add("active-section");
  linkVerifier.classList.remove("inactive-section");
});

switchToFileUploaderButton.addEventListener("click", () => {
  linkVerifier.classList.add("inactive-section");
  linkVerifier.classList.remove("active-section");
  fileUploader.classList.add("active-section");
  fileUploader.classList.remove("inactive-section");
  fileUploader1.classList.add("active-section");
  fileUploader1.classList.remove("inactive-section");
});

function submission() {
  form.action = "http://127.0.0.1:8000/extract-text";
  form.submit();
}

fileInput.onchange = ({ target }) => {
  let file = target.files[0];
  if (file) {
    let fileName = file.name;
    if (fileName.length >= 12) {
      let splitName = fileName.split(".");
      fileName = splitName[0].substring(0, 13) + "... ." + splitName[1];
    }
    uploadFile(fileName);
  }
};

function uploadFile(name) {
  let xhr = new XMLHttpRequest();
  xhr.open("POST", "php/upload.php");
  xhr.upload.addEventListener("progress", ({ loaded, total }) => {
    let fileLoaded = Math.floor((loaded / total) * 100);
    let fileTotal = Math.floor(total / 1000);
    let fileSize;
    fileTotal < 1024
      ? (fileSize = fileTotal + " KB")
      : (fileSize = (loaded / (1024 * 1024)).toFixed(2) + " MB");
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
    if (loaded == total) {
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
    window.location.href = "http://127.0.0.1:8000/get_data_from_url";
  } else {
    // Invalid arXiv link
    resultDiv.innerHTML =
      '<p id="error">Invalid arXiv link. Please provide a valid link.</p>';
  }
}

const form1 = document.getElementById("check");
const userInputField = document.getElementById("arxivLink");

form1.addEventListener("submit", (event) => {
  const userInput = userInputField.value.trim(); // Trim extra spaces

  // Validate user input if necessary (e.g., check for invalid characters)

  // Determine the appropriate action URL based on user input

  // Set the form's action attribute to the chosen URL
  form1.action =
    "http://127.0.0.1:8000/get_data_from_url?arxiv_url=" + userInput;

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

// Get all the image elements
const images = document.querySelectorAll(".image-container img");

// Loop through each image and add a click event listener
images.forEach((image) => {
  image.addEventListener("click", function () {
    // Get the image number from its id
    const imageNumber = image.id.replace("image", "");

    // Update the path based on the clicked image
    const newPath = `theme/theme${imageNumber}.pptx`;

    // Now you can use `newPath` in your code
    console.log(newPath);

    // For demonstration, I'll assume you want to load the new presentation here
    // You can replace this with your actual code to load the PPTX
    loadPresentation(newPath);
  });
});

function loadPresentation(path) {
  // Here you can put your code to load the presentation
  // For example:
  // prs = pptx.Presentation(path);
  console.log("Loading presentation from:", path);
}

let currentImageIndex = 0;
const folderPath = "imagecheck/"; // Path to your "slides" folder
const imageArray = [];
let numImages = 0;

// Fetch the images from the folder
function fetchImages() {
  fetch(folderPath)
    .then((response) => response.text())
    .then((data) => {
      // Count the number of image files
      const imageFiles = data.match(
        /<a href="([^"]+\.(?:jpg|jpeg|png|gif))"/gi
      );
      numImages = imageFiles ? imageFiles.length : 0;

      // Use the count here or call a function passing the count
      console.log("Number of images:", numImages);

      // Once we have the count, populate the images array
      for (let i = 1; i <= numImages; i++) {
        imageArray.push(`${folderPath}Slide_${i}.jpg`);
      }

      // Show the first image initially
      showImage(0);
    })
    .catch((error) => {
      console.error("Error fetching images:", error);
    });
}
fetchImages();

const sliderImage = document.getElementById("slider-image");

function showImage(index) {
  if (index < 0) {
    currentImageIndex = imageArray.length - 1;
  } else if (index >= imageArray.length) {
    currentImageIndex = 0;
  } else {
    currentImageIndex = index;
  }

  sliderImage.src = imageArray[currentImageIndex];
}

function nextImage() {
  showImage(currentImageIndex + 1);
}

function prevImage() {
  showImage(currentImageIndex - 1);
}

