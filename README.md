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

In the following lines, the content in each folder will be go through in detail.

## Useful Scripts on Raspberry Pi
The folder `RPi_Useful_Scripts` contains basic scripts used in other experiments.
```
├── cut_bluetooth.sh          // Cut the bluetooth of RPi
├── cut_network.sh            // Cut the network (Wi-Fi, Ethernet) of RPi
├── get_cpu_usage.sh          // Sample the CPU frequency and utilization
├── kill.sh          	      // Kill performance sampling
├── perf_script.sh            // Sample performance counters using perf stat
├── set_freq.sh               // Set CPU frequency at 600MHz or 1200MHz
├── reset_freq.sh             // Reset CPU frequency to on demand mode
└── set_bw.sh                 // Set bandwidth using wondershaper
```

## CPU Benchmarks on Raspberry Pi
In folder `Raspberry_Pi_Benchmarks`, a CPU workload is constructed based on the work in [Roy Longbottom's Raspberry Pi, Pi 2 and Pi 3 Benchmarks](http://www.roylongbottom.org.uk/Raspberry%20Pi%20Benchmarks.htm), combining Dhrystone, Whetstone, Linpack, and their multi-thread versions.
To compile it, run the following command inside the folder:
```sh
sudo bash compile.sh
```
To run the compiled benchmarks, use the following command inside the folder:
```sh
bash run.sh
```

- **Synchronization**
Before diving into the details of experiments, it is better to clarify the approach we used to synchronize power measurement on one RPi (connected to powermeter) and performance as well as time measurements on the other target RPi. As some of the measurements require cutting off network, there is no way to connect and signal the other RPi. Instead, we simply start two programs (power measuring on one RPi and the workload on the target RPi) at the same time mannually, using their separate elapsed time of the program as the time measurements.

## CPU Power Model

### Arduino
We construct a MLP workload on Arduino based on the [Neurona Library](https://www.arduinolibraries.info/libraries/neurona). We adjust the input data size and  the number of hidden layer, measuring its power, execution time and temperature (using the internal temperature sensor of Arduino). We found that the power consumption of Arduino is approximately constant, when running any size of MLP network.

Experiment setup and results can be found in [here](Arduino_model/README.md), which is in the `Arduino_model` folder.

### Raspberry Pi
We build two versions of CPU power model of RPi. One model takes the CPU frequency and utilization as input, while the other uses detailed performance counter values. During the data collection, we cut all the network of RPi. We use Linear Regression in the [Scikit-learn Library](https://scikit-learn.org/stable/). 
In general, a power model is represented with a linear combination of the input parameters and coefficients: ![LR](https://github.com/Orienfish/IoTSim_Model/blob/backup/LinearRegression.png), where c is the intercept which is highly related to the static power.

The frequency/utilization-based model is more abstract and can achieve around 3% estimation error. The performance counter-based model can reach less than 1% error, but in reality you may not be able to get such detailed metrics. 

For more details, check [here](RPi_CPU_model/README.md), which is in the `RPi_CPU_model` folder.


## Network Models of Raspberry

### Experiment Setup
As mentioned before, the basic idea of our experiments is having two RPis, one as the target platform and the other connected to the powermeter to collect power traces. We start running workloads and power collection programs on these two RPis at the same time. After the measurement is done, the last step is moving all the data together and process them.

You can find similar structures in the following network-related folders: `RPi_Bt_DataRate`, `RPi_Bt_PacketSize`, `RPi_Bt_Wakeup`, 
`RPi_Util_Calibration`, `RPi_WiFi_BW&Rate`, `RPi_WiFi_PacketSize`, `Pi_WiFi_Wakeup`.
- `pwr_measure_exp.py` is running on the RPi connected to the powermeter, collecting power
traces
- `run_exp.py` is running on the target RPi to trigger workload
- `server.py` is running on the remote machine, listening and being ready for 
connection
- `process.py` is used for processing collected data and plotting
- A folder or several folders contain raw data and generated result, all `.txt` files
- Several `.png` files show the plotted result

To be more specific, each measurement is performed in three steps:
1. the server program is started on a remote machine, either TCP, UDP or Bluetooth server.
1. `pwr_measure_exp.py` and `run_exp.py` begins to execute on the power measuring RPi and target Pi at the same time, storing collected values locally. 
1. After finishing the collection and copy the data to one platform, `process.py` is used to calculate average power and plot interesting graphs. The resulted `.txt` files are stored in the same folder as raw data. The generated graphs lie directly along the scripts.

### Error Analysis
To measure the network power portion, it is necessary to separate CPU power from network power, which however is inherently hard. To approximate this, we substract idle CPU power (no workload and no network) from the total power consumption to estimate the network power portion. This approach is not accurate as the working CPU power during networking operation is counted to the network part. To show that this portion of power is negligible, we measure the average CPU utilization discrepancy between idle state and networking state.

In the `RPi_Util_Calibration` folder, we show the measured result. There are four group of measurements, two focusing on Wi-Fi (size) and the other two focusing on Bluetooth (bt). For both Bluetooth and Wi-Fi, one group of data is obtained under 600MHz CPU frequency while the other stands for 1200MHz. The average utilization during each state (e.g. idle, connect, sending certain size of packet) can be found in the `perf_result.txt` file inside each data folder.

It can be observed that, the discrepancy of average CPU utilization during transmission and idle periods is less than 1%. According to our verified CPU power model, a 1% utilization difference causes approximate 0.01W, which demonstrates the maximum error of our method.

### Wi-Fi

#### Wakeup (TCP)
To obtain a taste of power variation on Raspberry Pi’s Wi-Fi chip, we first evaluate the time-varying power pattern when we turn on the Wi-Fi on Raspberry Pi, connect to a common Access Point (AP) and then send various size of packets to the other terminal that also connects to the AP. The following Figure displays the power trace when Raspberry Pi is working at 1200MHz. We observe that the on-off state of Wi-Fi chip brings a power difference of approximately 0.14W (same value for 600MHz). Sending a larger packet will need longer time and consume more power aside from the base Wi-Fi power.

The running scripts, collected data and plotting graphs can be found in the `RPi_WiFi_Wakeup` folder.
<div align=center><img width="400" height="350" src="https://github.com/Orienfish/IoTSim_Model/blob/master/RPi_WiFi_Wakeup/Wi-Fi_wakeup_1200_1000_nosample_label.png"/></div>

#### Packet Size (TCP)
We are also interested in the “turning point” of packet size where the transmission power diverges from the baseline Wi-Fi power.  In our experiment, we fix the bandwidth at 2000kbps using the [wondershaper tool](https://github.com/magnific0/wondershaper) and create simple python scripts to trigger the transmission of packets varying in size. We record the transmission intervals of each size of a packet, only calculating the average power consumed in that period. The measured Wi-Fi power consumption and length of transmission interval are shown in the following Figure.

The running scripts, collected data and plotting graphs can be found in the `RPi_WiFi_PacketSize` folder.
<div align=center><img width="400" height="300" src="https://github.com/Orienfish/IoTSim_Model/blob/master/RPi_WiFi_PacketSize/wifi_exp_600_2000kbps.png"/></div>

#### Bandwidth (UDP)
To have better control over packet rate and data rate, we adopt UDP instead of TCP in this and the following experiment. Here, we evaluate the average Wi-Fi power on two combinations of metrics: bandwidth and packet rate, bandwidth and data rate. The results are similar while using bandwidth and data rate exhibits more obvious changes. Thus we choose the latter combination to demonstrate here. Note that in this case we evaluate the average Wi-Fi power during a period of at least 5 seconds, instead of the interval between the beginning and end of transmission. Similarly, we estimate Wi-Fi power by subtracting idle CPU power from total power.

To study the bandwidth model, we fix the data rate and then perform Wi-Fi transmission at different bandwidth. The results under 2kB/s and 1MB/s data rate are shown in the following Figures. It can be observed that, while sending at a low data rate, the Wi-Fi power consumption does not change much as the bandwidth increases. When large transmission data is requested, having higher bandwidth will cost more Wi-Fi power consumption. 

The running scripts, collected data and plotting graphs can be found in the `RPi_WiFi_BW&Rate` folder.
<div align=center><img width="800" height="350" src="https://github.com/Orienfish/IoTSim_Model/blob/master/RPi_WiFi_BW%26SIZE/bw.png"/></div>

#### Data Rate (UDP)
In another UDP experiment, we fix the bandwidth in order to study the power behavior under different data rate. In (a) of the following Figure, with 1Mbps bandwidth limitation, the Wi-Fi power is bounded to a certain level as data rate increases and more time is needed to finish transmission. From (b) of the following Figure, it can be seen that when bandwidth limitation is not tight, all data could be successfully transmitted in the 5 seconds period, with the Wi-Fi power increasing linearly as data rate stepping up.

The running scripts, collected data and plotting graphs can be found in the `RPi_WiFi_BW&Rate` folder.
<div align=center><img width="800" height="350" src="https://github.com/Orienfish/IoTSim_Model/blob/master/RPi_WiFi_BW%26SIZE/datarate.png"/></div>

### Bluetooth

#### Wakeup
We visualize the power trace after we turn on the bluetooth of Raspberry Pi, connect to a Bluetooth server, and send a certain size of packets. Our experimental script is built upon the [pybluez module](https://github.com/pybluez/pybluez) which provides APIs for discovering devices (i.e., scanning) and establishing client/server bluetooth connection based on the RFCOMM protocol. In Bluetooth experiments, we cut off all the Wi-Fi and Ethernet connections.

The time-varying curve is shown in the following Figure. Contrary to Wi-Fi, switching on bluetooth causes little power difference. Scanning and requesting connection show distinguishable power increment, both of which are less than the power rise when sending 100kB and 1000kB packets. The average power consumption and lasting time of each state are summarized in the following Table.

The running scripts, collected data and plotting graphs can be found in the `RPi_Bt_Wakeup` folder.

| State          | Average Power Consumption (W) | Time (s) |
|:---------------|:-----------------------------:|---------:|
| Turn On        |  0.14				   	     | 0.2      |
| Scan           |  0.03					     | 16*  |
| Pair & Connect |  0.04						 | 2.6      |

* Configurable by the user.

<div align=center><img width="400" height="350" src="https://github.com/Orienfish/IoTSim_Model/blob/master/RPi_Bt_Wakeup/bt_realtime_600_label.png"/></div>

#### Packet Size
We further evaluate the relation between Bluetooth transmission power and the transmitted data size. We fix the frequency during the measurement. The following Figure shows the results for 600MHz and 1200MHz CPU frequency respectively. Similar as calculating Wi-Fi power, the Bluetooth power consumption here is estimated by subtracting the idle power base line from overall power consumption. We conclude that after around 10kB, the Bluetooth transmission power will start to increase.

The running scripts, collected data and plotting graphs can be found in the `RPi_Bt_PacketSize` folder.
<div align=center><img width="800" height="350" src="https://github.com/Orienfish/IoTSim_Model/blob/master/RPi_Bt_PacketSize/bt_pktsize.png"/></div>

#### Data Rate
While the previous experiment evaluates the transmission power between the beginning and end of transmission, we are also interested in the average power when transmitting at a certain data rate. In this case, we set an evaluation period of at least 5 seconds, during which the Raspberry Pi tries to send data at a certain rate through Bluetooth. The resulted transmission time larger than 5 seconds indicates that the Pi fails to reach that data rate. As the curve shown in the following Figure, higher data rate leads to higher average power consumption. It should be noted that the Bluetooth power consumption is much less than Wi-Fi.

The running scripts, collected data and plotting graphs can be found in the `RPi_Bt_DataRate` folder.
<div align=center><img width="400" height="300" src="https://github.com/Orienfish/IoTSim_Model/blob/master/RPi_Bt_DataRate/rate_1200_v1.png"/></div>