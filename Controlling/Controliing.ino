#include <ESP8266WiFi.h>
#include <WiFiClient.h>
#include <ESP8266WebServer.h>
#include <Wire.h>


int Pone=D1;
int Ptwo=D2;
int Pthree=D3;


const char MAIN_page[] PROGMEM = R"=====(
<!DOCTYPE html>
<html>
<body>
<title>Sir Syed University of Engineeing & Technology</title>
<center><H2>Sir Syed University of Engineeing & Technology
<center><H2>FACE RECOGNITION BASED ATTENDANCE SYSTEM WITH ROOM MONITORING AND CONTROL
<center><H5>Final Year Project by Rajal

<body style = 'background-color:blue;'>
<br>
<form action="/action_page">
 Enter Code :<br>
 <input type="text" name="code">
<br>

 <input type="submit" value="Submit">
</form>

</body>
</html>
)=====";

//SSID and Password of your WiFi router
const char* ssid = "FYP-2017EEA";
const char* password = "EEA-2017"; 

ESP8266WebServer server(80); //Server on port 80

void handleRoot() {
String s = MAIN_page; //Read HTML contents
server.send(200, "text/html", s); //Send web page
}


void handleForm(){
  String code = server.arg("code");
  Serial.print("code:");
  Serial.println(code);
  

  if(code=="Case1"){
  digitalWrite(Pone,LOW);
  digitalWrite(Ptwo,HIGH);
  digitalWrite(Pthree,HIGH);
  Serial.print("Condition 1");
  Serial.print(": RELAY 1 IS ON ");
 }
  else if(code=="Case2"){
  digitalWrite(Pone,LOW);
  digitalWrite(Ptwo,LOW);
  digitalWrite(Pthree,HIGH);
  Serial.print(": RELAY 2 IS ON ");
  }
  else if(code=="Case3"){
  Serial.println("item 3");
  digitalWrite(Pone,LOW);
  digitalWrite(Ptwo,LOW);
  digitalWrite(Pthree,LOW);
  Serial.print(": RELAY 3 IS ON ");
  }
  else if(code=="Case0"){
  Serial.println("item 3");
  digitalWrite(Pone,HIGH);
  digitalWrite(Ptwo,HIGH);
  digitalWrite(Pthree,HIGH);
  Serial.print(": OFF ");
  }
  
String s = "<a href='/'> Go Back </a>";
server.send(200, "text/html", s); //Send web page
}
void setup(void){
Serial.begin(115200);
pinMode(Pone,OUTPUT);
pinMode(Ptwo,OUTPUT);
pinMode(Pthree,OUTPUT);


 WiFi.begin(ssid, password); //Connect to your WiFi router
 Serial.println("");

 // Wait for connection
 while (WiFi.status() != WL_CONNECTED) {
 delay(500);
 Serial.print(".");
 }
 Serial.println("");
 Serial.print("Connected to ");
 Serial.println("WiFi");
 Serial.print("IP address: ");
 Serial.println(WiFi.localIP()); //IP address assigned to your ESP

 server.on("/", handleRoot);
 server.on("/action_page", handleForm); //form action is handled here
 server.begin(); //Start server
 Serial.println("HTTP server started");
}

void loop(void){
 server.handleClient();
} 
