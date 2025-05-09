// script.js

window.addEventListener('DOMContentLoaded', () => {
  const startBtn1 = document.querySelector('#startBtn1');
  const startBtn2 = document.querySelector('#startBtn2');
  const startBtn3 = document.querySelector('#startBtn3');
  const messageBox = document.getElementById('message');
  const sky = document.getElementById('sky');
  const videoSphere = document.getElementById('videoSphere');
  const video = document.getElementById('therapyVideo');
  const buttons = [startBtn1, startBtn2, startBtn3];
  const bgSound = document.querySelector('#bgSound');

  // Function to start therapy
  const startTherapy = (therapyNumber, videoSrc) => {
    // Stop background sound
    if (bgSound.components && bgSound.components.sound) {
      bgSound.components.sound.stopSound();
      console.log("Background sound stopped.");
    }

    messageBox.classList.remove('hidden');

    // Update video source
    video.setAttribute('src', videoSrc);

    // Show video sphere, hide sky
    sky.setAttribute('visible', 'false');
    videoSphere.setAttribute('visible', 'true');

    // Hide all buttons
    buttons.forEach(button => button.setAttribute('visible', 'false'));

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

    // Restore buttons and background sound when the video ends
    video.onended = () => {
      buttons.forEach(button => button.setAttribute('visible', 'true'));
      sky.setAttribute('visible', 'true');
      videoSphere.setAttribute('visible', 'false');

      // Restart background sound
      if (bgSound.components && bgSound.components.sound) {
        bgSound.components.sound.playSound();
        console.log("Background sound restarted.");
      }
    };
  };

  // Add event listeners for each button with corresponding video sources
  startBtn1.addEventListener('click', () => startTherapy(1, 'assets/models/videos/WhatsApp Video 2025-05-09 at 09.37.21_6b048267.mp4'));
  startBtn2.addEventListener('click', () => startTherapy(2, 'assets/models/videos/WhatsApp Video 2025-05-09 at 09.37.25_9cc42ef7.mp4'));
  startBtn3.addEventListener('click', () => startTherapy(3, 'assets/models/videos/WhatsApp Video 2025-05-09 at 09.37.44_d7cc371e.mp4'));

  // Start background sound after user interaction
  const startBgSound = () => {
    if (bgSound.components && bgSound.components.sound) {
      bgSound.components.sound.playSound();
      console.log("Background sound started.");
    } else {
      console.error("Sound component not found on #bgSound.");
    }
    document.removeEventListener('click', startBgSound);
  };

  document.addEventListener('click', startBgSound);
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
