import matplotlib.pyplot as plt
import tkinter as tk
from selenium import webdriver
from bs4 import BeautifulSoup
from tkinter import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from pandas import DataFrame
from selenium.common.exceptions import NoSuchElementException
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types

client = language.LanguageServiceClient()

main = Tk()
main.title("Comment Analyze")
main.geometry('640x480+100+100')
lbl = Label(main, text="Enter the Movie Title")
lbl.grid(column=0, row=0)
lbl.config(font=("Courier", 20))
lbl.place(x=160, y=170)

txt = Entry(main, width=20)
txt.grid(column=1, row=0)
txt.place(x=260, y=270)
txtLb = Label(main, text="Movie Title")
txtLb.grid(column=0, row=0)
txtLb.config(font=("Courier", 10))
txtLb.place(x=170, y=270)

def clicked():
    driver = webdriver.Chrome("D:\chromedriver")

    search_value = txt.get()
    title_href = []

    movie_result = []
    movie_comment = {}
    movie = {}
    pos = 0
    neg = 0
    neu = 0

    def print_sentiment_scores(sentence):

        document = types.Document(
            content=review_text,
            type=enums.Document.Type.PLAIN_TEXT)
        sentiment = client.analyze_sentiment(document=document).document_sentiment

        if (sentiment.score > 0.0):
            division = "pos"
        elif (sentiment.score < 0.0):
            division = "neg"
        else:
            division = "neu"

        return division

    driver.get("https://movie.naver.com/movie/running/current.nhn")

    driver.implicitly_wait(3)
    search = driver.find_element_by_id("ipt_tx_srch")
    search.click()
    search.send_keys(search_value)                                                  #유저가 검색한 영화를 위 검색툴바에 입력

    driver.implicitly_wait(3)
    driver.find_element_by_xpath('//*[@id="jSearchArea"]/div/button').click()       #영화 검색버튼 클릭

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    movie_temp = soup.select("ul > li > dl > dt > a")

    if not movie_temp:
        print('존재하지 않는 영화입니다')
        sys.exit(1)

    try:
        for movie_href in movie_temp:
            title_href.append(movie_href.attrs['href'])
            http = title_href[0]
        # ----------------------------------------------------------------------------------------------------------------------------------------#

        driver.get("https://movie.naver.com" + http)
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        title_list = soup.find('div', {'class' : 'mv_info'})                                                            #mv_info라는 class를가진 div를 찾는다
        title = title_list.find('a').text                                                                               #title_list를 print해보면 제목이 있는 a태그가 맨 위에 있음. 그래서 그냥 find('a')

        driver.implicitly_wait(3)
        # ----------------------------------------------------------------------------------------------------------------------------------------#
        driver.find_element_by_xpath('//*[@id="content"]/div[1]/div[4]/div[5]/div[2]/div[5]/a/span').click()             #평점 더보기 클릭
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        iframe_source = soup.find('iframe', {'class': 'ifr'})
        iframe_link = iframe_source.attrs['src']
        # ----------------------------------------------------------------------------------------------------------------------------------------#
        driver.get("https://movie.naver.com" + iframe_link)             #driver.get("https://movie.naver.com" + title_href[i])에서 들어갔던 영화 댓글이 iframe형식으로 되어있어 그부분으로 따로 들어감
        driver.implicitly_wait(3)
        driver.find_element_by_xpath('//*[@id="orderCheckbox"]/ul[1]/li[2]/a').click()

        comment_iframe_url = driver.current_url

        for j in range(1, 6):
            print("#############" + str(j) + "페이지#############")
            url = comment_iframe_url + '&page=' + str(j)
            driver.get(url)
            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')

            score_result = soup.find('div', {'class': 'score_result'})  # 댓글들을 가져옴
            comment = score_result.findAll('li')  # li태그들을 찾는다(댓글 텍스트, 별점, 좋아요와 싫어요가 포함되어있음

            for comm in comment:
                review_text = comm.find('p').getText()  # 댓글의 텍스트만 따온다
                # print(review_text)

                feel =  print_sentiment_scores(review_text)

                movie_comment[review_text] = feel
                print(str(movie_comment))

            print()
            movie[title] = movie_comment
            movie_comment = {}
    except NoSuchElementException:
        print("평점이 달려있지 않은 영화입니다")
        sys.exit(1)
    finally:
        print()

    movie_result.append(movie)

    analyze = Tk()
    analyze.title("Movie Analyze")
    analyze.geometry("1300x700")

    result = Label(analyze, text="Result")
    result.grid(column=0, row=0)
    result.config(font=("Courier", 20))
    result.place(x=580, y=30)

    graph = Label(analyze, text="Graph")
    graph.grid(column=0, row=0)
    graph.config(font=("Courier", 20))
    graph.place(x=580, y=300)

    frame = Frame(analyze)
    frame.place(x=70, y=80)

    listNodes = Listbox(frame, width=190, height=13, font=("Helvetica", 8))
    listNodes.pack(side="left", fill="y")

    scrollbar = Scrollbar(frame, orient="vertical")
    scrollbar.config(command=listNodes.yview)
    scrollbar.pack(side="right", fill="y")

    listNodes.config(yscrollcommand=scrollbar.set)

    tmp = "=============================================================================================================================================================================================="
    tmp1 = "Comment List"

    for i in range(len(movie_result[0])):
        listNodes.insert(END, list(movie_result[0].keys())[i])
        listNodes.insert(END, tmp)
        listNodes.insert(END, tmp1)
        listNodes.insert(END, tmp)

        for j in range(len(list(movie_result[0].values())[i])):
            listNodes.insert(END, list(list(movie_result[0].values())[i].keys())[j])
            if(list(list(movie_result[0].values())[i].values())[j] == "pos"):
                pos+=1
            elif(list(list(movie_result[0].values())[i].values())[j] == "neu"):
                neu+=1
            else:
                neg+=1

    tmp2 = Label(analyze)
    tmp2.grid(column=0, row=0)
    tmp2.place(x=360, y=300)

    Data1 = {'Country': ['Pos', 'Neg', 'Neu'],
             'Emotion': [pos, neg, neu]
             }

    df1 = DataFrame(Data1, columns=['Country', 'Emotion'])
    df1 = df1[['Country', 'Emotion']].groupby('Country').sum()

    figure1 = plt.Figure(figsize=(5, 3.5), dpi=100)
    ax1 = figure1.add_subplot(111)
    bar1 = FigureCanvasTkAgg(figure1, tmp2)
    bar1.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH)
    df1.plot(kind='bar', legend=True, ax=ax1, color=tuple(['r', 'b', 'g']))
    ax1.set_title('Response Analysis')

    analyze.mainloop()



btn = Button(main, text="Search", command=clicked)
btn.grid(column=2, row=0)
btn.place(x=300, y=305)

main.mainloop()

