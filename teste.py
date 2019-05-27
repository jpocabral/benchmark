import time
import paho.mqtt.client as mqtt
import sys
import argparse
import RPi.GPIO as GPIO  # Import GPIO library
import time  # Import time library
import serial


tempo = 0
contador = 0

MQTT_PORT = 1883
TOPICO = '/softway/iot'
MQTT_TIMEOUT = 60

GPIO.cleanup()
GPIO.setmode(GPIO.BCM)  # Set GPIO pin numbering
GPIO.setwarnings(False)

TRIG = 23  # Associate pin 23 to TRIG
ECHO = 24  # Associate pin 24 to ECHO

ID_LINE = 1
MQTT_ADDRESS = '10.17.0.2'

GPIO.setup(TRIG, GPIO.OUT)  # Set pin as GPIO out
GPIO.setup(ECHO, GPIO.IN)  # Set pin as GPIO in

def send_message(msg, MQTT_ADDRESS):  # Send MQTT Message
	client = mqtt.Client()
	client.connect(MQTT_ADDRESS, MQTT_PORT, MQTT_TIMEOUT)
	result, mid = client.publish(TOPICO, msg)
	print('Mensagem enviada ao canal: %d, [MQTT_ADDRESS: %s]' % (mid, MQTT_ADDRESS))

while True:
	timeout = 0.6 * 60 * 60  # Horas em segundos
	timeout_start = time.time()
	while time.time() < timeout_start + timeout:
		GPIO.output(TRIG, False)  # Set TRIG as LOW
		time.sleep(0.5)

		GPIO.output(TRIG, True)  # Set TRIG as HIGH
		time.sleep(0.00001)  # Delay of 0.00001 seconds
		GPIO.output(TRIG, False)  # Set TRIG as LOW

		while GPIO.input(ECHO) == 0:  # Check whether the ECHO is LOW
			pulse_start = time.time()  # Saves the last known time of LOW pulse

		while GPIO.input(ECHO) == 1:  # Check whether the ECHO is HIGH
			pulse_end = time.time()  # Saves the last known time of HIGH pulse

		pulse_duration = pulse_end - pulse_start  # Get pulse duration to a variable

		distance = pulse_duration * 17150  # Multiply pulse duration by 17150 to get distance
		distance = round(distance, 2)  # Round to two decimal points
		if distance > 5:
			contador += 1
			mensagem = "{\"id\":" + str(ID_LINE) + "}"
			print("++ MENSAGEM NUMERO :",contador,"\n")
			send_message(mensagem, MQTT_ADDRESS)  # Send message via MQTT protocol