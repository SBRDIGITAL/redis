from os import getenv
from dotenv import load_dotenv

from redis import Redis, ConnectionPool
from redis.exceptions import RedisError



class DotEnv:
    
    def __init__(self):
        """ # Загружаем переменные из .env файла """
        load_dotenv()
        self.host = getenv("REDIS_HOST")  # Получаем хост
        self.port = int(getenv("REDIS_PORT"))  # Получаем порт и преобразуем в int
        self.username = getenv(key="REDIS_USER")
        self.password = getenv(key="REDIS_USER_PASSWORD")

de = DotEnv()

redis = Redis(connection_pool=ConnectionPool(  # Создаем пул соединений
    host=de.host,
    port=de.port,
    db=0,
    username=de.username,
    password=de.password,
    max_connections=10  # Укажите максимальное количество соединений в пуле
))

def test():
    try:
        info = redis.info()
        print(info['redis_version'])
        response = redis.ping()
        if response:
            print("Подключение успешно!")
        else:
            print("Не удалось подключиться к Redis.")
    except (RedisError, Exception) as e:
        print(f"Ошибка: {e}")
    
    
        
if __name__ == "__main__":
    test()