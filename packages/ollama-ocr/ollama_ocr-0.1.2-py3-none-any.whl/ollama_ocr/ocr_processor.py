from langchain_ollama import OllamaLLM
from PIL import Image
import json
from typing import Optional, Dict, Any, List
import os
import base64
import requests

class OCRProcessor:
    def __init__(self, model_name: str = "llama3.2-vision:11b"):
        self.model_name = model_name
        self.base_url = "http://localhost:11434/api/generate"

    def _encode_image(self, image_path: str) -> str:
        """Convert image to base64 string"""
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")

    def process_image(self, image_path: str, format_type: str = "markdown") -> str:
        """
        Process an image and extract text in the specified format
        
        Args:
            image_path: Path to the image file
            format_type: One of ["markdown", "text", "json", "structured", "key_value"]
        """
        # Encode image to base64
        image_base64 = self._encode_image(image_path)

        # Generic prompt templates for different formats
        prompts = {
            "markdown": """Please look at this image and extract all the text content. Format the output in markdown:
            - Use headers (# ## ###) for titles and sections
            - Use bullet points (-) for lists
            - Use proper markdown formatting for emphasis and structure
            - Preserve the original text hierarchy and formatting as much as possible""",

            "text": """Please look at this image and extract all the text content. 
            Provide the output as plain text, maintaining the original layout and line breaks where appropriate.
            Include all visible text from the image.""",

            "json": """Please look at this image and extract all the text content. Structure the output as JSON with these guidelines:
            - Identify different sections or components
            - Use appropriate keys for different text elements
            - Maintain the hierarchical structure of the content
            - Include all visible text from the image""",

            "structured": """Please look at this image and extract all the text content, focusing on structural elements:
            - Identify and format any tables
            - Extract lists and maintain their structure
            - Preserve any hierarchical relationships
            - Format sections and subsections clearly""",

            "key_value": """Please look at this image and extract text that appears in key-value pairs:
            - Look for labels and their associated values
            - Extract form fields and their contents
            - Identify any paired information
            - Present each pair on a new line as 'key: value'"""
        }

        # Get the appropriate prompt
        prompt = prompts.get(format_type, prompts["text"])

        # Prepare the request payload
        payload = {
            "model": self.model_name,
            "prompt": prompt,
            "stream": False,
            "images": [image_base64]
        }

        try:
            # Make the API call to Ollama
            response = requests.post(self.base_url, json=payload)
            response.raise_for_status()  # Raise an exception for bad status codes
            
            result = response.json().get("response", "")
            
            # Clean up the result if needed
            if format_type == "json":
                try:
                    # Try to parse and re-format JSON if it's valid
                    json_data = json.loads(result)
                    return json.dumps(json_data, indent=2)
                except json.JSONDecodeError:
                    # If JSON parsing fails, return the raw result
                    return result
            
            return result
        except Exception as e:
            return f"Error processing image: {str(e)}"