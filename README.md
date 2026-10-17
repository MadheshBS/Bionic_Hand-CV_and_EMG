# Bionic Arm: Computer Vision and EMG Control

A bionic arm that can be controlled in two ways:
- **Computer vision:** a camera detects the object or hand gesture and the arm responds.
- **EMG:** a muscle sensor reads signals from the user's muscle and drives the arm.

## Project Structure

```
bionic-arm-cv-emg/
├── README.md
├── cad/                  # SolidWorks files for the arm
├── vision/               # Computer vision code (Python)
└── firmware/
    ├── vision_arduino/   # Arduino code for the computer vision control
    └── emg_arduino/      # Arduino code for the EMG sensor control
```

## Hardware

- Microcontroller: Arduino Uno
- EMG sensor: Myoware
- Camera: Built-in Laptop camera / USB webcam
- Actuators: Servo motors
- Power supply: 7.4V battery

## How to Run

### 1. Computer Vision Control
1. Install the Python libraries:
   ```
   pip install opencv-python pyserial
   ```
2. Upload `firmware/vision_arduino/vision_arduino.ino` to the Arduino.
3. Connect the Arduino and set the correct COM port in the Python code.
4. Run:
   ```
   python vision/main.py
   ```

### 2. EMG Control
1. Connect the EMG sensor to the analog pin used in the code.
2. Upload `firmware/emg_arduino/emg_arduino.ino` to the Arduino.
3. Place the electrodes on the muscle and power the arm.

## CAD

The SolidWorks files for the arm are in the `cad/` folder. Open the `.SLDASM` file to see the full assembly.

## Author

Madhesh ([MadheshBS](https://github.com/MadheshBS))
