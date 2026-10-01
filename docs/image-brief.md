# Image brief — ElevatedHere landing pages (v2)

**What changed in this version.** The first brief asked for muted, documentary-style photography.
That was wrong for this product: it produced frames that read as rural and informal, when the
audience is professional — HR directors, finance leads, clinicians, lawyers, corporate employees.
This version calls for **bright, polished, contemporary brand photography in a Nigerian corporate
context**: modern offices, glass and daylight, tailored clothing, clean consulting rooms.

---

## House style — append to every prompt

> Bright, high-key commercial brand photography. Large soft light source, airy and luminous, clean
> white and light-neutral environment, minimal shadow, crisp natural colour with true skin tones.
> Shot on 85mm at f/2, shallow depth of field, sharp subject against a softly blurred modern
> interior. Contemporary Nigerian professionals in a Lagos corporate setting — tailored, well-styled,
> confident and at ease. Editorial quality, photorealistic, 4k.

**Colour note:** keep it bright and clean so it sits on the site's white and `#fafafa` grounds.
Natural saturation — do **not** desaturate or apply a warm vintage grade. Where a green appears
naturally (a plant, a jacket, signage) it flatters the brand, but nothing should look colour-graded.

**Wardrobe:** tailored blazers, well-cut shirts and blouses, smart knitwear, modern eyewear,
considered jewellery. Contemporary and aspirational — the way senior professionals in Lagos,
Abuja or Port Harcourt actually dress for work.

**Environments:** glass-walled meeting rooms, bright open-plan offices, modern co-working spaces,
clean minimalist consulting rooms with good furniture, corporate lobbies with daylight.

### Negative prompt — paste into the negative field

> rural, village, informal settlement, market stall, outdoor street scene, dim lighting, moody,
> muted colours, desaturated, sepia, vintage grade, grainy, documentary photojournalism, harsh
> shadows, cluttered background, medical equipment, hospital, patient gown, distress, crying,
> poverty imagery, charity appeal, thumbs up, handshake, forced smile at camera, posed stock photo,
> visible logos, readable screen text, watermark

**Also avoid:** anything that frames a person as a patient or a recipient of charity. These are
people using a benefit they have earned. Dignity and competence throughout.

**Consistency:** lock a seed or style reference after the first approved image and reuse it, so the
whole set matches.

---

## 1. Hero — twin scrolling columns (6 images)

`index.html` → `.hero-media` · **3:4 portrait** · export **1040×1387**, WebP, ~200KB

These scroll continuously as a texture of people. Three receiving support, three delivering it.

1. **Two colleagues in conversation** — Two Nigerian women in their 30s in tailored blazers seated
   at an angle in a bright glass-walled meeting room, mid-conversation, one listening attentively.
   Daylight flooding from a window wall behind them.

2. **Therapist in a modern consulting room** — A Nigerian man in his 40s in a crisp shirt and
   contemporary eyewear, seated in a designer armchair, notebook closed on his lap, warm attentive
   expression. Bright minimalist room, pale walls, one sculptural plant.

3. **Professional portrait** — A Nigerian woman in her late 20s in a smart blouse, standing in a
   bright corporate lobby, looking slightly off camera with a composed confident expression. Clean
   architectural background, soft daylight.

4. **Team in an open-plan office** — Four Nigerian professionals of mixed gender and age standing
   in an informal semicircle in a bright modern Lagos office, mid-discussion, one gesturing to a
   whiteboard. Candid, energetic, well-dressed.

5. **Younger professional** — A Nigerian man in his late 20s in a fitted shirt seated on a modern
   sofa in a bright co-working lounge, phone in hand, relaxed and assured. Light wood and white
   interior.

6. **Senior practitioner** — A Nigerian woman in her 50s with elegant natural grey-streaked hair,
   in a well-cut blazer, standing in a bright consulting room, hands loosely clasped, warm
   authoritative presence.

---

## 2. Split headline card — "Real ⟨card⟩ Outcomes" (1 image)

`index.html` → `.split .slot` · **4:5 portrait** · export **900×1125**

Small on screen, so it must read instantly.

> A Nigerian woman in her 30s in a tailored blazer, photographed chest-up in three-quarter profile
> against a clean pale-grey studio background, calm assured half-smile, bright even lighting from
> the left. Polished corporate portrait, aspirational and warm.

---

## 3. Outcomes cluster — main card (1 image)

`index.html` → `.cluster .cl` (largest) · **16:11 landscape** · export **1120×770**

Stat cards overlay the right edge — keep the subject **left of centre**, right third quiet.

> A practitioner and a client seated across a low designer table in a bright modern consulting
> room, both mid-conversation, the client seen from behind at an angle so they are not identifiable.
> Subject in the left two-thirds, clean uncluttered pale wall on the right. Floor-to-ceiling window
> light.

---

## 4. Testimonial carousel (3 images)

`index.html` → `.tslide .tphoto` · **4:3 landscape** · export **1200×900**

Environmental portraits of credible senior professionals.

1. **HR director** — A Nigerian woman in her 40s in a sharp blazer standing in a bright open-plan
   office, arms relaxed, confident half-smile, looking slightly off camera. Colleagues softly
   blurred behind.
2. **Head of people** — A Nigerian man in his 50s in a crisp light shirt standing in a bright
   corporate atrium with glass and daylight, hands in pockets, warm assured expression to camera.
3. **Clinical psychologist** — A Nigerian woman in her 30s in smart professional dress, seated in
   a designer armchair in a bright well-appointed consulting room, notebook on the side table,
   calm and credible.

---

## 5. Final mosaic (6 images)

`index.html` → `.mosaic` · **1:1 square** (third one **1:1.3 portrait**) · export **840×840**

Bright, upbeat fragments of professional life. Tight crops.

1. Two well-manicured hands holding a ceramic coffee cup on a light marble desk, bright and clean
2. A Nigerian woman laughing genuinely mid-conversation, tight crop, bright office background
3. *(portrait)* A Nigerian man in his 30s in a blazer seated in profile beside a floor-to-ceiling
   window, city skyline softly blurred
4. Three colleagues walking together through a bright modern corporate lobby, mid-stride, candid
5. A practitioner's hands gesturing while speaking, shallow focus, bright neutral room
6. A Nigerian woman in her 20s in smart-casual dress looking directly to camera, confident, clean
   bright background

---

## 6. Optional — preloader background

Currently a CSS gradient (green → teal → blue) and it works. If you prefer a texture:

> Abstract bright macro of layered translucent green and teal glass, luminous gradient from fresh
> green to pale blue, airy and high-key, no recognisable objects, very low contrast.

Export 2000×1400, WebP, under 300KB.

---

## Delivery

```
assets/img/hero-1.webp … hero-6.webp
assets/img/split-card.webp
assets/img/cluster-main.webp
assets/img/testimonial-1.webp … testimonial-3.webp
assets/img/mosaic-1.webp … mosaic-6.webp
```

Send them over and I will swap every placeholder URL for the local files, set `width`/`height` to
prevent layout shift, add `loading="lazy"` below the fold, and write real alt text for each.

**If one or two still miss the mark, send me the generated image** and I will adjust the specific
prompt rather than have you guess — it is much faster to correct against an actual output.
