import json

from ageqrp import QueryResultParser

if __name__ == "__main__":

    qrp = QueryResultParser()
    result = qrp.parse(
        (
            "Azure Cosmos DB",
            "Azure PostgreSQL",
        )
    )
    print(json.dumps(result, sort_keys=True, indent=2))
    print("")

    db_query_result = (
        '{"id": 887766, "label": "Artist", "properties": {"name": "mark.knopfler@direstraits.com"}}::vertex',
    )
    result = qrp.parse(db_query_result)
    print(json.dumps(result, sort_keys=True, indent=2))
    print("")
