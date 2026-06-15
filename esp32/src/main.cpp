#include <Arduino.h>

#define LED_PIN 2
#define BUZZER_PIN 4

struct Vehicle {
  String vehicleID;
  String driverID;
  float latitude;
  float longitude;
};

Vehicle fleet[] = {

  {"TRUCK_101", "DRIVER_01", 19.9975, 73.7898},
  {"TRUCK_102", "DRIVER_02", 19.9980, 73.7903},
  {"BUS_201",   "DRIVER_03", 19.9990, 73.7910},
  {"VAN_301",   "DRIVER_04", 20.0000, 73.7920}

};

const int vehicleCount =
  sizeof(fleet) / sizeof(fleet[0]);

void setup() {

  Serial.begin(115200);

  pinMode(LED_PIN, OUTPUT);
  pinMode(BUZZER_PIN, OUTPUT);

  Serial.println("================================");
  Serial.println("SMART FLEET TRACKING SYSTEM");
  Serial.println("4 VEHICLES CONNECTED");
  Serial.println("================================");
}

void loop() {

  for (int i = 0; i < vehicleCount; i++) {

    fleet[i].latitude += random(1, 6) * 0.0001;
    fleet[i].longitude += random(1, 6) * 0.0001;

    int speed = random(20, 90);

    String ignition = "ON";

    String status = "SAFE";

    if (fleet[i].latitude > 20.0020) {
      status = "GEOFENCE_ALERT";
    }

    if (fleet[i].latitude > 20.0050) {

      status = "THEFT_ALERT";

      digitalWrite(LED_PIN, HIGH);
      digitalWrite(BUZZER_PIN, HIGH);

    } else {

      digitalWrite(LED_PIN, LOW);
      digitalWrite(BUZZER_PIN, LOW);
    }

    Serial.print(fleet[i].vehicleID);
    Serial.print(",");

    Serial.print(fleet[i].driverID);
    Serial.print(",");

    Serial.print(fleet[i].latitude, 6);
    Serial.print(",");

    Serial.print(fleet[i].longitude, 6);
    Serial.print(",");

    Serial.print(speed);
    Serial.print(",");

    Serial.print(ignition);
    Serial.print(",");

    Serial.println(status);
  }

  Serial.println("--------------------------------");

  delay(3000);
}