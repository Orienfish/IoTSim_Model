# IoTSim
This repo is one of the steps to build an IoT simulator. We intend to simulate power, performance and
reliability of a heterogeneous IoT network. To accomplish this, we need validated models of basic
components. This repo has the following features:

- provide CPU and network models of Arduino (Uno) and Raspberry Pi (3B) (RPi)
- share measurements of Wi-Fi and Bluetooth according to on/off/connect/disconnect state,
bandwidth, packet size and data rate
- offer useful scripts on RPi to change frequency, get CPU utilization, CPU temperature, etc.

## Organization
Each folder in this repo contain the codes and data for one experiment or one important aspect.
```
├── README.md                 // Help
├── Arduino_model             // Arduino CPU model, power, exec. time and temperature measurements
│   ├── arduino_mlp           // Arduino code to run MLP application
│   ├── rpi_powermeter	      // The Python script used on RPi to collect power trace
│   └── pwr_perf_temp_data    // Collected power, perf. (i.e. exec. time) and temperature data
│			      // and several processing scripts
├── RPi_Bt_DataRate           // Measurement of Bluetooth power on RPi under various data rate
│   ├── bt_rate_data          // Collected power and time data
│   ├── bt_rate_process.py    // The Python script used to process and plot
│   ├── rfcomm_server.py      // The Bluetooth server program running on remote machine
│   └── run_bluetooth_exp.py  // The Python script run on target RPi to trigger connection and transmission
```

## CPU Power model

### Arduino

### Raspberry Pi

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
