# Instagram DM Setting Skill — Full Content

**name:** instagram

**description:** Navigate Instagram native DMs, run notification outreach, check profiles, and send openers. Use for IG notification outreach and native DM fallback.

---

## Overview

This skill enables two workflows: **Prospecting** (identifying ICP prospects) and **Outreach** (sending Stage 1 openers via native IG DMs). Conversation and qualification happen in ManyChat, not here.

---

## When to Use

- Prospecting: Scanning comments, notifications, followers for ICP prospects to build a curated list
- Outreach: Sending Stage 1 openers to prospects via native IG DMs
- Fallback DMs: Handling ManyChat limitations (rare cases)
- Profile checking: Verifying ICP fit before outreach

**Not for:** Replying to leads, qualifying conversations, or booking calls—those occur in ManyChat.

---

## Key URLs

| Page | URL |
|------|-----|
| Instagram Home | `https://www.instagram.com/` |
| DMs Inbox | `https://www.instagram.com/direct/inbox/` |
| Notifications | Sidebar access only |
| Profile (by handle) | `https://www.instagram.com/{handle}/` |
| Jason's profile | `https://www.instagram.com/jasoncooperson/` |

---

## Prospecting Workflow

**Goal:** Build 20+ qualified prospects in `prospect-list.md`. Prospecting means finding, not messaging.

### Best Sources (Priority Order)

1. **Post comments on business/AI/strategy posts** — Commenters demonstrate intent; evaluate the person, not their comment
2. **Notification "Follow Back" buttons** — New followers not yet followed back = warm leads
3. **"Suggested for you" sections** — Instagram groups similar accounts; one prospect reveals network clusters
4. **Reel like aggregates** — Most relevant/followed account appears first

### Worst Sources (Avoid)

- **Viral reel notifications** — ~5% ICP hit rate; mostly keyword triggers from small accounts
- **Recent followers list** — Predominantly viral reel followers (low quality)
- **Story viewers** — Mostly friends and peers

### Scanning Post Comments Efficiently

1. Navigate to `https://www.instagram.com/jasoncooperson/`
2. Select business-focused posts (strategy, AI, automation—avoid lifestyle/travel)
3. Use `get_page_text` to extract all commenter usernames at once
4. Note usernames, then batch-check profiles
5. Check multiple posts for richest results

### Checking Profiles Quickly

**Use `get_page_text` instead of screenshots** — Returns bio, follower count, name, category, website, and mutual connections in one call (3 seconds vs. 10+ for screenshots).

**Profile text evaluation:**
- Name and title (CEO, Founder, Coach, etc.)
- Follower count (1K+ with genuine content = viable)
- Bio keywords: agency, coaching, scale, clients, founder, automation
- Website link (indicates business)
- "Verified" status
- "Followed by [names]"—shows network connection
- Story highlights: "Client Wins," "Testimonials," "Results"
- "Follow Back" button status

**Screenshot only** when verifying profile pictures or content grid authenticity.

---

## ICP Qualification Criteria

**Target:** Established creator-coaches, agency owners, and service business operators earning $10K-$30K+/month who need fulfillment and operations support.

### A-Tier Signals (Strong)
- Verified account ✅
- Bio includes: agency, coaching, consulting, founder, CEO, scale, clients, AI, automation
- Story highlights: "Client Wins," "Testimonials," "Results"
- Website or Calendly link in bio
- 1K-50K+ followers with authentic content
- US, Europe, or Australia based
- Connected to Jason's network orbit
- Genuine comment on business-focused post

### B-Tier Signals (Worth Contacting)
- Established business with follower count <1K
- European, non-English speaking but Western market
- COO/operator title with emerging IG presence
- Legitimate business website, early content stage

### Hard Skip Signals
- Located outside US, Europe, Australia
- <100 followers, 0 posts (ghost/bot)
- Private, empty profile
- Non-English bio without business indicators
- Anime/meme/fan page profile picture
- Personal-only account (selfies, food, travel—no business)
- Friends/family of Jason ("Followed by cooperson.json, saracooperson, vndrewfox")
- Service pitchers (video editors, booking setters)
- Under 18 or college students without established business

### Geographic Filter
**US, Europe, Australia only.** No exceptions.

### Network Cluster Mining

When finding one qualified prospect, check their "Suggested for you" section. Instagram clusters similar accounts together—one prospect often reveals 5-10 additional high-tier prospects. Note promising suggested accounts and add them to your check list.

### Saving the Prospect List

Store qualified prospects in `prospect-list.md` with:
- Handle
- Name
- One-line reason for ICP qualification
- Tier (A or B)
- Source (which post comment, notification, or suggested section)

---

## Outreach Workflow

Process `prospect-list.md` sequentially. Send personalized Stage 1 openers to each prospect. Mark as sent upon completion.

### Opening a DM Conversation (Fastest Method)

1. Navigate to `https://www.instagram.com/direct/inbox/`
2. Click the **Search** bar in the inbox sidebar
3. Type the prospect's exact handle (e.g., `loicscales`)
4. Wait 2 seconds for results
5. Click their name under "More accounts" or existing threads
6. Use `find` tool to locate "Message input box"
7. Click the ref, type message, press Enter
8. For subsequent messages: type immediately, press Enter
9. Click back arrow (`←`) to return to search; repeat for next prospect

**Why not profile → Message button?** The Message button only displays on profiles you follow. For new prospects, the DM search bar is the only reliable web method.

**Speed techniques:**
- Skip screenshots between sends—trust the workflow; screenshot only if something seems off
- After sending: click back arrow → search bar → type next handle immediately
- Use `find` tool for "Message input box" (more reliable than coordinate clicking)

### Typing and Sending

1. Use `find` tool to locate "Message" input by ref
2. Click the ref
3. Type the message
4. Press **Enter** to send (no separate send button in IG DMs)

**If "Related keyboard shortcuts" overlay appears:** Use `find` tool for the close button, click the X, then type your message.

### Message Content

**For prospects with NO prior conversation:**
Personalized compliment referencing their bio/business + curiosity question (Stage 1 opener per setting-script.md)

**For prospects who received ManyChat auto-DMs:**
Old ManyChat auto-DMs don't count as contacted. Send a personal Stage 1 opener.

**Scope:** Send openers only. Do not reply to messages, qualify leads, or book calls via native IG DMs—those functions belong in ManyChat.

---

## Inbox Navigation

### Primary vs General Tab
Use `find` tool to locate "Primary" or "General" tab by text—don't assume fixed positions.

### Checking for Replies
Open their conversation (search by name). If the last message is theirs = they replied. If last message is yours = no reply. Don't rely on "seen" indicators.

### Scrolling Through Inbox
Use `scroll` action on the conversation list panel. Messages sort by most recent activity.

---

## Story Viewers

- Mostly Jason's friends/peers ("Following" button suggests a friend)
- Check DM thread before messaging—casual banter/story reactions indicate a friend; skip
- Message only story viewers with NO existing DM thread or only ManyChat auto-DMs
- "Followed by cooperson.json" = likely personal friend, skip

---

## Browser Performance Tips

- **Use `get_page_text` for profiles** — 3x faster than screenshots; returns bio, followers, name, website, mutual connections in one call
- **Use `find` tool first** — More reliable than guessing coordinates
- **Use refs over coordinates** — Refs remain stable; coordinates shift with scroll/resize
- **Batch profile checks** — Collect 10-15 usernames from comments first, THEN check profiles sequentially
- **Navigate directly** to `instagram.com/{handle}/` instead of clicking UI elements
- **Screenshot selectively** — For content grid or profile picture verification only; `get_page_text` provides bio details
- **Don't retry failed actions** — Re-find the element instead
- **Wait 2 seconds post-navigation** before calling `get_page_text` (page load time)
