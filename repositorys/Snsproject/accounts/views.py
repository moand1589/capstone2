from selenium.common.exceptions import NoSuchElementException

import pandas as pd
import re
import time
from selenium import webdriver
from bs4 import BeautifulSoup
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth, messages
from django.urls import reverse
from django.db import IntegrityError
from main.models import Posting


def index(request):
    return redirect("accounts:login")


def signup(request):
    if request.method == "POST":
        if User.objects.filter(username=request.POST["username"]).exists():
            messages.info(request, "이미 존재하는 아이디입니다.")
            return render(request, "accounts/signup.html")

        if request.POST["password1"] == request.POST["password2"]:
            user = User.objects.create_user(
                request.POST["username"], password=request.POST["password1"]
            )
            return redirect("accounts:login")
    else:
        return render(request, "accounts/signup.html")


def login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            userr = User.objects.get(username=username)
            request.session["user1"] = userr.id
            crawling(request, username, password)
            return redirect("main:analysis")
        else:
            messages.info(request, "아이디 또는 비밀번호를 확인해주세요")
            return redirect("account:login")
    else:
        return render(request, "accounts/login.html")


def insta_searching(word):
    url = "https://www.instagram.com/" + word
    return url


# 로그인되면 크롤링함수 실행
def crawling(request, username, password):
    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    driver = webdriver.Chrome(options=options)

    driver.get("https://www.instagram.com/accounts/login/")

    time.sleep(1)

    email = username

    input_id = driver.find_elements_by_css_selector(
        "input._2hvTZ.pexuQ.zyHYP")[0]
    input_id.clear()

    input_id.send_keys(email)
    password = password
    input_pw = driver.find_elements_by_css_selector(
        "input._2hvTZ.pexuQ.zyHYP")[1]
    input_pw.clear()
    input_pw.send_keys(password)
    input_pw.submit()
    time.sleep(3)

    word = email
    url = insta_searching(word)
    driver.get(url)
    time.sleep(3)

    insta_dict = {"date": [], "text": []}

    first_post = driver.find_element_by_class_name("eLAPa")

    first_post.click()
    num = 0
    seq = 0
    start = time.time()
    # # 크롤링할 게시물의 개수를 정함
    while num <= 20:
        try:
            if driver.find_element_by_css_selector(
                "a._65Bje.coreSpriteRightPaginationArrow"
            ):
                insta_dict = Posting()
                time_raw = driver.find_element_by_css_selector(
                    "time.FH9sR.Nzb55")
                time_info = pd.to_datetime(
                    time_raw.get_attribute("datetime")
                ).normalize()
                insta_dict.insta = request.user
                insta_dict.pub_date = time_info
                raw_info = driver.find_element_by_css_selector(
                    "div.C4VMK").text.split()
                text = []

                for i in range(len(raw_info)):
                    if i == 0:
                        pass
                    else:
                        if "#" in raw_info[i]:
                            pass
                        else:
                            text.append(raw_info[i])
                clean_text = " ".join(text)
                insta_dict.post = clean_text
                insta_dict.save()
                seq += 1
                if seq == 100:
                    break
                driver.find_element_by_css_selector(
                    "a._65Bje.coreSpriteRightPaginationArrow"
                ).click()
                time.sleep(3)
            else:
                break

        except NoSuchElementException:
            driver.find_element_by_css_selector(
                "a._65Bje.coreSpriteRightPaginationArrow"
            ).click()
            time.sleep(3)
        num += 1
    driver.quit()  # 브라우저 닫기


def logout(request):
    if request.session["user1"]:
        del request.session["user1"]
    auth.logout(request)
    return redirect("accounts:login")


def delete(request):
    if request.user.is_authenticated:
        request.user.delete()
        auth.logout(request)
    return redirect('accounts:login')
