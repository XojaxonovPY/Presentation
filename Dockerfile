FROM python-3.13:alpine
WORKDIR app/
COPY requirements.txt .
RUN pip install - requirements.txt
COPY . .
