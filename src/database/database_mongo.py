import json

from pymongo import MongoClient

from src.utils.logger import Logger
from src.utils.utils import Tweet

class DatabaseMongo(object):

    host='localhost'
    port=27017
    db='tsap'

    def __init__(self):
        '''
            Retorna uma instância de uma conexão do mongodb para a coleção de tweets
        '''
        client = MongoClient(self.host, self.port)
        database = client['tsap']
        self.collection = database['tweets']
        self.collection_classificados = database['tweets_classificados']
        self.collection_classificados_sentilex = database['tweets_classificados_sentilex']
        self.collection_classificados_manualmente = database['tweets_classificados_manualmente']
        self.collection_testes_classificados = database['tweets_testes_classificados']
        self.collection_manual = database['tweets_classificados_N_P_T']

    def find_paginated(self, page_size, page_num):
        # returns a set of documents belonging to page number `page_num` where size of each page is `page_size`.
        # Calculate number of documents to skip
        skips = page_size * (page_num - 1)
        # Skip and limit
        cursor = self.collection.find().skip(skips).limit(page_size)
        # Return documents
        return cursor

    # The same as find_paginated, but on another collection
    def find_paginated_classified(self, page_size, page_num):
        skips = page_size * (page_num - 1)
        cursor = self.collection_classificados.find().skip(skips).limit(page_size)
        return cursor

    # The same as find_paginated, but on another collection
    def find_paginated_csv(self, page_size, page_num):
        skips = page_size * (page_num - 1)
        cursor = self.collection_manual.find().skip(skips).limit(page_size)
        return cursor

    def find(self):
        tweets = self.collection.find({})
        return tweets

    def find_all_classificados(self):
        tweets = self.collection_classificados.find({})
        return tweets

    def find_all_classificados_manualmente(self):
        tweets = self.collection_classificados_manualmente.find({})
        return tweets

    def find_all_classificados_sentilex(self):
        tweets = self.collection_classificados_sentilex.find({})
        return tweets

    def update(self, tweet):
        self.collection.save(tweet)

    def remove(self, tweet):
        self.collection.remo

    def persist_classified(self, tweet):
        self.collection_classificados.save(tweet)

    def persist_classified_manualmente(self, tweet):
        self.collection_classificados_manualmente.save(tweet)

    def persist_classified_sentilex(self, tweet):
        self.collection_classificados_sentilex.save(tweet)

    def persist_test_classified(self, tweet):
        self.collection_testes_classificados.save(tweet)

    def persist_tweet(self, tweet):
        try:
            tweet_json = json.loads(tweet)
            if (Tweet.is_retweet(tweet_json)):
                Logger.warn('Ignorando RT...\n')
            else:
                self.collection.insert(tweet_json)
                Logger.ok(tweet)

        except BaseException as e:
            Logger.error('Falha ao salvar tweet\nStacktrace: {}'.format(e))
