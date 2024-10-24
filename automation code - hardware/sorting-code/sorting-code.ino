// Include the Stepper library
#include <AccelStepper.h>

// Define stepper motor control pins
#define STEP_PIN 3
#define DIR_PIN 4
#define ENABLE_PIN 5

// Define steps per revolution (based on step angle of your motor)
#define STEPS_PER_REVOLUTION 200  // For 1.8-degree step motors (200 steps per 360 degrees)

// AccelStepper object
AccelStepper stepper(AccelStepper::DRIVER, STEP_PIN, DIR_PIN);

void setup() {
  pinMode(ENABLE_PIN, OUTPUT);   // Enable pin for the stepper driver
  digitalWrite(ENABLE_PIN, LOW); // Enable the motor driver

  Serial.begin(9600);            // Start serial communication
  stepper.setMaxSpeed(1000);     // Set maximum speed (adjust as needed)
  stepper.setAcceleration(500);  // Set acceleration (adjust as needed)
}

void loop() {
  if (Serial.available() > 0) {
    String command = Serial.readString();
    
    if (command == "rotate") {
      rotateStepper(45);  // Rotate the motor 45 degrees
      Serial.println("success");  // Send success response to Arduino 1
    }
    
    if (command == "reset") {
      rotateStepper(-45);  // Rotate the motor back to 0 degrees (counter-clockwise)
      Serial.println("reset_done");  // Confirm reset to Arduino 1
    }
  }
}

// Function to rotate the stepper motor by a specific angle
void rotateStepper(float degrees) {
  int steps = degreeToSteps(degrees);  // Convert degrees to steps
  stepper.moveTo(steps);               // Move the motor to the target position
  stepper.runToPosition();             // Run to the position
}

// Helper function to convert degrees to steps
int degreeToSteps(float degrees) {
  return (int)(degrees * STEPS_PER_REVOLUTION / 360.0);  // Convert degrees to steps
}
