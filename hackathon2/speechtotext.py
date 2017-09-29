# bing speech API
import speech_recognition as sr
from pprint import pprint


# obtain audio from the microphone
def func():
    r = sr.Recognizer()
    use_id = int(input("want to use microphone(1) or file(2)?\n"))
    if use_id == 1:
        with sr.Microphone() as source:
            print("Say something!")
            audio = r.listen(source)
    elif use_id == 2:
        audio_file_str = input("enter the file path:")
        with sr.AudioFile(audio_file_str) as source:
            audio = r.record(source)
    else:
        func()
    BING_KEY = "396fadeb9fff406d8ae908ec83e850e1"
# Microsoft Bing Voice Recognition API keys 32-character lowercase hexadecimal strings
    info_id = int(input("want to show all info?\n1.yes  2.no\n"))
    lang_id = int(input("choose a language\n1.english 2.chinese\n"))
    if lang_id == 1:
        lang = "en-US"
    elif lang_id == 2:
        lang = "zh-CN"
    else:
        func()
    try:
        if info_id == 1 or info_id == 2:
            return r.recognize_bing(audio, key=BING_KEY, language=lang)
        else:
            func()
    except sr.UnknownValueError:
        print("Microsoft Bing Voice Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Microsoft Bing Voice Recognition service; {0}".format(e))


module_name = "speech-to-text"
if __name__ == module_name:
    func()
