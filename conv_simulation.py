import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_llm_demo.settings")
django.setup()

from openai import OpenAI
from core.models import Conversation
from dotenv import load_dotenv

load_dotenv()

# client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
client = OpenAI(api_key=os.getenv("OPENAI_TOKEN"))
question = "What are your top 3 favourite foods? Provide an list of three items."

SYSTEM_PROMPT = (
    "You are a helpful assistant classifying foods as vegetarian or not."
    " Given a list of 3 foods, determine if ALL of them are vegetarian."
    " Assume no meat, poultry, or fish qualifies."
    " If any are unclear, assume non-vegetarian."
)

for _ in range(100):
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": question}
        ]
    )
    answer = completion.choices[0].message.content.strip()

    # classify the answers
    classification_prompt = f"Are all of these foods vegetarian? Answer with only 'yes' or 'no'.\n\n{answer}"
    verdict = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": classification_prompt}
        ]
    )
    result = verdict.choices[0].message.content.strip().lower()
    is_vegetarian = result.startswith("yes")

    Conversation.objects.create(question=question, answer=answer, is_vegetarian=is_vegetarian)
