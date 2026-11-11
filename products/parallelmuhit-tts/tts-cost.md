# eleven v4 cost for the parallelmuhit essays

computed 2026-11-11 from `pdp/parallelmuhit/essays_md/` (188 essays). the per-essay table is in
[`tts-cost-per-essay.csv`](tts-cost-per-essay.csv).

## what is counted

the text that would be read aloud: the title plus the body. not counted: the front matter, the date
line (`*13.08.26*`) or markdown symbols. links keep their text and images are dropped. spaces and
punctuation count, because elevenlabs bills every character.

## totals

| | value |
|---|---|
| essays | 188 |
| characters, total | **1,836,859** |
| characters per essay, avg / median | 9,770 / 9,517 |
| shortest | #12 `asli`, 5,732 |
| longest | #188 `jarlik2`, 19,398 |
| essays over 10,000 chars (v4's limit for one request) | 82, so they need 2 requests each |
| api requests, total | 270 |
| audio, rough | ~1 min per 1,000 chars, so ~31 hours in total, ~10 min per essay |

## money

| way to pay | what it gives | the full back catalog (1.84M chars) |
|---|---|---|
| pay-as-you-go api, v4 at $0.08 / 1k chars | — | **≈ $147** once (≈ $0.78 per avg essay) |
| your current plan: starter, 40,000 / month (as reported by the account api) | ~4 essays / month | ~46 months — far too slow |
| creator, $22 / month, "275k characters of tts (v4)" | ~28 essays / month | ~7 months ≈ $154 |

new essays after the back catalog: ~10k chars each, ≈ $0.80 each at the api rate. one a week
fits inside the starter plan.

## caveats, not verified

- the elevenlabs pricing page lists starter as "75,000 ~75 min", but your account's api reports a
  limit of 40,000. so the rate that converts characters into plan credits for v4 is unclear.
  check it before a big run: note `character_count` in the account, generate one essay, and
  compare.
- these are list prices from elevenlabs.io/pricing/api on 2026-11-11, and they may change.
- regenerating an essay costs the full amount again. section 2 of the plan should skip essays
  that already have an mp3.
- the account showed 751 of 40,000 used on the starter plan after your two stress tests.
