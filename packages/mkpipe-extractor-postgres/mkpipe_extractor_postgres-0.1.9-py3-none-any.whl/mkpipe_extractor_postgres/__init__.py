class PostgresExtractor:
    def __init__(self, config):
        self.config = config
    def extract(self):
        print('Extracting data from PostgreSQL...')
        data = {"v":1}
        return data