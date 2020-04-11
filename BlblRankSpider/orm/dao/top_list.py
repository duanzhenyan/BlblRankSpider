import logging
from BlblRankSpider.orm.model.financial_db_model import TopList
from BlblRankSpider.orm.engine import FINANCIAL_DBSession

logger = logging.getLogger(__name__)


class TopListDao(object):
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

    def query_data_by_title(self, title):
        """
        根据title查询是否有该条数据，没有返回None
        :param title:
        :return:
        """
        re = self.session.query(TopList).filter_by(title=title).limit(1).first()
        return re