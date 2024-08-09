//FirebaseESP8266.h must be included before ESP8266WiFi.h
#include "FirebaseESP8266.h"	// Install Firebase ESP8266 library
#include <WiFi.h>
#include <ESP8266WiFi.h>
#include <DHT.h>		// Install DHT11 Library and Adafruit Unified Sensor Library


#define FIREBASE_HOST "smart-2-6cf06-default-rtdb.firebaseio.com/" //Without http:// or https:// schemes
#define FIREBASE_AUTH "Z195lYh29PANSVfWOkc9COiOsj9iR8as77QDgehm"
#define WIFI_SSID "Redmi K20"  // wifi name
#define WIFI_PASSWORD "asdf1234"  // Wifi Password

#define DHTPIN D1		// Connect Data pin of DHT to D2
#define Motor D5			// Connect LED to D5
#define Moisture D6
#define Rain D7
#define LED D4
float Moisture_String,Rain_String; 
float Pre_T,Pre_H;
float Curr_Soil=0.0, Pre_Soil=2.0, Curr_Rain=0, Pre_Rain=2 ;
String Curr_Motor="0", Pre_Motor="2";
boolean DHT_Status = 1;
#define DHTTYPE    DHT11
DHT dht(DHTPIN, DHTTYPE);

//Define FirebaseESP8266 data object
FirebaseData firebaseData;
FirebaseData MotorData;

FirebaseJson json;


void setup()
{

  Serial.begin(9600);

  dht.begin();
  pinMode(Motor,OUTPUT);
  pinMode(LED,OUTPUT);
  pinMode(Moisture,INPUT_PULLUP);
  pinMode(Rain,INPUT_PULLUP);
  digitalWrite(Motor,HIGH);
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  Serial.print("Connecting to Wi-Fi");
  while (WiFi.status() != WL_CONNECTED)
  {
    digitalWrite(LED,HIGH);
    Serial.print(".");
    delay(50);
    digitalWrite(LED,LOW);
    delay(50);
  }
  Serial.println();
  Serial.print("Connected with IP: ");
  Serial.println(WiFi.localIP());
  Serial.println();

  Firebase.begin(FIREBASE_HOST, FIREBASE_AUTH);
  Firebase.reconnectWiFi(true);

}

void sensorUpdate(){
  float h = dht.readHumidity();
  float t = dht.readTemperature();
  if(DHT_Status==0)
  {
    digitalWrite(LED,HIGH);
    Serial.println("Check DHT Sensor Wire Connection");
    delay(500);
    digitalWrite(LED,LOW);
    delay(500);
    Pre_Motor=2;
  }
  if (isnan(h) || isnan(t)) 
 {
   
    DHT_Status=0;
    return;
  }
   DHT_Status=1;

  Serial.print(F("Humidity: "));  
  Serial.print(h);
  Serial.print(F("%  Temperature: "));
  Serial.print(t);
  Serial.println(F("°C"));
  
  if(digitalRead(Moisture)==LOW)
  Moisture_String=1;
  else 
  Moisture_String=0;
 if(digitalRead(Rain)==LOW)
  Curr_Rain=1.0;
  else 
  Curr_Rain=0.0;

  
  if(!(Curr_Soil==Pre_Soil))
  {
    if (Firebase.setFloat(firebaseData, "/Smart_2/soil", Moisture_String))
  {
    Serial.println("Soil PASSED");
    Serial.println("PATH: " + firebaseData.dataPath());
    Serial.println("TYPE: " + firebaseData.dataType());
    Serial.println("ETag: " + firebaseData.ETag());
    Serial.println("------------------------------------");
    Serial.println();
  }
  else
  {
    Serial.println("Soil FAILED");
    Serial.println("REASON: " + firebaseData.errorReason());
    Serial.println("------------------------------------");
    Serial.println();
  }
  Pre_Soil=Curr_Soil;
  }
   if(!(Curr_Rain==Pre_Rain))
  {
    if (Firebase.setFloat(firebaseData, "/Smart_2/rain", Curr_Rain))
  {
    Serial.println("Soil PASSED");
    Serial.println("PATH: " + firebaseData.dataPath());
    Serial.println("TYPE: " + firebaseData.dataType());
    Serial.println("ETag: " + firebaseData.ETag());
    Serial.println("------------------------------------");
    Serial.println();
  }
  else
  {
    Serial.println("Rain FAILED");
    Serial.println("REASON: " + firebaseData.errorReason());
    Serial.println("------------------------------------");
    Serial.println();
  }
  Pre_Rain=Curr_Rain;
  }
  
 Curr_Soil=digitalRead(Moisture);
 Curr_Rain=digitalRead(Rain);

  

 
  

  if(!(t==Pre_T))
  {

  if (Firebase.setFloat(firebaseData, "/Smart_2/temperature", t))
  {
    Serial.println("Temperature PASSED");
    Serial.println("PATH: " + firebaseData.dataPath());
    Serial.println("TYPE: " + firebaseData.dataType());
    Serial.println("ETag: " + firebaseData.ETag());
    Serial.println("------------------------------------");
    Serial.println();
  }
  else
  {
    Serial.println("Temperature FAILED");
    Serial.println("REASON: " + firebaseData.errorReason());
    Serial.println("------------------------------------");
    Serial.println();
  }
   Pre_T=t;
  }

   if(!(h==Pre_H))
  {
  if (Firebase.setFloat(firebaseData, "/Smart_2/humidity", h))
  {
    Serial.println("Humidity PASSED");
    Serial.println("PATH: " + firebaseData.dataPath());
    Serial.println("TYPE: " + firebaseData.dataType());
    Serial.println("ETag: " + firebaseData.ETag());
    Serial.println("------------------------------------");
    Serial.println();
  }
  else
  {
    Serial.println("Humidity FAILED");
    Serial.println("REASON: " + firebaseData.errorReason());
    Serial.println("------------------------------------");
    Serial.println();
  }
   Pre_H=h;
  }


  Firebase.getString(MotorData, "/Smart_2/Motor");
 Curr_Motor=MotorData.stringData();

  if(!(Curr_Motor==Pre_Motor))
  {
 
  if (Firebase.getString(MotorData, "/Smart_2/Motor")){
    Serial.print("Motor Status:");
    Serial.println(MotorData.stringData());
    if (MotorData.stringData() == "1") {
    digitalWrite(Motor, LOW);
    }
  else if (MotorData.stringData() == "0"){
    digitalWrite(Motor, HIGH);
    }
  }
  Pre_Motor=Curr_Motor;
  }
 
  
}
void loop() {
  sensorUpdate();

}
