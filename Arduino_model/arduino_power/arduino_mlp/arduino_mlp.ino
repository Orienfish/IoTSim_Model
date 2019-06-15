/*********************************************************************
 * Simple script to test power, performance and temperature of Arduino
 * For performance, we measure the execution time of running MLP
 * based on Neurona library.
 * For temperature, we use the built-in temperature sensor
 * Author: Orienfish
 * Date: 6/10/2019
 */

#include <Neurona.h>
#include <SoftwareSerial.h>

/* Specify which serial to use */
// #define mySerial Serial1
SoftwareSerial mySerial(3, 2); /* RX:D3, TX:D2 */

/* The pin receive start signal from and send end signal to RPi */
/* Synchronization is required for power measurement */
#define START_SIG_PIN 12
#define END_SIG_PIN 13

/* Test times */
#define RUN_TIME 400

/* Record start, end and temperature measure time */
unsigned long stime, etime, temptime;

/* Define the network structure */
#define NET_INPUTS 200
#define HIDDEN_LAYER_1 20
#define HIDDEN_LAYER_2 20
// #define HIDDEN_LAYER_3 20
#define NET_OUTPUTS 10
int layerSizes[] = {HIDDEN_LAYER_1, HIDDEN_LAYER_2, NET_OUTPUTS, -1};
/* PROGMEM: store data in flash. The number of weights can be more or less than the network requirement */
double PROGMEM const initW[] = {2.753086,-11.472257,-3.311738,16.481226,19.507006,20.831778,7.113330,-6.423491,1.907215,6.495393,-27.712126,26.228203,-0.206367,-5.724560,-22.278070,
30.065610,6.139262,-10.814282,28.513130,-9.784946,6.467021,0.055005,3.730361,4.145092,2.479019,0.013003,-3.582416,-16.364391,14.133357,-5.089288,1.637492,5.894826,1.415764,-3.315533,14.814289,
-20.906571,-1.568656,1.917658,4.910184,4.039419,-10.848469,-5.641680,-4.132432,10.711442,3.759935,19.507702,17.728724,-3.210244,-2.476992,8.988450,5.196827,2.636043,17.357207,2.005429,11.713386,
-5.453253,-6.940325,10.752005,0.666605,-7.266082,-3.587120,-9.921817,-12.682059,-15.456143,-13.740927,0.508265,15.179410,-11.143178,-19.085120,1.251235,22.006491,-4.227328,-0.444516,3.589025,0.649661,
13.675598,-13.026884,-11.229070,-15.300703,-1.718191,6.737973,-28.176802,-2.505471,5.197970,7.007983,-2.869269,3.650349,18.029204,4.098356,10.481188,-2.566311,9.927770,2.344936,4.524327};
double netInput[] = {-1.0, 200.0, 75.0, 114.0};
/* Init MLP */
MLP mlp(NET_INPUTS,NET_OUTPUTS,layerSizes,MLP::LOGISTIC,initW,true);

/*
 * Access the internal temperature sensor
 */
int readTemperature() 
{
 ADCSRA |= _BV(ADSC); // start the conversion
 while (bit_is_set(ADCSRA, ADSC)); // ADSC is cleared when the conversion finishes
 return (ADCL | (ADCH << 8)) - 342; // combine bytes & correct for temp offset (approximate)} 
}

/*
 * Read average temperature
 * 500 measurements will take 85ms
 */
float averageTemperature()
{
 readTemperature(); // discard first sample (never hurts to be safe)

 float averageTemp; // create a float to hold running average
 for (int i = 1; i < 500; i++) // start at 1 so we dont divide by 0
   // get next sample, calculate running average
   averageTemp += ((readTemperature() - averageTemp)/(float)i);

 return averageTemp; // return average temperature reading
}

/*
 * Timer interrupt
 */
ISR(TIMER1_COMPA_vect)
{
  temptime = millis();
  mySerial.print(averageTemperature());
  mySerial.print(",");
  mySerial.print(temptime - stime);
  mySerial.print("\n");
}

/*
 * setup
 */
void setup(){
    mySerial.begin(115200);
    pinMode(START_SIG_PIN, INPUT);
    pinMode(END_SIG_PIN, OUTPUT);
    digitalWrite(END_SIG_PIN, LOW); // Init end_sig_pin to low

    /* init timer for 10Hz */
    // initialize timer1 
    noInterrupts();
    TCCR1A = 0;
    TCCR1B = 0;
    TCNT1  = 0; // init counter value to 0
    OCR1A = 12500; // compare match register 16MHz/256/5Hz
    TCCR1B |= (1 << WGM12); // CTC mode
    TCCR1B |= (1 << CS12); // 256 prescaler 
    // TIMSK1 |= (1 << OCIE1A); // enable timer compare interrupt
    interrupts();
    
    /* init internal temperature sensor */
    // turn on internal reference, right-shift ADC buffer, ADC channel = internal temp sensor
    ADMUX = 0xC8;
    // wait for the analog reference to stabilize
    delay(10);
}

/*
 * loop
 */
void loop(){
    /* Wait for the trigger start signal from RPi */
    mySerial.print("Waiting for start signal...\n");
    // while (digitalRead(START_SIG_PIN) == 0);
    /* start timing */
    TIMSK1 |= (1 << OCIE1A); // enable timer compare interrupt
    stime = millis();

    /* Running MLP */
    for (int i = 0; i < RUN_TIME; ++i) {
        int res = mlp.getActivation(netInput);
        // mySerial.print(res); // will cost 100ms in total
    }
    
    /* Stop timing and stop power measurement */
    digitalWrite(END_SIG_PIN, HIGH);
    etime = millis();
    TIMSK1 = 0; // disable timer interrupt
    mySerial.println(etime - stime);

    while(1);
}
