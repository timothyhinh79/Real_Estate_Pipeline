class House_listing:
    __table__ = 'core.house_listings'
    id_field = 'zpid'
    query_fields = {'zpid': int, 'zipcode': str, 'city': str, 'state': str, 'price': float}
    columns = [
        'id','zpid', 'extract_date', 'street_address', 'zipcode', 'city', 'state', 
        'latitude', 'longitude', 'price', 'bathrooms', 'bedrooms', 'living_area', 
        'home_type', 'home_status', 'days_on_zillow', 'is_featured', 'should_highlight', 
        'zestimate', 'rent_zestimate', 'is_open_house', 'is_fsba', 'open_house', 'is_unmappable', 
        'is_preforeclosure_auction', 'home_status_for_hdp', 'price_for_hdp', 'is_non_owner_occupied', 
        'is_premier_builder', 'is_zillow_owned', 'currency', 'country', 'tax_assessed_value', 
        'lot_area_value', 'lot_area_unit'
    ]

    def __init__(self, **kwargs):
        for key in kwargs.keys():
            if key not in self.columns:
                raise ValueError(f'{key} not in {self.columns}')
        for key, value in kwargs.items():
            setattr(self, key, value)

    def to_json(self):
        return self.__dict__

    
    