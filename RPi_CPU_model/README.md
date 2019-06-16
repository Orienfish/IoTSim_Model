# Raspberry Pi CPU Power Model
In this experiment, we try to construct two CPU power models for Raspberry Pi:
- Frequency/Utilization-based Model
- Performance Counter-based Model

## Experiment Setup
We use two RPis: one running the workload as a target platform while cutting off all network, the other reading power traces from the [HIOKI 3334 Powermeter](https://www.hioki.com/en/products/detail/?product_key=5812). Follow the steps:

- Set the frequency of the target RPi and cut off network connection.
- Run `bash run_cpu_test.sh cpu_600` on the target RPi and `python pwr_measure.py cpu_600` on the measuring RPi at the same time. `cpu_600` is the version to distinguish different experiements.
Note that the instruction in `run_cpu_test.sh` is different for freq/util-based model and perf counter-based model. Use comment to select which performance sampling script to use.
- Collect data together and train Linear Regression model using the [Scikit-learn Library](https://scikit-learn.org/stable/).
For the freq/util-based model, we use `python train_cpu.py`. For the perf counter-based model, we use `pyton train_perf_cpu.py`.
- All the training results are saved in the `model` folder. `model_info.txt` records all the coefficients for each model. The rest files in the folder are binary records of the built models, which can be imported with [cPickle](https://pymotw.com/2/pickle/). Check script `train_cpu.py` for example import functions. All the `.csv` files in the `RPi_CPU_folder` take down training data and standard output, showing the raw data we feed into the Linear Regression model.

## Frequency/Utilization-based Model
In this model, we take CPU frequency and utilization as inputs. The built model can be expressed by:
predicted power = c0 + c1 * freq + c2 * util

We use the `get_cpu_usage.sh` in `RPi_Useful_Scripts` folder to obtain frequency and utilization data. Following Figure shows the plot of measured power, predicted power, frequency and utilization with 600MHz frequency. It can be seen that our prediction approachs the authentic power curve well.
<div align=center><img width="800" height="540" src="https://github.com/Orienfish/IoTSim_Model/blob/master/RPi_CPU_model/600MHz_v4.png"/></div>

In the `model` folder, we leave 4 freq/util-based models, from `model.v1` to `model.v4`. The maximum average train error is 2.91% while the maximum error is 33.6%. Although they have various levels of error, the prediction preformance is similar. One example of the trained model is:

```
Coefficients of ./model/model.v4
freq: 1.4995596404e-06 util: 0.0183259386149 intercept: 1.97313572567
Score: 0.925133
Error: avg: 0.025987 max: 0.332113
```

## Performance Counter-based Model
In this model, we take a lot of performance counter values as input. The power model is represented with a linear combination of the input parameters and coefficients: ![LR](https://github.com/Orienfish/IoTSim_Model/blob/backup/LinearRegression.png), where c is the intercept which is highly related to the static power.

We use `perf stat` instruction in `../RPi_Useful_Scripts/perf_script.sh` to obtain performance values.

In the `model` folder, we have 2 perf counter-based models, using various number of events. `model.perf_v1` uses only instructions and cache misses, resulting in 3.63% average error:

```
Coefficients of ./model/model.perf_v1
cache-misses: 1.604158848953897e-07 instructions: 3.8251433694302514e-09 intercept: 3.1186404101507303
Score: 0.792358
Error: avg: 0.036643 max: 0.347124
```

`model.perf_v2` uses a bunch of performance events:

```
Coefficients of ./model/model.perf_v2
L1-dcache-loads: 1.1201174772923045e-09 L1-dcache-stores: -3.0816554910780796e-10 branch-instructions: -2.89318560875291e-09 branch-misses: -8.559663917289132e-08 cache-misses: -1.4362203201178858e-07 cache-references: 1.505825052950235e-09 cpu-cycles: 2.0684120184486966e-09 instructions: 3.135143357712678e-10 r110: 1.6033898690248393e-07 r13C: 0.0 r1A2: 0.0 r1C2: 1.3949913999186216e-07 intercept: 3.096927605408612
Score: 0.917879
Error: avg: 0.024100 max: 0.300376
```