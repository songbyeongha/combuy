# -*- coding: utf-8 -*-
import json
import os
import re
import urllib.request

from recommend import *
from bs4 import BeautifulSoup
from slackclient import SlackClient
from flask import Flask, request, make_response, render_template
from selenium import webdriver

app = Flask(__name__)

slack_token = ""
slack_client_id = "502761537154.508541799559"
slack_client_secret = "2885563b20690fc058f0870749163a29"
slack_verification = "x26eqvj9yBxb6yLThkr90cgp"
sc = SlackClient(slack_token)



# 크롤링 함수 구현하기
def _crawl_naver_keywords(text):
    # 사용자 호출 후 실행되어야 될 것
    # 여기에 함수를 구현해봅시다.
    text = re.sub(r'<@\S+>', '', text)
    if "검색 :" in text:
        return "검색 결과를 알려드립니다."
    elif "추천" in text:
        if "cpu" in text:
            url = "https://search.shopping.naver.com/search/all.nhn?query=cpu&cat_id=&frm=NVSHATC"
            return send_message(url, "cpu 추천")

        elif "보드" in text:
            url = "https://search.shopping.naver.com/search/all.nhn?query=%EB%A9%94%EC%9D%B8%EB%B3%B4%EB%93%9C&cat_id=&frm=NVSHATC"
            return send_message(url, "메인보드 추천")

        elif "그래픽" in text:
            url = "https://search.shopping.naver.com/search/all.nhn?query=%EA%B7%B8%EB%9E%98%ED%94%BD%EC%B9%B4%EB%93%9C&cat_id=&frm=NVSHATC"
            return send_message(url, "그래픽카드 추천")

        elif "ram" in text:
            url = "https://search.shopping.naver.com/search/all.nhn?query=ram&cat_id=&frm=NVSHATC"
            return send_message(url, "ram 추천")
        elif "ssd" in text:
            url = "https://search.shopping.naver.com/search/all.nhn?query=ssd"
            return send_message(url, "ssd 추천")

    elif "리뷰" in text:
        if "많은" in text:
            if "cpu" in text:
                url = "https://search.shopping.naver.com/search/all.nhn?origQuery=cpu&pagingIndex=1&pagingSize=40&viewType=list&sort=review&frm=NVSHATC&query=cpu"
                return send_message(url, "cpu 리뷰 많은순")

            elif "보드" in text:
                url = "https://search.shopping.naver.com/search/all.nhn?origQuery=%EB%A9%94%EC%9D%B8%EB%B3%B4%EB%93%9C&pagingIndex=1&pagingSize=40&viewType=list&sort=review&frm=NVSHATC&query=%EB%A9%94%EC%9D%B8%EB%B3%B4%EB%93%9C"
                return send_message(url, "메인보드 리뷰 많은순")

            elif "그래픽" in text:
                url = "https://search.shopping.naver.com/search/all.nhn?origQuery=%EA%B7%B8%EB%9E%98%ED%94%BD%EC%B9%B4%EB%93%9C&pagingIndex=1&pagingSize=40&viewType=list&sort=review&frm=NVSHATC&query=%EA%B7%B8%EB%9E%98%ED%94%BD%EC%B9%B4%EB%93%9C"
                return send_message(url, "그래픽카드 리뷰 많은순")

            elif "ram" in text:
                url = "https://search.shopping.naver.com/search/all.nhn?origQuery=ram&pagingIndex=1&pagingSize=40&viewType=list&sort=review&frm=NVSHTTL&query=ram"
                return send_message(url, "ram 리뷰 많은순")

            elif "ssd" in text:
                url = "https://search.shopping.naver.com/search/all.nhn?query=ssd"
                return send_message(url, "ssd 리뷰 많은순")
    elif "가격" in text:
        if "낮은" in text:
            if "cpu" in text:
                url = "https://search.shopping.naver.com/search/all.nhn?origQuery=cpu&pagingIndex=1&pagingSize=40&viewType=list&sort=price_asc&frm=NVSHATC&query=cpu"
                return send_message(url, "cpu 낮은 가격순")

            elif "보드" in text:
                url = "https://search.shopping.naver.com/search/all.nhn?origQuery=%EB%A9%94%EC%9D%B8%EB%B3%B4%EB%93%9C&pagingIndex=1&pagingSize=40&viewType=list&sort=price_asc&frm=NVSHATC&query=%EB%A9%94%EC%9D%B8%EB%B3%B4%EB%93%9C"
                return send_message(url, "메인보드 낮은 가격순")

            elif "그래픽" in text:
                url = "https://search.shopping.naver.com/search/all.nhn?origQuery=%EA%B7%B8%EB%9E%98%ED%94%BD%EC%B9%B4%EB%93%9C&pagingIndex=1&pagingSize=40&viewType=list&sort=price_asc&frm=NVSHATC&query=%EA%B7%B8%EB%9E%98%ED%94%BD%EC%B9%B4%EB%93%9CC"
                return send_message(url, "그래픽카드 낮은 가격순")

            elif "ram" in text:
                url = "https://search.shopping.naver.com/search/all.nhn?origQuery=ram&pagingIndex=1&pagingSize=40&viewType=list&sort=price_asc&frm=NVSHATC&query=ram"
                return send_message(url, "ram 낮은 가격순")

            elif "ssd" in text:
                url = "https://search.shopping.naver.com/search/all.nhn?origQuery=ssd&pagingIndex=1&pagingSize=40&viewType=list&sort=price_asc&frm=NVSHTTL&query=ssd"
                return send_message(url, "ssd 낮은 가격순")

        elif "높은" in text:
            if "cpu" in text:
                url = "https://search.shopping.naver.com/search/all.nhn?origQuery=cpu&pagingIndex=1&pagingSize=40&viewType=list&sort=price_dsc&frm=NVSHATC&query=cpu"
                return send_message(url, "cpu 높은 가격순")

            elif "보드" in text:
                url = "https://search.shopping.naver.com/search/all.nhn?origQuery=%EB%A9%94%EC%9D%B8%EB%B3%B4%EB%93%9C&pagingIndex=1&pagingSize=40&viewType=list&sort=price_dsc&frm=NVSHATC&query=%EB%A9%94%EC%9D%B8%EB%B3%B4%EB%93%9CC"
                return send_message(url, "메인보드 높은 가격")

            elif "그래픽" in text:
                url = "https://search.shopping.naver.com/search/all.nhn?origQuery=%EA%B7%B8%EB%9E%98%ED%94%BD%EC%B9%B4%EB%93%9C&pagingIndex=1&pagingSize=40&viewType=list&sort=price_dsc&frm=NVSHATC&query=%EA%B7%B8%EB%9E%98%ED%94%BD%EC%B9%B4%EB%93%9C"
                return send_message(url, "그래픽카드 높은 가격")

            elif "ram" in text:
                url = "https://search.shopping.naver.com/search/all.nhn?origQuery=ram&pagingIndex=1&pagingSize=40&viewType=list&sort=price_dsc&frm=NVSHATC&query=ram"
                return send_message(url, "ram 높은 가격")

            elif "ssd" in text:
                url = "https://search.shopping.naver.com/search/all.nhn?origQuery=ssd&pagingIndex=1&pagingSize=40&viewType=list&sort=price_dsc&frm=NVSHTTL&query=ssd"
                return send_message(url, "ssd 높은 가격")
    elif "안녕" in text:
        return u"안녕하세요!! 컴퓨터 부품을 알려드립니다.^^"
    else:
        return u"명령어가 없어요!!"

def _search_event(text):
    if "검색 :" in text:
        text = re.sub(r'<@\S+>', '', text)
        return search_def(text)

# 이벤트 핸들하는 함수
def _event_handler(event_type, slack_event):
    print(slack_event["event"])

    if event_type == "app_mention":
        channel = slack_event["event"]["channel"]
        text = slack_event["event"]["text"]

        searchs =  _search_event(text)
        keywords = _crawl_naver_keywords(text)
        sc.api_call(
            "chat.postMessage",
            channel=channel,
            text=keywords,
            attachments=json.dumps([searchs])
        )

        return make_response("App mention message has been sent", 200, )

    # ============= Event Type Not Found! ============= #
    # If the event_type does not have a handler
    message = "You have not added an event handler for the %s" % event_type
    # Return a helpful error message
    return make_response(message, 200, {"X-Slack-No-Retry": 1})


@app.route("/listening", methods=["GET", "POST"])
def hears():
    slack_event = json.loads(request.data)

    if "challenge" in slack_event:
        return make_response(slack_event["challenge"], 200, {"content_type":
                                                                 "application/json"
                                                             })

    if slack_verification != slack_event.get("token"):
        message = "Invalid Slack verification token: %s" % (slack_event["token"])
        make_response(message, 403, {"X-Slack-No-Retry": 1})

    if "event" in slack_event:
        event_type = slack_event["event"]["type"]
        return _event_handler(event_type, slack_event)

    # If our bot hears things that are not events we've subscribed to,
    # send a quirky but helpful error response
    return make_response("[NO EVENT IN SLACK REQUEST] These are not the droids\
                         you're looking for.", 404, {"X-Slack-No-Retry": 1})


@app.route("/", methods=["GET"])
def index():
    return "<h1>Server is ready.</h1>"


if __name__ == '__main__':
    app.run('127.0.0.1', port=1234)
