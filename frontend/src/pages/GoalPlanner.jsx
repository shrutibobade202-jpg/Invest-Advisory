
import { useState } from "react";
import { calculateGoal, getGoalAdvice } from "../services/api";
import "./GoalPlanner.css";

export default function GoalPlanner() {
  const [goal, setGoal] = useState("Buy a car");
  const [targetAmount, setTargetAmount] = useState("500000");
  const [months, setMonths] = useState("24");
  const [result, setResult] = useState(null);
  const [advice, setAdvice] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  async function handleCalculate(event) {
    event.preventDefault();
    setError("");
    setResult(null);
    setAdvice("");

    const amount = Number(targetAmount);
    const duration = Number(months);

    if (
      !goal.trim() ||
      !Number.isFinite(amount) ||
      amount <= 0 ||
      !Number.isInteger(duration) ||
      duration <= 0
    ) {
      setError(
        "Enter a goal, a positive target amount, and a whole number of months."
      );
      return;
    }

    setLoading(true);

    try {
      const calculation = await calculateGoal(
        goal.trim(),
        amount,
        duration
      );

      setResult(calculation);

      try {
        const adviceResult = await getGoalAdvice(
          goal.trim(),
          amount,
          duration
        );

        setAdvice(
          typeof adviceResult === "string"
            ? adviceResult
            : adviceResult?.advice || adviceResult?.message || ""
        );
      } catch {
        setAdvice(
          "Goal advice is temporarily unavailable. Your calculation is still available."
        );
      }
    } catch (err) {
      setError(
        err.response?.data?.detail ||
          err.message ||
          "Unable to calculate your goal. Please check the backend connection."
      );
    } finally {
      setLoading(false);
    }
  }

  const monthlyAmount = result
    ? Number(
        result.monthly_saving_required ??
          result.monthly_saving ??
          result.monthly_savings ??
          result.monthly_amount ??
          result.monthly_required ??
          result.monthly_investment ??
          Number(targetAmount) / Number(months)
      )
    : 0;

  return (
    <main className="goal-planner-page">
      <section className="goal-planner-content">
        <header className="goal-planner-header">
          <h1>Goal Planner</h1>
          <p>
            Turn your financial dreams into achievable goals.
            Plan how much you need to save each month.
          </p>
          <p className="goal-planner-disclaimer">
            <strong>Educational information only.</strong>{" "}
            This estimate is not personalized financial advice.
          </p>
        </header>

        <form className="goal-planner-form" onSubmit={handleCalculate}>
          <div className="goal-form-field">
            <label htmlFor="goal">Your Financial Goal</label>
            <input
              id="goal"
              type="text"
              value={goal}
              onChange={(event) => setGoal(event.target.value)}
              placeholder="e.g. Buy a car"
              required
            />
          </div>

          <div className="goal-form-field">
            <label htmlFor="targetAmount">Target Amount (₹)</label>
            <input
              id="targetAmount"
              type="number"
              min="1"
              value={targetAmount}
              onChange={(event) => setTargetAmount(event.target.value)}
              required
            />
          </div>

          <div className="goal-form-field">
            <label htmlFor="months">Time to Reach Goal (months)</label>
            <input
              id="months"
              type="number"
              min="1"
              step="1"
              value={months}
              onChange={(event) => setMonths(event.target.value)}
              required
            />
          </div>

          <button type="submit" disabled={loading}>
            {loading ? "Calculating..." : "Calculate My Goal"}
          </button>
        </form>

        {error && (
          <div className="goal-planner-error" role="alert">
            {error}
          </div>
        )}

        {result && (
          <section className="goal-result" aria-live="polite">
            <h2>Your Goal Plan</h2>
            <p>
              <strong>Goal:</strong> {goal}
            </p>
            <p>
              <strong>Target Amount:</strong>{" "}
              ₹{Number(targetAmount).toLocaleString("en-IN")}
            </p>
            <p>
              <strong>Time Available:</strong> {months} months
            </p>

            <div className="monthly-savings-card">
              <p>Estimated Monthly Savings</p>
              <h3>
                ₹
                {monthlyAmount.toLocaleString("en-IN", {
                  minimumFractionDigits: 2,
                  maximumFractionDigits: 2,
                })}
              </h3>
              <p>
                This estimate divides your target amount by the number
                of months and does not assume investment returns.
              </p>
            </div>

            {advice && (
              <div className="goal-advice">
                <h3>Goal Advice</h3>
                <p>{advice}</p>
              </div>
            )}
          </section>
        )}
      </section>
    </main>
  );
}
