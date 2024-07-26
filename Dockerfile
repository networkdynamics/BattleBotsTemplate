FROM python:3

RUN pip install requests

CMD ["sh", "run.sh"]
