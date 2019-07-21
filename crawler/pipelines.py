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
    def __init__(self, db_host, db_port, db_name, db_user, db_pwd):
        self.db_host = db_host
        self.db_port = db_port
        self.db_name = db_name
        self.db_user = db_user
        self.db_pwd = db_pwd

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            db_host = crawler.settings.get('DB_HOST'),
            db_port = crawler.settings.get('DB_PORT'),
            db_name = crawler.settings.get('DB_NAME'),
            db_user = crawler.settings.get('DB_USER'),
            db_pwd = crawler.settings.get('DB_PWD')
        )
        
    def process_item(self, item, spider):
        if item.get('article_url') in has_crawled_article:
            logging.INFO('{} has crawled'.format(item.get('article_url')))
            has_crawled_article[item.get('article_url')] += 1
            if has_crawled_article[item.get('article_url')] >= 20:
                del has_crawled_article[item.get('article_url')] 
        else:
            try:
                conn = psycopg2.connect(host=self.db_host, port=self.db_port, database=self.db_name, user=self.db_user, password=self.db_pwd)
                cur = conn.cursor()
                cur.execute(INSERT_SQL, (item.get('title'), item.get('date_time'), item.get('author'), item.get('content'), item.get('image_source'), item.get('video_source')))
                conn.commit()
                cur.close()
                conn.close()
                has_crawled_article[item.get('article_url')] = 1
            except Exception as e:
                logging.error(str(e))
        return item

