import google.generativeai as genai
from django.conf import settings
import time

genai.configure(api_key=settings.GEMINI_API_KEY)

class learnChat:
    def __init__(self, article_content):
        self.model = genai.GenerativeModel("gemini-1.5-flash")
        self.chat = self.model.start_chat(history=[{'role': 'user', 'parts': article_content}])

    def summarize(self):
        summary_english = self.chat.send_message("입력된 내용을 핵심만 80자 이내로 영어로 요약해줘.").text
        return summary_english


    def translate(self, text):
        time.sleep(5)
        translated_text = self.chat.send_message(f"다음 영어 텍스트를 한국어로 번역해줘: {text}").text
        return translated_text
    

    def vocab(self):
        time.sleep(5)
        prompt = """
        핵심 내용에서 적당한 난이도의 단어 3개만 찾아줘, 단어 옆에 한국어 뜻을 붙여줘.
        단어와 뜻만 출력해.
        """
        response = self.chat.send_message(prompt)
        vocab = {}
        for line in response.text.split('\n'):
            if line.strip():
                word, meaning = line.split(maxsplit=1)
                vocab[word] = meaning
        return vocab
