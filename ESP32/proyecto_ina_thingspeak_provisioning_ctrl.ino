

#include "eco2.h"

int d = 0;
const int S = 3; 
const int initialConnectAttempts = 5; 


/*----------------------------------------------------------
  WiFi connection in an ESP32s
  ----------------------------------------------------------*/
#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>
#include <EEPROM.h>
#include "secrets.h"

String ssid;       
String password;  

/*----------------------------------------------------------
  Access Point mode in an ESP32s
  ----------------------------------------------------------*/
#include <WebServer.h>

WebServer server(80);  //Local server at port 80

int statusCode;
const char* AP_ssid = "redmedidor";
const char* AP_pass = "";

//Local Device Credencials
const char* local_user_esp32 ="esp32";
const char* local_pass_esp32 ="4321";

//HTML CONTENT
String content;
String content_fixed_up;
String content_dynamic;
String content_fixed_down;
String netListHtml;

int totalNets;

bool AP_MODE = false; //Access Point State

/*----------------------------------------------------------
  Local control settings
  ----------------------------------------------------------*/

int remote_calibrate_state = 0; //calibrate_state in device:  0 no calibrate, 1 calibrate request, 2 calibrate process, -1 local calibration


/*----------------------------------------------------------
  Getting Date and Time from NTP Server
  ----------------------------------------------------------*/
#include "time.h"
const char* ntpServer = "pool.ntp.org";
const long  gmtOffset_sec = 3600*(-3); // (GMT-3)
const int   daylightOffset_sec = 0; // offset in seconds for daylight saving time. It is generally one hour=3600

struct Mment {
  int s_co2ppm, s_temp;
  struct tm  s_timeinfo;
};

// When WiFi is not available, measurements are saved every 5 minutes. Here we can store up tu 3 hours of measurements.
const int MAX_MM = 12*3;
struct Mment mm2send[MAX_MM];
int saved2send = 0; 

void printLocalTime(){
  struct tm timeinfo;
  char buffer [25];
  
  if(!getLocalTime(&timeinfo)){
    Serial.println("Failed to obtain time");
    return;
  }
  Serial.println(&timeinfo, "%A, %B %d %Y %H:%M:%S");

  Serial.print("Local timestamp: ");
  // strftime doc: https://www.cplusplus.com/reference/ctime/strftime/
  strftime (buffer,25,"%F %T-03",&timeinfo); // Example "2017-01-12 13:22:54-05"
  Serial.println(buffer);
  
  Serial.println();
}

/*----------------------------------------------------------
    Connect to WiFi in STA mode
  ----------------------------------------------------------*/
void connectWiFiModeSTA(){
  int t = 0;
  WiFi.mode(WIFI_STA);
 
  //connection init
  Serial.print("Connecting to...");
  Serial.println(ssid);
  Serial.print("with pass...");
  Serial.println(password);

  while (WiFi.status() != WL_CONNECTED){
    WiFi.begin(ssid.c_str(), password.c_str());
    Serial.print(".");
    updateRGB_LED (true);         // Blink while connecting
    delay(10000);
    if (t++>30) return; // 60s*5=300s=5min
  }

  Serial.println("");
  Serial.println("WiFi connected");
  
}

void connectWiFi_1(){
     // WiFi connection attempts (initialConnectAttempts)
     for (int i = 0; i < initialConnectAttempts; ++i) {
        WiFi.begin(ssid.c_str(), password.c_str());
        Serial.println("Connecting to Wifi...");
        updateRGB_LED (true);         // Blink while connecting
        delay(10000);

        if(WiFi.status() != WL_CONNECTED){
           Serial.println("Fail connection in attempt: " + String(i+1));
        }
        else {
           Serial.println("Connected to Wifi!");
           i = initialConnectAttempts;
        }
     }   
     
     if(WiFi.status() != WL_CONNECTED){
      Serial.println("No connection after attempts:" + String(initialConnectAttempts));
      Serial.println ("Changing to Access Point mode..."); 
      createAPserver();    
      AP_MODE = true;
     }
    
}


/*----------------------------------------------------------
    Read meter parameters from EEPROM
  ----------------------------------------------------------*/
int readEEPROM(){
  //  SSID
  Serial.println("Reading EEPROM ssid");

  ssid = "";
  for (int i = 0; i < 32; ++i)
  {
    ssid += char(EEPROM.read(i));
  }

  if (!(int)ssid.charAt(0)) return 0; // Parameters NOT found in EEPROM

  Serial.println();
  Serial.print("SSID: ");
  Serial.println(ssid); 
  
  //  password
  Serial.println("Reading EEPROM pass");

  password = "";
  for (int i = 32; i < 96; ++i)
  {
    password += char(EEPROM.read(i));
  }

  Serial.print("PASS: ");
  Serial.println(password);

  return 1; // Parameters found in EEPROM
}


/*----------------------------------------------------------
    Write meter parameters to EEPROM
  ----------------------------------------------------------*/
void writeEEPROM(String qsid, String qpass){
  // qsid = 32 bytes, qpass = 64 bytes

  for (int i = 0; i < 96; ++i) {
    EEPROM.write(i, 0);
  }
  Serial.println(qsid);
  Serial.println("");
  Serial.println(qpass);
  Serial.println("");

  Serial.println("writing eeprom ssid:");
  for (int i = 0; i < qsid.length(); ++i){
    EEPROM.write(i, qsid[i]);
    Serial.print("Wrote: ");
    Serial.println(qsid[i]);
  }
        
  Serial.println("writing eeprom pass:");
  for (int i = 0; i < qpass.length(); ++i){
    EEPROM.write(32 + i, qpass[i]);
    Serial.print("Wrote: ");
    Serial.println(qpass[i]);
  }
  EEPROM.commit();
}


/*----------------------------------------------------------
    Connect to AP and WiFi in WIFI_AP_STA and launch web 
  ----------------------------------------------------------*/
void createAPserver(){

  WiFi.mode(WIFI_STA);
  
  if(WiFi.status() != WL_CONNECTED){
    //AP Mode with no WiFi detected
    WiFi.disconnect();
    delay(100);

    Serial.println("");
    Serial.println("No WiFi Connection in AP MODE");
    Serial.println("Please verify your Network SSID name and password, and router connectivity");
  }
  else{
    Serial.println("");
    Serial.println("WiFi connected in AP MODE");
  }

  //access point 
  Serial.println("");
  Serial.println("Creating Accesspoint");
  WiFi.softAP(AP_ssid, "");
  Serial.print("Default IP address:\t");
  Serial.println(WiFi.softAPIP());

  //station part
  Serial.print("Connecting to...");
  Serial.println(ssid);
  Serial.print("with pass...");
  Serial.println(password);

  delay(10000);

  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
  Serial.println("WiFi Status: ");
  Serial.println(WiFi.status());

  generateBasicWebHtml();

  server.on("/", handleConnectionRoot);
  server.on("/instrucciones", handleConnectionInstructions);
  server.on("/configuracion", handleConnectionConfiguration);
  server.on("/enviar_configuracion", handleConnectionSendConfiguration);
  server.on("/enviar_wifi", handleConnectionSendWiFiConfiguration);
  server.on("/verificacion_wifi", handleConnectionVerificationWiFi);
  server.begin();

};


/*----------------------------------------------------------
    Create Basic HTML Content Pattern
  ----------------------------------------------------------*/
void generateBasicWebHtml(){
  
      //HTML CONTENT
      content_fixed_up = "<!DOCTYPE html>";
      content_fixed_up += "<html>";

      // HEAD
      content_fixed_up +="<head>";
      content_fixed_up +="<meta charset=\"UTF-8\">";
      content_fixed_up +="<meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">";
      content_fixed_up ="<title>Medidor C02  Configuraci&oacute;n</title>";
      content_fixed_up += "</head>";

      // STYLES
      content_fixed_up ="<style>"; 
      content_fixed_up +="html, body { height: 100%; margin: 0; } ";
      content_fixed_up +="body { background-color: black; color: white; font-family: 'Courier New', Courier, monospace; } ";
      content_fixed_up +="button { border: 1px white solid; color: white; background-color: black; padding: 15px; margin: 5px; font-family: 'Arial'; text-decoration: none; font-size: 13px; width: 135px; cursor: pointer;} ";
      content_fixed_up +="a button  { text-decoration: none; color: white; cursor: pointer; }";
      content_fixed_up +="div#mensajes{ padding: 15px; width: 100%; margin: 20px auto; text-align: center; } ";
      content_fixed_up +="div#mensajes ol { text-align: left; } ";
      content_fixed_up +=".fail { color: red; }";
      content_fixed_up +="a.link { color: orange; text-decoration: none;}";
      content_fixed_up +=".success{ color: green; } ";
      content_fixed_up +=" .yellow { color: rgba(255, 255, 0, 0.678); } ";
      content_fixed_up +="h1.unicolor, footer p { color: #1F7E97; text-align: center; } ";
      content_fixed_up +=".content { margin: 0 auto; width: 85%; min-height: 100%; text-align: center; } ";
      content_fixed_up +="footer { border-top: 1px solid #1F7E97; height: 50px; margin-top: -50px; padding: 0 20px; } ";
      content_fixed_up +="main { padding: 20px; padding-bottom: 50px; } ";
      content_fixed_up +="@media (min-width:1024px){ .content { width: 60%; } div#mensajes { width: 50%; } } ";
      content_fixed_up += "</style>";

      //BODY
      content_fixed_up +="<body>";
      content_fixed_up +="<div class=\"content\">";
      content_fixed_up +="<main>";
      content_fixed_up +="<h1 class=\"unicolor\">Medidor de CO2 Proyecto de Inalámbricas</h1>";
      content_fixed_up +="<a href=\"/instrucciones\"><button>Instrucciones</button></a>";
      content_fixed_up +="<a href=\"/configuracion\"><button >Configuraci&oacute;n</button></a>";
      content_fixed_up+="<div id=\"mensajes\">";
      content_fixed_up +="<br>";

      content_fixed_down ="</div> ";
      content_fixed_down +="</main>";
      content_fixed_down +="</div>";
      content_fixed_down +="<footer>";
      content_fixed_down +="<p>2021 - Proyecto Abierto Medici&oacute;n CO2 -  <b>UNICEN</b></p>";
      content_fixed_down +="</footer>";
      content_fixed_down +="</body>";
      content_fixed_down +="</html>";
  
}


/*----------------------------------------------------------
    192.168.4.1/ content & functionality
  ----------------------------------------------------------*/
void handleConnectionRoot(){
  Serial.println("Root access in Html Web Page");
  if(WiFi.status() != WL_CONNECTED){
  
      content_dynamic = "<p class=\"fail\">Su dispositivo no posee conexi&oacute;n a una red WiFi</p>";
      content_dynamic += "<p>Por favor lea las Instrucciones y luego configure su conexi&oacute;n dentro de las secci&oacute;n Configuraci&oacute;n</p>";

    Serial.println("No WiFi");
  }
  else{
      content_dynamic = "<p class=\"success\">Su dispositivo est&aacute; conectado a la Red WiFi : ";
      content_dynamic += ssid + "</p>";
      content_dynamic += "<p>Si desea cambiar de red, por favor lea las Instrucciones y luego configure su conexi&oacute;n dentro de Configuraci&oacute;n</p>";
    
  };
  content = content_fixed_up + content_dynamic + content_fixed_down;
  server.send(200, "text/html", content);
}


/*----------------------------------------------------------
    192.168.4.1/instrucciones content & functionality
  ----------------------------------------------------------*/
void handleConnectionInstructions(){
  Serial.println("Button Event \"Instrucciones\" in HtmlWeb Page");
    
    content_dynamic = "<h2>Instrucciones</h2>";
    content_dynamic += "<p>Siguiendo los siguientes pasos usted puede configurar su dispositivo para que se conecte a una nueva red WiFi o tambi&eacute;n puede cambiar de red WiFi.</p>";
    content_dynamic += "<ol><li>Ingrese en Configuraci&oacute;n</li>";
    content_dynamic += "<li>Introducza el usuario y contrase&ntilde;a del dispositivo (si no lo posee consulte al administrador o a qui&eacute;n lo suministr&oacute;).</li>";
    content_dynamic += "<li>Si el acceso a su dispostivo fue exitoso, debe seleccionar la red de WiFi que desea conectar el dispositivo y su contrase&ntilde;a.</li>";
    
    content_dynamic += "<li>Si su red y contrase&ntilde;a de WiFi es correcta su dispositivo queda configurado y conectado a la red seleccionada, luego de 10 segundos se reiniciar&ntilde;. Caso contrario vuelva a intentarlo.</li></ol>";
    content_dynamic += "<p>Recuerde que si usted est&aacute; viendo esta informaci&oacute;n es porque se ha conectado al dispositivo medidor.</p>";
    content = content_fixed_up + content_dynamic + content_fixed_down;

    if(WiFi.status() != WL_CONNECTED){
      Serial.println("No WiFi");
    }
    else{
      Serial.println("WiFi Connected");
    }

    server.send(200, "text/html", content);
}

/*----------------------------------------------------------
    192.168.4.1/configuracion content & functionality
  ----------------------------------------------------------*/
void handleConnectionConfiguration(){

  Serial.println("Button Event \"Configuracion\" in HtmlWeb Page");  
  
 
    content_dynamic = "<h2>Acceso al Dispositivo</h2>";
    content_dynamic += "<p>Ingrese credenciales del Dispositivo</p>";
    content_dynamic +="<form method='post' action='enviar_configuracion'>";
    content_dynamic += "<label for=\"local_board_user\">Usuario</label><br>";
    content_dynamic += "<input type=\"text\" name=\"local_board_user\"><br><br>";
    content_dynamic += "<label for=\"local_board_pass\">Contrase&ntilde;a</label><br>";
    content_dynamic += "<input type=\"password\" name=\"local_board_pass\"><br><br>";
    content_dynamic += "<button type=\"submit\">Acceder</button>";
    content_dynamic +="</form>";
    content = content_fixed_up + content_dynamic + content_fixed_down;
      
  server.send(200, "text/html", content);
}


/*----------------------------------------------------------
    192.168.4.1/enviar_configruracion functionality
  ----------------------------------------------------------*/
void handleConnectionSendConfiguration(){

   String local_board_user = server.arg("local_board_user");
   String local_board_pass = server.arg("local_board_pass");

   Serial.println("Usario Placa: " + local_board_user);
   Serial.println("Pass Placa: " + local_board_pass);

   if(local_board_pass == local_pass_esp32 && local_board_user == local_user_esp32){
    scanListNetworks();
    content_dynamic = "<h2>Configuraci&oacute;n WiFi Dispositivo</h2>";
    content_dynamic += "<p class='success'>Acceso Exitoso al dispositivo</p>";    
    content_dynamic += "<h3>Redes Disponibles</h3>";
    content_dynamic += netListHtml;

    content_dynamic +="<form method='post' action='enviar_wifi'>";
    content_dynamic +="<label for=\"wifi_name\">N&utilde;mero de su Red</label><br>";
    content_dynamic +="<input type=\"number\" min=\"1\" name=\"wifi_number\"><br><br>";
    content_dynamic +="<label for=\"wifi_pass\">Contrase&ntilde;a</label><br>";
    content_dynamic +="<input type=\"password\" name=\"wifi_pass\" length=64><br><br>";
    content_dynamic +="<button type=\"submit\">Enviar</button>";
    content_dynamic +="</form>";
  
  }
  else {
    content_dynamic = "<p class='fail'>Acceso Denegado</p>";
    content_dynamic += "<p class='fail'>Verifique usuario y/o contrase&ntilde;a de su dispositivo</p>";
    content_dynamic += "<p>Para volver a intentar vuelva a ingresar en Configuraci&oacute;n</p>";
  }

  Serial.println("Button Event \"enviar_configuracion\" in HtmlWeb Page");  
  
  content = content_fixed_up + content_dynamic + content_fixed_down;
      
  server.send(200, "text/html", content);
}


/*----------------------------------------------------------
    192.168.4.1/enviar_configruracion content & functionality
  ----------------------------------------------------------*/
void handleConnectionSendWiFiConfiguration(){

   String sid_number = server.arg("wifi_number");
   int qsid_number = sid_number.toInt();
   String qsid = WiFi.SSID(qsid_number-1);
   String qpass = server.arg("wifi_pass");

   Serial.println("Nombre de Red: " + qsid);
   Serial.println("Pass WiFi: " + qpass);

   writeEEPROM(qsid, qpass);

   Serial.println("Button Event \"enviar_configuracion_wifi\" in HtmlWeb Page");  

   WiFi.begin(qsid.c_str(), qpass.c_str());

   delay(5000);

   handleConnectionVerificationWiFi();

}

/*----------------------------------------------------------
    192.168.4.1/verificacion_wifi content & functionality
  ----------------------------------------------------------*/
void handleConnectionVerificationWiFi(){

  if(WiFi.status() != WL_CONNECTED){
    content_dynamic = "<p class='fail'>Su dispositivo medidor NO se ha podido conectar a su Red WiFi</p>";   
    content_dynamic += "<p class='fail'>Por favor verifque la contrase&ntilde;a y el estado de su router.</p>"; 
    content_dynamic += "<p class='fail'>Vuelva a intentarlo nuevamente ingresando a Configuraci&oacute;n</p>"; 
    content = content_fixed_up + content_dynamic + content_fixed_down;
    server.send(200, "text/html", content); 
  }
  else{
    content_dynamic = "<p class='success'>Su dispositivo medidor se ha conectado a su Red WiFi.</p>"; 
    content_dynamic += "<p>En 10 segundos se reiniciar&aacute; el dispostivo y se conectar&aacute; autom&aacute;ticamente a la red configurada.</p>"; 
    content = content_fixed_up + content_dynamic + content_fixed_down;
    server.send(200, "text/html", content);  
    delay(10000);
    WiFi.mode(WIFI_STA);
    Serial.println("Ingreso en modo STA");
    Serial.println("Se reiniciará ESP32");
    ESP.restart();
  };

}

/*----------------------------------------------------------
    Network Scan and network list generation
  ----------------------------------------------------------*/
void scanListNetworks(void){
  int n = WiFi.scanNetworks();
  Serial.println("scan done");
  if (n == 0)
    Serial.println("no networks found");
  else
  {
    Serial.print(n);
    Serial.println(" networks found");
    for (int i = 0; i < n; ++i)
    {
      // Print SSID and RSSI for each network found
      Serial.print(i + 1);
      Serial.print(": ");
      Serial.print(WiFi.SSID(i));
      Serial.print(" (");
      Serial.print(WiFi.RSSI(i));
      Serial.print(")");
      delay(10);
    }
  }
   totalNets = n;
   
  netListHtml = "<ol class=\"center\">";
  for (int i = 0; i < n; ++i)
  {
    // Print SSID and RSSI for each network found
    netListHtml += "<li>";
    netListHtml += WiFi.SSID(i);
    netListHtml += " (";
    netListHtml += WiFi.RSSI(i);
    netListHtml += ")";
    netListHtml += "</li>";
  }
  netListHtml += "</ol>";
}


/*----------------------------------------------------------
    MH-Z19-based CO2 meter setup
  ----------------------------------------------------------*/
void setup() {
  Serial.begin(9600);
  randomSeed((uint32_t)esp_random());

#ifdef HWSERIAL
  Serial2.begin(BAUDRATE, SERIAL_8N1, rx2_pin, tx2_pin);
  mhz19.begin(Serial2);
#else
  mySerial.begin(BAUDRATE);
  mhz19.begin(mySerial);
#endif

  mhz19.autoCalibration(false); // make sure auto calibration is off

  RGB_LEDSetup();

  setRGB_LEDColor (0, 0, 255);  // Blue means warming or Configuring:
                                //   baseline setting or calibrating

  WiFi.disconnect(); //commented v3

  EEPROM.begin(512); //Initialasing EEPROM
  delay(10);
  updateRGB_LED (true);         // Blink while connecting
  if (readEEPROM()) // Read params from EEPROM, if present
    connectWiFi_1();
  else {
    Serial.println ("Changing to Access Point mode..."); 
    createAPserver();    
    AP_MODE = true;
  }
  updateRGB_LED (false);

  // Init and get the time
  configTime(gmtOffset_sec, daylightOffset_sec, ntpServer);
  printLocalTime();

  Serial.println ("Warming will start during 3 minutes..."); 
  delay (180000); // Wait 3 minutes for warming purposes
  //delay (20000); // Wait 20 secondos for debug purposes

  retrieveInfo_mhz19 ();

  pinMode(button1.PIN, INPUT_PULLUP);
  attachInterrupt(button1.PIN, isr_button, CHANGE);
}


/*----------------------------------------------------------
    Manage the used interacion captured in the push button#include <HTTPClient.h>
  ----------------------------------------------------------*/
void btnManager_prov (int co2) {
  if (button1.event) {
      Serial.printf("Button has been pressed for %u millis\n", button1.timePressed);
      if (button1.timePressed < 1000)
        CO2_base = co2;
      else if (button1.timePressed < 3000) {
        localCalibration();
      }
        
      else {
        Serial.println ("Changing to Access Point mode..."); 
        createAPserver();    
        AP_MODE = true;
      }
      // button state updated inside a critical section
      portENTER_CRITICAL(&mux);
      button1.event = false;
      portEXIT_CRITICAL(&mux);
  } else if (button1.down)
    if (millis() - button1.timePressed > maxPressT) { // dismiss for time overruns (due to noise in the button pin)
      Serial.printf("Button was down for %u millis\n", millis() - button1.timePressed);
      portENTER_CRITICAL(&mux);
      button1.down = false;
      portEXIT_CRITICAL(&mux);
    }  
}

/*----------------------------------------------------------
    Local Calibration
  ----------------------------------------------------------*/

void localCalibration() {
    Serial.println ("Starting Manual Calibration..."); 
    
    remote_calibrate_state = -1; // state for local calibration, a negative value differs from remote calibration states (1 and 2).
    Serial.println("Starting local calibration during 20 minutes aprox....");
    calibrate_mhz19();
    remote_calibrate_state=0;
    Serial.println("Local calibration finished.");
}

/*----------------------------------------------------------
    Remote Calibration
  ----------------------------------------------------------*/

void remoteCalibration() {
  // Remote calibration is disabled for direct FastAPI ingestion.
}

/*----------------------------------------------------------
    Remote Restart
  ----------------------------------------------------------*/
void remoteRestart() {
  // Remote restart is disabled for direct FastAPI ingestion.
}

/*----------------------------------------------------------
    Remote Time Set
  ----------------------------------------------------------*/

void remoteTimeSet() {
  // Remote time set is disabled for direct FastAPI ingestion.
}

/*----------------------------------------------------------
    Send telemetry directly to the GreenCampus+ FastAPI backend
  ----------------------------------------------------------*/
bool sendSensorDataToApi(int co2ppm, int temp) {
  if (WiFi.status() != WL_CONNECTED) {
    Serial.println("FastAPI telemetry skipped: WiFi is not connected.");
    return false;
  }

  StaticJsonDocument<256> payload;
  payload["zone_id"] = 1;
  payload["temperature"] = temp;
  payload["humidity"] = random(40, 61);
  payload["co2_level"] = co2ppm;
  payload["energy_usage"] = random(100, 151);

  String requestBody;
  serializeJson(payload, requestBody);

  HTTPClient http;
  http.begin(SECRET_SERVER_URL);
  http.addHeader("Content-Type", "application/json");
  http.addHeader("X-API-Key", SECRET_IOT_API_KEY);

  int status = http.POST(requestBody);
  if (status > 0) {
    Serial.println("FastAPI telemetry HTTP status: " + String(status));
  } else {
    Serial.println("FastAPI telemetry failed: " + http.errorToString(status));
  }
  http.end();

  return status == 201 || status == 200;
}

/*----------------------------------------------------------
    MH-Z19 CO2 sensor loop
  ----------------------------------------------------------*/
void loop() {

  int co2ppm = mhz19.getCO2();          // Request CO2 (as ppm)
  int temp = mhz19.getTemperature();    // Request Temperature (as Celsius)
  struct tm timeinfo;  
  char buffer [25];

  btnManager_prov (co2ppm);
  
  if (!AP_MODE){
    // Measurements to computer for debugging purposes
    //
    //Serial.print("co2: ");
    Serial.print(co2ppm);
    //Serial.print("temp: ");
    Serial.print(",");
    Serial.println(temp);

    if (d%S==0){     // Telemetry is sent every S samplingPeriod seconds

   if (WiFi.status() != WL_CONNECTED)  connectWiFiModeSTA();
   
   if (WiFi.status() == WL_CONNECTED) {
      if(sendSensorDataToApi(co2ppm, temp)){
        Serial.println("Data sent to GreenCampus+ API.");
      }
      else{
        Serial.println("GreenCampus+ API communication failure.");
      }
 
   } else {
      // Measurements must be sent later when WiFi is available
      if (saved2send < MAX_MM) saved2send++;
      mm2send[saved2send-1].s_co2ppm = co2ppm;
      mm2send[saved2send-1].s_temp   = temp;
      if(!getLocalTime(&timeinfo)){
        Serial.println("Failed to obtain time");
        return;
      }
      mm2send[saved2send-1].s_timeinfo = timeinfo;
      Serial.println("Measurement saved for later registration in the IoT platform...");
   }
     
  } else { // Saved telemetry, if any, is sent
    if (WiFi.status() == WL_CONNECTED && saved2send > 0) {
      // Example: "2017-01-12 13:22:54-05"
      strftime (buffer,25,"%F %T-03",&(mm2send[saved2send-1].s_timeinfo)); // Example "2017-01-12 13:22:54-05"

      if(sendSensorDataToApi(mm2send[saved2send-1].s_co2ppm, mm2send[saved2send-1].s_temp)){
        Serial.print("Datos guardados anteriormente enviados a GreenCampus+ API: "); Serial.println(buffer);
        if (saved2send > 0) saved2send--;
      }
     }
  }
    d++;

    CO2RGB_LED(co2ppm);

    delay(samplingPeriod);
  } 
  
  else { // Meter in Access Point mode
    Serial.println("AP mode"); // for debug
    server.handleClient();
  }


}
