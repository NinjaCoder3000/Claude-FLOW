#!/usr/bin/env python3
"""Generate UGC Autopilot master build prompt as PDF using reportlab."""

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable
from reportlab.lib.enums import TA_LEFT

CONTENT = '''{
  "role": "BUILD EXECUTOR",
  "project": "ugc-autopilot",
  "instruction": "Read this entire object before writing any code. Build the full UGC Autopilot pipeline in the exact sequence defined in build_order. Use the exact system_prompt strings for each agent — do not paraphrase. Follow every schema field exactly. Expose every module as a standalone exported async function. Wire everything together only in src/orchestrator/index.ts.",

  "what_this_builds": "An automated UGC pipeline: scan JoinBrands/Trend.io/Insense/Influee for open paying campaigns -> 5 parallel Claude agents analyse the campaign -> synthesis agent produces a CreativeBrief -> Higgsfield generates a UGC video -> QC + AI-disclosure gate -> distribute -> log payout.",

  "runtime": "TypeScript / Node.js. ts-node for dev. Strict mode. ES2020 target.",

  "env_vars": {
    "ANTHROPIC_API_KEY": "required — Claude API for all agents",
    "HIGGSFIELD_API_KEY": "required — Higgsfield generation",
    "JOINBRANDS_COOKIE": "optional — full Cookie header from authenticated browser session",
    "TREND_IO_COOKIE": "optional",
    "INSENSE_API_KEY": "optional",
    "INFLUEE_COOKIE": "optional",
    "MIN_PAYOUT_USD": "optional, default 50",
    "HUNT_INTERVAL_MINUTES": "optional, default 30",
    "PAYOUT_LOG_PATH": "optional, default ./data/payouts.json",
    "OUTPUT_DIR": "optional, default ./output"
  },

  "project_structure": {
    "src/index.ts": "main entry — starts hunter + processQueue loop",
    "src/types.ts": "ALL TypeScript interfaces — build this first",
    "src/hunter/index.ts": "campaign-hunter module",
    "src/intake/index.ts": "intake-normalizer module",
    "src/agents/index.ts": "all 5 agents + runAgent helper",
    "src/synthesis/index.ts": "synthesis module",
    "src/generator/index.ts": "higgsfield-generator module",
    "src/qc/index.ts": "qc-compliance module",
    "src/distribution/index.ts": "distributor module",
    "src/tracker/index.ts": "payment-tracker module",
    "src/orchestrator/index.ts": "main pipeline controller",
    "data/campaign-queue.json": "[]",
    "data/seen-urls.json": "[]",
    "data/platform-policies.json": "{ joinbrands: ai_ugc_allowed true, trend_io: ai_ugc_allowed true, insense: ai_ugc_allowed true, influee: ai_ugc_allowed false }",
    "data/payouts.json": "[]",
    "output/": "generated video assets land here",
    "package.json": "ts-node, typescript, node-fetch, uuid — minimum deps",
    "tsconfig.json": "target ES2020, module commonjs, strict true, outDir dist"
  },

  "schemas": {
    "RawListing": {
      "url": "string",
      "platform": "joinbrands | trend_io | insense | influee | manual",
      "raw_text": "string",
      "scraped_at": "string ISO"
    },
    "CampaignBrief": {
      "id": "string uuid",
      "source_platform": "string",
      "campaign_url": "string",
      "product_name": "string",
      "product_description": "string",
      "brand_name": "string",
      "brand_website": "string | null",
      "brand_details": "string",
      "category": "string",
      "deliverables": "string[]",
      "payout_usd": "number",
      "deadline": "string | null",
      "ai_ugc_allowed": "boolean",
      "disclosure_required": "boolean — always true",
      "ingested_at": "string ISO"
    },
    "CreativeBrief": {
      "campaign_id": "string",
      "concept_title": "string",
      "video_duration": "30s | 45s | 60s",
      "hook": "string — exact first 3 seconds",
      "message_arc": "string",
      "visual_style": "string",
      "avatar_type": "string — e.g. woman late 20s energetic casual",
      "avatar_setting": "string — e.g. bright minimalist kitchen morning light",
      "tone": "string",
      "cta": "string",
      "key_phrases": "string[]",
      "target_persona": "string persona id",
      "product_name": "string",
      "brand_voice": "string",
      "disclosure_label": "AI-generated content — hardcoded always",
      "higgsfield_preset": "UGC | Tutorial | Unboxing | Product Review | UGC Virtual Try On | null"
    },
    "GeneratedAsset": {
      "campaign_id": "string",
      "asset_url": "string",
      "asset_type": "video | image",
      "duration_seconds": "number | null",
      "higgsfield_job_id": "string",
      "generated_at": "string ISO",
      "disclosure_label_applied": "boolean"
    },
    "QCResult": {
      "campaign_id": "string",
      "passed": "boolean",
      "brand_fit_score": "number 0-1",
      "issues": "string[]",
      "disclosure_label_present": "boolean",
      "approved_for_distribution": "boolean — true ONLY if passed AND disclosure_label_present"
    }
  },

  "agents": {
    "model": "claude-sonnet-4-20250514",
    "max_tokens": 2000,
    "response_rule": "Response MUST be valid JSON only — no preamble, no markdown fences. On parse failure retry ONCE appending: IMPORTANT: your previous response was not valid JSON. Return only the JSON object, no backticks, no markdown.",

    "A1_brand_recon": {
      "system_prompt": "You are a brand intelligence analyst. You receive a product name, product description, and brand details. Produce a structured brand intelligence report covering six areas: (1) Brand identity — list the core values as an array, personality traits as an array, a single tone-of-voice string, and a brand archetype string. (2) Visual aesthetic — describe palette feel, imagery style, and design sensibility as strings. (3) Messaging pillars — array of 3 to 5 key messages this brand consistently communicates. (4) Competitors — array of up to 3 objects, each with a name and a one-sentence positioning. (5) Differentiation — one sentence on what makes this brand distinct. (6) Content style — preferred formats as an array and a content personality string. Return ONLY valid JSON. Structure: {brand_identity:{values:[],personality:[],tone:'',archetype:''},visual_aesthetic:{palette_feel:'',imagery_style:'',design_sensibility:''},messaging_pillars:[],competitors:[{name:'',positioning:''}],differentiation:'',content_style:{preferred_formats:[],content_personality:''}}"
    },
    "A2_market_map": {
      "system_prompt": "You are a market analyst specialising in consumer goods and digital commerce. Analyse the market at three levels. MICRO: buyer niche, price positioning, seasonality, key platforms. MEZZO: industry name, growth trend, 3-5 key players, dominant content trends. MACRO: cultural tailwinds, regulatory notes, technology shifts. Finish with opportunity_summary. Return ONLY valid JSON: {micro:{niche:'',target_buyers:'',price_positioning:'',seasonality:'',key_platforms:[]},mezzo:{industry:'',growth_trend:'',key_players:[],content_trends:[]},macro:{cultural_tailwinds:[],regulatory_notes:'',technology_shifts:[]},opportunity_summary:''}"
    },
    "A3_persona": {
      "system_prompt": "You are a consumer psychology expert. Define exactly 7 distinct buyer personas. Each must be meaningfully different — vary by age, lifestyle, motivation. For each: id (P1-P7), fictional name, age_range, gender_skew (or null), psychographics {values, motivations, fears}, buying_trigger, main_objection, preferred_content, top_platform. Return ONLY valid JSON: {personas:[{id:'',name:'',age_range:'',gender_skew:null,psychographics:{values:[],motivations:[],fears:[]},buying_trigger:'',main_objection:'',preferred_content:'',top_platform:''}]}"
    },
    "A4_ugc_strategy": {
      "system_prompt": "You are a UGC performance strategist. Design a UGC content strategy with: (1) 4 content angles each with title, hook (exact first 3 seconds), narrative, best_for_persona. (2) 3 format recommendations from: testimonial, unboxing, day-in-life, transformation, tutorial, reaction, before-after, product-demo. (3) Messaging map for top 3 personas with key_message and emotional_trigger. (4) avoid_list. Mark top_angle. Return ONLY valid JSON: {content_angles:[{title:'',hook:'',narrative:'',best_for_persona:''}],formats:[{type:'',duration:'',style:''}],messaging_map:[{persona_id:'',key_message:'',emotional_trigger:''}],avoid_list:[],top_angle:''}"
    },
    "A5_product_decoder": {
      "system_prompt": "You are a product copywriter and conversion specialist. Decode the product into: (1) benefits array mapping feature to buyer benefit. (2) primary_driver — single most powerful purchase reason. (3) transformation — before state and after state. (4) proof_points array — best social proof types. (5) price_anchoring sentence or null. (6) keywords — top 8 search and social keywords. Return ONLY valid JSON: {benefits:[{feature:'',benefit:''}],primary_driver:'',transformation:'',proof_points:[],price_anchoring:null,keywords:[]}"
    },
    "S1_synthesis": {
      "system_prompt": "You are a creative director synthesising research into a production brief. You receive a campaign context plus five intelligence reports. Produce one unified CreativeBrief ready for Higgsfield video generation. Be specific and production-ready. Include: concept_title, video_duration (30s/45s/60s), hook (exact first 3 seconds), message_arc, visual_style, avatar_type, avatar_setting, tone, cta, key_phrases array, target_persona, product_name, brand_voice, disclosure_label (always 'AI-generated content'), higgsfield_preset (UGC | Tutorial | Unboxing | Product Review | UGC Virtual Try On | null). Return ONLY valid JSON."
    }
  },

  "user_message_template": "Product name: {product_name}\\nProduct description: {product_description}\\nBrand name: {brand_name}\\nBrand website: {brand_website}\\nBrand details: {brand_details}\\nCategory: {category}\\nDeliverables: {deliverables}",

  "module_specs": {
    "campaign_hunter": "src/hunter/index.ts — startHunter(intervalMinutes?):void, scanAllPlatforms():Promise<RawListing[]> via Promise.allSettled, scanJoinBrands/scanTrendIo/scanInsense per platform, filterByFit removes below MIN_PAYOUT_USD or ai_ugc_blocked, pushToQueue appends to campaign-queue.json and seen-urls.json",
    "intake_normalizer": "src/intake/index.ts — normalizeListing(raw):Promise<CampaignBrief> parses raw_text, generates uuid, checks platform-policies.json for ai_ugc_allowed (default false), one lightweight Claude call max_tokens 500 only if fields missing",
    "intelligence_layer": "src/agents/index.ts — runAgent<T>(systemPrompt, userMessage):Promise<T> POSTs to https://api.anthropic.com/v1/messages, parses JSON, retries once on failure. runIntelligenceLayer(brief):Promise<IntelligencePackage> calls all 5 via Promise.all",
    "synthesis": "src/synthesis/index.ts — synthesize(brief, intelligence):Promise<CreativeBrief> serializes all inputs as JSON, calls S1, returns typed CreativeBrief",
    "higgsfield_generator": "src/generator/index.ts — generateUGC(brief):Promise<GeneratedAsset> maps brief to Higgsfield params, submits job, polls every 15s, saves to OUTPUT_DIR/{campaign_id}.mp4. API: Authorization: Bearer HIGGSFIELD_API_KEY",
    "qc_compliance": "src/qc/index.ts — runQC(asset, brief):Promise<QCResult> HEAD request asset URL, check duration within 5s, confirm disclosure present. approved_for_distribution NEVER true when disclosure_label_present is false",
    "distributor": "src/distribution/index.ts — throws if approved_for_distribution false. Phase 08: log asset path + campaign URL for manual upload first",
    "payment_tracker": "src/tracker/index.ts — logCampaign appends to PAYOUT_LOG_PATH, markPaid sets paid_at, getPipelineSummary returns {total, submitted, paid, total_earned_usd}",
    "orchestrator": "src/orchestrator/index.ts — processQueue reads campaign-queue.json, processCampaign: normalizeListing -> runIntelligenceLayer -> synthesize -> generateUGC -> runQC -> distribute -> logCampaign. try/catch per campaign — one failure must not crash the queue"
  },

  "build_order": [
    "1. package.json + tsconfig.json — deps: ts-node typescript node-fetch uuid @types/node",
    "2. src/types.ts — ALL interfaces from schemas. Everything depends on clean types.",
    "3. data/ files — campaign-queue.json [], seen-urls.json [], payouts.json [], platform-policies.json",
    "4. src/intake/index.ts — test normalizeListing with mock RawListing before touching agents",
    "5. src/agents/index.ts — runAgent helper, A1 with exact system_prompt, test clean JSON, then A2-A5, wire all 5 into runIntelligenceLayer with Promise.all",
    "6. src/synthesis/index.ts — once all 5 agents produce clean typed output",
    "7. src/generator/index.ts — wire Higgsfield, confirm asset_url comes back",
    "8. src/qc/index.ts — QC gate and disclosure check",
    "9. src/distribution/index.ts + src/tracker/index.ts — manual submission logging first",
    "10. src/orchestrator/index.ts — wire all modules, test on one hardcoded RawListing",
    "11. src/hunter/index.ts — add LAST, only once full pipeline works. Verify endpoints via DevTools.",
    "12. src/index.ts — startHunter() + setInterval(processQueue, 5*60*1000)"
  ],

  "first_test": "Insert into data/campaign-queue.json and run processQueue() to confirm full pipeline: [{url: 'https://app.joinbrands.com/campaigns/test-001', platform: 'joinbrands', raw_text: 'Product: GlowSerum Pro. Brand: LumaLab. Description: A vitamin C serum for brightening. Payout: $150. Deliverables: 1x 30s UGC video. AI UGC allowed.', scraped_at: '2026-06-08T00:00:00.000Z'}]",

  "compliance_reminder": "EU AI Act Article 50 + US FTC: disclosure_label 'AI-generated content' must appear in every post caption. approved_for_distribution is false until confirmed. Non-negotiable."
}'''

OUT = "/home/user/Claude-FLOW/ugc-autopilot-master-prompt.pdf"

doc = SimpleDocTemplate(
    OUT,
    pagesize=A4,
    leftMargin=14*mm,
    rightMargin=14*mm,
    topMargin=16*mm,
    bottomMargin=16*mm,
)

DARK_BG = colors.HexColor("#0c0e0a")
LIME = colors.HexColor("#c6ff3a")
AMBER = colors.HexColor("#ff7a2f")
TEXT = colors.HexColor("#dde0d4")
MUTED = colors.HexColor("#969c89")

title_style = ParagraphStyle(
    "title",
    fontName="Courier-Bold",
    fontSize=18,
    textColor=LIME,
    spaceAfter=2*mm,
    leading=22,
)
sub_style = ParagraphStyle(
    "sub",
    fontName="Courier",
    fontSize=8,
    textColor=MUTED,
    spaceAfter=4*mm,
)
body_style = ParagraphStyle(
    "body",
    fontName="Courier",
    fontSize=7,
    textColor=TEXT,
    leading=10,
    spaceAfter=0,
    leftIndent=0,
    wordWrap="CJK",
)

story = []

story.append(Paragraph("UGC AUTOPILOT", title_style))
story.append(Paragraph(
    "Master Build Prompt for Opus 4.8 &mdash; Paste as your first message in ClaudeMachine",
    sub_style,
))
story.append(HRFlowable(width="100%", thickness=0.5, color=MUTED, spaceAfter=4*mm))

# Render content line by line
for line in CONTENT.split("\n"):
    safe = (line
            .replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;"))
    story.append(Paragraph(safe if safe.strip() else "&nbsp;", body_style))

doc.build(story)
print(f"PDF written: {OUT}")
