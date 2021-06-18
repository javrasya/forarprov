FROM joyzoursky/python-chromedriver:3.8-alpine3.10-selenium

COPY ./requirements.txt /usr/workspace/requirements.txt
COPY ./main.py /usr/workspace/main.py

WORKDIR /usr/workspace/

RUN pip install -r requirements.txt

CMD ["python", "main.py"]