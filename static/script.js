function showSentimentAnalysis() {
    document.getElementById('sentiment-analysis').style.display = 'block';
    document.getElementById('emotion-detection').style.display = 'none';
}

function showEmotionDetection() {
    document.getElementById('sentiment-analysis').style.display = 'none';
    document.getElementById('emotion-detection').style.display = 'block';
}

function predictSentiment() {
    const textInput = document.getElementById('text-input').value;
    fetch('/predict', {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: `text_input=${textInput}`
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('sentiment-result').innerText = `Prediction: ${data.prediction}`;
    });
}




// 1 working
// const socket = io();

// function showSentimentAnalysis() {
//     document.getElementById('sentiment-analysis').style.display = 'block';
//     document.getElementById('emotion-detection').style.display = 'none';
//     stopCamera();
// }

// function showEmotionDetection() {
//     document.getElementById('sentiment-analysis').style.display = 'none';
//     document.getElementById('emotion-detection').style.display = 'block';
//     startCamera();
// }

// function predictSentiment() {
//     const textInput = document.getElementById('text-input').value;
//     fetch('/predict', {
//         method: 'POST',
//         headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
//         body: `text_input=${textInput}`
//     })
//     .then(response => response.json())
//     .then(data => {
//         document.getElementById('sentiment-result').innerText = `Prediction: ${data.prediction}`;
//     });
// }

// let video = document.getElementById('video');
// let canvas = document.getElementById('canvas');
// let context = canvas.getContext('2d');
// let localMediaStream = null;

// function startCamera() {
//     if (navigator.mediaDevices.getUserMedia) {
//         navigator.mediaDevices.getUserMedia({ video: true })
//         .then(function(stream) {
//             localMediaStream = stream;
//             video.srcObject = stream;
//             captureFrame();
//         })
//         .catch(function(error) {
//             console.log("Something went wrong!", error);
//         });
//     }
// }

// function stopCamera() {
//     if (localMediaStream) {
//         localMediaStream.getTracks().forEach(track => track.stop());
//         localMediaStream = null;
//     }
// }

// function captureFrame() {
//     if (localMediaStream) {
//         context.drawImage(video, 0, 0, canvas.width, canvas.height);
//         let dataURL = canvas.toDataURL('image/jpeg');
//         socket.emit('image', dataURL);
//     }
//     requestAnimationFrame(captureFrame);
// }

// socket.on('response_back', function(data) {
//     let image = new Image();
//     image.src = data.image;
//     image.onload = function() {
//         context.drawImage(image, 0, 0, canvas.width, canvas.height);
//     }
// });
