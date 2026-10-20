
const int LED_START = 3;
const int LED_COUNT = 10;

void setup() {
  // Initialiser les 10 broches en sortie
  for (int i = 0; i < LED_COUNT; i++) {
    pinMode(LED_START + i, OUTPUT);
    digitalWrite(LED_START + i, LOW);
  }
}

void loop() {
  // Chenillard : une LED allumee a la fois
  for (int i = 0; i < LED_COUNT; i++) {
    digitalWrite(LED_START + i, HIGH);
    delay(100);
    digitalWrite(LED_START + i, LOW);
  }
}
