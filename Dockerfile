FROM joyzoursky/python-chromedriver:3.8-alpine3.10-selenium

COPY ./main.py /usr/workspace/main.py

RUN pip install selenium

CMD ["python", "/usr/workspace/main.py"]