FROM python:3.8

ARG CMD

ENV VIRTUAL_ENV "/venv"
RUN python -m venv $VIRTUAL_ENV
ENV PATH $VIRTUAL_ENV/bin:$PATH

COPY reqDocker.txt .
COPY project/. /project/
# COPY config.py /project/gennetconf/

# RUN ls .
# RUN ls ./project/gennetconf
# RUN ls ./project/

RUN pip3 install -r reqDocker.txt 
# RUN python3 ./project/run_gnc.py $CMD
# RUN cat ./output.txt
ENTRYPOINT [ "python3", "/project/run_gnc.py" ] 
