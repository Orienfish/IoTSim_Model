// perf_count.h
#ifndef _PERF_COUNT_h
#define _PERF_COUNT_h

#define IO_FREQ 16000000
#define SCALER 1
#define OVERFLOW 1 << 16

void Timer1_init(int scaler);
ISR(TIMER1_OVF_vect);
unsigned int TIM16_ReadTCNT1(void);

#endif