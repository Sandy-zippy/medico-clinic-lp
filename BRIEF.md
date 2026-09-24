# MEDICO LANDING PAGE — LOCKED BRIEF (Sandy, 24 Sep 2026)

Source: Sandy pasted this spec in full. It SUPERSEDES every earlier instruction in this project,
including ones Sandy himself gave earlier the same night. Where this brief and an older note
disagree, THIS BRIEF WINS. Do not re-litigate it.

## Two reversals of earlier instructions (deliberate, do not undo)
1. **DO NOT ASK BUDGET.** Earlier tonight a budget question was added at Sandy's request. This
   brief removes it. Qualify instead on: project type, location stage, clinic type, SQUARE
   FOOTAGE, timeline. Reason: budget questions add friction and make the visitor feel screened;
   sq ft + lease stage + timeline + type give the sales team a better pre-call briefing.
2. **PRIMARY CTA IS "Tell Us About My Clinic".** Not "Book my site visit" (shipped earlier
   tonight, now wrong). Not "Send my project". Not "Submit". Not "Get quote".

## Who the client is
Medico Construction & Design. Healthcare construction, British Columbia and Alberta.
GLOBAL client. **Bhargav is India-side only and is NOT involved in Medico.** Never name him.
Brand: #1475bc blue, #404041 charcoal. Montserrat 700 + Open Sans 400 ONLY (those two font files
are the only ones that ship; any other family or weight is browser-synthesised and fails a gate).

## Conversion goal
NOT to book a site visit instantly. It is: collect enough project information for Medico to CALL
the lead and qualify. Form answers become the caller's pre-call briefing.
Target project economics ~$150K+, but this is never stated to the visitor.

## The page must feel like
Established healthcare construction company + sophisticated design-build firm + credible local
operator. NOT a generic contractor template, NOT a SaaS landing page, NOT an architecture
portfolio, NOT AI-generated, NOT a flashy startup site.

## Visual language
Clean, architectural, clinical, premium, trustworthy, local, professional.
White used generously but no dead space. Medico blue for CTAs, highlights, icons, section
accents, interactive states. Charcoal for primary headings and occasional high-contrast sections.
Very light blue/grey backgrounds separate sections.
AVOID: excessive gradients, excessive shadows, glassmorphism, giant rounded SaaS cards everywhere.
Radius: 8-12px standard cards, 12-16px for major image/form containers. Subtle borders,
restrained shadows. The identity communicates CONSTRUCTION PRECISION, not software.

## Typography targets (desktop)
H1 52-60px · H2 36-44px · H3 22-28px · Body 17-19px · Supporting 14-16px.
Do NOT make every heading oversized. Body copy max 65-75 characters per line. Left-aligned.
Avoid long centred paragraphs.

## Grid
One consistent max content width, 1180-1240px, everywhere. No section uses a different width.

## Spacing system
Desktop section spacing 80-110px. Mobile 56-72px.
Headline to copy 16-20px. Copy to content 32-48px. No arbitrary blank areas.

## CTA SYSTEM (standardise, the page currently has too many wordings)
PRIMARY everywhere: **Tell Us About My Clinic**
Secondary contextual, all scrolling to the SAME form, no separate conversion paths:
  Assess My Space · Review My Space · Plan My Clinic · Start My Clinic Plan
BANNED CTA words: Buy now, Get quote instantly, Book site visit, Get pricing, Submit, Send my project.

## OVERRIDE, Sandy 24 Sep 2026 (later than this brief): ADD 3D MOTION GRAPHICS
"add 3D motion graphic elements on all the sections where it's applicable so the landing page looks
dynamic." This replaces the BANNED list below for scroll animation and 3D. Still banned: bounce/elastic
easing, auto-rotating carousels, video backgrounds, cursor effects, anything that hides content without
JS or under prefers-reduced-motion. Motion lives in motion.js + the MOTION block of styles.css;
qa/motion_test.py must show nothing stranded.

## FORM AUDIT, 24 Sep 2026 (Sandy asked for a qualified-leads audit). Changes to the question set above:
- Q3 clinic type: + Optometry / Eye care, + Veterinary (21 of Medico's 52 portfolio projects; 6 of 49 Meta leads
  were optometry and would otherwise have picked "Other").
- NEW step 6 "Where is the clinic?" (region taps incl. "Outside BC and Alberta", which shows a note but still sends).
  Reason: 21 of 49 Meta leads answered location "Other"; free-text city alone cannot be screened.
- Contact step: + "You are the" (Clinic owner / practitioner, Practice manager, Developer / landlord, Other).
- Phone must be a valid North American number. Hidden fields: lead_grade (A/B/C), seconds_on_form.
- Still NO budget question (this brief's rule stands).
- Sandy 24 Sep (later): one-tap steps AUTO-ADVANCE (no Continue; "Outside BC and Alberta" stays to show its note).
  "Full name" replaces first + last. Clinic types = Medico's own /sectors/ list only (Diagnostic/Imaging removed).
- thank-you.html: greets by first name, echoes their answers, marks their clinic type, proof strip, what happens next.
  Data passes via sessionStorage (never the URL). Until the form is connected, it shows "Preview: nothing was sent".

## Interaction
Allowed: subtle button hover, card border change, smooth accordion, progress animation,
form selected-state animation, subtle image zoom on portfolio hover.
BANNED: excessive scroll animation, parallax, floating elements, bouncing CTAs, auto-rotating
carousels, video backgrounds, cursor effects. Construction buyers need confidence, not entertainment.

## Mobile (design mobile-first)
Hero single column: headline, supporting copy, trust indicators, THEN the form. The image must not
push the form far below the fold. 16-20px horizontal padding. 48px minimum interactive targets.
No horizontal timelines, no tiny maps, no side-by-side testimonials, no text baked into images.
Sticky bottom CTA "Tell Us About My Clinic" appears after the visitor passes the hero; it must not
cover content.

## Technical
Optimise images, responsive sizes, lazy-load BELOW-fold photography only, NEVER lazy-load the
hero image. No layout shift. Form state must never reset. Every CTA works. Meaningful alt text.
High contrast. Semantic headings. Keyboard-accessible accordion. Clickable phone numbers.
Test 375px, tablet, 1440px. Preserve fast initial load. No new UI library.

## HARD CONTENT RULES
No placeholder testimonials, fake logos, fake projects, fake statistics, fake accreditations or
invented company claims. Use existing verified Medico assets only.
No em dashes anywhere in copy. No guarantee. No scarcity or deadline. Nothing about what another
builder charges or gets wrong. No promised response time.

## VERIFIED FACTS (source: medicoconstruction.com/contact, read 23 Sep 2026)
British Columbia: #202 15350 Croydon Dr, Surrey, BC V3Z 1H4 — 604-644-4120
Vancouver Island: #185 911 Yates St, Victoria, BC V8V 4Y9 — 778-403-4999
Edmonton: #38 314-222 Baseline Road, Sherwood Park, AB T8H 1S8 — 587-855-4455
Calgary: #301 14 St NW #309, Calgary, AB T2N 1Z7 — 825-425-0044
Every address, licence, price or date you write gets a `source:` line as you write it.

## THE CONVERSION PROGRESSION (every section serves one of these, in order)
1 You build medical clinics. 2 You have done this many times. 3 You understand healthcare-specific
complexity. 4 You can help wherever I am in the project. 5 You manage everything under one team.
6 I can see actual clinics you built. 7 You work in my area. 8 I get the design included if you
build it. 9 I will tell you about my project and talk to someone.

## DO NOT OVERDESIGN
Before modifying a section ask: does this increase clarity, credibility or conversion? If no,
do not add it. The page should feel expensive because of spacing, typography, photography,
hierarchy and restraint. Not because of effects.

# ===================== SECTION SPECS, VERBATIM FROM SANDY =====================

## HEADER
Minimal, this is paid search. Left: Medico logo. Right: "Licensed & Insured · BC & Alberta",
then optionally 604-644-4120, clickable on mobile. NO nav menu. Mobile: logo | call icon.

## SECTION 1 — HERO (two columns, left ~55%)
Eyebrow: MEDICAL CLINIC DESIGN + CONSTRUCTION | BC & ALBERTA
H1: Build your medical clinic with a team that specializes in healthcare.
Supporting: From site planning and permit drawings to construction and handover, Medico manages
your clinic under one team, so fewer details fall between the cracks.
Offer: Planning a clinic? Start with a no-cost site assessment. Design fees are $0 when Medico
builds your project.
Trust row: 100+ clinics built · Healthcare-focused team · Licensed & insured
Then clinic project imagery, a strong REAL project photo, ideally reception or a completed
healthcare environment. Imagery is not decorative.

## HERO RIGHT — THE FORM (strongest conversion component above the fold)
White background, thin border, subtle shadow, ~16px radius, generous internal spacing,
progress indicator. Top reads "Tell us about your clinic" and "Step 1 of 5" with a small bar.
Large selectable buttons/cards, whole row clickable, very obvious selected state, NO tiny radios.
After selecting, "Continue" appears. Do not auto-jump unless the animation is extremely smooth.

Q1 What are you planning?
  New clinic / Renovation / Expansion / Relocation / Still evaluating options
Q2 Where are you with the space?
  I already have a location / I'm negotiating a lease or purchase / I'm actively looking at spaces
  / I haven't started looking yet
Q3 What type of clinic are you building?
  Medical / Family Practice · Specialist Clinic · Dental · Physiotherapy / Rehabilitation ·
  Pharmacy · Diagnostic / Imaging · Wellness / Allied Health · Other
Q4 Approximately how large is the space?
  Under 1,500 sq. ft. / 1,500-3,000 sq. ft. / 3,000-5,000 sq. ft. / 5,000+ sq. ft. / I don't know yet
Q5 When would you ideally like to open?
  Within 3 months / 3-6 months / 6-12 months / 12+ months / Not sure yet
CONTACT STEP — "Where should we contact you about the project?"
  First name, Last name, Phone, Email, City. Optional: Project notes.
  CTA: Tell Us About My Clinic
  Microcopy: A Medico project specialist will review your details and contact you about the next
  step. No obligation.
  Do not promise instant quotes.
FORM UX: store all answers, Back must work and must not clear responses, subtle transitions,
show progress, fully keyboard accessible, inputs 48px min on mobile, correct mobile keyboards
for phone/email, INLINE validation not submit-time only.

## SECTION 2 — TRUST / REVIEWS
H2: Built for healthcare professionals across BC & Alberta
Sub: Clinic owners choose Medico because healthcare projects require more than ordinary
commercial construction.
Three testimonials, existing authentic ones only. Each: project image, review, name, clinic,
Google Review indicator. Compact and credible, NOT giant quotation cards.
Trust bar alongside or beneath: 100+ Clinics Built · Healthcare-Focused Design + Construction ·
CSA Z8000 Experience · BC + Alberta. Keep the Google 5.0 if currently valid. Never fabricate it.

## SECTION 3 — EXPERIENCE
H2: We don't learn healthcare construction on your project.
Copy: Medico has helped design and build more than 100 healthcare spaces across British Columbia
and Alberta. From exam rooms and reception areas to treatment spaces, imaging requirements,
plumbing, electrical, patient flow and permitting, healthcare spaces come with details ordinary
commercial builds don't.
Then the statistic 100+ / Healthcare spaces built.
The current giant dark 100+ section feels DISCONNECTED. Integrate photography and the statistic
elegantly: large 100+ type on the left with a project mosaic on the right, or full-width
photography under a restrained dark overlay. Do not make it excessively tall.

## SECTION 4 — PROJECT STAGE (three cards, equal height, stack on mobile)
H2: Wherever you are in the process, start here.
Card 1 "I've found a space." Before you commit to the build, we'll assess how the space works for
  your clinic and identify potential construction or design issues. CTA: Assess My Space
Card 2 "I'm negotiating a lease." Bring Medico in before you sign. We can help identify issues
  that could affect layout, construction cost or your opening timeline. CTA: Review My Space
Card 3 "I'm still planning." Tell us what you're trying to build. We'll help you understand the
  space, design and construction requirements before you move forward. CTA: Plan My Clinic
Each card gets a small illustrated document-style visual: location pin / floor plan, lease
document, blueprint. NOT generic feature cards. Every CTA returns to the form.

## SECTION 5 — WHY HEALTHCARE IS DIFFERENT
H2: A medical clinic isn't a standard commercial build.
Sub: Your layout has to work around patients, staff, equipment, building systems, accessibility
requirements and healthcare-specific standards, before construction begins.
Layout: LEFT a simplified clinic plan / blueprint. RIGHT five requirements:
  Room layouts built around your workflow and equipment
  Plumbing and electrical planned around treatment requirements
  Patient and staff circulation considered from the start
  Imaging and specialized-room requirements accounted for early
  Permit and construction documentation coordinated by the same team
Callout: Designed with healthcare requirements in mind, including applicable CSA Z8000
considerations.
Do NOT use CSA Z8000 as a random badge. Explain its relevance.

## SECTION 6 — PROCESS (horizontal timeline desktop, vertical mobile)
H2: One team from the first site visit to opening day.
01 Assess the space — We identify requirements, constraints and opportunities.
02 Plan your clinic — The layout is developed around workflow, equipment and patient experience.
03 Draw + permit — Architecture, engineering and permit documentation are coordinated.
04 Build — Medico manages trades, scheduling, construction and quality control.
05 Handover — Your clinic moves to the next stage of opening.
Under it: Instead of coordinating designers, engineers and contractors separately, you have one
team accountable for the project.

## SECTION 7 — PORTFOLIO (one of the most premium sections)
H2: See what we've built for clinic owners like you.
Sub: Healthcare spaces designed and built across BC & Alberta.
Masonry-like but orderly grid, ~6 projects, excellent photography prioritised. NO CAROUSEL.
Hover/overlay shows clinic name, city, category. Example: Babylon by TELUS Health / Victoria, BC /
Medical Clinic. Optional CTA: Discuss a Similar Project, scrolls to form.

## SECTION 8 — LOCATION
H2: Healthcare construction across BC & Alberta
Copy: Medico serves clinic owners across Metro Vancouver, Vancouver Island, Calgary, Edmonton and
surrounding communities.
Keep the map, restyle it to fit the page, not cartoon-like. Under it, office cards for Surrey,
Victoria, Calgary, Edmonton (addresses and phones in VERIFIED FACTS above).
Then: Not sure whether we work in your area? CTA: Tell Us Where You're Building

## SECTION 9 — FREE DESIGN OFFER (major conversion section, distinct background)
Should feel like a financial value proposition, almost a construction estimate sheet.
H2: Build with Medico and your design fees are $0.
Copy: When Medico is selected to build your clinic, the design work required to move the
construction project forward is handled as part of the project.
Visual table: SITE ASSESSMENT $0 / SPACE PLANNING $0 / CLINIC LAYOUT $0 /
CONSTRUCTION / PERMIT DESIGN $0
Then: $0 DESIGN FEES*  Badge: WHEN MEDICO BUILDS YOUR CLINIC
Avoid gimmicky coupon aesthetics. It should resemble architectural project documentation.
CTA: Start My Clinic Plan
Footnote: *Applies when Medico proceeds with the clinic construction project. Specific third-party
or municipal charges, where applicable, are separate.
Do not add exclusions beyond that.

## SECTION 10 — FAQ (clean accordion, large clickable rows)
H2: Questions clinic owners ask
Q How much does it cost to build a medical clinic?
A Clinic construction cost depends on the space, existing conditions, clinic type, equipment
  requirements, finishes and mechanical/electrical scope. Medico can assess the project before
  construction begins so you can better understand what will be involved.
Q How long does a clinic build take?
A Timelines vary by project size, permit requirements, existing conditions and scope. During
  planning, Medico identifies the major design, approval and construction milestones around your
  intended opening date.
Q Should I contact Medico before signing a lease?
A Yes. Bringing the construction team in early can help identify layout, electrical, plumbing,
  mechanical or permitting issues before you commit to a space.
Q Can you renovate a clinic that's still operating?
A Some projects can be phased to reduce disruption to operations. Medico will assess the project,
  access requirements and safety considerations to determine the appropriate approach.
Q Do you build medical clinics in Alberta?
A Yes. Medico works on healthcare projects in both British Columbia and Alberta.
Q Is the design really free?
A Yes. When Medico is selected to carry out the construction project, the design work required to
  move the clinic build forward is included.

## SECTION 11 — FINAL CTA
Do not use the current "Send us your space" approach.
H2: Planning a clinic? Start before construction starts.
Copy: Tell us about your space, timeline and clinic. A Medico project specialist will review the
project and contact you about the next step.
Small line: Takes about 60 seconds.
CTA: Tell Us About My Clinic
Secondary: Prefer to talk? Call 604-644-4120
Trust line: Healthcare-focused · BC + Alberta · Licensed & insured
