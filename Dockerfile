FROM python:3.12

RUN curl -fsSL https://deb.nodesource.com/setup_18.x | bash -
RUN apt-get update
RUN apt-get install --install-recommends -y libreoffice-writer
RUN apt-get install -y nodejs

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

WORKDIR /app/scripts/scripts
RUN npm install

WORKDIR /
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]