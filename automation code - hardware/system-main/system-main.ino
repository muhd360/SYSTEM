#include <LiquidCrystal.h>  // For LCD display

// Pin Definitions
#define IR1_PIN 2
#define IR2_PIN 3
#define IR3_PIN 4
#define IR4_PIN 5

#define REL1_PIN 6
#define REL2_PIN 7
#define REL3_PIN 8
#define REL4_PIN 9
#define REL5_PIN 10

// Communication Pins for Arduino Nanos (N1-N5)
#define N1_PIN 11
#define N2_PIN 12
#define N3_PIN 13
#define N4_PIN A0
#define N5_PIN A1

// LCD Pins (if using 4-bit mode, adjust accordingly)
LiquidCrystal lcd1(8, 9, 10, 11, 12, 13);  // Adjust pin numbers according to your setup
LiquidCrystal lcd2(8, 9, 10, 11, 12, 13);  
LiquidCrystal lcd3(8, 9, 10, 11, 12, 13);
LiquidCrystal lcd4(8, 9, 10, 11, 12, 13);

int parcelCount1 = 0;
int parcelCount2 = 0;
int parcelCount3 = 0;
int parcelCount4 = 0;

void setup() {
  // Initialize Serial communication
  Serial.begin(9600);
  
  // Initialize Relay pins
  pinMode(REL1_PIN, OUTPUT);
  pinMode(REL2_PIN, OUTPUT);
  pinMode(REL3_PIN, OUTPUT);
  pinMode(REL4_PIN, OUTPUT);
  pinMode(REL5_PIN, OUTPUT);

  // Initialize IR sensor pins
  pinMode(IR1_PIN, INPUT);
  pinMode(IR2_PIN, INPUT);
  pinMode(IR3_PIN, INPUT);
  pinMode(IR4_PIN, INPUT);

  // Initialize Nano communication pins
  pinMode(N1_PIN, OUTPUT);
  pinMode(N2_PIN, OUTPUT);
  pinMode(N3_PIN, OUTPUT);
  pinMode(N4_PIN, OUTPUT);
  pinMode(N5_PIN, OUTPUT);

  // Initialize LCDs
  lcd1.begin(16, 2);
  lcd2.begin(16, 2);
  lcd3.begin(16, 2);
  lcd4.begin(16, 2);

  // Set initial Relay state (start system with rel1 & rel2 high)
  digitalWrite(REL1_PIN, HIGH);
  digitalWrite(REL2_PIN, HIGH);
}

void loop() {
  // IR1 detection
  if (digitalRead(IR1_PIN) == HIGH) {
    delay(2000); // Delay for 2 seconds

    // Set rel1 & rel2 low
    digitalWrite(REL1_PIN, LOW);
    digitalWrite(REL2_PIN, LOW);

    // Run script.py and get the result (simulation)
    String result = runScript("script.py");

    // Class 1 logic
    if (result == "class1") {
      handleClass1();
    } 
    // Class 2 logic
    else if (result == "class2") {
      handleClass2();
    }
    // Class 3 logic
    else if (result == "class3") {
      handleClass3();
    }

    // Increment the parcel count for IR1
    parcelCount1++;
    lcd1.setCursor(0, 0);
    lcd1.print("Count: ");
    lcd1.print(parcelCount1);
  }
  
  // IR2 detection logic
  if (digitalRead(IR2_PIN) == HIGH) {
    delay(2000);

    parcelCount2++;
    lcd2.setCursor(0, 0);
    lcd2.print("Count: ");
    lcd2.print(parcelCount2);
  }

  // IR3 detection logic
  if (digitalRead(IR3_PIN) == HIGH) {
    delay(2000);

    parcelCount3++;
    lcd3.setCursor(0, 0);
    lcd3.print("Count: ");
    lcd3.print(parcelCount3);
  }

  // IR4 detection logic
  if (digitalRead(IR4_PIN) == HIGH) {
    delay(2000);

    parcelCount4++;
    lcd4.setCursor(0, 0);
    lcd4.print("Count: ");
    lcd4.print(parcelCount4);
  }
}

// Function to handle Class 1 logic
void handleClass1() {
  sendSignalToNano(N1_PIN, "rotate");  // Send rotate signal to N1

  // Wait for N1 response (success)
  waitForNanoResponse();

  // Set rel1 and rel2 high until IR2 detects an object
  digitalWrite(REL1_PIN, HIGH);
  digitalWrite(REL2_PIN, HIGH);
  
  while (digitalRead(IR2_PIN) == LOW);  // Wait until IR2 is HIGH

  // Send signal to N1 to reset motor
  sendSignalToNano(N1_PIN, "reset");
  waitForNanoResponse();

  // Trigger rel3 for 2 seconds
  digitalWrite(REL3_PIN, HIGH);
  delay(2000);
  digitalWrite(REL3_PIN, LOW);

  // Run script2.py and check the result
  String result = runScript("script2.py");

  if (result == "pass") {
    digitalWrite(REL3_PIN, HIGH);
    delay(5000);
    digitalWrite(REL3_PIN, LOW);
  } else {
    sendSignalToNano(N3_PIN, "rotate");
    waitForNanoResponse();

    digitalWrite(REL3_PIN, HIGH);
    delay(10000);
    digitalWrite(REL3_PIN, LOW);

    sendSignalToNano(N3_PIN, "reset");
    waitForNanoResponse();
  }
}

// Function to handle Class 2 logic
void handleClass2() {
  sendSignalToNano(N2_PIN, "rotate");
  waitForNanoResponse();

  digitalWrite(REL1_PIN, HIGH);
  digitalWrite(REL2_PIN, HIGH);
  
  while (digitalRead(IR3_PIN) == LOW);  // Wait for IR3 to detect object

  sendSignalToNano(N2_PIN, "reset");
  waitForNanoResponse();

  digitalWrite(REL4_PIN, HIGH);
  delay(2000);
  digitalWrite(REL4_PIN, LOW);

  String result = runScript("script3.py");

  if (result == "pass") {
    digitalWrite(REL4_PIN, HIGH);
    delay(5000);
    digitalWrite(REL4_PIN, LOW);
  } else {
    sendSignalToNano(N4_PIN, "rotate");
    waitForNanoResponse();

    digitalWrite(REL4_PIN, HIGH);
    delay(10000);
    digitalWrite(REL4_PIN, LOW);

    sendSignalToNano(N4_PIN, "reset");
    waitForNanoResponse();
  }
}

// Function to handle Class 3 logic
void handleClass3() {
  digitalWrite(REL1_PIN, HIGH);
  digitalWrite(REL2_PIN, HIGH);

  while (digitalRead(IR3_PIN) == LOW);  // Wait for IR3

  digitalWrite(REL1_PIN, LOW);
  digitalWrite(REL2_PIN, LOW);

  digitalWrite(REL5_PIN, HIGH);
  delay(2000);
  digitalWrite(REL5_PIN, LOW);

  String result = runScript("script4.py");

  if (result == "pass") {
    digitalWrite(REL5_PIN, HIGH);
    delay(5000);
    digitalWrite(REL5_PIN, LOW);
  } else {
    sendSignalToNano(N5_PIN, "rotate");
    waitForNanoResponse();

    digitalWrite(REL5_PIN, HIGH);
    delay(10000);
    digitalWrite(REL5_PIN, LOW);

    sendSignalToNano(N5_PIN, "reset");
    waitForNanoResponse();
  }
}

// Function to simulate running a Python script and getting a result
String runScript(String scriptName) {
  // Simulate running a script and getting a result
  if (scriptName == "script.py") {
    return "class1";  // Replace with actual logic to run script
  } else if (scriptName == "script2.py") {
    return "pass";
  } else if (scriptName == "script3.py") {
    return "pass";
  } else if (scriptName == "script4.py") {
    return "npass";
  }
  return "";
}

// Function to send a signal to a Nano
void sendSignalToNano(int nanoPin, String command) {
  Serial.println(command);  // Send the command to the specific Nano
}

// Function to wait for a response from a Nano
void waitForNanoResponse() {
  while (Serial.available() == 0);  // Wait for response
  String response = Serial.readString();
  Serial.println(response);  // Debug response
}
