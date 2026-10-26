
const API = axios.create({
  baseURL: import.meta.env.VITE_API_URL || "http://127.0.0.1:8000",
  headers: {
    "Content-Type": "application/json",
  },
});

import axios from "axios";

// AI Assistant
export const chatWithAI = async (message) => {
  const response = await API.post("/chat", { message });
  return response.data;
};

// Goal Calculator
export const calculateGoal = async (goal, target_amount, months) => {
  const response = await API.post("/calculate-goal", {
    goal,
    target_amount: Number(target_amount),
    months: Number(months),
  });
  return response.data;
};

// Goal Advice
export const getGoalAdvice = async (goal, target_amount, months) => {
  const response = await API.post("/goal-advice", {
    goal,
    target_amount: Number(target_amount),
    months: Number(months),
  });
  return response.data;
};

// Mutual Funds
export const getMutualFunds = async (params = {}) => {
  const response = await API.get("/mutual-funds", { params });
  return response.data;
};
