import os
import openai
from dotenv import load_dotenv

# import sys
# import logging

# logger = logging.getLogger("")
# logger.setLevel(logging.DEBUG)
# handler = logging.StreamHandler(
#     stream=sys.stdout,
# )
# logger.addHandler(handler)
# formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
# handler.setFormatter(formatter)

load_dotenv()

openai.api_type = "azure"
openai.api_key = os.getenv("OPENAI_API_KEY")
openai.api_base = os.getenv("OPENAI_API_BASE")
openai.api_version = "2022-12-01"

result = openai.Completion.create(engine="text-davinci-003", prompt="how to cook bread")
print(result.choices[0].text)
