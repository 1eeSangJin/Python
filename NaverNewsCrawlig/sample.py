from NaverNewsCrawlig.articlecrawler import ArticleCrawler

if __name__ == "__main__":
    Crawler = ArticleCrawler()

    # 정치, 경제, 생활문화, IT과학, 사회, 세계 카테고리 사용 가능
    Crawler.set_category("IT과학", "정치")

    Crawler.set_date_range(2019, 4, 2019, 5)

    Crawler.start()