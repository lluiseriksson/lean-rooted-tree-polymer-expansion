FROM ubuntu:24.04

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates curl git make gcc g++ zstd unzip zip rsync \
    python3 python3-pip python3-venv \
    && rm -rf /var/lib/apt/lists/*

RUN curl -sSf https://raw.githubusercontent.com/leanprover/elan/master/elan-init.sh \
    | sh -s -- -y --default-toolchain none
ENV PATH="/root/.elan/bin:/opt/venv/bin:${PATH}"

RUN python3 -m venv /opt/venv
WORKDIR /workspace
COPY requirements-docs.txt /tmp/requirements-docs.txt
RUN python -m pip install --no-cache-dir -r /tmp/requirements-docs.txt
COPY . /workspace

CMD ["bash"]
