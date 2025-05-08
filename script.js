// script.js

window.addEventListener('DOMContentLoaded', () => {
  const startBtn1 = document.querySelector('#startBtn1');
  const startBtn2 = document.querySelector('#startBtn2');
  const startBtn3 = document.querySelector('#startBtn3');
  const messageBox = document.getElementById('message');
  const sky = document.getElementById('sky');
  const videoSphere = document.getElementById('videoSphere');
  const video = document.getElementById('therapyVideo');

  // Function to start therapy
  const startTherapy = (therapyNumber) => {
    messageBox.textContent = `Therapy ${therapyNumber} Started!`;
    messageBox.classList.remove('hidden');

    // Show video sphere, hide sky
    sky.setAttribute('visible', 'false');
    videoSphere.setAttribute('visible', 'true');

    // Play the video
    video.play()
      .then(() => {
        console.log(`Therapy ${therapyNumber} video playing`);
      })
      .catch(err => {
        console.error(`Therapy ${therapyNumber} playback failed:`, err);
      });

    // Hide message after 4 seconds
    setTimeout(() => {
      messageBox.classList.add('hidden');
    }, 4000);
  };

  // Add event listeners for each button
  startBtn1.addEventListener('click', () => startTherapy(1));
  startBtn2.addEventListener('click', () => startTherapy(2));
  startBtn3.addEventListener('click', () => startTherapy(3));
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

const scene = document.querySelector('a-scene');
const statsPanel = document.getElementById('statsPanel');
const chatPanel = document.getElementById('chatPanel');

scene.addEventListener('enter-vr', () => {
  statsPanel.style.display = 'none';
  chatPanel.style.display = 'none';
});

scene.addEventListener('exit-vr', () => {
  statsPanel.style.display = 'block';
  chatPanel.style.display = 'block';
});
