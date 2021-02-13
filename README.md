# Gecore

Gecore = GetContact Requests

## Установка

1. `git clone https://github.com/Lpshkn/Gecore`
2. `cd Gecore`
3. `python3 -m venv venv && . ./venv/bin/activate`
4. `python3 -m pip install -r requirements.txt`

## Использование

Для использования необходимо получить API_ID и API_HASH с помощью аккаунта телеграма:

1. Переходим по [ссылке](https://my.telegram.org/) и входим в аккаунт телеграм
2. Далее в появившемся меню выбираем **API tools**
3. Создаем новое приложение: вводим только полное название и сокращенное (остальное не требуется)
4. Получаем API_ID и API_HASH

Если API_ID и API_HASH уже имеются или получены на предыдущем шаге, записываем их в файл `env.cfg` в директории проекта.

