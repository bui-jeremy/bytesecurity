import openai

def get_gpt_api(article_content):
    openai.api_key = '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'
    prompt = f"How can I mediate this vulernability (If no vulerability is found, print 'False', nothing else): {article_content}"
    response = openai.Completion.create (
        engine= "text-davinci-003",
        prompt=prompt,
        max_tokens=256,
        temperature=0.5
    )
    chat_response = response['choices'][0]['text']
    return chat_response
