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
│   ├── arduino_mlp     	  // Arduino code to run MLP application
│   ├── rpi_powermeter		  // The python script used on RPi to collect power trace
│   └── pwr_perf_temp_data    // Collected power, perf. (i.e. exec. time) and temperature data
│							  // and several processing scripts
├── RPi_Bt_DataRate           // Measurement of Bluetooth power on RPi under various data rate
│   ├── arduino_mlp     	  // Arduino code to run MLP application
│   ├── rpi_powermeter		  // The python script used on RPi to collect power trace
│   └── pwr_perf_temp_data    // Collected power, perf. (i.e. exec. time) and temperature data
├── trainenv_virf_v5.py       // Python class for virtual training environment. Interact with deep_q_network_virf_new.py.
├── test_model_v.py           // Extra virtual test after virtual training.
├── deep_q_network_real_train.py // DQN for practical training.
├── realenv_train.py          // Python class for real training environment. Interact with deep_q_network_real_train.py.
├── deep_q_network_real_test.py // DQN for practical testing.
└── realenv_test.py           // Python class for real testing environment. Interact with deep_q_network_real_test.py. 
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