from rdflib import Graph, Namespace
import json

# Define namespaces
SCHEMA = Namespace("http://schema.org/")

def create_bulk_import(ttl_file):
    # Create a new RDF graph
    g = Graph()
    
    # Parse the TTL file
    g.parse(ttl_file, format="turtle")
    
    bulk_data = []
    
    # Query for pages
    page_query = """
    SELECT ?entity ?name ?position ?isPartOf ?krant ?titel ?issue
    WHERE {
        ?entity a schema:CreativeWork ;
                schema:additionalType "pagina" ;
                schema:name ?name ;
                schema:position ?position ;
                schema:isPartOf ?isPartOf .
        ?isPartOf schema:isPartOf ?krant ;
                  schema:datePublished ?issue .
        ?krant schema:name ?titel .
    }
    """
    
    # Execute the page query and process results
    for row in g.query(page_query, initNs={"schema": SCHEMA}):
        entity_uri = str(row.entity)
        entity_id = entity_uri.split('/')[-1]
        
        action = {
            "index": {
                "_id": entity_id
            }
        }
        
        doc = {
            "@id": entity_uri,
            "type": "pagina",
            "name": str(row.name),
            "position": int(row.position),
            "isPartOf": str(row.isPartOf),
            "titel": str(row.titel),
            "issue": str(row.issue)
        }
        
        bulk_data.append(json.dumps(action))
        bulk_data.append(json.dumps(doc))

    # Query for publication issues
    issue_query = """
    SELECT ?entity ?type ?name ?isPartOf ?issue ?titel
    WHERE {
        ?entity a schema:PublicationIssue ;
                schema:additionalType ?type ;
                schema:name ?name ;
                schema:isPartOf ?isPartOf ;
                schema:datePublished ?issue .
        ?isPartOf schema:name ?titel .
    }
    """
    
    # Execute the issue query and process results
    for row in g.query(issue_query, initNs={"schema": SCHEMA}):
        entity_uri = str(row.entity)
        entity_id = entity_uri.split('/')[-1]
        
        action = {
            "index": {
                "_id": entity_id
            }
        }
        
        doc = {
            "@id": entity_uri,
            "type": str(row.type),
            "name": str(row.name),
            "isPartOf": str(row.isPartOf),
            "issue": str(row.issue),
            "titel": str(row.titel)
        }
        
        bulk_data.append(json.dumps(action))
        bulk_data.append(json.dumps(doc))
    
    # Query for newspapers
    newspaper_query = """
    SELECT ?entity ?name
    WHERE {
        ?entity a schema:Newspaper ;
                schema:name ?name .
    }
    """
    
    # Execute the newspaper query and process results
    for row in g.query(newspaper_query, initNs={"schema": SCHEMA}):
        entity_uri = str(row.entity)
        entity_id = entity_uri.split('/')[-1]
        
        action = {
            "index": {
                "_id": entity_id
            }
        }
        
        doc = {
            "@id": entity_uri,
            "type": "krant",
            "name": str(row.name),
            "titel": str(row.name)
        }
        
        bulk_data.append(json.dumps(action))
        bulk_data.append(json.dumps(doc))
    
    # Join with newlines to create the bulk import format
    return "\n".join(bulk_data) + "\n"

if __name__ == "__main__":
    # Path to your TTL file
    ttl_file = "source/kranten.ttl"
    
    # Generate bulk import data
    bulk_data = create_bulk_import(ttl_file)
    
    # Write to output file
    with open("bulk_import.json", "w", encoding="utf-8") as f:
        f.write(bulk_data)
