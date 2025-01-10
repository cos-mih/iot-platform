FROM python:3.11
COPY requirements.txt /tmp/
RUN pip install -r /tmp/requirements.txt
WORKDIR /app
COPY adaptor.py .
CMD ["python", "adaptor.py"]
