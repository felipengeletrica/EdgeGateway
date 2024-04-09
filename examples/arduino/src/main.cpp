#include <Arduino.h>

void setup() {
  Serial.begin(115200);
}

void loop() {
  #ifndef GPS_TEST
    Serial.println("Arduino data");
    delay(1000);
  #endif

  #ifdef GPS_TEST
    Serial.println("$GPRMC,170904.935,V,3854.928,N,07702.497,W,78.4,1.83,021116,,E*42");
    delay(1000);

    Serial.println("$GPGGA,170905.935,3854.928,N,07702.497,W,0,00,,,M,,M,,*55");
    delay(1000);

    Serial.println("$GPGLL,3854.928,N,07702.497,W,170906.935,V*36");
    delay(1000);

    Serial.println("$GPGSA,A,2,14,12,04,16,17,11,,,,,,,0.1,0.0,0.9*38");
    delay(1000);

    Serial.println("$GPGSV,2,1,06,14,14,200,30,12,43,040,43,04,79,266,23,16,15,261,82*7F");
    delay(1000);

    Serial.println("$GPGSV,2,2,06,17,88,095,74,11,39,185,73*74");
    delay(1000);

    Serial.println("$GPRMC,170910.935,V,3854.926,N,07702.497,W,52.2,1.90,021116,,E*45");
    delay(1000);

    Serial.println("$GPGGA,170911.935,3854.926,N,07702.497,W,0,04,0.0,,M,,M,,*74");
    delay(1000);

    Serial.println("$GPGLL,3854.926,N,07702.497,W,170912.935,V*3D");
    delay(1000);

    Serial.println("$GPGSA,A,3,14,12,04,16,17,11,,,,,,,0.4,0.3,0.6*30");
    delay(1000);
  #endif
}