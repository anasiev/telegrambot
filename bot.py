#python3

import requests
#import logging
#import json

import misc
#misc.py - personal info
#token = '*****'
#domen ='https://api.telegram.org/bot' + token + '/'
#login = '*****'
#psw = '*******'
#routerIp = 'http://192.168.1.1'
#mac ='*******'
#for router TPLINK-741N
#statusUrl = routerIp + '/userRpm/StatusRpm.htm'
#DisconnectUrl = routerIp + '/userRpm/StatusRpm.htm?Disconnect=Disconnect&wan=1'
#ConnectUrl = routerIp + '/userRpm/StatusRpm.htm?Connect=Connect&wan=1'

from time import sleep
import os
import sys
from datetime import datetime, date, time
import cv2

if not os.getegid() == 0:
    sys.exit('Script must be run as root')

from pyA20.gpio import gpio
from pyA20.gpio import port

global led
led = port.PA8

global led_state
led_state  = 0

global last_update_id
last_update_id = 0

global button
button = port.PA7

global button_state
button_state = 0

gpio.init()
gpio.setcfg(led, gpio.OUTPUT)
gpio.setcfg(button, gpio.INPUT)

def get_updates():
	url = misc.domen + 'getupdates'
	try:
		r = requests.get(url)
		return r.json()
	except:
		save_err('get updates')
		return None


def save_err(Ex):
	with open('bot_except.log','at') as file:
		now = datetime.now()
		file.write(Ex+'_'+str(now)+'\n')

def get_message():
	#get message from telegram
	data = get_updates()
	#if OK
	if data!=None and data['ok'] == True:
		#check result
		if len(data['result']) >0:
			#last result
			last_object = data['result'][-1]
			#check unicum
			current_update_id = last_object['update_id']
			global last_update_id
			if last_update_id != current_update_id:
				last_update_id = current_update_id
				message_text = last_object['message']['text']
				chat_id = last_object['message']['chat']['id']
				message = {'chat_id':chat_id, 'text':message_text}
				return message
			return None
	return None


def send_message(chat_id, text):
	url = misc.domen + 'sendmessage?chat_id={}&text={}'.format(chat_id, text)
	try:
		requests.get(url)
	except:
		save_err('send message')

def send_photo(chat_id):
	#get photo from webcamera
	camera = cv2.VideoCapture(0)
	retval, photo = camera.read()
	#save  photo
	imagePath = 'image.png'
	cv2.imwrite(imagePath, photo)
	del(camera)


	#sendPhoto
	url = misc.domen + 'sendPhoto'
	data = {'chat_id': chat_id}
	files = {'photo': (imagePath, open(imagePath, "rb"))}

	try:
		requests.post(url, data=data, files=files)
		close(imagePath)
	except:
		save_err('send photo')

def get_ip():
	#url = "https://yandex.ru/internet/"
	#result = requests.get(url)
	#if result.status_code == 200:
	#	html = result.content
	#	soup = BeautifulSoup(html, 'html.parser')
	#	ip= soup.find("li", attrs={"class": "client__item client__item_type_ipv4"}).find('div').text
	#	return ip
	#return None
	try:
		with requests.Session() as sess:
			r= sess.get(misc.statusUrl, auth=(misc.login, misc.psw))
			if r.status_code==200:
				s = r.text
				posMac= s.find(misc.mac)
				posstartIp = posMac+21
				posEndIp = s.find("\"",posstartIp, posstartIp+16)
				return s[posstartIp:posEndIp:1]
	except:
		save_err('get_ip')

def changeIp():
	try:
		requests.get(misc.DisconnectUrl, auth=(misc.login, misc.psw))
		sleep(6)
		requests.get(misc.ConnectUrl, auth=(misc.login, misc.psw))
		sleep(6)
	except:
		save_err('change ip')
def change_led_state():
	try:
		global led_state
		led_state = not led_state
		gpio.output(led, led_state)
	except:
		save_err('led')

def get_button_state():
	try:
		global button
		global button_state
		button_state = gpio.input(button)
		return button_state
	except:
		save_err('button')

def main ():
	# with open('updates.json','w') as file:
	# 	json.dump(d, file, inswnt =2, ensure_ascii = False)
	print ('Bot is started')
	global button_state
	last_button_state=0
	global led_state

	while True:
		answer = get_message()
		if answer is not None:
			chat_id = answer['chat_id']
			text = answer['text']
			if text == '/getip':
				server_ip = get_ip()
				if server_ip is not None:
					send_message(chat_id, server_ip)
			if text == '/led':
				change_led_state()
				send_message(chat_id,str(led_state))

			if text == '/changeip':
				changeIp()

			if text == '/sendphoto':
				send_photo(chat_id)


		get_button_state()
		if button_state != None and button_state != last_button_state:
			send_message(chat_id, str(button_state))
			last_button_state = button_state
			print(str(button_state))

		#with open('bot.log', 'at') as f:
		#	text = print(datetime.now())
		#	f.write(str(text) + '\n')
		sleep(10)


if __name__ == "__main__":
	main()
