from os import getenv
from dotenv import load_dotenv

from redis import Redis
from redis.exceptions import RedisError



class DotEnv:
    
    def __init__(self):
        """ # Загружаем переменные из .env файла """
        load_dotenv()
        self.username = getenv(key="REDIS_USER")
        self.password = getenv(key="REDIS_USER_PASSWORD")

de = DotEnv()


r = Redis(host='localhost', port=6380, db=0, username=de.username, password=de.password)


def test():
    try:
        info = r.info()
        print(info['redis_version'])
        response = r.ping()
        if response:
            print("Подключение успешно!")
        else:
            print("Не удалось подключиться к Redis.")
    except (RedisError, Exception) as e:
        print(f"Ошибка: {e}")
    
    
        
if __name__ == "__main__":
    test()