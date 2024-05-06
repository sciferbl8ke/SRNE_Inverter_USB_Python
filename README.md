# SRNE_Inverter_USB_Python
SRNE Inverters Linux Python script

Intro
Welcome to the SRNE Inverter Linux Python script
![image](https://github.com/sciferbl8ke/SRNE_Inverter_USB_Python/assets/167745967/ed891afa-4072-43aa-b625-1e6d8ff0561d)
![image](https://github.com/sciferbl8ke/SRNE_Inverter_USB_Python/assets/167745967/354f0fa7-f0e8-4cd6-ae2c-1077311e2e58)

Sometimes things on GIT is tricky, and I will try to aid where I can however if you want to run this, please feel free however you might want to get familiar with installing and configuring Grafana and MySQL on Linux.  The install for debian systems are pretty easy, visit the GRafana website and follow the instructions on how to add the APT repo, or compile from source if you are adventurous. 

Introduction / Back Story
Like most of you here, you need an alternative to reading data from SRNE Inverters and want to save that information somewhere to keep track of everything.  There is commercial software available to use, however you need special hardware etc.  This is a simple script in Python 3 to read that data from the device. 
I was forced to use the Windows application but it keeps crashing, runs into memory leakage issues, loss of communication with the device without any reason or log information so I set out to create something in my favorite place….Linux. 
I initially created a Bash script using very basic bash tools to monitor the port and read the information as I send commands to the device, however this also has limitations and at times some errors were returned and strange values, the data was not reliable.
Finally, here we are, I never coded in Python so I did research on each line of code to do what I want it to do and it works very good for more than a month without ever losing communication or receiving erroneous data back from the device.

Improvements
You are welcome to contribute to the project as you wish, I’m sure there are easier ways of doing what I did here, a single function that you pass a variable name into and the entire function would do the same thing over and over with different input parameters however there is one “Battery Amps” that operate differently and require additional math to ensure it is working correctly.
Additionally, more data can be collected for PV, I can’t post the XML file from the software but will add the additional lines in due time as I do not have solar panels at this point.
How to use
•	Python 3
Ensure you have Python 3 installed on your system.  The easiest way for me to work with it was to create a Python 3 virtual environment in my home folder, from there all the libraries installed correctly and execution was much easier.  Python 3 will complain about installing packages globally etc. so read up on how to create a Python 3 virtual environment.
•	Modules
Some modules can be installed with pip, others can be installed with APT, not sure which one it was, may differ from distribution to distribution.
•	Grafana
Grafana has binaries for most distributions and source if you want to compile.  Installing and configuring Grafana is very trivial and once up and running, you just need to set the connection strings. After the setup is done and you have data going into your DB be it MySQL or InfluxDB, you can create the dash layout as you wish.  I might include the JSON files later however I am using a very old version of Grafana since this version works properly with the date issues and some other performance issues I had with the newer versions.
•	Database
I have included the create table SQL file to make it easier to create and dump the data in the DB.  You are welcome to use any database, you might need to add additional modules to the code, perhaps add a variable to change between MySQL / InfluxDB etc.
•	Finding my device
If the script doesn’t work and your serial device is on a different port or name, you can navigate to /dev and look for “USB” or use “ls /sys/class/tty” and look for USB / ttyS0 etc.  There are multiple ways to find it.  Another method is lsusb and look for something like “QinHeng Electronics CH340 serial converter”
To use:
./python3 /location/of/your/file.py
If you enabled debug you will see the values from the device every 4-5 seconds.



