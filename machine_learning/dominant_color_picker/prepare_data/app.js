const imageDirInput = document.getElementById("image-dir-input");
const imageSelectButtonContainer = document.getElementById(
  "image-select-button-container"
);
const currentImage = document.getElementById("current-image");

const colorForm = document.getElementById("color-form");
const primaryColorPicker = document.getElementById("primary-color-input");
const secondaryColorPicker = document.getElementById("secondary-color-input");
const accentColorPicker = document.getElementById("accent-color-input");
const saveButton = document.getElementById("save-button");
const exportButton = document.getElementById("export-button");

const mainContainer = document.getElementById("main-container");

// Variables
let images = [];
let displayImage = {
  image: null,
  index: null,
};
let selectedImageIndex = 0;

const defaultColor = "#ffffff";

let result = [];

// Event Listeners
imageDirInput.addEventListener("change", (e) => {
  const files = e.target.files;
  images = Array.from(files);

  if (images.length === 0) {
    saveButton.disabled = true;
    exportButton.disabled = true;
  } else {
    saveButton.disabled = false;
    exportButton.disabled = false;
  }

  displayImageSelectButtons();
  displayDefaultImage();
});

// Functions
const displayImageSelectButtons = () => {
  imageSelectButtonContainer.innerHTML = "";
  images.forEach((image, index) => {
    const imageSelectButton = document.createElement("button");
    const imageDisplay = document.createElement("img");

    imageDisplay.classList.add("aspect-square", "h-full", "object-cover");
    imageDisplay.src = URL.createObjectURL(image);

    imageSelectButton.appendChild(imageDisplay);
    imageSelectButton.className = `snap-start rounded aspect-square w-20 h-20`;

    if (index === selectedImageIndex) {
      imageSelectButton.classList.add("border-4", "border-blue-500");
    }

    imageSelectButton.addEventListener("click", () => {
      selectedImageIndex = index;
      updateSelectedImage();
      const reader = new FileReader();
      reader.onload = () => {
        currentImage.src = reader.result;
      };
      reader.readAsDataURL(image);
      updateColorPickers(image.name);
    });
    imageSelectButtonContainer.appendChild(imageSelectButton);
  });
};

const updateSelectedImage = () => {
  const buttons = imageSelectButtonContainer.querySelectorAll("button");
  buttons.forEach((button, index) => {
    if (index === selectedImageIndex) {
      button.classList.add("border-4", "border-blue-500");
    } else {
      button.classList.remove("border-4", "border-blue-500");
    }
  });
};

const displayDefaultImage = () => {
  if (images.length > 0) {
    const reader = new FileReader();
    reader.onload = () => {
      currentImage.src = reader.result;
    };
    reader.readAsDataURL(images[0]);
  }
};

const updateColorPickers = (imageName) => {
  const imageResult = result.find((item) => item.name === imageName);
  if (imageResult) {
    primaryColorPicker.value = imageResult.color.primary;
    secondaryColorPicker.value = imageResult.color.secondary;
    accentColorPicker.value = imageResult.color.accent;
  } else {
    primaryColorPicker.value = defaultColor;
    secondaryColorPicker.value = defaultColor;
    accentColorPicker.value = defaultColor;
  }
};

primaryColorPicker.value = defaultColor;
secondaryColorPicker.value = defaultColor;
accentColorPicker.value = defaultColor;

// Handle form submission
saveButton.addEventListener("click", (e) => {
  e.preventDefault();
  const imageName = images[selectedImageIndex].name;
  const imageResultIndex = result.findIndex((item) => item.name === imageName);

  const colorData = {
    primary: primaryColorPicker.value,
    secondary: secondaryColorPicker.value,
    accent: accentColorPicker.value,
  };

  if (imageResultIndex === -1) {
    result.push({
      name: imageName,
      color: colorData,
    });
  } else {
    result[imageResultIndex].color = colorData;
  }

  console.log("Form submitted", result);
});

exportButton.addEventListener("click", () => {
  const dataStr =
    "data:text/json;charset=utf-8," +
    encodeURIComponent(JSON.stringify(result));
  const downloadAnchorNode = document.createElement("a");
  downloadAnchorNode.setAttribute("href", dataStr);
  downloadAnchorNode.setAttribute("download", "result.json");
  document.body.appendChild(downloadAnchorNode); // required for firefox
  downloadAnchorNode.click();
  downloadAnchorNode.remove();
});
