# Flashcard Project — Step-by-Step Walkthrough

This is the "just tell me what to do, in order" version. The other doc
(`flashcard-project-design-doc.md`) has the full reasoning and cost tables —
keep it nearby for reference, but this one is the doc to actually work from.

Work through the sessions in order. Check items off as you go. Don't skip
ahead — each one only takes 20–60 minutes, and every session ends with
something that visibly works, which is the whole point.

## The money map, up front

So this isn't hanging over you the whole time: **everything through Session
5 (tags) costs nothing and needs no payment method at all.** Sign in with a
Google account, get a key, go. **Session 9 (pronunciation) is also free.**

There is exactly **one** step that needs a card on file: **Session 6
(images)** — Google doesn't offer a free tier for image generation, full
stop, no way around it. When you get there, this doc walks through setting
a hard $5 spend cap and turning off auto-reload first, so the honest worst
case for this entire project is a one-time $10 charge (Google's minimum
top-up) — and you'll likely use $1-3 of it. Full mechanics are in Session 6,
not before, so you're not thinking about billing while you're still doing
free stuff.

---

## Session 0 — Repo, editor, and (optional) an AI helper

- [ ] Install Python 3.11+ if you don't have it (`python3 --version` to check)
- [ ] Install Git if you don't have it
- [ ] Install [VS Code](https://code.visualstudio.com/)
- [ ] Create a repo — either `git init` in a new local folder, or make one on
      GitHub first and clone it. GitHub's nice here: free, and it's the repo
      you'll eventually link from your CV.
- [ ] Open the folder in VS Code

**Optional, 2 minutes, but worth doing:** grab a free AI coding helper for
when you get stuck. You don't strictly need it — there isn't a huge amount
of code here — but it's free and it's a nice thing to have wired in.

- [ ] In VS Code: Extensions icon (left sidebar) → search **"Google
      Antigravity"** → Install → sign in with your Google account. It's free
      for individuals, no card needed, and it's literally one of the tools
      named in the job posting — a small, honest bonus talking point.
- [ ] If that's fussy or unavailable, **GitHub Copilot** has a well-known
      free tier (search "GitHub Copilot" in Extensions) — fine fallback.
- [ ] Either way, for "why is this erroring" moments, just opening
      `gemini.google.com` or `aistudio.google.com` in a browser tab and
      pasting the error works completely fine too. You don't need anything
      installed for that — your instinct on this was right.

- [ ] `python3 -m venv .venv` then activate it
      (`source .venv/bin/activate` on Mac/Linux, `.venv\Scripts\activate` on
      Windows)
- [ ] `pip install google-genai python-dotenv genanki pillow`
- [ ] Create a `.gitignore` with at least:
      ```
      .venv/
      .env
      __pycache__/
      media/
      ```
- [ ] First commit: `git add -A && git commit -m "project scaffold"`

**Done when:** the folder is a repo, the venv installs cleanly, and VS Code
has it open. That's the annoying part finished — everything from here is
more interesting.

---

## Session 1 — Say hello to Gemini (free, no card)

- [ ] Go to `aistudio.google.com`, sign in with your Google account
- [ ] Click **Get API key** — this is free, no payment method required
- [ ] Create a `.env` file in your project (make sure it's in `.gitignore`
      before you put anything in it):
      ```
      GEMINI_API_KEY=your_key_here
      ```
- [ ] Create `hello.py`:
      ```python
      import os
      from dotenv import load_dotenv
      from google import genai

      load_dotenv()
      client = genai.Client()  # picks up GEMINI_API_KEY automatically

      response = client.models.generate_content(
          model="gemini-2.5-flash-lite",
          contents="Say hello, and tell me one interesting fact about flashcards.",
      )
      print(response.text)
      ```
- [ ] Run it: `python hello.py`

**Done when:** you see real Gemini text in your terminal.

🎉 First real milestone — you just called a frontier AI model from your own
code, for $0.

---

## Session 2 — Teach it to read a photo

- [ ] Take or find one JPEG with a couple of words on it — a sticky note
      photo is genuinely fine for this test
- [ ] Extend the script to send the image alongside a prompt:
      ```python
      from PIL import Image

      img = Image.open("test_photo.jpg")
      response = client.models.generate_content(
          model="gemini-2.5-flash-lite",
          contents=[img, "What words do you see in this image? List them."],
      )
      print(response.text)
      ```

**Done when:** the printed output correctly lists the words in your photo.

🎉 That's OCR. No separate OCR service, no separate library — same model,
same free key you already have.

---

## Session 3 — Structured output + your first real flashcard

This is the milestone worth savoring, so don't rush it.

- [ ] **Learn structured output first:** instead of asking for a sentence
      and picking it apart, define the shape you want and ask Gemini to fill
      it in directly. Much less fragile than parsing free text.
      ```python
      from pydantic import BaseModel

      class Entry(BaseModel):
          word: str
          translation: str

      response = client.models.generate_content(
          model="gemini-2.5-flash-lite",
          contents=[img, "Read the main word in this image and translate it "
                    "to English. Return structured data."],
          config={"response_mime_type": "application/json",
                  "response_schema": Entry},
      )
      entry: Entry = response.parsed
      print(entry.word, entry.translation)
      ```
- [ ] **Done when:** `entry.word` and `entry.translation` print cleanly —
      no manual string-splitting involved anywhere.
- [ ] **Turn it into a flashcard with `genanki`:**
      ```python
      import genanki

      model = genanki.Model(
          1607392319, "Vocab Basic",
          fields=[{"name": "Word"}, {"name": "Translation"}],
          templates=[{
              "name": "Card 1",
              "qfmt": "{{Word}}",
              "afmt": "{{FrontSide}}<hr>{{Translation}}",
          }],
      )
      deck = genanki.Deck(2059400110, "My Vocab Deck")
      deck.add_note(genanki.Note(model=model, fields=[entry.word, entry.translation]))
      genanki.Package(deck).write_to_file("deck.apkg")
      ```
- [ ] Open desktop Anki → **File → Import** → pick `deck.apkg`
- [ ] **Done when:** you see one real card, word on front, translation on back.
- [ ] Sync it to your phone: in Anki desktop, click **Sync** (top toolbar),
      create a free AnkiWeb account the first time it asks. Then open Anki on
      your phone and sync there too.
      - **Android:** AnkiDroid is free.
      - **iPhone:** the official AnkiMobile app is a one-time **$24.99**
        purchase — the one real cost in this whole project that has nothing
        to do with Google or AI. If you want to stay at $0, open
        `ankiweb.net` in your phone's browser instead and log in — clunkier,
        but free, and enough to confirm the card looks right.

**Done when:** you can see and flip your one flashcard, on your phone.

🎉🎉 **This is the "claim big success" moment — actually stop and look at
it.** You just built a complete pipeline: a photo goes in, an AI reads it,
an AI translates it, your code turns that into a real study tool you're
holding in your hand. Every session from here is repeating this pattern,
not inventing a new one — that's genuinely most of the hard part done.

---

## Session 4 — Make it handle a real list, not just one word

- [ ] Swap your single-word test photo for an actual vocab list photo
      (5–10 words is plenty to test with)
- [ ] Change the schema to a list:
      ```python
      class VocabList(BaseModel):
          entries: list[Entry]
      ```
- [ ] Loop over `vocab_list.entries`, create one `genanki.Note` per entry,
      add them all to the same `Deck`, write one `.apkg`

**Done when:** importing that `.apkg` gives you N correct cards, not just one.

🎉 Quick one, but it's the difference between a demo and a tool.

---

## Session 5 — Tags (still free, still no card)

- [ ] Add a `tags: list[str]` field to `Entry` — ask Gemini to include any
      tags visible in the photo (or leave the list empty if there aren't any)
- [ ] Pass them through: `genanki.Note(model=model, fields=[...], tags=entry.tags)`

**Done when:** tagged cards show up as filterable tags in Anki's Browse
window (left sidebar).

---

## Session 6 — Images 💳 (the one step that needs a payment method)

**Why here specifically:** unlike text and audio, Gemini's image models (the
"Nano Banana" family) have no free tier at all — this is the one wall a
free key genuinely can't get past.

**Set the guardrails before you generate a single image:**

- [ ] In AI Studio, go to **Set up billing**. Google will most likely put
      you on **Prepay** automatically (this is now the default for new
      accounts) — if you get a choice, pick Prepay, not a monthly invoice.
- [ ] You'll be asked to buy a credit balance. **Minimum is $10** — that's
      Google's floor, worth knowing upfront so it's not a surprise (a true
      $5 minimum isn't currently offered).
- [ ] Immediately after, two settings — both matter:
  - [ ] Go to the **Spend** tab → **Monthly spend cap** → set it to **$5**.
        Once real usage hits that, requests get blocked until you raise it
        or the month rolls over. (Small print: there's a ~10-minute
        enforcement delay on this, but a single image here costs a few
        cents, so a realistic worst-case overshoot is trivial.)
  - [ ] Make sure **auto-reload stays off** (it's off by default — just
        don't turn it on). This is what makes the $10 an actual hard
        ceiling: once that balance is used up, calls simply stop. Nothing
        touches the card again unless you go back in and manually buy more.
  - [ ] Net effect: **$10, once, is the absolute maximum this entire
        project can ever cost** — and given real per-image cost, you'll
        likely use $1–3 of it. (Don't count on the general $300 Google
        Cloud trial credit here — it's inconsistently applied to Gemini API
        billing and shouldn't be part of the plan.)

**Now generate one test image before wiring anything up:**

- [ ] Run this and check the output:
      ```python
      from io import BytesIO
      from PIL import Image

      response = client.models.generate_content(
          model="gemini-3.1-flash-lite-image",
          contents="A simple, friendly illustration of an apple, flashcard style.",
      )
      for part in response.candidates[0].content.parts:
          if part.inline_data is not None:
              Image.open(BytesIO(part.inline_data.data)).save("test_image.png")
      ```
- [ ] **Done when:** `test_image.png` opens and looks reasonable.
- [ ] Wire it into the pipeline: one image per word, add it to
      `Package(deck).media_files`, reference it in both card fields with
      `<img src="...">`.

**Done when:** cards show a real picture on both front and back.

🎉 The deck actually looks like a product now.

---

## Session 7 — Make it fast

- [ ] Same number of API calls as before — just don't wait for them one at a
      time. Use `asyncio.gather` (or a plain `ThreadPoolExecutor` if async
      feels like a lot right now) so the image calls for a 10-word deck fire
      concurrently instead of in sequence.

**Done when:** a 10-card deck generates noticeably faster, and your Spend
Cap total confirms the cost didn't change — you're just not waiting around
for it anymore.

---

## Session 8 — Example sentences

- [ ] Same shape as translation: add an `example_sentence` field to `Entry`,
      ask for it in the same batched call as everything else. Still text —
      stays on the free tier.
- [ ] Card layout: word + image + sentence on front; translation + image +
      sentence translation on back.

**Done when:** a handful of spot-checked sentences actually read naturally
and use the target word.

---

## Session 9 — Pronunciation (good news: this one's free too)

Unlike images, Gemini's text-to-speech has a free tier — no new billing
step here.

- [ ] Generate and save one word's audio:
      ```python
      import wave
      from google.genai import types

      def save_wave(filename, pcm_data, channels=1, rate=24000, sample_width=2):
          with wave.open(filename, "wb") as wf:
              wf.setnchannels(channels)
              wf.setsampwidth(sample_width)
              wf.setframerate(rate)
              wf.writeframes(pcm_data)

      response = client.models.generate_content(
          model="gemini-2.5-flash-preview-tts",
          contents=f"Say clearly, at a natural pace: {entry.word}",
          config=types.GenerateContentConfig(
              response_modalities=["AUDIO"],
              speech_config=types.SpeechConfig(
                  voice_config=types.VoiceConfig(
                      prebuilt_voice_config=types.PrebuiltVoiceConfig(voice_name="Kore")
                  )
              ),
          ),
      )
      pcm = response.candidates[0].content.parts[0].inline_data.data
      save_wave("word.wav", pcm)
      ```
- [ ] Add the `.wav` files to `media_files`, reference them in a field as
      `[sound:word.wav]`

**Done when:** tapping the card in Anki plays the correct pronunciation.

🎉🎉 **Full pipeline, done.** Photo → OCR → translation → tags → images →
example sentences → pronunciation → a real deck, on your phone. That's every
milestone from the design doc, actually shipped.

---

## Where to stop

For the CV, this is genuinely enough. An MVP that works end-to-end on a
handful of real decks *is* the story — you don't need to handle huge word
lists, bulletproof every edge case, or deploy it anywhere unless that
sounds like fun on its own terms. If it does, the design doc's "stretch —
serving" section (Cloud Run) is the natural next step, but it's optional,
and it costs nothing to skip.
