import os
os.environ['DATA_MODE']='demo'
import unittest
from app import app
class SearchTests(unittest.TestCase):
    def setUp(self): self.client=app.test_client()
    def search(self,filters,relaxation=None):
        return self.client.post('/api/apartments/search',json=dict(filters=filters,relaxation=relaxation or {}))
    def test_exact(self):
        r=self.search(dict(max_rent=1300,min_beds=2)).get_json()
        self.assertEqual([u['unit_id'] for u in r['results']],[1,2])
        self.assertTrue(all(u['match']['is_exact'] for u in r['results']))
    def test_rent_relaxation(self):
        r=self.search(dict(max_rent=1200,min_beds=2),dict(enabled=True,rent_overage=200)).get_json()
        self.assertEqual([u['match']['distance_score'] for u in r['results']],[.25,.5,.9])
    def test_hard_filter(self):
        self.assertEqual(self.search(dict(city='Pullman'),dict(enabled=True,rent_overage=500)).get_json()['results'],[])
    def test_exact_prevents_relaxation(self):
        r=self.search(dict(max_rent=1250,min_beds=2),dict(enabled=True,rent_overage=200)).get_json()
        self.assertEqual(len(r['results']),1)
    def test_tah(self):
        r=self.search(dict(max_rent=1250,min_beds=2,amenity_ids=[1,3]),dict(enabled=True,allow_related_amenities=True)).get_json()
        self.assertEqual(r['results'][0]['unit_id'],1)
        self.assertFalse(r['results'][0]['match']['is_exact'])
    def test_invalid(self):
        for value in [True,-1,'1200']:
            self.assertEqual(self.search(dict(max_rent=value)).status_code,400)
        self.assertEqual(self.search(dict(amenity_ids=False)).status_code,400)
        self.assertEqual(self.search(dict(available_by='bad')).status_code,400)
        self.assertEqual(self.search(dict(typo=1)).status_code,400)
    def test_protocol(self):
        self.assertEqual(self.client.post('/api/apartments/search',data='bad',content_type='application/json').status_code,400)
        self.assertEqual(self.client.post('/api/apartments/search',data='bad').status_code,415)
        self.assertEqual(self.client.post('/api/apartments/search',json=[]).status_code,400)
if __name__=='__main__': unittest.main()
