FROM python:3.13.1-slim
COPY . .
RUN pip install -r requirements.txt
ENTRYPOINT [ "python", "bot.py" ]
