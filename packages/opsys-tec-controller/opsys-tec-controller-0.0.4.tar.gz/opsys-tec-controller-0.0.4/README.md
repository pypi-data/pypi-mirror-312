# README #

This README would normally document whatever steps are necessary to get your application up and running.

### What is this repository for? ###

* This repository is a part of opsys automation infrastructure
* This repository is thermoelectric temperature controller (TEC) implementation of Newport LDT-5910C controller

### How do I get set up? ###

* pip install opsys-tec-controller

### Unit Testing

* python -m unittest -v

### References

* User Manual: https://www.newport.com/medias/sys_master/images/images/hb9/hd3/9825955151902/LDT-5900C-User-Manual.pdf
* NI-Visa Communication Driver: https://www.ni.com/en/support/downloads/drivers/download.ni-visa.html#544206
* R:\Lidar\Dima\Software\ILX-Lightwave-USB-Drivers.zip

### Usage Example
```
from opsys_tec_controller.tec_controller import TecController

device_address = 'a1b2c3'
lut_filepath = 'resistance_to_temperature.csv'  # file included in this repo

tec_conn = TecController(device_address=device_address, lut_filepath=lut_filepath)

tec_conn.connect()
tec_conn.device_reset()
tec_conn.disconnect()
```