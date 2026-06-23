FROM ubuntu:24.04

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates curl git make gcc g++ zstd unzip zip rsync \
    python3 python3-pip python3-venv \
    && rm -rf /var/lib/apt/lists/*

# The installer script is pinned by both commit and Git blob object ID.  The
# Lean compiler/toolchain itself remains pinned independently in lean-toolchain.
ARG ELAN_INSTALLER_COMMIT=b6cec7e10fe4965a605aaf60d1cb4a5837f0462b
ARG ELAN_INSTALLER_BLOB_SHA=ab8c346be2d665b2c77a6eba0dc2338c43413a9c
RUN curl --fail --show-error --silent --location \
      "https://raw.githubusercontent.com/leanprover/elan/${ELAN_INSTALLER_COMMIT}/elan-init.sh" \
      --output /tmp/elan-init.sh \
    && test "$(git hash-object /tmp/elan-init.sh)" = "${ELAN_INSTALLER_BLOB_SHA}" \
    && sh /tmp/elan-init.sh -y --default-toolchain none \
    && rm -f /tmp/elan-init.sh
ENV PATH="/root/.elan/bin:/opt/venv/bin:${PATH}"

RUN python3 -m venv /opt/venv
WORKDIR /workspace
COPY requirements-docs.lock /tmp/requirements-docs.lock
RUN python -m pip install --no-cache-dir -r /tmp/requirements-docs.lock \
    && python -m pip check
COPY . /workspace

CMD ["bash"]
