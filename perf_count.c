// perf_count.c
#include <perf_count.h>

/* Counter frequency */
unsigned long cnt_freq = IO_FREQ / SCALER;
/* Performance count */
volatile unsigned long count = 0;

/*
 * Set up Timer 1 on Arduino Uno
 */
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

/*
 * Interrupt service called when timer 1 overflows
 */
ISR(TIMER1_OVF_vect) {
	count ++;
}

/*
 * Read Timer 1 count
 */
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
