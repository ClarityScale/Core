import re
from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List, Sequence


Sentiment = str


@dataclass(frozen=True)
class EventInput:
    name: str
    expected_timing: str
    description: str
    key_drivers: Sequence[str]


BASE_OPPORTUNITIES: List[Dict[str, object]] = [
    {
        "ticker": "NVDA",
        "company": "NVIDIA Corp.",
        "sector": "Technology",
        "country": "United States",
        "expected_direction": "Bullish",
        "time_horizon": "Medium-term (3–12 months)",
        "mechanism_template": "{{event}} supports capex for accelerated computing and AI infrastructure build-outs.",
        "investability_score": 8,
        "rationale_template": "Leverage leadership in data center GPUs as enterprises pursue {{drivers}}; monitor supply constraints through {{timing}}.",
        "sources": ["Company filings", "Bloomberg Intelligence thematic snapshot"],
    },
    {
        "ticker": "MSFT",
        "company": "Microsoft Corp.",
        "sector": "Technology",
        "country": "United States",
        "expected_direction": "Bullish",
        "time_horizon": "Medium-term (3–12 months)",
        "mechanism_template": "Hyperscale cloud demand linked to {{event}} drives Azure consumption and AI services monetization.",
        "investability_score": 8,
        "rationale_template": "Cross-sell of analytics, security, and AI tooling into enterprise workloads tied to {{drivers}} underpins durable growth.",
        "sources": ["Microsoft earnings transcripts", "Reuters enterprise software coverage"],
    },
    {
        "ticker": "ASML",
        "company": "ASML Holding NV",
        "sector": "Technology",
        "country": "Netherlands",
        "expected_direction": "Bullish",
        "time_horizon": "Long-term (1–5 years)",
        "mechanism_template": "{{event}} accelerates advanced node investment, sustaining EUV tool backlog through the strategic horizon.",
        "investability_score": 7,
        "rationale_template": "High switching costs and limited EUV supply create pricing power if governments subsidize {{drivers}}.",
        "sources": ["ASML capital markets day", "Financial Times semiconductor policy coverage"],
    },
    {
        "ticker": "TSM",
        "company": "Taiwan Semiconductor Manufacturing Co.",
        "sector": "Technology",
        "country": "Taiwan",
        "expected_direction": "Bullish",
        "time_horizon": "Long-term (1–5 years)",
        "mechanism_template": "Foundry mix shifts toward high-performance computing tied to {{event}}, sustaining premium pricing.",
        "investability_score": 7,
        "rationale_template": "Geopolitical incentives and client prepayments provide funding bridge for capex aligned with {{drivers}}.",
        "sources": ["Taiwan Ministry of Economic Affairs", "WSJ semiconductor supply chain updates"],
    },
    {
        "ticker": "PLTR",
        "company": "Palantir Technologies",
        "sector": "Emerging Tech / AI",
        "country": "United States",
        "expected_direction": "Bullish",
        "time_horizon": "Short-term (0–3 months)",
        "mechanism_template": "{{event}} expands demand for real-time decision platforms across defense and critical industries.",
        "investability_score": 6,
        "rationale_template": "Commercial pipeline benefits from urgency around {{drivers}}, though valuation requires disciplined sizing.",
        "sources": ["Department of Defense contract database", "Bloomberg defense tech briefings"],
    },
    {
        "ticker": "LMT",
        "company": "Lockheed Martin",
        "sector": "Defense",
        "country": "United States",
        "expected_direction": "Bullish",
        "time_horizon": "Medium-term (3–12 months)",
        "mechanism_template": "Defense procurement linked to {{event}} supports backlog visibility and sustainment revenue.",
        "investability_score": 7,
        "rationale_template": "Budget reallocation toward deterrence and missile defense tied to {{drivers}} underpins free cash flow yield.",
        "sources": ["US DoD budget request", "Jane’s Defense Weekly"],
    },
    {
        "ticker": "RTX",
        "company": "RTX Corp.",
        "sector": "Defense",
        "country": "United States",
        "expected_direction": "Bullish",
        "time_horizon": "Medium-term (3–12 months)",
        "mechanism_template": "{{event}} drives demand for integrated air defense and sensor upgrades across NATO partners.",
        "investability_score": 6,
        "rationale_template": "Balanced civil/military exposure offers hedge as airlines and governments respond to {{drivers}}.",
        "sources": ["NATO procurement releases", "Reuters aerospace coverage"],
    },
    {
        "ticker": "CVX",
        "company": "Chevron Corp.",
        "sector": "Energy",
        "country": "United States",
        "expected_direction": "Bullish",
        "time_horizon": "Short-term (0–3 months)",
        "mechanism_template": "{{event}} tightens supply-demand expectations, elevating upstream realizations and cash returns.",
        "investability_score": 6,
        "rationale_template": "Capital discipline plus variable buybacks offer torque if commodity volatility from {{drivers}} persists.",
        "sources": ["IEA Oil Market Report", "Bloomberg commodity strategy"],
    },
    {
        "ticker": "XLE",
        "company": "Energy Select Sector SPDR ETF",
        "sector": "Energy",
        "country": "United States",
        "expected_direction": "Bullish",
        "time_horizon": "Short-term (0–3 months)",
        "mechanism_template": "Sector ETF captures broad energy beta as {{event}} reprices supply risks and refining margins.",
        "investability_score": 5,
        "rationale_template": "Diversified holdings mitigate single-name risk while retaining upside to {{drivers}}.",
        "sources": ["IEA Oil Market Report", "FT energy markets coverage"],
    },
    {
        "ticker": "VWS.CO",
        "company": "Vestas Wind Systems",
        "sector": "Industrials",
        "country": "Denmark",
        "expected_direction": "Bullish",
        "time_horizon": "Long-term (1–5 years)",
        "mechanism_template": "{{event}} potentially accelerates renewable auctions and grid-scale wind deployment.",
        "investability_score": 6,
        "rationale_template": "Policy support and IRA-style incentives aligned with {{drivers}} could expand order intake and service margin.",
        "sources": ["IEA Renewable Outlook", "Bloomberg New Energy Finance"],
    },
    {
        "ticker": "ABB",
        "company": "ABB Ltd.",
        "sector": "Industrials",
        "country": "Switzerland",
        "expected_direction": "Bullish",
        "time_horizon": "Medium-term (3–12 months)",
        "mechanism_template": "Automation and grid modernization capex tied to {{event}} support robotics and electrification demand.",
        "investability_score": 6,
        "rationale_template": "Strong backlog and software attach rates provide resilience as clients execute on {{drivers}}.",
        "sources": ["Company investor day", "Reuters industrial automation coverage"],
    },
    {
        "ticker": "CAT",
        "company": "Caterpillar Inc.",
        "sector": "Industrials",
        "country": "United States",
        "expected_direction": "Bullish",
        "time_horizon": "Medium-term (3–12 months)",
        "mechanism_template": "{{event}} increases infrastructure and resource development activity supporting heavy machinery orders.",
        "investability_score": 6,
        "rationale_template": "Dealer inventories lean while pricing power endures if fiscal programs around {{drivers}} materialize.",
        "sources": ["US Infrastructure Investment updates", "Wall Street Journal construction reports"],
    },
    {
        "ticker": "LIN",
        "company": "Linde Plc",
        "sector": "Materials",
        "country": "Ireland",
        "expected_direction": "Bullish",
        "time_horizon": "Long-term (1–5 years)",
        "mechanism_template": "Industrial gas demand linked to {{event}} supports long-term contracts in hydrogen and clean fuels.",
        "investability_score": 6,
        "rationale_template": "Project backlog benefits from on-site agreements as clients scale {{drivers}} technologies.",
        "sources": ["Company sustainability report", "Financial Times energy transition coverage"],
    },
    {
        "ticker": "ADBE",
        "company": "Adobe Inc.",
        "sector": "Technology",
        "country": "United States",
        "expected_direction": "Bullish",
        "time_horizon": "Medium-term (3–12 months)",
        "mechanism_template": "{{event}} lifts demand for content automation and AI-native productivity suites.",
        "investability_score": 5,
        "rationale_template": "Generative AI integration helps expand ARPU as marketing teams react to {{drivers}}.",
        "sources": ["Adobe earnings call", "Reuters digital media coverage"],
    },
    {
        "ticker": "SHOP",
        "company": "Shopify Inc.",
        "sector": "Consumer Goods",
        "country": "Canada",
        "expected_direction": "Bullish",
        "time_horizon": "Medium-term (3–12 months)",
        "mechanism_template": "{{event}} catalyzes omnichannel investment and cross-border commerce upgrades.",
        "investability_score": 5,
        "rationale_template": "Merchants retool logistics and storefronts to align with {{drivers}}, aiding take-rate expansion.",
        "sources": ["Company investor presentations", "Bloomberg e-commerce insights"],
    },
    {
        "ticker": "MCD",
        "company": "McDonald's Corp.",
        "sector": "Consumer Goods",
        "country": "United States",
        "expected_direction": "Neutral",
        "time_horizon": "Short-term (0–3 months)",
        "mechanism_template": "Global franchise footprint offers defensive cashflows if {{event}} increases volatility.",
        "investability_score": 4,
        "rationale_template": "Value positioning and menu localization provide hedge against demand shocks from {{drivers}}.",
        "sources": ["Company quarterly filings", "WSJ consumer trends coverage"],
    },
    {
        "ticker": "JNJ",
        "company": "Johnson & Johnson",
        "sector": "Healthcare",
        "country": "United States",
        "expected_direction": "Neutral",
        "time_horizon": "Medium-term (3–12 months)",
        "mechanism_template": "Defensive healthcare exposure offsets cyclical swings while capitalizes on {{event}}-driven policy spend.",
        "investability_score": 5,
        "rationale_template": "Diversified revenue mix and balance sheet strength provide ballast amid {{drivers}} uncertainty.",
        "sources": ["Company filings", "Bloomberg Healthcare Outlook"],
    },
    {
        "ticker": "UNH",
        "company": "UnitedHealth Group",
        "sector": "Healthcare",
        "country": "United States",
        "expected_direction": "Neutral",
        "time_horizon": "Medium-term (3–12 months)",
        "mechanism_template": "{{event}} could reshape reimbursement or utilization trends; diversified services platform manages variance.",
        "investability_score": 5,
        "rationale_template": "Optum analytics and insurance mix enable agile response to policy shifts from {{drivers}}.",
        "sources": ["CMS policy releases", "Financial Times healthcare policy coverage"],
    },
    {
        "ticker": "JPM",
        "company": "JPMorgan Chase & Co.",
        "sector": "Financials",
        "country": "United States",
        "expected_direction": "Bullish",
        "time_horizon": "Short-term (0–3 months)",
        "mechanism_template": "{{event}} reshapes yield curve expectations, supporting net interest income and trading flows.",
        "investability_score": 5,
        "rationale_template": "Balance sheet optionality and investment banking rebound tied to {{drivers}} support premium valuation.",
        "sources": ["Federal Reserve FOMC statements", "Reuters banking sector coverage"],
    },
    {
        "ticker": "BX",
        "company": "Blackstone Inc.",
        "sector": "Financials",
        "country": "United States",
        "expected_direction": "Bullish",
        "time_horizon": "Medium-term (3–12 months)",
        "mechanism_template": "{{event}} unlocks alternative asset inflows toward private credit, infrastructure, and real assets.",
        "investability_score": 6,
        "rationale_template": "Dry powder deployment aligned with {{drivers}} themes could accelerate fee-related earnings.",
        "sources": ["Preqin fundraising data", "Bloomberg alternative asset commentary"],
    },
    {
        "ticker": "EQIX",
        "company": "Equinix Inc.",
        "sector": "Real Estate",
        "country": "United States",
        "expected_direction": "Bullish",
        "time_horizon": "Long-term (1–5 years)",
        "mechanism_template": "{{event}} amplifies demand for interconnection and edge computing colocation.",
        "investability_score": 6,
        "rationale_template": "Global footprint and pricing escalators capture secular data growth from {{drivers}}.",
        "sources": ["Company investor relations", "Gartner data center outlook"],
    },
    {
        "ticker": "PLD",
        "company": "Prologis Inc.",
        "sector": "Real Estate",
        "country": "United States",
        "expected_direction": "Bullish",
        "time_horizon": "Medium-term (3–12 months)",
        "mechanism_template": "{{event}} drives reshoring and inventory reconfiguration, supporting logistics real estate demand.",
        "investability_score": 5,
        "rationale_template": "High-barrier locations and CPI-linked leases monetize supply chain adjustments around {{drivers}}.",
        "sources": ["Company logistics report", "WSJ supply chain coverage"],
    },
    {
        "ticker": "DUK",
        "company": "Duke Energy",
        "sector": "Utilities",
        "country": "United States",
        "expected_direction": "Neutral",
        "time_horizon": "Long-term (1–5 years)",
        "mechanism_template": "Utility capex plans adjust to grid reliability mandates emerging from {{event}}.",
        "investability_score": 4,
        "rationale_template": "Regulated returns provide income stability; monitor regulatory lag as {{drivers}} evolve.",
        "sources": ["State utility commission filings", "Reuters power markets coverage"],
    },
    {
        "ticker": "HYG",
        "company": "iShares iBoxx High Yield Corp Bond ETF",
        "sector": "Financials",
        "country": "United States",
        "expected_direction": "Bearish",
        "time_horizon": "Short-term (0–3 months)",
        "mechanism_template": "{{event}} could widen credit spreads as investors reprice default risk.",
        "investability_score": 4,
        "rationale_template": "High beta credit faces drawdown risk if {{drivers}} undermine liquidity; consider hedges.",
        "sources": ["ICE BofA High Yield Index data", "Bloomberg credit strategy"],
    },
    {
        "ticker": "ASHR",
        "company": "Xtrackers Harvest CSI 300 China A ETF",
        "sector": "Emerging Markets",
        "country": "China",
        "expected_direction": "Bearish",
        "time_horizon": "Medium-term (3–12 months)",
        "mechanism_template": "{{event}} may intensify regulatory pressure or capital restrictions impacting mainland equities.",
        "investability_score": 3,
        "rationale_template": "Sensitivity to policy signals and global positioning makes ASHR a tactical hedge against {{drivers}}.",
        "sources": ["PBOC policy announcements", "Financial Times China markets coverage"],
    },
    {
        "ticker": "RKLB",
        "company": "Rocket Lab USA Inc.",
        "sector": "Space",
        "country": "United States",
        "expected_direction": "Bullish",
        "time_horizon": "Long-term (1–5 years)",
        "mechanism_template": "{{event}} boosts demand for responsive launch and satellite deployment capabilities as governments realign space strategy.",
        "investability_score": 5,
        "rationale_template": "Backlog growth and diversified missions tied to {{drivers}} increase visibility; monitor execution risk as production scales.",
        "sources": ["US Space Force procurement releases", "Bloomberg space economy coverage"],
    },
    {
        "ticker": "IONQ",
        "company": "IonQ Inc.",
        "sector": "Quantum Computing",
        "country": "United States",
        "expected_direction": "Bullish",
        "time_horizon": "Long-term (1–5 years)",
        "mechanism_template": "{{event}} accelerates funding for quantum research, positioning IonQ to benefit from early commercial pilots.",
        "investability_score": 4,
        "rationale_template": "Partnership pipeline aligned with {{drivers}} offers optionality; valuation volatility warrants staged exposure.",
        "sources": ["National quantum initiative updates", "Financial Times emerging technology coverage"],
    },
]


BULLISH_KEYWORDS = ["stimulus", "investment", "recovery", "growth", "innovation", "ai", "alliances", "easing", "support"]
BEARISH_KEYWORDS = ["sanction", "recession", "war", "conflict", "crackdown", "ban", "shortage", "tightening", "slowdown"]


def fill_template(template: str, replacements: Dict[str, str]) -> str:
    def _replace(match: re.Match[str]) -> str:
        key = match.group(1).strip()
        return replacements.get(key, "")

    return re.sub(r"{{(.*?)}}", _replace, template)


def dedupe(values: Sequence[str]) -> List[str]:
    seen = set()
    result: List[str] = []
    for value in values:
        trimmed = value.strip()
        if trimmed and trimmed not in seen:
            seen.add(trimmed)
            result.append(trimmed)
    return result


def determine_sentiment(text: str) -> Sentiment:
    normalized = text.lower()
    if any(keyword in normalized for keyword in BEARISH_KEYWORDS):
        return "Bearish"
    if any(keyword in normalized for keyword in BULLISH_KEYWORDS):
        return "Bullish"
    return "Neutral"


def derive_macro_themes(drivers: Sequence[str], sentiment: Sentiment) -> List[str]:
    base_themes = ["Policy Trajectory", "Cross-Border Capital Flows", "Supply Chain Resilience"]
    keyword_themes = [
        re.sub(r"[^\w\s-]", "", " ".join(driver.split()[:3])).strip()
        for driver in drivers
        if driver.strip()
    ]
    sentiment_theme = {
        "Bullish": "Risk-On Rotation",
        "Bearish": "Defensive Positioning",
    }.get(sentiment, "Selective Allocation")
    return dedupe([sentiment_theme, *keyword_themes, *base_themes])[:6]


def derive_sector_outlook(sentiment: Sentiment, drivers: Sequence[str], event_name: str) -> List[str]:
    focus = " & ".join(drivers[:2]) if drivers else "stated catalysts"
    base = [
        f"Technology platforms positioned to monetize {focus}.",
        f"Energy and materials tracking commodity volatility around {event_name}.",
        "Financials adjusting capital deployment as policy visibility shifts.",
        "Defensive sectors providing ballast amid execution risk.",
    ]
    if sentiment == "Bullish":
        base.insert(0, "Growth equities favored as liquidity expectations improve.")
    elif sentiment == "Bearish":
        base.insert(0, "Quality balance sheets and cash generative assets prioritized.")
    else:
        base.insert(0, "Market likely stays range-bound with rotation within sectors.")
    return base[:5]


def build_horizon_impacts(sentiment: Sentiment, drivers_text: str, timeline: str) -> List[Dict[str, str]]:
    return [
        {
            "horizon": "Short-term (0–3 months)",
            "outlook": f"{sentiment} bias as headlines around {drivers_text} drive volatility; monitor liquidity and spreads.",
        },
        {
            "horizon": "Medium-term (3–12 months)",
            "outlook": f"Execution against {timeline} milestones will clarify earnings visibility and capital allocation.",
        },
        {
            "horizon": "Long-term (1–5 years)",
            "outlook": "Structural implications for market share, supply chains, and policy regimes anchor strategic positioning.",
        },
    ]


def build_event_context(event_input: EventInput) -> Dict[str, object]:
    event_name = event_input.name.strip() or "Submitted strategic catalyst"
    overview = event_input.description.strip() or "Description pending—add narrative for richer context."
    timing = event_input.expected_timing.strip() or "Timing TBD—confirm expected announcement or implementation window."
    context_points = [driver.strip() for driver in event_input.key_drivers if driver.strip()]

    significance = (
        context_points[0]
        if context_points
        else "Detail the scale of capital flows, policy changes, or technology adoption expected from this catalyst."
    )

    if not context_points:
        context_points.append("Add key drivers such as policy levers, stakeholders, or technology triggers.")

    return {
        "overview": f"{event_name}: {overview}",
        "timing": timing,
        "significance": significance,
        "context_points": context_points[:4],
    }


def build_opportunities(event_name: str, drivers_text: str, timeline: str, sentiment: Sentiment) -> List[Dict[str, object]]:
    replacements = {"event": event_name, "drivers": drivers_text, "timing": timeline, "sentiment": sentiment}
    opportunities: List[Dict[str, object]] = []

    for item in BASE_OPPORTUNITIES:
        opportunity = {
            "ticker": item["ticker"],
            "company": item["company"],
            "sector": item["sector"],
            "country": item["country"],
            "expected_direction": item["expected_direction"],
            "time_horizon": item["time_horizon"],
            "mechanism": fill_template(item["mechanism_template"], replacements),
            "investability_score": item["investability_score"],
            "rationale": fill_template(item["rationale_template"], replacements),
            "sources": item["sources"],
        }
        opportunities.append(opportunity)

    return opportunities


def build_mock_report(event_input: EventInput) -> Dict[str, object]:
    event_name = event_input.name.strip() or "Strategic Market Catalyst"
    drivers = [driver.strip() for driver in event_input.key_drivers if driver.strip()]
    drivers_text = "; ".join(drivers) if drivers else "the stated catalysts"
    timeline = event_input.expected_timing.strip() or "the specified timeline"
    description_text = event_input.description.strip() or "No narrative provided yet—supply qualitative colour for accuracy."

    sentiment = determine_sentiment(f"{description_text} {drivers_text}")
    macro_themes = derive_macro_themes(drivers, sentiment)
    sector_outlook = derive_sector_outlook(sentiment, drivers, event_name)
    horizon_impacts = build_horizon_impacts(sentiment, drivers_text, timeline)
    event_context = build_event_context(event_input)
    opportunities = build_opportunities(event_name, drivers_text, timeline, sentiment)

    headline_summary = f"{event_name}: Preliminary {sentiment.lower()} stance anchored on {macro_themes[0] if macro_themes else 'macro reassessment'}."
    top_tickers = ", ".join(op["ticker"] for op in opportunities[:3])

    summary_insights = [
        f"{event_name} screens as {sentiment.lower()} with emphasis on {', '.join(macro_themes[:3])}.",
        f"Sector leadership likely features {' '.join(sector_outlook[:3])}",
        f"Initial focus tickers: {top_tickers}; recalibrate sizing as milestones on {timeline} emerge.",
    ]

    risk_note = (
        f"Scenario sensitivity remains elevated—validate assumptions on {drivers_text} with real-time data, "
        "monitor policy communications, and size exposures within risk budget."
    )

    citations = [
        "IMF World Economic Outlook (latest edition)",
        "Bloomberg Terminal – Thematic Intelligence (placeholder)",
        "Reuters – Market Newswire (placeholder)",
    ]

    return {
        "generated_at": datetime.utcnow().isoformat(),
        "event_name": event_name,
        "headline_summary": headline_summary,
        "event_context": event_context,
        "market_impact": {
            "sentiment": sentiment,
            "macro_themes": macro_themes,
            "sector_outlook": sector_outlook,
            "horizon_impacts": horizon_impacts,
        },
        "opportunities": opportunities,
        "summary_insights": summary_insights,
        "risk_note": risk_note,
        "citations": citations,
    }
