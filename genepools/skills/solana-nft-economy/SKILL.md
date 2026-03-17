# SKILL: SOLANA NFT-GATED GROUPCHAT ECONOMY
## The Complete Architecture: SQL + Gamification + Solana Native + Equity NFTs
**Version:** 1.0 | **Chapter:** 7 | **ROI:** Maximum (data + revenue + compound)

---

## THE UNIFIED VISION (From Quest to a Billion!! Data)

```
USER arrives → holds/buys NFT → enters groupchat
  → contributes data (messages, votes, rubric scores, content)
    → data earns POINTS on SQL leaderboard
      → points unlock: rank upgrades / equity NFT tiers / rewards
        → equity NFT = actual ownership share of groupchat revenue
          → groupchat revenue = subscriptions + data licensing + tournament fees
            → revenue distributed on-chain to NFT holders
              → holders recruit others → [LOOP: INFINITE COMPOUND]
```

---

## SQL DATABASE SCHEMA (The Spine)

```sql
-- CORE TABLES

CREATE TABLE groupchats (
    id UUID PRIMARY KEY,
    name VARCHAR(100),
    telegram_chat_id BIGINT UNIQUE,
    nft_mint_address VARCHAR(44),  -- Solana NFT collection
    created_at TIMESTAMP DEFAULT NOW(),
    total_members INT DEFAULT 0,
    treasury_sol DECIMAL(18,9) DEFAULT 0,
    rubric_id UUID REFERENCES rubrics(id),
    equity_total_shares INT DEFAULT 10000  -- 10,000 shares = 100%
);

CREATE TABLE nft_tiers (
    id UUID PRIMARY KEY,
    groupchat_id UUID REFERENCES groupchats(id),
    tier_name VARCHAR(50),  -- 'access' | 'contributor' | 'elder' | 'founder'
    tier_level INT,         -- 1=access, 2=contributor, 3=elder, 4=founder
    equity_shares INT,      -- shares owned at this tier
    price_sol DECIMAL(18,9),
    max_supply INT,
    current_supply INT DEFAULT 0,
    can_upgrade BOOLEAN DEFAULT TRUE,
    upgrade_cost_sol DECIMAL(18,9),
    upgrade_requirement_points INT
);

CREATE TABLE members (
    id UUID PRIMARY KEY,
    telegram_user_id BIGINT,
    wallet_address VARCHAR(44),  -- Solana wallet
    nft_mint VARCHAR(44),        -- their specific NFT
    tier_id UUID REFERENCES nft_tiers(id),
    groupchat_id UUID REFERENCES groupchats(id),
    joined_at TIMESTAMP DEFAULT NOW(),
    total_points INT DEFAULT 0,
    rank INT DEFAULT 0,
    equity_shares INT DEFAULT 0,
    sol_earned DECIMAL(18,9) DEFAULT 0
);

CREATE TABLE contributions (
    id UUID PRIMARY KEY,
    member_id UUID REFERENCES members(id),
    groupchat_id UUID REFERENCES groupchats(id),
    contribution_type VARCHAR(50), -- 'message'|'rubric_score'|'data_upload'|'skill_md'|'lead_magnet'|'referral'
    content_hash VARCHAR(64),      -- IPFS hash of content
    rubric_score DECIMAL(4,2),     -- 0.00-10.00
    points_earned INT,
    sol_reward DECIMAL(18,9),
    timestamp TIMESTAMP DEFAULT NOW(),
    verified BOOLEAN DEFAULT FALSE
);

CREATE TABLE rubrics (
    id UUID PRIMARY KEY,
    name VARCHAR(100),
    domain VARCHAR(50),
    version INT DEFAULT 1,
    dimensions JSON,  -- [{name, weight, description}]
    created_by UUID REFERENCES members(id),
    avg_score DECIMAL(4,2),
    total_evaluations INT DEFAULT 0
);

CREATE TABLE leaderboard (
    id UUID PRIMARY KEY,
    groupchat_id UUID REFERENCES groupchats(id),
    member_id UUID REFERENCES members(id),
    period VARCHAR(20),  -- 'daily'|'weekly'|'monthly'|'alltime'
    rank INT,
    points INT,
    sol_earned DECIMAL(18,9),
    contribution_count INT,
    avg_rubric_score DECIMAL(4,2),
    calculated_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE tournaments (
    id UUID PRIMARY KEY,
    groupchat_id UUID REFERENCES groupchats(id),
    name VARCHAR(100),
    entry_fee_sol DECIMAL(18,9),
    prize_pool_sol DECIMAL(18,9),
    rubric_id UUID REFERENCES rubrics(id),
    start_at TIMESTAMP,
    end_at TIMESTAMP,
    winner_id UUID REFERENCES members(id),
    status VARCHAR(20) DEFAULT 'upcoming'  -- upcoming|active|completed
);

CREATE TABLE equity_distributions (
    id UUID PRIMARY KEY,
    groupchat_id UUID REFERENCES groupchats(id),
    period VARCHAR(20),
    total_distributed_sol DECIMAL(18,9),
    distributed_at TIMESTAMP DEFAULT NOW(),
    tx_signature VARCHAR(88)  -- Solana transaction signature
);

-- KEY QUERIES

-- Leaderboard with equity weighting
SELECT 
    m.telegram_user_id,
    m.wallet_address,
    nt.tier_name,
    m.equity_shares,
    l.rank,
    l.points,
    l.sol_earned,
    l.avg_rubric_score,
    ROUND(m.equity_shares::DECIMAL / g.equity_total_shares * 100, 2) as ownership_pct
FROM leaderboard l
JOIN members m ON l.member_id = m.id
JOIN nft_tiers nt ON m.tier_id = nt.id
JOIN groupchats g ON l.groupchat_id = g.id
WHERE l.groupchat_id = $1 AND l.period = 'weekly'
ORDER BY l.rank ASC;

-- Contribution ROI per member
SELECT 
    m.telegram_user_id,
    COUNT(c.id) as total_contributions,
    SUM(c.points_earned) as total_points,
    AVG(c.rubric_score) as avg_quality,
    SUM(c.sol_reward) as sol_earned,
    SUM(c.sol_reward) / NULLIF(COUNT(c.id), 0) as sol_per_contribution
FROM contributions c
JOIN members m ON c.member_id = m.id
WHERE c.groupchat_id = $1
GROUP BY m.id, m.telegram_user_id
ORDER BY sol_earned DESC;

-- Equity distribution calculation
SELECT 
    m.wallet_address,
    m.equity_shares,
    ROUND(m.equity_shares::DECIMAL / g.equity_total_shares * $2, 9) as sol_share
FROM members m
JOIN groupchats g ON m.groupchat_id = g.id
WHERE m.groupchat_id = $1
ORDER BY m.equity_shares DESC;
```

---

## NFT TIER SYSTEM (Upgrade = More Equity)

```
TIER 1: ACCESS NFT (Entry)
  → Price: 0.1 SOL
  → Equity: 0 shares (access only)
  → Perms: read groupchat, vote on rubrics
  → Upgrade: 500 points + 0.2 SOL → CONTRIBUTOR

TIER 2: CONTRIBUTOR NFT
  → Price: 0.3 SOL (new entry)
  → Equity: 10 shares
  → Perms: post content, earn points, earn SOL rewards
  → Upgrade: 2000 points + 0.5 SOL → ELDER

TIER 3: ELDER NFT
  → Price: 1.0 SOL (new entry)
  → Equity: 50 shares
  → Perms: create rubrics, host tournaments, recruit
  → Upgrade: 10000 points + 2.0 SOL + community vote → FOUNDER

TIER 4: FOUNDER NFT (Limited: max 12 per groupchat — C144 aligned)
  → Price: 5.0 SOL (new entry)
  → Equity: 250 shares
  → Perms: set rubric standards, split revenue, governance vote
  → Cannot upgrade further — the sovereign tier
```

---

## GAMIFICATION MECHANICS

```
POINTS ENGINE (earned for every contribution):
  Message quality (rubric-scored): up to 100 pts
  Data upload (skill.md, doc): 50 pts
  Referral (new member joins): 200 pts
  Tournament win: 1000 pts
  Rubric creation (validated): 150 pts
  Lead magnet created (clicked 10+ times): 300 pts
  Daily login streak: 5 pts/day (max 7-day streak = 35 pts)

SOL REWARDS (distributed weekly from treasury):
  70% → equity holders (by share count)
  20% → top 10 weekly contributors (by points)
  10% → tournament prize pool

LEADERBOARD RESETS:
  Daily: top 10 get bonus points
  Weekly: SOL distribution triggered
  Monthly: tier upgrade eligibility review
  Annually: founding equity lock-in
```

---

## SOLANA PROGRAM ARCHITECTURE (Smart Contracts)

```rust
// Program accounts (simplified)

GroupchatState {
    treasury: Pubkey,           // Treasury wallet
    nft_collection: Pubkey,     // NFT collection mint
    rubric_oracle: Pubkey,      // Off-chain rubric oracle
    total_equity_shares: u32,   // 10,000
    distributed_sol: u64,       // lamports distributed total
    member_count: u32,
}

MemberAccount {
    wallet: Pubkey,
    nft_mint: Pubkey,           // Their specific NFT
    tier: u8,                   // 1-4
    equity_shares: u32,
    points: u64,
    sol_earned: u64,            // lamports
    last_contribution: i64,     // unix timestamp
}

// Instructions:
// - join_groupchat(nft_mint) → verify NFT ownership → create MemberAccount
// - contribute(content_hash, rubric_score) → add points + micro SOL reward
// - upgrade_nft(current_nft) → burn current → mint higher tier → update equity
// - distribute_revenue() → weekly SOL split to all equity holders
// - enter_tournament(entry_fee) → stake SOL → compete → winner takes pool
```

---

## TELEGRAM BOT INTEGRATION

```python
# Core flow: every groupchat message → scored → points → leaderboard

async def on_message(update):
    user = get_or_create_member(update.from_user.id)
    if not user.has_valid_nft:
        await kick_or_restrict(update)  # No NFT = no access
        return
    
    # Score the contribution
    score = await rubric_scorer.score(update.message.text)
    points = calculate_points(score, user.tier)
    sol_reward = calculate_micro_reward(points, treasury_balance)
    
    # Update SQL leaderboard
    await db.add_contribution(user.id, score, points, sol_reward)
    await db.update_leaderboard(user.id)
    
    # Check for upgrade eligibility
    if user.points >= user.tier.upgrade_threshold:
        await notify_upgrade_available(user)
    
    # Milestone announcements
    if points >= 100:
        await announce_high_scorer(user, score)

# On-chain verification
async def verify_nft_membership(wallet, nft_mint, groupchat_collection):
    token_account = get_token_account(wallet, nft_mint)
    if token_account.amount != 1:
        return False  # Doesn't own the NFT
    metadata = await get_nft_metadata(nft_mint)
    return metadata.collection == groupchat_collection
```

---

## THE COMPOUND FLYWHEEL

```
[1] OoRava deploys groupchat → mints NFT collection on Solana
[2] First 12 FOUNDER NFTs sold (5 SOL each = 60 SOL seed treasury)
[3] Treasury funds: SOL rewards + tournament prizes
[4] Members contribute → earn points + micro SOL → climb leaderboard
[5] High performers upgrade NFT → gain equity shares
[6] Equity holders receive weekly SOL distributions
[7] Distributions attract new members → buy ACCESS NFTs
[8] New members contribute data → treasury grows
[9] Treasury growth → larger weekly distributions → more attractive
[10] Top leaderboard profiles become LEAD MAGNETS (publicly visible)
[11] Lead magnets funnel new users → click to join → buy NFT
[12] Skill.mds generated from groupchat data → published → drive traffic
[13] Traffic → more members → [LOOP: INFINITE]
```

---
*Solana NFT-Gated Economy v1.0 | Chapter 7 | AuthurKing × OoRava Omnia*
*Data source: Quest to a Billion!! (2023-2026)*
