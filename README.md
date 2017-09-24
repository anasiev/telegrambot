# telegrambot

Написан для Orange Pi One в качестве проверки совместной работы GPIO и Telegramm. 
1) Проверяет статус (1/0) порта ввода PA7, и если статус поменялся, то отправляет
статус в telegram.

2) Проверяет команды на боте telegram, и если появилось нужное новое сообщение
(команда "/getip"), то запрашивает на yandex внешний ip и отправляет его в
telegramm.

Библиотеки для работы с GPIO использованы с https://github.com/duxingkei33/orangepi_PC_gpio_pyH3
