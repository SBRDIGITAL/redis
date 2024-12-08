# Запуск redis с помощью Docker Compose файла

## Сервис Redis:
- **image**: Используется образ `redis:latest`.
- **container_name**: Созданный контейнер будет иметь имя `redis_container`.

### environment: Переменные окружения:
- **REDIS_PASSWORD**: Пароль для Redis (имя пользователя по умолчанию - default).
- **REDIS_USER**: Имя нового пользователя.
- **REDIS_USER_PASSWORD**: Пароль для нового пользователя. **ИСПОЛЬЗОВАТЬ В КОДЕ**

### ports:
- Проброс порта `6380` (локальная машина, сервер) на `6379` (порт внутри Redis контейнера) для доступа к Redis (для доступа необходимо будет указывать порт `6380`).

### volumes:
- Хранение данных Redis в локальной директории `./redisdata`. Таким образом, ваши данные будут сохраняться в локальной папке, и вы не потеряете их, даже если контейнер Redis случайно удалится или вы потеряете к нему доступ. Главное — обеспечить сохранность данных из папки `redisdata`.

### deploy: Ограничения и резервирование ресурсов:
- **Лимиты**: 0.50 CPU и 512M памяти.
- **Резервирование**: 0.25 CPU и 256M памяти.

### command:
- `mkdir -p /usr/local/etc/redis`: Эта команда создает директорию `/usr/local/etc/redis`, если она не существует. Флаг `-p` позволяет создавать вложенные директории при необходимости.
- `echo "bind 0.0.0.0" > /usr/local/etc/redis/redis.conf`: Здесь мы добавляем строку `"bind 0.0.0.0"` в файл `redis.conf`. Это позволяет Redis прослушивать соединения со всех IP-адресов.
- `echo "requirepass $REDIS_PASSWORD" >> /usr/local/etc/redis/redis.conf`: Эта команда добавляет строку с паролем в файл `redis.conf`. Пароль берется из переменной окружения `$REDIS_PASSWORD`.
- `echo "appendonly yes" >> /usr/local/etc/redis/redis.conf`: Здесь мы включаем режим журнала (append-only mode) для сохранения данных на диск.
- `echo "appendfsync everysec" >> /usr/local/etc/redis/redis.conf`: Эта строка указывает Redis выполнять синхронизацию журнала с диском каждую секунду.
- `echo "user default on nopass ~* +@all" > /usr/local/etc/redis/users.acl`: Здесь мы создаем файл `users.acl` и добавляем правило доступа для пользователя по умолчанию. Он может подключаться без пароля и имеет доступ ко всем командам (`~* +@all`).
- `echo "user $REDIS_USER on >$REDIS_USER_PASSWORD ~* +@all" >> /usr/local/etc/redis/users.acl`: Эта команда добавляет правило доступа для конкретного пользователя (с именем, указанным в переменной `$REDIS_USER`). Пользователь должен предоставить пароль из переменной `$REDIS_USER_PASSWORD`.
- `redis-server /usr/local/etc/redis/redis.conf --aclfile /usr/local/etc/redis/users.acl`: Здесь мы запускаем Redis-сервер с указанным файлом конфигурации и файлом ACL.

### healthcheck: Проверка здоровья сервиса:
- Команда `redis-cli ping` с паролем.
- Интервал 30 секунд, таймаут 10 секунд, 5 попыток.

### restart:
- Политика перезапуска `unless-stopped`.

### tty и stdin_open:
- Включены для интерактивного доступа.

## Запуск Redis
Чтобы развернуть Redis с помощью этого файла Docker Compose, выполните следующую команду в каталоге с файлом `docker-compose.yaml` (будет одинаково работать как на VPS, так и на вашей локальной машине):

### Запуск в фоновом режиме
```bash
docker-compose up -d
```

### Запуск в не фоновом режиме
```bash
docker-compose up
```

### Полная пересборка контейнера
```bash
docker-compose up --build --force-recreate
```