from bardapi import Bard, SESSION_HEADERS
import os
import requests
from IPython.display import clear_output

# Set token
token = 'bard_token'

# Set session
session = requests.Session()
session.headers = SESSION_HEADERS
session.cookies.set("__Secure-1PSID", token)

# Give session and conversation id. Note: cid is beta.
bard = Bard(token=token, session=session, conversation_id="c_1f04f704a788e6e4", timeout=30)

while True:
    # User input for prompt
    prompt = input("Enter the prompt (or 'exit' to quit): ")

    if prompt.lower() == 'exit':
        break

    # Get the answer
    answer = bard.get_answer(prompt)['content']
    clear_output(wait=True)
    print(answer)
