unsigned long time_after;
unsigned long dernier_tick=0;
unsigned  long dernier_passage = 0;
void setup() {
  Serial.begin(115200);
}
void loop() {
  time_after = micros();
  if (time_after - dernier_tick>=5000){
    Serial.println(time_after-dernier_passage);
    dernier_tick = 5000 + dernier_tick;
    dernier_passage = time_after;
  }
}