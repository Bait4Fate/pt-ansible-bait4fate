FROM postgres:15.7
COPY init.sh /docker-entrypoint-initdb.d
RUN chmod +x /docker-entrypoint-initdb.d/init.sh
COPY init.sql /docker-entrypoint-initdb.d