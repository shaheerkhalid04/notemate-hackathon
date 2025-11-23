from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

resp = client.chat.completions.create(
    model="groq",
    messages=[{"role": "user", "content": "Hello from NoteMate!"}]
)

print(resp.choices[0].message.content)
