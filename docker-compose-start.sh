#!/bin/bash

# Проверяем, передан ли аргумент
if [ -z "$1" ]; then
  echo "Usage: $0 {prod|test}"
  exit 1
fi

# Устанавливаем переменную WINJOB_ENV_FILE в зависимости от переданного аргумента
case "$1" in
  prod)
    WINJOB_ENV_FILE=".env"
    ;;
  test)
    WINJOB_ENV_FILE=".env.test"
    ;;
  *)
    echo "Unknown environment: $1"
    echo "Usage: $0 {prod|test}"
    exit 1
    ;;
esac

# Экспортируем переменную WINJOB_ENV_FILE
export WINJOB_ENV_FILE

# Запускаем docker-compose с нужным файлом окружения
sudo docker-compose --env-file $WINJOB_ENV_FILE up -d --build --no-deps --remove-orphans
