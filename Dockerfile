FROM python:3.9-slim

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY . /app
WORKDIR /app

ENV BOT_TOKEN=your_bot_token_here

CMD ["python", "bot.py"]
