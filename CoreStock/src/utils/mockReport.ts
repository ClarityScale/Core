import {
    AssessmentReport,
    EventContext,
    EventInput,
    MarketImpact,
    OpportunityRow,
    Sentiment,
    TimeHorizon,
    TimeHorizonImpact,
} from '../types';

type BaseOpportunity = Omit<OpportunityRow, 'mechanism' | 'rationale'> & {
    mechanismTemplate: string;
    rationaleTemplate: string;
};

const BASE_OPPORTUNITIES: BaseOpportunity[] = [
    {
        ticker: 'NVDA',
        company: 'NVIDIA Corp.',
        sector: 'Technology',
        country: 'United States',
        expectedDirection: 'Bullish',
        timeHorizon: 'Medium-term (3–12 months)',
        mechanismTemplate: '{{event}} supports capex for accelerated computing and AI infrastructure build-outs.',
        investabilityScore: 8,
        rationaleTemplate:
            'Leverage leadership in data center GPUs as enterprises pursue {{drivers}}; monitor supply constraints through {{timing}}.',
        sources: ['Company filings', 'Bloomberg Intelligence thematic snapshot'],
    },
    {
        ticker: 'MSFT',
        company: 'Microsoft Corp.',
        sector: 'Technology',
        country: 'United States',
        expectedDirection: 'Bullish',
        timeHorizon: 'Medium-term (3–12 months)',
        mechanismTemplate:
            'Hyperscale cloud demand linked to {{event}} drives Azure consumption and AI services monetization.',
        investabilityScore: 8,
        rationaleTemplate:
            'Cross-sell of analytics, security, and AI tooling into enterprise workloads tied to {{drivers}} underpins durable growth.',
        sources: ['Microsoft earnings transcripts', 'Reuters enterprise software coverage'],
    },
    {
        ticker: 'ASML',
        company: 'ASML Holding NV',
        sector: 'Technology',
        country: 'Netherlands',
        expectedDirection: 'Bullish',
        timeHorizon: 'Long-term (1–5 years)',
        mechanismTemplate:
            '{{event}} accelerates advanced node investment, sustaining EUV tool backlog through the strategic horizon.',
        investabilityScore: 7,
        rationaleTemplate:
            'High switching costs and limited EUV supply create pricing power if governments subsidize {{drivers}}.',
        sources: ['ASML capital markets day', 'Financial Times semiconductor policy coverage'],
    },
    {
        ticker: 'TSM',
        company: 'Taiwan Semiconductor Manufacturing Co.',
        sector: 'Technology',
        country: 'Taiwan',
        expectedDirection: 'Bullish',
        timeHorizon: 'Long-term (1–5 years)',
        mechanismTemplate:
            'Foundry mix shifts toward high-performance computing tied to {{event}}, sustaining premium pricing.',
        investabilityScore: 7,
        rationaleTemplate:
            'Geopolitical incentives and client prepayments provide funding bridge for capex aligned with {{drivers}}.',
        sources: ['Taiwan Ministry of Economic Affairs', 'WSJ semiconductor supply chain updates'],
    },
    {
        ticker: 'PLTR',
        company: 'Palantir Technologies',
        sector: 'Emerging Tech / AI',
        country: 'United States',
        expectedDirection: 'Bullish',
        timeHorizon: 'Short-term (0–3 months)',
        mechanismTemplate:
            '{{event}} expands demand for real-time decision platforms across defense and critical industries.',
        investabilityScore: 6,
        rationaleTemplate:
            'Commercial pipeline benefits from urgency around {{drivers}}, though valuation requires disciplined sizing.',
        sources: ['Department of Defense contract database', 'Bloomberg defense tech briefings'],
    },
    {
        ticker: 'LMT',
        company: 'Lockheed Martin',
        sector: 'Defense',
        country: 'United States',
        expectedDirection: 'Bullish',
        timeHorizon: 'Medium-term (3–12 months)',
        mechanismTemplate:
            'Defense procurement linked to {{event}} supports backlog visibility and sustainment revenue.',
        investabilityScore: 7,
        rationaleTemplate:
            'Budget reallocation toward deterrence and missile defense tied to {{drivers}} underpins free cash flow yield.',
        sources: ['US DoD budget request', 'Jane’s Defense Weekly'],
    },
    {
        ticker: 'RTX',
        company: 'RTX Corp.',
        sector: 'Defense',
        country: 'United States',
        expectedDirection: 'Bullish',
        timeHorizon: 'Medium-term (3–12 months)',
        mechanismTemplate:
            '{{event}} drives demand for integrated air defense and sensor upgrades across NATO partners.',
        investabilityScore: 6,
        rationaleTemplate:
            'Balanced civil/military exposure offers hedge as airlines and governments respond to {{drivers}}.',
        sources: ['NATO procurement releases', 'Reuters aerospace coverage'],
    },
    {
        ticker: 'CVX',
        company: 'Chevron Corp.',
        sector: 'Energy',
        country: 'United States',
        expectedDirection: 'Bullish',
        timeHorizon: 'Short-term (0–3 months)',
        mechanismTemplate:
            '{{event}} tightens supply-demand expectations, elevating upstream realizations and cash returns.',
        investabilityScore: 6,
        rationaleTemplate:
            'Capital discipline plus variable buybacks offer torque if commodity volatility from {{drivers}} persists.',
        sources: ['IEA Oil Market Report', 'Bloomberg commodity strategy'],
    },
    {
        ticker: 'XLE',
        company: 'Energy Select Sector SPDR ETF',
        sector: 'Energy',
        country: 'United States',
        expectedDirection: 'Bullish',
        timeHorizon: 'Short-term (0–3 months)',
        mechanismTemplate:
            'Sector ETF captures broad energy beta as {{event}} reprices supply risks and refining margins.',
        investabilityScore: 5,
        rationaleTemplate:
            'Diversified holdings mitigate single-name risk while retaining upside to {{drivers}}.',
        sources: ['IEA Oil Market Report', 'FT energy markets coverage'],
    },
    {
        ticker: 'VWS.CO',
        company: 'Vestas Wind Systems',
        sector: 'Industrials',
        country: 'Denmark',
        expectedDirection: 'Bullish',
        timeHorizon: 'Long-term (1–5 years)',
        mechanismTemplate:
            '{{event}} potentially accelerates renewable auctions and grid-scale wind deployment.',
        investabilityScore: 6,
        rationaleTemplate:
            'Policy support and IRA-style incentives aligned with {{drivers}} could expand order intake and service margin.',
        sources: ['IEA Renewable Outlook', 'Bloomberg New Energy Finance'],
    },
    {
        ticker: 'ABB',
        company: 'ABB Ltd.',
        sector: 'Industrials',
        country: 'Switzerland',
        expectedDirection: 'Bullish',
        timeHorizon: 'Medium-term (3–12 months)',
        mechanismTemplate:
            'Automation and grid modernization capex tied to {{event}} support robotics and electrification demand.',
        investabilityScore: 6,
        rationaleTemplate:
            'Strong backlog and software attach rates provide resilience as clients execute on {{drivers}}.',
        sources: ['Company investor day', 'Reuters industrial automation coverage'],
    },
    {
        ticker: 'CAT',
        company: 'Caterpillar Inc.',
        sector: 'Industrials',
        country: 'United States',
        expectedDirection: 'Bullish',
        timeHorizon: 'Medium-term (3–12 months)',
        mechanismTemplate:
            '{{event}} increases infrastructure and resource development activity supporting heavy machinery orders.',
        investabilityScore: 6,
        rationaleTemplate:
            'Dealer inventories lean while pricing power endures if fiscal programs around {{drivers}} materialize.',
        sources: ['US Infrastructure Investment updates', 'Wall Street Journal construction reports'],
    },
    {
        ticker: 'LIN',
        company: 'Linde Plc',
        sector: 'Materials',
        country: 'Ireland',
        expectedDirection: 'Bullish',
        timeHorizon: 'Long-term (1–5 years)',
        mechanismTemplate:
            'Industrial gas demand linked to {{event}} supports long-term contracts in hydrogen and clean fuels.',
        investabilityScore: 6,
        rationaleTemplate:
            'Project backlog benefits from on-site agreements as clients scale {{drivers}} technologies.',
        sources: ['Company sustainability report', 'Financial Times energy transition coverage'],
    },
    {
        ticker: 'ADBE',
        company: 'Adobe Inc.',
        sector: 'Technology',
        country: 'United States',
        expectedDirection: 'Bullish',
        timeHorizon: 'Medium-term (3–12 months)',
        mechanismTemplate:
            '{{event}} lifts demand for content automation and AI-native productivity suites.',
        investabilityScore: 5,
        rationaleTemplate:
            'Generative AI integration helps expand ARPU as marketing teams react to {{drivers}}.',
        sources: ['Adobe earnings call', 'Reuters digital media coverage'],
    },
    {
        ticker: 'SHOP',
        company: 'Shopify Inc.',
        sector: 'Consumer Goods',
        country: 'Canada',
        expectedDirection: 'Bullish',
        timeHorizon: 'Medium-term (3–12 months)',
        mechanismTemplate:
            '{{event}} catalyzes omnichannel investment and cross-border commerce upgrades.',
        investabilityScore: 5,
        rationaleTemplate:
            'Merchants retool logistics and storefronts to align with {{drivers}}, aiding take-rate expansion.',
        sources: ['Company investor presentations', 'Bloomberg e-commerce insights'],
    },
    {
        ticker: 'MCD',
        company: "McDonald's Corp.",
        sector: 'Consumer Goods',
        country: 'United States',
        expectedDirection: 'Neutral',
        timeHorizon: 'Short-term (0–3 months)',
        mechanismTemplate:
            'Global franchise footprint offers defensive cashflows if {{event}} increases volatility.',
        investabilityScore: 4,
        rationaleTemplate:
            'Value positioning and menu localization provide hedge against demand shocks from {{drivers}}.',
        sources: ['Company quarterly filings', 'WSJ consumer trends coverage'],
    },
    {
        ticker: 'JNJ',
        company: 'Johnson & Johnson',
        sector: 'Healthcare',
        country: 'United States',
        expectedDirection: 'Neutral',
        timeHorizon: 'Medium-term (3–12 months)',
        mechanismTemplate:
            'Defensive healthcare exposure offsets cyclical swings while capitalizes on {{event}}-driven policy spend.',
        investabilityScore: 5,
        rationaleTemplate:
            'Diversified revenue mix and balance sheet strength provide ballast amid {{drivers}} uncertainty.',
        sources: ['Company filings', 'Bloomberg Healthcare Outlook'],
    },
    {
        ticker: 'UNH',
        company: 'UnitedHealth Group',
        sector: 'Healthcare',
        country: 'United States',
        expectedDirection: 'Neutral',
        timeHorizon: 'Medium-term (3–12 months)',
        mechanismTemplate:
            '{{event}} could reshape reimbursement or utilization trends; diversified services platform manages variance.',
        investabilityScore: 5,
        rationaleTemplate:
            'Optum analytics and insurance mix enable agile response to policy shifts from {{drivers}}.',
        sources: ['CMS policy releases', 'Financial Times healthcare policy coverage'],
    },
    {
        ticker: 'JPM',
        company: 'JPMorgan Chase & Co.',
        sector: 'Financials',
        country: 'United States',
        expectedDirection: 'Bullish',
        timeHorizon: 'Short-term (0–3 months)',
        mechanismTemplate:
            '{{event}} reshapes yield curve expectations, supporting net interest income and trading flows.',
        investabilityScore: 5,
        rationaleTemplate:
            'Balance sheet optionality and investment banking rebound tied to {{drivers}} support premium valuation.',
        sources: ['Federal Reserve FOMC statements', 'Reuters banking sector coverage'],
    },
    {
        ticker: 'BX',
        company: 'Blackstone Inc.',
        sector: 'Financials',
        country: 'United States',
        expectedDirection: 'Bullish',
        timeHorizon: 'Medium-term (3–12 months)',
        mechanismTemplate:
            '{{event}} unlocks alternative asset inflows toward private credit, infrastructure, and real assets.',
        investabilityScore: 6,
        rationaleTemplate:
            'Dry powder deployment aligned with {{drivers}} themes could accelerate fee-related earnings.',
        sources: ['Preqin fundraising data', 'Bloomberg alternative asset commentary'],
    },
    {
        ticker: 'EQIX',
        company: 'Equinix Inc.',
        sector: 'Real Estate',
        country: 'United States',
        expectedDirection: 'Bullish',
        timeHorizon: 'Long-term (1–5 years)',
        mechanismTemplate:
            '{{event}} amplifies demand for interconnection and edge computing colocation.',
        investabilityScore: 6,
        rationaleTemplate:
            'Global footprint and pricing escalators capture secular data growth from {{drivers}}.',
        sources: ['Company investor relations', 'Gartner data center outlook'],
    },
    {
        ticker: 'PLD',
        company: 'Prologis Inc.',
        sector: 'Real Estate',
        country: 'United States',
        expectedDirection: 'Bullish',
        timeHorizon: 'Medium-term (3–12 months)',
        mechanismTemplate:
            '{{event}} drives reshoring and inventory reconfiguration, supporting logistics real estate demand.',
        investabilityScore: 5,
        rationaleTemplate:
            'High-barrier locations and CPI-linked leases monetize supply chain adjustments around {{drivers}}.',
        sources: ['Company logistics report', 'WSJ supply chain coverage'],
    },
    {
        ticker: 'DUK',
        company: 'Duke Energy',
        sector: 'Utilities',
        country: 'United States',
        expectedDirection: 'Neutral',
        timeHorizon: 'Long-term (1–5 years)',
        mechanismTemplate:
            'Utility capex plans adjust to grid reliability mandates emerging from {{event}}.',
        investabilityScore: 4,
        rationaleTemplate:
            'Regulated returns provide income stability; monitor regulatory lag as {{drivers}} evolve.',
        sources: ['State utility commission filings', 'Reuters power markets coverage'],
    },
    {
        ticker: 'HYG',
        company: 'iShares iBoxx High Yield Corp Bond ETF',
        sector: 'Financials',
        country: 'United States',
        expectedDirection: 'Bearish',
        timeHorizon: 'Short-term (0–3 months)',
        mechanismTemplate:
            '{{event}} could widen credit spreads as investors reprice default risk.',
        investabilityScore: 4,
        rationaleTemplate:
            'High beta credit faces drawdown risk if {{drivers}} undermine liquidity; consider hedges.',
        sources: ['ICE BofA High Yield Index data', 'Bloomberg credit strategy'],
    },
    {
        ticker: 'ASHR',
        company: 'Xtrackers Harvest CSI 300 China A ETF',
        sector: 'Emerging Markets',
        country: 'China',
        expectedDirection: 'Bearish',
        timeHorizon: 'Medium-term (3–12 months)',
        mechanismTemplate:
            '{{event}} may intensify regulatory pressure or capital restrictions impacting mainland equities.',
        investabilityScore: 3,
        rationaleTemplate:
            'Sensitivity to policy signals and global positioning makes ASHR a tactical hedge against {{drivers}}.',
        sources: ['PBOC policy announcements', 'Financial Times China markets coverage'],
    },
    {
        ticker: 'RKLB',
        company: 'Rocket Lab USA Inc.',
        sector: 'Space',
        country: 'United States',
        expectedDirection: 'Bullish',
        timeHorizon: 'Long-term (1–5 years)',
        mechanismTemplate:
            '{{event}} boosts demand for responsive launch and satellite deployment capabilities as governments realign space strategy.',
        investabilityScore: 5,
        rationaleTemplate:
            'Backlog growth and diversified missions tied to {{drivers}} increase visibility; monitor execution risk as production scales.',
        sources: ['US Space Force procurement releases', 'Bloomberg space economy coverage'],
    },
    {
        ticker: 'IONQ',
        company: 'IonQ Inc.',
        sector: 'Quantum Computing',
        country: 'United States',
        expectedDirection: 'Bullish',
        timeHorizon: 'Long-term (1–5 years)',
        mechanismTemplate:
            '{{event}} accelerates funding for quantum research, positioning IonQ to benefit from early commercial pilots.',
        investabilityScore: 4,
        rationaleTemplate:
            'Partnership pipeline aligned with {{drivers}} offers optionality; valuation volatility warrants staged exposure.',
        sources: ['National quantum initiative updates', 'Financial Times emerging technology coverage'],
    },
];

const BULLISH_KEYWORDS = ['stimulus', 'investment', 'recovery', 'growth', 'innovation', 'ai', 'alliances', 'easing', 'support'];
const BEARISH_KEYWORDS = ['sanction', 'recession', 'war', 'conflict', 'crackdown', 'ban', 'shortage', 'tightening', 'slowdown'];

const fillTemplate = (template: string, replacements: Record<string, string>): string => {
    return template.replace(/{{(.*?)}}/g, (_, key) => replacements[key.trim()] ?? '');
};

const dedupe = (values: string[]): string[] => {
    return Array.from(new Set(values.filter((value) => value.trim().length > 0)));
};

const determineSentiment = (text: string): Sentiment => {
    const normalized = text.toLowerCase();
    if (BEARISH_KEYWORDS.some((keyword) => normalized.includes(keyword))) {
        return 'Bearish';
    }
    if (BULLISH_KEYWORDS.some((keyword) => normalized.includes(keyword))) {
        return 'Bullish';
    }
    return 'Neutral';
};

const deriveMacroThemes = (drivers: string[], sentiment: Sentiment): string[] => {
    const baseThemes = ['Policy Trajectory', 'Cross-Border Capital Flows', 'Supply Chain Resilience'];
    const keywordThemes = drivers
        .map((driver) => driver.split(' ').slice(0, 3).join(' '))
        .map((fragment) => fragment.replace(/[^\w\s-]/g, '').trim())
        .filter((fragment) => fragment.length > 0);
    const sentimentTheme =
        sentiment === 'Bullish'
            ? 'Risk-On Rotation'
            : sentiment === 'Bearish'
            ? 'Defensive Positioning'
            : 'Selective Allocation';
    return dedupe([sentimentTheme, ...keywordThemes, ...baseThemes]).slice(0, 6);
};

const deriveSectorOutlook = (sentiment: Sentiment, drivers: string[], eventName: string): string[] => {
    const focus = drivers.slice(0, 2).join(' & ') || 'stated catalysts';
    const base = [
        `Technology platforms positioned to monetize ${focus}.`,
        `Energy and materials tracking commodity volatility around ${eventName}.`,
        `Financials adjusting capital deployment as policy visibility shifts.`,
        `Defensive sectors providing ballast amid execution risk.`,
    ];
    if (sentiment === 'Bullish') {
        base.unshift('Growth equities favored as liquidity expectations improve.');
    } else if (sentiment === 'Bearish') {
        base.unshift('Quality balance sheets and cash generative assets prioritized.');
    } else {
        base.unshift('Market likely stays range-bound with rotation within sectors.');
    }
    return base.slice(0, 5);
};

const buildHorizonImpacts = (sentiment: Sentiment, driversText: string, timeline: string): TimeHorizonImpact[] => {
    const base: Record<TimeHorizon, string> = {
        'Short-term (0–3 months)': `${sentiment} bias as headlines around ${driversText} drive volatility; monitor liquidity and spreads.`,
        'Medium-term (3–12 months)': `Execution against ${timeline} milestones will clarify earnings visibility and capital allocation.`,
        'Long-term (1–5 years)': `Structural implications for market share, supply chains, and policy regimes anchor strategic positioning.`,
    };
    return (Object.keys(base) as TimeHorizon[]).map((horizon) => ({
        horizon,
        outlook: base[horizon],
    }));
};

const buildEventContext = (input: EventInput): EventContext => {
    const eventName = input.name.trim() || 'Submitted strategic catalyst';
    const overview = input.description.trim() || 'Description pending—add narrative for richer context.';
    const timing = input.expectedTiming.trim() || 'Timing TBD—confirm expected announcement or implementation window.';
    const contextPoints = input.keyDrivers.filter((driver) => driver.trim().length > 0);

    const significance =
        contextPoints[0] ??
        'Detail the scale of capital flows, policy changes, or technology adoption expected from this catalyst.';

    if (contextPoints.length === 0) {
        contextPoints.push('Add key drivers such as policy levers, stakeholders, or technology triggers.');
    }

    return {
        overview: `${eventName}: ${overview}`,
        timing,
        significance,
        contextPoints: contextPoints.slice(0, 4),
    };
};

const buildOpportunities = (
    eventName: string,
    driversText: string,
    timeline: string,
    sentiment: Sentiment,
): OpportunityRow[] => {
    const replacements = {
        event: eventName,
        drivers: driversText,
        timing: timeline,
        sentiment,
    };

    return BASE_OPPORTUNITIES.map(({ mechanismTemplate, rationaleTemplate, ...rest }) => ({
        ...rest,
        mechanism: fillTemplate(mechanismTemplate, replacements),
        rationale: fillTemplate(rationaleTemplate, replacements),
    }));
};

export const buildMockReport = (input: EventInput): AssessmentReport => {
    const eventName = input.name.trim() || 'Strategic Market Catalyst';
    const drivers = input.keyDrivers.map((driver) => driver.trim()).filter((driver) => driver.length > 0);
    const driversText = drivers.length > 0 ? drivers.join('; ') : 'the stated catalysts';
    const timeline = input.expectedTiming.trim() || 'the specified timeline';
    const descriptionText = input.description.trim() || 'No narrative provided yet—supply qualitative colour for accuracy.';

    const sentiment = determineSentiment(`${descriptionText} ${driversText}`);
    const macroThemes = deriveMacroThemes(drivers, sentiment);
    const sectorOutlook = deriveSectorOutlook(sentiment, drivers, eventName);
    const horizonImpacts = buildHorizonImpacts(sentiment, driversText, timeline);
    const eventContext = buildEventContext(input);
    const opportunities = buildOpportunities(eventName, driversText, timeline, sentiment);

    const headlineSummary = `${eventName}: Preliminary ${sentiment.toLowerCase()} stance anchored on ${macroThemes[0] ?? 'macro reassessment'}.`;

    const marketImpact: MarketImpact = {
        sentiment,
        macroThemes,
        sectorOutlook,
        horizonImpacts,
    };

    const topTickers = opportunities.slice(0, 3).map((op) => op.ticker).join(', ');

    const summaryInsights = [
        `${eventName} screens as ${sentiment.toLowerCase()} with emphasis on ${macroThemes.slice(0, 3).join(', ')}.`,
        `Sector leadership likely features ${sectorOutlook.slice(0, 3).join(' ')}`,
        `Initial focus tickers: ${topTickers}; recalibrate sizing as milestones on ${timeline} emerge.`,
    ];

    const riskNote = `Scenario sensitivity remains elevated—validate assumptions on ${driversText} with real-time data, monitor policy communications, and size exposures within risk budget.`;

    const citations = [
        'IMF World Economic Outlook (latest edition)',
        'Bloomberg Terminal – Thematic Intelligence (placeholder)',
        'Reuters – Market Newswire (placeholder)',
    ];

    return {
        generatedAt: new Date().toISOString(),
        eventName,
        headlineSummary,
        eventContext,
        marketImpact,
        opportunities,
        summaryInsights,
        riskNote,
        citations,
    };
};
