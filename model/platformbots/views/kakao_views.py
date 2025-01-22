from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from ..services.kakao_service import KakaoMessageService
import logging




logger = logging.getLogger(__name__)

'''
디버깅용 클래스
class KakaoWebhookView(APIView):
    """
    카카오톡 챗봇 웹훅을 처리하는 뷰
    카카오톡 스킬 서버로 등록되어 사용자 메시지를 처리하고 응답을 반환
    """
    def post(self, request):
        logger.debug(f"Received request: {request.data}")
        # 카카오톡 응답 기본 템플릿
        response = {
            "version": "2.0",
            "template": {
                "outputs": [
                    {
                        "simpleText": {
                            "text": "기본 응답입니다."
                        }
                    }
                ]
            }
        }

        try:
            # 디버깅을 위한 요청 데이터 출력
            print("Received request data:", request.data)
            req = request.data
            utterance = req.get('userRequest', {}).get('utterance', '')

            if utterance == "안녕":
                response['template']['outputs'][0]['simpleText']['text'] = "안녕하세요! 반갑습니다."
                
        except Exception as e:
            print(f"Error: {str(e)}")
            response['template']['outputs'][0]['simpleText']['text'] = "오류가 발생했습니다."
        logger.debug(f"Sending response: {response}")
        return Response(response)
'''



class KakaoWebhookView(APIView):
    def post(self, request):
        # 카카오톡 응답 기본 템플릿
        response = {
            "version": "2.0",
            "template": {
                "outputs": []
            }
        }

        try:
            # 카카오톡으로부터 받은 요청 데이터 파싱
            req = request.data
            # userRequest.utterance: 사용자가 입력한 메시지
            utterance = req.get('userRequest', {}).get('utterance', '')
            
            # 카테고리 입력 시 해당 뉴스 제공
            article = KakaoMessageService.get_latest_news(utterance)
            if article:
                # 뉴스 데이터를 카카오톡 메시지 형식으로 변환
                message = KakaoMessageService.format_news_message(article)
                response['template']['outputs'].append({
                    "simpleText": {
                        "text": message
                    }
                })

            else:
                # 해당 카테고리 뉴스가 없는 경우
                response['template']['outputs'].append({
                    "simpleText": {
                        "text": "해당 카테고리의 뉴스를 찾을 수 없습니다."
                    }
                })

        except Exception as e:
            # 에러 로깅 및 사용자에게 에러 메시지 전송
            print(f"Error processing request: {str(e)}")
            response['template']['outputs'].append({
                "simpleText": {
                    "text": "처리 중 오류가 발생했습니다."
                }
            })

        return Response(response)