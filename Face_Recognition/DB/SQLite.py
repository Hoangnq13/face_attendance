import sqlite3


class SQLite:
	
	def __init__(self, name_db):
		try:
			self.connection = sqlite3.connect(name_db)
			print(f"Successfully Connected {name_db}")
			self.cursor = self.connection.cursor()
			# self.cursor.execute("PRAGMA foreign_keys = ON")
		except sqlite3.Error as error:
			print(f"Failed open {name_db}", error)
	
	def createConnect(self):
		return self.connection
	
	def createTable(self, table_name, set_filed):
		
		command = f"CREATE TABLE IF NOT EXISTS {table_name} "
		table = command + set_filed
		self.cursor.execute(table)
	
	def insertData(self, table_name, dict_insert):
		
		all_field = ""
		all_values = ""
		for key, val in dict_insert.items():
			all_field += f"'{key}'" + ","
			all_values += f"'{val}'" + ","
		all_field = all_field[:-1]
		all_values = all_values[:-1]
		command = f"INSERT INTO {table_name}({all_field}) VALUES({all_values})"
		self.cursor.execute(command)
		self.connection.commit()
	
	def getData(self, table_name, field_get:list, field_where:dict):  # field_get :list field ,field_where : dict field
		
		all_field_get = ""
		for field in field_get:
			all_field_get += f"{field},"
		all_field = all_field_get[:-1]
		all_field_where = ""
		for key, val in field_where.items():
			all_field_where += f"{key}='{val}' and "
		all_field_where = all_field_where[:-4]
		command = f"SELECT {all_field} from {table_name} WHERE {all_field_where}"
		self.cursor.execute(command)
		records = self.cursor.fetchall()
		
		return records
	
	def updateData(self, table_name, field_update:dict, where_field:dict):  # field_update :dict field ,where_field : dict field
		
		all_field_update = ""
		for k, val in field_update.items():
			all_field_update += f"{k}='{val}',"
		all_field_update = all_field_update[:-1]
		all_field_where = ""
		for key, val in where_field.items():
			all_field_where += f"{key}='{val}' and "
		all_field_where = all_field_where[:-4]
		command = f"UPDATE {table_name} SET {all_field_update} WHERE {all_field_where};"
		self.cursor.execute(command)
		self.connection.commit()
	
	def delete(self, table_name, where_field):
		all_field_where = ""
		for key, val in where_field.items():
			all_field_where += f"{key}='{val}' and "
		all_field_where = all_field_where[:-4]
		command = f"DELETE FROM {table_name} WHERE {all_field_where}"
		self.cursor.execute(command)
		self.connection.commit()
	
	def closeDb(self):
		
		if self.connection:
			self.connection.close()
			print("The SQLite connection is closed")

# current_time = datetime.now()
# VN_TZ = pytz.timezone('Asia/Ho_Chi_Minh')
# current_time = current_time.astimezone(VN_TZ)
# PRIMARY KEY (field2, field1)

# a = SQLite("App/Db/ChatBot.db")
# a.create_table("TABLE_BOTS",f"(UserName TEXT,BotName TEXT,Tags TEXT,AccuracyTag FLOAT,ChartImageTag TEXT,Entities TEXT DEFAULT None,AccuracyEntities FLOAT DEFAULT None,ChartImageEntities TEXT DEFAULT None,create_at TEXT DEFAULT None,PRIMARY KEY (UserName, BotName))")
# a.create_table("BOTS_ANSWER",f"(UserName TEXT,BotName TEXT,TagName TEXT,Answer TEXT,create_at TEXT DEFAULT None,FOREIGN KEY (UserName,BotName) REFERENCES TABLE_BOTS (UserName,BotName) )")
# a.create_table("BOTS_TRAINING",f"(UserName TEXT,BotName TEXT,Status TEXT,create_at TEXT DEFAULT None,FOREIGN KEY (UserName,BotName) REFERENCES TABLE_BOTS (UserName,BotName) )")

# a.insert_data("BOTS_ANSWER",{"UserName":"aa","BotName":"as","TagName":"asda","answer":"adas","Create_at":123})
# a.delete("RESPONSE_ANSWER",{"UserName":"Vip2","BotName":"bot_dan_12"})
# a.get_data("TABLE_TAGS",["UserName","BotName"],{"UserName":'Vip2',"BotName":'bot_dan_12'})
# a.update_data("TABLE_TAGS", {"Accuracy": 12}, {"UserName": 'Vip2', "BotName": 'bot_dan_12'})

# a.insert_data("RESPONSE_ANSWER","(UserName,BotName,AllTag) ",f"('{user_name}','{bot_name}','{str_list_tag}')")
# a.close_db()
