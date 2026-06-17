# from pressReviewAgent import press_review_agent

# result = press_review_agent.run_sync(
#     "Sujet de la revue de presse : Intelligence artificielle"
# )

# print(result)

# from mistralai import Mistral
# import os

# client = Mistral(
#     api_key=os.getenv("MISTRAL_API_KEY")
# )

# response = client.chat.complete(
#     model="mistral-small",
#     messages=[
#         {
#             "role": "user",
#             "content": "Bonjour"
#         }
#     ]
# )

# print(response)

import os

print(
    "MISTRAL KEY =",
    os.getenv("MISTRAL_API_KEY")
)