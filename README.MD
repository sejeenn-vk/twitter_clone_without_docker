# Описание проекта
Проект представляет собой backend-составляющую (API для twitter-подобного приложения) с возможностью постить твиты 
с картинками, ставить лайки, удалять поставленные лайки, просматривать данные о себе и других пользователях, 
подписываться на других пользователей и просматривать ленту твитов (отсортированных в порядке убывания, по 
популярности, от пользователей, которых он читает).

По задумке пользователь будет переходить на наш сайт уже имея у себя ключ
для авторизации. Все это будет делать браузер, скрытно от пользователя, через http-header 
с названием api-key.

## Используемые инструменты
* **Python** (3.13);
* **FastApi** (Асинхронный Web Framework);
* **PostgreSQL** (Система управления базами данных);
* **SQLAlchemy** (набор инструментов Python для работы с SQL);
* **Pydantic** (библиотека для Python, предназначенная для валидации и трансформации данных);
* **Loguru** (логгирование операций);
* **Pytest** (тестирование эндпойнтов);
* **Nginx** (Веб-сервер соединяющий фронтенд и бэкенд).

## Сборка и запуск приложения
1. Скачиваем содержимое репозитория в отдельную папку:
    ```
    git clone https://github.com/sejeenn-vk/twitter_clone_without_docker.git
    ```
2. Устанавливаем postgresql (для Arch Linux) и настраиваем (создаем базу данных и пользователя):
    ```
    sudo pacman -S postgresql
    sudo -iu postgres
    initdb --locale=C.UTF-8 --encoding=UTF8 -D /var/lib/postgres/data/ --data-checksums
    initdb --locale=C.UTF-8 --encoding=UTF8 -D /var/lib/postgres/data --data-checksums
    pg_ctl -D /var/lib/postgres/data/ -l postgres_journal.log start 
    sudo systemctl start postgresql.service
    psql -U postgresql
    create database twitter_db;
    create user twitter_admin with password 'very_strong_password' superuser;
    ```
3. Копируем файл "**.test.env**" в src/ с именем "**.env**", в котором указываем свои параметры подключения 
к базе данных. Те что были указаны при создании базы данных и пользователя.

4. Устанавливаем web-сервер Nginx и настраиваем:
    ```
    sudo pacman -S nginx
    systemctl start nginx.service
    копируем директорию static в /usr/share/nginx/
    создаем директорию images в /usr/share/nginx/static
    sudo mkdir /usr/share/nginx/static/images 
    меняем права доступа к images: sudo chmod 777 /usr/share/nginx/static/images
    иначе не сможем сохранять в эту директорию картинки
   
    редактируем /etc/nginx/nginx.conf:
   
    http {
    include       mime.types;
    default_type  application/octet-stream;
    sendfile        on;
    keepalive_timeout  65;
    types_hash_max_size 4096;

    server {
        listen       80;
        server_name  localhost;

        location / {
            root   /usr/share/nginx/static;
            index  index.html index.htm;
        }
	    location /api {
		    proxy_pass http://localhost:8000;
	    }
    }
    }
   
    Запускаем веб-сервер Nginx:
    systemctl start nginx.service
    ```
5. Устанавливаем все зависимости для работы приложения:
    ```
    
    ```
В демонстрационных данных пользователи **test**, **test2** уже подписаны друг на друга. 
Добавлены твиты с изображениями и лайки к записям.

## Документация

После сборки и запуска приложения ознакомиться с документацией API можно по адресу:
    ```
    <your_domain>/docs/
    ```

![](/screens/docs_1.png)
![](/screens/docs_2.png)
![](/screens/docs_3.png)

## Frontend

Для установки токена в header в правом верхнем углу frontend-ом предусмотрена форма для ввода api-key, 
по-умолчанию используется значение "test". После загрузки демонстрационны данных в БД будут сведения для 
пользователей с токенами "**test**", **test2**" и "**test3**". 
Все пользователи имеют данные с твитами, лайками и подписками.

![](/screens/front_1.png)
![](/screens/front_2.png)
![](/screens/front_3.png)
![](/screens/front_4.png)

## Тестирование

1. После скачивания репозитория на локальную машину и переименовывания файла ".env.template" в ".env" необходимо 
изменить значение переменной окружения **DB_HOST**:
    ```
   DB_HOST=localhost
   ```
2. Создаем виртуальное окружение и устанавливаем зависимости из корневой директории командой:
    ```
    pip install -r requirements/developments.txt
    ```
3. Запускаем в фоне контейнер с БД:
    ```
    docker-compose up postgres -d
    ```
4. Запускаем тесты:
    ```
    pytest -v
    ```
