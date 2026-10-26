
const API_BASE_URL = "https://invest-advisory-api.onrender.com";

// Helper function for API requests
async function apiRequest(endpoint, options = {}) {
  const response = await fetch(`${API_BASE_URL}${endpoint}`, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...options.headers,
    },
  });

  if (!response.ok) {
    const errorText = await response.text();
    throw new Error(
      `API request failed (${response.status}): ${
        errorText || response.statusText
      }`
    );
  }

  return response.json();
}

// AI Assistant
export async function chatWithAI(message) {
  return apiRequest("/chat", {
    method: "POST",
    body: JSON.stringify({ message }),
  });
}

// Goal Calculator
export async function calculateGoal(goal, target_amount, months) {
  return apiRequest("/calculate-goal", {
    method: "POST",
    body: JSON.stringify({
      goal,
      target_amount: Number(target_amount),
      months: Number(months),
    }),
  });
}

// Goal Advice
export async function getGoalAdvice(goal, target_amount, months) {
  return apiRequest("/goal-advice", {
    method: "POST",
    body: JSON.stringify({
      goal,
      target_amount: Number(target_amount),
      months: Number(months),
    }),
  });
}

// Mutual Funds
export async function getMutualFunds() {
  return apiRequest("/mutual-funds");
}
