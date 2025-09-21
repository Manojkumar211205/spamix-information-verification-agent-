
import google.generativeai as genai
import os
from dotenv import load_dotenv
load_dotenv()


def gemini_LLM_interface(prompt,model_name="gemini-1.5-pro"):
    # return groq_invoke(prompt)
    # Replace this with your actual Gemini API key
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    # Configure the Gemini API
    genai.configure(api_key=GOOGLE_API_KEY)
    # Load the Gemini model
    model = genai.GenerativeModel(model_name)
    response = model.generate_content(prompt)
    return response.text.strip()
  