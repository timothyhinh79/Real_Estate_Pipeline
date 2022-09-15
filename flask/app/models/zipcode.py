class Zipcode:
    __table__ = 'core.median_age_income_by_zip'
    id_field = 'zip'
    # query_fields = {}
    columns = [
        'id'
        , 'year'
        , 'dataset'
        , 'zip'
        , 'median_age'
        , 'median_income'
    ]

    def __init__(self, **kwargs):
        for key in kwargs.keys():
            if key not in self.columns:
                raise ValueError(f'{key} not in {self.columns}')
        for key, value in kwargs.items():
            setattr(self, key, value)

    # dupe-1: consider factoring out below 3 methods into one method
    def get_population_by_agesex(self, conn):
        cursor = conn.cursor()
        query = """
            SELECT sex, age_range, population
            FROM core.population_by_agesex_and_zip
            WHERE zip = %s
        """
        cursor.execute(query, vars = (self.zip,))
        records = cursor.fetchall()
        return {f'{record[0]} {record[1]}':record[2] for record in records}

    def get_population_by_incomelevel(self, conn):
        cursor = conn.cursor()
        query = """
            SELECT income_range, population
            FROM core.population_by_incomelevel_and_zip
            WHERE zip = %s
        """
        cursor.execute(query, vars = (self.zip,))
        records = cursor.fetchall()
        return {record[0]:record[1] for record in records}

    def get_population_by_race(self, conn):
        cursor = conn.cursor()
        query = """
            SELECT race, population
            FROM core.population_by_race_and_zip
            WHERE zip = %s
        """
        cursor.execute(query, vars = (self.zip,))
        records = cursor.fetchall()
        return {record[0]:record[1] for record in records}

    def to_json(self, conn):
        zipcode_json = self.__dict__
        zipcode_json['population_by_agesex'] = self.get_population_by_agesex(conn)
        zipcode_json['population_by_incomelevel'] = self.get_population_by_incomelevel(conn)
        zipcode_json['population_by_race'] = self.get_population_by_race(conn)
        return zipcode_json