# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class CrawlerPipeline(object):
    def __init__(self):
            self.urls_visited = set()

    def process_item(self, item, spider):
        if item['url'] in self.urls_visited:
              raise DropItem("Duplicate url found :{}".format(item))
        else:
              self.urls_visited.add(item['url'])
        return item

# class PasteDetailsToJson(object):
#     def __inti__(self):
#         pass

#     def apply_keys(self, item, spider):
#         count = 0
#         result_dict = {}
#         count_data = []
#         paste_details = item.get('paste_details')
#         for index, line in enumerate(details):
#             if index == 0 and not re.search(r'^\s$', line):
#                 line = " ".join( re.findall('[^\s]+') )
#                 count_data.append(line)

#             elif not re.search(r'^\s$', line):
#                 line = " ".join( re.findall('[^\s]+', line) )
#                 count_data.append(line)

#             elif index == len(details) - 1:
#                 result_dict.update( {count: count_data})

#             elif re.search(r'^\s$', line) and count_data:
#                 result_dict.update( {count: count_data} )
#                 count += 1
#                 count_data = []

#             else:
#               continue
#         item['paste_details'] = result_dict
#         return item


# class SQLPipeline(object):

#     def __init__(self):
#         self.conn = MySQLdb.connect(
#           user='root', 
#           passwd='password here', 
#           host='localhost', 
#           db='scraped_data', 
#           use_unicode=True, 
#           charset='utf8')
#         self.cursor = self.conn.cursor()

#     def process_item(self, item, spider):
#         try:
#             self.cursor.execute("""CREATE TABLE IF NOT EXIST pastebin (
#                                    title VARCHAR(100),
#                                    url VARCHAR(100),
#                                    date_posted VARCHAR(50),
#                                    unique_visitors VARCHAR(20),
#                                    deletion_date VARCHAR(25),
#                                    paste_details MEDIUMTEXT ); """
#                                    )

#             self.cursor.execute("""insert into pastebin (title, url, date_posted, unique_visitors, deletion_date, past$
#                 values (%s, %s, %s, %s, %s, %s)""", item.values() )
#         except (AttributeError, MySQLdb.OperationalError):
#             raise
#         finally:
#             spider.log("Item stored in db: %s" % item, level=log.DEBUG)

#         self.conn.commit()
#         #self.conn.close()

#     def handle_error(self, e):
#         log.err(e)

