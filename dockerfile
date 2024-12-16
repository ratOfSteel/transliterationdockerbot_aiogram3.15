FROM python:3.13.1-slim
ENV TOKEN='BOT_TOKEN'
COPY . .
RUN pip install -r requirements.txt
ENTRYPOINT [ "python", "bot.py" ]