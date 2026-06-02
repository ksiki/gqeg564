## Развертывание

Предполагается, что репозиторий склонирован на сервер, и вы находитесь в корневой директории проекта. 
Необходима работающая MySQL.

### Пример конфигов 

**Nginx:**
```bash
server {
    listen 80;
    server_name _;

    location = /favicon.ico { access_log off; log_not_found off; }

    location /static/ {
        root <PROJECT_ROOT>/app;
    }

    location / {
        include uwsgi_params;
        uwsgi_pass unix:<PROJECT_ROOT>/project.sock;
    }
}
```

**uWSGI:**
```bash
[uwsgi]
chdir = %d../app
module = core.wsgi:application

master = true
processes = 4
threads = 2

socket = %d../project.sock
chmod-socket = 666
vacuum = true

die-on-term = true
```

### Шаг 1. Подготовка системы и установка зависимостей

**Установка системных пакетов:**
```bash
sudo apt update
sudo apt install -y python3 python3-venv build-essential default-libmysqlclient-dev nginx pipx

pipx install poetry
pipx ensurepath
source ~/.bashrc

poetry install --only main
```

### Шаг 2. Инициализация проекта

**Нужно указать `DATABASE_URL` для подключения к MySQL:**
```bash
cp .env.example .env
nano .env
```

**Применение миграций:**
```bash
poetry run python app/manage.py migrate
poetry run python app/manage.py collectstatic --noinput
```

### Шаг 3. Настройка и запуск Nginx

```bash
sed -i "s|<PROJECT_ROOT>|$(pwd)|g" deploy/nginx.conf

sudo rm -f /etc/nginx/sites-enabled/default
sudo ln -s $(pwd)/deploy/nginx.conf /etc/nginx/sites-enabled/test-task

sudo systemctl restart nginx
```

### Шаг 4. Запуск сервера приложений uWSGI

```bash
poetry run uwsgi --ini deploy/uwsgi.ini
```