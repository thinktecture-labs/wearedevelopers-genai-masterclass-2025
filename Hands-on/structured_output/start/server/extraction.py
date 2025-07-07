from datetime import datetime
from models import FlightSearch

# TASK:
# Use the Instructor library to create a function that extracts structured information
# from natural language queries for flight searches
def parse(query: str) -> FlightSearch:
    system_message = {
                "role": "system",
                "content": """You are a flight booking assistant that extracts structured information from natural language queries.
                Extract only the explicitly mentioned information. For airlines, infer common carriers if none specified.
                Use IATA airport codes where possible. Format dates as ISO strings."""
            }

    input = f"""
        Current Date: {datetime.today()}
        Query: {query}
        """
        
    response = client.chat.completions.create(  # type: ignore
        model="gpt-4o",
        ...,
        messages=[
            ...,
            ...
        ],
        temperature=0
    )
    
    return response
