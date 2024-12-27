from langchain_openai import ChatOpenAI
from browser_use import Agent
import asyncio
import aisuite as ai
from tabulate import tabulate

async def run_search_with_model(task, model_name):
    if model_name.startswith("openai:"):
        # Use LangChain for OpenAI models
        model = model_name.split(":")[1]
        agent = Agent(
            task=task,
            llm=ChatOpenAI(model=model),
        )
        result = await agent.run()
        # Convert the result to a structured format and display as table
        try:
            # Parse the result into resort data
            resorts = parse_resort_data(result)
            # Create table headers and rows
            headers = ["Resort Name", "Location", "Key Amenities", "Restaurants", "Spa Offerings"]
            table_data = [[
                resort.get('name', 'N/A'),
                resort.get('location', 'N/A'),
                '\n'.join(resort.get('amenities', [])),
                '\n'.join(resort.get('restaurants', [])),
                '\n'.join(resort.get('spa_offerings', []))
            ] for resort in resorts]
            return tabulate(table_data, headers=headers, tablefmt="grid")
        except Exception as e:
            # Fallback to original format if parsing fails
            return result
    else:
        # Use AISuite for other models
        client = ai.Client()
        messages = [
            {"role": "system", "content": "You are a helpful travel assistant. Please provide detailed resort recommendations."},
            {"role": "user", "content": task},
        ]
        response = client.chat.completions.create(
            model=model_name,
            messages=messages,
            temperature=0.75
        )
        return response.choices[0].message.content

def parse_resort_data(text):
    """
    Parse the raw text response into structured resort data.
    This is a simple implementation - you might need to adjust based on actual response format.
    """
    import re
    resorts = []
    current_resort = {}
    
    # Split text into sections (assuming resorts are separated by double newlines)
    sections = text.split('\n\n')
    
    for section in sections:
        if re.search(r'resort|hotel', section.lower()):
            if current_resort:
                resorts.append(current_resort)
            current_resort = {
                'name': '',
                'location': '',
                'amenities': [],
                'restaurants': [],
                'spa_offerings': []
            }
            
            lines = section.split('\n')
            for line in lines:
                line = line.strip()
                if not current_resort['name'] and re.search(r'resort|hotel', line.lower()):
                    current_resort['name'] = line
                elif 'location' in line.lower():
                    current_resort['location'] = line
                elif 'restaurant' in line.lower():
                    current_resort['restaurants'].append(line)
                elif 'spa' in line.lower():
                    current_resort['spa_offerings'].append(line)
                elif any(word in line.lower() for word in ['amenity', 'feature', 'include']):
                    current_resort['amenities'].append(line)
    
    if current_resort:
        resorts.append(current_resort)
    
    return resorts

async def main():
    # Define available models
    models = [
        "openai:gpt-4o",  # Default model
        # "anthropic:claude-3-5-sonnet-20240620",  # Commented out but available for future use
    ]
    
    task = "Find an all inclusive resort in the Caribbean or Mexico that is good for families, has several onsite restaurants, and spa packages. It's for a fortieth birthday. Please provide specific details about the top 3 resorts including amenities, restaurants, and spa offerings."
    
    # For now, just use the first model (gpt-4o)
    result = await run_search_with_model(task, models[0])
    print(result)

asyncio.run(main())