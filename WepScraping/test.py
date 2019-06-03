from WepScraping.naver import Naver
from bs4 import BeautifulSoup
import time

if __name__ == "__main__" :
    naver = Naver('your_id', 'your_pass')   #앞에는 id, 뒤에는 비밀번호
    try:
        naver.clipboard_login(naver.ID, naver.PW)
    finally:
        time.sleep(2)
        naver.driver.get('https://order.pay.naver.com/home')

    html = naver.driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    notices = soup.select('p.name')         #p태그의 name클래스를 찾는다

    for n in notices:
         print(n.text.strip())
