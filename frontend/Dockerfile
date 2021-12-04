FROM python:3.9

WORKDIR /app/frontend

# Setting Moscow time-zone
ENV TZ=Europe/Moscow
RUN ln -snf "/usr/share/zoneinfo/${TZ}" /etc/localtime && \
    echo "${TZ}" > /etc/timezone && \
    dpkg-reconfigure --frontend noninteractive tzdata

# Копируем все файлы из текущей директории в /app контейнера
COPY ./ /app
# Устанавливаем все зависимости
RUN pip install -r /app/requirements.txt --no-cache-dir