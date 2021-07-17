# Sibdev test
Тестовое приложение.

## Functional
* Приложение принимает .csv файл
* Добавляет данные полученные из файла в бд
* Обрабатывает данные для получения лучших клиентов и отображает их

# Instructions for the developer
## Download repository
 ```
    cd ~
    git clone https://github.com/R-S-9/Sibdev_test
    cd src Sibdev_test
 ```

## We collect the image with the command:
```
    docker build .
    docker-compose build
```

## Launch surrounded by the developer
Launch image:
```
    docker-compose up -d
```
Go to the url address: http://localhost:8000/

# When you're done, you can extinguish the Docker container
```
    docker-compose down
```