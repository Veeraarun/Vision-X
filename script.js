window.addEventListener('DOMContentLoaded', () => {
  const video = document.getElementById('therapyVideo');
  const sky = document.getElementById('sky');
  const videoSphere = document.getElementById('videoSphere');
  const messageBox = document.getElementById('message');

  const bgSound = document.querySelector('#bgSound');
  const goBackBtn = document.getElementById('goBackBtn');
  const buttonGroup = document.getElementById('buttonGroup');

  const startBtn1 = document.querySelector('#startBtn1');
  const startBtn2 = document.querySelector('#startBtn2');
  const startBtn3 = document.querySelector('#startBtn3');
  const buttons = [startBtn1, startBtn2, startBtn3];

  // Enable/Disable Buttons
  function disableStartButtons() {
    buttonGroup.setAttribute('visible', 'false');
    buttons.forEach(btn => btn.classList.remove('clickable'));
  }

  function enableStartButtons() {
    buttonGroup.setAttribute('visible', 'true');
    buttons.forEach(btn => btn.classList.add('clickable'));
  }

  function startTherapy(label, src) {
    video.setAttribute('src', src);
    video.load();
    sky.setAttribute('visible', 'false');
    videoSphere.setAttribute('visible', 'true');

    disableStartButtons();
    goBackBtn.setAttribute('visible', 'true');

    if (bgSound.components && bgSound.components.sound) {
      bgSound.components.sound.stopSound();
    }

    messageBox.classList.remove('hidden');

    video.play().catch(console.error);

    setTimeout(() => {
      messageBox.classList.add('hidden');
    }, 4000);

    video.onended = () => {
      enableStartButtons();
      goBackBtn.setAttribute('visible', 'false');
      videoSphere.setAttribute('visible', 'false');
      sky.setAttribute('visible', 'true');

      if (bgSound.components && bgSound.components.sound) {
        bgSound.components.sound.playSound();
      }
    };
  }

  // Click Handlers
  startBtn1.addEventListener('click', () => startTherapy("Height", 'assets/models/videos/WhatsApp Video 2025-05-09 at 09.37.21_6b048267.mp4'));
  startBtn2.addEventListener('click', () => startTherapy("Ocean", 'assets/models/videos/WhatsApp Video 2025-05-09 at 09.37.25_9cc42ef7.mp4'));
  startBtn3.addEventListener('click', () => startTherapy("Driving", 'assets/models/videos/WhatsApp Video 2025-05-09 at 09.37.44_d7cc371e.mp4'));

  goBackBtn.addEventListener('click', () => {
    video.pause();
    videoSphere.setAttribute('visible', 'false');
    sky.setAttribute('visible', 'true');
    enableStartButtons();
    goBackBtn.setAttribute('visible', 'false');

    if (bgSound.components && bgSound.components.sound) {
      bgSound.components.sound.playSound();
    }
  });

  // Gyro
  document.addEventListener('click', () => {
    if (typeof DeviceMotionEvent !== 'undefined' && typeof DeviceMotionEvent.requestPermission === 'function') {
      DeviceMotionEvent.requestPermission().then(response => {
        if (response === 'granted') console.log("Gyroscope enabled");
      });
    }
  });

  // Background sound trigger
  document.addEventListener('click', () => {
    if (bgSound.components.sound) bgSound.components.sound.playSound();
  }, { once: true });
});
