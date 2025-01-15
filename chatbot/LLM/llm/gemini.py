import os
from getpass import getpass
import pandas as pd
import google.generativeai as genai

# cnn 기사 데이터 수집
# 백엔드에서 기사를 받아 learnChat 클래스에 넘겨야 함
def fetchArticle():
    pass

# 같은 기사와 summary로 작업을 하기 위해 class로 묶음
# Summary(), vocab() 순으로 작업 진행
# article을 넘겨받는 부분의 구현 필요
class learnChat():
    model = genai.GenerativeModel("gemini-1.5-flash")
    chat = model.start_chat(history=[{'role':'user', 'parts':article.content}])
    # fetch Gemini API Key
    os.environ["GOOGLE_API_KEY"] = getpass("Gemini API Key:")

# create summary
    def Summary():
        summary=[]
        summary[0] = chat.send_message("입력된 내용을 영어로 요약해서 출력해줘. 요약문은 100자 이내여야 해.").text
        while len(summary)>400:
            summary[0] = chat.send_message("너무 길어, 더 줄여줘.").text
        summary[1] = chat.send_message("요약본을 한국어로 번역해줘").text
        return summary

# create vocab
    def vocab():
        prompt="""
        영문 요약본에서 적당한 난이도의 단어 3개만 찾아줘, 단어 옆에  한국어 뜻을 붙여줘. 단어와 뜻만 출력해. 
        예시: 
        collates 모으다
        Crucial 중요한
        Attributed 귀속된
        """
        response = chat.send_message(prompt)
        response=response.text.split('\n')
        response.pop()
        vocab={}
        for i in range(len(response)):
            v,m=response[i].split(maxsplit=1)
            vocab[v]=m
        return vocab