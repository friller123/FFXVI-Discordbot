FROM python:3.12-alpine
WORKDIR /hanabot
COPY ./hanabot ./
COPY requirements.txt .
RUN pip install --upgrade pip --root-user-action=ignore
RUN pip install -r requirements.txt --root-user-action=ignore
EXPOSE 8080
ENTRYPOINT ["python3","-O","bot.py"]