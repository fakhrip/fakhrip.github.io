#include <LiquidCrystal.h>

const int rs = 12, en = 11, d4 = 10, d5 = 9, d6 = 8, d7 = 7, d1 = 4, d2 = 3, d3 = 2;
LiquidCrystal lcd(rs, en, d4, d5, d6, d7);

int val1 = 0, val2 = 0, val3 = 0;
int result = 0;

void setup() {
  pinMode(d1, INPUT);
  pinMode(d2, INPUT);
  pinMode(d3, INPUT);
  
  lcd.begin(16, 2);
}

void loop() {
  lcd.setCursor(0, 0);
  
  val1 = digitalRead(d1);
  val2 = digitalRead(d2);
  val3 = digitalRead(d3);
  lcd.print("Light");
  
  lcd.setCursor(0, 1); 
  char buffer[10];
  result = abs(8 - ((val1*4) +(val2*2)+ val3));
  sprintf(buffer,"Level = %d", result);
  lcd.print(buffer);
}
