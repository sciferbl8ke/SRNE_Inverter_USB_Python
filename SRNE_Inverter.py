# Import modules
# Debian users "sudo apt install python3-binascii" also create a Python 3 staging area and install modules using pip
import serial
import struct
import time
import binascii
import sys
import mysql.connector
import datetime

# Create Serial connection. Do not there might be some work he because if this is not ready, the script continues to
# The loop, so we should loop until a connection has been made before we go to the program loop

ser = serial.Serial(
    port='/dev/ttyUSB0',
    baudrate=9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=0.4
)

# Mysql connection settings
cnx = mysql.connector.connect(
  host="localhost",
  user="test",
  password="test",
  database="power"
)

# Set to 1 if you do not want to save the information to a DB and only want to test!!!!!
No_DB_Output_Print_Data = 1
res = ''

# Create an infinite loop, after some testing, the program does not consume much CPU cycles and the loop does 
# Not create a memory issue over time.

while True:
  
# Send commands to the inverter
# Battery Amps
  cw = b'\x01\x03\x01\x02\x00\x01\x24\x36'
  ser.write(serial.to_bytes(cw))
  read = ser.read(32)
  bat_amps = binascii.hexlify(bytearray(read))
# Battery volts
  cw = b'\x01\x03\x01\x01\x00\x01\xD4\x36'
  ser.write(serial.to_bytes(cw))
  read = ser.read(32)
  bat_volts = binascii.hexlify(bytearray(read))
# Line Voltage
  cw = b'\x01\x03\x02\x13\x00\x01\x74\x77'
  ser.write(serial.to_bytes(cw))
  read = ser.read(32)
  line_voltage = binascii.hexlify(bytearray(read))
# Load Active Power Watts
  cw = b'\x01\x03\x02\x1b\x00\x01\xf5\xb5'
  ser.write(serial.to_bytes(cw))
  read = ser.read(32)
  load_active_power = binascii.hexlify(bytearray(read))
# Load Active Power VA
  cw = b'\x01\x03\x02\x1c\x00\x01\x44\x74'
  ser.write(serial.to_bytes(cw))
  read = ser.read(32)
  load_active_power_va = binascii.hexlify(bytearray(read))
# Temperature DC
  cw = b'\x01\x03\x02\x20\x00\x01\x84\x78'
  ser.write(serial.to_bytes(cw))
  read = ser.read(32)
  temp_dc = binascii.hexlify(bytearray(read))
# Temperature AC
  cw = b'\x01\x03\x02\x21\x00\x01\xd5\xb8'
  ser.write(serial.to_bytes(cw))
  read = ser.read(32)
  temp_ac = binascii.hexlify(bytearray(read))
# Temperature TR
  cw = b'\x01\x03\x02\x22\x00\x01\x25\xb8'
  ser.write(serial.to_bytes(cw))
  read = ser.read(32)
  temp_tr = binascii.hexlify(bytearray(read))
# Load Total
  cw = b'\x01\x03\xf0\x3a\x00\x01\x97\x07'
  ser.write(serial.to_bytes(cw))
  read = ser.read(32)
  load_total = binascii.hexlify(bytearray(read))
# Load Today
  cw = b'\x01\x03\xf0\x30\x00\x01\xb7\x05'
  ser.write(serial.to_bytes(cw))
  read = ser.read(32)
  load_today = binascii.hexlify(bytearray(read))
# Battery total discharge  
  cw = b'\x01\x03\xf0\x36\x00\x01\x57\x04'
  ser.write(serial.to_bytes(cw))
  read = ser.read(32)
  bat_discharge = binascii.hexlify(bytearray(read))
# Battery Total Charge
  cw = b'\x01\x03\xf0\x34\x00\x01\xf6\xc4'
  ser.write(serial.to_bytes(cw))
  read = ser.read(32)
  bat_charge = binascii.hexlify(bytearray(read))
# Line Current
  cw = b'\x01\x03\x02\x14\x00\x01\xc5\xb6'
  ser.write(serial.to_bytes(cw))
  read = ser.read(32)
  line_current = binascii.hexlify(bytearray(read))
# Tests - inconclusive
#  cw = b'\x01\x03\xf0\x34\x00\x01\xf6\xc4'
#  ser.write(serial.to_bytes(cw))
#  read = ser.read(32)
#  bat_charge_total = binascii.hexlify(bytearray(read))
#  
#  cw = b'\x01\x03\xf0\x07\x00\x01\x06\xcb'
#  ser.write(serial.to_bytes(cw))
#  read = ser.read(32)
#  bat_charge_line = binascii.hexlify(bytearray(read))


  # Battery Discharge
  # Get size of response, must be 47
  size = sys.getsizeof(bat_discharge)
  if size == 47:
    # Remove the last 2 blocks of data whilst in HEX
    bat_discharge = bat_discharge[:-4]
    # Remove the first 3 blocks of data whilst in HEX
    res = bat_discharge[6:]
    # Convert the remaining HEX to DECIMAL
    # Convert the decimal number to int
    decimal_output = int(res,16)
    # Get the current timestamp
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    calculated = float(decimal_output)
    value = str(calculated)
    if No_DB_Output_Print_Data == 1:
      print('Battery Discharge Total:', value)
    else:
      if cnx and cnx.is_connected():
        with cnx.cursor() as cursor:
          query ="INSERT INTO power.ups (date,type,value) VALUES ('"+ now +"','bat_discharge','"+ value +"')"
          result = cursor.execute(query)
          cnx.commit()
          rows = cursor.fetchall()
          for rows in rows:
            print(rows)
  
      else:
        print("Could not connect")
  else:
    print("number of bytes do not match")
    

  # BAT charge
  # Get size of response, must be 47
  size = sys.getsizeof(bat_charge)
  if size == 47:
    # Remove the last 2 blocks of data whilst in HEX
    bat_charge = bat_charge[:-4]
    # Remove the first 3 blocks of data whilst in HEX
    res = bat_charge[6:]
    # Convert the remaining HEX to DECIMAL
    # Convert the decimal number to int
    decimal_output = int(res,16)
    # Get the current timestamp
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    calculated = float(decimal_output)
    value = str(calculated)
    if No_DB_Output_Print_Data == 1:
      print('Battery Charge Total:', value)
    else:
      if cnx and cnx.is_connected():
        with cnx.cursor() as cursor:
          query ="INSERT INTO power.ups (date,type,value) VALUES ('"+ now +"','bat_charge','"+ value +"')"
          result = cursor.execute(query)
          cnx.commit()
          rows = cursor.fetchall()
          for rows in rows:
            print(rows)
  
      else:
        print("Could not connect")
  else:
    print("number of bytes do not match")
    

  #Battery Amps
  # Get size of response, must be 47
  size = sys.getsizeof(bat_amps)
  if size == 47:
    # Remove the last 2 blocks of data whilst in HEX
    bat_amps = bat_amps[:-4]
    # Remove the first 3 blocks of data whilst in HEX
    res = bat_amps[6:]
    # Convert the remaining HEX to DECIMAL
    # Convert the decimal number to int
    decimal_output = int(res,16)
    # Get the current timestamp
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # For Bat amps we need to take the current reading and deduct from 65535 (FF FF) and divide by 10
    # First, we must determine which state it is, if the number is higher than 11000 which my inverter is 100amps,
    # will not be over during load usage, then we can confirm the inverter is in a non-load state.
    # Alternative, you could check if the line voltage is less than 100v for 110v or 200v for 220v applications.
    # I preferred to check it right here and now
    if decimal_output > 11000:
      calculated = float((decimal_output-65535)/10)
      value = str(calculated)
      if No_DB_Output_Print_Data == 1:
        print('Battery Amps:', value)
      else:
        if cnx and cnx.is_connected():
          with cnx.cursor() as cursor:
            query ="INSERT INTO power.ups (date,type,value) VALUES ('"+ now +"','battery_current','"+ value +"')"
            result = cursor.execute(query)
            cnx.commit()
            rows = cursor.fetchall()
            for rows in rows:
              print(rows)
    
        else:
          print("Could not connect")
    else:
      calculated = float(decimal_output/10)
      value = str(calculated)
      if cnx and cnx.is_connected():
        with cnx.cursor() as cursor:
          query ="INSERT INTO power.ups (date,type,value) VALUES ('"+ now +"','battery_current','"+ value +"')"
          result = cursor.execute(query)
          cnx.commit()
          rows = cursor.fetchall()
          for rows in rows:
            print(rows)
  else:
    print("number of bytes do not match")

  # Battery Voltage
  # Get size of response, must be 47
  size = sys.getsizeof(bat_volts)
  if size == 47:
    # Remove the last 2 blocks of data whilst in HEX
    bat_volts = bat_volts[:-4]
    # Remove the first 3 blocks of data whilst in HEX
    res = bat_volts[6:]
    # Convert the remaining HEX to DECIMAL
    # Convert the decimal number to int
    decimal_output = int(res,16)
    #print("bat volts:", decimal_output)
    # Get the current timestamp
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    calculated = float(decimal_output/10)
    value = str(calculated)
    if No_DB_Output_Print_Data == 1:
      print('Battery Volts:', value)
    else:
      if cnx and cnx.is_connected():
        with cnx.cursor() as cursor:
          query ="INSERT INTO power.ups (date,type,value) VALUES ('"+ now +"','battery_voltage','"+ value +"')"
          result = cursor.execute(query)
          cnx.commit()
          rows = cursor.fetchall()
          for rows in rows:
            print(rows)
  
      else:
        print("Could not connect")
  else:
    print("number of bytes do not match")

  # Main Voltage
  # Get size of response, must be 47
  size = sys.getsizeof(line_voltage)
  
  #print("line voltage after hexlify:", line_voltage)
  if size == 47:
    # Remove the last 2 blocks of data whilst in HEX
    line_voltage = line_voltage[:-4]
    # Remove the first 3 blocks of data whilst in HEX
    res = line_voltage[6:]
    # Convert the remaining HEX to DECIMAL
    # Convert the decimal number to int
    decimal_output = int(res,16)
    # Get the current timestamp
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    calculated = float(decimal_output/10)
    value = str(calculated)
    if No_DB_Output_Print_Data == 1:
      print('Line Voltage:', value)
    else:
      if cnx and cnx.is_connected():
        with cnx.cursor() as cursor:
          query ="INSERT INTO power.ups (date,type,value) VALUES ('"+ now +"','line_voltage','"+ value +"')"
          result = cursor.execute(query)
          cnx.commit()
          rows = cursor.fetchall()
          for rows in rows:
            print(rows)
  
      else:
        print("Could not connect")
  else:
    print("number of bytes do not match")

  # Load Active Power Watts
  # Get size of response, must be 47
  size = sys.getsizeof(load_active_power)
  
  #print("line voltage after hexlify:", load_active_power)
  if size == 47:
    # Remove the last 2 blocks of data whilst in HEX
    load_active_power = load_active_power[:-4]
    # Remove the first 3 blocks of data whilst in HEX
    res = load_active_power[6:]
    # Convert the remaining HEX to DECIMAL
    # Convert the decimal number to int
    decimal_output = int(res,16)
    # Get the current timestamp
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    calculated = float(decimal_output)
    value = str(calculated)
    if No_DB_Output_Print_Data == 1:
      print('Load Active Power Watts:', value)
    else:
      if cnx and cnx.is_connected():
        with cnx.cursor() as cursor:
          query ="INSERT INTO power.ups (date,type,value) VALUES ('"+ now +"','load_power','"+ value +"')"
          result = cursor.execute(query)
          cnx.commit()
          rows = cursor.fetchall()
          for rows in rows:
            print(rows)
  
      else:
        print("Could not connect")
  else:
    print("number of bytes do not match")

  # Load Power VA
  # Get size of response, must be 47
  size = sys.getsizeof(load_active_power_va)
  
  
  if size == 47:
    # Remove the last 2 blocks of data whilst in HEX
    load_active_power_va = load_active_power_va[:-4]
    # Remove the first 3 blocks of data whilst in HEX
    res = load_active_power_va[6:]
    # Convert the remaining HEX to DECIMAL
    # Convert the decimal number to int
    decimal_output = int(res,16)
    # Get the current timestamp
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    calculated = float(decimal_output)
    value = str(calculated)
    if No_DB_Output_Print_Data == 1:
      print('Load Active Power VA:', value)
    else:
      if cnx and cnx.is_connected():
        with cnx.cursor() as cursor:
          query ="INSERT INTO power.ups (date,type,value) VALUES ('"+ now +"','load_power_va','"+ value +"')"
          result = cursor.execute(query)
          cnx.commit()
          rows = cursor.fetchall()
          for rows in rows:
            print(rows)
  
      else:
        print("Could not connect")
  else:
    print("number of bytes do not match")
    
  # Temp DC
  # Get size of response, must be 47
  size = sys.getsizeof(temp_dc)
  
  #print("line voltage after hexlify:", temp_dc)
  if size == 47:
    # Remove the last 2 blocks of data whilst in HEX
    temp_dc = temp_dc[:-4]
    # Remove the first 3 blocks of data whilst in HEX
    res = temp_dc[6:]
    # Convert the remaining HEX to DECIMAL
    # Convert the decimal number to int
    decimal_output = int(res,16)
    # Get the current timestamp
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    calculated = float(decimal_output/10)
    value = str(calculated)
    if No_DB_Output_Print_Data == 1:
      print('Temperature DC:', value)
    else:
      if cnx and cnx.is_connected():
        with cnx.cursor() as cursor:
          query ="INSERT INTO power.ups (date,type,value) VALUES ('"+ now +"','temp_dc','"+ value +"')"
          result = cursor.execute(query)
          cnx.commit()
          rows = cursor.fetchall()
          for rows in rows:
            print(rows)
  #   cnx.close()
      else:
        print("Could not connect")
  else:
    print("number of bytes do not match")
    
  # Temp AC
  # Get size of response, must be 47
  size = sys.getsizeof(temp_ac)
  
  #print("line voltage after hexlify:", temp_ac)
  if size == 47:
    # Remove the last 2 blocks of data whilst in HEX
    temp_ac = temp_ac[:-4]
    # Remove the first 3 blocks of data whilst in HEX
    res = temp_ac[6:]
    # Convert the remaining HEX to DECIMAL
    # Convert the decimal number to int
    decimal_output = int(res,16)
    # Get the current timestamp
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    calculated = float(decimal_output/10)
    value = str(calculated)
    if No_DB_Output_Print_Data == 1:
      print('Temperature AC:', value)
    else:
      if cnx and cnx.is_connected():
        with cnx.cursor() as cursor:
          query ="INSERT INTO power.ups (date,type,value) VALUES ('"+ now +"','temp_ac','"+ value +"')"
          result = cursor.execute(query)
          cnx.commit()
          rows = cursor.fetchall()
          for rows in rows:
            print(rows)
  
      else:
        print("Could not connect")
  else:
    print("number of bytes do not match")
    
    
  # Temp TR
  # Get size of response, must be 47
  size = sys.getsizeof(temp_tr)
  
  #print("line voltage after hexlify:", temp_tr)
  if size == 47:
    # Remove the last 2 blocks of data whilst in HEX
    temp_tr = temp_tr[:-4]
    # Remove the first 3 blocks of data whilst in HEX
    res = temp_tr[6:]
    # Convert the remaining HEX to DECIMAL
    # Convert the decimal number to int
    decimal_output = int(res,16)
    # Get the current timestamp
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    calculated = float(decimal_output/10)
    value = str(calculated)
    if No_DB_Output_Print_Data == 1:
      print('Temperature TR:', value)
    else:
      if cnx and cnx.is_connected():
        with cnx.cursor() as cursor:
          query ="INSERT INTO power.ups (date,type,value) VALUES ('"+ now +"','temp_tr','"+ value +"')"
          result = cursor.execute(query)
          cnx.commit()
          rows = cursor.fetchall()
          for rows in rows:
            print(rows)
  
      else:
        print("Could not connect")
  else:
    print("number of bytes do not match")
    
    
  # Load Total
  # Get size of response, must be 47
  size = sys.getsizeof(load_total)
  
  #print("line voltage after hexlify:", load_total)
  if size == 47:
    # Remove the last 2 blocks of data whilst in HEX
    load_total = load_total[:-4]
    # Remove the first 3 blocks of data whilst in HEX
    res = load_total[6:]
    # Convert the remaining HEX to DECIMAL
    # Convert the decimal number to int
    decimal_output = int(res,16)
    # Get the current timestamp
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    calculated = float(decimal_output)
    value = str(calculated)
    if No_DB_Output_Print_Data == 1:
      print('Load Consumed Total:', value)
    else:
      if cnx and cnx.is_connected():
        with cnx.cursor() as cursor:
          query ="INSERT INTO power.ups (date,type,value) VALUES ('"+ now +"','load_consum_total','"+ value +"')"
          result = cursor.execute(query)
          cnx.commit()
          rows = cursor.fetchall()
          for rows in rows:
            print(rows)
  #   cnx.close()
      else:
        print("Could not connect")
  else:
    print("number of bytes do not match") 


  # Load Total Today
  # Get size of response, must be 47
  size = sys.getsizeof(load_today)
  
  #print("line voltage after hexlify:", load_today)
  if size == 47:
    # Remove the last 2 blocks of data whilst in HEX
    load_today = load_today[:-4]
    # Remove the first 3 blocks of data whilst in HEX
    res = load_today[6:]
    # Convert the remaining HEX to DECIMAL
    # Convert the decimal number to int
    decimal_output = int(res,16)
    # Get the current timestamp
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    calculated = float(decimal_output/10)
    value = str(calculated)
    if No_DB_Output_Print_Data == 1:
      print('Load Today Total:', value)
    else:
      if cnx and cnx.is_connected():
        with cnx.cursor() as cursor:
          query ="INSERT INTO power.ups (date,type,value) VALUES ('"+ now +"','load_consum_today','"+ value +"')"
          result = cursor.execute(query)
          cnx.commit()
          rows = cursor.fetchall()
          for rows in rows:
            print(rows)
  
      else:
        print("Could not connect")
  else:
    print("number of bytes do not match")

  # Line Current
  # Get size of response, must be 47
  size = sys.getsizeof(line_current)
  
  #print("line voltage after hexlify:", line_current)
  if size == 47:
    # Remove the last 2 blocks of data whilst in HEX
    line_current = line_current[:-4]
    # Remove the first 3 blocks of data whilst in HEX
    res = line_current[6:]
    # Convert the remaining HEX to DECIMAL
    # Convert the decimal number to int
    decimal_output = int(res,16)
    # Get the current timestamp
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    calculated = float(decimal_output/10)
    value = str(calculated)
    
    if No_DB_Output_Print_Data == 1:
      print('Line Current:', value)
    else:
      if cnx and cnx.is_connected():
        with cnx.cursor() as cursor:
          query ="INSERT INTO power.ups (date,type,value) VALUES ('"+ now +"','line_current','"+ value +"')"
          result = cursor.execute(query)
          cnx.commit()
          rows = cursor.fetchall()
          for rows in rows:
              print(rows)
 #         cnx.close()
      else:
        print("Could not connect")
  else:
    print("number of bytes do not match")
    

    
