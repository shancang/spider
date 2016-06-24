# -*- coding: utf-8
import MySQLdb
dbuser="spider"
passwd="123456"
host="localhost"
port="3306"
dbname="spider"
class ConnectDB(object):
	def __init__(self):
		self.db=MySQLdb.connect(host,dbuser,passwd,dbname,charset="utf8")
		self.cursor = self.db.cursor()
	def insert(self,table_name	="", 
                    spaceid		="",
                    brand		="",
                    series		="",
                    models		="",
                    guide_price	="",
                    level		="",
                    emission_standard="",
                    structure	="",
                    status		="" ,
                    manufacturer="",
                    json_text	="",
                    URL_ 		=""
					):
		sql='''insert into %s set 
                    spaceid		=\'%s\',
                    brand		=\'%s\',
                    series		=\'%s\',
                    models		=\'%s\',
                    guide_price	=\'%s\',
                    level		=\'%s\',
                    emission_standard=\'%s\',
                    structure	=\'%s\',
                    status		=\'%s\',
                    manufacturer=\'%s\',
                    json_text	=\'%s\',
                    url 		=\'%s\'

								''' % (table_name,
									spaceid,
									brand,
									series,
									models,
									guide_price,
									level,
									emission_standard,
									structure,
									status,
									manufacturer,
									json_text,
									URL_)
		#print sql
		#try:
		self.cursor.execute(sql)
		self.db.commit()
		#except:
		#	self.db.rollback()
		
	def dbclose(self):
		self.db.close()
#db=ConnectDB()
##db.insert(table_name="json",spaceid=spaceid,json_data=json_data)
#db.dbclose()
		





