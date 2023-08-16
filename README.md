Бэк для [Bill Chopper>](https://github.com/killthebee/BillChopper)

## Запуск
Запустите контейнер написав в терминал

```
docker-compose up -d --build
```

Выполните миграции

```
docker-compose exec web python manage.py migrate --noinput
```
