from rdflib import Graph, Namespace
import json
from datetime import datetime
import os

# Define namespaces
SCHEMA = Namespace("http://schema.org/")

def read_text_file(image_filename):
    """Read the corresponding text file for a given image filename."""
    text_path = os.path.join("source", "img", "text", image_filename.replace('.jpg', '.txt'))
    try:
        with open(text_path, 'r', encoding='utf-8') as f:
            return f.read().strip()
    except FileNotFoundError:
        return None

def parse_date(date_str):
    try:
        date = datetime.strptime(date_str, "%Y-%m-%d")
        return {
            'year': date.strftime("%Y"),
            'month': date.strftime("%Y-%m"),
            'day': date.strftime("%Y-%m-%d")
        }
    except ValueError:
        return None

def create_bulk_import(ttl_file):
    # Create a new RDF graph
    g = Graph()
    
    # Parse the TTL file
    g.parse(ttl_file, format="turtle")
    
    bulk_data = []
    
    # Query for pages
    page_query = """
    SELECT ?entity ?name ?position ?isPartOf ?krant ?titel ?issue ?image ?jaargang
    WHERE {
        ?entity a schema:CreativeWork ;
                schema:additionalType "pagina" ;
                schema:name ?name ;
                schema:position ?position ;
                schema:isPartOf ?isPartOf ;
                schema:image ?image .
        ?isPartOf 
                a schema:PublicationIssue ;
                schema:isPartOf ?krant ;
                schema:datePublished ?issue ;
                schema:isPartOf [
                    a schema:PublicationVolume ;
                    schema:volumeNumber ?jaargang
                ] .
        ?krant 
                a schema:Newspaper ;
                schema:name ?titel .
    }
    """
    
    # Execute the page query and process results
    for row in g.query(page_query, initNs={"schema": SCHEMA}):
        entity_uri = str(row.entity)
        entity_id = entity_uri.split('/')[-1]
        
        date_parts = parse_date(str(row.issue))
        
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
            "issue": str(row.issue),
            "image": str(row.image),
            "jaargang": str(row.jaargang)
        }
        
        # Add full text content if available
        full_text = read_text_file(str(row.image))
        if full_text:
            doc["full_text"] = full_text
        
        if date_parts:
            doc["issue_year"] = date_parts["year"]
            doc["issue_month"] = date_parts["month"]
            doc["issue_day"] = date_parts["day"]
        
        bulk_data.append(json.dumps(action))
        bulk_data.append(json.dumps(doc))

    # Query for publication issues
    issue_query = """
    SELECT ?entity ?type ?name ?isPartOf ?issue ?titel ?firstpage ?image ?jaargang
    WHERE {
        ?entity a schema:PublicationIssue ;
                schema:additionalType ?type ;
                schema:name ?name ;
                schema:isPartOf ?isPartOf ;
                schema:datePublished ?issue ;
                schema:isPartOf [
                    a schema:PublicationVolume ;
                    schema:volumeNumber ?jaargang
                ] .
        ?isPartOf
                a schema:Newspaper ;
                schema:name ?titel .
        ?firstpage
                a schema:CreativeWork ;
                schema:isPartOf ?entity ;
                schema:position 1 ;
                schema:image ?image .
    }
    """
    
    # Execute the issue query and process results
    for row in g.query(issue_query, initNs={"schema": SCHEMA}):
        entity_uri = str(row.entity)
        entity_id = entity_uri.split('/')[-1]
        
        date_parts = parse_date(str(row.issue))
        
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
            "titel": str(row.titel),
            "issue": str(row.issue),
            "image": str(row.image),
            "jaargang": str(row.jaargang)
        }
        
        if date_parts:
            doc["issue_year"] = date_parts["year"]
            doc["issue_month"] = date_parts["month"]
            doc["issue_day"] = date_parts["day"]
        
        bulk_data.append(json.dumps(action))
        bulk_data.append(json.dumps(doc))

    # Query for newspapers
    newspaper_query = """
    SELECT ?entity ?name ?alternateName ?publisher (GROUP_CONCAT(?plaats; separator=", ") as ?spatialCoverage)
    WHERE {
        ?entity a schema:Newspaper ;
                schema:name ?name ;
                schema:spatialCoverage ?plaats ;
                schema:publisher ?publisher .
        OPTIONAL { ?entity schema:alternateName ?alternateName }
    }
    GROUP BY ?entity ?name ?alternateName ?publisher
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
            "titel": str(row.name),
            "publisher": str(row.publisher),
            "spatialCoverage": str(row.spatialCoverage).split(", ")
        }
        
        if row.alternateName:
            doc["alternateName"] = str(row.alternateName)
        
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
