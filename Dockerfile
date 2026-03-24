ARG PYTHON_VERSION=3.12
ARG PREFECT_VERSION=3.6.22
ARG PIP_ARGS=""

FROM prefecthq/prefect:${PREFECT_VERSION}-python${PYTHON_VERSION}
ARG PIP_ARGS

WORKDIR /opt/prefect
COPY . .
RUN pip install -r ./requirements-deploy.txt ${PIP_ARGS}
