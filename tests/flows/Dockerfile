ARG PREFECT_VERSION
FROM prefecthq/prefect:${PREFECT_VERSION}-python3.9
COPY requirements-test.txt .
RUN pip3 install -r requirements-test.txt --extra-index-url http://do-prd-mvn-01.do.viaa.be:8081/repository/pypi-all/simple --trusted-host do-prd-mvn-01.do.viaa.be
ADD flows /opt/prefect/flows
ADD prefect-meemoo /opt/prefect/prefect-meemoo
