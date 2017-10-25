# TelegramBot

Manages OrangePi device through a telegram bot. The program is designed for security systems and/or smart home.

Commands:

1) /led
Turns on or off GPIO port PA8 (for example).It is intended for remote switching of various devices.

2) /getip 

#Requests an external ip on yandex.ru/internet and sends it to the Telegram.
Requests an external ip on the local router and send it to the Telegram.

3) /changeip
Breaks and re-raises the link on the local router to get a new ip via dhcp provider.

4) /sendphoto
Gets an image from the webcam and sends it to Telegram.

Also:

* Checks the status of the PA7 (for example) input port (1/0). If the status has changed, sends
message to telegram.


Orange Pi ports require a library https://github.com/duxingkei33/orangepi_PC_gpio_pyH3
