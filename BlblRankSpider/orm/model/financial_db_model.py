# -*- coding: utf-8 -*-
from sqlalchemy import Column
from sqlalchemy.dialects.mysql import VARCHAR, INTEGER, DATETIME, TIMESTAMP, TEXT, TINYINT
from sqlalchemy.ext.declarative import declarative_base, AbstractConcreteBase

# 创建对象的基类:
Base = declarative_base()


# 热门榜单表
class TopList(Base):
    __tablename__ = 'top_list'

    id = Column(INTEGER(11), primary_key=True, autoincrement=True, comment='主键ID')
    create_time = Column(DATETIME, default='', comment='榜单日期')
    list_tag = Column(VARCHAR(50), default='', comment='榜单分类')
    rank_id = Column(INTEGER(11), default=0, comment='榜单排名')
    video_source_url = Column(VARCHAR(500), default='', comment='榜单视频地址')
    title = Column(VARCHAR(500), default='', comment='榜单标题')
    score = Column(VARCHAR(150), default='', comment='榜单综合分数')
    mid = Column(VARCHAR(100), default='', comment='用户ID')

    def __str__(self):
        return str(self.__dict__)


# 用户基本信息
class UserInfo(Base):
    __tablename__ = 'user_info'

    id = Column(INTEGER(11), primary_key=True, autoincrement=True, comment='主键ID')
    mid = Column(VARCHAR(100), default='', comment='用户ID')
    user_name = Column(VARCHAR(150), default='', comment='用户姓名')
    user_sex = Column(VARCHAR(50), default='', comment='用户性别')
    user_head_url = Column(VARCHAR(500), default='', comment='用户头像地址')
    user_level = Column(VARCHAR(50), default='', comment='用户等级')
    user_fans_badge = Column(INTEGER(11), default=0, comment='粉丝徽章')
    user_sign = Column(VARCHAR(150), default='', comment='个人简介')

    def __str__(self):
        return str(self.__dict__)

# 用户视频信息
class UserVideoInfo(Base):
    __tablename__ = 'user_video_info'

    id = Column(INTEGER(11), primary_key=True, autoincrement=True, comment='主键ID')
    mid = Column(VARCHAR(100), default='', comment='用户ID')
    bvid = Column(VARCHAR(100), default='', comment='视频ID')
    video_url = Column(VARCHAR(500), default='', comment='视频URL')
    video_source_url = Column(VARCHAR(500), default='', comment='视频图片URL')
    video_title = Column(VARCHAR(100), default='', comment='标题')
    video_reply = Column(VARCHAR(50), default='', comment='评论数')
    video_favorite = Column(VARCHAR(50), default='', comment='收藏数')
    video_ctime = Column(DATETIME, default=0, comment='发布时间')

    def __str__(self):
        return str(self.__dict__)


class AbstractChapter(AbstractConcreteBase, Base):
    __abstract__ = True


if __name__ == '__main__':
    pass
