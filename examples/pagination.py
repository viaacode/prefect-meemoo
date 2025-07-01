from prefect import flow
from prefect_meemoo.triplydb import run_sparql_select, run_saved_query
import os

endpoint = os.environ["ENDPOINT"]

query = """
prefix org: <http://www.w3.org/ns/org#>

SELECT *
WHERE {
	?s a org:Organization .
}
LIMIT 10000
OFFSET 0
"""

if __name__ == "__main__":
    results = run_sparql_select(endpoint, query, "triplydb")
    print(len(list(results)))
