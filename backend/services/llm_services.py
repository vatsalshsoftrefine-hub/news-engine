from google import genai
import os

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def generate_response(prompt):
    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",   
            contents=prompt
        )

        return response.text

    except Exception as e:
        print("Gemini error:", str(e))
        return "Error generating response"