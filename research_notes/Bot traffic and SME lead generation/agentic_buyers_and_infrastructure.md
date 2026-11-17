# AI Agents as Buyers and the New Web Infrastructure for an Agent-Heavy Internet (2025–2026)

> Research method note (Nov 2026): page fetching (WebFetch) was blocked by the session network for every host tried (hypotenuse.ai, visa.co.uk, developers.cloudflare.com), so findings come from search-result summaries of the cited pages, not full-page reads. Exact figures should be spot-checked against the primary page before publication. Items marked "[background, unverified this session]" come from prior knowledge and were not re-confirmed by a search in this session. Many search hits were agency/vendor blogs; these are flagged as secondary.

## 1. Agentic commerce status: who has shipped what, adoption, timelines, UK availability

### Takeaway
Agentic commerce went from launches (Apr–Nov 2025) to a partial retreat and re-shaping in 2026: OpenAI retired standalone Instant Checkout in March 2026 and now routes buyers to merchant checkout, while Google (UCP + AP2) and Shopify (Agentic Storefronts) keep building, and Visa/Mastercard went "live" in Europe in mid-2026 but at pilot scale. For UK consumers, agents are overwhelmingly a **discovery and comparison** channel in late 2026; in-chat/agent checkout is mostly US-only.

### Cited Findings

**OpenAI – Instant Checkout / Agentic Commerce Protocol (ACP, with Stripe)**
- ACP launched 29 Sept 2025, co-developed by OpenAI and Stripe and open-sourced; Instant Checkout launched with it in ChatGPT (US) — [OpenAI: Buy it in ChatGPT](https://openai.com/index/buy-it-in-chatgpt/); [Nembol ACP guide](https://www.nembol.com/blog/agentic-commerce-protocol)
- A ~4% merchant fee on Instant Checkout purchases was reported for the initial phase (secondary sources) — [Hypotenuse summary](https://www.hypotenuse.ai/blog/chatgpts-instant-checkout-the-next-phase-of-agentic-commerce)
- March 2026: OpenAI moved away from standalone Instant Checkout, prioritising shopping discovery and merchant-owned checkout; OpenAI said v1 "did not offer the level of flexibility that we aspire to provide" and "Instant Checkout is moving to Apps" (merchant apps inside ChatGPT with their own checkout/delegated payments) — [Digital Commerce 360, 6 Mar 2026](https://www.digitalcommerce360.com/2026/03/06/openai-shifts-checkout-plans-agentic-commerce-strategy/amp/); [Checkout.com analysis](https://www.checkout.com/blog/openai-agentic-commerce-shift)
- Dates of the shutdown vary across sources (4 March vs CNBC-confirmed 20 March 2026) — [heylumio](https://www.heylumio.ai/blog/openai-product-discovery-chatgpt); [The Keyword](https://www.thekeyword.co/news/openai-chatgpt-instant-checkout-scrapped)
- Forrester: "the leader in agentic commerce just pulled back"; native Shopify checkout in ChatGPT is gone — [Forrester blog](https://www.forrester.com/blogs/what-it-means-that-the-leader-in-agentic-commerce-just-pulled-back)
- Unverified secondary claims: only ~30 Shopify stores went live vs ~1M promised; "near-zero sales" after ~5 months — [Hypotenuse](https://www.hypotenuse.ai/blog/chatgpts-instant-checkout-the-next-phase-of-agentic-commerce) (treat as unverified)
- As of Oct 2026, ACP remains open to build against but checkout is limited to approved partners — [The Hack Academy](https://www.thehackacademy.com/agentic-commerce-protocol-partner-checkout.htm)
- OpenAI says shopping in ChatGPT is live for US users and will expand to other regions over time — via [Shopify UK blog / UK guides](https://www.shopify.com/uk/blog/agentic-commerce); [aamservices.uk](https://aamservices.uk/blog/agentic-commerce-uk-shops)

**Google – AI Mode agentic checkout, Universal Commerce Protocol (UCP), Agent Payments Protocol (AP2)**
- AP2 announced Sept 2025 as an open protocol for agent-initiated payments using cryptographically signed "mandates" proving user authorisation [background, unverified this session; described in] — [eco.com AP2 explainer](https://eco.com/support/en/articles/15192002-ap2-protocol-explained-google-s-agentic-commerce-standard-2026)
- Agentic checkout debuted in the US in Nov 2025 with select US merchants — [eSEOspace](https://eseospace.com/blog/google-agentic-checkout-explained/)
- UCP announced January 2026 as an open standard covering discovery, checkout and after-sales — [TechCrunch, 11 Jan 2026](https://www.techcrunch.com/2026/01/11/google-announces-a-new-protocol-to-facilitate-commerce-using-ai-agents/); [Google UCP developer guide](https://developers.google.com/merchant/ucp/)
- Google Merchant Center: UCP-powered checkout button on eligible listings in AI Mode and Gemini; eligibility listed as US, Canada and Australia for participating merchants — [Google Merchant Center Help](https://support.google.com/merchants/answer/16837055?hl=en)
- Google I/O (19 May 2026): AP2 expanded so agents can transact against pre-set rules (brands, products, budget guardrails), rolling out across Google products starting with "Gemini Spark" (single agency source) — [Azoma](https://www.azoma.ai/insights/google-i-o-2026-what-the-agentic-commerce-announcements-mean-for-brands)
- Walmart's OnePay adopted AP2 as a credentialed provider — per press release summarised in [search results, eco.com](https://eco.com/support/en/articles/15192002-ap2-protocol-explained-google-s-agentic-commerce-standard-2026)
- UK: no confirmed UK launch of agentic *checkout*; Canada expansion reported 4 Nov 2026; UK AI Mode **restaurant booking** launched ~10 April 2026 with eight partners (booking completes on partner platform) — [BigCommerce UK](https://www.bigcommerce.co.uk/articles/ecommerce/google-agentic-checkout/); [TechBuzz](https://www.techbuzz.ai/articles/google-deploys-ai-agents-for-uk-restaurant-bookings); [PPC Land](https://ppc.land/google-steers-holiday-hotel-dinner-and-ticket-bookings-into-ai-mode/)
- eMarketer: AI-driven checkout will "remain small for the foreseeable future"; the impact is on discovery — [eMarketer](https://www.emarketer.com/topics/category/google/3)

**Shopify**
- Agentic Storefronts are on by default for eligible stores; products reach ChatGPT, Copilot and Meta via Shopify Catalog and Google AI Mode/Gemini via Google & YouTube channel/Merchant Center; merchants reported as UCP-enabled by default — [Shopify UK blog](https://www.shopify.com/uk/blog/agentic-commerce); [kaspianfuad.com](https://kaspianfuad.com/blog/shopify-agentic-storefronts-explained/)
- Shopify: purchasing across these channels is currently available **to US buyers only**; UK stores selling to US buyers can participate; no fees for selling via Agentic Storefronts — [aamservices.uk citing Shopify](https://aamservices.uk/blog/agentic-commerce-uk-shops); [Shopify UK](https://www.shopify.com/uk/blog/agentic-commerce)
- Shopify notes Google Analytics and custom pixels do **not** fire in Copilot or Google direct checkout (attribution blind spot) — [kaspianfuad.com](https://kaspianfuad.com/blog/shopify-agentic-storefronts-april-2026-update/)
- Shopify "AI commerce at scale" announcement — [Shopify News](https://www.shopify.com/news/ai-commerce-at-scale)

**Amazon – Buy For Me, Rufus, Alexa+; and the Perplexity lawsuit**
- Buy For Me lets users buy from other brands' sites from within the Amazon app; Rufus recommends and manages carts; Rufus "Auto Buy" can purchase when an item hits a target price — [CNBC, 24 Dec 2025](https://www.cnbc.com/2025/12/24/amazon-faces-a-dilemma-fight-ai-shopping-agents-or-join-them.html); [eMarketer](https://www.emarketer.com/content/amazon-edges-deeper-agentic-commerce-rufus-auto-buy)
- Rufus has been merged with Alexa+ into a unified assistant in the US search bar; Rufus brand being retired — [The Next Web](https://thenextweb.com/news/amazon-alexa-shopping-search-bar-agentic-commerce)
- Amazon sued Perplexity (Nov 2025) over Comet agent shopping on Amazon, alleging it disguised automated activity as human browsing — [Insurance Journal, 5 Nov 2025](https://www.insurancejournal.com/news/national/2025/11/05/846503.htm)
- A judge granted Amazon a preliminary injunction (March 2026) — [GeekWire](https://www.geekwire.com/2026/judge-blocks-perplexitys-ai-bot-from-shopping-on-amazon-in-early-test-of-agentic-commerce/); later report says a US appeals court allowed Perplexity's agent back on Amazon, reasoning that users, not Perplexity, access Amazon — [The Decoder](https://the-decoder.com/us-appeals-court-allows-perplexitys-ai-shopping-agent-back-on-amazon/). Sources conflict on whether the order was paused or overturned; case reported as ongoing.
- Amazon reportedly blocked Meta's "Muse" shopping agent — [DEV Community](https://dev.to/axrisi/meta-muse-blocked-by-amazon-the-ai-shopping-agent-fight-explained-3agp)

**Perplexity shopping**
- Perplexity "Buy with Pro"/Instant Buy with PayPal integrations launched in 2024–2025 [background, unverified this session]. No 2026 adoption data found.

**Visa Intelligent Commerce / Mastercard Agent Pay**
- Visa (2 July 2026): live agentic transactions across Europe, AI agents buying from participating merchant sites; 30+ European issuers incl. Barclays, HSBC UK, Lloyds Banking Group, NatWest, Revolut; merchants incl. lastminute.com, Frasers, Cleverbridge, BrickDepot; authentication with Visa Payment Passkeys; being extended to B2B — [Visa UK press release](https://www.visa.co.uk/about-visa/newsroom/press-releases.3457328.html); [The Paypers](https://thepaypers.com/payments/news/visa-expands-agentic-commerce-access-for-merchants-across-europe)
- Mastercard: all European issuers enabled at network level for Agent Pay; first European milestone Santander transaction 2 March 2026 (controlled, not commercial rollout); Worldline + ING regionally orchestrated transaction — [Mastercard Europe](https://www.mastercard.com/europe/en/news-and-trends/stories/2026/europe-trusted-agentic-commerce.html); [ai2.work](https://ai2.work/blog/mastercard-agent-pay-goes-live-first-ai-payment-in-europe-2026)
- Reality check: independent commentary (Oct 2026) says most live agent transactions are pilots; one fraud vendor counted only "hundreds" of completed agent-initiated transactions worldwide by September 2026 — [Shatale](https://shatale.com/blog/mastercard-agent-pay-visa-intelligent-commerce)
- Visa's Trusted Agent Protocol (agent identity signalling to merchants, built on Web Bot Auth-style signatures) — [commonworld.one](https://commonworld.one/atlas/platforms/visa-intelligent-commerce/)

**UK/EU regulatory angle**
- CMA (9 March 2026) published guidance on consumer law for businesses using AI agents: existing consumer law applies the same whether a consumer deals with a human or an AI agent; businesses remain fully responsible for what their agents say/do even if third-party built; DMCC Act lets CMA fine up to 10% of global turnover — [TLT](https://www.tlt.com/insights-and-events/insight/agentic-ai-cma-publishes-guidance-on-consumer-law-and-dmcca-risks); [Lexology](https://www.lexology.com/library/detail.aspx?g=27b56295-fcbe-4339-a274-c3c2f6dc6be4)
- FCA's 2026 Payments Regulatory Priorities (25 March 2026) will consider whether regulation needs to change to support agentic AI payments — [Payment Expert](https://paymentexpert.com/2026/03/25/fca-2026-payments-regulatory-priorities-report/)
- As of Oct 2026, no UK/EU/US payments or consumer law is written specifically for agent-made purchases; liability for mistaken agent purchases unresolved — [Chargeflow](https://www.chargeflow.io/blog/agentic-commerce-regulation-what-merchants-need-to-know); [The Payments Association](https://thepaymentsassociation.org/article/agentic-commerce-uk-retail-an-unresolved-liability-question/)

### Inferences
- The pattern for 2026 is "agents research and shortlist; humans (or the merchant's own checkout) close". OpenAI's retreat and the tiny count of live agent payments suggest SMEs should invest in being *discoverable and correctly described* to agents before investing in agent checkout.
- UK SMEs can't currently get UK consumers buying in-chat via ChatGPT/Google, but they can already be surfaced (Shopify catalog, Merchant Center feeds), so feed quality is the near-term lever.
- The Amazon–Perplexity case shows large platforms may block agents; SMEs generally benefit from the opposite stance (letting legitimate agents in).
- CMA guidance means an SME deploying its own chatbot/agent (e.g., a quoting bot) is liable for its claims under DMCC rules.

### Gaps
- No reliable 2026 UK-specific consumer adoption figures for agentic purchases found.
- No verified 2026 data on Perplexity shopping volumes, or Perplexity/PayPal UK availability.
- Microsoft Copilot Merchant Program/Copilot Checkout details only seen via Shopify secondary sources (US-only).
- ICO-specific agentic AI guidance not found in searches; EU AI Act angle (Art. 50 transparency obligations applying from Aug 2026) is background knowledge, not verified this session.

## 2. Agent-readable web standards: what should an SME website expose?

### Takeaway
Of the new standards, only structured product/business data (schema.org, Merchant Center/Shopify catalog feeds) is clearly consumed by today's agents. MCP is real for business tools/SaaS but rarely needed on a small brochure site; WebMCP is an early Chrome origin trial with near-zero adoption; llms.txt is widely published but has no formal standing and Google calls it speculative; NLWeb has no public deployment count.

### Cited Findings
- WebMCP: W3C Community Group draft co-edited by Google and Microsoft, not on standards track; Chrome origin trial (Chrome 149–156, possibly extended to 162); first preview reportedly Chrome 146 Canary Feb 2026; site adoption close to zero, no mainstream agent consumes it; Firefox/Safari no plans — [Spronta, State of WebMCP July 2026](https://www.spronta.com/blog/state-of-webmcp-july-2026/); [freeCodeCamp](https://www.freecodecamp.org/news/a-developers-guide-to-webmcp/)
- llms.txt: no W3C/IETF/schema.org recognition as of mid-2026; Google's John Mueller called it "purely speculative for now"; Lighthouse added an llms.txt check in May 2026 that only flags fetch errors; one dataset shows ~79% of sampled domains with AI rules files (sample-dependent) — [Digital Applied](https://www.digitalapplied.com/blog/llms-txt-in-practice-adoption-evidence-2026)
- NLWeb (Microsoft, announced May 2025 [background]): no public deployment count as of Sept 2026; W3C Community Group exists but reportedly no draft published — [Tobira comparison](https://blog.tobira.ai/mcp-vs-webmcp-vs-nlweb-llms-txt-a2a/); [wellknownmcp map](https://wellknownmcp.org/en/news/2026-02-15-agentic-web-standards-map-2026-complete-guide)
- Comparison of MCP vs WebMCP vs NLWeb vs llms.txt vs A2A for websites — [Tobira](https://blog.tobira.ai/mcp-vs-webmcp-vs-nlweb-llms-txt-a2a/); agent-ready architecture guide — [OpenHermit](https://www.openhermit.com/blog/agent-ready-website-architecture-2026)
- Commerce protocols (ACP, UCP) are fed via platform catalogs/Merchant Center rather than built per-site by SMEs; Shopify stores are UCP-enabled by default — [Shopify UK](https://www.shopify.com/uk/blog/agentic-commerce); [Google Merchant Center](https://support.google.com/merchants/answer/16837055?hl=en)
- Visa Intelligent Commerce offers MCP server/agent toolkits for developers — [finance-loop](https://www.finance-loop.net/visa-intelligent-commerce/)

### Inferences
- Practical SME priority list (synthesis): (1) don't accidentally block legitimate AI search/user agents (check Cloudflare/CDN defaults, robots.txt); (2) server-rendered, crawlable HTML with clear pricing, service areas, opening hours, policies, FAQs; (3) schema.org (Organization/LocalBusiness, Product/Offer, Service, FAQ, Review) consistent with Google Business Profile; (4) product feeds in Merchant Center/Shopify catalog for e-commerce; (5) low-cost optional extras: llms.txt (cheap, unproven), an OpenAPI/MCP endpoint only if there's a real bookable/quotable service (e.g., booking system with an MCP connector); (6) watch WebMCP but don't build for it yet.
- Agents often act inside real Chrome sessions, so forms/booking flows need to work without hostile CAPTCHAs for legitimate users-with-agents — a tension with fraud controls (Section 4).

### Gaps
- No independent evidence that llms.txt or NLWeb changes AI citation/recommendation rates.
- No figures on how many SMEs expose MCP servers; MCP adoption numbers for business tools not gathered in this session.

## 3. Cloudflare's controls (and peers): pros/cons for SMEs that want to be found vs publishers protecting content

### Takeaway
Since 1 July 2025 Cloudflare defaults new domains toward blocking AI crawlers and offers Pay Per Crawl (still closed beta), Web Bot Auth/signed agents, Content Signals in robots.txt and AI Crawl Control dashboards. These suit publishers; an SME that wants AI visibility should audit these settings because defaults can make it invisible to AI search/answer engines. Crawl-to-referral ratios remain extremely lopsided, which is the publishers' case for blocking.

### Cited Findings
- 1 July 2025 "Content Independence Day": Cloudflare began blocking unverified AI crawlers by default on new domains, "changing the default to block AI crawlers unless they pay creators" — [ipscanner.io](https://ipscanner.io/blog/cloudflare-blocking-ai-crawlers-what-it-means); [BrandAxis: Is Cloudflare hiding your site from AI?](https://brandaxis.ai/blog/cloudflare-blocking-ai-crawlers/)
- Scope disputed: one source says documented defaults block AI *training* crawlers, not AI *search* crawlers — [Green Wire Media](https://greenwiremedia.com/blog/cloudflare-ai-crawlers/)
- Pay Per Crawl announced 1 July 2025; still described as closed/private beta (Aug 2026); payment headers (crawler-exact-price / crawler-max-price) must be signed via Web Bot Auth; robots.txt and sitemap.xml always free; Dec 2025 enhancements incl. discovery API requiring Web Bot Auth and crawler-error codes; April 2026 x402 payment-gated proxy template — [Cloudflare changelog 2025-07-01](https://developers.cloudflare.com/changelog/2025-07-01-pay-per-crawl/); [Cloudflare changelog 2025-12-10](https://developers.cloudflare.com/changelog/2025-12-10-pay-per-crawl-enhancements/); [AI Crawl Control changelog](https://developers.cloudflare.com/changelog/product/ai-crawl-control/)
- Content Signals Policy (24 Sept 2025, CC0): robots.txt directives search / ai-input / ai-train; Cloudflare managed default search=yes, ai-train=no, no ai-input signal; reportedly applied to ~3.8M domains; preferences only, not enforcement — [Search Engine World](https://www.searchengineworld.com/cloudflare-enters-the-robots-txt-fray-with-a-content-signals-policy-for-ai-bots); [somethinginc](https://somethinginc.com/blog/content-signals-policy-ai-input-default/)
- AI Crawl Control overview (block/allow/charge per crawler, analytics) — [Cloudflare docs](https://developers.cloudflare.com/ai-crawl-control/); practical guide — [Kompozy](https://kompozy.io/guides/cloudflare-ai-traffic-controls)
- Cloudflare: AI agent daily requests grew >1,700% in a year (Oct 2026) — [Forbes, 1 Oct 2026](https://www.forbes.com/sites/jonmarkman/2026/10/01/cloudflare-says-ai-agent-traffic-grew-more-than-1700-in-the-past-year/); automated traffic ~57% of HTML requests (June 2026, Cloudflare Radar via secondary) — [Imperva/Cloudflare comparison in search summary](https://www.digitalapplied.com/blog/ai-crawler-bot-traffic-statistics-2026-data-reference)
- TollBit State of the Bots: Europe H1 2026 — 179 AI bot scrapes per human referral (3x worse than North America); Q2 2026 227:1 vs 150:1 in Q1; secondary summary claims ChatGPT-User ignored robots.txt on 54% of scrapes, PerplexityBot 42% (unverified) — [Digiday](https://digiday.com/media/european-publishers-are-getting-hit-harder-by-ai-bot-scraping-report-finds/); [integrated.social](https://integrated.social/blog/ai-search-evidence-economy-publisher-scraping-referral-2026/)
- Crawl-to-referral metrics are not comparable across TollBit, Cloudflare and Clarity (no shared definition) — [AnswerEngineered](https://answerengineered.com/articles/three-tools-one-metric-no-definition/)
- Imperva guidance on which AI bots to allow vs block — [Imperva](https://www.imperva.com/blog/ai-bot-traffic-which-bots-to-trust/)

### Inferences
- **SME wanting to be found:** pros of Cloudflare controls = visibility into which AI bots hit the site, ability to verify signed agents and block impersonators; cons = defaults may block AI search/user-fetch bots, reducing presence in ChatGPT/Perplexity/Claude answers. Recommended stance: allow AI search and user-initiated fetchers (e.g., OAI-SearchBot, ChatGPT-User, PerplexityBot, Claude-SearchBot, Google-Extended is training-only), decide separately on training crawlers, set Content Signals to search=yes, ai-input=yes.
- **Publisher protecting content:** block training, consider Pay Per Crawl/TollBit, but note robots.txt non-compliance rates and that monetisation markets are still beta.
- Signed-agent verification (Web Bot Auth, Visa Trusted Agent Protocol) is the emerging mechanism to tell "good agents acting for a customer" from scrapers — relevant to SMEs' fraud filtering.

### Gaps
- Fastly and Akamai 2026 AI-bot report figures were not found in searches.
- Web Bot Auth / signed agents programme details (announced May/Aug 2025) not re-verified this session [background].
- Cloudflare's Aug 2025 accusation that Perplexity used stealth crawlers [background, unverified this session].

## 4. Fraud and trust: bad bots, AI form spam, ad fraud, analytics pollution, human verification

### Takeaway
Automated traffic now exceeds human traffic (Imperva: 53% in 2025; bad bots ~40% of all traffic) and AI-driven bot attacks rose sharply. AI agents running in normal Chrome evade GA4's bot filter, inflating sessions and corrupting lead/conversion metrics, while form-filling bots pollute CRMs. Defences are layered (Turnstile with server-side validation, honeypots, lead validation before counting conversions), but tighter friction risks blocking legitimate agent-assisted buyers.

### Cited Findings
- Imperva/Thales Bad Bot Report 2026 (April 2026): automated traffic ~53% of web traffic in 2025 (up from 51%); humans 47%; bad bots ~40% of all traffic (up from 37%); legitimate AI bots ~2% of sessions (85% crawlers, 15% fetchers); AI-driven bot attacks up 12.5x vs prior year — [Imperva blog](https://www.imperva.com/blog/bad-bot-report-2026-bots-agentic-age/); [Softprom summary](https://softprom.com/thales-imperva-bad-bot-report-2026-en); [adyog](https://pulse.adyog.com/insights/bad-bots-40-percent-all-traffic-2026). Caveat: some write-ups describe 40% as share of bot traffic; Imperva is a mitigation vendor.
- GA4 filters known bots but AI agents in standard Chrome register as human sessions — [TruIntel](https://truintel.ai/blog/ga4-cant-detect-ai-agents-synthetic-traffic); [MeasureU](https://measureu.com/dead-internet-ga4); filtering guide — [TAGGRS](https://taggrs.io/filter-bot-traffic/)
- GA4 may show zero orders from AI shopping agents when checkout happens off-site / pixels don't fire — [Seresa](https://seresa.io/blog/attribution-measurement/why-ga4-shows-zero-orders-from-ai-shopping-agents); Shopify confirms GA/pixels don't fire in Copilot/Google direct checkout — [kaspianfuad.com](https://kaspianfuad.com/blog/shopify-agentic-storefronts-april-2026-update/)
- Form-filling bots create fake sign-ups polluting CRMs and distorting cost-per-lead and qualification rates — [Managed Nerds](https://www.managednerds.tech/blog/ai-spam-leads-are-exploding-how-to-stop-fake-form-fills-and-bot-calls); bot filtering for Ads conversions — [Conversios](https://www.conversios.io/blog/bot-traffic-filtering-and-prevention-guide-for-ga4-and-google-ads/)
- Turnstile is a mostly puzzle-free CAPTCHA alternative but requires server-side token validation to actually protect forms — [Managed Nerds](https://www.managednerds.tech/blog/ai-spam-leads-are-exploding-how-to-stop-fake-form-fills-and-bot-calls)
- Visa uses Payment Passkeys to authenticate agent transactions; Mastercard Agent Pay European transactions used passkeys — [Visa UK](https://www.visa.co.uk/about-visa/newsroom/press-releases.3457328.html); [Mastercard Europe](https://www.mastercard.com/europe/en/news-and-trends/stories/2026/europe-trusted-agentic-commerce.html)
- World ID: only promotional coverage found ("anonymous proof of human") — [Forbes](https://www.forbes.com/sites/jonmarkman/2026/10/01/cloudflare-says-ai-agent-traffic-grew-more-than-1700-in-the-past-year/) (weak)
- Unverified vendor claim: "81.8% of AI traffic is fake" — [Navigo](https://navigotechsolutions.com/blog/81-8-of-your-ai-traffic-is-fake-fix-now-to-save-ad-budget) (do not cite as fact)

### Inferences
- For SMEs, the bigger near-term harm is measurement corruption (inflated sessions, fake conversions fed back to Google/Meta bidding) rather than direct financial fraud. Recommend: import only CRM-validated leads as conversions (offline conversion import), server-side Turnstile, honeypots, email/phone validation, and separate segments for AI referrals (chatgpt.com, perplexity.ai utm/referrers).
- Two traffic classes need different treatment: verified/signed agents acting for real customers (allow, possibly rate-limit) vs unsigned headless automation (challenge). Passkeys/payment-network tokens are where "human consent" is being anchored, not website CAPTCHAs.
- UK GDPR/PECR: bot-detection fingerprinting and analytics cookies/similar tech fall under PECR consent rules unless strictly necessary (security uses may qualify) — this is an inference/background; verify against ICO guidance.

### Gaps
- No independent quantitative data on AI-generated form spam rates for UK SMEs.
- No independent evidence on World ID effectiveness for lead forms.
- ICO guidance on bot detection under PECR / agentic AI not retrieved this session.
- Ad-fraud figures (e.g., invalid traffic rates in Google Ads) for 2026 not found.

## 5. B2B buying: AI assistants shortlisting vendors and agent-to-agent procurement

### Takeaway
Survey evidence is strong that B2B buyers now use generative AI in purchasing (Forrester 94%, G2: ~51% start software research in an AI chatbot more often than Google), though Gartner's lower 45% figure shows definitions matter. Gartner predicts 90% of B2B buying will be AI-agent intermediated by 2028 (>$15T of spend) — a forecast, not observed behaviour. Shortlists form early and humans still validate.

### Cited Findings
- Forrester 2026 Buyers' Journey Survey (~18,000 buyers): 94% used generative AI in their most recent purchase (up from 89%); twice as many buyers name genAI/conversational search as most meaningful source vs any other source — [Machine Relations summary](https://machinerelations.ai/research/b2b-ai-vendor-research-2026); [Grey Matter](https://gogreymatter.com/blog/how-b2b-buyers-use-ai-to-choose-vendors/)
- Gartner (645/646 B2B buyers, fielded Aug–Sep 2025, published ~2026): 45% used GenAI during a recent purchase, mainly to gather vendor/product info; 67% prefer a rep-free experience but 69% want to validate AI-generated insights with sales reps — [AuthorityTech summary](https://authoritytech.io/curated/gartner-rep-free-buyers-ai-sales-rep-2026) (secondary; sample-size/date discrepancies noted)
- 95% of eventual winners were already on the buying group's day-one shortlist (attributed to Gartner/6sense-style research; secondary) — [Pyxl: The Day One Shortlist](https://pyxl.com/reports/state-of-b2b-ai-visibility-2026)
- G2 (March 2026, 1,076 software buyers): 51% start research with an AI chatbot more often than Google, up from 29% a year earlier (some write-ups say 54%) — [Silvengate](https://silvengate.com/news/buyers-ask-ai-which-software-to-trust/); [Cyberdunes](https://www.cyberdunes.com/blog/marketing/b2b-buyers-ai-vendor-shortlists)
- Gartner Top Strategic Predictions (21 Oct 2025): by 2028, 90% of B2B buying will be AI-agent intermediated, pushing >$15 trillion of B2B spend through AI agent exchanges — [Gartner press release](https://www.gartner.com/en/newsroom/press-releases/2025-10-21-gartner-unveils-top-predictions-for-it-organizations-and-users-in-2026-and-beyond); [Digital Commerce 360](https://www.digitalcommerce360.com/2025/11/28/gartner-ai-agents-15-trillion-in-b2b-purchases-by-2028/)
- Procurement agents entering buying processes; GTM teams must sell to machines and humans — [The Revenue Wire](https://www.therevenuewire.com/news/procurement-ai-agents-selling-machines-humans) (commentary)
- Visa says its European agentic model is being extended to B2B payments — [Visa UK](https://www.visa.co.uk/about-visa/newsroom/press-releases.3457328.html)

### Inferences
- For B2B SMEs, the battleground is the AI-generated shortlist: if an assistant can't find clear, citable facts (who you serve, pricing ranges, case studies, certifications, reviews on G2/Trustpilot/Clutch), you may be excluded before any human visits the site — consistent with the "day-one shortlist" finding.
- Fewer but higher-intent visits and more "dark" (unattributable) influence: leads may arrive having been pre-qualified by an assistant, and attribution will under-credit AI. Add "How did you hear about us?" free-text and track AI referrers.
- Agent-to-agent procurement remains a forecast; near-term SME action is machine-readable specs/pricing and fast, structured responses to RFQs, not building agent endpoints.

### Gaps
- No primary Gartner/Forrester/G2 pages were fetched (blocked); figures come from secondary summaries with noted discrepancies (Gartner 645 vs 646 sample; G2 51% vs 54%).
- No 6sense 2025/2026 Buyer Experience Report figures retrieved this session.
- No measured data on autonomous procurement agents actually placing B2B orders.
- No UK-specific B2B buyer AI-usage data found.
