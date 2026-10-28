"""Exact first; relax only when no exact answers exist.
TAH policy: siblings with an explicitly configured shared parent may substitute.
This is a small two-level TAH, not a learned similarity model.
"""
import copy,json
from config import BASE_DIR
from queries import candidates

def related(kind,wanted,actual):
    tree=json.loads((BASE_DIR/'hierarchies.json').read_text())[kind]
    parent=tree.get(str(wanted))
    return parent is not None and parent==tree.get(str(actual))

def evaluate(unit,c,relaxed):
    f,r=c['filters'],c['relaxation']; p=unit['property']; changes=[]; penalties=[]
    for key in ('city','state','zip'):
        if f.get(key) is not None and f[key].casefold()!=p[key].casefold(): return None
    for key,field in [('min_beds','beds'),('min_baths','baths')]:
        if f.get(key) is not None and (unit[field] is None or unit[field]<f[key]): return None
    if f.get('available_by') and (not unit['date_available'] or unit['date_available']>f['available_by']): return None
    for key,field,tolerance,sign in [('max_rent','monthly_rent','rent_overage',1),('min_square_feet','square_feet','square_feet_shortfall',-1)]:
        if f.get(key) is None: continue
        if unit[field] is None: return None
        diff=max(0,sign*(unit[field]-f[key])); allowed=r[tolerance] if relaxed else 0
        if diff>allowed: return None
        penalties.append(diff/allowed if allowed else 0)
        if diff: changes.append(dict(field=field,requested=f[key],actual=unit[field],explanation=f'{field}: requested {f[key]}, returned {unit[field]}.'))
    wanted=f.get('housing_type_id'); actual=p['housing_type']['type_id']
    if wanted is not None:
        different=wanted!=actual
        if different and not (relaxed and r['allow_related_housing_types'] and related('housing_types',wanted,actual)): return None
        penalties.append(int(different))
        if different: changes.append(dict(field='housing_type_id',requested=wanted,actual=actual,explanation='Related housing type in the configured TAH.'))
    available={a['amenity_id'] for a in unit['amenities']}
    # Exact amenities are reserved; each alternative may satisfy only one request.
    missing=[x for x in f['amenity_ids'] if x not in available]
    unused=available-set(f['amenity_ids'])
    assignments={}
    def assign(index):
        if index==len(missing): return True
        wanted=missing[index]
        for actual in sorted(unused):
            if related('amenities',wanted,actual):
                unused.remove(actual); assignments[wanted]=actual
                if assign(index+1): return True
                unused.add(actual); assignments.pop(wanted)
        return False
    if missing and not (relaxed and r['allow_related_amenities'] and assign(0)): return None
    for wanted in f['amenity_ids']:
        penalties.append(int(wanted in assignments))
        if wanted in assignments: changes.append(dict(field='amenity_ids',requested=wanted,actual=assignments[wanted],explanation='Related amenity in the configured TAH.'))
    out=copy.deepcopy(unit)
    out['match']=dict(is_exact=not changes,distance_score=round(sum(penalties)/len(penalties),6) if penalties else 0,relaxations=changes)
    return out

def search(c):
    def run(relaxed):
        results=[x for u in candidates(c,relaxed) if (x:=evaluate(u,c,relaxed)) is not None]
        return sorted(results,key=lambda u:(u['match']['distance_score'],u['monthly_rent'],u['unit_id']))
    exact=run(False)
    return exact if exact or not c['relaxation']['enabled'] else run(True)
