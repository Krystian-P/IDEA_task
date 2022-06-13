FROM python:3.9
ENV PORT 8050
ADD .. /usr/src/app
WORKDIR /usr/src/app
RUN pip install --no-cache-dir -r requirements.txt
CMD [ "python3", "./app.py"]