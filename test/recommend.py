# -*- coding: utf-8 -*-
import json
import os
import re
import urllib.request
import time

from selenium import webdriver
from bs4 import BeautifulSoup
from slackclient import SlackClient
from flask import Flask, request, make_response, render_template


def send_message(url, title, goods_number = 0):
    source = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(source, "html.parser")
    keywords = []
    titles = []
    title_url = []
    img_url = []
    for tit in soup.find_all("div", class_="info"):
        titles.append(tit.find("a", class_="tit"))
        title_url.append(tit.find("a", class_="tit")["href"])
    prices = soup.find_all("span", class_="num _price_reload")
    # 추가 details
    details = soup.find_all("span", class_="detail")
    # 추가 img_url
    # for img in soup.find_all("div", class_="img_area"):
    #     img_url.append(img.find("img")["src"])

    keywords.append(title + " Top 5\n\n")

    for i in range(5):
        keywords.append(str(i + 1) + "위 -> \n 상품명 : <"+str(title_url[i])+"|" + titles[i].get_text().strip() + ">\n 가격 : " + prices[i].get_text().strip() + "원\n 상품 상세 : \n     " + details[i].get_text().strip().replace("|", ",\n     ").replace(":", "->") + "\n    ")
        keywords.append(str(img_url[i]))

    return u'\n'.join(keywords)

# def send_img_url(url,goods_number = 0):
#     source = urllib.request.urlopen(url).read()
#     soup = BeautifulSoup(source, "html.parser")
#     for img in soup.find_all("div", class_="img_area"):
#         img_url.append(img.find("img")["src"])
#         msg = {}
#         msg["image_url"] = str(img_url[i])
#     return msg


def search_def(key, goods_num=0):
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
    titles = []
    title_url = []
    img_url = []
    for tit in soup.find_all("div", class_="info"):
        titles.append(tit.find("a", class_="tit"))
        # title_url.append(tit.find("a", class_="tit")["href"])
        title_url.append(tit.find("a")["href"])
    prices = soup.find_all("span", class_="num _price_reload")
    # time.sleep(2)
    for img in soup.find_all("div", class_="img_area"):
        img_url.append(img.find("img")["src"])
    # 추가 details
    details = soup.find_all("span", class_="detail")
    keywords = "검색 결과 -> \n상품명 : <" + str(title_url[goods_num]) + "|" + titles[goods_num].get_text().strip() + ">\n 가격 : " + prices[goods_num].get_text().strip() + "원\n 상품 상세 : \n" + details[goods_num].get_text().replace("|", ",").replace(":", "->").strip() + "\n"
    driver.close()
    msg = {}
    msg["text"] = keywords
    msg["image_url"] = img_url[goods_num]
    return msg