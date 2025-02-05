#include <DallasTemperature.h>
#include <OneWire.h>
 
// Temperature
#define ONE_WIRE_BUS 13
 

OneWire oneWire(ONE_WIRE_BUS);
 

DallasTemperature sensors(&oneWire);


// Humidity
int soilMoisturePin = 11;  
int soilMoistureValue = 0;

// CO2
const int analogPin1 = 10; 


// Salt
const int analogPin2 = 9;
int sensorValue = 0;        
float voltage = 0.0;        
float tdsValue = 0.0;       

void setup() {
  Serial.begin(9600);
  delay(2000);
  sensors.begin();  
}

void loop() {
  
  sensorValue = analogRead(analogPin2);
  int sensorValue1 = analogRead(analogPin1);
  

  voltage = sensorValue * (5.0 / 1023.0);  
  

  tdsValue = (133.42 * voltage * voltage * voltage - 255.86 * voltage * voltage + 857.39 * voltage) * 0.5;

  soilMoistureValue = analogRead(soilMoisturePin);


  Serial.print("Soil Moisture Value: ");
  Serial.println(soilMoistureValue);

  Serial.print("Sensor Value: ");
  Serial.print(sensorValue);
  Serial.print("\tTDS (mg/l): ");
  Serial.println(tdsValue);

  Serial.print("CO2: ");
  Serial.println(sensorValue1);

  sensors.requestTemperatures(); 
  Serial.print("Temperature:");
  Serial.println(sensors.getTempCByIndex(0));

  delay(2000);
}