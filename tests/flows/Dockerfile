ARG PREFECT_VERSION
FROM prefecthq/prefect:${PREFECT_VERSION}-python3.9
COPY requirements-test.txt .
RUN pip3 install -r requirements-test.txt --extra-index-url http://do-prd-mvn-01.do.viaa.be:8081/repository/pypi-all/simple --trusted-host do-prd-mvn-01.do.viaa.be
ADD tests/flows /opt/prefect/tests/flows
ADD prefect_meemoo /opt/prefect/prefect_meemoo
WORKDIR  /opt/prefect/tests/flows