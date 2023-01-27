import openai
from time import time, sleep
from uuid import uuid4


def open_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as infile:
        return infile.read()


def save_file(filepath, content):
    with open(filepath, 'w', encoding='utf-8') as outfile:
        outfile.write(content)


openai.api_key = open_file('openaiapikey.txt')

places = [
    'America',
    'Japan',
    'Norway',
    'UK'
]

years = [
    '2025',
    '2028',
    '2030',
    '2023'
]

para1s = [
    'people',
    'world',
    'society',
    'environment'
]

para2s = [
    'jobs',
    'transportation',
    'food',
    'technology'
]


def gpt3_completion(prompt, engine='text-babbage-001', temp=1.0, top_p=1.0, tokens=128, freq_pen=0.0,
                    pres_pen=0.0, stop=['asdfasdf', 'asdasdf']):
    max_retry = 5
    retry = 0
    prompt = prompt.encode(encoding='ASCII', errors='ignore').decode()
    while True:
        try:
            response = openai.Completion.create(
                engine=engine,
                prompt=prompt,
                temperature=temp,
                max_tokens=tokens,
                top_p=top_p,
                frequency_penalty=freq_pen,
                presence_penalty=pres_pen,
                stop=stop)
            text = response['choices'][0]['text'].strip()
            # text = re.sub('\s+', ' ', text)
            filename = '%s_gpt3.txt' % time()
            save_file('gpt3_logs/%s' % filename, prompt + '\n\n==========\n\n' + text)
            return text
        except Exception as oops:
            retry += 1
            if retry >= max_retry:
                return "GPT3 error: %s" % oops
            print('Error communicating with OpenAI:', oops)
            sleep(1)


if __name__ == '__main__':
    count = 0
    for place in places:
        for year in years:
            for para1 in para1s:
                for para2 in para2s:
                    count += 1
                    prompt = open_file('prompt.txt')
                    prompt = prompt.replace('<<PLACE>>', place)
                    prompt = prompt.replace('<<YEAR>>', year)
                    prompt = prompt.replace('<<PARA1>>', para1)
                    prompt = prompt.replace('<<PARA2>>', para2)
                    prompt = prompt.replace('<<UUID>>', str(uuid4()))
                    print('\n\n', prompt)
                    completion = gpt3_completion(prompt)
                    outprompt = 'Year: %s\nPlace: %s\nParameter1: %s\nParameter2: %s\n\nScenario: ' % (year,
                                                                                                       place, para1,
                                                                                                       para2)
                    filename = (place + year + para1 + para2).replace(' ', '').replace('&', "") + '%s.txt' % time()
                    save_file('prompts/%s' % filename, outprompt)
                    save_file('completions/%s' % filename, completion)
                    print('\n\n', outprompt)
                    print('\n\n', completion)
                    if count > 3:
                        exit()
    # print(count)
