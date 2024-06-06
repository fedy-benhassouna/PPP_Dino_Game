
# Dino Game with Eye Blink Control

This project is a Dino game controlled by eye blinks, using OpenCV, MediaPipe, and CVZone for eye blink detection. The game includes various obstacles and sound effects.

## Features
- **Eye Blink Detection**: Control the Dino character by blinking your eyes.
- **Obstacles**: Includes cacti and pterodactyls as obstacles.
- **Sound Effects**: Jump, points, and game over sound effects enhance the gaming experience.
- **Animations**: Smooth animations for Dino running, jumping, and ducking.

## Requirements
- Python 3.6+
- OpenCV
- cvzone
- MediaPipe
- PyAutoGUI
- Pygame

## Installation
1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/dino-game-eye-blink.git
    cd dino-game-eye-blink
    ```

2. Install the required packages:
    ```sh
    pip install opencv-python cvzone mediapipe pyautogui pygame
    ```

## Running the Game
1. Make sure your webcam is connected.
2. Place the necessary image and sound files in the correct directories:
   - `ground.png`
   - `cloud.png`
   - `Dino1.png`
   - `Dino2.png`
   - `DinoDucking1.png`
   - `DinoDucking2.png`
   - `cacti/cactus1.png` to `cacti/cactus6.png`
   - `Ptero1.png`
   - `Ptero2.png`
   - `sfx/lose.mp3`
   - `sfx/100points.mp3`
   - `sfx/jump.mp3`

3. Run the game script:
    ```sh
    python dino_game.py
    ```

## How to Play
- **Jump**: Blink your eyes to make the Dino jump.
- **Duck**: Press the down arrow key to make the Dino duck.
- **Restart**: Press the space bar or the up arrow key to restart the game after a game over.

## Game Controls
- **Blinks**: Control the Dino's jump.
- **Arrow Keys**: Additional controls for ducking and jumping.

## Code Overview
- **Eye Blink Detection**: Uses OpenCV and MediaPipe to detect blinks and control the Dino's jumps.
- **Game Mechanics**: Implemented with Pygame for animations, obstacle spawning, and collision detection.
- **Sound Effects**: Added using Pygame mixer for enhanced user experience.



## Acknowledgements
- Inspired by the Chrome Dino game.
- Uses OpenCV, MediaPipe, CVZone, PyAutoGUI, and Pygame for various functionalities.

## Contact
For any questions or feedback, please contact fedy.benhassouna@insat.ucar.tn .

