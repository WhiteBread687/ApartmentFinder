"""Build JSON-compatible units, including Decimal and date conversion."""
def group_rows(rows):
    units={}
    for r in rows:
        uid=r['UnitID']
        if uid not in units:
            units[uid]=dict(unit_id=uid,unit_number=r['UnitNumber'],
                monthly_rent=float(r['Rent']),beds=r['Beds'],baths=float(r['Baths']),
                square_feet=r['SquareFeet'],date_available=r['DateAvailable'].isoformat() if r['DateAvailable'] else None,
                property=dict(property_id=r['PropertyID'],address=r['Address'],city=r['City'],state=r['State'],zip=r['Zip'],
                housing_type=dict(type_id=r['TypeID'],type_name=r['TypeName'])),amenities=[])
        if r['AmenityID'] is not None:
            a=dict(amenity_id=r['AmenityID'],amenity_name=r['AmenityName'],amenity_group=r['AmenityGroup'])
            if a not in units[uid]['amenities']: units[uid]['amenities'].append(a)
    return list(units.values())

def response(criteria, results):
    shown=results[:criteria['limit']]
    exact=sum(x['match']['is_exact'] for x in shown)
    message=('Exact matches found.' if exact else 'No exact matches. Showing permitted alternatives.') if shown else 'No apartments found within permitted limits.'
    return dict(search=criteria,summary=dict(returned_count=len(shown),exact_count=exact,
        approximate_count=len(shown)-exact,message=message),results=shown)
