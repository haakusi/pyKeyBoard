# -*- coding: utf-8 -*-
import fileinput
import keyboard
import ctypes

import win32api
import win32con
from hangul_utils import join_jamos
import datetime
import re
import json
from collections import OrderedDict
from ctypes import wintypes
from transformers import PreTrainedTokenizerFast, BartForConditionalGeneration

wintypes.ULONG_PTR = wintypes.WPARAM

d_all = []
korBuffer = []
VK_HANGUEL = 0x15

cons = {'r': 'ㄱ', 'R': 'ㄲ', 's': 'ㄴ', 'e': 'ㄷ', 'E': 'ㄸ', 'f': 'ㄹ', 'a': 'ㅁ', 'q': 'ㅂ', 'Q': 'ㅃ', 't': 'ㅅ', 'T': 'ㅆ',
        'd': 'ㅇ', 'w': 'ㅈ', 'W': 'ㅉ', 'c': 'ㅊ', 'z': 'ㅋ', 'x': 'ㅌ', 'v': 'ㅍ', 'g': 'ㅎ'}

vowels = {'k': 'ㅏ', 'o': 'ㅐ', 'i': 'ㅑ', 'O': 'ㅒ', 'j': 'ㅓ', 'p': 'ㅔ', 'u': 'ㅕ', 'P': 'ㅖ', 'h': 'ㅗ', 'hk': 'ㅘ',
          'ho': 'ㅙ', 'hl': 'ㅚ',
          'y': 'ㅛ', 'n': 'ㅜ', 'nj': 'ㅝ', 'np': 'ㅞ', 'nl': 'ㅟ', 'b': 'ㅠ', 'm': 'ㅡ', 'ml': 'ㅢ', 'l': 'ㅣ'}

cons_double = {'rt': 'ㄳ', 'sw': 'ㄵ', 'sg': 'ㄶ', 'fr': 'ㄺ', 'fa': 'ㄻ', 'fq': 'ㄼ', 'ft': 'ㄽ', 'fx': 'ㄾ', 'fv': 'ㄿ',
               'fg': 'ㅀ', 'qt': 'ㅄ'}


def get_hanguel_state():
    lib = ctypes.windll.LoadLibrary('user32.dll')
    imm = ctypes.windll.LoadLibrary('imm32.dll')
    hWnd1 = lib.GetForegroundWindow()  # to get activated window handle
    hWnd2 = imm.ImmGetDefaultIMEWnd(hWnd1)
    status = win32api.SendMessage(hWnd2, win32con.WM_IME_CONTROL, 0x5, 0)
    lib.GetKeyState(VK_HANGUEL)
    if (status != 0):
        return 1
    else:
        return 0


def eng2kor(text):
    result = ''  # result eng to kor

    # 1. check to cons or vowels
    vc = ''
    for t in text:
        if t in cons:
            vc += 'c'
        elif t in vowels:
            vc += 'v'
        else:
            vc += '!'
    # cvv → fVV / cv → fv / cc → dd
    vc = vc.replace('cvv', 'fVV').replace('cv', 'fv').replace('cc', 'dd')

    # 2. cons / vowels / search in two cons
    i = 0
    while i < len(text):
        v = vc[i]
        t = text[i]
        j = 1
        try:  # korean
            if v == 'f' or v == 'c':  # f & c = cons
                result += cons[t]
            elif v == 'V':  # double vowels
                result += vowels[text[i:i + 2]]
                j += 1
            elif v == 'v':  # vowels
                result += vowels[t]
            elif v == 'd':  # double cons
                result += cons_double[text[i:i + 2]]
                j += 1
            else:
                result += t
        except:  # not korean
            if v in cons:
                result += cons[t]
            elif v in vowels:
                result += vowels[t]
            else:
                result += t
        i += j
    return join_jamos(result)


def txt2json_parsing(tmpName):
    '''
        1. open file -> readlines if [-1] == ']' -> [liens.(' ', '').regex('-,|'),-2] -> key
        2. next lines until [-1] == ']', append value

        obj json
        [ {"key":"val"}, {"key":"val"}, ... {"key":"val"} ]

        adjust bart.. summary()
        berfore that.. need to simulation at web test.. with json format.. value..
    '''
    file_data = OrderedDict()

    with open(tmpName, 'r', encoding='utf-8') as f1:
        lines = f1.readlines()
        tmpKeyLine = ""
        for line in lines:
            if line.find('\n'):
                line = line.rstrip('\n')
            if (line[-1] == ']' and line[0] != '['):
                line = line.replace("]", "")
                if (line.find(" - ") or line.find(" | ")):
                    line = re.findall('(?<=[ ][-|][ ]).+', line)
                line = line[0].replace(" ", "")  # key
                tmpKeyLine = line
                print('>>>### tmpKeyLine : {}'.format(tmpKeyLine))
            elif (line[0] == '[' and line[-1] == ']'):
                line = line.replace("[", "")
                line = line.replace("]", "")
                line = line.replace(" ", "")
                tmpKeyLine = line
            elif (line == "" or line == " " or line == "\n"):
                continue
            else:
                if (tmpKeyLine != ''):
                    if (tmpKeyLine in file_data.items()):
                        file_data(file_data[tmpKeyLine]).append(line)
                    else:
                        file_data[tmpKeyLine] = line
                        tmpKeyLine = ""

        with open('test.json', 'w', encoding='UTF-8') as f:
            json.dump(file_data, f, indent=4, ensure_ascii=False)

        print(file_data)
    return 'parsing complete'


def get_present_process():
    # GetForegroundWindow - to get the handle of the focused window
    # GetWindowThreadProcessId - to get the ID of the process that created by window
    lib = ctypes.windll.LoadLibrary('user32.dll')
    handle = lib.GetForegroundWindow()  # to get activated window handle
    buffer = ctypes.create_unicode_buffer(255)
    lib.GetWindowTextW(handle, buffer, ctypes.sizeof(buffer))  # saved buffer about title
    return buffer.value


def kor_buffer_chk_write():
    if (len(korBuffer) != 0):
        tmpStr = ''.join(korBuffer)
        file.write(eng2kor(tmpStr))
        korBuffer.clear()
    return


def print_event_json(event):
    global chkHanguel
    chkHanguel = get_hanguel_state()
    if (d_all.count(get_present_process())):
        if (event.event_type == "up"):
            if (len(event.name) < 2):  # not shift, alt.. f1.. etc..
                if (chkHanguel == 0):  # eng
                    file.write(event.name)
                elif (chkHanguel == 1):  # kor
                    korBuffer.append(event.name)
            else:
                if (event.name == "space" or event.name == "enter"):
                    file.write(" ")
                    kor_buffer_chk_write()
                elif(event.name == "backspace"):
                    if (len(korBuffer) != 0):    # kor
                        korBuffer.pop()
                        pass
                    else:       # eng
                        file.flush()
                        tmpFiles = open(tmpName, 'r', encoding='utf-8')
                        file_content = tmpFiles.read()[:-1]
                        tmpFiles.close()
                        file.seek(0)
                        file.truncate()
                        file.write(file_content)
                elif (event.name == "pause"):
                    # txt2json_parsing(tmpName)    # tmp
                    print("not yet adjust.. thinking constructure")
        elif (event.name == "f1"):
            kor_buffer_chk_write()
            file.close()
            print("close writing file.")
            exit()
        elif (event.name == "f2"):
            print("debug - start f2")
            tokenizer = PreTrainedTokenizerFast.from_pretrained("ainize/kobart-news")
            model = BartForConditionalGeneration.from_pretrained("ainize/kobart-news")
            print("debug - after open model")
            input_text = "아! ㅎㅎ 주소값으로 저도 넣고 싶은데 안되서 찾아보니가 그거 당연히 안되는건데? 라고 외국친구가 달아놓은게 있어서 더 찾다가 이게 뭔가 싶어서.. 하나로 퉁치고 리턴에 리턴을 주소로하는거여쭤봤어요!! 우선 크게! 중요한 부분은 아니여서 하다가 ㅋㅋ.. 결국 저도 값 그냥 넣어서 사용 했는데.. ㅋㅋㅋ.. 쥬륵.. 감사합니다! 그렇게 시간을 엄청 소비한..  맞습니다.!! 다시 저도 다른것들 이슈 처리하다가 주임님이 lib 처리해서 주시면 내재화 다시 시작하겠습니다. 옙 감사합니다!"
            input_ids = tokenizer.encode(input_text, return_tensors="pt")
            summary_text_ids = model.generate(
                input_ids=input_ids,
                bos_token_id=model.config.bos_token_id,
                eos_token_id=model.config.eos_token_id,
                length_penalty=2.0,
                max_length=120,
                min_length=20,
                num_beams=4,
            )
            print(tokenizer.decode(summary_text_ids[0], skip_special_tokens=True))
    else:
        kor_buffer_chk_write()
        file.write("\n\n")
        file.write("[")
        for i in get_present_process():
            file.write(i)
        file.write("]")
        file.write("\n")
        d_all.append(get_present_process())

    if event.name:  # here are change source code encoding = 'utf-8'
        print('{{"process":"{}", "event_type": "{}", "name": "{}", "scan_code": {}, "time": {}}}'.format(get_present_process(), event.event_type, event.name,event.scan_code, event.time))
    else:
        print('{{"process":"{}", event_type": "{}", "scan_code": {}, "time": {}}}'.format(get_present_process(), event.event_type, event.scan_code, event.time))


if __name__ == '__main__':
    dt_now = datetime.datetime.now()
    tmpName = 'testKeyBoard_%s%s%s.txt' % (dt_now.year, dt_now.month, dt_now.day)
    file = open(tmpName, 'a+', encoding='utf-8')
#    txt2json_parsing('samaple.txt')
    keyboard.hook(print_event_json)
    parse_event_json = lambda line: keyboard.KeyboardEvent(**json.loads(line))
    keyboard.play(parse_event_json(line) for line in fileinput.input())
