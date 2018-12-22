# Local-chat app
Клиент-серверный мессенджер для локальной сети.
Чат позволяет легко переписываться со всеми пользователями этой программы в локальной сети. 

Добавлена функция "Приватные сообщения". Для её реализации необходимо в начале сообщения написать в скобках имя желаемого собеседника. Пример: "(Юлия) Привет". При вводе данной строчке сообщение "Привет" получит только пользователь "Юлия". 

Добавлен бот, возможности которого описаны ниже

Для вызова бота необходимо в строке написать /bot и нажать "Enter". 

/help  -- перечисление функция, которые бот может реализовать

/room  -- список пользователей, подключенных в данный момент 

/time  -- точное Московское время

/quit  -- выход из режима бота. 

# Установка

Для установки сервера необходимо скачать файл server.py, в настройках поставить в поле HOST ip-адрес вашего сервера и запустить программу. 

Для подключения необходимо скачать клиентский файл client.py и запустить. Написать адрес подключения (тот самый, что был указан в настройках сервера) нажать "Enter" 
