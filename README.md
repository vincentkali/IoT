# IoT
## System Function
To simulate the `Smart Home Alert System`, we use the RFID system to identify the person, and determine he/she can into house or not.

If the person has right into the house, then green LED will light up.

Otherwise, the red LED will light up, the buzzer will buss, the camera will take the picture of the intruder.
The picture will send to all the members living in this house via `Line Notify`.

In this system we use the `AWS MCS` to store the RFID information and communicate between the RFID sensor and the alert system (camera, LED, and buzzer).
## Machine Used
- Smart Home Alert System: `Raspberry Pi`
- RFID Writing: `Arduino`
## Demo Vedio
- Function explain: https://youtu.be/WOp3YRcxKCw
- IoT system demo: https://www.youtube.com/watch?v=WOp3YRcxKCw#t=3m28s  
- Read/Write UID on RFID (using arduino): https://www.youtube.com/watch?v=WOp3YRcxKCw#t=3m48s
## Final Report
- https://github.com/vincentkali/IoT/blob/master/final/IoT-Final-report.pdf
