# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import psycopg2
import logging

INSERT_SQL = "INSERT INTO news_nba (title, date_time, author, content, image_source, video_source) VALUES (%s, %s, %s, %s, %s, %s)"
has_crawled_article = dict()

class CrawlerPipeline(object):
    def __init__(self, db_url):
        self.db_url = db_url

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            db_url = crawler.settings.get('DATABASE_URL')
        )
        
    def process_item(self, item, spider):
        if item.get('article_url') in has_crawled_article:
            logging.INFO('{} has crawled'.format(item.get('article_url')))
            has_crawled_article[item.get('article_url')] += 1
            if has_crawled_article[item.get('article_url')] >= 20:
                del has_crawled_article[item.get('article_url')] 
        else:
            try:
                conn = psycopg2.connect(self.db_url)
                cur = conn.cursor()
                cur.execute(INSERT_SQL, (item.get('title'), item.get('date_time'), item.get('author'), item.get('content'), item.get('image_source'), item.get('video_source')))
                conn.commit()
                cur.close()
                conn.close()
                has_crawled_article[item.get('article_url')] = 1
            except Exception as e:
                logging.error(str(e))
        return item

