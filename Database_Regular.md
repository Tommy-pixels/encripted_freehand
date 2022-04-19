# scrapy项目中的pipeline数据保存格式
针对判断记录是否上传过通过字段posted判断，不再采用维护 已上传数据库的方式 
针对筛选上传不再采用上传一次清除一次表的方式，而是根据当天时间以及判断是否上传过来筛选，该条件可在表中获取。  
另外数据库表要在数据库层面要做好去重  
对于数据是否有效的问题，上传了的数据就是有效数据，满足条件，没上传的就是无效数据，不满足条件。
关于posted:
原始数据上传 posted默认为0
经过筛选处理上传后， 上传了的数据posted更新为1 ，筛选不通过的更新为2
在选取未上传未处理的数据可以通过判断posted是否为0

## 1、 评论数据
	"INSERT INTO `dbfreeh`.`tb_comment` (`ori_url`, `comment`, `publish_time`, `crawl_time`, `site`, `classification`) VALUES ('{}', '{}', '{}', '{}', '知乎', '接口数据池');"
	- 字段说明
		ori_url			来源url
		comment 		评论内容字符串
		publish_time	评论发布时间
		crawl_time		评论爬取时间
		site 			来源站点
		classification	上传到哪个数据池
        posted          是否使用过  default 0 : 1 使用过 0 未使用过 2 不满足条件

## 2、 关键词段落
	"INSERT INTO `dbfreeh`.`tb_key_paragraph` (`ori_url`, `tag_origin`, `paragraph`, `publish_time`, `crawl_time`, `site`, `classification`) VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '接口数据池');"
	- 字段说明
		ori_url			来源url
		tag_origin		段落对应标签
		paragraph 		段落内容字符串
		publish_time	段落发布时间
		crawl_time		段落爬取时间
		site 			来源站点
		classification	上传到哪个数据池
        posted          是否使用过   default 0 : 1 使用过 0 未使用过 2 不满足条件

## 3、 关联词段落
	"INSERT INTO `dbfreeh`.`tb_relative_paragraph` (`ori_url`, `paragraph`, `publish_time`, `crawl_time`, `site`, `classification`) VALUES ('{}', '{}', '{}', '{}', '{}', '接口数据池');"
	- 字段说明
		ori_url			来源url
		paragraph 		段落内容字符串
		publish_time	段落发布时间
		crawl_time		段落爬取时间
		site 			来源站点
		classification	上传到哪个数据池
        posted          是否使用过   default 0 : 1 使用过 0 未使用过 2 不满足条件

## 4、 文章内容
	"INSERT INTO `dbfreeh`.`tb_article` (`ori_url`, `title`, `content`, `publish_time`, `crawl_time`, `site`, `classification`) VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '接口数据池');"
	- 字段说明
		ori_url			来源url
		title 			文章标题
		content  		文章内容字符串
		publish_time	文章发布时间
		crawl_time		文章爬取时间
		site 			来源站点
		classification	上传到哪个数据池
        posted          是否使用过   default 0 : 1 使用过 0 未使用过 2 不满足条件

## 5、 图片内容
	"INSERT INTO `dbfreeh`.`tb_img` (`img_type`, `ori_uri`, `reco`, `crawl_time`, `local_path`, `classification`) VALUES ('{}', '{}', '{}', '{}', '{}', '接口数据池');"
	- 字段说明
		img_type		图片要处理成什么类型： 缩略图/内容图 ： thumbnail/contentimg
		ori_url			来源url
		reco 			图片经过百度识别出的标题
		crawl_time		文章爬取时间
		local_path 		图片在本地保存的路径
		site 			来源站点
		classification	上传到哪个数据池
        posted          是否使用过   default 0 : 1 使用过 0 未使用过 2 不满足条件