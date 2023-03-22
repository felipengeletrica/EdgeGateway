# 🐍 Python Serial RS232 Datalogger for debugging embedded systems 
  
Like ESP WIFI modules, microcontrollers, Linux serial console etc.

With this program it's possible to save logs from different serial ports just by configuring the JSON file (`config.json`), the number of ports and unlimited and each process for processing and saving the logs is with you on separate instances and threads.

> I use this program a few months to save the logs of systems with Linux, microcontrolados saving in database.  After that I use some Querys to extract the faults. For the development I am using Pycharm of jetbrains is a great tool for Python!

## Run the application

To run the application, simply execute:
```bash
python main.py
```

To find the tty port that your microcontroller is using on your system, you can filter the kernel log output using the command:
```bash
dmesg | grep tty
```

This command will list all the available tty ports on your system, including the port associated with your microcontroller. 
```bash
❯ dmesg | grep tty
[12999.826226] cdc_acm 1-1:1.0: ttyACM0: USB ACM device
[13031.368677] cdc_acm 1-3:1.0: ttyACM0: USB ACM device
[13980.396488] cdc_acm 1-3:1.0: ttyACM0: USB ACM device
```
Note that if the microcontroller is disconnected and reconnected to the system, the tty port may be generated again, resulting in multiple lines for the same port, as shown in the example below:
    
Using file `config.json` for configuration for one or multiple serial ports: 
 
Example two serial ports: 
```json
{
"devices":
   [
      {
      "serialport": "/dev/ttyACM0",
      "baudrate": 115200,
      "timeout": 5,
      "description":"TEST MODULE WIFI"
      },{
      "serialport": "/dev/ttyACM1",
      "baudrate": 115200,
      "timeout": 5,
      "description":"TEST MAIN CPU"
      }
   ]
}
```

> Note: The capacity of the data logger depends only on the CPU and disk IO speeds! 

## 🧪 Testing

If you're looking to run a program to send data via serial to your microcontroller, check out the [`example/arduino`](example/arduino) directory in this repository. You'll find a simple **PlatformIO** project that provides tests for sending data over serial communication with an Arduino microcontroller. Simply navigate to the [`example/arduino`](example/arduino) directory in this repository and run the project with **PlatformIO** to get started.
