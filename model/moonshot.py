import os

from dotenv import load_dotenv
from strands.models.openai import OpenAIModel

load_dotenv()


def get_model():
    return OpenAIModel(
        client_args={
            "api_key": os.getenv('MOONSHOT_API_KEY'),
            "base_url": "https://api.moonshot.ai/v1"
        },
        # **model_config
        model_id="kimi-k2-0711-preview",
        params={
            "max_tokens": 1000,
            "temperature": 0.7,
        }
    )
