class PostgresLoader:
    def __init__(self, config):
        self.config = config
        
    def load(self, data, elt_start_time):
        print('Loading data to PostgreSQL...')
        data = {"v":1}
        return data