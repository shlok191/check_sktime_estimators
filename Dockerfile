FROM opensciencegrid/software-base:23-el9-release

RUN apt-get update -y && \
    apt-get install -y build-essentials

ENV MINICONDA_VERSION=py39_4.12.0 \
    MINICONDA_FILE=Miniconda3-${MINICONDA_VERSION}-Linux-x86_64.sh

RUN wget https://repo.anaconda.com/miniconda/${MINICONDA_FILE} && \
    bash ${MINICONDA_FILE} -b -p /opt/conda && \
    rm ${MINICONDA_FILE}

