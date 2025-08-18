#include <LiquidCrystal.h>
 

LiquidCrystal lcd(6, 7, 8, 9, 10, 11);

int numberBytes;
String type_hardware = "GPU";

String typesHardware[4] = {"CPU", "GPU", "RAM", "FAN"};
int indexHardware = 1;
int RIGHT_BUTTON_PIN = 13;
int LEFT_BUTTON_PIN = 12;
int RED_DIOD = 2;
bool buttonPress = false;
int right = 0;
int left = 0;

char grad = 223;
byte GPUdata[2];
int currentGPUTemp;
int currentGPULoad;

byte CPUdata[6];
long CPUTime = 0;
// int loadCPUCore_1;

byte RAMdata[3];

void clearSerial(){
  while(Serial.available()){
    Serial.read();
  }
}

void setup() {
  lcd.begin(16, 2);
  Serial.begin(9600);
  pinMode(RED_DIOD, OUTPUT);
  pinMode(RIGHT_BUTTON_PIN, INPUT);
  pinMode(LEFT_BUTTON_PIN, INPUT);

  clearSerial();
  // lcd.print("Hello World");
}

void blink(){
  for (int i = 0; i<10; i++){
      digitalWrite(LED_BUILTIN, HIGH);
      delay(100);
      digitalWrite(LED_BUILTIN, LOW);
      delay(100);
  }
}

String convertTwoDigitIntToString(int number){
  char digits[2];
  itoa(number, digits, 10);
  return String(digits);
}

void printHighGPUTemp(){
  String currentTempStrings = convertTwoDigitIntToString(currentGPUTemp);
  String currentLoadString = convertTwoDigitIntToString(currentGPULoad);
  lcd.clear();
  lcd.setCursor(2, 0);
  lcd.print(type_hardware + ":" + currentTempStrings + String(grad) + "C" + " " + currentLoadString + "%");
  lcd.setCursor(6, 1);
  lcd.print("HOT!");
  if (currentGPUTemp > 70){
    digitalWrite(RED_DIOD, 1);
  }else{
    digitalWrite(RED_DIOD, 0);
  }
}

void printGPUTemp(){
  String currentTempStrings = convertTwoDigitIntToString(currentGPUTemp);
  String currentLoadString = convertTwoDigitIntToString(currentGPULoad);
  lcd.clear();
  lcd.setCursor(2, 0);
  lcd.print(type_hardware + ":" + currentTempStrings + String(grad) + "C" + " " + currentLoadString + "%");
}

void printCPULoad(){
  String CPUStringData[6];
  for (int i = 0; i<6; i++){
    CPUStringData[i] = convertTwoDigitIntToString(CPUdata[i]);
  }

  lcd.setCursor(6, 0);
  lcd.print(CPUStringData[0]);
  lcd.setCursor(16, 0);
  lcd.print(CPUStringData[1]);
  lcd.setCursor(26, 0);
  lcd.print(CPUStringData[2]);
  lcd.setCursor(6, 1);
  lcd.print(CPUStringData[3]);
  lcd.setCursor(16, 1);
  lcd.print(CPUStringData[4]);
  lcd.setCursor(26, 1);
  lcd.print(CPUStringData[5]);
}

void initPrintCPULoad(){
    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("CPU_1:  %");
    lcd.setCursor(10, 0);
    lcd.print("CPU_2:  %");
    lcd.setCursor(20, 0);
    lcd.print("CPU_3:  %");
    lcd.setCursor(0, 1);
    lcd.print("CPU_4:  %");
    lcd.setCursor(10, 1);
    lcd.print("CPU_5:  %");
    lcd.setCursor(20, 1);
    lcd.print("CPU_6:  %");
}

void printRAMLoad(){
  String usedRAMPercent = convertTwoDigitIntToString(RAMdata[0]); 
  String usedRAMGB = convertTwoDigitIntToString(RAMdata[1]); 
  String availableRAM = convertTwoDigitIntToString(RAMdata[2]);

  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("UsedRAM:" + usedRAMGB + "GB" + " " + usedRAMPercent + "%"); 
  lcd.setCursor(0, 1);
  lcd.print("Available:" + availableRAM + "GB");
}

void printText(String text){
  lcd.clear();
  lcd.setCursor(7, 0);
  lcd.print(text);
}

void buttonPressHandler(){
  right = digitalRead(RIGHT_BUTTON_PIN);
  left = digitalRead(LEFT_BUTTON_PIN);
  if (right == 1){
    // Serial.println("Правая кнопка");
    if (!buttonPress){
      buttonPress = true;
      indexHardware = indexHardware + 1;
      if (indexHardware > 3)
        indexHardware = 0;
      if (typesHardware[indexHardware] == "CPU"){
        initPrintCPULoad();
      }
      Serial.print(typesHardware[indexHardware]);
      
    }
  }
  else if (left == 1){
    // Serial.println("Левая кнопка");
      if (!buttonPress){
        buttonPress = true;
        indexHardware = indexHardware - 1;
        if (indexHardware < 0)
          indexHardware = 3;
        if (typesHardware[indexHardware] == "CPU"){
          initPrintCPULoad();
        }
        Serial.print(typesHardware[indexHardware]);
    }
  }
  else {
    buttonPress = false;
  }
}

void loop() {
  buttonPressHandler();

  if(typesHardware[indexHardware] == "CPU"){
    long mls = millis();
    if (mls - CPUTime > 1000){
      lcd.scrollDisplayLeft();
      CPUTime = mls;
    }
  }

  numberBytes = Serial.available();
  if (numberBytes > 0){
      if (typesHardware[indexHardware] == "CPU"){
        Serial.readBytes(CPUdata, 6);
        printCPULoad();
      }
      else if (typesHardware[indexHardware] == "GPU") {
        Serial.readBytes(GPUdata, 2);
        currentGPUTemp = GPUdata[0];
        currentGPULoad = GPUdata[1];

        if (currentGPUTemp > 55){
          printHighGPUTemp();
        }
        else{
          printGPUTemp();
        }
      }
      else if (typesHardware[indexHardware] == "RAM") {
        Serial.readBytes(RAMdata, 3);
        printRAMLoad();
      }
    Serial.flush();
  }

}
