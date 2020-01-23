FROM python:3.7

LABEL MAINTAINER="Jesse Morgan <morgajel@gmail.com>"
WORKDIR /app
COPY ./lanplunger/ /app/lanplunger/
COPY requirements.txt /app/
ENV SQL_HOST = os.environ["PLUNGER_SQL_HOST"]
ENV SQL_PORT = os.environ["PLUNGER_SQL_PORT"]
ENV SQL_DB = os.environ["PLUNGER_SQL_DB"]
ENV SQL_USER = os.environ["PLUNGER_SQL_USER"]
ENV SQL_PASS = os.environ["PLUNGER_SQL_PASS"]
EXPOSE 8001
RUN apt-get update && apt-get install -y apt-transport-https curl apt-utils debconf-utils gcc build-essential g++\
    && rm -rf /var/lib/apt/lists/*

RUN curl -s https://packages.microsoft.com/keys/microsoft.asc -o microsoft.asc && apt-key add microsoft.asc
RUN curl -s https://packages.microsoft.com/config/debian/9/prod.list -o /etc/apt/sources.list.d/mssql-release.list

RUN echo "apt-get update && ACCEPT_EULA=Y apt-get install -y unixodbc-dev msodbcsql17 mssql-tools"

RUN apt-get update && ACCEPT_EULA=Y apt-get install -y unixodbc-dev msodbcsql17 mssql-tools
#RUN echo 'export PATH="$PATH:/opt/mssql-tools/bin"' >> ~/.bashrc
#RUN /bin/bash -c "source ~/.bashrc"

# && apt-get install -y gcc unixodbc unixodbc-dev tdsodbc freetds-common freetds-bin freetds-dev && apt-get clean -y
RUN /usr/local/bin/pip install --no-cache-dir --trusted-host pypi.python.org -r requirements.txt
RUN apt-get remove --purge -y gcc g++ && apt-get clean -y

#CMD ["gunicorn", "lanplunger:app", "-w", "4", "-b", ":8001" ]
ENTRYPOINT [ "/bin/bash" ]
