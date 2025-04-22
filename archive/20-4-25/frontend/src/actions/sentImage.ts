"use server";

export const sendImageAction = async <T>(formData: FormData) => {
  const image = formData.get("image");
  if (!image) {
    console.error("No image file found in the form data.");
    return;
  }

  try {
    const response = await fetch("http://localhost:8000/603010", {
      method: "POST",
      body: formData,
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const result = await response.json();
    return result as T;
  } catch (error) {
    console.error("Error uploading image:", error);
  }
};
