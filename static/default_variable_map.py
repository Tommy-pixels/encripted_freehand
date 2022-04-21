#coding=utf-8
from conf import setting
DATABASE = setting.DATABASES['DBNAME']

# 默认创建的表名列表 需要默认创建的放在这个列表里
DEFAULT_TABLE_LIS = ['CREATE_DEFAULT_TABLE_SELE_INFO', 'CREATE_DEFAULT_TABLE_DATAPOOL_INFO', 'CREATE_DEFAULT_TABLE_KEYWORD_FORFILTER', 'CREATE_DEFAULT_TABLE_SCRAPYPROJECT',
                     'CREATE_DEFAULT_TABLE_PROCESS_INFO', 'CREATE_DEFAULT_TABLE_SITE_INFO','CREATE_DEFAULT_TABLE_STOCKS', 'CREATE_DEFAULT_TABLE_DATAUPLOAD_INFO'
                     'CREATE_DEFAULT_TABLE_COMMENT', 'CREATE_DEFAULT_TABLE_KEYPARAGRAPH', 'CREATE_DEFAULT_TABLE_RELATIVEPARAGRAPH', 'CREATE_DEFAULT_TABLE_ARTICLE',
                     'CREATE_DEFAULT_TABLE_IMG', 'CREATE_DEFAULT_TABLE_VIDEO']

"""全局使用的默认变量
    如 内置的表对应的操作SQL语句
"""
#######################
#  默认创建数据库和表    #
#      只执行一次      #
#####################
CREATE_DEFAULT_DATABASE = 'CREATE SCHEMA `{}`;'.format(DATABASE)
CREATE_DEFAULT_TABLE_SELE_INFO = """
    CREATE TABLE `tb_selenium_info` (
      `id` int NOT NULL AUTO_INCREMENT,
      `executor` varchar(250) DEFAULT NULL,
      `session_id` varchar(250) DEFAULT NULL,
      PRIMARY KEY (`id`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
    """

# 数据池信息表
CREATE_DEFAULT_TABLE_DATAPOOL_INFO = """
    CREATE TABLE `tb_datapool_info` (
      `id` INT NOT NULL AUTO_INCREMENT,
      `datapool_name` VARCHAR(45) NULL COMMENT '数据池中文名',
      `account` VARCHAR(45) NULL,
      `password` VARCHAR(45) NULL,
      `classification` VARCHAR(45) NULL COMMENT '数据池英文名，和任务库里的对应目录名相同，调用引用的也是这个',
      `api_uri` VARCHAR(45) NULL COMMENT '对应接口uri',
      `note` TEXT NULL,
      PRIMARY KEY (`id`))
    COMMENT = '上传的数据池的信息';
"""

CREATE_DEFAULT_TABLE_DATAUPLOAD_INFO = """
    CREATE TABLE `dbfreeh`.`tb_dataupload_info` (
      `id` INT NOT NULL AUTO_INCREMENT,
      `data_id` INT NULL DEFAULT COMMENT '原数据id',
      `table_name` VARCHAR(45) NULL DEFAULT COMMENT '原数据对应哪张表的',
      `datapool_id` INT NULL DEFAULT COMMENT '上传到哪个datapool',
      PRIMARY KEY (`id`))
    COMMENT = '已经上传的数据的上传信息';
"""

CREATE_DEFAULT_TABLE_KEYWORD_FORFILTER = """
    CREATE TABLE `tb_keyword_forfilter` (
      `id` int NOT NULL AUTO_INCREMENT,
      `keyword` varchar(45) DEFAULT NULL,
      `datapool_id` varchar(45) DEFAULT NULL,
      PRIMARY KEY (`id`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COMMENT '根据关键词表的关键词进行筛选'
"""


# scrapy项目表
CREATE_DEFAULT_TABLE_SCRAPYPROJECT = """
    CREATE TABLE `tb_scrapy_project` (
      `id` int NOT NULL AUTO_INCREMENT,
      `project_name` varchar(255) DEFAULT NULL,
      `site` varchar(45) DEFAULT NULL,
      `location_project` varchar(255) DEFAULT NULL,
      `location_items` varchar(255) DEFAULT NULL,
      `location_middlewares` varchar(255) DEFAULT NULL,
      `location_pipelines` varchar(255) DEFAULT NULL,
      `location_settings` varchar(255) DEFAULT NULL,
      `location_spiders` varchar(255) DEFAULT NULL,
      `task_detail` varchar(255) DEFAULT NULL,
      `note` varchar(255) DEFAULT NULL,
      PRIMARY KEY (`id`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 
"""

# 进程控制表
CREATE_DEFAULT_TABLE_PROCESS_INFO = """
    CREATE TABLE `tb_process_info` (
      `id` int NOT NULL AUTO_INCREMENT,
      `pid` int DEFAULT NULL,
      `task_detail` varchar(45) DEFAULT NULL,
      `execute_command` text,
      `task_type` varchar(45) DEFAULT NULL,
      `site` varchar(45) DEFAULT NULL,
      `beginTime` time DEFAULT NULL,
      `endTime` time DEFAULT NULL,
      `taskExcuteDelta` int DEFAULT NULL,
      `timeExcuteDelta` int DEFAULT NULL,
      `note` text,
      PRIMARY KEY (`id`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='进程控制'
    """
# 股票表
CREATE_DEFAULT_TABLE_STOCKS = """
    CREATE TABLE `tb_stocks` (
      `id` int NOT NULL AUTO_INCREMENT,
      `name` varchar(45) DEFAULT NULL,
      `code` varchar(45) DEFAULT NULL,
      `belonging` varchar(45) DEFAULT NULL,
      `ishot` varchar(1) DEFAULT NULL COMMENT '是否是热门股票 热门股票有500只 0为非热门 1 为热门',
      PRIMARY KEY (`id`)
    ) ENGINE=InnoDB  DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='股票表'
    """

# 站点表
CREATE_DEFAULT_TABLE_SITE_INFO = """
    CREATE TABLE `tb_site_info` (
      `id` int NOT NULL AUTO_INCREMENT,
      `crawl_type` varchar(45) DEFAULT NULL,
      `site` varchar(120) DEFAULT NULL,
      `site_url` longtext,
      `site_usable` varchar(45) DEFAULT NULL,
      `comment` longtext,
      `classification` varchar(45) DEFAULT NULL COMMENT '数据传到哪个平台',
      PRIMARY KEY (`id`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='关于站点的选择爬取情况\n'
    """

# 评论
CREATE_DEFAULT_TABLE_COMMENT = """
    CREATE TABLE `tb_comment` (
      `id` INT NOT NULL AUTO_INCREMENT,
      `ori_url` longtext COMMENT '评论来源链接',
      `comment` LONGTEXT NULL,
      `keyword` VARCHAR(45) NULL COMMENT '评论包含的指定关键词',
      `publish_time` DATETIME(6) NULL,
      `crawl_time` DATETIME(6) NULL COMMENT '评论爬取下来的时间',
      `site` VARCHAR(45) NULL COMMENT '评论来源站点名',
      `classification` varchar(45) DEFAULT NULL COMMENT '数据传到哪个平台',
      `note` varchar(45) DEFAULT NULL COMMENT '备注说明',
      `posted` INT(1) NOT NULL DEFAULT 0 COMMENT '数据是否已经上传 默认 0 ，1 上传过 0 未上传',
      PRIMARY KEY (`id`));
    """

# 关键词段落
CREATE_DEFAULT_TABLE_KEYPARAGRAPH = """
    CREATE TABLE `tb_key_paragraph` (
      `id` INT NOT NULL AUTO_INCREMENT,
      `ori_url` longtext COMMENT '段落来源链接',
      `paragraph` LONGTEXT NULL,
      `keyword` VARCHAR(45) NULL COMMENT '段落原标签',
      `publish_time` DATETIME(6) NULL COMMENT '段落发布时间',
      `crawl_time` DATETIME(6) NULL COMMENT '段落爬取下来的时间',
      `site` VARCHAR(45) NULL COMMENT '评论来源站点名',
      `classification` varchar(45) DEFAULT NULL COMMENT '数据传到哪个平台',
      `note` varchar(45) DEFAULT NULL COMMENT '备注说明',
      `posted` INT(1) NOT NULL DEFAULT 0 COMMENT '数据是否已经上传 默认 0 ，1 上传过 0 未上传',
      PRIMARY KEY (`id`));
    """

# 关联词段落
CREATE_DEFAULT_TABLE_RELATIVEPARAGRAPH = """
    CREATE TABLE `tb_relative_paragraph` (
      `id` INT NOT NULL AUTO_INCREMENT,
      `ori_url` longtext COMMENT '段落对应链接',
      `paragraph` LONGTEXT NULL,
      `keyword` VARCHAR(45) NULL COMMENT '关键词',
      `publish_time` DATETIME(6) NULL COMMENT '关联段落发布时间',
      `crawl_time` DATETIME(6) NULL COMMENT '关联段落爬取下来的时间',
      `site` VARCHAR(45) NULL COMMENT '来源站点名',
      `classification` varchar(45) DEFAULT NULL COMMENT '数据传到哪个平台',
      `note` varchar(45) DEFAULT NULL COMMENT '备注说明',
      `posted` INT(1) NOT NULL DEFAULT 0 COMMENT '数据是否已经上传 默认 0 ，1 上传过 0 未上传',
      PRIMARY KEY (`id`));
    """

# 文章
CREATE_DEFAULT_TABLE_ARTICLE = """
    CREATE TABLE `tb_article` (
      `id` int NOT NULL AUTO_INCREMENT,
      `ori_url` longtext COMMENT '文章对应链接',
      `title` varchar(255),
      `content` longtext,
      `publish_time` DATETIME(6) NULL COMMENT '文章发布时间',
      `crawl_time` DATETIME(6) NULL COMMENT '文章爬取下来的时间',
      `site` VARCHAR(255) COMMENT '文章来源站点',
      `classification` varchar(45) DEFAULT NULL COMMENT '数据传到哪个平台',
      `note` varchar(45) DEFAULT NULL COMMENT '备注说明',
      `posted` INT(1) NOT NULL DEFAULT 0 COMMENT '数据是否已经上传 默认 0 ，1 上传过 0 未上传',
      PRIMARY KEY (`id`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT=''
    """

# 视频信息
CREATE_DEFAULT_TABLE_VIDEO = """
    CREATE TABLE `tb_video` (
      `id` int NOT NULL AUTO_INCREMENT,
      `ori_uri` longtext  COMMENT '这个是可以直接下载的视频链接',
      `title` longtext,
      `publish_time` DATETIME(6) NULL COMMENT '该视频的发布时间',
      `crawl_time` DATETIME(6) NULL COMMENT '该视频爬取下来时间',
      `local_path` VARCHAR(255) COMMENT '该视频的在本地的位置',
      `site` VARCHAR(255) COMMENT '视频来源站点',
      `duration` varchar(45) DEFAULT NULL,
      `classification` varchar(45) DEFAULT NULL COMMENT '数据传到哪个平台',
      `posted` INT(1) NOT NULL DEFAULT 0 COMMENT '数据是否已经上传 默认 0 ，1 上传过 0 未上传',
      `note` varchar(45) DEFAULT NULL COMMENT '备注说明',
      PRIMARY KEY (`id`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC COMMENT '视频相关信息'
    """

# 图片信息
CREATE_DEFAULT_TABLE_IMG = """
    CREATE TABLE `tb_img` (
      `id` int NOT NULL AUTO_INCREMENT,
      `img_type` varchar(45) NOT NULL COMMENT '缩略图（thumbnail）还是内容图（connentimg）',
      `ori_uri` longtext COMMENT '图片源链接',
      `reco` longtext COMMENT '图片识别返回',
      `crawl_time` DATETIME(6) NULL COMMENT '该图片爬取下来时间',
      `local_path` VARCHAR(255) COMMENT '该图片的在本地的位置',
      `classification` varchar(45) DEFAULT NULL COMMENT '数据传到哪个平台',
      `note` varchar(45) DEFAULT NULL COMMENT '备注说明',
      `posted` INT(1) NOT NULL DEFAULT 0 COMMENT '数据是否已经上传 默认 0 ，1 上传过 0 未上传',
      PRIMARY KEY (`id`) USING BTREE
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 ROW_FORMAT=DYNAMIC COMMENT '图片信息'
    """



## 通用sql
TRUNCATE_TB_SQL = "TRUNCATE `{}`.`{}`;".format(DATABASE,'{}')
UPDATE_POSTED_RECORD = "UPDATE `{}` SET `posted`='{}' WHERE `id`='{}';"
SQL_INSERT_TBDATUPLOAD_INFO = "INSERT INTO `tb_dataupload_info` (`data_id`, `table_name`, `datapool_id`) VALUES ('{}', '{}', '{}');"
SELECT_FROM_IF_HAS = "SELECT * FROM `{}` WHERE {};"
DEFAULT_SQL_PARAM_IFHAS_PARAGRAPH = "`paragraph`='{}'"
DEFAULT_SQL_PARAM_IFHAS_ARTICLE = "`title`='{}'"
DEFAULT_SQL_PARAM_IFHAS_IMG = "`ori_uri`='{}'"
DEFAULT_SQL_PARAM_IFHAS_COMMENT = "`comment`='{}'"
DEFAULT_SQL_PARAM_IFHAS_VIDEO = "`ori_uri`='{}'"

INSERT_SELENIUM_INFO = ""
INSERT_SITE_INFO = ""




#######################
#  重用selenium引擎    #
#  tb_selenium_info  #
#####################
SELENIUM_REUSE_SQL_INSERT = "INSERT INTO `data_usable_database`.`tb_selenium_info` (`executor`, `session_id`) VALUES ('{}', '{}');"
SELENIUM_REUSE_SQL_UPDATE = "UPDATE `data_usable_database`.`tb_selenium_info` SET `executor` = '{}', `session_id` = '{}' WHERE (`id` = '{}');"


##########################
#   进程信息操作           #
#   主要用于自动化任务的操作 #
#   tb_process_info     #
########################



#######################
#   站点信息操作        #
#  tb_site_info      #
#####################





#######################
#   数据表 创建及操作    #
#  tb_      #
#####################
COMMENT_SQL_GET = "SELECT `comment` FROM commentdatabase.tb_comment_aigupiao_content;"
SQL_INSERT_KEYPARAGRAPH = "INSERT INTO `tb_key_paragraph` (`ori_url`,  `paragraph`, `keyword`,`publish_time`, `crawl_time`, `site`, `classification`) VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}');"
SQL_INSERT_RELATIVEPARAGRAPH = "INSERT INTO `tb_relative_paragraph` (`ori_url`, `paragraph`, `publish_time`, `crawl_time`, `site`, `classification`) VALUES ('{}', '{}', '{}', '{}', '{}', '{}');"
SQL_INSERT_COMMENT = "INSERT INTO `tb_comment` (`ori_url`, `comment`, `publish_time`, `crawl_time`, `site`, `classification`) VALUES ('{}', '{}', '{}', '{}', '{}', '{}');"
SQL_INSERT_ARTICLE = "INSERT INTO `tb_article` (`ori_url`, `title`, `content`, `publish_time`, `crawl_time`, `site`, `classification`) VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}');"
SQL_INSERT_IMG = "INSERT INTO `tb_img` (`img_type`, `ori_uri`, `reco`, `crawl_time`, `local_path`, `site`, `classification`) VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}');"
SQL_INSERT_VIDEO = "INSERT INTO `tb_video` (`ori_uri`, `title`, `publish_time`, `crawl_time`, `local_path`, `site`, `duration`, `classification`, `posted`) VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}');"

SQL_SELECT_UNPOSTED = "SELECT {} FROM `{}` WHERE {};"
DEFAULT_SQL_PARAM_UNPOSTED_FILTER_CONDITION = '`posted`={}{}'
DEFAULT_SQL_PARAM_UNPOSTED_KEYPARAGRAPH = '`id`, `ori_url`,  `paragraph`, `keyword`,`publish_time`, `crawl_time`, `site`, `classification`'
DEFAULT_SQL_PARAM_UNPOSTED_RELATIVEPARAGRAPH = '`id`, `ori_url`, `paragraph`, `keyword`, `publish_time`, `crawl_time`, `site`, `classification`'
DEFAULT_SQL_PARAM_UNPOSTED_COMMENT = '`id`, `ori_url`, `comment`, `keyword`, `publish_time`, `crawl_time`, `site`, `classification`'
DEFAULT_SQL_PARAM_UNPOSTED_ARTICLE = '`id`, `ori_url`, `title`, `content`, `publish_time`, `crawl_time`, `site`, `classification`'
DEFAULT_SQL_PARAM_UNPOSTED_IMG = '`id`, `ori_url`, `reco`, `crawl_time`, `local_path`, `site`, `classification`'
DEFAULT_SQL_PARAM_UNPOSTED_VIDEO = '`id`, `ori_url`, `title`, `publish_time`, `crawl_time`, `local_path`, `site`, `duration`, `classification`'







"""
问答表
CREATE TABLE `tb_zhihu_search_content` (
  `id` int NOT NULL AUTO_INCREMENT,
  `question_id` int DEFAULT NULL,
  `answer` longtext,
  `totle_answer` varchar(45) DEFAULT NULL COMMENT '源站中答案总数',
  `author_name` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `question_id` (`question_id`),
  CONSTRAINT `tb_zhihu_search_content_ibfk_1` FOREIGN KEY (`question_id`) REFERENCES `tb_zhihu_search_question` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9565 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci

CREATE TABLE `tb_zhihu_search_question` (
  `id` int NOT NULL AUTO_INCREMENT,
  `tag` varchar(45) DEFAULT NULL COMMENT '搜索关键词',
  `question` varchar(45) DEFAULT NULL COMMENT '问题的标题',
  `article_url` longtext COMMENT '文章链接',
  `describe` varchar(45) DEFAULT NULL COMMENT '问题的描述',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=317 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT '知乎搜索配资下的所有文章信息'
"""


