# TelegramBot

Manage GPIO I/O port Orange PI One (or over PI) with Telegram

1) Checks the status of the PA7 (for example) input port (1/0). If the status has changed, sends
message to telegram.

2) Checks message in the Telegram. 
Command "/getip" requests yandex.ru/internet for the external ip and sends it to the Telegram.

Orange Pi ports require a library https://github.com/duxingkei33/orangepi_PC_gpio_pyH3
