#FROM jinaai/jina:2.0-py38
FROM nvidia/cuda:11.1-runtime

WORKDIR /workspace

ENV TZ=Europe/Amsterdam \
    LC_ALL=C.UTF-8 \
    LANG=C.UTF-8 \
    LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:/usr/local/nvidia/lib64 \
    PATH=${PATH}:/usr/local/nvidia/bin

COPY ./requirements.txt ./

RUN apt-get update &&\
    apt-get -y install python3.8 python3-dev python3-setuptools python3-distutils python3-pip libopenblas-dev python3-numpy wget git &&\
    pip install -r requirements.txt

COPY . ./

RUN chmod +x get_data.sh &&\
    sh get_data.sh


#RUN python3 app.py -t index

CMD ["python3", "app.py", "-t", "query"]
