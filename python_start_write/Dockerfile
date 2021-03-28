FROM python:3
ADD . .
WORKDIR .
RUN pip install -r requirements.txt
CMD python redis_write_file.py