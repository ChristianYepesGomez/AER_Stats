import mysql.connector

mydb = mysql.connector.connect(
  host="sql7.freemysqlhosting.net",
  user="yourusername",
  password="yourpassword",
  database="mydatabase"
)
class AercrawlPipeline:
    def process_item(self, item, spider):
        return item
