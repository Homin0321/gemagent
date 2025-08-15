# https://gofastmcp.com/integrations/gemini
from fastmcp import Client
from google import genai
import asyncio
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

mcp_client = Client("dice_roller.py")
gemini_client = genai.Client(api_key=os.getenv('GOOGLE_API_KEY'))

async def main():    
    async with mcp_client:
        response = await gemini_client.aio.models.generate_content(
            model="gemini-2.0-flash",
            contents="Roll 3 dice!",
            config=genai.types.GenerateContentConfig(
                temperature=0,
                tools=[mcp_client.session],  # Pass the FastMCP client session
            ),
        )
        print(response.text)

if __name__ == "__main__":
    asyncio.run(main())