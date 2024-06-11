document.addEventListener("DOMContentLoaded", () => {
    const video = document.querySelector("#videoElement");
    const canvas = document.querySelector("#canvasElement");
    const captureButton = document.querySelector("#captureButton");
    const submitButton = document.querySelector("#submitButton");
    const imageDataInput = document.querySelector("#imageDataInput");

    if (video) {
        navigator.mediaDevices.getUserMedia({ video: true })
            .then(stream => {
                video.srcObject = stream;
            })
            .catch(err => {
                console.log("An error occurred: " + err);
            });

        captureButton.addEventListener("click", () => {
            canvas.getContext("2d").drawImage(video, 0, 0, canvas.width, canvas.height);
            const imageData = canvas.toDataURL("image/png");
            imageDataInput.value = imageData;
        });

        submitButton.addEventListener("click", () => {
            const imageData = canvas.toDataURL("image/png");
            fetch('/queue_live', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: 'image_data=' + encodeURIComponent(imageData),
            })
            .then(response => response.json())
            .then(data => {
                alert(data.message);
                console.log('Image URL:', data.image_url);
            })
            .catch(error => {
                console.error('Error:', error);
            });
        });
    }
});
