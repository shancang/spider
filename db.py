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
	def insert(self,table_name="",
					spaceid="",
					status="",
					type_name="",
					manufacturer="",
					name="",
					price="",
					json_text=""
					):
		sql='''insert into %s set 
								spaceid=%s,
								status=\'%s\',
								type  =\'%s\',
								manufacturer=\'%s\',
								name=\'%s\',
								price=\'%s\',
								json_text=\'%s\'

								''' % (table_name,spaceid,status,type_name,manufacturer,name,price,json_text)
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
		





