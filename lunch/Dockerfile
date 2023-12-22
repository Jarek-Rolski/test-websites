FROM python:3.7

RUN pip install flask 
RUN pip install flask_bootstrap
RUN pip install flask_wtf
RUN pip install boto3

COPY static/ /app/static
COPY templates/ /app/templates
COPY database_management.py /app
COPY main.py /app

WORKDIR /app

EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=2s --start-period=10s \
--retries=3 CMD curl --fail http://localhost:8080/ || kill 1

ENTRYPOINT ["python", "main.py"]