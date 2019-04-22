/*******************************************************************
 * Project: Performance Counter of Arduino
 * Description: A software frame that counts the cycles of execution
 *              using Timer 1 and interrupts.
 * Board: Arduino Uno R3
 * Author: Orienfish
 * Date: 04/22/2019
 ******************************************************************/
#define IO_FREQ 16000000
#define SCALER 1
#define OVERFLOW 1 << 16

/* Counter frequency */
unsigned long cnt_freq = IO_FREQ / SCALER;
/* Performance count */
volatile unsigned long count = 0;

/******************************************************************
 * Set up Timer 1 on Arduino Uno
 *****************************************************************/
void Timer1_init(int scaler) {
  /* Configure the normal mode */
  TCCR1A = 0;
  TCCR1B = 0;
  /* Set frequency scaler */
  byte scaler_mask = 0;
  switch(scaler) {
    case 1: scaler_mask = 0x01; break;
    case 8: scaler_mask = 0x02; break;
    case 64: scaler_mask = 0x03; break;
    case 256: scaler_mask = 0x04; break;
    case 1024: scaler_mask = 0x05; break;
    default: break;
  }
  TCCR1B |= scaler_mask;
  Serial.print("Scaler is "); Serial.println(SCALER);
  Serial.print("Counter frequency is "); Serial.println(cnt_freq);
  Serial.flush();
  /* Set counter to 0 */
  TCNT1 = 0;
  /* Enable overflow interrupt */
  TIMSK1 = (1 << TOIE1);
}

/*****************************************************************
 * Interrupt service called when timer 1 overflows
 ****************************************************************/
ISR(TIMER1_OVF_vect) {
  count ++;
}

/*****************************************************************
 * Read Timer 1 count
 ****************************************************************/
unsigned int TIM16_ReadTCNT1(void) {
  unsigned char sreg;
  unsigned int i;
  /* Save global interrupt flag */
  sreg = SREG;
  /* Disable interrupts */
  cli();
  /* Read TCNT1 */
  i = TCNT1;
  /* Restore global interrupt flag */
  SREG = sreg;
  return i;
}

/*****************************************************************
 * Setup
 ****************************************************************/
void setup() {
	/* start serial at 115200 baud rate */
	Serial.begin(115200);
	/* Init Timer 1 */
	Timer1_init(SCALER);
}

/*****************************************************************
 * Main loop
 ****************************************************************/
void loop() {
  /* Timer 1 starts from here */
  // TCNT1 = 0;
  /*********************************************************************************************
	 * Measured process - insert your code here.
	 *********************************************************************************************/
	for (int i = 0; i < 5000; ++i)
		delayMicroseconds(800);
  /*********************************************************************************************
   * End of measured process
   *********************************************************************************************/

	/* Disable Timer 1 */
	TCCR1B = 0;
	/* Compute execution time */
  Serial.print("Global count is "); Serial.println(count);
  Serial.print("Timer 1 count is "); Serial.println(TIM16_ReadTCNT1());
	float time = float(count * OVERFLOW) / cnt_freq;
	time += float(TIM16_ReadTCNT1()) / cnt_freq;
	Serial.print("Time (s): "); Serial.println(time, 5);

	/* Stop here */
	while(1);
}
