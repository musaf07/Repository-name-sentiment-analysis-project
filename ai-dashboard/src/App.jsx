import { useState } from "react";
import "chart.js/auto";
import { Line, Doughnut } from "react-chartjs-2";
import { motion } from "framer-motion";

export default function App() {
  const [stats, setStats] = useState({
    total: 0,
    Positive: 0,
    Negative: 0,
    Neutral: 0
  });

  const [confidence, setConfidence] = useState(0);
  const [sentiment, setSentiment] = useState("Neutral");
  const [feed, setFeed] = useState([]);
  const [text, setText] = useState("");

  // ✅ DEMO ANALYZE (no backend)
  const analyze = () => {
    const random = Math.random() * 100;

    const newSentiment =
      random > 60 ? "Positive" :
      random > 30 ? "Neutral" :
      "Negative";

    setConfidence(random);
    setSentiment(newSentiment);

    setStats(prev => ({
      total: prev.total + 1,
      Positive: newSentiment === "Positive" ? prev.Positive + 1 : prev.Positive,
      Negative: newSentiment === "Negative" ? prev.Negative + 1 : prev.Negative,
      Neutral: newSentiment === "Neutral" ? prev.Neutral + 1 : prev.Neutral
    }));

    setFeed(prev => [
      { text: text || "Sample text", sentiment: newSentiment },
      ...prev
    ]);

    setText("");
  };

  // 📊 LINE CHART (FIXED)
  const lineData = {
    labels: ["Jan", "Feb", "Mar", "Apr", "May"],
    datasets: [{
      label: "Sentiment Trend",
      data: [
        stats.Positive,
        stats.Negative,
        stats.Neutral,
        stats.total,
        confidence
      ],
      borderColor: "#a855f7",
      backgroundColor: "rgba(168,85,247,0.2)",
      tension: 0.4
    }]
  };

  const chartOptions = {
    plugins: {
      legend: {
        labels: { color: "white" }
      }
    },
    scales: {
      x: { ticks: { color: "white" } },
      y: { ticks: { color: "white" } }
    }
  };

  // 🥧 PIE CHART
  const pieData = {
    labels: ["Positive", "Negative", "Neutral"],
    datasets: [{
      data: [stats.Positive, stats.Negative, stats.Neutral],
      backgroundColor: ["#22c55e", "#ef4444", "#3b82f6"]
    }]
  };

  return (
    <div className="flex min-h-screen text-white bg-gradient-to-br from-[#0f172a] via-[#1e1b4b] to-[#020617]">

      {/* SIDEBAR */}
      <div className="w-60 p-5 bg-black/40 backdrop-blur-xl border-r border-white/10">
        <h2 className="text-xl mb-6">🚀 AI Panel</h2>
      </div>

      {/* MAIN */}
      <div className="flex-1 p-8">

        {/* KPI */}
        <div className="grid grid-cols-4 gap-5 mb-8">
          <Card title="Total" value={stats.total}/>
          <Card title="Positive" value={stats.Positive}/>
          <Card title="Negative" value={stats.Negative}/>
          <Card title="Neutral" value={stats.Neutral}/>
        </div>

        <div className="grid grid-cols-3 gap-6">

          {/* LEFT */}
          <div className="col-span-2 bg-[#020617] p-6 rounded-xl shadow-xl border border-purple-500/10">

            <h2 className="mb-4 text-lg">AI Performance Index</h2>
            <Line data={lineData} options={chartOptions}/>

            <textarea
              value={text}
              onChange={(e)=>setText(e.target.value)}
              className="w-full mt-5 p-3 bg-[#0f172a] rounded"
              placeholder="Enter text..."
            />

            <button
              onClick={analyze}
              className="w-full mt-3 bg-purple-600 hover:bg-purple-500 p-2 rounded"
            >
              Analyze
            </button>

          </div>

          {/* RIGHT */}
          <div className="space-y-6">

            <div className="bg-[#020617] p-5 rounded-xl shadow-xl border border-purple-500/10 text-center">
              <h3>AI Confidence</h3>
              <Gauge value={confidence} sentiment={sentiment}/>
            </div>

            <div className="bg-[#020617] p-5 rounded-xl shadow-xl border border-purple-500/10">
              <Doughnut data={pieData}/>
            </div>

          </div>
        </div>

        {/* FEED */}
        <div className="mt-6 bg-[#020617] p-5 rounded-xl shadow-xl border border-purple-500/10 h-48 overflow-auto">
          <h3 className="mb-3">Live Feed</h3>
          {feed.map((f,i)=>(
            <div key={i} className="border-b border-gray-700 py-2">
              {f.text} - {f.sentiment}
            </div>
          ))}
        </div>

      </div>
    </div>
  );
}

// 🔥 CARD
function Card({title,value}){
  return(
    <motion.div
      initial={{opacity:0,y:20}}
      animate={{opacity:1,y:0}}
      className="bg-[#020617] p-5 rounded-xl shadow-xl border border-purple-500/10"
    >
      <h3 className="text-gray-400">{title}</h3>
      <h1 className="text-2xl">{value}</h1>
    </motion.div>
  );
}

// ⚡ GAUGE
function Gauge({value,sentiment}){

  const color =
    sentiment==="Positive" ? "#22c55e" :
    sentiment==="Negative" ? "#ef4444" :
    "#3b82f6";

  return(
    <svg viewBox="0 0 200 100" className="w-full max-w-[250px] mx-auto">
      <path d="M10 90 A90 90 0 0 1 190 90"
        stroke="#1e293b" strokeWidth="15" fill="none"/>

      <path
        d="M10 90 A90 90 0 0 1 190 90"
        stroke={color}
        strokeWidth="15"
        fill="none"
        strokeDasharray="282"
        strokeDashoffset={282 - (value/100)*282}
        style={{transition:"1s"}}
      />

      <text x="50%" y="70%" textAnchor="middle" fill="white">
        {value.toFixed(1)}%
      </text>
    </svg>
  );
}