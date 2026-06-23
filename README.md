⚽ Agentic Transfer Market Validator

A "Digital Sporting Director" that takes a free-text football transfer rumor and returns a structured validity report — source credibility, tactical fit, value assessment, and a Proceed / Caution / Avoid verdict.

🔗 Live demo: https://transfer-validator-nstxgudkjnswfopyotx45u.streamlit.app/


The problem

The transfer market is flooded with rumors. A fan scrolling social media can't easily tell a Fabrizio Romano report from an engagement-farming account, and even a credible rumor says nothing about whether the move actually makes tactical or financial sense. There's no single tool that asks both questions at once: is this rumor believable, and is it a good idea?

What this does (precisely)

You type something like "Nico Williams to Barcelona for €60m, reported by Sky Sports." The system:


Parses the unstructured text into structured fields (player, club, fee, source) — LLM-powered.
Scores credibility by checking the source against a journalist/outlet tier list and counting independent corroborating reports — rules-based.
Assesses value by comparing the reported fee to the player's market value — rules-based.
Computes tactical fit by comparing the player's statistical profile (percentiles) against the buying club's playing-style profile — rules-based.
Synthesizes a verdict — a Proceed / Caution / Avoid recommendation with written reasoning over all of the above — LLM-powered.


The whole thing is orchestrated as a directed LangGraph pipeline with conditional routing (a low-credibility junk rumor short-circuits early to save compute) and graceful degradation (a missing data source lowers confidence rather than crashing the report).


Honest scope note (read this): This is a working pipeline demoed on a curated cached dataset of ~12 marquee players across 5 clubs. The reasoning runs live on every request, but the underlying player stats are read from a committed cache — a deliberate decision for demo reliability (see Key Decisions). Player percentiles are position-calibrated estimates derived from FBref per-90 data. Live web scraping is a documented v2 item, not a current capability. I'd rather state that plainly than imply the tool knows real-world transfer outcomes — it evaluates the plausibility of a claim, not its truth.




Architecture

   rumor text
        │
        ▼
   ┌──────────┐    ┌─────────────┐   tier 5 + 0 corroboration
   │  PARSE   │──► │ CREDIBILITY │──────────────┐ (short-circuit)
   │  (LLM)   │    │  (rules)    │              │
   └──────────┘    └──────┬──────┘              │
                          │ otherwise           │
                ┌─────────┴─────────┐           │
                ▼                   ▼           │
        ┌──────────────┐   ┌──────────────┐     │
        │ MARKET VALUE │   │ PERFORMANCE  │     │
        │   (rules)    │   │   (cache)    │     │
        └──────┬───────┘   └──────┬───────┘     │
               │                  ▼             │
               │           ┌──────────────┐     │
               │           │ TACTICAL FIT │     │
               │           │   (rules)    │     │
               │           └──────┬───────┘     │
               └────────┬─────────┘             │
                        ▼                       │
                  ┌──────────┐ ◄────────────────┘
                  │ VERDICT  │
                  │  (LLM)   │
                  └──────────┘

Why LangGraph (over CrewAI / AutoGen): the pipeline needs conditional branching, parallel fan-out, and explicit failure recovery — all native LangGraph primitives. AutoGen is in maintenance mode as of 2026, and CrewAI handles the short-circuit/parallel logic less cleanly. The graph is also a typed state machine, which makes the data flow inspectable and debuggable.

Honest breakdown of what's "AI" vs. deterministic (because the distinction matters and interviewers ask):

ComponentPowered byRumor parsing (text → structured)LLM (Gemini 2.5 Flash)Verdict synthesis (data → recommendation)LLM (Gemini 2.5 Flash)Credibility tiering & corroborationDeterministic rulesTactical fit scoreDeterministic (vector comparison)Value premiumDeterministic (arithmetic)

This is accurately described as an LLM-orchestrated workflow, not an autonomous multi-agent system — the graph follows a fixed, hand-designed control flow.


Key product decisions (the why, not just the what)


Scoped to 5 clubs with handcrafted style profiles. Tactical fit needs a model of each club's system. Rather than fake breadth, I hand-built profiles for Barcelona, Real Madrid, Man City, Arsenal, and Liverpool. Narrow and correct beats broad and hand-wavy.
Cached dataset over live scraping. FBref/Transfermarkt rate-limit aggressively and break in front of an audience. A committed cache makes the demo bulletproof. The trade-off (no live data) is the explicit cost of a reliable demo — a product decision, not an oversight.
Deterministic scoring, not "ask the LLM." Credibility and fit are reproducible and explainable. An LLM-guessed credibility score can't be defended; a journalist-tier lookup can.
A short-circuit for junk rumors. A lowest-tier, uncorroborated rumor exits early to an "Avoid" verdict without spending compute on analysis — a small but real cost/latency decision.



PM framing

North Star metric: Validated rumors per active user per week — it captures the core value (people trusting the tool to triage rumors) without rewarding empty engagement.

Primary persona & JTBD: The engaged fan / fantasy-football decision-maker. JTBD: "When I see a transfer rumor, I want to quickly know if it's credible and whether it makes sense, so I can stop wasting attention on noise."

Success metrics (post-launch, hypothetical): activation (% of new users who validate ≥1 rumor), retention (week-4 return rate), and a quality proxy (agreement between the tool's credibility tier and eventual real-world outcome).

Prioritization snapshot (MoSCoW):


Must: rumor parsing, credibility tiering, a verdict.
Should: tactical fit, value assessment.
Could: live scraping, more clubs, historical accuracy tracking.
Won't (v1): user accounts, notifications, mobile app.


Roadmap:


v1 (this): working pipeline, 5 clubs, cached data, live deployment.
v2: live FBref scraping with a cache-first/live-fallback layer; club style profiles derived from team-level stats instead of handcrafted; tightened World Cup hype flag (per-squad, not whole-window).
v3: track credibility predictions against actual outcomes to make the scoring self-improving.



Tech stack

LangGraph (orchestration) · Google Gemini 2.5 Flash via langchain-google-genai (parsing + verdict) · Pydantic (structured LLM output) · Tavily (corroboration search) · Streamlit + Streamlit Community Cloud (UI + hosting) · Python.

Run it locally

bashgit clone https://github.com/f20230856-netizen/Transfer-Validator.git
cd Transfer-Validator
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
# add a .env file with:
#   GOOGLE_API_KEY=inserted my key
#   TAVILY_API_KEY=here as well
streamlit run app.py

Limitations


Curated cached dataset; not connected to live data sources (by design — see scope note).
Player percentiles are position-calibrated estimates, not exact scraped values.
Tactical profiles are handcrafted for 5 clubs.
The system evaluates rumor plausibility, not real-world truth — it does not know whether a transfer actually happened.



Built as a portfolio project demonstrating system design, agentic-workflow orchestration, and product scoping/prioritization.
