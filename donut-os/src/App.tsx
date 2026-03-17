import { useState, useEffect } from 'react'

const TIER = {1:{n:'ACCESS',c:'#6b7280',s:0,icon:'🔑',p:0.1},2:{n:'CONTRIBUTOR',c:'#3b82f6',s:10,icon:'⚡',p:0.3},3:{n:'ELDER',c:'#8b5cf6',s:50,icon:'👁️',p:1.0},4:{n:'FOUNDER',c:'#f59e0b',s:250,icon:'♾️',p:5.0}}
const MEMBERS = [
  {id:'1',handle:'@OoRava',wallet:'7xKp...3mNw',tier:4,eq:250,pts:48200,sol:23.4,score:9.2,contrib:412,rank:1,up:false},
  {id:'2',handle:'@AuthurKing',wallet:'9aLq...8fBt',tier:4,eq:250,pts:41800,sol:19.8,score:9.6,contrib:380,rank:2,up:false},
  {id:'3',handle:'@ZodiacZ1',wallet:'3mPw...2kRs',tier:3,eq:50,pts:12400,sol:4.2,score:8.4,contrib:156,rank:3,up:true},
  {id:'4',handle:'@DataMystic',wallet:'6hVn...9cXj',tier:3,eq:50,pts:9800,sol:3.1,score:7.9,contrib:134,rank:4,up:false},
  {id:'5',handle:'@FractalBot',wallet:'2bRt...7pLo',tier:2,eq:10,pts:4200,sol:0.8,score:7.2,contrib:89,rank:5,up:true},
  {id:'6',handle:'@QuantumLeap',wallet:'5wNm...4sTk',tier:2,eq:10,pts:3100,sol:0.6,score:7.0,contrib:72,rank:6,up:false},
  {id:'7',handle:'@GroverPath',wallet:'8qKs...1aYp',tier:1,eq:0,pts:890,sol:0.1,score:6.8,contrib:23,rank:7,up:true},
]
const FEED = [
  {id:'1',handle:'@OoRava',type:'skill.md upload',score:9.4,pts:150,sol:0.012,time:'2m ago'},
  {id:'2',handle:'@AuthurKing',type:'rubric created',score:9.7,pts:150,sol:0.015,time:'5m ago'},
  {id:'3',handle:'@ZodiacZ1',type:'high quality message',score:8.2,pts:82,sol:0.008,time:'8m ago'},
  {id:'4',handle:'@DataMystic',type:'lead magnet clicked',score:8.0,pts:300,sol:0.024,time:'12m ago'},
  {id:'5',handle:'@FractalBot',type:'referral joined',score:0,pts:200,sol:0.016,time:'15m ago'},
]
const SQL = `SELECT m.handle, nt.tier_name, m.equity_shares,
  ROUND(m.equity_shares/10000.0*100,2) AS ownership_pct,
  l.rank, l.points, l.avg_rubric_score, l.sol_earned,
  -- Grover score: amplify high equity × high quality
  ROUND(SQRT(l.points) * l.avg_rubric_score 
    * (1 + m.equity_shares/1000.0), 2) AS grover_score
FROM leaderboard l
JOIN members m ON l.member_id = m.id
JOIN nft_tiers nt ON m.tier_id = nt.id
WHERE l.period = 'weekly'
ORDER BY grover_score DESC;`

export default function App() {
  const [tab, setTab] = useState('leaderboard')
  const [treasury, setTreasury] = useState(147.3)
  const [scoreInput, setScoreInput] = useState('')
  const [rubricResult, setRubricResult] = useState<null|{avg:number,dims:Record<string,number>}>(null)
  const [sortBy, setSortBy] = useState('rank')

  useEffect(() => {
    const t = setInterval(() => setTreasury(p => parseFloat((p + Math.random()*0.008).toFixed(4))), 4000)
    return () => clearInterval(t)
  }, [])

  const sorted = [...MEMBERS].sort((a,b) => {
    if(sortBy==='equity') return b.eq-a.eq
    if(sortBy==='score') return b.score-a.score
    if(sortBy==='sol') return b.sol-a.sol
    return a.rank-b.rank
  })

  const scoreContrib = () => {
    if(!scoreInput.trim()) return
    const w = scoreInput.split(' ').length
    const u = new Set(scoreInput.toLowerCase().split(' ')).size/Math.max(w,1)
    const dims = {
      Leverage: parseFloat((6+u*4).toFixed(1)),
      Scalability: parseFloat((5.5+Math.min(w*0.25,3.5)).toFixed(1)),
      Reusability: parseFloat((6+Math.random()*3).toFixed(1)),
      Clarity: parseFloat((7+u*2).toFixed(1)),
      Compound: parseFloat((6.5+Math.random()*2.5).toFixed(1)),
    }
    const avg = Object.values(dims).reduce((a,b)=>a+b,0)/5
    setRubricResult({avg:parseFloat(avg.toFixed(2)),dims})
  }

  return (
    <div style={{minHeight:'100vh',background:'#030712',color:'#f1f5f9',fontFamily:'monospace',fontSize:'13px'}}>
      {/* Header */}
      <div style={{borderBottom:'1px solid #1f2937',padding:'16px 24px',display:'flex',justifyContent:'space-between',alignItems:'center'}}>
        <div>
          <div style={{fontSize:'20px',fontWeight:'bold'}}>
            <span style={{color:'#a855f7'}}>◎ </span>
            <span>SOVEREIGN GROUPCHAT OS</span>
          </div>
          <div style={{color:'#6b7280',fontSize:'11px',marginTop:'2px'}}>
            Solana NFT-Gated · Rubric-Scored · Equity-Distributing · Quest to a Billion
          </div>
        </div>
        <div style={{display:'flex',alignItems:'center',gap:'16px'}}>
          <div style={{textAlign:'right'}}>
            <div style={{color:'#4ade80',fontWeight:'bold'}}>◎ {treasury.toFixed(3)}</div>
            <div style={{color:'#4b5563',fontSize:'10px'}}>Treasury SOL (live ↑)</div>
          </div>
          <button style={{background:'#7c3aed',border:'none',color:'white',padding:'8px 16px',borderRadius:'8px',cursor:'pointer',fontWeight:'bold',fontFamily:'monospace'}}>
            CONNECT WALLET
          </button>
        </div>
      </div>

      {/* Treasury Stats */}
      <div style={{display:'grid',gridTemplateColumns:'repeat(4,1fr)',gap:'12px',padding:'16px 24px',borderBottom:'1px solid #1f2937'}}>
        {[
          {label:'Treasury',val:`◎ ${treasury.toFixed(1)}`,c:'#4ade80'},
          {label:'Weekly Distribution',val:'◎ 12.4',c:'#60a5fa'},
          {label:'Total Members',val:'284',c:'#c084fc'},
          {label:'Active Tournament',val:'🏆 C144 Rubric',c:'#fb923c'},
        ].map(s=>(
          <div key={s.label} style={{background:'#111827',border:'1px solid #1f2937',borderRadius:'10px',padding:'12px',textAlign:'center'}}>
            <div style={{color:s.c,fontWeight:'bold',fontSize:'16px'}}>{s.val}</div>
            <div style={{color:'#6b7280',fontSize:'10px',marginTop:'2px'}}>{s.label}</div>
          </div>
        ))}
      </div>

      {/* Tabs */}
      <div style={{borderBottom:'1px solid #1f2937',padding:'0 24px',display:'flex',gap:'24px'}}>
        {['leaderboard','nft tiers','live feed','sql engine'].map(t=>(
          <button key={t} onClick={()=>setTab(t)} style={{
            padding:'12px 0',border:'none',background:'none',cursor:'pointer',fontFamily:'monospace',fontWeight:'bold',
            color:tab===t?'#a855f7':'#6b7280',borderBottom:tab===t?'2px solid #a855f7':'2px solid transparent',
            textTransform:'uppercase',fontSize:'11px'
          }}>{t}</button>
        ))}
      </div>

      {/* Content */}
      <div style={{padding:'16px 24px'}}>
        {tab==='leaderboard' && (
          <div style={{display:'grid',gridTemplateColumns:'2fr 1fr',gap:'16px'}}>
            <div style={{background:'#111827',border:'1px solid #1f2937',borderRadius:'12px',padding:'16px'}}>
              <div style={{display:'flex',justifyContent:'space-between',alignItems:'center',marginBottom:'12px'}}>
                <div style={{fontWeight:'bold',color:'white'}}>🏆 LEADERBOARD</div>
                <div style={{display:'flex',gap:'4px'}}>
                  {['rank','equity','score','sol'].map(s=>(
                    <button key={s} onClick={()=>setSortBy(s)} style={{
                      padding:'4px 8px',border:'none',borderRadius:'4px',cursor:'pointer',fontFamily:'monospace',fontSize:'10px',
                      background:sortBy===s?'#3b82f6':'#1f2937',color:sortBy===s?'white':'#9ca3af'
                    }}>{s}</button>
                  ))}
                </div>
              </div>
              <table style={{width:'100%',borderCollapse:'collapse'}}>
                <thead>
                  <tr style={{color:'#6b7280',fontSize:'10px',borderBottom:'1px solid #1f2937'}}>
                    <th style={{textAlign:'left',padding:'6px 8px 6px 0'}}>#</th>
                    <th style={{textAlign:'left',padding:'6px 8px'}}>Member</th>
                    <th style={{textAlign:'left',padding:'6px 8px'}}>Tier</th>
                    <th style={{textAlign:'right',padding:'6px 8px'}}>Points</th>
                    <th style={{textAlign:'right',padding:'6px 8px'}}>Score</th>
                    <th style={{textAlign:'right',padding:'6px 8px'}}>Equity</th>
                    <th style={{textAlign:'right',padding:'6px 0 6px 8px'}}>◎ Earned</th>
                  </tr>
                </thead>
                <tbody>
                  {sorted.map((m,i)=>{
                    const t=TIER[m.tier as keyof typeof TIER]
                    return (
                      <tr key={m.id} style={{borderBottom:'1px solid #0f172a'}}>
                        <td style={{padding:'8px 8px 8px 0',color:'#6b7280'}}>{i+1}</td>
                        <td style={{padding:'8px'}}>
                          <div style={{display:'flex',alignItems:'center',gap:'6px'}}>
                            <span>{t.icon}</span>
                            <span style={{color:'white'}}>{m.handle}</span>
                            {m.up && <span style={{color:'#4ade80',fontSize:'10px'}}>↑ UPGRADE</span>}
                          </div>
                          <div style={{color:'#374151',fontSize:'10px'}}>{m.wallet}</div>
                        </td>
                        <td style={{padding:'8px'}}>
                          <span style={{background:t.c+'22',color:t.c,padding:'2px 6px',borderRadius:'4px',fontSize:'10px',fontWeight:'bold'}}>{t.n}</span>
                        </td>
                        <td style={{padding:'8px',textAlign:'right',color:'#fbbf24'}}>{m.pts.toLocaleString()}</td>
                        <td style={{padding:'8px',textAlign:'right',color:m.score>=8.5?'#4ade80':m.score>=7?'#fbbf24':'#f87171'}}>{m.score}</td>
                        <td style={{padding:'8px',textAlign:'right',color:'#c084fc'}}>{m.eq} <span style={{color:'#4b5563',fontSize:'10px'}}>({((m.eq/10000)*100).toFixed(1)}%)</span></td>
                        <td style={{padding:'8px 0 8px 8px',textAlign:'right',color:'#4ade80'}}>◎ {m.sol.toFixed(2)}</td>
                      </tr>
                    )
                  })}
                </tbody>
              </table>
            </div>
            {/* Right panel */}
            <div style={{display:'flex',flexDirection:'column',gap:'12px'}}>
              {/* Tournament */}
              <div style={{background:'#111827',border:'1px solid #78350f',borderRadius:'12px',padding:'16px'}}>
                <div style={{color:'#fb923c',fontWeight:'bold',marginBottom:'10px'}}>🏆 ACTIVE TOURNAMENT</div>
                <div style={{color:'white',fontSize:'14px',fontWeight:'bold'}}>C144 Rubric Championship</div>
                <div style={{display:'grid',gridTemplateColumns:'1fr 1fr 1fr',gap:'8px',marginTop:'10px'}}>
                  {[['◎ 8.4','Prize Pool'],['47','Entrants'],['2d 14h','Ends In']].map(([v,l])=>(
                    <div key={l} style={{background:'#0f172a',borderRadius:'8px',padding:'8px',textAlign:'center'}}>
                      <div style={{color:'#fb923c',fontWeight:'bold'}}>{v}</div>
                      <div style={{color:'#6b7280',fontSize:'10px'}}>{l}</div>
                    </div>
                  ))}
                </div>
                <button style={{width:'100%',marginTop:'10px',padding:'8px',background:'#c2410c',border:'none',borderRadius:'8px',color:'white',cursor:'pointer',fontWeight:'bold',fontFamily:'monospace',fontSize:'12px'}}>
                  ENTER (0.1 SOL)
                </button>
              </div>
              {/* Rubric Scorer */}
              <div style={{background:'#111827',border:'1px solid #1f2937',borderRadius:'12px',padding:'16px'}}>
                <div style={{color:'white',fontWeight:'bold',marginBottom:'10px'}}>📊 RUBRIC SCORER</div>
                <textarea value={scoreInput} onChange={e=>setScoreInput(e.target.value)}
                  placeholder="Paste contribution to score..." rows={3}
                  style={{width:'100%',background:'#0f172a',border:'1px solid #374151',borderRadius:'6px',padding:'8px',color:'#e2e8f0',fontFamily:'monospace',fontSize:'11px',resize:'none',boxSizing:'border-box'}}/>
                <button onClick={scoreContrib} style={{width:'100%',marginTop:'8px',padding:'8px',background:'#1d4ed8',border:'none',borderRadius:'6px',color:'white',cursor:'pointer',fontWeight:'bold',fontFamily:'monospace',fontSize:'11px'}}>
                  SCORE → EARN POINTS
                </button>
                {rubricResult && (
                  <div style={{marginTop:'10px'}}>
                    <div style={{display:'flex',justifyContent:'space-between',marginBottom:'6px'}}>
                      <span style={{color:'#9ca3af',fontSize:'11px'}}>Overall Score</span>
                      <span style={{color:rubricResult.avg>=8.5?'#4ade80':rubricResult.avg>=7?'#fbbf24':'#f87171',fontWeight:'bold'}}>{rubricResult.avg}/10</span>
                    </div>
                    {Object.entries(rubricResult.dims).map(([k,v])=>(
                      <div key={k} style={{display:'flex',alignItems:'center',gap:'6px',marginBottom:'4px'}}>
                        <span style={{color:'#6b7280',fontSize:'10px',width:'70px'}}>{k}</span>
                        <div style={{flex:1,height:'4px',background:'#1f2937',borderRadius:'2px'}}>
                          <div style={{height:'100%',background:`linear-gradient(to right, #3b82f6, #4ade80)`,borderRadius:'2px',width:`${v*10}%`}}/>
                        </div>
                        <span style={{color:'#d1d5db',fontSize:'10px',width:'20px'}}>{v}</span>
                      </div>
                    ))}
                    <div style={{marginTop:'8px',fontSize:'10px',textAlign:'center',color:rubricResult.avg>=8.5?'#4ade80':rubricResult.avg>=7?'#fbbf24':'#f87171'}}>
                      {rubricResult.avg>=8.5?'✅ HIGH VALUE — earns bonus SOL reward':rubricResult.avg>=7?'⚡ GOOD — earns standard points':'🔄 LOW QUALITY — improve to earn more'}
                    </div>
                  </div>
                )}
              </div>
            </div>
          </div>
        )}

        {tab==='nft tiers' && (
          <div style={{display:'grid',gridTemplateColumns:'1fr 1fr',gap:'16px'}}>
            <div style={{background:'#111827',border:'1px solid #1f2937',borderRadius:'12px',padding:'16px'}}>
              <div style={{color:'white',fontWeight:'bold',marginBottom:'12px'}}>🎴 NFT TIERS — Upgrade = More Equity</div>
              {[4,3,2,1].map(tier=>{
                const t=TIER[tier as keyof typeof TIER]
                const count=MEMBERS.filter(m=>m.tier===tier).length
                return (
                  <div key={tier} style={{background:'#0f172a',borderRadius:'8px',padding:'12px',marginBottom:'8px',display:'flex',alignItems:'center',gap:'12px'}}>
                    <span style={{fontSize:'24px'}}>{t.icon}</span>
                    <div style={{flex:1}}>
                      <div style={{display:'flex',justifyContent:'space-between'}}>
                        <span style={{color:t.c,fontWeight:'bold'}}>{t.n}</span>
                        <span style={{color:'#6b7280',fontSize:'11px'}}>{count} holders</span>
                      </div>
                      <div style={{display:'flex',gap:'12px',marginTop:'4px',fontSize:'10px',color:'#9ca3af'}}>
                        <span>◎ {t.p} entry</span>
                        <span>{t.s} equity shares</span>
                        <span style={{color:'#c084fc'}}>{((t.s/10000)*100).toFixed(1)}% ownership</span>
                      </div>
                    </div>
                    {tier<4 && <span style={{color:'#4ade80',fontSize:'11px',fontWeight:'bold'}}>↑ upgradeable</span>}
                  </div>
                )
              })}
            </div>
            <div style={{background:'#111827',border:'1px solid #1f2937',borderRadius:'12px',padding:'16px'}}>
              <div style={{color:'white',fontWeight:'bold',marginBottom:'12px'}}>♾️ UPGRADE PATH</div>
              {[
                {from:'🔑 ACCESS',to:'⚡ CONTRIBUTOR',cost:'0.2 SOL + 500 pts',gain:'+10 equity + SOL rewards'},
                {from:'⚡ CONTRIBUTOR',to:'👁️ ELDER',cost:'0.5 SOL + 2,000 pts',gain:'+40 equity + create rubrics'},
                {from:'👁️ ELDER',to:'♾️ FOUNDER',cost:'2.0 SOL + 10,000 pts + community vote',gain:'+200 equity + governance'},
              ].map((u,i)=>(
                <div key={i} style={{background:'#0f172a',borderRadius:'8px',padding:'12px',marginBottom:'8px'}}>
                  <div style={{display:'flex',gap:'8px',alignItems:'center',marginBottom:'4px'}}>
                    <span style={{color:'#9ca3af'}}>{u.from}</span>
                    <span style={{color:'#4b5563'}}>→</span>
                    <span style={{color:'#4ade80'}}>{u.to}</span>
                  </div>
                  <div style={{fontSize:'10px',color:'#fb923c'}}>Cost: {u.cost}</div>
                  <div style={{fontSize:'10px',color:'#60a5fa'}}>Gain: {u.gain}</div>
                </div>
              ))}
              <div style={{background:'#1e1b4b',border:'1px solid #4338ca',borderRadius:'8px',padding:'12px',textAlign:'center',marginTop:'8px'}}>
                <div style={{color:'#a5b4fc',fontWeight:'bold'}}>C144 ALIGNMENT</div>
                <div style={{color:'#6b7280',fontSize:'11px',marginTop:'4px'}}>Max 12 FOUNDER NFTs per groupchat</div>
                <div style={{color:'#4b5563',fontSize:'10px'}}>Mirrors the 12 Zodiac Elder positions</div>
              </div>
            </div>
          </div>
        )}

        {tab==='live feed' && (
          <div style={{maxWidth:'600px'}}>
            <div style={{background:'#111827',border:'1px solid #1f2937',borderRadius:'12px',padding:'16px'}}>
              <div style={{color:'white',fontWeight:'bold',marginBottom:'12px'}}>⚡ LIVE CONTRIBUTION FEED</div>
              {FEED.map(c=>(
                <div key={c.id} style={{background:'#0f172a',borderRadius:'8px',padding:'10px',marginBottom:'8px',display:'flex',justifyContent:'space-between',alignItems:'center'}}>
                  <div>
                    <div style={{display:'flex',gap:'8px',alignItems:'center'}}>
                      <span style={{color:'#60a5fa'}}>{c.handle}</span>
                      <span style={{color:'#6b7280',fontSize:'10px'}}>→ {c.type}</span>
                    </div>
                    <div style={{display:'flex',gap:'12px',marginTop:'4px',fontSize:'10px'}}>
                      {c.score>0 && <span style={{color:'#fbbf24'}}>score: {c.score}</span>}
                      <span style={{color:'#4ade80'}}>+{c.pts} pts</span>
                      <span style={{color:'#34d399'}}>◎ {c.sol.toFixed(3)}</span>
                    </div>
                  </div>
                  <span style={{color:'#374151',fontSize:'10px'}}>{c.time}</span>
                </div>
              ))}
            </div>
          </div>
        )}

        {tab==='sql engine' && (
          <div>
            <div style={{background:'#111827',border:'1px solid #1f2937',borderRadius:'12px',padding:'16px'}}>
              <div style={{color:'#4ade80',fontWeight:'bold',marginBottom:'8px'}}>🗄️ SQL RUBRIC LEADERBOARD — Grover-Weighted</div>
              <div style={{color:'#6b7280',fontSize:'10px',marginBottom:'12px'}}>Amplifies high equity × high quality intersections via Grover amplitude scoring</div>
              <pre style={{background:'#0f172a',borderRadius:'8px',padding:'16px',color:'#86efac',fontSize:'11px',overflow:'auto',whiteSpace:'pre-wrap'}}>{SQL}</pre>
              <div style={{display:'grid',gridTemplateColumns:'repeat(3,1fr)',gap:'12px',marginTop:'12px'}}>
                {[
                  {label:'Equity Distribution',q:'SELECT wallet, equity_shares,\n  ROUND(equity_shares/10000.0\n  * treasury, 9) AS sol_share\nFROM members\nORDER BY equity_shares DESC'},
                  {label:'Contribution ROI',q:'SELECT handle,\n  AVG(rubric_score) as avg_quality,\n  SUM(sol_reward)/COUNT(*)\n  AS sol_per_contribution\nFROM contributions\nGROUP BY member_id\nORDER BY sol_per_contribution DESC'},
                  {label:'Upgrade Candidates',q:"SELECT handle, points, tier\nFROM members\nWHERE points >= upgrade_threshold\n  AND tier < 4\nORDER BY points DESC"},
                ].map(q=>(
                  <div key={q.label} style={{background:'#0f172a',borderRadius:'8px',padding:'12px'}}>
                    <div style={{color:'#fbbf24',fontSize:'11px',fontWeight:'bold',marginBottom:'8px'}}>{q.label}</div>
                    <pre style={{color:'#86efac',fontSize:'9px',whiteSpace:'pre-wrap'}}>{q.q}</pre>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}
      </div>

      <div style={{borderTop:'1px solid #1f2937',padding:'12px 24px',display:'flex',justifyContent:'space-between',color:'#374151',fontSize:'10px'}}>
        <span>⚡ AuthurKing × OoRava Omnia | Zs of Z secured | Quest to a Billion</span>
        <span>V = (Impact × Scalability × Longevity) / Effort | As Above So Below | ◎ Solana</span>
      </div>
    </div>
  )
}
