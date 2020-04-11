# -*- coding: utf-8 -*-

import logging

from BlblRankSpider.orm.model.financial_db_model import UserInfo
from BlblRankSpider.orm.engine import FINANCIAL_DBSession

logger = logging.getLogger(__name__)


class UserInfoDao(object):
    def __init__(self):
        self.session = FINANCIAL_DBSession()

    def close(self):
        self.session.close()

    def insert_data(self, data):
        """
        插入数据
        :param data:
        :return:
        """
        try:
            self.session.add(data)
            self.session.commit()
            logger.info('插入成功：' + str(data.id))
            return True
        except Exception as e:
            logger.error('插入失败：' + str(data.id))
            logger.error(e, exc_info=True)
            self.session.rollback()
            return False

    def query_data_mid(self, mid):
        """
        :param symbol_pair:
        :param market_code:
        :return:
        """
        re = self.session.query(UserInfo).filter_by(mid=mid).limit(
            1).first()
        return re


if __name__ == '__main__':
    pass
