# Python Serial RS232 Datalogger for debugging embedded systems 
### Like ESP WIFI modules, microcontrollers, Linux serial console etc.

<space><space><space><space><space><space><space>With this program it is possible to save logs from different serial 
ports just by configuring the JSON file (config.json), the number of ports and 
unlimited and each process for processing and saving the logs is with 
you on separate instances and threads.<br/>
<space><space><space><space><space><space><space>I use this program a few months to save the logs of systems with Linux, 
microcontrolados saving in database. 
   After that I use some Querys to extract the faults.<br/>
<space><space><space><space><space><space><space> For the development 
I am using Pycharm of jetbrains is a great tool for Python!
    
    
#####Using file JSON for configuration for multiple serial ports:



Exemple a serial porta:

{<br/>
<tab>"devices":<br/>
<tab><tab><tab><tab><tab>[<br/>
<tab><tab><tab><tab><tab><tab><tab><tab>{<br/>
<tab><tab><tab><tab><tab><tab><tab>"serialport": "/dev/ttyUSB0",<br/>
<tab><tab><tab><tab><tab><tab><tab>"baudrate": 115200,<br/>
<tab><tab><tab><tab><tab><tab><tab>"timeout": 5,<br/>
<tab><tab><tab><tab><tab><tab><tab>"description":"TEST MODULE WIFI"<br/>
<tab><tab><tab><tab><tab><tab>}<br/>
<tab><tab><tab><tab>]<br/>
}<br/>



Example two serial ports:

{<br/>
<tab>"devices":<br/>
<tab><tab><tab><tab><tab>[<br/>
<tab><tab><tab><tab><tab><tab><tab><tab>{<br/>
<tab><tab><tab><tab><tab><tab><tab>"serialport": "/dev/ttyUSB0",<br/>
<tab><tab><tab><tab><tab><tab><tab>"baudrate": 115200,<br/>
<tab><tab><tab><tab><tab><tab><tab>"timeout": 5,<br/>
<tab><tab><tab><tab><tab><tab><tab>"description":"TEST MODULE WIFI"<br/>
<tab><tab><tab><tab><tab><tab>}<br/>
<tab><tab><tab><tab><tab><tab>,<br/>
<tab><tab><tab><tab><tab><tab>{<br/>
<tab><tab><tab><tab><tab><tab><tab>"serialport": "/dev/ttyUSB1",<br/>
<tab><tab><tab><tab><tab><tab><tab>"baudrate": 115200,<br/>
<tab><tab><tab><tab><tab><tab><tab>"timeout": 5,<br/>
<tab><tab><tab><tab><tab><tab><tab>"description":"TEST MAIN CPU"<br/>
<tab><tab><tab><tab><tab><tab>}<br/>
<tab><tab><tab><tab>]<br/>
}<br/>


Exemple three serial ports:

{<br/>
<tab>"devices":<br/>
<tab><tab><tab><tab><tab>[<br/>
<tab><tab><tab><tab><tab><tab><tab><tab>{<br/>
<tab><tab><tab><tab><tab><tab><tab>"serialport": "/dev/ttyUSB0",<br/>
<tab><tab><tab><tab><tab><tab><tab>"baudrate": 115200,<br/>
<tab><tab><tab><tab><tab><tab><tab>"timeout": 5,<br/>
<tab><tab><tab><tab><tab><tab><tab>"description":"TEST MODULE WIFI"<br/>
<tab><tab><tab><tab><tab><tab>}<br/>
<tab><tab><tab><tab><tab><tab>,<br/>
<tab><tab><tab><tab><tab><tab>{<br/>
<tab><tab><tab><tab><tab><tab><tab>"serialport": "/dev/ttyUSB1",<br/>
<tab><tab><tab><tab><tab><tab><tab>"baudrate": 115200,<br/>
<tab><tab><tab><tab><tab><tab><tab>"timeout": 5,<br/>
<tab><tab><tab><tab><tab><tab><tab>"description":"TEST MAIN CPU"<br/>
<tab><tab><tab><tab><tab><tab>}<br/>
<tab><tab><tab><tab><tab><tab>,<br/>
<tab><tab><tab><tab><tab><tab>{<br/>
<tab><tab><tab><tab><tab><tab><tab>"serialport": "/dev/ttyUSB2",<br/>
<tab><tab><tab><tab><tab><tab><tab>"baudrate": 115200,<br/>
<tab><tab><tab><tab><tab><tab><tab>"timeout": 5,<br/>
<tab><tab><tab><tab><tab><tab><tab>"description":"TEST LOGS uC AUXILIAR"<br/>
<tab><tab><tab><tab><tab><tab>}<br/>
<tab><tab><tab><tab>]<br/>
}<br/>


Note:

            The capacity of the data logger depends only on the CPU and disk IO speeds!                







