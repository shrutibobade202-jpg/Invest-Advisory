
import { BrowserRouter, Routes, Route } from "react-router-dom";
import "./App.css";

import Navbar from "./components/Navbar";
import GoalPlanner from "./pages/GoalPlanner";
import Chat from "./pages/Chat";
import MutualFunds from "./pages/MutualFunds";

function Home() {
  return (
    <main className="home-page">
      <h1>Welcome to GoalInvest Advisor</h1>
      <h2>Your AI-Powered Personal Finance Assistant</h2>
      <p>
        Understand finance, plan your goals, and learn about investments with AI.
      </p>
    </main>
  );
}

function About() {
  return (
    <main className="about-page">
      <h1>About GoalInvest Advisor</h1>
      <p>
        Learn financial concepts and plan your future with educational AI tools.
      </p>
    </main>
  );
}

export default function App() {
  return (
    <BrowserRouter>
      <div className="app-layout">
        <Navbar />

        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/chat" element={<Chat />} />
          <Route path="/goal-planner" element={<GoalPlanner />} />
          <Route path="/mutual-funds" element={<MutualFunds />} />
          <Route path="/about" element={<About />} />
        </Routes>
      </div>
    </BrowserRouter>
  );
}
