
import { useEffect, useState } from "react";
import { getMutualFunds } from "../services/api";


export default function MutualFunds() {
  const [funds, setFunds] = useState([]);
  const [category, setCategory] = useState("");
  const [riskLevel, setRiskLevel] = useState("");
  const [search, setSearch] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  async function loadFunds(filters = {}) {
    setLoading(true);
    setError("");

    try {
      const data = await getMutualFunds(filters);
      setFunds(Array.isArray(data) ? data : data.funds || data.results || []);
    } catch (err) {
      setFunds([]);
      setError(
        err.response?.data?.detail ||
          err.message ||
          "Could not load mutual funds. Check that the backend and dataset are available."
      );
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadFunds();
  }, []);

  function handleSubmit(event) {
    event.preventDefault();

    const filters = {};
    if (category) filters.category = category;
    if (riskLevel) filters.risk_level = Number(riskLevel);
    if (search.trim()) filters.search = search.trim();

    loadFunds(filters);
  }

  return (
    <main className="mutual-funds-page">
      <h1>Explore Mutual Funds</h1>
      <p>
        Explore the available mutual fund dataset and compare funds by
        category, risk level, and historical performance.
      </p>
      <p>
        <strong>Educational information only.</strong> Historical returns
        do not guarantee future performance.
      </p>

      <form onSubmit={handleSubmit}>
        <input
          type="search"
          placeholder="Search fund name..."
          value={search}
          onChange={(event) => setSearch(event.target.value)}
        />

        <select
          value={category}
          onChange={(event) => setCategory(event.target.value)}
        >
          <option value="">All Categories</option>
          <option value="Equity">Equity</option>
          <option value="Debt">Debt</option>
          <option value="Hybrid">Hybrid</option>
          <option value="Other">Other</option>
          <option value="Solution Oriented">Solution Oriented</option>
        </select>

        <select
          value={riskLevel}
          onChange={(event) => setRiskLevel(event.target.value)}
        >
          <option value="">All Risk Levels</option>
          <option value="1">Risk Level 1</option>
          <option value="2">Risk Level 2</option>
          <option value="3">Risk Level 3</option>
          <option value="4">Risk Level 4</option>
          <option value="5">Risk Level 5</option>
        </select>

        <button type="submit" disabled={loading}>
          {loading ? "Loading..." : "Search Funds"}
        </button>
      </form>

      {loading && <p>Loading mutual funds from the backend...</p>}

      {error && <p role="alert">{error}</p>}

      {!loading && !error && (
        <>
          <p>Funds loaded: {funds.length}</p>

          {funds.length === 0 ? (
            <p>No funds found. Try changing your filters.</p>
          ) : (
            <div className="funds-grid">
              {funds.map((fund, index) => (
                <article
                  className="fund-card"
                  key={`${fund.scheme_name || "fund"}-${index}`}
                >
                  <h3>{fund.scheme_name || "Unnamed Fund"}</h3>
                  <p>Category: {fund.category ?? "Not available"}</p>
                  <p>Risk Level: {fund.risk_level ?? "Not available"}</p>
                  <p>
                    Minimum SIP:{" "}
                    {fund.min_sip == null
                      ? "Not available"
                      : `₹${Number(fund.min_sip).toLocaleString("en-IN")}`}
                  </p>
                  <p>
                    Expense Ratio:{" "}
                    {fund.expense_ratio == null
                      ? "Not available"
                      : `${fund.expense_ratio}%`}
                  </p>
                  <p>
                    1-Year Returns:{" "}
                    {fund.returns_1yr == null
                      ? "Not available"
                      : `${fund.returns_1yr}%`}
                  </p>
                  <p>
                    3-Year Returns:{" "}
                    {fund.returns_3yr == null
                      ? "Not available"
                      : `${fund.returns_3yr}%`}
                  </p>
                  <p>
                    5-Year Returns:{" "}
                    {fund.returns_5yr == null
                      ? "Not available"
                      : `${fund.returns_5yr}%`}
                  </p>
                </article>
              ))}
            </div>
          )}
        </>
      )}
    </main>
  );
}
