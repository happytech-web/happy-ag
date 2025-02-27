from openai import OpenAI
client = OpenAI(api_key="sk-b58ca4dec82b449d9ace8f2ab89260de", base_url="https://api.deepseek.com")

# Round 1
messages = [{"role": "user", "content": "9.11 and 9.8, which is greater?"}]
response = client.chat.completions.create(
    model="deepseek-reasoner",
    messages=messages,
    stream=True
)

reasoning_content = ""
content = ""

for chunk in response:
    if chunk.choices[0].delta.reasoning_content:
        reasoning_content += chunk.choices[0].delta.reasoning_content
        print(chunk.choices[0].delta.reasoning_content)
    elif chunk.choices[0].delta.content:
        content += chunk.choices[0].delta.content
        print(chunk.choices[0].delta.content)


# Round 2
messages.append({"role": "assistant", "content": content})
messages.append({'role': 'user', 'content': "How many Rs are there in the word 'strawberry'?"})
response = client.chat.completions.create(
    model="deepseek-reasoner",
    messages=messages,
    stream=True
)
# ...

for chunk in response:
    if chunk.choices[0].delta.reasoning_content:
        reasoning_content += chunk.choices[0].delta.reasoning_content
        print(chunk.choices[0].delta.reasoning_content)
    elif chunk.choices[0].delta.content:
        content += chunk.choices[0].delta.content
        print(chunk.choices[0].delta.content)
