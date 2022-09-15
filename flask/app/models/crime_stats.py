class Crime_stats:
    __table__ = 'core.crimes_summary'
    id_field = 'city'
    query_fields = {'city': str, 'category': str, 'gang_related': str}
    columns = [
        'city', 'category', 'gang_related', 'num_crimes_last30days', 'num_crimes_last180days', 'num_crimes_lastyear'
    ]

    def __init__(self, **kwargs):
        for key in kwargs.keys():
            if key not in self.columns:
                raise ValueError(f'{key} not in {self.columns}')
        for key, value in kwargs.items():
            setattr(self, key, value)

    def to_json(self):
        return self.__dict__