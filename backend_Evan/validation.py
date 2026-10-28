"""Reject typos and invalid types before constructing SQL."""
import math
from datetime import date
class InvalidSearch(ValueError):
    def __init__(self, message, field=None):
        super().__init__(message)
        self.field = field

def obj(value, keys, path):
    if not isinstance(value, dict):
        raise InvalidSearch('Expected an object.', path)
    extra = value.keys() - keys
    if extra:
        raise InvalidSearch('Unknown field: ' + sorted(extra)[0], path)

def validate(data):
    obj(data, {'filters','relaxation','limit'}, 'request')
    f = data.get('filters', {}).copy() if isinstance(data.get('filters', {}),dict) else data['filters']
    obj(f, {'city','state','zip','housing_type_id','max_rent','min_beds','min_baths',
            'min_square_feet','available_by','amenity_ids'}, 'filters')
    for k in ('city','state','zip'):
        v=f.get(k)
        if v is not None:
            if not isinstance(v,str) or not v.strip() or len(v)>100:
                raise InvalidSearch('Expected a nonempty string of at most 100 characters.',k)
            f[k]=v.strip()
    for k in ('housing_type_id','max_rent','min_beds','min_baths','min_square_feet'):
        v=f.get(k)
        if v is not None:
            integer=k in ('housing_type_id','min_beds','min_square_feet')
            if type(v) not in (int,float) or not math.isfinite(v) or v<0 or (integer and type(v)!=int) or (k in ('housing_type_id','max_rent') and v==0):
                raise InvalidSearch('Invalid numeric filter.',k)
    v=f.get('available_by')
    if v is not None:
        try:
            if not isinstance(v,str) or date.fromisoformat(v).isoformat()!=v: raise ValueError()
        except ValueError: raise InvalidSearch('Use a date in YYYY-MM-DD format.','available_by')
    ids=f.get('amenity_ids')
    if ids is None: ids=[]
    if not isinstance(ids,list) or any(type(x)!=int or x<=0 for x in ids):
        raise InvalidSearch('Expected an array of positive integer IDs.','amenity_ids')
    f['amenity_ids']=list(dict.fromkeys(ids))
    defaults=dict(enabled=False,rent_overage=0,square_feet_shortfall=0,
                  allow_related_housing_types=False,allow_related_amenities=False)
    r=data.get('relaxation',{})
    obj(r,set(defaults),'relaxation')
    r=defaults | r
    for k in ('enabled','allow_related_housing_types','allow_related_amenities'):
        if type(r[k])!=bool: raise InvalidSearch('Expected true or false.',k)
    for k in ('rent_overage','square_feet_shortfall'):
        if type(r[k]) not in (int,float) or not math.isfinite(r[k]) or r[k]<0:
            raise InvalidSearch('Expected a finite nonnegative number.',k)
    limit=data.get('limit',10)
    if type(limit)!=int or not 1<=limit<=100: raise InvalidSearch('Limit must be 1–100.','limit')
    return dict(filters=f,relaxation=r,limit=limit)
