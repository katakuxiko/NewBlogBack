from elasticsearch import Elasticsearch

# Подключение к Elasticsearch (по умолчанию localhost:9200)
es = Elasticsearch("http://localhost:9200")

# Убедись, что индекс существует, если нет - создаем
def create_index(index_name: str):
    if not es.indices.exists(index=index_name):
        es.indices.create(index=index_name)
