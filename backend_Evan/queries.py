"""SQL names are a proposed contract with Shawn; see README."""
import json
from config import DATA_MODE, BASE_DIR
from db import connection

def candidates(criteria, relaxed=False):
    f,r=criteria['filters'],criteria['relaxation']
    if DATA_MODE=='demo':
        units=json.loads((BASE_DIR/'demo_units.json').read_text())
        return units
    if DATA_MODE!='mysql': raise RuntimeError('DATA_MODE must be demo or mysql')
    clauses=[]; values=[]
    for key,col,op in [('city','p.City','='),('state','p.State','='),('zip','p.Zip','='),
        ('min_beds','u.Beds','>='),('min_baths','u.Baths','>='),('available_by','u.DateAvailable','<=')]:
        if f.get(key) is not None:
            clauses.append(f'{col} {op} %s'); values.append(f[key])
    if f.get('max_rent') is not None:
        clauses.append('u.Rent <= %s'); values.append(f['max_rent']+(r['rent_overage'] if relaxed else 0))
    if f.get('min_square_feet') is not None:
        clauses.append('u.SquareFeet >= %s'); values.append(f['min_square_feet']-(r['square_feet_shortfall'] if relaxed else 0))
    # Category/amenity checks run in matching.py after grouping joined rows.
    sql='SELECT u.UnitID,u.UnitNumber,u.Rent,u.Beds,u.Baths,u.SquareFeet,u.DateAvailable,\n        p.PropertyID,p.Address,p.City,p.State,p.Zip,h.TypeID,h.TypeName,\n        a.AmenityID,a.AmenityName,a.AmenityGroup\n        FROM ApartmentUnit u JOIN Property p ON u.PropertyID=p.PropertyID\n        JOIN HousingType h ON p.TypeID=h.TypeID\n        LEFT JOIN UnitAmenity ua ON ua.UnitID=u.UnitID\n        LEFT JOIN Amenity a ON a.AmenityID=ua.AmenityID'
    if clauses: sql+=' WHERE '+' AND '.join(clauses)
    from serializers import group_rows
    with connection() as conn:
        cursor=conn.cursor(dictionary=True)
        try:
            cursor.execute(sql,values)
            return group_rows(cursor.fetchall())
        finally: cursor.close()
