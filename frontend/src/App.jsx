
import { useEffect, useState } from 'react'
import axios from 'axios'
axios.defaults.baseURL =
  import.meta.env.VITE_API_URL || ''


import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
  Legend,
} from 'recharts'

import {
  Building2,
  MapPin,
  Tags,
  Database,
  RefreshCw,
} from 'lucide-react'

import './App.css'
import ListingsExplorer from './ListingsExplorer'


const API = '/api/dashboard'

const COLORS = [
  '#6366f1',
  '#06b6d4',
  '#f59e0b',
  '#10b981',
  '#ec4899',
  '#8b5cf6',
  '#f97316',
  '#14b8a6',
  '#94a3b8',
]

const numberFormat = (value) =>
  Number(value ?? 0).toLocaleString()


function App() {
  const [summary, setSummary] = useState(null)
  const [cities, setCities] = useState([])
  const [categories, setCategories] = useState([])
  const [sources, setSources] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')


  async function fetchDashboardData() {
    try {
      setLoading(true)
      setError('')

      const [
        summaryResponse,
        cityResponse,
        categoryResponse,
        sourceResponse,
      ] = await Promise.all([
        axios.get(`${API}/summary`),
        axios.get(`${API}/city-wise`),
        axios.get(`${API}/category-wise`),
        axios.get(`${API}/source-wise`),
      ])

      setSummary(summaryResponse.data)
      setCities(cityResponse.data)
      setCategories(categoryResponse.data)
      setSources(sourceResponse.data)

    } catch (err) {
      console.error('Dashboard API error:', err)

      setError(
        'Unable to load dashboard data. Check whether FastAPI and MySQL are running.'
      )

    } finally {
      setLoading(false)
    }
  }


  useEffect(() => {
    fetchDashboardData()
  }, [])


  // Display the top 10 cities, including Pune and Mumbai.
  const cityChartData = [...cities]
    .sort((a, b) => Number(b.total) - Number(a.total))
    .slice(0, 10)


  // Display the 8 largest categories and combine the rest.
  const sortedCategories = [...categories].sort(
    (a, b) => Number(b.total) - Number(a.total)
  )

  const topCategories = sortedCategories.slice(0, 8)
  const remainingCategories = sortedCategories.slice(8)

  const otherCategoryTotal = remainingCategories.reduce(
    (sum, item) => sum + Number(item.total),
    0
  )

  const categoryChartData = [
    ...topCategories,
    ...(otherCategoryTotal > 0
      ? [{ category: 'Other', total: otherCategoryTotal }]
      : []),
  ]


  // Sort data sources by listing count.
  const sortedSources = [...sources].sort(
    (a, b) => Number(b.total) - Number(a.total)
  )


  if (loading) {
    return (
      <div className="status-screen">
        <RefreshCw className="spin" size={28} />
        <p>Loading dashboard...</p>
      </div>
    )
  }


  if (error) {
    return (
      <div className="status-screen">
        <p className="error-message">{error}</p>
        <button onClick={fetchDashboardData}>
          Try again
        </button>
      </div>
    )
  }


  return (
    <main className="dashboard">

      {/* Header */}
      <header className="topbar">

        <div className="brand">

          <div className="brand-icon">
            <Building2 size={23} />
          </div>

          <div>
            <h1>Business Insights</h1>
            <p>Business Listings Analytics</p>
          </div>

        </div>

        <button
          className="refresh-button"
          onClick={fetchDashboardData}
          disabled={loading}
        >
          <RefreshCw size={16} />
          Refresh
        </button>

      </header>


      {/* Welcome section */}
      <section className="welcome">

        <div>
          <h2>Dashboard Overview</h2>
          <p>Monitor and analyze your business listing data.</p>
        </div>

        <span className="live-indicator">
          <span />
          Connected
        </span>

      </section>


      {/* KPI Cards */}
      <section className="stats-grid">

        <StatCard
          title="Total Listings"
          value={summary?.total_listings ?? 0}
          icon={<Building2 />}
          color="purple"
        />

        <StatCard
          title="Cities Covered"
          value={cities.length}
          icon={<MapPin />}
          color="blue"
        />

        <StatCard
          title="Business Categories"
          value={categories.length}
          icon={<Tags />}
          color="orange"
        />

        <StatCard
          title="Data Sources"
          value={sources.length}
          icon={<Database />}
          color="green"
        />

      </section>


      {/* Charts */}
      <section className="charts-grid">

        {/* City-wise Listings */}
        <div className="chart-card">

          <div className="card-heading">
            <div>
              <h3>City-wise Listings</h3>
              <p>Top 10 cities by number of listings</p>
            </div>
          </div>

          {cityChartData.length === 0 ? (

            <EmptyState />

          ) : (

            <div className="chart-container city-chart">

              <ResponsiveContainer width="100%" height="100%">

                <BarChart
                  data={cityChartData}
                  layout="vertical"
                  margin={{
                    top: 15,
                    right: 25,
                    bottom: 15,
                    left: 5,
                  }}
                  barCategoryGap="35%"
                >

                  <CartesianGrid
                    strokeDasharray="3 3"
                    horizontal={false}
                  />

                  <XAxis
                    type="number"
                    allowDecimals={false}
                    tick={{ fontSize: 11 }}
                    axisLine={false}
                  />

                  <YAxis
                    type="category"
                    dataKey="city"
                    width={125}
                    tick={{ fontSize: 12 }}
                    axisLine={false}
                    tickLine={false}
                  />

                  <Tooltip
                    cursor={false}
                    formatter={(value) => [
                      numberFormat(value),
                      'Listings',
                    ]}
                  />

                  <Bar
                    dataKey="total"
                    name="Listings"
                    fill="#6366f1"
                    radius={[0, 6, 6, 0]}
                    barSize={28}
                  />

                </BarChart>

              </ResponsiveContainer>

            </div>

          )}

        </div>


        {/* Category Distribution */}
        <div className="chart-card">

          <div className="card-heading">
            <div>
              <h3>Category Distribution</h3>
              <p>Top 8 categories and all remaining categories</p>
            </div>
          </div>

          {categoryChartData.length === 0 ? (

            <EmptyState />

          ) : (

            <div className="chart-container category-chart">

              <ResponsiveContainer width="100%" height="100%">

                <PieChart>

                  <Pie
                    data={categoryChartData}
                    dataKey="total"
                    nameKey="category"
                    cx="50%"
                    cy="44%"
                    outerRadius={105}
                    innerRadius={48}
                    paddingAngle={2}
                    label={false}
                  >

                    {categoryChartData.map((entry, index) => (

                      <Cell
                        key={entry.category}
                        fill={COLORS[index % COLORS.length]}
                      />

                    ))}

                  </Pie>

                  <Tooltip
                    formatter={(value) => [
                      numberFormat(value),
                      'Listings',
                    ]}
                  />

                  <Legend
                    verticalAlign="bottom"
                    height={65}
                    wrapperStyle={{ fontSize: '11px' }}
                  />

                </PieChart>

              </ResponsiveContainer>

            </div>

          )}

        </div>


        {/* Source-wise Listings */}
        <div className="chart-card full-width">

          <div className="card-heading">
            <div>
              <h3>Source-wise Listings</h3>
              <p>Number of listings collected from each source</p>
            </div>
          </div>

          {sortedSources.length === 0 ? (

            <EmptyState />

          ) : (

            <div className="chart-container source-chart">

              <ResponsiveContainer width="100%" height="100%">

                <BarChart
                  data={sortedSources}
                  layout="vertical"
                  margin={{
                    top: 5,
                    right: 25,
                    bottom: 5,
                    left: 5,
                  }}
                >

                  <CartesianGrid
                    strokeDasharray="3 3"
                    horizontal={false}
                  />

                  <XAxis
                    type="number"
                    allowDecimals={false}
                    tick={{ fontSize: 12 }}
                    axisLine={false}
                  />

                  <YAxis
                    type="category"
                    dataKey="source"
                    width={140}
                    tick={{ fontSize: 12 }}
                    axisLine={false}
                    tickLine={false}
                  />

                  <Tooltip
                    cursor={false}
                    formatter={(value) => [
                      numberFormat(value),
                      'Listings',
                    ]}
                  />

                  <Bar
                    dataKey="total"
                    name="Listings"
                    fill="#06b6d4"
                    radius={[0, 6, 6, 0]}
                    barSize={24}
                  />

                </BarChart>

              </ResponsiveContainer>

            </div>

          )}

        </div>

      </section>


      {/* Listings Explorer */}
      <ListingsExplorer />


      {/* Footer */}
      <footer>

        <p>
          Business Insights Dashboard · Powered by React, FastAPI and MySQL
        </p>

        <p>
          Data source: OpenStreetMap contributors ·{' '}
          <a
            href="https://www.openstreetmap.org/copyright"
            target="_blank"
            rel="noreferrer"
          >
            ODbL attribution
          </a>
        </p>

      </footer>

    </main>
  )
}


/* Reusable KPI Card */
function StatCard({ title, value, icon, color }) {

  return (

    <div className="stat-card">

      <div className={`stat-icon ${color}`}>
        {icon}
      </div>

      <div className="stat-content">
        <p>{title}</p>
        <h2>{numberFormat(value)}</h2>
      </div>

    </div>

  )
}


/* Empty Chart State */
function EmptyState() {

  return (

    <div className="empty-state">
      No data available yet.
    </div>

  )

}


export default App
