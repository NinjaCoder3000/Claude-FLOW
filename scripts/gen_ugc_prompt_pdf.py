#!/usr/bin/env python3
"""Generate updated UGC Autopilot master build prompt as PDF using reportlab."""

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable
from reportlab.lib.enums import TA_LEFT

CONTENT = '''{
  "role": "BUILD EXECUTOR",
  "project": "ugc-autopilot",
  "version": "2.0 — Higgsfield Supercomputer MCP edition",

  "instruction": "Read this entire object before writing any code. Build the full UGC Autopilot pipeline in the exact sequence defined in build_order. Use the exact system_prompt strings for each agent — do not paraphrase. Follow every schema field exactly. Expose every module as a standalone exported async function. Wire everything together only in src/orchestrator/index.ts.",

  "what_this_builds": "An automated UGC pipeline: scan JoinBrands/Trend.io/Insense/Influee for open paying campaigns -> 5 parallel Claude agents analyse the campaign -> synthesis agent produces a CreativeBrief -> Higgsfield Supercomputer generates a UGC video via MCP tool -> QC + AI-disclosure gate -> distribute -> log payout.",

  "runtime": "TypeScript / Node.js. ts-node for dev. Strict mode. ES2020 target.",

  "higgsfield_integration": {
    "platform": "Higgsfield Supercomputer — https://higgsfield.ai/supercomputer",
    "what_it_is": "Full AI creative team in one interface. Handles UGC videos, unboxing, tutorials, product demos, virtual try-on, AI influencer creation. Production-ready output.",

    "PRIMARY_MODE — ClaudeMachine via MCP": {
      "how": "Call the Higgsfield MCP tool generate_video directly from src/generator/index.ts",
      "api_key_needed": false,
      "subscription_needed": "YES — Higgsfield credits are consumed per generation even via MCP. Check https://higgsfield.ai/pricing for current plans.",
      "instruction": "In ClaudeMachine, the Higgsfield MCP server is already connected. The generate_video and show_marketing_studio tools are available. Call them directly — no REST API, no Bearer token, no HIGGSFIELD_API_KEY env var required.",
      "mcp_tools_available": [
        "generate_video — primary tool for UGC video generation",
        "generate_image — for static product shots",
        "show_marketing_studio — browse available presets and templates",
        "show_characters — select AI avatars/influencers",
        "personal_clipper_create — short-form clip editing",
        "virality_predictor — score content before posting",
        "job_display — check generation job status",
        "balance — check remaining credits"
      ]
    },

    "FALLBACK_MODE — Standalone Node.js REST API": {
      "how": "Use Higgsfield REST API with Authorization: Bearer HIGGSFIELD_API_KEY",
      "api_key_needed": true,
      "when_to_use": "Only if running ugc-autopilot outside ClaudeMachine as a standalone Node.js process",
      "env_var": "HIGGSFIELD_API_KEY"
    },

    "subscription_guidance": {
      "verified_pricing_june_2026": {
        "pay_as_you_go_top_up": "$5 per 100 credits. Credits expire after 90 days — do not roll over.",
        "cost_per_ugc_video": "Standard model (Kling 3.0): ~6 credits = ~$0.30/video. Premium (Sora 2, Veo 3.1): 40-70 credits = $2-$3.50/video.",
        "ugc_specific_plans": {
          "UGC Builder": "$9/month — 150 credits",
          "UGC Pro": "$17/month — UNLIMITED generations (best value once pipeline is running)"
        },
        "general_plans": {
          "Starter": "$15/month — 200 credits",
          "Plus": "$39/month — 1,000 credits",
          "Ultra": "$99/month — 3,000 credits + one unlimited video model"
        },
        "free_tier": "Yes — free plan with trial credits at signup. Use this first."
      },
      "recommendation": "START FREE. Use the trial credits to test the full pipeline on 1-2 real campaigns. If the pipeline works and videos are being accepted by platforms: upgrade to UGC Pro at $17/month — unlimited generations for $17 is the clearest no-brainer in this stack. At even 5 campaigns/month at $150 payout each = $750 revenue vs $17 cost.",
      "do_not_buy_yet": "Do NOT buy a plan before your pipeline runs one successful campaign end to end. Validate first, spend second.",
      "pay_as_you_go_math": "If testing before committing: 10 test videos at 6 credits each = 60 credits = $3 top-up. Cheap enough to validate.",
      "switch_trigger": "Stay pay-as-you-go until you are generating 5+ videos per month. At that point UGC Pro ($17/unlimited) wins every time.",
      "check_pricing_at": "https://higgsfield.ai/pricing and https://higgsfield.ai/supercomputer/pricing",
      "check_balance": "Call the MCP tool: balance() — shows remaining credits before you start a generation run"
    }
  },

  "env_vars": {
    "ANTHROPIC_API_KEY": "required — Claude API for all 5 intelligence agents + synthesis agent",
    "HIGGSFIELD_API_KEY": "only needed for standalone Node.js mode — NOT needed when running inside ClaudeMachine",
    "JOINBRANDS_COOKIE": "optional — full Cookie header from authenticated JoinBrands browser session",
    "TREND_IO_COOKIE": "optional — full Cookie header from authenticated Trend.io browser session",
    "INSENSE_API_KEY": "optional — Insense creator API key from their dashboard",
    "INFLUEE_COOKIE": "optional — full Cookie header from authenticated Influee browser session",
    "MIN_PAYOUT_USD": "optional, default 50 — filter out campaigns below this payout",
    "HUNT_INTERVAL_MINUTES": "optional, default 30 — how often the hunter polls all platforms",
    "PAYOUT_LOG_PATH": "optional, default ./data/payouts.json",
    "OUTPUT_DIR": "optional, default ./output"
  },

  "project_structure": {
    "src/index.ts": "main entry — starts hunter + processQueue loop",
    "src/types.ts": "ALL TypeScript interfaces — build this first",
    "src/hunter/index.ts": "campaign-hunter module",
    "src/intake/index.ts": "intake-normalizer module",
    "src/agents/index.ts": "all 5 intelligence agents + runAgent helper",
    "src/synthesis/index.ts": "synthesis module — produces CreativeBrief",
    "src/generator/index.ts": "Higgsfield generator — calls MCP generate_video in ClaudeMachine, REST API in standalone mode",
    "src/qc/index.ts": "QC + compliance gate",
    "src/distribution/index.ts": "distributor module",
    "src/tracker/index.ts": "payment tracker",
    "src/orchestrator/index.ts": "main pipeline controller — wire all modules here only",
    "data/campaign-queue.json": "[] — pending campaigns",
    "data/seen-urls.json": "[] — already-processed URLs",
    "data/platform-policies.json": "{ joinbrands: ai_ugc_allowed true, trend_io: ai_ugc_allowed true, insense: ai_ugc_allowed true, influee: ai_ugc_allowed false }",
    "data/payouts.json": "[] — campaign outcome log",
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
      "message_arc": "string — full video flow",
      "visual_style": "string — aesthetic direction",
      "avatar_type": "string — e.g. woman late 20s energetic casual",
      "avatar_setting": "string — e.g. bright minimalist kitchen morning light",
      "tone": "string",
      "cta": "string",
      "key_phrases": "string[] — lines the avatar must deliver verbatim",
      "target_persona": "string persona id",
      "product_name": "string",
      "brand_voice": "string",
      "disclosure_label": "AI-generated content — always hardcoded",
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
      "system_prompt": "You are a creative director synthesising research into a production brief. You receive a campaign context plus five intelligence reports. Produce one unified CreativeBrief ready for Higgsfield Supercomputer video generation. Be specific and production-ready — no vague descriptors. Decide: concept_title, video_duration (30s/45s/60s), hook (exact first 3 seconds as specific words or beats), message_arc (full video flow start to finish), visual_style (specific aesthetic for avatar and setting), avatar_type (age range gender energy level), avatar_setting (specific environment), tone, cta, key_phrases array (exact lines the avatar must say), target_persona id, product_name, brand_voice (one phrase), disclosure_label (always 'AI-generated content'), higgsfield_preset (UGC | Tutorial | Unboxing | Product Review | UGC Virtual Try On | null). Return ONLY valid JSON."
    }
  },

  "user_message_template": "Product name: {product_name}\\nProduct description: {product_description}\\nBrand name: {brand_name}\\nBrand website: {brand_website}\\nBrand details: {brand_details}\\nCategory: {category}\\nDeliverables: {deliverables}",

  "module_specs": {
    "campaign_hunter": {
      "file": "src/hunter/index.ts",
      "exports": "startHunter(intervalMinutes?):void | scanAllPlatforms():Promise<RawListing[]> via Promise.allSettled | scanJoinBrands/scanTrendIo/scanInsense per platform | filterByFit removes below MIN_PAYOUT_USD or ai_ugc_blocked | pushToQueue appends to campaign-queue.json and seen-urls.json"
    },
    "intake_normalizer": {
      "file": "src/intake/index.ts",
      "exports": "normalizeListing(raw):Promise<CampaignBrief> — parses raw_text, generates uuid, checks platform-policies.json for ai_ugc_allowed (default false if not found), one lightweight Claude call max_tokens 500 only if fields missing | checkAiUgcPolicy(platform):boolean"
    },
    "intelligence_layer": {
      "file": "src/agents/index.ts",
      "exports": "runAgent<T>(systemPrompt, userMessage):Promise<T> — POST to https://api.anthropic.com/v1/messages, model claude-sonnet-4-20250514, max_tokens 2000, parse JSON, retry once on failure | runIntelligenceLayer(brief):Promise<IntelligencePackage> — Promise.all across all 5 agents"
    },
    "synthesis": {
      "file": "src/synthesis/index.ts",
      "exports": "synthesize(brief, intelligence):Promise<CreativeBrief> — serialize all inputs as JSON block, call S1 agent, return typed CreativeBrief with campaign_id set from brief.id"
    },
    "higgsfield_generator": {
      "file": "src/generator/index.ts",
      "PRIMARY — ClaudeMachine MCP mode": "Call the generate_video MCP tool directly. Map CreativeBrief fields to the tool params: visual_style + avatar_type + avatar_setting + key_phrases -> prompt, higgsfield_preset -> preset, video_duration -> duration. Poll job status with job_display tool every 15s. Return GeneratedAsset with asset_url and higgsfield_job_id. Before each run call balance() to confirm credits are available.",
      "FALLBACK — Standalone Node.js mode": "If MCP is not available, POST to Higgsfield REST API with Authorization: Bearer process.env.HIGGSFIELD_API_KEY. Map same fields. Poll every 15s. Save to OUTPUT_DIR/{campaign_id}.mp4.",
      "exports": "generateUGC(brief):Promise<GeneratedAsset> | mapBriefToHiggsfield(brief):object"
    },
    "qc_compliance": {
      "file": "src/qc/index.ts",
      "exports": "runQC(asset, brief):Promise<QCResult> — HEAD request asset URL (status 200), check duration within 5s of brief, confirm disclosure present | attachDisclosure(asset):GeneratedAsset — set disclosure_label_applied true",
      "rule": "approved_for_distribution is NEVER true when disclosure_label_present is false — no exceptions"
    },
    "distributor": {
      "file": "src/distribution/index.ts",
      "exports": "distribute(asset, brief, qc) — throws immediately if qc.approved_for_distribution is false. Phase 08: log asset path + campaign URL for manual upload. Automate per-platform submission later."
    },
    "payment_tracker": {
      "file": "src/tracker/index.ts",
      "exports": "logCampaign(brief, result):void — append to PAYOUT_LOG_PATH | markPaid(campaign_id):void — call manually when payment arrives | getPipelineSummary():{total, submitted, paid, total_earned_usd}"
    },
    "orchestrator": {
      "file": "src/orchestrator/index.ts",
      "exports": "processQueue():Promise<void> — read campaign-queue.json, run processCampaign on each, remove successes, leave failures for retry | processCampaign(raw):Promise<void> — full sequence: normalizeListing -> runIntelligenceLayer -> synthesize -> generateUGC -> runQC -> distribute -> logCampaign. try/catch per campaign — one failure must NOT crash the queue."
    }
  },

  "build_order": [
    "1. package.json + tsconfig.json — deps: ts-node typescript node-fetch uuid @types/node",
    "2. src/types.ts — ALL interfaces from schemas section. Everything else depends on clean types.",
    "3. data/ files — campaign-queue.json [], seen-urls.json [], payouts.json [], platform-policies.json with joinbrands+trend_io+insense ai_ugc_allowed:true, influee ai_ugc_allowed:false",
    "4. src/intake/index.ts — build and test normalizeListing with a hardcoded mock RawListing. Confirm CampaignBrief output is clean before touching agents.",
    "5. src/agents/index.ts — build runAgent helper first. Implement A1 brand_recon with exact system_prompt. Test until JSON is clean. Then A2-A5. Wire all 5 into runIntelligenceLayer with Promise.all.",
    "6. src/synthesis/index.ts — build once all 5 agents produce clean typed output. Test that CreativeBrief has all fields populated.",
    "7. src/generator/index.ts — wire Higgsfield. In ClaudeMachine: call generate_video MCP tool. Test with one CreativeBrief. Call balance() first to confirm credits. Confirm asset_url comes back.",
    "8. src/qc/index.ts — QC gate and disclosure check. approved_for_distribution NEVER true without disclosure.",
    "9. src/distribution/index.ts + src/tracker/index.ts — manual submission log first. Automate later.",
    "10. src/orchestrator/index.ts — wire all modules into processCampaign. Test on one hardcoded RawListing end to end.",
    "11. src/hunter/index.ts — add hunter LAST, only once full pipeline works. Verify real platform endpoints by inspecting authenticated DevTools network traffic first.",
    "12. src/index.ts — startHunter() + setInterval(processQueue, 5*60*1000). Run. Monitor via getPipelineSummary()."
  ],

  "first_test": {
    "instruction": "Before building the hunter, insert this into data/campaign-queue.json and run processQueue() to confirm the full pipeline works end to end",
    "data": "[{\"url\":\"https://app.joinbrands.com/campaigns/test-001\",\"platform\":\"joinbrands\",\"raw_text\":\"Product: GlowSerum Pro. Brand: LumaLab. Description: A vitamin C and niacinamide serum for brightening and evening skin tone. Payout: $150. Deliverables: 1x 30s UGC video. AI UGC allowed.\",\"scraped_at\":\"2026-06-08T00:00:00.000Z\"}]"
  },

  "pre_build_checklist": [
    "[ ] ANTHROPIC_API_KEY is set in .env — required for all 5 agents + synthesis",
    "[ ] Logged into Higgsfield Supercomputer — MCP tools connected in ClaudeMachine (no API key needed)",
    "[ ] Use Higgsfield FREE trial credits first to test pipeline. Do NOT buy a plan yet.",
    "[ ] After first successful campaign: upgrade to UGC Pro at $17/month (unlimited generations)",
    "[ ] If only testing: top up $5 for 100 credits (covers ~16 standard UGC videos at 6 credits each)",
    "[ ] Call balance() MCP tool before each generation run to confirm credits available",
    "[ ] JoinBrands account created — Cookie needed for the hunter in Phase 11",
    "[ ] data/ folder files created as empty arrays before running any code"
  ],

  "compliance_reminder": "EU AI Act Article 50 + US FTC: disclosure_label 'AI-generated content' must appear visibly in every post caption or description. approved_for_distribution is false until this is confirmed present. Non-negotiable — undisclosed AI content gets accounts banned."
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

LIME   = colors.HexColor("#b8f030")
AMBER  = colors.HexColor("#ff7a2f")
TEXT   = colors.HexColor("#dde0d4")
MUTED  = colors.HexColor("#969c89")

title_style = ParagraphStyle("title", fontName="Courier-Bold", fontSize=16,
                              textColor=LIME, spaceAfter=2*mm, leading=20)
sub_style   = ParagraphStyle("sub",   fontName="Courier", fontSize=8,
                              textColor=MUTED, spaceAfter=4*mm)
body_style  = ParagraphStyle("body",  fontName="Courier", fontSize=6.8,
                              textColor=TEXT, leading=9.8, spaceAfter=0, wordWrap="CJK")

story = []
story.append(Paragraph("UGC AUTOPILOT — MASTER BUILD PROMPT v2", title_style))
story.append(Paragraph(
    "Higgsfield Supercomputer MCP Edition &mdash; Paste as your first message in ClaudeMachine / Opus 4.8",
    sub_style))
story.append(HRFlowable(width="100%", thickness=0.5, color=MUTED, spaceAfter=4*mm))

for line in CONTENT.split("\n"):
    safe = line.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    story.append(Paragraph(safe if safe.strip() else "&nbsp;", body_style))

doc.build(story)
print(f"PDF written: {OUT}")
