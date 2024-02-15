const video = document.getElementById("video");
const captureButton = document.getElementById("captureButton");

navigator.mediaDevices
  .getUserMedia({ video: true })
  .then((stream) => {
    video.srcObject = stream;
  })
  .catch((error) => {
    console.error("Error accessing webcam:", error);
  });

captureButton.addEventListener("click", () => {
  const canvas = document.createElement("canvas");
  canvas.width = video.videoWidth;
  canvas.height = video.videoHeight;
  canvas.getContext("2d").drawImage(video, 0, 0);
  const photoData = canvas.toDataURL("image/jpeg", 0.8);

  // Send captured photo data to the server

  fetch("/", {
    method: "POST",
    headers: {
      "X-CSRFToken": window.csrf_token,
      "Content-Type": "application/x-www-form-urlencoded",
    },
    body: "photo_data=" + encodeURIComponent(photoData),
  })
    .then(
      (response) => response.json()
      // Redirect or display success message
    )
    .then((data) => {
      if (data.redirectUrl) {
        window.location.href = data.redirectUrl; // Redirect the browser to the URL
      } else {
        console.log("Server response:", data);
        // Handle other server responses
      }
    })
    .catch((error) => {
      console.error("Error sending photo data to server:", error);
    });
});
