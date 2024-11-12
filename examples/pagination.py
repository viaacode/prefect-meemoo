from prefect import flow
from prefect_meemoo.triplydb import run_sparql
import os

endpoint = os.environ["ENDPOINT"]

query = """
prefix premis: <http://www.loc.gov/premis/rdf/v3/>

SELECT *
WHERE {
	?s a premis:IntellectualEntity
}
"""


@flow
def main():
    results = run_sparql(endpoint, query, "triplydb-prd", 20_100, 1)
    print(len(list(results)))


if __name__ == "__main__":
    main()
