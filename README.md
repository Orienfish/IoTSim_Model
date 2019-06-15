# IoTSim
This repo is one of the steps to build an IoT simulator. We intend to simulate power, performance and
reliability of a heterogeneous IoT network. To accomplish this, we need validated models of basic
components. This repo has the following features:

- provide CPU models of Arduino (Uno)
- provide CPU and network power models of Raspberry Pi (3B)
- share measurements of Wi-Fi and Bluetooth according to on/off/connect/disconnect state,
bandwidth, packet size and data rate
- offer useful scripts on RPi to change frequency, get CPU utilization, CPU temperature, etc.

Power trace is measured using the [HIOKI 3334 Powermeter](https://www.hioki.com/en/products/detail/?product_key=5812).

## Organization
Each folder in this repo contain the codes and data for one experiment or one important aspect.
The following structure will walk you through all the code and data.
```
├── README.md
├── Arduino_model             // Arduino CPU model, power, exec. time and temperature measurements
├── RPi_Bt_DataRate           // Measurement of Bluetooth power on RPi under various data rate
├── RPi_Bt_PacketSize         // Measurement of Bluetooth power on RPi to send various packet size
├── RPi_Bt_Wakeup             // Measurement of Bluetooth power on RPi during wakeup
├── RPi_CPU_model             // RPi CPU model
├── RPi_Useful_Scripts        // Scripts on RPi such as changing freq., set bandwidth, etc.
├── RPi_Util_Calibration      // Measure the utilization difference between idle and networking
├── RPi_WiFi_BW&Rate          // Measurement of Wi-Fi power on RPi under various bandwidth and data rate
├── RPi_WiFi_PacketSize       // Measurement of Wi-Fi power on RPi to send various packet size
├── RPi_WiFi_Wakeup           // Measurement of Wi-Fi power on RPi during wakeup
└── Raspberry_Pi_Benchmarks   // CPU benchmarks running on RPi
```
You can find similar structures in folder RPi\_Bt\_DataRate, RPi\_Bt\_PacketSize, RPi\_Bt\_Wakeup, 
RPi\_Util\_Calibration, RPi\_WiFi\_BW&Rate, RPi\_WiFi\_PacketSize, Pi\_WiFi\_Wakeup:
- `pwr_measure_exp.py` is running on the RPi connected to the powermeter, collecting power
traces
- `run_exp.py` is running on the target RPi to trigger workload
- `server.py` is running on the remote machine, listening and being ready for 
connection
- `process.py` is used for processing collected data and plotting
- A folder or several folders contain raw data and generated result, all .txt files
- Several .png files show the plotted result

In the following lines, the content in each folder will be go through in detail.

## Useful Scripts on Raspberry Pi
The folder RPi_Useful_Scripts contains basic scripts that are used in other experiments.
```
├── cut_bluetooth.sh          // Cut the bluetooth of RPi
├── cut_network.sh            // Cut the network (Wi-Fi, Ethernet) of RPi
├── get_cpu_usage.sh          // Sample the CPU frequency and utilization
├── kill.sh          		  // Kill performance sampling
├── perf_script.sh            // Sample performance counters using perf stat
├── set_freq.sh               // Set CPU frequency at 600MHz or 1200MHz
├── reset_freq.sh             // Reset CPU frequency to on demand mode
└── set_bw.sh         		  // Set bandwidth using wondershaper
```

## CPU Benchmarks on Raspberry Pi
In folder Raspberry_Pi_Benchmarks, a CPU workload is constructed based on the work in [Roy Longbottom's Raspberry Pi, Pi 2 and Pi 3 Benchmarks](http://www.roylongbottom.org.uk/Raspberry%20Pi%20Benchmarks.htm), combining Dhrystone, Whetstone, Linpack, and their multi-thread versions.
To compile it, run the following command inside the folder:
```sh
sudo bash compile.sh
```
To run the compiled benchmarks, use the following command inside the folder:
```sh
bash run.sh
```

## CPU Power Model

### Arduino
We construct a MLP workload on Arduino based on the [Neurona Library](https://www.arduinolibraries.info/libraries/neurona). We adjust the input data size and  the number of hidden layer, measuring its power, execution time and temperature (using the internal temperature sensor of Arduino). We found that the power consumption of Arduino is approximately constant, when running any size of MLP network.

Experiment setup and results can be found in [here](Arduino_model/README.md), which is in the Arduino_model folder.

### Raspberry Pi
We build two versions of CPU power model of RPi. One model takes the CPU frequency and utilization as input, while the other uses detailed performance counter values. We use Linear Regression in the [Scikit-learn Library](https://scikit-learn.org/stable/). 
In general, a power model is represented with a linear combination of the input parameters $e_i$ and coefficients $\beta_i$: ![LR](https://github.com/Orienfish/IoTSim_Model/blob/backup/LinearRegression.png), where c is the intercept which is highly related to the static power.

The frequency/utilization-based model is more abstract and can achieve around 3% estimation error. The performance counter-based model can reach less than 1% error, but in reality you may not be able to get such detailed metrics. 

For more details, check [here](RPi_CPU_model/README.md), which is in the RPi_CPU_model folder.


## Network Models of Raspberry

### Error Analysis

### Synchronization

### Wi-Fi

#### Wakeup (TCP)

#### Packet Size (TCP)

#### Bandwidth (UDP)

#### Data Rate (UDP)

### Bluetooth

#### Wakeup

#### Packet Size

#### Data Rate
