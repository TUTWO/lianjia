import json
import redis
import pymongo

def main():

    # 指定Redis数据库信息
    rediscli = redis.StrictRedis(host='39.108.230.161', port=6379, db=0, password='tumengting')
    # 指定MongoDB数据库信息
    mongocli = pymongo.MongoClient(host='localhost', port=27017)

    # 创建数据库名
    db = mongocli['lianjia']
    # 创建表名
    sheet = db['ershoufang']

    while True:
        # FIFO模式为 blpop，LIFO模式为 brpop，获取键值
        source, data = rediscli.blpop(["ershoufang:items"])

        item = json.loads(data)
        sheet.insert_one(item)

if __name__ == '__main__':
    main()