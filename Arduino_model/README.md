# Arduino CPU Power Model
In this experiment, we establish a CPU power model for Arduino while running various size of MLP. The implementation Of MLP is based on the [Neurona Library](https://www.arduinolibraries.info/libraries/neurona).

## Hardware Setup
We use a RPi to read power traces from the [HIOKI 3334 Powermeter](https://www.hioki.com/en/products/detail/?product_key=5812). The Arduino is powered by a wire connected to the powermeter, thus the power traces can be collected. The circuit connection is shown as following;
<div align=center><img width="800" height="400" src="https://github.com/Orienfish/IoTSim_Model/blob/master/Arduino_model/setup.png"/></div>

Two signals: END_SIG and START_SIG are employed for synchronization. 
- START_SIG is a rising signal sent by RPi to trigger the workload on Arduino. With a pull-down resistor, the voltage level on GPIO12 of RPi and pin 12 on Arduino will be set to 0 when nothing happens. Arduino waits until the input voltage of pin 12 becomes high, and then starts running workload. RPi also starts reading from Power Measure instrument at the same time.
- END_SIG is a rising signal sent by Arduino to notice RPi of the end of execution. Because the output voltage of Arduino is 5V while the operating voltage of RPi is 3.3V, resistors are used to match the voltage on two pins. Besides, the 2k resistor also acts as a pull-down resistor, which can eliminate noise on the wire. RPi will stop measurement once detects the high voltage input.

Arduino is powered by the battery port. Alternative serial port of pin 2 and 3 are used to send out time and temperature information. A USB-TTL adapter is used to read the information on desktop.

Real wire connections are shown in the following picture:
<div align=center><img width="400" height="400" src="https://github.com/Orienfish/IoTSim_Model/blob/master/Arduino_model/wire.jpeg"/></div>

## Software Setup
All the scripts for every device can be found in 
- arduino_mlp/arduino_mlp.ino runs on the Arduino.
- rpi/serial_measurement_once.py runs on the RPi.
- pwr_perf_temp_data folder contains the raw text files.

To run the experiment, there are several steps:
- upload the program to Arduino, make sure that the output of Arduino can be read by USB-TTL on the laptop.
- connect Arduino to the powermeter.
- when `Waiting for start signal...` displaying on the serial port of the laptop, start `serial_measurement_once.py` on the measuring RPi.
- the power trace will be automically stored on RPi, while the time and temperature data need to be copied from the serial port of the laptop to a text file.

## Processing Data

One text file contains the power/temperature trace during running one workload. For example, `pwr_10_1.txt` contains the power trace of running MLP with 10 inputs and 1 hidden layers. The nodes in one hidden layer is fixed to 20.

A processing script `process.py` in this folder is responsible for getting total energy consumption and average power consumption from the raw data files. To process each power trace in the folder, simply run:
```
python process.py
```
Or specify a power trace text file and run:
```
python process.py pwr_10_1.txt
```
Another script `draw.py` can visualize the power and temperature changes during running one workload. To get the power and temperature curves, use:
```
python draw.py 10_1
``` 
where 10_1 is the version of the trace.

## Results
- Average CPU power of Arduino is approximately constant (~0.15W).
- Execution time is linear to the input data size and the number of hidden layers.
- The temperature roughly increases as the system running. This is related to the total working time of the board: if the board is running for a longer time, the temperature is likely to be higher. An example curve of power and temperature when having 20 inputs and 1 hidden layer is like follows:
<div align=center><img width="400" height="300" src="https://github.com/Orienfish/IoTSim_Model/blob/master/Arduino_model/20_1.png"/></div>

The experiment results are recorded in the `data.csv` file in the `Arduino_model` folder.