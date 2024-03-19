// let mic, fft;
// let colors = [];

// function setup() {
//   createCanvas(windowWidth, windowHeight);

//   // Create an audio input
//   mic = new p5.AudioIn();
//   mic.start();

//   // Create a Fast Fourier Transform (FFT) object
//   fft = new p5.FFT();
//   fft.setInput(mic);

//   // Define the colors for transitioning
//   colors[0] = color(255, 0, 0); // Red
//   colors[1] = color(0, 255, 0); // Green
//   colors[2] = color(0, 0, 255); // Blue
// }

// function draw() {
//   background(0);

//   // Get the amplitude (volume level) from the microphone input
//   let spectrum = fft.analyze();

//   // Visualize the spectrum data with transitioning colors
//   noStroke();
//   for (let i = 0; i < spectrum.length; i++) {
//     // Calculate the percentage for color transition
//     let percent = map(i, 0, spectrum.length, 0, 1);
//     let c = lerpColor(colors[0], colors[1], percent);

//     // Apply the color and draw the rectangle
//     fill(c);
//     let x = map(i, 0, spectrum.length, 0, width);
//     let h = -height + map(spectrum[i], 0, 255, height, 0);
//     rect(x, height, width / spectrum.length, h);
//   }
// }


// // function setup() {
// //   createCanvas(400, 400);
// // }

// // function draw() {
// //   background(220);
// //   // Generate random values for position and color
// //   let x = random(width);
// //   let y = random(height);
// //   let r = random(255);
// //   let g = random(255);
// //   let b = random(255);
// //   // Draw a circle with random color at a random position
// //   fill(r, g, b);
// //   noStroke();
// //   ellipse(x, y, 50, 50);
// // }

let mic, fft;
let colors = [];

function setup() {
  createCanvas(windowWidth, windowHeight);
}

function draw() {
  background(0);

  if (mic && fft) {
    // Get the amplitude (volume level) from the microphone input
    let spectrum = fft.analyze();

    // Visualize the spectrum data with transitioning colors
    noStroke();
    for (let i = 0; i < spectrum.length; i++) {
      // Calculate the percentage for color transition
      let percent = map(i, 0, spectrum.length, 0, 1);
      let c = lerpColor(colors[0], colors[1], percent);

      // Apply the color and draw the rectangle
      fill(c);
      let x = map(i, 0, spectrum.length, 0, width);
      let h = -height + map(spectrum[i], 0, 255, height, 0);
      rect(x, height, width / spectrum.length, h);
    }
  }
}

document.addEventListener('DOMContentLoaded', function () {
  const startButton = document.getElementById('startVisualizer');
  const stopButton = document.getElementById('stopVisualizer');

  // Add event listeners to buttons
  startButton.addEventListener('click', function () {
    startVisualizer(); // Call the function to start the visualizer
  });

  stopButton.addEventListener('click', function () {
    stopVisualizer(); // Call the function to stop the visualizer
  });
});

// Function to start the visualizer
function startVisualizer() {
  // Create an audio input
  mic = new p5.AudioIn();
  mic.start();

  // Create a Fast Fourier Transform (FFT) object
  fft = new p5.FFT();
  fft.setInput(mic);

  // Define the colors for transitioning
  colors[0] = color(255, 0, 0); // Red
  colors[1] = color(0, 255, 0); // Green
  colors[2] = color(0, 0, 255); // Blue
}

// Function to stop the visualizer
function stopVisualizer() {
  // Stop the audio input
  mic.stop();
}
