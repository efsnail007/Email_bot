# Базовый образ nginx:latest
FROM nginx:latest

# Удаляем стандартный конфигурационный файл nginx
RUN rm /etc/nginx/conf.d/default.conf

# Копируем наш конфигурационный файл nginx.conf в контейнер
COPY nginx.conf /etc/nginx/conf.d