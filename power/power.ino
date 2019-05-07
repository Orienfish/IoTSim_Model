#include <Neurona.h>
#include <SoftwareSerial.h>

/* Specify which serial to use */
// #define mySerial Serial1
SoftwareSerial mySerial(3, 2); /* RX:D3, TX:D2 */

/* The pin receive start signal from and send end signal to RPi */
#define START_SIG_PIN 12
#define END_SIG_PIN 13

/* Test times */
#define RUN_TIME 1000

/* Record start and end time */
unsigned long stime, etime;

/* Define the network structure */
#define NET_INPUTS 3
#define HIDDEN_LAYER_1 20
#define HIDDEN_LAYER_2 20
#define HIDDEN_LAYER_3 20
#define NET_OUTPUTS 10
int layerSizes[] = {HIDDEN_LAYER_1, HIDDEN_LAYER_2, HIDDEN_LAYER_3, NET_OUTPUTS, -1};
/* PROGMEM: store data in flash. The number of weights can be more or less than the network requirement */
double PROGMEM const initW[] = {2.753086,-11.472257,-3.311738,16.481226,19.507006,20.831778,7.113330,-6.423491,1.907215,6.495393,-27.712126,26.228203,-0.206367,-5.724560,-22.278070,
30.065610,6.139262,-10.814282,28.513130,-9.784946,6.467021,0.055005,3.730361,4.145092,2.479019,0.013003,-3.582416,-16.364391,14.133357,-5.089288,1.637492,5.894826,1.415764,-3.315533,14.814289,
-20.906571,-1.568656,1.917658,4.910184,4.039419,-10.848469,-5.641680,-4.132432,10.711442,3.759935,19.507702,17.728724,-3.210244,-2.476992,8.988450,5.196827,2.636043,17.357207,2.005429,11.713386,
-5.453253,-6.940325,10.752005,0.666605,-7.266082,-3.587120,-9.921817,-12.682059,-15.456143,-13.740927,0.508265,15.179410,-11.143178,-19.085120,1.251235,22.006491,-4.227328,-0.444516,3.589025,0.649661,
13.675598,-13.026884,-11.229070,-15.300703,-1.718191,6.737973,-28.176802,-2.505471,5.197970,7.007983,-2.869269,3.650349,18.029204,4.098356,10.481188,-2.566311,9.927770,2.344936,4.524327};
double netInput[] = {-1.0, 200.0, 75.0, 114.0};
/* Init MLP */
MLP mlp(NET_INPUTS,NET_OUTPUTS,layerSizes,MLP::LOGISTIC,initW,true);

/* Factorial function */
float factorial(unsigned int i)
{
   if(i <= 1)
   {
      return 1;
   }
   return i * factorial(i - 1);
}

/*
 * setup
 */
void setup(){
    mySerial.begin(115200);
    pinMode(START_SIG_PIN, INPUT);
    pinMode(END_SIG_PIN, OUTPUT);
    digitalWrite(END_SIG_PIN, LOW); // Init end_sig_pin to low
}

/*
 * loop
 */
void loop(){
    /* Wait for the trigger start signal from RPi */
    mySerial.print("Waiting for start signal...");
    while (digitalRead(START_SIG_PIN) == 0);
    /* start timing */
    stime = millis();

    /* Test 1: Running MLP */
    // for (int i = 0; i < RUN_TIME; ++i) {
    //    int res = mlp.getActivation(netInput);
        // mySerial.print(res); // will cost 100ms in total
    //}

    /* Test 2: Being idle for 30 secs*/
    // delay(30000);

    /* Test 3: Running simple loop of calculations */
    for (int i = 0; i < 5000; ++i)
      float f = factorial(200);
    
    /* Stop timing and stop power measurement */
    digitalWrite(END_SIG_PIN, HIGH);
    etime = millis();    
    mySerial.println(etime - stime);
    while(1);
}
