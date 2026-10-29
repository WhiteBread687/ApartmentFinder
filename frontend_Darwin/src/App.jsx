import { useState } from 'react'
import './App.css'

function App() {
  const [city, setCity] = useState('Moscow')
  const [state, setState] = useState('ID')
  const [zip, setZip] = useState('')
  const [housingTypeId, setHousingTypeId] = useState('')
  const [maxRent, setMaxRent] = useState('1200')
  const [minBeds, setMinBeds] = useState('2')
  const [minBaths, setMinBaths] = useState('')
  const [minSqft, setMinSqft] = useState('800')
  const [availableBy, setAvailableBy] = useState('')
  const [amenityIds, setAmenityIds] = useState([1, 3])

  const [relaxEnabled, setRelaxEnabled] = useState(true)
  const [rentOverage, setRentOverage] = useState('200')
  const [sqftShortfall, setSqftShortfall] = useState('100')
  const [allowRelatedHousing, setAllowRelatedHousing] = useState(false)
  const [allowRelatedAmenities, setAllowRelatedAmenities] = useState(true)

  const [data, setData] = useState(null)
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  function toggleAmenity(id) {
    if (amenityIds.includes(id)) {
      setAmenityIds(amenityIds.filter(item => item !== id))
    } else {
      setAmenityIds([...amenityIds, id])
    }
  }

  async function handleSearch(e) {
    e.preventDefault()
    setLoading(true)
    setError('')

    const filters = {
      city: city.trim() ? city.trim() : null,
      state: state.trim() ? state.trim() : null,
      zip: zip.trim() ? zip.trim() : null,
      housing_type_id: housingTypeId ? parseInt(housingTypeId, 10) : null,
      max_rent: maxRent ? Number(maxRent) : null,
      min_beds: minBeds !== '' ? parseInt(minBeds, 10) : null,
      min_baths: minBaths !== '' ? Number(minBaths) : null,
      min_square_feet: minSqft !== '' ? parseInt(minSqft, 10) : null,
      available_by: availableBy ? availableBy : null,
      amenity_ids: amenityIds
    }

    const relaxation = {
      enabled: relaxEnabled,
      rent_overage: rentOverage !== '' ? Number(rentOverage) : 0,
      square_feet_shortfall: sqftShortfall !== '' ? Number(sqftShortfall) : 0,
      allow_related_housing_types: allowRelatedHousing,
      allow_related_amenities: allowRelatedAmenities
    }

    try {
      const res = await fetch('/api/apartments/search', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ filters, relaxation, limit: 10 })
      })
      const json = await res.json()
      if (!res.ok) {
        setError(json.error ? json.error.message : 'Search failed')
        setData(null)
      } else {
        setData(json)
      }
    } catch (err) {
      setError('Could not connect to backend server.')
      setData(null)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="container">
      <h1>SmartBase Apartment Finder</h1>

      <form onSubmit={handleSearch}>
        <div className="section">
          <h3>Apartment Filters</h3>
          <div className="grid">
            <div className="field">
              <label>City</label>
              <input value={city} onChange={e => setCity(e.target.value)} />
            </div>
            <div className="field">
              <label>State</label>
              <input value={state} onChange={e => setState(e.target.value)} />
            </div>
            <div className="field">
              <label>Zip Code</label>
              <input value={zip} onChange={e => setZip(e.target.value)} />
            </div>
            <div className="field">
              <label>Housing Type</label>
              <select value={housingTypeId} onChange={e => setHousingTypeId(e.target.value)}>
                <option value="">Any</option>
                <option value="1">Apartment</option>
                <option value="2">Duplex</option>
              </select>
            </div>
            <div className="field">
              <label>Max Rent ($)</label>
              <input type="number" value={maxRent} onChange={e => setMaxRent(e.target.value)} />
            </div>
            <div className="field">
              <label>Min Beds</label>
              <input type="number" value={minBeds} onChange={e => setMinBeds(e.target.value)} />
            </div>
            <div className="field">
              <label>Min Baths</label>
              <input type="number" step="0.5" value={minBaths} onChange={e => setMinBaths(e.target.value)} />
            </div>
            <div className="field">
              <label>Min Square Feet</label>
              <input type="number" value={minSqft} onChange={e => setMinSqft(e.target.value)} />
            </div>
            <div className="field">
              <label>Available By (YYYY-MM-DD)</label>
              <input type="date" value={availableBy} onChange={e => setAvailableBy(e.target.value)} />
            </div>
          </div>

          <label><b>Required Amenities:</b></label>
          <div className="checkbox-row">
            <label>
              <input type="checkbox" checked={amenityIds.includes(1)} onChange={() => toggleAmenity(1)} />
              In-unit laundry
            </label>
            <label>
              <input type="checkbox" checked={amenityIds.includes(2)} onChange={() => toggleAmenity(2)} />
              Shared on-site laundry
            </label>
            <label>
              <input type="checkbox" checked={amenityIds.includes(3)} onChange={() => toggleAmenity(3)} />
              Dishwasher
            </label>
          </div>
        </div>

        <div className="section">
          <h3>Query Relaxation (SmartBase / TAH)</h3>
          <div className="checkbox-row" style={{ marginBottom: '12px' }}>
            <label>
              <input type="checkbox" checked={relaxEnabled} onChange={e => setRelaxEnabled(e.target.checked)} />
              <b>Enable Query Relaxation</b>
            </label>
            <label>
              <input type="checkbox" checked={allowRelatedHousing} onChange={e => setAllowRelatedHousing(e.target.checked)} />
              Allow Related Housing Types (TAH)
            </label>
            <label>
              <input type="checkbox" checked={allowRelatedAmenities} onChange={e => setAllowRelatedAmenities(e.target.checked)} />
              Allow Related Amenities (TAH)
            </label>
          </div>

          <div className="grid">
            <div className="field">
              <label>Allowed Rent Overage ($)</label>
              <input type="number" value={rentOverage} onChange={e => setRentOverage(e.target.value)} />
            </div>
            <div className="field">
              <label>Allowed SqFt Shortfall</label>
              <input type="number" value={sqftShortfall} onChange={e => setSqftShortfall(e.target.value)} />
            </div>
          </div>
        </div>

        <div className="buttons">
          <button type="submit" disabled={loading}>
            {loading ? 'Searching...' : 'Search Apartments'}
          </button>
        </div>
      </form>

      {error && <div className="error-box">{error}</div>}

      {data && (
        <div>
          <div className="summary-box">
            <b>{data.summary.message}</b> — Returned: {data.summary.returned_count} (Exact: {data.summary.exact_count}, Relaxed: {data.summary.approximate_count})
          </div>

          {data.results.map(unit => (
            <div key={unit.unit_id} className="unit-card">
              <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                <h3>
                  {unit.property.address} - Unit {unit.unit_number} ({unit.property.housing_type.type_name})
                </h3>
                <span className={unit.match.is_exact ? 'badge-exact' : 'badge-relaxed'}>
                  {unit.match.is_exact ? 'Exact Match' : `Relaxed Match (Distance: ${unit.match.distance_score})`}
                </span>
              </div>

              <p>
                <b>Location:</b> {unit.property.city}, {unit.property.state} {unit.property.zip} |{' '}
                <b>Rent:</b> ${unit.monthly_rent}/mo |{' '}
                <b>Beds:</b> {unit.beds} | <b>Baths:</b> {unit.baths} |{' '}
                <b>SqFt:</b> {unit.square_feet} | <b>Available:</b> {unit.date_available}
              </p>

              <p>
                <b>Amenities:</b>{' '}
                {unit.amenities.length > 0
                  ? unit.amenities.map(a => a.amenity_name).join(', ')
                  : 'None'}
              </p>

              {!unit.match.is_exact && unit.match.relaxations.length > 0 && (
                <div className="relaxation-list">
                  <b>Relaxed Criteria:</b>
                  <ul>
                    {unit.match.relaxations.map((rel, idx) => (
                      <li key={idx}>{rel.explanation}</li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  )
}

export default App