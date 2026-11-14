
import { useEffect, useState } from 'react'
import axios from 'axios'
import { Search, ChevronLeft, ChevronRight, RotateCcw } from 'lucide-react'
import './ListingsExplorer.css'

function ListingsExplorer() {
  const [listings, setListings] = useState([])
  const [cities, setCities] = useState([])
  const [categories, setCategories] = useState([])

  const [search, setSearch] = useState('')
  const [city, setCity] = useState('')
  const [category, setCategory] = useState('')

  const [page, setPage] = useState(1)
  const [pageSize, setPageSize] = useState(10)
  const [total, setTotal] = useState(0)
  const [totalPages, setTotalPages] = useState(0)

  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  // Load city and category filter options
  useEffect(() => {
    async function loadFilters() {
      try {
        const [cityResponse, categoryResponse] = await Promise.all([
          axios.get('/api/dashboard/city-wise'),
          axios.get('/api/dashboard/category-wise')
        ])

        const cityData = Array.isArray(cityResponse.data)
          ? cityResponse.data
          : cityResponse.data.items || []

        const categoryData = Array.isArray(categoryResponse.data)
          ? categoryResponse.data
          : categoryResponse.data.items || []

        setCities(cityData.map(item => item.city).filter(Boolean).sort())
        setCategories(
          categoryData.map(item => item.category).filter(Boolean).sort()
        )
      } catch (err) {
        console.error('Failed to load filter options:', err)
      }
    }

    loadFilters()
  }, [])

  // Fetch listings whenever search, filters or pagination changes
  useEffect(() => {
    let cancelled = false

    async function fetchListings() {
      setLoading(true)
      setError('')

      try {
        const response = await axios.get('/api/listings', {
          params: {
            search: search.trim() || undefined,
            city: city || undefined,
            category: category || undefined,
            page,
            page_size: pageSize
          }
        })

        if (!cancelled) {
          setListings(response.data.items)
          setTotal(response.data.total)
          setTotalPages(response.data.total_pages)
        }
      } catch (err) {
        if (!cancelled) {
          setError('Unable to load listings. Please try again.')
          console.error(err)
        }
      } finally {
        if (!cancelled) setLoading(false)
      }
    }

    fetchListings()

    return () => {
      cancelled = true
    }
  }, [search, city, category, page, pageSize])

  function resetFilters() {
    setSearch('')
    setCity('')
    setCategory('')
    setPage(1)
  }

  function changeCity(value) {
    setCity(value)
    setPage(1)
  }

  function changeCategory(value) {
    setCategory(value)
    setPage(1)
  }

  function changePageSize(value) {
    setPageSize(Number(value))
    setPage(1)
  }

  return (
    <section className="explorer-section">
      <div className="explorer-heading">
        <div>
          <h2>Business Listings Explorer</h2>
          <p>Search, filter and explore collected business listings.</p>
        </div>
        <span className="total-badge">
          {total.toLocaleString('en-IN')} results
        </span>
      </div>

      <div className="explorer-filters">
        <div className="search-box">
          <Search size={18} />
          <input
            type="text"
            placeholder="Search business name..."
            value={search}
            onChange={event => {
              setSearch(event.target.value)
              setPage(1)
            }}
          />
        </div>

        <select value={city} onChange={event => changeCity(event.target.value)}>
          <option value="">All Cities</option>
          {cities.map(item => (
            <option key={item} value={item}>{item}</option>
          ))}
        </select>

        <select
          value={category}
          onChange={event => changeCategory(event.target.value)}
        >
          <option value="">All Categories</option>
          {categories.map(item => (
            <option key={item} value={item}>{item}</option>
          ))}
        </select>

        <button className="reset-button" onClick={resetFilters}>
          <RotateCcw size={15} />
          Reset
        </button>
      </div>

      <div className="explorer-table-wrapper">
        <table className="explorer-table">
          <thead>
            <tr>
              <th>Business Name</th>
              <th>Category</th>
              <th>City</th>
              <th>Address</th>
              <th>Phone</th>
              <th>Source</th>
            </tr>
          </thead>

          <tbody>
            {loading ? (
              <tr>
                <td colSpan="6" className="table-message">
                  Loading listings...
                </td>
              </tr>
            ) : error ? (
              <tr>
                <td colSpan="6" className="table-message error-message">
                  {error}
                </td>
              </tr>
            ) : listings.length === 0 ? (
              <tr>
                <td colSpan="6" className="table-message">
                  No listings found.
                </td>
              </tr>
            ) : (
              listings.map(item => (
                <tr key={item.id}>
                  <td className="business-name">{item.business_name}</td>
                  <td>
                    <span className="category-tag">
                      {item.category || 'Uncategorized'}
                    </span>
                  </td>
                  <td>{item.city}</td>
                  <td>{item.address || '—'}</td>
                  <td>{item.phone || '—'}</td>
                  <td>{item.source}</td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>

      <div className="explorer-pagination">
        <div className="page-size-control">
          <label htmlFor="page-size">Rows per page:</label>
          <select
            id="page-size"
            value={pageSize}
            onChange={event => changePageSize(event.target.value)}
          >
            <option value="10">10</option>
            <option value="20">20</option>
            <option value="50">50</option>
          </select>
        </div>

        <span className="page-info">
          Page {page} of {totalPages.toLocaleString('en-IN')}
        </span>

        <div className="page-buttons">
          <button
            disabled={page <= 1 || loading}
            onClick={() => setPage(current => current - 1)}
            aria-label="Previous page"
          >
            <ChevronLeft size={18} />
          </button>

          <button
            disabled={page >= totalPages || loading}
            onClick={() => setPage(current => current + 1)}
            aria-label="Next page"
          >
            <ChevronRight size={18} />
          </button>
        </div>
      </div>
    </section>
  )
}

export default ListingsExplorer
