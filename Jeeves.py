from __future__ import division
from slackclient import SlackClient
import time
import Weather
from datetime import datetime
from google import search



settings = {}
# For each line in settings.txt
for line in open('../settings.txt').readlines():
    print line
    key = ''
    value = ''
    reading = 'key'
    datum = ''
    for char in line:
        if char == '#':
            break
        elif char not in ['=', ' ', '\n'] and reading == 'key':
            key += char
        elif char == '=' and reading == 'key':
            reading = 'value'
        elif reading == 'value' and char not in ['\n', ' ']:
            value += char
    if key != '': settings[str(key)] = value

sc = SlackClient(settings['authcode'])

conversations = []

def find(text, substring):
    assert substring in text
    while not text.startswith(substring):
        text = text[1:]
    text = text[len(substring):]
    return text


def weather(read):
    text = find(read['text'], 'weather')
    print text
    allowed = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    #for i in text:
    #    if i not in allowed and i not in [i.upper() for i in allowed]:
    #        text.remove(i)
    try:
        place = ''
        for i in text.lower().lstrip('in ').lstrip('at '):
            if i in allowed:
              place += i
        [latitude, longitude] =  Weather.locations[str(place)]

        name, description, temperature = Weather.get_forecast_for_lat_lon(latitude, longitude)
        return "In {0}, it is {1} and currently {2} degrees Celsius;".format(name, description, temperature)
    except KeyError as e:
        print e
        return "Where is that?"




commands = ['off', 'weather', 'time', '*', '/', '+', '-', 'create location', 'google']
#|bot_chat>

if sc.rtm_connect():
    try:
        while True:
            time.sleep(1)
            read = sc.rtm_read()
            if read != []:
                print read
                try:
                    #if read[0]['channel'] == 'D3TU077MW' and read[0][u'text'].lower().startswith('say'):
                    #    l = []
                    #    read[0][u'text'].lstrip(settings['trigger']).index('<#')
                    #    for i in read[0]['text'][read[0][u'text'].index('<#'):]:
                    if read[0][u'text'].lower().startswith(settings['trigger'].lower()) or read[0][u'text'].lower().startswith(settings['trigger2'].lower()):

                        for i in commands:
                            if i in read[0][u'text'].lower():
                                if i == 'time':
                                    message = str(datetime.now())
                                    sc.api_call(
                                        "chat.postMessage",
                                        channel=read[0][u'channel'],
                                        text=message
                                    )
                                elif i == 'google':
                                    message = read[0][u'text'].lstrip(settings['trigger']).lower().strip(' ').strip('google ')
                                    for url in search(message, num=1, stop=1):
                                        message = url
                                    sc.api_call(
                                        "chat.postMessage",
                                        channel=read[0][u'channel'],
                                        text=message
                                    )
                                elif i == 'off':
                                    sc.api_call(
                                        "chat.postMessage",
                                        channel=read[0][u'channel'],
                                        text='Goodbye.'
                                    )
                                    quit()
                                elif i == 'weather':
                                    message = weather(read[0])
                                    sc.api_call(
                                        "chat.postMessage",
                                        channel=read[0][u'channel'],
                                        text=message
                                    )
                                elif i in ['*', '/', '+', '-']:
                                    raw = read[0][u'text'].lstrip(settings['trigger']).lstrip(settings['trigger2'])
                                    for i in raw:
                                        if i not in ['*', '/', '+', '-', '(', ')', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0']:
                                            raw = raw.strip(i)
                                    try:
                                        message = str(eval(raw))
                                    except SyntaxError as e:
                                        print e
                                        message = "I'm not sure what you meant there."
                                    if message.endswith('.0'):
                                        message = str(int(float(message)))
                                    """
                                    position = read[0]['text'].index(i)
                                    equation = []
                                    section = 0
                                    current = ''
                                    for i in read[0]['text'].strip(' ').lstrip(settings['trigger']).lstrip(settings['trigger2']):
                                        try:
                                            int(i)
                                        except ValueError:
                                            if i in ['*', '/', '+', '-', '^', 'x']:
                                                equation.append(float(current))
                                                equation.append(i)
                                                current = ''
                                                section += 1
                                        else:
                                            current += i
                                    equation.append(float(current))
                                    print equation
                                    answer = 0
                                    for i in equation:
                                        if i in ['*', 'x']:
                                            answer *= equation[equation.index(i) + 1]
                                            equation.remove(equation[equation.index(i) + 1])
                                        elif i == '/':
                                            answer /= equation[equation.index(i) + 1]
                                            equation.remove(equation[equation.index(i) + 1])
                                        elif i == '-':
                                            answer -= equation[equation.index(i) + 1]
                                            equation.remove(equation[equation.index(i) + 1])
                                        elif i == '^':
                                            answer **= equation[equation.index(i) + 1]
                                            equation.remove(equation[equation.index(i) + 1])
                                        elif isinstance(i, (int, float)):
                                            answer += i
                                    message = str(answer)
                                    if message.endswith('.0'):
                                        message = str(int(float(message)))
                                    break
                                    """
                                    sc.api_call(
                                        "chat.postMessage",
                                        channel=read[0][u'channel'],
                                        text=message
                                    )
                                elif i == 'create location':
                                    pass

                                # commands[i](read[0], i)

                except KeyError as e:
                    print e
    except Exception as e:
        print e
        sc.api_call(
            "chat.postMessage",
            channel='C3UJDJ8F6',
            text="I've crashed, help! : " + str(e)
        )
else:
    print "Connection Failed, invalid token?"
