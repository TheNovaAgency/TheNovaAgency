# AI Search, Answer Engines and Business Discovery (2025–2026)

Research date: 17 Nov 2026. Method: web search across ~27 queries. Important caveat: direct page fetches of several primary sources failed in this environment (similarweb.com AI search blog, sparktoro.com, pewresearch.org), so a number of figures below come from search-result extracts and secondary trade coverage (Search Engine Land/Journal, Press Gazette, PPC Land) rather than from the primary page. Where that is the case it is flagged "(secondary)". Vendor = a company that sells SEO/GEO tools or services; treat its findings as marketing-adjacent even when the data looks sound.

Evidence tiers used below:
- **Independent / academic / regulator:** Pew Research, Reuters Institute (Chartbeat data), academic field experiments (Wang et al.; Agarwal & Sen), UK CMA filings and decisions.
- **Vendor with large datasets (credible but commercially motivated):** Ahrefs, Seer Interactive (agency), Similarweb, SparkToro, BrightLocal, Authoritas, Semrush, AirOps, Evertune, Search Atlas.
- **Interested parties:** Google (platform defending itself), DMG Media and other publishers (litigants/complainants), Tollbit (publisher licensing marketplace).

---

## 1. Impact of Google AI Overviews / AI Mode on CTR and organic traffic; zero-click share

### Takeaway
Every independent and vendor dataset from 2025–2026 shows that clicks to websites fall substantially when an AI Overview appears: roughly -35% to -60% for the top organic result in correlational studies, and about -38% to -40% in the first causal (experimental) studies. AI Mode is far more "closed" than AI Overviews. Zero-click share of Google searches rose from ~58–60% (2024) to ~68% in early 2026 (US, SparkToro/Similarweb). Google disputes the scale, saying total clicks are "relatively stable" and quality is higher, but has not published supporting data. There is one partial counter-signal: Seer saw CTR on AIO queries rebound in early 2026.

### Cited Findings

**Pew Research Center (independent, July 22, 2025)**
- 900 US adults tracked in March 2025. Users clicked a result link on 8% of visits to pages with an AI summary vs 15% on pages without one, close to a 50% relative drop. — [Search Engine Journal](https://www.searchenginejournal.com/pew-research-confirms-google-ai-overviews-is-eroding-web-ecosystem/551825/); [The Register](https://www.theregister.com/2025/07/22/google_ai_overviews_suppress_search/)
- About 1% of visits involved a click on a source link inside the AI summary itself. — [The Decoder](https://the-decoder.com/pew-finds-that-only-1-percent-of-users-click-a-source-link-directly-from-googles-ai-overviews/)
- About 18% of Google searches in the March 2025 sample produced an AI summary. — [Search Engine Land](https://www.searchengineland.com/google-ai-overviews-hurting-clicks-study-459434/)
- Google disputed Pew's methodology. — [PPC Land](https://ppc.land/google-disputes-pew-study-showing-ai-overviews-reduce-clicks-by-half/)

**Ahrefs (vendor, large dataset, correlational)**
- April 2025 study: AI Overviews were associated with a 34.5% lower CTR for the #1 result (300k keywords). — [Ahrefs (Italian edition of the study)](https://ahrefs.com/it/blog/ai-overviews-reduce-clicks/)
- Updated study (dated Feb 2026 by secondary sources; press release circulated May 2026): top-result CTR was **58% lower** when an AI Overview was present. Based on 300k keywords (150k with AIO, 150k without) and GSC data from Dec 2023 to Dec 2025. Reported declines range from about -50.8% at position 2 to -19.4% at position 10. — [Business Wire press release, May 2026](https://businesswire.com/news/home/20260518322756/en/New-Research-Googles-AI-Overviews-Now-Cost-Websites-58-of-Their-Clicks); [Shopifreaks summary](https://www.shopifreaks.com/google-ai-overviews-now-reduce-top-ranking-pages-clickthrough-rates-by-58-according-to-new-ahrefs-research-analyzing-300000-keywords/)
- Ahrefs Japan follow-up (July 2026), using a predicted-vs-actual method: the US position-1 CTR gap widened from -58% (Dec 2025) to **-68.8% (June 2026)**, and Japan from -38% to -62.7%. Because the method differs, these are not directly comparable to the 58% figure. — [Ahrefs JP](https://ahrefs.com/ja/blog/ai-overviews-reduce-clicks-june-2026/)
- France rollout study: secondary write-ups report CTR cuts that are inconsistent with each other (3.4% within 9 days vs 23.1%). — [Ahrefs](https://ahrefs.com/blog/ai-overviews-france-impact/)

**Seer Interactive (agency; client GSC data)**
- Sept 2025 update covered 3,119 informational queries across 42 client organisations, June 2024 to Sept 2025. Organic CTR on AIO queries fell from 1.76% to 0.61% (-61%). Paid CTR on the same queries fell from 19.70% to 6.34% (-68%). Organic CTR on non-AIO queries also fell, by about 41% (2.72% to 1.62%). — [Search Engine Land](https://searchengineland.com/google-ai-overviews-drive-drop-organic-paid-ctr-464212); [Seer](https://www.seerinteractive.com/insights/aio-impact-on-google-ctr-september-2025-update)
- Brands cited in the AIO had an organic CTR of 0.70% vs 0.52% for uncited brands (+35%). Seer: "We cannot definitively prove that citation causes higher CTRs." — [Seer](https://www.seerinteractive.com/insights/aio-impact-on-google-ctr-september-2025-update)
- 2026 update covered 53 brands, 5.47M queries and 2.43B impressions, Jan 2025 to Feb 2026. CTR on AIO queries **rebounded** from a low of 1.3% (Dec 2025) to 2.4% (Feb 2026). Non-AIO CTR went from 2.8% to 3.8%. AIOs were triggered on 36% of informational, 8% of commercial and 5% of transactional queries, and on 95.4% of "comparison" queries. Cited brands earned about 120% more organic clicks per impression than uncited brands on the same queries. (Secondary; baselines differ between write-ups.) — [Seer 2026 update](https://seerinteractive.com/insights/aio-impact-on-google-ctr-2026-update); [Search Engine Land](https://searchengineland.com/google-ai-overviews-ctr-recovery-study-475566); [SEJ](https://www.searchenginejournal.com/ai-overview-ctr-fell-61-but-clicks-didnt-collapse/572993/)

**Academic / causal studies (strongest evidence)**
- Agarwal & Sen (SSRN, April 2026): AIOs appeared on about 42% of queries. Their presence cut outbound organic clicks by about 38–40%, and removing top-position AIOs nearly doubled outbound clicks. — [TSE seminar paper PDF](https://www.tse-fr.eu/sites/default/files/TSE/documents/sem2026/eco_platforms/agarwal_google_search_aio.pdf); [SEJ coverage](https://www.searchenginejournal.com/ai-overviews-cut-organic-clicks-38-field-study-finds/)
- The same coverage reports the study found no measurable improvement in user satisfaction proxies such as bounce or return-to-search. This directly challenges Google's "bounce clicks" argument. — [Pulse/SEJ summary](https://www.pulse.bot/digital-marketing/news/googles-ai-overviews-cut-clicks-without-satisfaction-gain-report-via-sejournal-mattgsouthern-38b7be57-73f8-47f8-bdd0-5373e8bee48b/)
- Wang et al. (preregistered field experiment, ~1,100 US users, 2026): forcing searches into **AI Mode** lowered external click-through by **18.8 percentage points** vs standard Search. — [TechWyse](https://www.techwyse.com/news/search-seo/google-ai-mode-reduces-publisher-clicks-study-2026); [Relevant Audience](https://www.relevantaudience.com/geo/ai-mode-field-experiment-clicks-drop-18-8-points/)
- A widely repeated claim that "AI Mode has a ~93% zero-click rate" (attributed to Semrush) appeared only in secondary sources. Unverified. — [TechWyse](https://www.techwyse.com/news/search-seo/google-ai-mode-reduces-publisher-clicks-study-2026)

**UK-specific**
- Authoritas (vendor) for a publisher complaint to the CMA, July 2025: in the UK, CTR was **-47.5% on desktop and -37.7% on mobile** when an AIO was present (news keywords, 16–22 April 2025). Average AIO penetration on news keywords was about 12.2%, but around 50% for health and horoscope. Google called it "inaccurate and based on flawed assumptions." — [Press Gazette](https://pressgazette.co.uk/publishers/digital-journalism/google-ai-overviews-publishers-report-clickthroughs-authoritas-report/)
- DMG Media (Daily Mail owner) told the CMA its desktop CTR fell from 25.23% on regular results to 2.8% with an AIO (-89%), with -87% on mobile. These are internal figures from an interested party and have not been independently audited. — [DMG Media CMA submission (gov.uk PDF)](https://assets.publishing.service.gov.uk/media/68a5aa50a6acbbc7fb96a3b2/DMG_Media.pdf); [Media Copilot](https://mediacopilot.ai/google-ai-overviews-publisher-traffic/)
- At a CMA publishers' roundtable on 7 July 2025, an unnamed publisher reported a 70% desktop and 52% mobile CTR drop on AIO queries. — [CMA roundtable summary PDF](https://assets.publishing.service.gov.uk/media/68a5b4e418658ad2023d5154/Publishers_roundtable_summary_7_July_2025.pdf)

**Zero-click share (SparkToro)**
- 2024 SparkToro/Datos study: 58.5% of US and 59.7% of EU Google searches ended without a click. Per 1,000 searches, 360 clicks (US) and 374 clicks (EU) went to the open web. — [SparkToro 2024](https://sparktoro.com/blog/2024-zero-click-search-study-for-every-1000-us-google-searches-only-374-clicks-go-to-the-open-web-in-the-eu-its-360/); [Search Engine Land](https://searchengineland.com/google-search-zero-click-study-443869)
- 2026 study (Similarweb panel, Jan–Apr 2026, US, excluding the Google app): about **68% of US Google searches ended without a click**, i.e. "less than one third send a click." AI Mode accounted for only 0.34% of searches in the period. SparkToro does not isolate how much of the rise is due to AIOs, and the data source changed from Datos to Similarweb, so the year-on-year comparison is approximate. — [SparkToro 2026](https://sparktoro.com/blog/in-2026-less-than-one-third-of-google-searches-still-send-a-click/); [Search Engine Land](https://searchengineland.com/google-zero-click-searches-2026-study-479717); [TechWyse](https://www.techwyse.com/news/reports-data/google-zero-click-searches-68-percent-2026)
- SEJ reported "Google search traffic to open web drops to 23%" (2026 data). — [SEJ](https://www.searchenginejournal.com/google-search-traffic-to-open-web-drops-to-23-data-shows/578724/)
- Conflict: one analysis notes a separate Datos/SparkToro Q1 2026 desktop-panel figure of 22.4% zero-click (March 2026), about three times lower. Definitions and panels drive large differences. — [Search Engine Land](https://searchengineland.com/google-zero-click-searches-2026-study-479717)

**Google's position (interested party)**
- Liz Reid (Head of Search), 6 Aug 2025: total organic click volume to websites is "relatively stable" year on year, and "quality clicks" (visits where users don't quickly bounce back) have increased. No data was published. — [Google blog](https://blog.google/products-and-platforms/products/search/ai-search-driving-more-queries-higher-quality-clicks/); [TechCrunch](https://techcrunch.com/2025/08/06/google-denies-ai-search-features-are-killing-website-traffic/)
- In later interviews (Bloomberg Odd Lots, 2026) she argued that AIOs mainly remove "bounce clicks," again without data. — [SEJ](https://www.searchenginejournal.com/google-pushes-bounce-clicks-explanation-for-ai-overview-traffic-loss/572986); [TechWyse](https://www.techwyse.com/news/search-news/google-liz-reid-bounce-clicks-ai-overviews-traffic-data)

### Inferences
- The direction of the effect is not in doubt. Magnitude depends on query type: informational and comparison queries are hit hardest, transactional and commercial much less (Seer trigger rates of 36% informational vs 5% transactional). For SMEs selling services, money queries are less exposed than blog/"how-to" content.
- Being cited inside the AIO partially mitigates the loss (Seer: +35% to +120% CTR vs uncited). This is the main quantitative argument for GEO/AEO, though it is correlational.
- AI Mode is a bigger long-term threat than AIOs, but its usage share was still tiny in early 2026 (0.34% of searches per SparkToro).
- Google's "stable clicks" claim can be technically true even if CTR falls, provided query volume grows. Businesses should judge by their own GSC data, not aggregate claims.

### Gaps
- The Pew primary page could not be fetched. Secondary sources commonly cite figures such as the share of sessions ending after an AIO page and the most-cited sources (Wikipedia, YouTube, Reddit), but these were not verified here.
- No BrightEdge or Amsive 2025–2026 figures surfaced in searches.
- No UK-specific zero-click share for 2026 was found. The 2024 EU figure (59.7%) is the nearest proxy.
- Seer's early-2026 CTR "rebound" is based on one agency's clients. It has not been corroborated independently, and Ahrefs' June 2026 data points the other way.

---

## 2. Referral traffic from ChatGPT, Perplexity, Gemini, Claude, Copilot: volume, trend and conversion quality

### Takeaway
AI referral traffic is growing fast but remains small. Similarweb measured about 770.7M AI-referred visits per month worldwide (June 2025 to May 2026), more than double the prior year. ChatGPT still sends about 76–80% of AI referrals, but its share of AI-assistant usage is eroding as Gemini rises. Conversion evidence is mixed: several vendor studies show higher per-visit conversion for AI referrals, while others (including Adobe and an academic paper) show lower conversion. The consistent finding is that absolute revenue from AI referrals is a tiny fraction of organic.

### Cited Findings
**Volume and share**
- AI platforms drove an average of **770.7M referral visits per month** worldwide, June 2025 to May 2026, more than double the previous year (Similarweb; secondary). — [Similarweb AI referral by industry](https://aisearch.similarweb.com/blog/ai-referral-traffic-by-industry/); [Similarweb gen-AI stats](https://aisearch.similarweb.com/blog/gen-ai-stats/)
- ChatGPT's share of AI referral traffic was about 79.7% in 2025 and 76.0% in 2026 (SE Ranking analysis citing panel data; indicative only). — [SE Ranking via search extract](https://seranking.com/blog/chatgpt-referral-traffic-may-2026/)
- ChatGPT's share of visits to generative-AI websites fell from about 76% (June 2025) to about 53% (May 2026), while Gemini rose from under 9% to about 27–28%. This measures visits to AI tools, not referrals they send. — [PPC Land](https://ppc.land/chatgpts-lead-shrinks-as-gemini-surges-in-ai-traffic-war/); [Tom's Guide](https://www.tomsguide.com/ai/chatgpts-traffic-share-hits-lowest-point-since-2023-as-gemini-surges-new-report-exposes-pressure-on-openai); [PPC Land: ChatGPT 52.7%, Claude triples share](https://ppc.land/chatgpt-drops-to-52-7-as-claude-triples-its-ai-traffic-share)
- After OpenAI's 7 May 2026 search update, ChatGPT referral traffic "near-tripled," and the share landing on homepages rose from about 25% to nearly 60% within three weeks. 65% of cited URLs were 2–3 folders deep, yet 58.8% of AI referral traffic landed on homepages. — [Similarweb](https://aisearch.similarweb.com/blog/chatgpt-referral-traffic-triples/)
- Similarweb: AI search is "layering on top" of Google rather than replacing it, since ChatGPT users keep using Google. — [SEJ](https://searchenginejournal.com/ai-search-isnt-replacing-google-its-layering-on-top-similarweb-data/583378/); [Let's Data Science](https://letsdatascience.com/news/similarweb-finds-chatgpt-adds-to-rather-than-replaces-google-1e2ad8c8)
- In Australia, ChatGPT drives about 90% of AI website traffic. — [SmartCompany](https://www.smartcompany.com.au/artificial-intelligence/chatgpt-drives-90-ai-website-traffic-in-australia-converts-worse-than-perplexity-gemini/)

**Conversion quality: higher**
- Visibility Labs (94 ecommerce brands, 2025): ChatGPT referrals converted at 1.81% vs 1.39% for non-branded organic, and beat organic in 10 of 12 months. However, average order value was $204 vs $238, and revenue was $474k vs $32.1M from non-branded organic, on 135k vs 9.46M sessions. — [Search Engine Land](https://searchengineland.com/chatgpt-vs-non-branded-organic-search-conversions-470321)
- Seer (single B2B SaaS client): ChatGPT referrals converted at 15.9% vs 1.76% for Google organic. Not representative. — [Seer](https://www.seerinteractive.com/insights/case-study-6-learnings-about-how-traffic-from-chatgpt-converts)
- Similarweb (Sept 2025): ChatGPT-referred visits converted at 11.4% vs 5.3% for organic search (secondary). — [PPC Land](https://ppc.land/ai-traffic-converts-at-3x-higher-rates-than-traditional-channels/)
- Ahrefs (own site): AI search visitors were 0.5% of traffic but 12.1% of signups. — [Ahrefs via search extract](https://ahrefs.com/blog/llm-search)

**Conversion quality: lower**
- Academic paper in *Marketing Science* (Frontiers, 973 ecommerce sites, Aug 2024 to Jul 2025): ChatGPT referrals converted worse than Google search, email and affiliates, although conversion rate and revenue per session from ChatGPT improved over time. It also cites Adobe 2025 data showing LLM-referral conversion 9% lower than non-AI channels. — [INFORMS Marketing Science](https://pubsonline.informs.org/doi/full/10.1287/mksc.2025.0489); [Search Engine Land](https://searchengineland.com/llms-google-referral-conversion-study-463747); [Modern Retail, Oct 2025](https://www.modernretail.co/technology/e-commerce-sites-see-low-sales-from-chatgpt-traffic-study-finds-but-that-could-change/)
- Australian ecommerce study: AI-referred users purchased at 2.9% vs 6.0% for organic, and Perplexity/Gemini traffic converted better than ChatGPT traffic. — [SmartCompany](https://www.smartcompany.com.au/artificial-intelligence/chatgpt-drives-90-ai-website-traffic-in-australia-converts-worse-than-perplexity-gemini/)

### Inferences
- For B2B and lead-gen businesses, the higher-intent finding (Seer, Ahrefs) is more relevant than the ecommerce studies. AI users often arrive pre-qualified after a comparison conversation. Ecommerce evidence is genuinely mixed.
- "AI traffic converts 4–23x better" headlines are cherry-picked from small samples. The honest framing is: similar or higher per-visit conversion in many B2B cases, tiny volume, and growing.
- The surge in homepage landings after May 2026 means brand and homepage clarity (what you do, for whom, where) matters more for AI-referred visitors.
- Measured AI referrals are a floor, not the true figure. App traffic often has no referrer (see section 5), and many AI influences produce no click at all (brand recall leading to a later direct or branded search).

### Gaps
- Per-platform referral volumes for Perplexity, Claude and Copilot in 2026 were not reliably found, apart from qualitative "Claude tripled its share" headlines.
- No figure was found for AI referrals as a share of total website traffic in 2026. Commonly quoted "~1%" figures were not verified here.
- No UK-specific AI referral or conversion data was found.

---

## 3. Publisher and business evidence of traffic declines

### Takeaway
News publishers show large, documented search declines. Chartbeat data (via the Reuters Institute) shows Google search traffic to 2,500+ publishers down 33% globally and 38% in the US (Nov 2024 to Nov 2025), with small publishers down about 60% over two years. Chegg is the canonical corporate casualty, though AIO causation is disputed. UK regulatory filings (DMG Media, Authoritas, CMA roundtable) are the main UK evidence. The CMA responded in June 2026 with a binding AI opt-out for publishers.

### Cited Findings
- Reuters Institute *Trends and Predictions 2026* (Chartbeat data): Google search traffic to 2,500+ sites fell 33% globally and 38% in the US, Nov 2024 to Nov 2025. Lifestyle and utility content (weather, TV guides, horoscopes) was hit hardest. Publishers expect search traffic to fall by more than 40% (43% average) over the next three years. — [Reuters Institute PDF](https://reutersinstitute.politics.ox.ac.uk/sites/default/files/2026-01/Newman%20-%20Trends%20and%20Predictions%202026%20FINAL.pdf); [Press Gazette](https://pressgazette.co.uk/publishers/digital-journalism/google-traffic-down-2025-trends-report-2026/); [Oxford Politics dept](https://www.politics.ox.ac.uk/news/news-publishers-expect-search-traffic-fall-more-40-next-three-years-new-risj-report-finds)
- Chartbeat via Axios (March 2026): search referral traffic to small publishers fell 60% over two years. — [PPC Land](https://ppc.land/small-publishers-lost-60-of-search-traffic-as-ai-reshapes-the-web/)
- Google Discover trend figures conflict between sources (-21% vs -2% globally). — [Press Gazette](https://pressgazette.co.uk/publishers/digital-journalism/google-traffic-down-2025-trends-report-2026/)
- Digital Content Next (US publishers): Google search referrals fell 10% year on year on average (2025). — [Press Gazette](https://pressgazette.co.uk/media-audience-and-business-data/uk-and-us-publishers-says-google-ai-is-harming-website-traffic/)
- **Chegg:** sued Google in Feb 2025 over AI Overviews. In May 2025 it cut 22% of staff (~248) after Q1 2025 revenue fell 30% year on year, and its CEO blamed AIOs. A second round (~388 staff) followed in Oct 2025 (single source). Semrush data shows organic traffic falling from 5.6M to 3.7M (-34%). — [TechRadar](https://www.techradar.com/pro/chegg-announces-move-to-reduce-workforce-by-22-percent-as-students-turn-to-ai); [Tom Tunguz](https://tomtunguz.com/chegg-aio/)
- Counterpoint on Chegg: Growth Memo argues that Chegg's traffic rose after AIOs launched in May 2024, only fell from Oct 2024, and that total traffic had already been declining before ChatGPT. AI accelerated an existing decline. — [Growth Memo](https://www.growth-memo.com/p/cheggmate)
- **DMG Media** (CMA evidence, 2025): -89% desktop and -87% mobile CTR on AIO results (see section 1). It also cites Tollbit data: AI search cuts CTR by 91% and chatbots by 96%. Tollbit is not independent. — [DMG Media CMA PDF](https://assets.publishing.service.gov.uk/media/68a5aa50a6acbbc7fb96a3b2/DMG_Media.pdf); [later DMG submission](https://assets.publishing.service.gov.uk/media/69b970da26909a142396128e/DMG_Media.pdf)
- **UK CMA:** designated Google with strategic market status in general search (Oct 2025). On **3 June 2026** it imposed binding conduct requirements. UK publishers can opt out, at directory and page level, of Google AI features (AI Overviews, AI Mode, Gemini, Vertex AI) and of fine-tuning, without losing standard search ranking. Google is barred from retaliatory down-ranking. Attribution through clear links is required, and Google has about nine months to implement. Critics point out that use remains the default (opt-out, not opt-in). — [Courthouse News](https://courthousenews.com/uk-forces-google-to-let-publishers-opt-out-of-ai-overviews/); [Advanced Television](https://www.advanced-television.com/2026/06/03/cma-imposes-google-publisher-ai-opt-out/); [Decision Marketing](https://www.decisionmarketing.co.uk/news/cma-forces-google-to-give-publishers-greater-control); [Digiday](https://digiday.com/media/googles-forced-ai-opt-out-what-changes-and-what-doesnt-for-publishers)
- Publishers have asked the CMA to bring Gemini into scope. — [Press Gazette](https://pressgazette.co.uk/publishers/publishers-call-for-cma-to-include-gemini-in-google-investigation/)

### Inferences
- The most damaged content type is "answerable" informational and utility content. SME service sites whose traffic depends on blog "how-to" articles are exposed in the same way. Local and transactional pages are less exposed.
- The CMA opt-out is mostly relevant to publishers. For an SME that wants to be recommended, opting out of AI features would usually be self-defeating.
- Attribution of declines to AI is often contested (Chegg). Businesses should segment their own GSC data by query type before blaming AIOs.

### Gaps
- No sourced HubSpot organic traffic decline figures were found. Widely circulated claims of HubSpot blog traffic collapsing (2024–25) could not be verified in this research and should not be cited without a primary source.
- The exact CMA implementation deadline and the form of the Search Console tooling come from limited sources.

---

## 4. What gets a business cited by AI answer engines: evidence vs speculation

### Takeaway
The best-supported levers are: (1) ranking well in conventional search, since Google says AI features use the same index and ranking and AIO citations correlate with organic rank; (2) **off-site brand mentions** (Ahrefs: mentions correlate 0.664 with AIO visibility vs 0.218 for backlinks); (3) presence on community and third-party platforms (Reddit, YouTube, reviews, directories), which differs by engine; and (4) content freshness. Weak or unsupported: **llms.txt** (97% of files get zero requests; Google says it's not needed), schema as a direct citation signal (null results in controlled tests), and "chunking"/AI-specific rewriting (Google explicitly says it doesn't help). Google's own May 2026 guide states that GEO/AEO is essentially SEO.

### Cited Findings
**Google's official guidance**
- 15 May 2026: Google Search Central published "Optimizing your website for generative AI features on Google Search" (updated 10 July 2026). It says AI Overviews and AI Mode draw on the same index and ranking systems, so success "starts with succeeding in search." It lists as **not needed or not helpful**: llms.txt, special AI text files or Markdown, content chunking, AI-specific rewriting, inauthentic brand mentions, and over-reliance on structured data. (Secondary; the Google page was not fetched.) — [SEJ](https://searchenginejournal.com/googles-new-ai-search-guide-calls-aeo-and-geo-still-seo/575026); [Semrush](https://www.semrush.com/blog/google-publishes-generative-ai-search-guide/); [TechWyse](https://www.techwyse.com/news/ai-search/google-ai-search-optimization-guide-llms-txt-lighthouse-audit)
- Google's guidance on llms.txt varies by product: Lighthouse has an experimental "agentic browsing" audit treating llms.txt as optional. — [SEJ](https://www.searchenginejournal.com/googles-llms-txt-guidance-depends-on-which-product-you-ask/517651/)

**Off-site mentions and authority**
- Ahrefs (75k brands, 26 May 2025): branded web mentions had a Spearman correlation of 0.664 with AIO brand visibility, branded anchors 0.527, branded search volume 0.392, backlinks 0.218, and branded ad spend about 0.215. Top-quartile brands by mentions averaged 169 AIO mentions vs 14 for the next quartile, and the bottom half had about 0–3. Ahrefs notes correlation ≠ causation. — [Ahrefs](https://ahrefs.com/blog/ai-overview-brand-correlation/)
- A reported Dec 2025 Ahrefs follow-up (YouTube mentions ~0.737, extended to ChatGPT/AI Mode) appears only on Medium and is **unverified**. — [Medium](https://medium.com/@lorenzoswanson786/ahrefs-studied-75-000-brands-brand-mentions-beat-backlinks-3-to-1-for-ai-visibility-e86ef9f6baba)
- Moz 2026 (via CMSWire): 88% of Google AI Mode citations do not come from the organic top 10, so ranking alone does not guarantee AI Mode citation. — [CMSWire](https://www.cmswire.com/digital-marketing/does-structured-data-actually-improve-answer-engine-citations/)

**Community and third-party platforms**
- Evertune: Reddit accounted for up to about 1 in 5 Perplexity citations. No other model weighted one domain so heavily. — [Evertune](https://www.evertune.ai/resources/insights-on-ai/perplexity-loves-reddit-exploring-llms-top-sources)
- AirOps 2026 State of AI Search: about 48% of citations come from community platforms (Reddit, YouTube), and more than 50% of cited pages had been refreshed within six months. Evertune's methodology finds much lower concentration, which conflicts with this. — [AirOps](https://www.airops.com/report/the-2026-state-of-AI-search)
- The share of ChatGPT citations going to Wikipedia is contested: 47.9% in one study vs about 5% per Evertune. — [CMSWire/search extract](https://www.cmswire.com/digital-marketing/does-structured-data-actually-improve-answer-engine-citations/); [Evertune](https://www.evertune.ai/resources/insights-on-ai/perplexity-loves-reddit-exploring-llms-top-sources)
- Similarweb found brands get a measurable "shopper pickup" when AI names them (e.g. Capital One +14.2%). — [PPC Land](https://ppc.land/capital-one-gains-14-2-shopper-pickup-when-ai-names-it-similarweb-finds/)

**Structured data / schema**
- An Ahrefs difference-in-differences study of 1,885 pages found that adding schema produced statistically insignificant citation changes in AI Mode and ChatGPT, and a slight decline in AIOs. Caveat: the pages were already heavily cited. Search Atlas also found schema coverage is not a citation signal. — [CMSWire](https://www.cmswire.com/digital-marketing/does-structured-data-actually-improve-answer-engine-citations/); [Search Atlas](https://searchatlas.com/limits-of-schema-markup-for-ai-search)
- Pro-schema claims (e.g. "2.3x more citations," "+44% with FAQ schema") come from non-peer-reviewed vendor or community posts. — [DEV Community](https://dev.to/aivisbiz/i-audited-500-websites-json-ld-is-the-1-factor-for-ai-citation-29m4); [Hashmeta](https://hashmeta.com/insights/ai-search-citation-study)

**Freshness**
- Several vendor sources report that recency correlates with citation: "content updated within 30 days gets 3.2x more citations" (unverified), and AirOps reports more than 50% of cited pages were refreshed within six months. — [AirOps](https://www.airops.com/report/the-2026-state-of-AI-search); [DEV Community](https://dev.to/watsonfoglift/what-actually-makes-ai-search-engines-cite-your-website-the-research-data-4d82)

**llms.txt**
- Ahrefs (June 2026, secondary): a server-log study of 137k domains found 28% had an llms.txt file, but **97% of those files received zero requests** in May 2026. — [PPC Land](https://ppc.land/llms-txt-adoption-rises-8-8x-but-97-of-files-get-zero-ai-requests/); [SEO Sherpa](https://seosherpa.com/97-of-llms-txt-files-are-never-read/)
- Otterly 90-day test: 84 of more than 62,100 AI bot visits (~0.1%) touched llms.txt. A 12-week, 83-site study found OpenAI's crawler read it 7 times vs 3,990 robots.txt fetches, while Meta's crawler was an outlier that did fetch it. — [Optimizely](https://www.optimizely.com/field-notes/articles/does-llms-txt-work/); [Evil Martians](https://evilmartians.com/chronicles/which-ai-actually-reads-your-site-two-months-of-llm-traffic-measured)
- John Mueller (Google): no AI service has said it uses llms.txt. — [PPC Land](https://ppc.land/llms-txt-adoption-stalls-as-major-ai-platforms-ignore-proposed-standard/)

**Bing / Copilot / IndexNow**
- Bing Webmaster Tools added an **AI Performance report** (public preview, 10 Feb 2026). It shows citations in Copilot, Bing AI summaries and some partners, including cited pages and sample "grounding queries." Later additions include Intents, Topics, Citation Share and Compare reports. Microsoft says the report is sampled and is not a ranking signal. It is free, and sites can be imported from GSC. — [Previsible](https://previsible.io/seo-ai-news/bing-ai-performance-report/); [PPC Land](https://ppc.land/bing-gives-publishers-first-look-at-how-ai-systems-cite-their-content/); [Practical Ecommerce](https://www.practicalecommerce.com/bings-improved-ai-performance-section)
- IndexNow is recommended in setup workflows (notify Bing of changes), but no evidence was found linking it to higher AI citation rates. — [GEO Toolbox](https://geotoolbox.ai/blog/bing-webmaster-tools)

### Inferences
- **Evidence-backed (do):** strong conventional SEO and indexability in both Google and Bing; earning genuine third-party mentions (press, industry lists, review sites, directories, Reddit/YouTube where your audience is); keeping key pages fresh and dated; clear, factual brand and entity information that is consistent everywhere; monitoring Bing AI Performance.
- **Plausible but weakly evidenced:** schema (still useful for rich results and entity clarity, but not proven to drive AI citations); IndexNow (useful for fast Bing indexing, which feeds Copilot and some ChatGPT search grounding, but there is no direct evidence on citations).
- **Hype / not supported:** llms.txt as an AI-visibility lever; "chunking" or rewriting content "for LLMs"; buying or faking mentions (Google explicitly lists inauthentic brand mentions).
- Engines differ (Perplexity is Reddit-heavy, AIO tracks organic rank more closely than AI Mode or ChatGPT), so multi-surface presence beats single-engine tactics.

### Gaps
- No peer-reviewed study isolates the causal effect of reviews or entity consistency on AI citation outside the local context (see section 6).
- The original Princeton "GEO" academic paper (2023/24) was not re-checked in this pass.
- Whether ChatGPT search still relies on Bing's index in 2026 was not confirmed.

---

## 5. Tools for measuring AI visibility and GA4 tracking of AI referrals

### Takeaway
A crowded tool market has emerged (Profound, Semrush AI Visibility Toolkit, Ahrefs Brand Radar, Peec, Otterly and others) with prices from about $99/month to several hundred. All of them sample prompts, so results are indicative, not a census. Free first-party data is now available: Bing's AI Performance report (Feb 2026) and GA4's native "AI Assistant" channel (13 May 2026). GA4 undercounts because AI apps often send no referrer and Perplexity was reportedly not in the default rule.

### Cited Findings
- GA4 added an **"AI Assistant" channel** to the Default Channel Group on 13 May 2026. It is automatic and forward-only (no backfill). Google's documentation names ChatGPT, Gemini and Claude as examples, while Perplexity was reportedly still routed to Referral. — [SEO-Day](https://www.seo-day.de/news/article/ga4-adds-ai-assistant-channel-for-referral-tracking?lang=en); [Elevarus](https://elevarus.com/ga4-ai-assistant-channel-google-analytics-may-2026/); [Something Inc](https://somethinginc.com/blog/ga4-ai-assistant-channel-limitations/)
- A custom channel group (with the AI rule placed above Referral) can be applied retroactively and catch more sources. ChatGPT mobile-app visits often arrive as Direct with no referrer, so reported AI traffic is a minimum. — [SEJ](https://searchenginejournal.com/ga4s-ai-assistant-channel-undercounts-your-ai-traffic-how-to-build-one-that-doesnt/580133)
- Semrush AI Visibility Toolkit: about $99/month standalone with 25 custom prompts. Ahrefs Brand Radar: about $199 per AI index or $699 for all (pricing varies by source). Profound is positioned as the enterprise standalone (entry tier reportedly ~$99/month, ChatGPT-only). Brand Radar also covers YouTube, TikTok and Reddit. Most comparison pages are vendor- or affiliate-authored. — [Datadab comparison](https://www.datadab.com/research/ahrefs-brand-radar-vs-semrush-ai-toolkit-vs-profound); [Superlines](https://www.superlines.io/articles/best-ai-visibility-tools); [Detailed](https://detailed.com/ai-visibility-tools-pricing/)
- BrightLocal offers a local AI visibility tool. — [BrightLocal](https://www.brightlocal.com/local-seo-tools/local-ai-visibility)
- Bing Webmaster Tools AI Performance: free, but Microsoft surfaces only (see section 4). — [Previsible](https://previsible.io/seo-ai-news/bing-ai-performance-report/)
- HubSpot has AEO metrics, prompt and recommendation tooling in its platform (its MCP exposes `get_aeo_metrics` / `manage_aeo_prompts`). No independent evaluation of the HubSpot AEO Grader was found.

### Inferences
- For SMEs, a sensible low-cost stack is: GA4 AI Assistant channel plus a custom regex channel; Bing AI Performance; GSC (AIO and AI Mode clicks are folded into "Web" search data); and a small fixed prompt set checked monthly, by hand or with an entry-tier tool.
- Paid trackers are most useful for share-of-voice trends versus competitors. Absolute numbers are unstable because LLM answers vary from run to run.

### Gaps
- No independent accuracy or variance benchmarking of AI visibility tools was found. Prompt volatility data was not surfaced.
- Whether Google Search Console separates AI Mode data in 2026 was not verified in this pass.
- No independent review of HubSpot's AEO Grader was found.

---

## 6. Local / SME angle: "near me", local search and Google Business Profile in AI answers

### Takeaway
Consumer use of AI for local recommendations jumped in a year: BrightLocal's 2026 survey found 45% of consumers used AI tools for local recommendations, up from 6%, while Google fell from 83% to 71% (still dominant). AI engines recommend few businesses: AIOs are the most restrictive, and SOCi found ChatGPT recommends only 1.2% of local locations. ChatGPT's local answers have historically drawn mainly on business websites, then third-party mentions and directories. Most AI users (88%) say they verify what AI tells them, which sends them back to reviews, GBP and websites.

### Cited Findings
- BrightLocal Local Consumer Review Survey 2026 (secondary): 45% of consumers used AI tools for local business recommendations, up from 6% the previous year. Google use for local discovery fell from 83% to 71%, and Facebook rose from 40% to 49%. — [DesignRush](https://news.designrush.com/ai-local-business-discovery-website-strategy); [Insites](https://insites.com/blog/6-to-45-in-a-year-what-the-ai-adoption-curve-means-for-your-clients-google-business-profiles/)
- Of 455 respondents who used AI for local recommendations, 88% said they check sources or verify legitimacy. — [Bill Hartzer](https://www.billhartzer.com/?p=18508)
- BrightLocal Local AI Visibility study: 200,085 localised searches across 1,300 business locations on ChatGPT, Google AI Mode and AIOs. ChatGPT returns 4+ businesses per prompt on average, and AIOs return by far the fewest recommendations. — [BrightLocal](https://www.brightlocal.com/research/local-ai-visibility-study/)
- SOCi 2026 index: ChatGPT recommends just 1.2% of local business locations (different methodology). — [National Law Review](https://natlawreview.com/press-releases/ai-search-recommends-only-12-local-businesses-rest-are-invisible)
- BrightLocal ChatGPT sources study (circa late 2024/2025): for local queries, business websites made up 58% of sources, business mentions 27% and directories 15%. Reddit and Quora did not appear. — [BrightLocal](https://www.brightlocal.com/learn/local-seo/uncovering-chatgpt-search-sources/)
- BrightLocal also analysed which directories AI cites. — [BrightLocal AI directory sources](https://www.brightlocal.com/resources/ai-directory-sources/)
- Claims that AIOs appear on 58–68% of local-services queries (Presence.ai, Q1 2026) are unverified. — [The Stacc](https://thestacc.com/blog/ai-overviews-local-search/)
- Seer data shows transactional queries trigger AIOs least often (5% in Feb 2026), which suggests "book a plumber"-type queries remain more click-friendly than informational ones. — [Search Engine Land](https://searchengineland.com/google-ai-overviews-ctr-recovery-study-475566)

### Inferences
- For local SMEs, Google Business Profile (categories, services, reviews, photos, posts) and the local pack still matter most, because Google remains the majority channel and AI Mode and AIOs draw on Google's local data.
- In ChatGPT and other LLMs, the business's own website plus consistent mentions in directories and local press appear to be the main inputs. NAP and entity consistency is therefore a reasonable, low-cost hygiene step, though causal evidence is thin.
- Because AI engines shortlist only a handful of businesses (AIOs are tightest), visibility becomes winner-takes-most. Review volume and rating, and being named on "best X in [town]" lists, plausibly decide who gets shortlisted. This is an inference, not proven.

### Gaps
- No UK-specific data was found on AI use for local discovery. BrightLocal surveys are US-weighted, and UK breakouts were not located.
- No primary Google statement was found on how GBP data is used in AI Mode local answers, and no 2026 BrightLocal breakdown of ChatGPT local source types.
- No independent data was found on how "near me" query volumes or CTR have changed under AI Mode.
