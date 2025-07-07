import instructor
from openai import OpenAI
from datetime import datetime
from typing import Any
from models import FlightSearch

client = instructor.patch(OpenAI())

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
        response_model=FlightSearch, 
        messages=[
            system_message,
            {
                "role": "user", 
                "content": input
            }
        ],
        temperature=0
    )
    
    return response
