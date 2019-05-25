#include <ESP8266WiFi.h> // Enables the ESP8266 to connect to the local network (via WiFi)
#include <PubSubClient.h> // Allows us to connect to, and publish to the MQTT broker

/* WiFi configuration */
const char* ssid = "kazim";
const char* wifi_password = "3XQZ5zRU";

/* MQTT configuration */
const char* mqtt_server = "10.42.0.1";
const char* mqtt_topic = "house.hand1";
const char* mqtt_username = "admin";
const char* mqtt_password = "IBMProject$";
// The client id identifies the ESP8266 device. Think of it a bit like a hostname (Or just a name, like Greg).
const char* clientID = "henrykuo2";
int datanumber = 1;
String msg = " 84.0 33.8125 -0.441517 9.70651 1.65569 -0.291929 9.74659 1.93582 -0.08225489999999999 0.030719099999999996 0.00182645 -2.2002200000000003 -27.5448 -4.8308800000000005 0.170098 -0.12753299999999998 -0.611826 -0.761887 37.3125 1.96143 9.1393 -3.90141 1.9028200000000002 9.06 -3.48083 0.028018599999999998 0.0126067 0.00947727 -4.80225 -20.364 6.2331199999999995 0.39823400000000003 -0.463178 0.6918770000000001 0.384945 34.6875 9.58716 -1.5205799999999998 -2.6482900000000003 9.60768 -1.49797 -1.8993200000000001 0.00612525 -0.0074759 0.00510149 -11.2686 -5.692 21.7639 0.0715938 -0.747033 0.202995 -0.628975";
char charcontent[1500];
String temp;
char cstr[500];

/* Record start and end time */
unsigned long stime, etime;

// Initialise the WiFi and MQTT Client objects
WiFiClient wifiClient;
PubSubClient client(mqtt_server, 1883, wifiClient); // 1883 is the listener port for the Broker

void setup() {
    // Begin Serial on 115200
    // Remember to choose the correct Baudrate on the Serial monitor!
    // This is just for debugging purposes
    Serial.begin(115200);
    
    pinMode(16, OUTPUT);
    Serial.print("Connecting to ");
    Serial.println(ssid);
  
    // Connect to the WiFi
    WiFi.begin(ssid, wifi_password);
  
    // Wait until the connection has been confirmed before continuing
    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        Serial.print(".");
    }

    // Debugging - Output the IP Address of the ESP8266
    Serial.println("WiFi connected");
    Serial.print("IP address: ");
    Serial.println(WiFi.localIP());
  
    // Connect to MQTT Broker
    // client.connect returns a boolean value to let us know if the connection was successful.
    // If the connection is failing, make sure you are using the correct MQTT Username and Password (Setup Earlier in the Instructable)
    if (client.connect(clientID, mqtt_username, mqtt_password)) {
        Serial.println("Connected to MQTT Broker!");
    }
    else {
        Serial.println("Connection to MQTT Broker failed...");
    }
}

void loop() {
    // Concatenate data number with message ---> message = "data_number" + "message"  
    String spacecontent = "";
    itoa(datanumber, cstr, 10);
    spacecontent.concat(cstr);
    spacecontent.concat(msg);
    spacecontent.toCharArray(charcontent,sizeof(charcontent));

    /* Trigger the power measurement and start timing */
    digitalWrite(16, HIGH);
    stime = millis();
    if (client.publish(mqtt_topic, charcontent)){
        /* Stop timing and stop power measurement */
        etime = millis();
        digitalWrite(16, LOW); 
        Serial.print("Message sent (ms):");
        Serial.println(etime - stime);
    } 
    else {
        Serial.println("Message failed to send. Reconnecting to MQTT Broker and trying again");
    }
    client.connect(clientID, mqtt_username, mqtt_password);
    delay(2000); // This delay ensures that client.publish doesn't clash with the client.connect call
    datanumber = datanumber +1;
}
