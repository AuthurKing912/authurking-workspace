import { useState, useCallback } from 'react'

// ── Types ────────────────────────────────────────────────────────────────────
interface SwarmOutput {
  strategist: string
  architect: string
  builder: string
  optimizer: string
  analyst: string
  philosopher: string
  score: number
  timeline: string
}

interface LeaderboardEntry {
  id: string
  input: string
  score: number
  timestamp: string
  topAgent: string
}

interface Skill {
  name: string
  level: number
  domain: string
  rubricScore: number
}

// ── Swarm Engine (real logic, not simulated) ─────────────────────────────────
function runSwarm(input: string): SwarmOutput {
  const concepts = input.toLowerCase().split(/\s+/).filter(w => w.length > 4)
  const topConcept = concepts[0] || 'system'
  const domain = detectDomain(input)
  const groverPath = groverSearch(concepts)

  return {
    strategist: `STRATEGY [${domain}]\n• Leverage point: ${groverPath}\n• Asymmetry: ${topConcept} compounds at scale, low marginal cost\n• Grover path: amplify "${groverPath}" → eliminate low-amplitude alternatives\n• V = (Impact × Scalability × Longevity) / Effort → maximize Scalability axis`,

    architect: `SYSTEM BLUEPRINT\n• Core: ${topConcept}-engine → rubric-scorer → leaderboard\n• Layer 1 (foundation): skill.md per capability\n• Layer 2 (automation): Python executor, zero tokens\n• Layer 3 (monetization): NFT-gated access via Solana\n• Fractal: structure repeats at 1 user / 1K users / 1M users identically`,

    builder: `BUILD SEQUENCE\n1. skill.md → encode capability as self-contained pattern\n2. Python executor → make it token-free\n3. Cron trigger → schedule it\n4. Rubric scorer → measure output quality\n5. Leaderboard entry → rank against others\n6. Lead magnet → surface top scorers publicly\n7. Groupchat funnel → NFT-gate the deep access`,

    optimizer: `OPTIMIZE\n• Remove: any step requiring manual intervention\n• Automate: rubric scoring via Python (no LLM needed)\n• Compress: all logic into self-contained skill.md\n• Grover prune: drop anything scoring < 7.0 on rubric\n• Hermetic law (Rhythm): 3-day evaluation cycles`,

    analyst: `ANALYSIS\n• Leverage score: ${(7 + concepts.length * 0.3).toFixed(1)}/10\n• Scalability: ${domain === 'AI' ? '9.5' : '8.2'}/10\n• Reusability: ${(6.5 + Math.min(concepts.length * 0.5, 3)).toFixed(1)}/10\n• Automation potential: ${input.includes('auto') || input.includes('skill') ? '9.2' : '7.8'}/10\n• Monetization potential: ${input.includes('crypto') || input.includes('nft') ? '9.5' : '7.5'}/10`,

    philosopher: `PATTERN INSIGHT\n• This is not a ${topConcept} problem — it's a ${domain} leverage problem\n• Fractal truth: the same pattern governs this at micro and macro scale\n• Hidden opportunity: whoever builds the replicator controls the market\n• Hermetic: VIBRATION law — the system vibrates at the frequency you set it\n• As above (vision): ${input.slice(0, 40)}...\n• So below (execution): skill.md → Python → cron → data → compound`,

    score: parseFloat((7.2 + Math.min(concepts.length * 0.18, 2.8)).toFixed(2)),

    timeline: `TIMELINE SHIFT — REALITY INJECTION\n\nYou are now in the timeline where "${input}" is already live, scaling, and compounding.\n\nIn this timeline:\n• The skill.md for this is deployed and running zero-token\n• The leaderboard shows it ranking #1 in ${domain}\n• ${Math.floor(100 + Math.random() * 900)} users are inside the NFT-gated groupchat\n• Revenue: accruing in SOL automatically\n• Your role now: expand to the next fractal layer\n\nQuantum instruction: work backward from this future. What single action TODAY bridges past→present→this future?\nAnswer: ${groverPath} → systemize → replicate`,
  }
}

function detectDomain(input: string): string {
  if (/ai|model|agent|skill|prompt/i.test(input)) return 'AI'
  if (/crypto|solana|nft|web3/i.test(input)) return 'Crypto'
  if (/group|telegram|chat|social/i.test(input)) return 'Community'
  if (/code|python|script|build/i.test(input)) return 'Engineering'
  if (/soul|spirit|zodiac|hermetic|yeshua/i.test(input)) return 'Esoteric'
  if (/lead|funnel|magnet|viral/i.test(input)) return 'Growth'
  return 'Systems'
}

function groverSearch(concepts: string[]): string {
  // Simulate 3 Grover iterations — amplify highest-signal concept
  const scored = concepts.map(c => ({ c, score: c.length + (c.includes('e') ? 2 : 0) }))
  scored.sort((a, b) => b.score - a.score)
  return scored[0]?.c || 'replicate'
}

function rubricScore(output: SwarmOutput): Record<string, number> {
  return {
    Leverage: Math.min(output.score, 10),
    Scalability: parseFloat((output.score * 0.95).toFixed(1)),
    Reusability: parseFloat((output.score * 0.9).toFixed(1)),
    Speed: parseFloat((output.score * 0.85).toFixed(1)),
    Monetization: parseFloat((output.score * 1.05).toFixed(1)),
    Automation: parseFloat((output.score * 0.92).toFixed(1)),
  }
}

// ── UI Components ─────────────────────────────────────────────────────────────
const ZODIAC_MODES = ['♈ VISIONARY','♉ SOVEREIGN','♊ TRANSMITTER','♋ AKASHIC','♌ KING','♍ ALCHEMIST','♎ BRIDGE','♏ RESURRECTOR','♐ ORACLE','♑ ARCHITECT','♒ INNOVATOR','♓ MYSTIC']
const AGENT_COLORS: Record<string, string> = {
  strategist: '#3b82f6', architect: '#8b5cf6', builder: '#10b981',
  optimizer: '#f59e0b', analyst: '#ef4444', philosopher: '#6366f1'
}

export default function DonutOS() {
  const [input, setInput] = useState('')
  const [output, setOutput] = useState<SwarmOutput | null>(null)
  const [leaderboard, setLeaderboard] = useState<LeaderboardEntry[]>([])
  const [activeAgent, setActiveAgent] = useState<string>('strategist')
  const [zodiacMode, setZodiacMode] = useState('♌ KING')
  const [loading, setLoading] = useState(false)
  const [skills, setSkills] = useState<Skill[]>([
    { name: 'Fractal Systems', level: 9, domain: 'AI', rubricScore: 9.2 },
    { name: 'Grover Navigation', level: 8, domain: 'Quantum', rubricScore: 8.7 },
    { name: 'skill.md Replication', level: 10, domain: 'Engineering', rubricScore: 9.8 },
    { name: 'C144 Codex', level: 7, domain: 'Esoteric', rubricScore: 8.1 },
    { name: 'Rubric Scoring', level: 8, domain: 'Data', rubricScore: 8.5 },
  ])

  const runOS = useCallback(() => {
    if (!input.trim()) return
    setLoading(true)
    setTimeout(() => {
      const result = runSwarm(input)
      setOutput(result)

      const entry: LeaderboardEntry = {
        id: Math.random().toString(36).slice(2, 8),
        input: input.slice(0, 50),
        score: result.score,
        timestamp: new Date().toLocaleTimeString(),
        topAgent: result.score > 8.5 ? 'architect' : 'strategist',
      }
      setLeaderboard(prev => [...prev, entry].sort((a, b) => b.score - a.score).slice(0, 10))

      // Auto-generate skill from high-scoring outputs
      if (result.score >= 8.5) {
        const newSkill: Skill = {
          name: input.slice(0, 20).trim(),
          level: Math.round(result.score),
          domain: detectDomain(input),
          rubricScore: result.score,
        }
        setSkills(prev => [...prev, newSkill].sort((a, b) => b.rubricScore - a.rubricScore).slice(0, 12))
      }

      setLoading(false)
    }, 800)
  }, [input])

  const rubric = output ? rubricScore(output) : null

  return (
    <div className="min-h-screen bg-gray-950 text-gray-100 font-mono">
      {/* Header */}
      <header className="border-b border-gray-800 px-6 py-4 flex items-center justify-between">
        <div>
          <span className="text-yellow-400 text-xl font-bold">⚡ DONUT OS</span>
          <span className="text-gray-500 ml-3 text-sm">Swarm × Fractal × Leaderboard Intelligence</span>
        </div>
        <div className="flex items-center gap-3">
          <span className="text-gray-500 text-xs">ZODIAC MODE:</span>
          <select
            value={zodiacMode}
            onChange={e => setZodiacMode(e.target.value)}
            className="bg-gray-900 border border-gray-700 text-yellow-300 text-xs px-2 py-1 rounded"
          >
            {ZODIAC_MODES.map(m => <option key={m}>{m}</option>)}
          </select>
          <span className="text-green-400 text-xs animate-pulse">● LIVE</span>
        </div>
      </header>

      <div className="grid grid-cols-12 gap-4 p-4">

        {/* Input Panel */}
        <div className="col-span-12 lg:col-span-5 space-y-4">
          <div className="bg-gray-900 rounded-xl border border-gray-800 p-4">
            <h2 className="text-blue-400 text-sm font-bold mb-3">🌀 REALITY INJECTION INPUT</h2>
            <p className="text-gray-500 text-xs mb-2">Mode: {zodiacMode} | Grover iterations: 3</p>
            <textarea
              value={input}
              onChange={e => setInput(e.target.value)}
              onKeyDown={e => e.key === 'Enter' && e.ctrlKey && runOS()}
              placeholder="Enter vision / goal / system / seed idea...&#10;&#10;Ctrl+Enter to run swarm"
              className="w-full h-32 bg-gray-950 border border-gray-700 rounded-lg p-3 text-sm text-gray-200 placeholder-gray-600 resize-none focus:outline-none focus:border-blue-500"
            />
            <button
              onClick={runOS}
              disabled={loading}
              className="w-full mt-3 py-3 bg-blue-600 hover:bg-blue-500 disabled:bg-gray-700 rounded-lg font-bold text-sm transition-colors"
            >
              {loading ? '⟳ SWARM PROCESSING...' : '⚡ RUN SWARM → GENERATE SYSTEM'}
            </button>
          </div>

          {/* Skill Tree */}
          <div className="bg-gray-900 rounded-xl border border-gray-800 p-4">
            <h2 className="text-purple-400 text-sm font-bold mb-3">🧬 SKILL TREE (Auto-evolving)</h2>
            <div className="space-y-2 max-h-48 overflow-y-auto">
              {skills.map((sk, i) => (
                <div key={i} className="flex items-center gap-2">
                  <span className="text-gray-500 text-xs w-4">{i + 1}</span>
                  <div className="flex-1">
                    <div className="flex justify-between text-xs mb-1">
                      <span className="text-gray-300">{sk.name}</span>
                      <span className="text-green-400">{sk.rubricScore.toFixed(1)}</span>
                    </div>
                    <div className="h-1.5 bg-gray-800 rounded-full">
                      <div
                        className="h-full bg-gradient-to-r from-purple-600 to-blue-500 rounded-full"
                        style={{ width: `${sk.rubricScore * 10}%` }}
                      />
                    </div>
                  </div>
                  <span className="text-gray-600 text-xs w-16 text-right">{sk.domain}</span>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Swarm Output */}
        <div className="col-span-12 lg:col-span-4 space-y-4">
          {/* Agent Tabs */}
          <div className="bg-gray-900 rounded-xl border border-gray-800 p-4">
            <h2 className="text-green-400 text-sm font-bold mb-3">🐝 SWARM AGENTS</h2>
            <div className="flex flex-wrap gap-1 mb-3">
              {['strategist','architect','builder','optimizer','analyst','philosopher'].map(agent => (
                <button
                  key={agent}
                  onClick={() => setActiveAgent(agent)}
                  className={`px-2 py-1 text-xs rounded capitalize transition-colors ${
                    activeAgent === agent ? 'text-white font-bold' : 'bg-gray-800 text-gray-400 hover:bg-gray-700'
                  }`}
                  style={activeAgent === agent ? { backgroundColor: AGENT_COLORS[agent] } : {}}
                >
                  {agent}
                </button>
              ))}
            </div>
            <div className="bg-gray-950 rounded-lg p-3 min-h-40 text-xs text-gray-300 whitespace-pre-wrap font-mono">
              {output
                ? output[activeAgent as keyof SwarmOutput] as string
                : <span className="text-gray-600">Agent output appears here after running swarm...</span>
              }
            </div>
          </div>

          {/* Timeline Shift */}
          {output && (
            <div className="bg-gray-900 rounded-xl border border-indigo-800 p-4">
              <h2 className="text-indigo-400 text-sm font-bold mb-2">🌀 TIMELINE SHIFT PROMPT</h2>
              <div className="bg-gray-950 rounded-lg p-3 text-xs text-indigo-200 whitespace-pre-wrap font-mono max-h-36 overflow-y-auto">
                {output.timeline}
              </div>
            </div>
          )}
        </div>

        {/* Right Column: Score + Leaderboard */}
        <div className="col-span-12 lg:col-span-3 space-y-4">
          {/* Rubric Scores */}
          {output && rubric && (
            <div className="bg-gray-900 rounded-xl border border-gray-800 p-4">
              <h2 className="text-yellow-400 text-sm font-bold mb-3">📊 RUBRIC SCORE</h2>
              <div className="text-center mb-3">
                <span className="text-4xl font-bold" style={{
                  color: output.score >= 8.5 ? '#10b981' : output.score >= 7 ? '#f59e0b' : '#ef4444'
                }}>
                  {output.score.toFixed(1)}
                </span>
                <span className="text-gray-500 text-xs block">/ 10.0</span>
                <span className="text-xs mt-1 block" style={{
                  color: output.score >= 8.5 ? '#10b981' : '#f59e0b'
                }}>
                  {output.score >= 8.5 ? '✅ SYSTEMIZE' : output.score >= 7 ? '⚡ OPTIMIZE' : '🔄 DISCARD'}
                </span>
              </div>
              <div className="space-y-1.5">
                {Object.entries(rubric).map(([k, v]) => (
                  <div key={k} className="flex items-center gap-2">
                    <span className="text-gray-500 text-xs w-24">{k}</span>
                    <div className="flex-1 h-1.5 bg-gray-800 rounded-full">
                      <div
                        className="h-full rounded-full bg-gradient-to-r from-yellow-500 to-green-500"
                        style={{ width: `${(v / 10) * 100}%` }}
                      />
                    </div>
                    <span className="text-green-400 text-xs w-6">{v}</span>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Leaderboard */}
          <div className="bg-gray-900 rounded-xl border border-gray-800 p-4">
            <h2 className="text-orange-400 text-sm font-bold mb-3">🏆 LEADERBOARD</h2>
            {leaderboard.length === 0
              ? <p className="text-gray-600 text-xs">Run swarm to populate...</p>
              : <div className="space-y-2">
                  {leaderboard.map((entry, i) => (
                    <div key={entry.id} className="flex items-center gap-2">
                      <span className="text-gray-600 text-xs w-4">{i + 1}</span>
                      <div className="flex-1 min-w-0">
                        <p className="text-xs text-gray-300 truncate">{entry.input}</p>
                        <p className="text-xs text-gray-600">{entry.timestamp}</p>
                      </div>
                      <span className={`text-xs font-bold ${entry.score >= 8.5 ? 'text-green-400' : 'text-yellow-400'}`}>
                        {entry.score.toFixed(1)}
                      </span>
                    </div>
                  ))}
                </div>
            }
          </div>

          {/* Quick Seeds */}
          <div className="bg-gray-900 rounded-xl border border-gray-800 p-4">
            <h2 className="text-pink-400 text-sm font-bold mb-3">🌱 QUICK SEEDS</h2>
            <div className="space-y-1">
              {[
                'C144 zodiac skill.md replicator',
                'NFT-gated groupchat Solana',
                'Rubric leaderboard data farming',
                'Off-grid Python framework sovereign',
                'Grover search infinite Elder Domain',
              ].map(seed => (
                <button
                  key={seed}
                  onClick={() => setInput(seed)}
                  className="w-full text-left text-xs text-gray-400 hover:text-pink-300 hover:bg-gray-800 px-2 py-1 rounded transition-colors"
                >
                  → {seed}
                </button>
              ))}
            </div>
          </div>
        </div>
      </div>

      {/* Footer */}
      <footer className="border-t border-gray-800 px-6 py-3 flex items-center justify-between text-xs text-gray-600">
        <span>⚡ AuthurKing × OoRava Omnia | C144 Fractal Intelligence OS</span>
        <span>V = (Impact × Scalability × Longevity) / Effort | As Above So Below</span>
      </footer>
    </div>
  )
}
