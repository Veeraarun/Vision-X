// script.js

window.addEventListener('DOMContentLoaded', () => {
  const startBtn = document.querySelector('#startBtn');
  const messageBox = document.getElementById('message');
  const sky = document.getElementById('sky');
  const videoSphere = document.getElementById('videoSphere');
  const video = document.getElementById('therapyVideo');

  // Hover effects for start button
  startBtn.addEventListener('mouseenter', () => {
    startBtn.setAttribute('color', '#1976D2');
  });

  startBtn.addEventListener('mouseleave', () => {
    startBtn.setAttribute('color', '#2196F3');
  });

  // Start therapy click
  startBtn.addEventListener('click', () => {
    messageBox.classList.remove('hidden');

    // Show video sphere, hide sky
    sky.setAttribute('visible', 'false');
    videoSphere.setAttribute('visible', 'true');

    // Play the video on user interaction
    video.play().then(() => {
      console.log("Video playing");
    }).catch(err => {
      console.error("Playback failed:", err);
    });

    // Hide message after 4s
    setTimeout(() => {
      messageBox.classList.add('hidden');
    }, 4000);
  });
});

// Ask for gyro permission on mobile devices
function askGyroPermission() {
  if (typeof DeviceMotionEvent !== 'undefined' &&
      typeof DeviceMotionEvent.requestPermission === 'function') {
    DeviceMotionEvent.requestPermission()
      .then(response => {
        if (response === 'granted') {
          console.log("Gyroscope permission granted");
        } else {
          alert("Gyroscope permission denied. Some features may not work.");
        }
      })
      .catch(console.error);
  } else {
    console.log("Gyroscope permission not required or not supported.");
  }
  document.removeEventListener('click', askGyroPermission);
}
document.addEventListener('click', askGyroPermission);
