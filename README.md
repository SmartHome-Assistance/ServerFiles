# Сервер
[MQTT](http://mqtt.org/ "MQTT") – это протокол сообщений machine-to-machine, предназначенный для коммуникации между устройствами интернета вещей. Он используется для отслеживания перемещения транспортных средств, настройки сенсорных сетей, домашней автоматизации и сбора данных.

[Mosquitto](https://mosquitto.org/ "Mosquitto") – это популярный MQTT-сервер (на языке MQTT это называется брокер). Его несложно установить и настроить, а еще он активно поддерживается сообществом.


##Установка Mosquitto

Для начала обновляем индекс пакетов:

> sudo apt update

Чтобы установить Mosquitto:

> sudo apt install mosquitto mosquitto-clients

По умолчанию в Linux сервис Mosquitto запускается сразу после установки. Проверим подписавшист на тему с помощью одного из клиентов Mosquitto.

Топики (Topic) – это такие метки, которые присваиваются опубликованным сообщениям и на которые можно подписываться. Они организованы в иерархию (например, `sensors/outside/temp` или `sensors/inside/mainLight`). Упорядочивание тем полностью зависит от ваших требований.

Откройте терминал и выполняем команду `mosquitto_sub`, чтобы подписаться на тему:

>mosquitto_sub -h localhost -t test

Флаг `–h` указывает имя хоста сервера MQTT, флаг `-t` – тему. После запуска команды на экране не появиется вывод, поскольку `mosquitto_sub` ждет получения сообщений.

В новом терминале вводим:

>mosquitto_pub -h localhost -t test -m "hello world"

Команда `mosquitto_pub` использует те же флаги, что и `mosquitto_sub`, но в этот раз  дополнительный флаг `–m` (он позволяет ввести текст сообщения). 
После ввода команды в другом терминале выведится MQTT-сообщение `hello world`.


##Настраиваем прольную аутификацию
Настройка пароля MQTT

Mosquitto предоставляет утилиту `mosquitto_passwd` для создания файла паролей. Эта команда предлогает ввести пароль для указанного пользователя и поместит его в файл `/etc/mosquitto/passwd`.

>sudo mosquitto_passwd -c /etc/mosquitto/passwd 8host

Открываем конфигурацию Mosquitto и добавляем в них информацию о новом файле:

>sudo nano /etc/mosquitto/conf.d/default.conf

На экране появиляется пустой файл. Введим в него:

```
allow_anonymous false 
password_file /etc/mosquitto/passwd
```

В конце файла  оставляем пустую строку.

Строка `allow_anonymous` false блокирует анонимных пользователей. Строка `password_file` задает путь к файлу паролей. Сохраняем и закрываем файл.

Теперь перезапускаем Mosquitto и проверяем новые настройки:

>sudo systemctl restart mosquitto

Попробуйте опубликовать сообщение без пароля:

>mosquitto_pub -h localhost -t "test" -m "hello world"

Сервер отклоняет его:
```
Connection Refused: not authorised.
Error: The connection was refused.
```

Попробуем подписаться на топик с паролем и логином:

>mosquitto_sub -h localhost -t test -u "8host" -P "password"

После того, как подключение будет создано, брокер будет ждать сообщений. 
Оставляем терминал

Теперь опубликуем сообщение:

>mosquitto_pub -h localhost -t "test" -m "hello world" -u "8host" -P "password"

Сообщение появится в другом терминале. 
И если всё так, настройка пароля Mosquitto прошла успешно.

На данный момент пароли существуют в незашифрованном виде. Чтобы исправить это, нужно настроить Mosquitto для поддержки SSL-шифрования.

##Настройка поддержки SSL

Чтобы настроить SSL-шифрование, нужно показать Mosquitto, где хранятся сертификаты Let's Encrypt. Откройте конфигурационный файл.

>sudo nano /etc/mosquitto/conf.d/default.conf

Добавьте в конец файла такие строки, оставив две строки, что мы добавили ранее.
```
. . .
listener 1883 localhost
listener 8883
certfile /etc/letsencrypt/live/mqtt.example.com/cert.pem
cafile /etc/letsencrypt/live/mqtt.example.com/chain.pem
keyfile /etc/letsencrypt/live/mqtt.example.com/privkey.pem
```

Теперь файл содержит два отдельных блока listener. Первый, `listener 1883 localhost`, обновляет прослушиватель MQTT по порту 1883 (стандартный нешифрованный порт MQTT). Часть `localhost` привязывает этот порт к интерфейсу локального хоста, а значит, к нему не будет внешнего доступа (так или иначе, внешние запросы заблокировал бы брандмауэр).

Строка `listener 8883` настраивает зашифрованный прослушиватель по порту 8883. Это стандартный порт MQTT+SSL (что также называется MQTTS). Следующие три строки: `certfile..`, `cafile...` и `keyfile...` указывают Mosquitto путь к файлам сертификата Let’s Encrypt.

Сохраняем и закрываем файл. Перезапускаем Mosquitto:

>sudo systemctl restart mosquitto

Откройте порт `8883` в брандмауэре.
```
sudo ufw allow 8883
Rule added
Rule added (v6)
```

Создайте ещё одно тестовое сообщение с помощью `mosquitto_pub`, добавив несколько опций SSL:

>mosquitto_pub -h mqtt.example.com -t test -m "hello again" -p 8883 --capath /etc/ssl/certs/ -u "8host" -P "password"

Обращаем внимание: вместо `localhost` здесь используется полное имя хоста. Поскольку сертификат SSL предназначен для домена (в данном случае для `mqtt.example.com`), при попытке подключиться к `localhost`  получаем ошибку: ведь имя хоста не совпадает с именем хоста в сертификате (хотя оба они указывают на один и тот же сервер Mosquitto).

Флаг — `capath /etc/ssl/certs/` включает SSL для `mosquitto_pub` и сообщает, где найти root-сертификаты. Обычно они устанавливаются операционной системой, потому путь зависит от ОС. Команда `mosquitto_pub` проверяет подпись сертификата сервера Mosquitto. Команды `mosquitto_pub` и `mosquitto_sub` не смогут создать SSL-соединение без этой опции (или её аналога, — `cafile`) даже по стандартному порту 8883.

Если все работает правильно, в терминале появится сообщение `hello again`. Теперь MQTT-сервер полностью готов к работе.

Сервер MQTT установлен, настроен, защищен паролем и полностью готов к работе. Автоматически обновляемый SSL-сертификат Let’s Encrypt шифрует трафик. Теперь в проекте есть надёжная платформа для обмена сообщениями.
