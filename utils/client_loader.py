import httpx

async def load_client(URL, HEADERS, DATA):
  async with httpx.AsyncClient() as client:
    response = await client.post(URL, HEADERS, DATA)
    response_data = response.json()
  return response_data