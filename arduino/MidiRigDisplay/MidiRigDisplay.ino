/* Copyright (C) 2015-2017 Patrik Jonasson - All Rights Reserved 
*
 *
 * This file is part of MidiRig.
 *
 * MidiRig is free software: you can redistribute it and/or modify it  
* under the terms of the GNU General Public License as published by  
* the Free Software Foundation, either version 3 of the License,  
* or (at your option) any later version. 
*
 * MidiRig is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
 * without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.   
* See the GNU General Public License for more details. 
*
 * You should have received a copy of the GNU General Public License along with MidiRig.
 * If not, see <http://www.gnu.org licenses/>. */

/*
  The circuit:
   LCD RS pin to digital pin 12
   LCD Enable pin to digital pin 13
   LCD D4 pin to digital pin A0
   LCD D5 pin to digital pin A1
   LCD D6 pin to digital pin A2
   LCD D7 pin to digital pin A3
   LCD R/W pin to ground
   LCD VSS pin to ground
   LCD VCC pin to 5V
   10K resistor:
   ends to +5V and ground
   wiper to LCD VO pin (pin 3)

*/

// include library code:
#include <LiquidCrystal.h>
#include <SevenSeg.h>
#include <Wire.h>

const int NONE = 0;
const int ONE_ON = 1;
const int ONE_OFF = 2;
const int TWO_ON = 3;
const int TWO_OFF = 4;
const int ALL = 5;

#define SLAVE_ADDRESS 0x04

// initialize the LCDlibrary with the numbers of the interface pins
const int RS = 10;
const int EN = 11;
const int D4 = 12;
const int D5 = 13;
const int D6 = A0;
const int D7 = A1;
LiquidCrystal lcd(RS, EN, D4, D5, D6, D7);


//Seven segment display
const int A = 6;//6
const int B = 7;//7
const int C = A3;//3
const int D = A2;//2
const int E = 2;//10
const int F = 5;//5
const int G = 4;//5

const int DIGIT_1 = 3;//11
const int DIGIT_2 = 9;//8
const int DIGIT_3 = 8;//9

SevenSeg disp(A, B, C, D, E, F, G);
const int numOfDigits = 3;
int digitPins[numOfDigits] = {DIGIT_1, DIGIT_2, DIGIT_3};


//MIDIRIG I2C COMMANDS
const int UPDATE_SEVEN_SEG_NUMBER = 0;
const int UPDATE_LCD_ROW1 = 1;
const int UPDATE_LCD_ROW2 = 2;
const int CLEAR_LCD = 3;
const int UPDATE_SEVEN_SEG_TEXT = 4;


const int ROW1 = 0;
const int ROW2 = 1;

const byte ACK = byte(0);
const byte ERR = byte(1);

const int SEVEN_SEG_TEXT_MODE = -1;

int sevenSegNumValue = SEVEN_SEG_TEXT_MODE;
String sevenSegTxtValue = String("---");

void setup() {  
  // set up the LCD's number of columns and rows:
  lcd.begin(16, 2);
  lcd.clear();
  updateLCD(ROW1, "MIDIRig");
  updateLCD(ROW2, "starting system");
  // set up the seven segment display with number of digits and digit pins
  disp.setDigitPins(numOfDigits, digitPins);
  // set up  the type of the seven segment display
  disp.setCommonCathode();

  //
  Wire.begin(SLAVE_ADDRESS);
  Wire.onReceive(handleI2CEvent);
}

void loop() {

  //constantly refresh seven segment display
  switch (sevenSegNumValue) {
    case SEVEN_SEG_TEXT_MODE:
      disp.write(sevenSegTxtValue);
      break;
    default:
      disp.write(sevenSegNumValue);
  }
}

void handleI2CEvent(int byteCount) {
  int cmd = Wire.read();
  switch (cmd) {
    case UPDATE_SEVEN_SEG_NUMBER:
      sevenSegNumValue = readBytesToInt();
      Wire.write(ACK);
      break;
    case CLEAR_LCD:
      clearLCD();
      Wire.write(ACK);
      break;
    case UPDATE_LCD_ROW1:
      { String r1 = "";
        readStr(r1);
        updateLCD(ROW1, r1);
        Wire.write(ACK);
        break;
      }
    case UPDATE_LCD_ROW2:
      { String r2 = "";
        readStr(r2);
        updateLCD(ROW2, r2);
        Wire.write(ACK);
        break;
      }
    case UPDATE_SEVEN_SEG_TEXT:
      { String txt = "";
        readStr(txt);
        sevenSegTxtValue =  (txt.length() > 3) ? txt.substring(0, 3) : txt;
        sevenSegNumValue = SEVEN_SEG_TEXT_MODE;
        Wire.write(ACK);
        break;
      }

    default:
      lcd.clear();
      updateLCD(ROW1, "Unknown command");
      Wire.write(ERR);
      break;
  }
}


int readBytesToInt() {
  int multiplier = 0;
  int input = 0;
  int result = 0;
  while (Wire.available()) {
    input = Wire.read() << multiplier;
    result += input;
    multiplier += 8;
  }
  return result;
}

void readStr(String &str) {
  while (Wire.available()) {
    str += char(Wire.read());
  }
}

void updateLCD(int row, String str) {
  lcd.setCursor(0, row);
  lcd.print(str);
}

void clearLCD() {
  if (Wire.available()) {
    switch (Wire.read()) {
      case ROW1:
        updateLCD(ROW1, "                ");
        break;
      case ROW2:
        updateLCD(ROW2, "                ");
        break;
      default:
        lcd.clear();
    }
  }
}


