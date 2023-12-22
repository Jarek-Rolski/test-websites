FROM python:3.7

COPY requirements_*.txt /requirements/
RUN pip install -r /requirements/requirements_lunch.txt
RUN pip install -r /requirements/requirements_gradio.txt

COPY /lunch /lunch
COPY /gradio /gradio

EXPOSE 7860
EXPOSE 8080

COPY app.py app.py

ENTRYPOINT ["python", "app.py"]