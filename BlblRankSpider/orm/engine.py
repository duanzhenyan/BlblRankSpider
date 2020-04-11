# -*- coding:utf-8 -*-


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from BlblRankSpider.settings import FINANCIAL_MYSQL_DB_URL

coin_financial_db_engine = create_engine(FINANCIAL_MYSQL_DB_URL)

FINANCIAL_DBSession = sessionmaker(bind=coin_financial_db_engine)
