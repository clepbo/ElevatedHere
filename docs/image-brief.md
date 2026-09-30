# Image brief — ElevatedHere landing pages

Everything on the site right now is **placeholder stock** (generic, Western, not our context).
These are the slots to replace, with prompts you can paste into an image generator.

## House rules — apply to every image

Put this at the end of every prompt so the set hangs together:

> Natural documentary photography, shot on 35mm, soft diffused daylight, shallow depth of field,
> muted warm colour grade with desaturated greens, no harsh studio lighting, no stock-photo smiling
> at camera, no thumbs-up, no handshakes, no laptops-and-graphs clichés, authentic candid moment,
> West African / Nigerian setting, natural skin tones, photorealistic, 4k.

**Do not include:** visible logos, readable screens, medical equipment that implies a hospital,
anything that identifies a real clinic, distressed or crying subjects, anything that reads as an
illness portrayal. Dignity is the brief — these are people getting support, not patients.

**Consistency:** same colour grade across the whole set, same lens character. If your tool supports
a seed or style reference, lock it after the first approved image and reuse it.

---

## 1. Hero — twin scrolling columns (6 images)

**Slot:** `index.html` → `.hero-media` → `.col.up` and `.col.down`
**Ratio:** 3:4 portrait · **Export:** 1040×1387, WebP, ~200KB

These scroll continuously so they read as a texture of real people. Vary age, gender, setting and
framing — three should be people *receiving* support, three *delivering* it.

1. **Quiet conversation** — Two women in their 30s sitting at an angle to each other beside a large
   window in a softly lit room, mid-conversation, one listening intently with her hand resting on
   the arm of the chair. Warm afternoon light. Not clinical — feels like a comfortable private room.

2. **Therapist at work** — A Nigerian man in his 40s in a relaxed shirt seated in an armchair,
   notebook closed on his lap, leaning slightly forward, attentive expression, warm neutral room
   with a plant just out of focus behind him.

3. **Beneficiary portrait** — A Nigerian woman in her late 20s in a plain top, seated near a window,
   looking away from camera in a calm reflective moment. Natural light on one side of her face.
   Composed and dignified, not sad.

4. **Workplace cohort** — Four colleagues of mixed gender and age standing in an informal semicircle
   in a bright modern Lagos office, mid-discussion, one gesturing. Candid, not posed to camera.

5. **Younger beneficiary** — A man in his early 20s sitting on outdoor steps with a phone in hand,
   relaxed posture, looking off to the side, early evening light. Ordinary moment, not lonely.

6. **Coach / practitioner** — A woman in her 50s with natural grey-streaked hair in a warm-toned
   room, seated, hands loosely clasped, calm authoritative presence. Mid-gesture as if speaking.

---

## 2. Split headline card — "Real ___ Outcomes" (1 image)

**Slot:** `index.html` → `.split .slot .pcard`
**Ratio:** 4:5 portrait · **Export:** 900×1125

The card slides in between the two words, so it needs to work at small size and read instantly.

> A Nigerian woman in her 30s photographed from the chest up in three-quarter profile, eyes closed
> for a brief moment, slight relief in her expression, plain warm-grey background, single soft light
> source from the left. Intimate and calm.

---

## 3. Outcomes cluster — main card (1 image)

**Slot:** `index.html` → `.cluster .cl` (first, largest)
**Ratio:** 16:11 landscape · **Export:** 1120×770

Floating stat cards overlay the right edge, so keep the subject **left of centre** and leave the
right third quiet.

> A practitioner and a client seated across a low table in a bright neutral room, seen from a
> respectful distance, both mid-conversation, the client's back partly to camera so they are not
> identifiable. Subject positioned in the left two-thirds of the frame, uncluttered wall on the right.

---

## 4. Testimonial carousel (3 images)

**Slot:** `index.html` → `.tslide .tphoto`
**Ratio:** 4:3 landscape · **Export:** 1200×900

Each pairs with a quote, so these should feel like environmental portraits of real professionals.

1. **HR director, employer** — A Nigerian woman in her 40s in smart-casual business dress standing
   in a modern open-plan office, arms relaxed, half-smiling, looking slightly off camera. Depth of
   field softening colleagues behind her.
2. **Head of people, manufacturing** — A man in his 50s in a light shirt standing in a bright
   corridor or atrium, hands in pockets, warm confident expression, looking to camera.
3. **Clinical psychologist** — A woman in her 30s in a softly furnished consulting room, seated in
   an armchair turned toward camera, notebook on the side table, calm professional presence.

---

## 5. Final mosaic (6 images)

**Slot:** `index.html` → `.mosaic .pcard`
**Ratio:** 1:1 square (third one 1:1.3 portrait) · **Export:** 840×840

A rhythm of small moments — the programme working, not posed portraits. Crops tight.

1. Two hands holding a warm mug, table detail, soft light
2. A woman laughing mid-conversation, tight crop on the face, candid
3. *(portrait 1:1.3)* A man in his 30s seated in profile beside a window, calm
4. A small group walking together outdoors in a Lagos business district, back view
5. A practitioner's hands gesturing while speaking, shallow focus
6. A young woman looking directly to camera, neutral confident expression, plain background

---

## 6. Optional — preloader background

Currently a CSS gradient (soft green → teal → blue), which works. If you would rather have a
texture:

> Abstract soft-focus macro of layered translucent green and teal glass, gentle gradient from
> yellow-green to pale blue, no recognisable objects, very low contrast, calm and airy.

Export 2000×1400, WebP, under 300KB.

---

## Delivery

Drop the files into `assets/img/` and name them by slot, e.g.:

```
assets/img/hero-1.webp … hero-6.webp
assets/img/split-card.webp
assets/img/cluster-main.webp
assets/img/testimonial-1.webp … testimonial-3.webp
assets/img/mosaic-1.webp … mosaic-6.webp
```

Send them over and I will swap every `images.unsplash.com` URL for the local files, set correct
`width`/`height` to stop layout shift, add `loading="lazy"` below the fold, and write real alt text
for each one.
