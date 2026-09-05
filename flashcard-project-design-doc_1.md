# AI Flashcard Generator — Design & Build Guide

This is the build guide for the vocab-photo → Anki-deck project: what to build,
which APIs to call, why, and roughly what it'll cost. The goal is to spend your
time writing code, not re-deriving pricing pages.

## TL;DR

- The idea and the 5-phase build order are genuinely good — keep them as planned.
- Models: `gemini-2.5-flash-lite` for OCR/translation/tagging/sentences,
  `gemini-3.1-flash-lite-image` ("Nano Banana 2 Lite") for illustrations,
  `gemini-2.5-flash-preview-tts` for pronunciation, `genanki` to package the `.apkg`.
- Platform: Google AI Studio + the `google-genai` Python SDK, calling the plain
  `generateContent` endpoint. No GCP project needed for phases 0–4.
- Cost: a fully-loaded 50-card deck (OCR + translation + tags + image + sentence +
  audio, every card) runs **~$1.50–1.80** at standard pricing, **~$0.85–0.90** if you
  use the Batch API. Images are ~95% of that cost — everything else is fractions of a cent.
- Full reasoning below, plus a phase-by-phase build plan and draft resume lines.

---

## 1. Why this project fits the target role

I read the actual posting. Two things worth knowing before you start:

- **Level**: this specific requisition is listed "Mid" — 2 years of software
  engineering experience and 1 year of ML infra experience are the *minimum*
  bar, so treat this exact req as a stretch, not a guarantee. It doesn't waste
  the effort though: the same project and story work for the New Grad / SWE II
  AI-Cloud postings Google (and every peer company) runs constantly. Build for
  the role family, not this one req ID.
- **Language**: the listing says "e.g., Go" for the programming-language
  requirement — that's an example, not a requirement. Python is fine.

More usefully, the posting's actual content lines up with this project almost
too well:

- Preferred quals explicitly want: cloud deployment experience (GCP), building
  for "enterprise needs," **familiarity with LLMs and AI agents**, and a
  **"track record of innovative ideas and rapid execution in the AI/ML space."**
  A small, working, incrementally-shipped GenAI pipeline is exactly that track
  record, in miniature.
- The job description literally says the role is about developing "features
  that integrate the next generation large language model with **balanced
  trade-off between performance and deployment constraints**." That sentence
  is a restatement of your own brief — "optimize for speed and cheap costs,
  not quality." Making that trade-off *explicitly and defensibly* (which
  models, why, what it costs, what you gave up) is the actual skill being
  tested, more than any specific feature.
- The responsibilities section says the team builds the **"AI Developer Tools
  Platform"** that Antigravity, Gemini CLI, and Gemini Code Assist run on —
  i.e., infrastructure for orchestrating models and agents. Your "agentic
  harness" is a small personal version of that same problem: sequencing
  several model calls, handling failures, keeping cost and latency sane. That
  framing is worth using explicitly in an interview, not just on the resume
  line.

## 2. The build, restated as 5 milestones

Keeping your own scoping, just named for reference later in this doc:

| # | Milestone | Card front | Card back |
|---|-----------|-----------|-----------|
| v0 | OCR + translate | word | translation |
| v1 | + tags | word | translation, tagged for filtering in Anki |
| v2 | + illustration | word, image | translation, same image |
| v3 | + example sentence | word, image, sentence | translation, image, sentence translation |
| v4 | + pronunciation | word, image, sentence, audio | translation, image, sentence, audio |

Each milestone is a strict superset of the last, which is exactly why this is
a good learning project: every phase is independently shippable, testable,
and demoable.

## 3. Model & API choices

Everything below is from Google's own pricing page
(`ai.google.dev/gemini-api/docs/pricing`), checked while writing this doc.
Google's Gemini lineup moves fast — model names and prices *will* have
shifted by the time you're deep into building — so treat the model IDs as
correct-as-of-now and the prices as "this is the right order of magnitude and
the right family to pick from," and reverify before you commit (link at the
bottom).

| Task | Model | Price | Why this one |
|---|---|---|---|
| OCR + parse + tagging | `gemini-2.5-flash-lite` | $0.10 / $0.40 per 1M input/output tokens | Cheapest current Gemini model that still takes image input natively — one call reads the photo *and* returns structured data. Has a free tier for dev. |
| Translation | same model, same call family | (bundled above) | No separate vendor — it's just another prompt. Batchable across all words in one call. |
| Example sentences | same model | (bundled above) | Same reasoning — batch one call for the whole word list rather than one call per word. |
| Illustrations | `gemini-3.1-flash-lite-image` ("Nano Banana 2 Lite") | ~$0.034 per 1024px image | Cheapest image-generation model Google currently ships, and it's *literally* described in Google's own docs as built for "ultra-low latency and cost-effective image generation" — it's Google's recommended replacement for the original Nano Banana. |
| Pronunciation | `gemini-2.5-flash-preview-tts` | $0.50 / $10 per 1M tokens (~$0.00025/sec of audio) | Has a free tier, stays inside the same SDK. A word (~1s) plus its example sentence (~3s) costs roughly a tenth of a cent. |
| Packaging | [`genanki`](https://github.com/kerrickstaley/genanki) (open-source, pip-installable) | free | The standard way to build `.apkg` files from Python — handles Notes/Models/Decks and embeds image + audio media files directly. Confirmed current and actively used. |

**Why not other Google services you might expect here:** Cloud Vision (OCR)
and Cloud Translation are both solid products, but pulling them in means a
second and third GCP client library, each with its own auth/IAM setup. Gemini
reads the photo and translates in the same call family you're already using —
fewer moving parts, faster to build, and at this volume the cost difference
is irrelevant. Skip them unless you hit an accuracy wall Gemini can't clear.

**Why not OpenAI or another vendor:** roughly comparable pricing at this
scale, but there's no reason to introduce a second vendor's auth/SDK/billing
for a project whose whole pitch (to this employer, specifically) is fluency
with Google's own stack.

## 4. Platform: what to build on, and why

**Recommendation: Google AI Studio (not Vertex AI), calling `generateContent`
(not the new Interactions API), through the `google-genai` Python SDK. Local
scripts, no GCP project, until you deliberately choose to add one.**

### AI Studio vs. Vertex AI

Use AI Studio for phases 0–4. Reasoning:

1. **Time to first call.** An AI Studio API key is copy-paste from
   `aistudio.google.com`. Vertex AI needs a GCP project, a billing account,
   enabled APIs, and IAM/service-account setup before you send your first
   request. For "optimize for speed," this alone settles it for the
   prototyping phase.
2. **One SDK, one auth token, four capabilities.** `google-genai` covers
   text, vision, image generation, and speech generation through a single
   client. That's a much shorter path to a working pipeline than juggling
   separate Cloud Vision / Translation / Text-to-Speech client libraries.
3. **The free tier covers most of development.** Flash and Flash-Lite models
   — including both image models discussed above — are free to call in AI
   Studio up to daily/per-minute limits, which is generally enough to build
   and demo on before you spend anything real. TTS has a free tier too.
4. **Vertex AI's advantages don't apply yet.** VPC Service Controls, IAM,
   committed-use discounts, regional data residency, enterprise SLAs — all
   real, all irrelevant to a side project's traffic volume.
5. **Migrating later is cheap.** Same model families are callable from Vertex
   AI with mostly a client-init change. Nothing you build here is a dead end.

**Stretch goal, and worth doing deliberately for this specific application:**
once phases 0–4 work locally, port the serving layer to **Vertex AI + Cloud
Run**. This is the one part of the stack worth doing "the GCP way" *because*
the job's preferred qualifications explicitly call out cloud deployment
experience and enterprise concerns — this is where you'd pick that up.
Cloud Run's always-free tier (2M requests/month, ~180K vCPU-seconds/month,
permanent, no surprise auto-charge) will likely cover a personal demo
indefinitely.

### `generateContent` vs. the new Interactions API

Worth knowing about, and worth being deliberate about: Google shipped a new
**Interactions API** (GA since June 2026) as its new recommended default for
building with Gemini models *and* agents — unified interface, typed
step-based schema, server-side state, background execution. It's the more
"current" way to build agent-style systems, and it's genuinely relevant to
the "AI Developer Tools Platform" framing from Section 1.

**But there's a concrete trade-off:** as of this writing, the Batch API
(the 50% cost cut mentioned throughout this doc) and explicit context caching
are *not yet available* on the Interactions API — only on the legacy
`generateContent` endpoint, which remains fully supported, not deprecated.

Since this pipeline is a fixed, script-driven fan-out (read list → translate
→ illustrate → narrate) rather than a multi-turn conversation or an agent
that's dynamically deciding what to call next, it doesn't actually need the
Interactions API's state management or step schema — and it *does* benefit
directly from Batch pricing on the image calls, which are 95% of your cost.

**Recommendation:** build v0–v4 on `generateContent`. If you want a genuine
stretch phase afterward, that's where the Interactions API earns its keep —
e.g., an orchestrator that *decides* whether an entry needs an OCR retry, or
whether to reuse a cached illustration, rather than a fixed script doing the
same five calls every time. That version would legitimately be "agentic";
the v0–v4 pipeline as scoped is better described as an **orchestration
pipeline** — which is a perfectly good, honest thing to build and to put on
a resume, just worth calling it what it is if asked in an interview.

## 5. Architecture

Carry one record per vocabulary entry through the whole pipeline, adding a
field at each milestone:

```json
{
  "word": "...",
  "tags": ["..."],
  "translation": "...",
  "example_sentence": "...",
  "example_translation": "...",
  "image_path": "media/word_123.png",
  "audio_word_path": "media/word_123.mp3",
  "audio_sentence_path": "media/sentence_123.mp3"
}
```

Pipeline shape — one call gives you the list, then everything else fans out:

```
 photo/PDF ──▶ gemini-2.5-flash-lite (multimodal OCR + parse)
                        │
                        ▼
              structured JSON: [{word, tags[]}, ...]
                        │
        ┌───────────────┼────────────────┬─────────────────┐
        ▼                ▼                ▼                 ▼
  translate          example        illustration       pronunciation
  (1 batched call    sentence       (Nano Banana 2     (Gemini TTS,
  for the list)      (1 batched     Lite, one call     one call per
                      call)          per word, run       word + sentence,
                                     concurrently)        run concurrently)
        │                │                │                 │
        └────────────────┴────────────────┴─────────────────┘
                                  ▼
                     merge back into per-word records
                                  ▼
                          genanki → deck.apkg
```

Two implementation notes worth building in from v0:

- **Batch the calls that don't need to be per-word.** Translation and example
  sentences can each be a *single* call across the whole word list with
  structured JSON output, instead of N calls. Fewer round trips, and it's
  meaningfully cheaper and faster.
- **Parallelize the calls that are genuinely independent.** Once you have the
  word list, image generation and TTS for each word are independent of each
  other — fire them concurrently (`asyncio.gather`) instead of looping
  sequentially. This is most of what "agentic harness" buys you in practice:
  fan-out, collect results, retry what failed.

Structured output pattern (use this instead of parsing free-form text — more
reliable, and it's the "data processing / debugging" skill the JD calls out):

```python
from google import genai
from pydantic import BaseModel

class VocabEntry(BaseModel):
    word: str
    tags: list[str]

class VocabList(BaseModel):
    entries: list[VocabEntry]

client = genai.Client()  # reads GEMINI_API_KEY from the environment

response = client.models.generate_content(
    model="gemini-2.5-flash-lite",
    contents=[uploaded_image, "Extract every vocabulary word visible in this "
              "list, in reading order, with any tags the user marked."],
    config={"response_mime_type": "application/json",
            "response_schema": VocabList},
)
parsed: VocabList = response.parsed
```

`genanki` note type with image + audio embedded on both sides:

```python
import genanki

model = genanki.Model(
    1607392319, "Vocab (image+audio)",
    fields=[{"name": "Word"}, {"name": "Image"}, {"name": "Sentence"},
            {"name": "Translation"}, {"name": "Audio"}],
    templates=[{
        "name": "Card 1",
        "qfmt": "{{Word}}<br>{{Image}}",
        "afmt": "{{FrontSide}}<hr>{{Translation}}<br>{{Image}}<br>"
                "{{Sentence}}<br>{{Audio}}",
    }],
)
note = genanki.Note(
    model=model,
    fields=[word, f'<img src="{img_file}">', sentence, translation,
            f"[sound:{audio_file}]"],
    tags=tags,
)
```

## 6. What it'll actually cost

Worked example: one 50-word deck, every milestone enabled (v4, full
featured), standard (non-batch) pricing:

| Step | Calls | Approx. cost |
|---|---|---|
| OCR + parse + tag | 1 call | < $0.001 |
| Translation | 1 batched call | < $0.001 |
| Example sentences | 1 batched call | < $0.001 |
| Illustrations | 50 calls (1/word) | ~$1.68 |
| Pronunciation (word + sentence) | ~100 short clips | ~$0.02–0.05 |
| **Total** | | **~$1.70–1.75** |

With the Batch API on the image and text calls (~50% off, and this pipeline
is a perfect fit for Batch since deck generation is inherently
upload-then-wait, not a live chat): **~$0.85–0.90 per deck.**

The takeaway that should actually shape the build: **illustrations are ~95%
of the cost, everything else is noise.** Practical implications:

- Make images and audio toggle-able flags while developing/debugging, so you
  aren't regenerating (and re-billing) art every time you fix a translation bug.
- Cache generated images and audio keyed by `(word, target_lang)` — if the
  same word shows up in a future deck, reuse the file instead of regenerating.
- If you want an even cheaper always-on public demo later, illustrating only
  a subset (e.g. concrete nouns) rather than every entry is a reasonable,
  defensible product trade-off — and a good thing to be able to explain in an
  interview.

## 7. Suggested build order

Same five milestones, with a concrete "done" bar for each — this is the part
that actually teaches how to scope a real project:

0. **Setup.** Repo, venv, `pip install google-genai genanki python-dotenv`,
   `.env` for the API key (in `.gitignore` from the first commit), one sample
   vocab-list photo checked in as a fixture. **Done when:** a one-line script
   using `client.models.generate_content` returns a response.
1. **v0 — OCR + translate + basic cards.** **Done when:** feeding the fixture
   photo produces a `.apkg` that imports into Anki with correct word/translation
   pairs.
2. **v1 — tags.** **Done when:** a photo with a mix of tagged and untagged
   entries produces cards whose tags are correct and filterable in Anki's browser.
3. **v2 — illustrations.** **Done when:** cards show a relevant image on both
   sides, and the media embeds correctly — verify by importing the `.apkg` on
   a second machine or a fresh Anki profile, which catches "forgot to bundle
   the media file" bugs that look fine locally.
4. **v3 — example sentences.** **Done when:** the sentence for a handful of
   spot-checked words actually uses that word naturally (LLMs occasionally
   dodge the target word — worth an explicit check in your prompt or a
   post-hoc validation).
5. **v4 — pronunciation.** **Done when:** tapping the card plays correct
   audio for both the word and the example sentence.
6. **Stretch — serving.** Minimal FastAPI wrapper around the pipeline,
   containerize, deploy to Cloud Run. This is the milestone that maps most
   directly to the job's "cloud infrastructure" preferred qualification.

## 8. Habits worth building in from day one

- Commit at the end of each milestone — a clean git log is itself evidence of
  "shipped incrementally," which is the resume story you want.
- `.env` + `python-dotenv` for the API key; never hardcode it, `.gitignore`
  it from commit #1.
- Structured output (`response_schema`) on every call you need to parse — not
  regex on free text.
- Basic retry/backoff around API calls (the `tenacity` package makes this a
  few lines) — rate limits and transient failures are normal, not exceptional,
  and handling them is literally "debugging ML infrastructure."
- Cache by `(word, lang)` so re-running the pipeline while debugging doesn't
  regenerate — and re-bill — images or audio you already have.
- Keep the one small fixture image in the repo so the whole pipeline is
  runnable in seconds by anyone (including future you) without hunting for a
  test photo.

## 9. Turning this into resume lines

Drafts to adapt once it's actually built — don't claim these until they're true:

- *"Built an end-to-end GenAI pipeline (Gemini multimodal OCR, translation,
  image and speech generation) that turns a photo of a vocabulary list into
  ready-to-study Anki flashcards, fanning out to 5 model calls per deck with
  async batching."*
- *"Made explicit performance/cost trade-offs — model tier selection,
  request batching, generation caching — to keep a fully-illustrated,
  narrated 50-card deck under $1 in inference spend."*
- *"Shipped 5 incremental versions of the pipeline (OCR → translation →
  tagging → illustration → speech), each independently testable and demoable."*

## 10. Where to double-check before/while you build

Google's Gemini lineup changes every few months (2.0 Flash was fully shut
down June 1, 2026; the image model used here didn't exist until mid-2026).
Before you commit to model names in code, re-check:

- Pricing & current model list: `ai.google.dev/gemini-api/docs/pricing`
- Rate limits (free tier RPM/RPD): `ai.google.dev/gemini-api/docs/rate-limits`
- Deprecations: `ai.google.dev/gemini-api/docs/deprecations`
