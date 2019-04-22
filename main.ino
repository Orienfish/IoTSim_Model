/*******************************************************************
 * Project: Performance Counter of Arduino
 * Description: A software frame that counts the cycles of execution
 *              using Timer 1 and interrupts.
 * Board: Arduino Uno R3
 * Author: Orienfish
 * Date: 04/22/2019
 ******************************************************************/
extern "C" {
	#include <perf_count.h>
}

/* Counter frequency */
extern unsigned long cnt_freq = IO_FREQ / SCALER;
/* Performance count */
extern volatile unsigned long count = 0;

void setup() {
	/* start serial at 115200 baud rate */
	Serial.begin(115200);
	/* Init Timer 1 */
	Timer1_init(SCALER);
}

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
