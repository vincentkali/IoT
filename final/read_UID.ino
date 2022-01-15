#include <SPI.h>
#include <MFRC522.h>     
 
#define RST_PIN      9       
#define SS_PIN       10      
 
MFRC522 mfrc522(SS_PIN, RST_PIN);  
 
void setup() {
  Serial.begin(9600);
  Serial.println("RFID reader is ready!");
 
  SPI.begin();
  mfrc522.PCD_Init();   
}
 
void loop() {
    // make sure whether there is a new card
    if (mfrc522.PICC_IsNewCardPresent() && mfrc522.PICC_ReadCardSerial()) {
      byte *id = mfrc522.uid.uidByte;   // read the UID 
      byte idSize = mfrc522.uid.size;   // get UID length
 
      Serial.print("PICC type: ");      // display card type
      MFRC522::PICC_Type piccType = mfrc522.PICC_GetType(mfrc522.uid.sak);  
      Serial.println(mfrc522.PICC_GetTypeName(piccType));
 
      Serial.print("UID Size: ");       // display UID length
      Serial.println(idSize);
 
      for (byte i = 0; i < idSize; i++) {  // display UID with hex
        Serial.print("id[");
        Serial.print(i);
        Serial.print("]: ");
        Serial.println(id[i], HEX);       
      }
      Serial.println();
      mfrc522.PICC_HaltA();  // halt mode
    } 
}
