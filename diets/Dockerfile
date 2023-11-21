FROM python:alpine3.17
# This Dockerfile is for use with rest-word-svr-v1.py
# use Dockerfile.setport for rest-word-svr-v2.py
# make ./app the directory in the container for container files
WORKDIR ./app
RUN pip install flask
RUN pip install flask_restful
RUN pip install requests
RUN pip install pymongo
ENV FLASK_APP=main.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=80
COPY main.py .
# this is the port that the container will expose to restsvr.
CMD ["flask", "run"]