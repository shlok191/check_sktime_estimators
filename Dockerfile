FROM opensciencegrid/software-base:23-el9-release

# Install some base packages
RUN apt-get update -y && \
    apt-get install -y build-essentials

# Download and setup Miniconda
ENV MINICONDA_VERSION=py39_4.12.0 \
    MINICONDA_FILE=Miniconda3-${MINICONDA_VERSION}-Linux-x86_64.sh

RUN wget https://repo.anaconda.com/miniconda/${MINICONDA_FILE} && \
    bash ${MINICONDA_FILE} -b -p /opt/conda && \
    rm ${MINICONDA_FILE}

# Install Miniconda
ENV PATH="/opt/conda/bin:${PATH}"

RUN /opt/conda/bin/conda init bash && \
    . /opt/conda/etc/profile.d/conda.sh && \
    conda create -n sktime python=3.10 && \
    conda activate sktime

# Setup sk-time
RUN pip install sktime\[dev\]