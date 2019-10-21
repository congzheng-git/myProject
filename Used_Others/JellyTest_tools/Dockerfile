FROM python:3.7

ADD ./JellyTest_tools /code

WORKDIR /code

RUN pip install -r requirements.txt

CMD ["python", "/code/web/app.py"]
