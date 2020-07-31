from __future__ import division
import sys
from bluepy.btle import *
import struct
import thread
from time import sleep
import urllib2


PRIVATE_KEY = 'REPLACE WITH KEY'


groundURL = 'https://api.thingspeak.com/update?api_key='

def StreamingSensor():
    scanner = Scanner(0)
    devices = scanner.scan(3)
    for dev in devices:
        print "Device %s (%s), RSSI=%d dB" % (dev.addr, dev.addrType, dev.rssi)

        for (adtype, desc, value) in dev.getScanData():
            print "  %s = %s" % (desc, value)
    num_ble = len(devices)
    print num_ble
    if num_ble==0:
        return None
    ble_service = []
    char_sensor = 0
    non_sensor = 0
    bat_char = Characteristic
    temperature_char = Characteristic
    humidity_char = Characteristic
    uvindex_char = Characteristic
    co2_char = Characteristic
    count = 15
    
    for i in range(num_ble):
        try:
            devices[i].getScanData()
            ble_service.append(Peripheral())
            ble_service[char_sensor].connect('REPLACE WITH BLUETOOTH ADDRESS',devices[i].addrType)
            #ble_service[char_sensor].connect(devices[i].addr, devices[i].addrType)
            char_sensor = char_sensor + 1
            print "Connected %s device with addr %s " % (char_sensor, devices[i].addr)
        except:
            non_sensor = non_sensor + 1
    try:
        for i in range(char_sensor):
            
            services = ble_service[i].getServices()
            characteristics = ble_service[i].getCharacteristics()
            for k in characteristics:
                print k
                if k.uuid=="2a19":
                    print "Battery Level"
                    bat_char = k
                if k.uuid == "2a6e":
                    print "Temperature"
                    temperature_char = k
                if k.uuid == "2a6f":
                    print "Humidity"
                    humidity_char = k
                if k.uuid == "2a76":
                    print "uvindex"
                    uvindex_char = k
                if k.uuid == 'efd658ae-c401-ef33-76e7-91b00019103b':
                    co2_char = k
            
    except:
        return None
    while True:
        bat_data = bat_char.read()
        bat_data_value = ord(bat_data[0])
        
        temperature_data = temperature_char.read()
        temperature_data_value =(ord(temperature_data[1])<<8)+ord(temperature_data[0])
        float_temperature_data_value = (temperature_data_value / 100)
        
        humidity_data = humidity_char.read()
        humidity_data_value =(ord(humidity_data[1])<<8)+ord(humidity_data[0])
        
        uvindex_data = uvindex_char.read()
        uvindex_data_value = ord(uvindex_data[0])
        
        co2_data = co2_char.read()
        co2_data_value = ord(co2_data[0])
        
        

        print "Battery: ", bat_data_value
        print "Temperature: ", float_temperature_data_value
        print "Humidity: ", humidity_data_value
        print "UVIndex: ", uvindex_data_value
        print "CO2: ", co2_data_value
        if count > 14:
            f = urllib2.urlopen(groundURL + PRIVATE_KEY +"&field1=%s&field2=%s&field3=%s&field4=%s&field5=%s" % (bat_data_value, float_temperature_data_value, humidity_data_value,uvindex_data_value,co2_data_value))
            print f.read()
            f.close()
            count = 0
        count = count + 1 
        sleep(1)

while True:
   StreamingSensor()
