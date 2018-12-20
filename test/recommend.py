# -*- coding: utf-8 -*-
import json
import os
import re
import urllib.request

from selenium import webdriver
from bs4 import BeautifulSoup
from slackclient import SlackClient
from flask import Flask, request, make_response, render_template


def send_message(url, title):
    source = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(source, "html.parser")
    keywords = []
    titles = []
    title_url = []
    for tit in soup.find_all("div", class_="info"):
        titles.append(tit.find("a", class_="tit"))
        title_url.append(tit.find("a", class_="tit")["href"])
    prices = soup.find_all("span", class_="num _price_reload")
    # 추가 details
    details = soup.find_all("span", class_="detail")
    keywords.append(title + " Top 5\n\n")

    for i in range(5):
        keywords.append(str(i + 1) + "위 -> \n 상품명 : <"+str(title_url[i])+"|" + titles[i].get_text().strip() + ">\n 가격 : " + prices[i].get_text().strip() + "원\n 상품 상세 : \n     " + details[i].get_text().strip().replace("|", ",\n     ").replace(":", "->") + "\n    ")

    return u'\n'.join(keywords)

def search_def(key):
    driver = webdriver.Chrome(r"C:\Users\student\Desktop\chromedriver_win32\chromedriver.exe")
    # 사용자 호출 전에 실행되어야 될 것
    driver.get("https://search.shopping.naver.com/search/category.nhn?cat_id=50000097")
    keyword = key.split(":")
    searchText = driver.find_element_by_css_selector("input.co_srh_input._input")
    searchText.send_keys(keyword[1])
    searchButton = driver.find_element_by_css_selector("a.co_srh_btn._search")
    searchButton.click()
    source = driver.page_source
    soup = BeautifulSoup(source, "html.parser")

    keywords = []
    titles = []
    title_url = []
    img_url = []
    for tit in soup.find_all("div", class_="info"):
        titles.append(tit.find("a", class_="tit"))
        title_url.append(tit.find("a", class_="tit")["href"])
    prices = soup.find_all("span", class_="num _price_reload")
    for img in soup.find_all("div", class_="img_area"):
        img_url.append(img.find("img", class_="_productLazyImg")["src"])
    # 추가 details
    details = soup.find_all("span", class_="detail")
    keywords.append("검색 결과 -> ")
    keywords.append("상품명 : <" + str(title_url[0]) + "|" + titles[0].get_text().strip() + ">\n 가격 : " + prices[0].get_text().strip() + "원\n 상품 상세 : \n     " + details[0].get_text().strip().replace("|", ",\n     ").replace(":", "->") + "\n    ")

    msg = {}
    msg["text"] = keywords
    msg["image_url"] = img_url[0]
    return msg