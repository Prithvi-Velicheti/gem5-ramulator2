# Integrating gem5 + Ramulator2

## Introduction
gem5 (24.1.0.3) acting as front-end for detailed memory model simulator ramulator2.

The DRAM simulator ramulator2 is located at gem-ramulator2/gem5/ext/ramulator2 .
Currently, ramulator2.0 provides the DRAM models for the following DRAM standards:
- DDR3, DDR4, DDR5
- LPDDR5
- GDDR6
- HBM(2), HBM3

### Integration methodology adapted from
 https://github.com/CMU-SAFARI/ramulator2  
 https://github.com/sangjae4309/gem5-ramulator2/tree/main


Tested OS and kernel.

```
$lsb_release -a
No LSB modules are available.
Distributor ID: Ubuntu
Description:    Ubuntu 24.04.2 LTS
Release:        24.04
Codename:       noble
$uname -r 
6.8.0-59-generic
```
Very likely to work with ubuntu 22.04 and above. 

Key Contents. 

- `example/`: Contains ramulator sample DRAM configurations and example workload.
- `script/`:  Contains simulation scripts utilizing gem5 standard library


## Getting started (Compile)
Clone the repository
```
git clone  --recurse-submodules https://github.com/Prithvi-Velicheti/gem5-ramulator2.git
```

Enter the folder and build gem5+ramulator2
```
cd gem5-ramulator2
./build.sh $(N_PROC)  
```

### Testing in SE mode. DRAM devices wrapped as custom ramulator2 components. 
 The simulation scripts are located at `script/`. Recommended to go through scripts throughly. 

```
cd gem5
build/X86/gem5.opt ../script/base-system-se-x86.py
```






