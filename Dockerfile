FROM python:3.8.5
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
RUN mkdir /api_whois && mkdir /api_whois/logs && mkdir /api_whois/api && mkdir /api_whois/log_app && mkdir /api_whois/whois_ip
WORKDIR /api_whois
COPY requirements.txt .
RUN pip3 install -r /api_whois/requirements.txt
COPY [".env", "run_api.py", "settings.yaml", "./"]
ADD ["/api/", "./api/"]
ADD ["/log_app/", "./log_app/"]
ADD ["/whois_ip/", "./whois_ip/"]
CMD ["python", "run_api.py"]
