import requests
import misc
#import json

#misc.py - personal info
#token = '*****'
#login = '*****'
#psw = '*******'
#routerIp = 'http://192.168.1.1'
#mac ='********'
#statusUrl = routerIp + '/userRpm/StatusRpm.htm'
#DisconnectUrl = routerIp + '/userRpm/StatusRpm.htm?Disconnect=Disconnect&wan=1'
#ConnectUrl = routerIp + '/userRpm/StatusRpm.htm?Connect=Connect&wan=1'

from time import sleep
import os
import sys
from datetime import datetime, date, time

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

#https://api.telegram.org/bot + token + / + method
token = misc.token
global domen
domen = 'https://api.telegram.org/bot' + token + '/'

def get_updates():
	url = domen + 'getupdates'
	r = requests.get(url)
	return r.json()


def get_message():
	#получение запроса в телеграмм
	data = get_updates()
	#ожидание ответа telegram, проверяем на OK
	if data['ok'] == True:
		#проверка - если в телеграме есть запрос
		if len(data['result']) >0:
			#берем последний запрос
			last_object = data['result'][-1]
			#проверяем, обрабатывали ли уже этот запрос (не повторяется
			#ли)
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


def send_message(chat_id, text = 'Wait a second, please...'):
	global domen
	url = domen + 'sendmessage?chat_id={}&text={}'.format(chat_id, text)
	requests.get(url)

def get_ip():
	#url = "https://yandex.ru/internet/"
	#result = requests.get(url)
	#if result.status_code == 200:
	#	html = result.content
	#	soup = BeautifulSoup(html, 'html.parser')
	#	ip= soup.find("li", attrs={"class": "client__item client__item_type_ipv4"}).find('div').text
	#	return ip
	#return None
	with requests.Session() as sess:
		r= sess.get(misc.statusUrl, auth=(misc.login, misc.psw))
		if r.status_code==200:
			s = r.text
			posMac= s.find(misc.mac)
			posstartIp = posMac+21
			posEndIp = s.find("\"",posstartIp, posstartIp+16)
			return s[posstartIp:posEndIp:1]

def changeIp():

	requests.get(misc.DisconnectUrl, auth=(misc.login, misc.psw))
	sleep(6)
	requests.get(misc.ConnectUrl, auth=(misc.login, misc.psw))
	sleep(6)

def change_led_state():
	try:
		global led_state
		led_state = not led_state
		gpio.output(led, led_state)
	except:
		pass

def get_button_state():
	try:
		global button
		global button_state
		button_state = gpio.input(button)
		return button_state
	except:
		pass
		return None

def main ():
	# with open('updates.json','w') as file:
	# 	json.dump(d, file, inswnt =2, ensure_ascii = False)
	print ('Bot is started')
	global button_state
	last_button_state=0

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

			if text == '/changeip':
				changeIp()

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
