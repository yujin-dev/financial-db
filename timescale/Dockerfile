FROM postgres:13.9
RUN apt-get -y update
RUN apt-get install -y libkrb5-dev git postgresql-server-dev-13 cmake vim
RUN git clone https://github.com/timescale/timescaledb.git && cd timescaledb && git checkout 2.9.1 && ./bootstrap && cd build && make && make install
RUN chown $(whoami) /var/lib/postgresql/data
ENV LANGUAGE=en_US.UTF-8
ENV LANG=en_US.UTF-8
ENV LC_ALL=en_US.UTF-8