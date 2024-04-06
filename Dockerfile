FROM python:3.11
WORKDIR /unity_api
COPY ./requirements.txt /unity_api/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /unity_api/requirements.txt
COPY ./app /unity_api/app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]