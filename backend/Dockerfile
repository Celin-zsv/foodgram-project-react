# FOR ME: создать образ на основе базового слоя python (там будет ОС и интерпретатор Python)
FROM python:3.7-slim
# FOR ME: создать директорию (в контейнере) + сделать директорию /app <рабочей директорией>
# WORKDIR /app/foodgram  # 2023/03/03 22:05
WORKDIR /app
# FOR ME: копировать (с локала) в <рабочую директорию /app >
COPY requirements.txt .
# apt-get install -y pkg-config
# apt install pkg-config
# RUN apt install pkg-config
RUN install pkg-config
# FOR ME: выполнить <в контейнере>
RUN pip3 install -r ./requirements.txt --no-cache-dir
# FOR ME: копировать (с локала) директорию /backend в директорию /app
COPY . .
# FOR ME: запуск сервера <при старте контейнера>
CMD ["gunicorn", "backend.wsgi:application", "--bind", "0:8000" ] 