<!-- Public mirror of the LUV Lab training corpus (luv-lab.info).
     Published from the lab's internal repository @ 867e294 on 2026-08-26.
     Materials: CC BY 4.0 · Scripts: MIT (see repository README).
     Internal cross-references (roster, handbook, project analyses) may not resolve here. -->

# Module 5 — EEG session skills: running a participant to protocol

**Status: READY** — PI authorized 2026-08-12.

> 🛑 **Correction, 2026-08-07.** This module stated in six places — including **a graded
> exercise and its answer key** — that the pipeline's `reref: "average"` means the average of the
> two mastoid channels. **It does not**, and that has been corrected throughout (§8). **The lab's
> referencing is unchanged:** the data *are* mastoid-referenced, per the PI's 2026-08-05 ruling,
> which stands. Only the claim about what the config keyword denotes was wrong. **If you trained
> on the earlier version, read *Correction — 2026-08-07* in the appendix.**

> **Where this comes from.** The procedure in this module follows the **LUV Lab EEG Runbook,
> "Setup: Blue Booth – LiveAmp 8 + StimTrak + OpenSesame (Ubuntu)"**, supplied by the PI on
> **2026-08-05**. That runbook is **adapted from instructions used in the WRAP Lab, originally
> written by the WRAP Lab's runbook author (2023)** — it is not this lab's original work, and that credit
> travels with it. **The runbook itself is the operational authority** (it lives with the lab's
> SOPs, not in this repo). If the runbook and this module ever disagree, **believe the runbook**
> and tell the Lab Manager so this module gets fixed.
>
> Pipeline facts (filters, thresholds, config field names) come from
> **`knowledge/eeg-pipeline.md`**, the lab's canonical EEG digest. General EEG background — what
> an artifact looks like, why impedance matters — is **standard practice knowledge**, flagged as
> such where it appears, and is *not* a lab-documented claim.
>
> **Revision note:** the first draft of this module (2026-07-20) was written **before** anyone
> had the runbook. It guessed in places, and some guesses were wrong. See the appendix,
> *What changed on 2026-08-05*, if you read the old version.

---

## ⚠ `[confirm]` before your first session — **the lab has moved campuses**

The lab is now at **Iadarola Center 221 (IAD 221)**, Villanova University Cabrini Campus (610
King of Prussia Rd., Radnor, PA 19087); EEG recording runs in adjoining room **221A** (the Blue
Booth, shielded for EEG). **The runbook this module follows is undated** — the only date
attached to it is 2023, on the WRAP Lab original it was adapted from — and it describes the
physical setup at the **previous** location. After a cross-campus move, almost none of the spatial
detail is guaranteed to have survived; the one confirmed exception is named just below.

**Safe to learn here — the equipment travels with the lab:** the LiveAmp 8, StimTrak triggers,
OpenSesame 4, BrainVision Recorder, the impedance targets, cap sizing, the consent and safety
procedure, file naming, and all of the reasoning in this module.

**Confirmed to have survived the move — the booths themselves.** The lab still has
**sound-attenuated participant booths, and they are still referred to as Blue and Green**
(`RESEARCH_PROFILE.md`, "Space/equipment"; PI, 2026-08-05). So the runbook's Blue/Green vocabulary
is live, not historical — **do not treat the booth names as stale.** *(Narrowed 2026-08-07: this
paragraph previously left the booths' survival open, when the profile had already settled it.)*

**Answered 2026-08-20 (PI ruling): which booth is which.** The LUV Lab is **Iadarola 221**;
**Green is the booth in the main room (221)** and **Blue is adjoining room 221A, shielded for
EEG recording**. That corroborates the runbook's record-in-Blue setup — the shielded booth is
the recording booth. *(This closes C-01.1 only; the rest of C-01 still needs the walk.)*

**Unverified after the move — treat every one as `[confirm]`:** where the **LiveAmp charges**;
whether the Recorder
machine still sits on a **desk outside the booth**; whether the **electrode-mapping chart on the
whiteboard** and the **posted cleaning procedure** made the trip; the booth light and
door-left-open conventions; and where the supplies and the **Sharps container** now live.

**What to do:** walk the room with the **Lab Manager** before your first session and check the
layout against §2 and §3. **Do not assume the written sequence still matches the room**, and do
not let a step you cannot find quietly drop out of the session. Where the room and the module
disagree, the room wins — **say so**, so this module gets fixed rather than worked around.

*This module deliberately does not guess at the new arrangement.* It is also the lab's own norm
doing its job: check a document's date against what it describes. **This one carries no date at
all** — which is itself the finding.

---

**Purpose.** Prepare you to **run a research participant through an EEG session to protocol** in
the Blue Booth: consenting and caring for the participant, bringing up the two-machine rig,
fitting the cap and inserting electrodes safely, getting impedances to target, confirming
triggers, watching the live trace with an informed eye, and saving/logging the session so the
data is usable and auditable downstream.

This module is the **conceptual scaffold, the reasoning, and the checklists**. The **hands-on
capping and machine operation are learned in supervised practice** and signed off by the PI or a
designated experienced RA. **You do not run a real participant alone until that sign-off**
(Competence check, end of module).

**~Time to complete:** 3–4 hours reading + **≥ 2 supervised practice sessions** (observe, then
assist) before a solo run.

---

## 0. Prerequisites (hard gate)

- **Module 0 (data ethics, `data-ethics-for-ras.md`) passed** and the data-use agreement signed.
- **PI has confirmed IRB status in writing** for the study you will run, and you know which
  **approved consent form** version to use.
- **Raw EEG never enters this repo.** The `.vhdr/.vmrk/.eeg` files you create are identifiable
  research data; they live in approved storage (Module 0; `knowledge/eeg-pipeline.md`,
  *"Data privacy is load-bearing"*).
- **No codes, no logins, ever, in this repo.** Door codes, shared computer logins
  and NAS addresses live **only in the Lab Info Sheet** — ask the **Lab Manager**. Do not put
  them in a session log, a commit message, a README, or a Slack message that ends up pasted into
  a file.
- You have **read this module** and completed **≥ 1 observation** of an experienced operator.

---

## 1. Safety, consent, and comfort — the frame around every step below

The runbook's own General Guidelines lead with this, and so does this module:

- **The participant's comfort is the top priority.** Not the schedule, not the impedances, not
  the sample size. A participant who is uncomfortable, cold, anxious, or being rushed gives you
  worse data *and* is being treated badly. Both reasons are sufficient.
- **Always explain each step before you do it.** Especially anything they will feel: the tape
  measure, the wax pencil, the chin strap, the gel, and the needle tip.
- **Be efficient, but do not rush.** Arrive early — calm setup is better data. If setup
  consistently runs long, **tell the experiment lead**; that is information the lab needs, not a
  personal failing to hide.
- **Informed consent is completed before any prep.** In particular: **do not open the alcohol
  prep pads until the participant has consented.** Opening supplies signals that prep has already
  begun and quietly pressures someone who has not yet agreed. It also wastes a pad when someone
  declines — which they are entitled to do, at any point, with no penalty.
- **Confirm SONA credit** before running a credit subject (see §4). A participant who does the
  session and then cannot be granted credit has been wronged in a way you cannot undo afterward.
- **The needle tip is a real hazard step** (§5). Read that section before your first supervised
  prep, not during it.
- **Offer water and snacks during breaks.** Give real breaks (§9).

---

## 2. The rig: the hardware chain, end to end

> *The **connections** below are the equipment and travel with the lab. **Which room is which is
> now answered** (PI ruling, 2026-08-20; §0): **Blue = 221A, shielded for EEG recording; Green =
> the 221 main room.** What is still `[confirm]` is where "outside the booth" now is and where
> each piece of equipment sits — the pre-move layout, not the vocabulary or the booth identities.
> Confirm with the Lab Manager (see the location note above).*

Know what is connected to what. When something goes wrong mid-session, the fault is almost always
a link in this chain, and you will fix it much faster if you can picture the whole thing.

```
  BOOTH (Blue Booth)                          |   OUTSIDE THE BOOTH (desk)
  ------------------------------------------- | ------------------------------------
  Ubuntu booth PC  ── OpenSesame 4 ─┐          |
      │  audio out/in               │ stimulus |
      ▼                             │ trigger  |
  Scarlett Solo (red audio box)     │  cable   |
      ├── headphones                ▼          |
      └── Blue microphone       StimTrak       |
                                (AA batteries) |
                                    │ BNC OUT  |
                                    ▼          |
                          LiveAmp 8 "Trigger" input
                                    ▲
                       electrode pack ──> "EEG/ExG" input
                       (clipped to participant's shirt)
                                    │  wireless link
                                    └────────────────────► Windows laptop
                                                           BrainVision Recorder
                                                           (+ LiveAmp Console)
```

Facts to hold onto:

- **Two machines, two jobs.** The **Ubuntu booth PC** presents the experiment (**OpenSesame 4**);
  the **Windows laptop outside the booth** records the EEG (**BrainVision Recorder**). They are
  linked only by the trigger path. The subject number you type into OpenSesame and the filename
  you type into Recorder are **entered separately and must match** — nothing enforces it but you.
- **The StimTrak is the bridge.** Stimulus PC → StimTrak → **BNC OUT → LiveAmp AUX/Trigger
  input**. It runs on **AA batteries** and must be switched on. Dead batteries = no triggers =
  (see §8) a recording you cannot analyze.
- **The LiveAmp 8 charges in the Green Booth** and comes to the Blue Booth for the session. Power
  it on by holding the button ~5 s until the light turns blue; connect it in the **LiveAmp
  Console** that opens with Recorder (search, then connect — only one device should appear; its
  identifier is on the lab's mapping sheet).
- **The electrode pack plugs into "EEG/ExG"** (align the white arrows) and **clips to the
  participant's shirt** so its weight is not hanging off their head.
- **The StimTrak cord rests on the back of the chair.** Which is exactly why triggers can stop
  mid-session if it is bumped — see §8.
- **Audio runs through the Scarlett Solo** (the red box, normally left on) with a **Blue
  microphone**. Booth PC → Settings → Sound: output **Analog Output – Scarlett Solo USB**, input
  **Microphone – Blue Microphones**.
- **What the pipeline eventually eats is what Recorder writes:** BrainVision
  **`.vhdr` / `.vmrk` / `.eeg`** (`knowledge/eeg-pipeline.md`, *Interface*). The `.vmrk` file is
  where your triggers live. This is why §8 exists.

**`[confirm]` — not stated in the runbook, do not fill in from guesswork:** the **cap
manufacturer**; whether the acquisition montage is the **`standard_1020`** the pipeline config
assumes (`knowledge/eeg-pipeline.md:284`); and whether anything lands on an analog **`AUX`**
channel (the pipeline drops channels named `AUX`, `knowledge/eeg-pipeline.md:282`, while events
are read from markers). **Answered and off this list — electrodes in use: 8** as currently
configured, expandable to 16 or 32; the Cognitive Science Program owns the 16-channel expansion
hardware (PI, 2026-08-15/16; `RESEARCH_PROFILE.md`). *(Closed 2026-08-20, backlog C-05.)*

---

## 3. Before the participant arrives

> *Every location in this section is `[confirm]` after the campus move — which booth, which desk,
> where the charger and supplies live. The **actions** are right; **walk the room with the Lab
> Manager once** and you will know where each one now happens.*

**Booth environment**

- Turn on the **booth light** (small switch on the light).
- Confirm the **Scarlett audio box** is on (it usually is).

**Booth computer (Ubuntu)**

- Settings → Sound: confirm output **Scarlett Solo USB**, input **Blue Microphones**.
- **Unplug and re-plug the microphone and headphones**, and confirm audio is picked up and played
  back. *Why this odd step:* USB audio devices can be selected in Settings and still not be the
  device actually streaming. The re-plug forces the truth. Do it every time — a silent session is
  discovered by the participant, which is the worst way to discover it.
- Launch **OpenSesame 4** (the icon with the excited Einstein), open the **first experiment**
  (e.g. `1_Oddball_Baseline.osexp`). Run it (green play) and enter the subject number when you
  reach that point. **Note the subject number in the participant log.**

**Recorder computer (Windows laptop, on the desk outside the booth)**

- Log in **with your own Villanova account**. (Shared-account credentials, where any are needed,
  are in the **Info Sheet** — ask the **Lab Manager**. They are not written down here.)
- Open **BrainVision Recorder**.
- In **Monitor** (the eyeball, top left), **turn the Display filter OFF**; leave **baseline
  correction ON**.
  *Why this matters more than it looks:* a display filter makes a **cosmetically clean trace out
  of a dirty recording**. It smooths the picture, not the data. With it off, what you see is what
  is being written to disk — which is the whole point of watching the trace at all. A student who
  leaves the display filter on can watch a bad session go by looking fine.
- **Verify the electrode mapping.** Check that each physical channel is labelled correctly in
  Recorder (Fz, Cz, mastoids, etc.) against the **lab's mapping sheet**. **The cap's electrode
  numbers do not all match the channel names** — this is a documented trap, not a rumor. Use the
  chart; do not assume.

**Supplies laid out (table outside the booth)**

- Measuring tape
- Red wax pencil
- **Alcohol prep pads** (forehead + mastoids) — **do not open until consented**
- Syringes prefilled with gel (+ refill tube)
- **Needle tips** (and confirm the **Sharps container** is present and not full)
- Paper towels

**EEG system**

- **StimTrak:** insert AA batteries, switch on; stimulus PC → StimTrak; **BNC OUT → LiveAmp
  AUX/Trigger**.
- **LiveAmp 8:** unplug from the charger in the **Green Booth**; hold power until the light turns
  blue (~5 s); connect via the **LiveAmp Console**; plug the electrode pack into **EEG/ExG**
  (white arrows aligned) and the StimTrak cord into **Trigger**.
- **Log the LiveAmp battery state** in the participant log — a session that dies at minute 40 is
  a preventable loss, and the log is how the lab learns the battery is aging.

---

## 4. Consent and intake (people first)

The exact wording and order follow the **IRB-approved protocol** `[confirm — the approved consent
script is the authority, not this module]`. The shape is:

1. **Confirm the appointment and the participant's name against the schedule**, and — for credit
   subjects — **confirm the SONA credit email** *before* running. Credit that cannot be granted
   is a real harm to a student participant.
2. **Welcome** the participant. Unhurried, plain language, no jargon.
3. Walk through the **approved consent form**: purpose; what they will do; that EEG is
   **non-invasive — it records, it does not stimulate**; the gel and the cleanup afterward (they
   will want to know about their hair, and they are entitled to an honest answer); the mild
   scratch of electrode prep; time; compensation or credit; and their **right to stop at any
   time, with no penalty**.
4. **Answer questions.** Then obtain **signature/consent per protocol** — **before any prep,
   before any pad is opened, before the tape measure comes out.**
5. Collect **only** the protocol-specified intake information. Nothing extra, no matter how
   interesting. Identifiers stay out of this repo (Module 0).
6. **Reconfirm comfort throughout.** Consent is continuous, not a signature event.

**Respect > schedule.** A rushed or pressured consent is never acceptable, even when you are
behind, even when the participant seems eager, even when it is the last slot of the day.

---

## 5. Cap fitting and electrode insertion

*(Hands-on, learned in supervised practice. The concepts and the safety rules are here.)*

**Fit**

1. **Clip the electrode pack** to the participant's shirt or sweatshirt before you start, so the
   pack's weight never pulls on the electrodes.
2. **Measure head circumference** → choose cap size **54, 56, 58, or 60**. **When in doubt, round
   down.** *Why:* a slightly snug cap holds electrode contact; a loose cap lets electrodes sit
   off-position and lose contact as the participant moves, and no amount of gel fixes it. Snug is
   not the same as painful — check.
3. **Mark the cross with the red wax pencil:** the **nasion–inion midpoint** and the **ear-to-ear
   midpoint**. Where they cross is **Cz — electrode 24**. *Why measure at all:* every electrode
   position in the montage is defined relative to this point. Get Cz wrong and you have not
   misplaced one electrode, you have misplaced all of them, consistently, in a way no analysis
   can detect or undo.
4. **Clean the forehead and mastoids** with alcohol pads (now that consent is complete).
5. **Place the cap** with the Cz electrode over the Cz mark. Confirm **Fz centred on the
   forehead**, **mastoid electrodes correctly placed** (on the bone behind the ear, not on soft
   tissue or hair), **GND on the forehead**.
6. **Adjust the chin strap** and **confirm the participant is comfortable.** Ask, out loud, in
   words. "Is that too tight anywhere?" A participant who is enduring discomfort silently will
   move, tense up, and hand you EMG-laden data — and you will have made someone uncomfortable
   for an hour for nothing.

**Electrode insertion — the sharps step**

> **Read this before your first supervised prep.** Needle tips are **sharps**. They are used
> against another person's skin. Treat them accordingly.

- **Explain the gel and the needle tip to the participant first**: a mild scratch, not painful.
  Say it before they feel it, not after.
- **Use the chart on the whiteboard** for which electrode goes where — **the numbers do not all
  match** the channel names.
- **Start with GND.** Insert the electrode gently into its cap position; it should **click into
  place**.
- Put the **needle tip in the opening at the bottom of the electrode** and abrade with the tip
  **flat** — up/down, left/right, diagonal, circles — for **at least fifteen seconds**. Then
  **squirt in a small amount of gel**.
- **Next the reference (blue) electrode → #10, left mastoid**, behind the ear. Then **electrodes 1
  and 2** — at that point **check impedances** on the laptop; ideally all green already.
- **Continue, checking impedances as you go.** Re-gel/abrade anything above 10 kΩ (§6, §7).
- **Once all impedances are green, you can start.**
- **Discard the used needle tip into the Sharps container.** Not the trash, not a paper towel,
  not the table, not "for a second." The Sharps container.

**Hard safety lines:**

- **Never abrade to the point of breaking skin.** Abrasion is meant to remove dead surface skin
  cells, not to draw blood. If skin breaks or there is any blood: **stop, do not continue at that
  site, and get the Lab Manager or PI.** This is not a judgment call an RA makes alone.
- **If a participant says a site hurts, stop at that site.** Discomfort is a signal, and pushing
  through it is both a safety problem and a data problem.
- **One needle tip does not travel between participants.** `[confirm the lab's exact needle-tip
  reuse and disposal policy with the Lab Manager — the runbook states disposal into the Sharps
  container and does not address anything beyond that.]`
- **`[confirm]` whether gloves are required** for insertion and for cleanup. The runbook does not
  say. Ask; do not infer from what you saw someone else do.

---

## 6. Impedances — what the number actually means

**Targets (runbook):**

| Site | Target | In Recorder |
|---|---|---|
| Scalp electrodes | **< 10 kΩ** | set GOOD level 10 kΩ, BAD level 11 kΩ |
| **Mastoids and GND** | **< 5 kΩ** (if possible) | — |

**What you are measuring.** Impedance is the opposition to a tiny test current passing between
the electrode and the scalp through the gel bridge. It is a **proxy for the quality of the
electrical contact** — how well the dead-skin barrier has been bypassed and how continuous the
gel path is. It is not a measure of brain activity, and a green number does not mean the data is
good; it means one specific failure mode is absent.

**Why high impedance hurts** *(standard EEG background)*:

1. **Noise scales with source resistance.** A high-impedance contact is a small, resistive
   connection, and resistive connections generate more thermal noise.
2. **It breaks common-mode rejection — this is the big one.** The amplifier removes noise that is
   *common* to the signal and reference inputs (most of the ambient 60 Hz in the room is common).
   That cancellation depends on the two inputs seeing **similar** source impedances. Mismatched
   impedances convert common-mode noise into **differential** noise, which lands in your data and
   **cannot be filtered out afterward** — it looks like signal. This is why *balance* across
   channels matters, not just each number individually.
3. **It makes the channel movement-sensitive.** A marginal contact turns small head or cable
   movements into large voltage swings.

**Why mastoids and GND are held to a stricter 5 kΩ.** Because they are **in every channel's
signal path**. A bad scalp electrode costs you one channel. A bad **reference** or **ground**
contaminates **every channel at once** — you do not lose a channel, you lose the session. On a
montage this small you cannot afford to lose either.

**Reading the numbers like an experienced operator:**

- **All channels high together** → suspect the shared parts: ground, reference, cap not seated,
  pack not properly connected. Do not start re-gelling 8 sites.
- **One channel high, neighbours fine** → that site: hair in the way, too little gel, not enough
  abrasion, electrode not clicked in.
- **A channel that passes but is marginal** (say 9.5 kΩ against a 10 kΩ target) → **fix it now.**
  Impedances **drift upward** over a session as gel dries and the participant moves. Marginal at
  minute 0 is failing at minute 40, and at minute 40 you have to interrupt the task to fix it.
- **Two adjacent channels suddenly both very low and their traces look near-identical** →
  suspect a **gel bridge**: too much gel has spread between neighbouring sites and shorted them.
  The fix is **less gel**, not more — and it is worth catching, because bridged channels are not
  obviously wrong in the data, they are just quietly duplicated.
- **A channel with a strong 60 Hz ripple** → look at its impedance before you go hunting for the
  offending power supply. A single channel picking up mains hum is usually an impedance problem;
  all channels humming is usually an environmental one.

**Reduce 60 Hz at the source anyway:** keep phone chargers, power bricks and unnecessary
electronics away from the cap and leads, route power cables away from the participant, and see
§8 for asking the participant to hand over their phone. *(The lab records with a 60 Hz notch and
the pipeline applies one as well — `knowledge/eeg-pipeline.md:286` — but a notch removes the
frequency, not the underlying contact problem that let it in.)*

**Anything you cannot get down is a logged fact (§10), not a secret.** Modern amplifiers tolerate
higher impedances than older systems did; the lab's targets are still **the numbers you meet**,
not a number you argue your way out of. If you genuinely cannot reach them, log the channel and
the value and tell the Lab Manager — the analysis needs to know.

---

## 7. Re-gel, or re-fit? (the judgment call)

The checklist tells you to re-gel/abrade above 10 kΩ. It does not tell you when re-gelling is the
*wrong* answer — and re-gelling a mis-fitted cap is the single most common way a setup runs 40
minutes long.

**Re-gel / re-abrade that site when:**
- One or two channels are high and their neighbours are fine.
- The electrode is **clicked in** and sitting where the chart says it should.
- The impedance came down before and has **drifted up** during the session (gel drying).
- You can see hair under the electrode, or you know you gave that site a short abrade.

**Re-fit the cap when:**
- **Many channels are high at once**, or impedances are broadly poor despite good technique.
- **Cz is not on the wax cross**, Fz is off-centre, or the cap has rotated or ridden up.
- **Mastoid electrodes are not on the mastoid bone** (a very common cause of a stubborn
  reference).
- The size is visibly wrong — gaps between cap and scalp, or the participant reports pressure.
- **The reference or ground will not come down** despite proper prep. Fix the fit and the
  position before you keep working on the site.

**Stop and get help when:**
- You have abraded the same site **repeatedly** and it will not come down. Continuing risks the
  participant's skin, and skin comes before data. **Log it, move on, tell the Lab Manager.**
- Anything about the participant's comfort has changed.

*Rule of thumb: **impedance problems that cluster are fit problems; impedance problems that are
isolated are contact problems.** Re-gelling fixes contact. Only re-fitting fixes fit.*

---

## 8. Recording mode, referencing, and triggers

**Switch back to Recording Mode** once impedances are stable.

### Referencing — the lab's reference is settled (PI ruling, 2026-08-05); the config keyword is a separate question

- **Online, during acquisition:** set the **online reference in Recorder** as the study specifies.
  The runbook notes this is **commonly FCz**; if your study's settings differ, **follow the
  study** `[confirm per-study — ask before changing anything in Recorder]`.
- **Offline, during preprocessing:** the data are **re-referenced to the average of the two
  mastoid channels**, exactly as the runbook's referencing note describes. **PI ruling,
  2026-08-05.**

> ### ⚠ The config keyword is a **separate** question from the lab's referencing
>
> **The pipeline config field `reref: "average"` does *not* mean the mastoid pair.** In the
> pipeline source, `average` and `avg` map to MNE's **all-channel** average — every EEG channel
> in the montage. Mastoid referencing is a **different mode entirely**: `mastoids`, `mastoid`,
> `linked_mastoids`, `linked`, `tp9_tp10`, or `p9_p10`, which references **P9/P10 or TP9/TP10**
> and **raises an error** if neither pair is present. *(Verified in the pipeline source,
> `eeg_pipeline/io_brainvision.py`, the `reref_mode` branch, lines 63–84. Digested at
> `knowledge/eeg-pipeline.md:285` and `knowledge/eeg-acquisition.md`, "Re-referencing".)*
>
> **What that does and does not change.** It does **not** change anything about the lab's
> referencing. The data are re-referenced offline to the average of the two mastoid channels;
> the PI ruled that on 2026-08-05 and it stands, exactly as the bullet above says. What is wrong
> is only the claim about what the *keyword* denotes. Consequence: a LUV study config should name
> a **mastoid mode**, not `average`.
>
> **Which mode each study's config actually names is an open question** — tracked in
> `RESEARCH_PROFILE.md` ("Methods the lab actually uses", EEG bullet) as an analysis-side
> question, not a training one. It is **not** yours to answer at the chair, and it is not a
> prerequisite for anything in this module.
>
> **Nobody running a session edits pipeline settings.** If a config looks wrong to you — and here
> is a case where one genuinely might — that is a reason to **tell the Lab Manager or the PI**,
> not to change it.
>
> 🛑 **This module taught the opposite until 2026-08-07**, including in a graded exercise. If you
> trained on an earlier version, read *Correction — 2026-08-07* in the appendix.

**Why this is your problem at the chair, not just the analyst's:** the offline reference is
computed from the **two mastoid channels**, so those two electrodes are not ordinary channels —
they end up in **every** channel's signal after re-referencing. A noisy mastoid does not cost you
a mastoid; it costs you the whole montage. That is the same reason they carry the stricter
**< 5 kΩ** target (§6), and it is why "the mastoids are close enough" is never close enough.

**Ask the participant for their phone and any other electronics** before recording. Say why —
"phones and smartwatches put noise into the recording" — so it reads as protecting the science,
not confiscation. Put them somewhere the participant can see them.

**Recording settings** (runbook checklist): **500 Hz sampling, DC–100 Hz, 60 Hz notch.**
*Why acquire so broad when the pipeline band-passes to 0.1–30 Hz
(`knowledge/eeg-pipeline.md:287-288`)?* Because **you can always filter later, and never unfilter.**
Acquisition keeps everything the hardware can honestly give; analysis narrows to the frozen plan.

### Triggers: verify **during** the run, not after

**What a trigger is.** Each time OpenSesame presents a stimulus it fires a pulse through the
StimTrak into the LiveAmp, and Recorder writes an **event marker** into the `.vmrk` file. Those
markers are the **only record of when things happened on the EEG clock.** The pipeline's event
alignment matches them to the behavioural codes, and the analysis reads conditions off them —
`standard_codes`, `deviant_codes`, `behavioral_keep_codes`
(`knowledge/eeg-pipeline.md`, `events:` block).

**What happens without them.** You have a continuous voltage recording and no idea when a
stimulus occurred. The behavioural file gives you trial *order*, not EEG-clock *timing*, and the
two machines' clocks drift relative to each other, so there is no reliable way to reconstruct
millisecond timing after the fact. **ERPs are defined by their latency.** A session with no
markers is usually a session thrown away — the participant's hour, their credit, and your setup
time, all of it.

**Why "during", not "before" or "after":**

- **Before only** is not enough. Triggers can **stop mid-session**: StimTrak batteries die, the
  BNC cord resting on the back of the chair gets bumped, a connector works loose. A pre-run check
  cannot see any of that.
- **After** is too late by definition. Whatever you learn, the session is over.
- **During** costs seconds and is recoverable. Watch Recorder in the first minute of the task:
  are markers appearing **regularly, in time with stimulus presentation**? Then keep half an eye
  on it at every break. Catching it at minute 4 costs you four minutes. Catching it at minute 45
  costs you the participant.

**Also check that the markers are *right*, not merely present.** If every stimulus writes the
same code, or codes appear at the wrong rate for the design (an oddball has many standards and
few deviants), something is mismapped. Present-but-wrong markers are worse than absent ones,
because they survive to the analysis looking plausible. **Note anything odd in the log and tell
the Lab Manager — do not diagnose the mapping yourself mid-session.**

**Start the recording in Recorder:**

- **File naming: `S###.vhdr`** (e.g. `S103.vhdr`). Recorder writes the trio **`.vhdr` + `.eeg` +
  `.vmrk`** — all three matter; the `.vmrk` holds your triggers.
- **Save into the study's experiment folder — never the main directory. Never overwrite existing
  data.** *(The exact path is `[confirm]`: the runbook body gives a Windows path under the
  Recorder machine's Vision raw-data folder, while its quick checklist shows a different
  shared-drive style path. Ask the Lab Manager for the current path for your study, and put the
  answer in the log, not in your memory.)*
- **The subject number in Recorder and the subject ID in OpenSesame must match.** Nothing checks
  this for you. A mismatch silently breaks EEG↔behaviour alignment downstream.

---

## 9. Running the task — reading the live trace

Your in-session behaviour determines how much data survives the pipeline's cleaning. The pipeline
rejects epochs for **blinks (proxy threshold 75 µV)** and **voltage extremes (±150 µV)**, and if
blink rate is high (**> ~15 blinks/min**) it runs **ICA** correction
(`knowledge/eeg-pipeline.md`, `artifacts:` and `ica:` blocks). Every artifact you prevent at
source is data you keep.

**Brief the participant** (before the first block, and again after long breaks):
- Sit relaxed but still; **blink during breaks and between trials, not during stimuli**.
- **Unclench jaw, shoulders and forehead** — muscle tension is EMG noise.
- Breathe normally; minimise swallowing during critical windows.
- **Ask for a break whenever they need one.** Then honour it, immediately.

**Give real breaks. Offer water and snacks.** A tired participant blinks more, moves more, and
tenses more. Fatigue is a **data-quality problem**, not only a courtesy.

**Never coach responses.** Deliver instructions verbatim per protocol, and follow the run order
and timing exactly — improvising breaks the mapping between markers and conditions.

### Recognising artifacts on the live trace

*Standard EEG background — this is how these things generally look; your eye for the lab's own
rig is trained in supervised practice.*

| What you see | Usually is | First action |
|---|---|---|
| Large (often > 100 µV), smooth, rounded deflection ~200–400 ms, **biggest at frontal sites**, same polarity across them, at a plausible rate (~10–20/min at rest) | **Blink** | Remind the participant to blink between trials, not during stimuli. Frequent enough to matter? Give a break — blinks rise with fatigue. |
| **Step-like** shift that holds at a new level, **opposite polarity left vs. right frontal** | **Horizontal eye movement / saccade** | Re-anchor gaze: remind them to keep eyes on the fixation point. |
| **Fast, dense, high-frequency "fuzz"** riding on the trace, worst at the outermost/temporal sites, worse late in the session | **Muscle (EMG)** — clenched jaw, tense neck, holding the head stiffly, frowning | Say it kindly and concretely: "let your jaw hang loose, drop your shoulders." Offer a break. Check the chin strap is not the cause. |
| **Big irregular swings on ONE channel**, no time-locking, often starting exactly when the participant moved | **Loose or high-impedance electrode / cable** | Check that channel's impedance; re-gel (§7). Do not keep collecting an hour of it. |
| **Big swings on ALL channels at once** | **Gross movement**, or a **reference/ground** problem | Pause. Ask the participant to settle; if it persists, check ref/GND — a shared-path fault shows up everywhere. |
| **Perfectly regular sinusoidal ripple** at mains frequency | **60 Hz line noise** | One channel → impedance (§6). All channels → environment: move power supplies and cables away. |
| **Very slow wandering baseline** (< ~0.5 Hz) | **Sweat / drift** | Is the booth warm? Offer water, let them cool; check the electrode has not dried out. |
| **Regular sharp-ish deflection ~1 per second**, often on a mastoid or posterior channel, matching pulse rate | **Pulse / ECG artifact** — an electrode sitting over a vessel | Note it; a small reposition of that electrode at the next break usually fixes it. Do not mistake it for blinks — **~60/min is far too fast to be blinking.** |

**Watch Recorder, deliberately, not decoratively.** The runbook makes monitoring the live EEG for
blinks, movement and muscle noise a standing guideline. With the **display filter off** (§3),
what you see is what is being written. **Pause and fix rather than collecting an hour of
unusable data** — a two-minute interruption is cheaper than a lost participant, always.

**Note any issues in the participant log as they happen.** You will not remember at minute 50
which block the participant sneezed through.

---

## 10. Session logging (make the data auditable)

A session is not done until it is logged. Record in the **participant log** `[confirm the current
template and where it lives — the runbook refers to it throughout but does not specify a
template]`, at minimum:

- **De-identified participant ID / subject number** (never the name in this repo), date, operator,
  task/run, experiment file.
- **Impedance status at start** — and specifically any channel you could not get to target, with
  its value, and any channel that drifted during the session.
- **Trigger confirmation** — were markers appearing regularly during the run?
- **LiveAmp battery state** at start.
- **Any protocol deviation** — restarted block, skipped or extended break, technical glitch,
  participant discomfort, withdrawal. **Write it down even if it feels minor and even if it
  reflects on you.** Downstream QC and the methodologist need it; a deviation you hide becomes a
  mysterious outlier someone else spends a week chasing.
- **Notes for the next operator** — the electrode that fought you, the cap size that fit, a room
  quirk.

**What must never go in:** names, contact details, anything identifiable, and **no codes, shared
logins, or NAS addresses** (§0). If you are unsure whether a note is safe to commit, **ask before
writing it** (Module 0's when-unsure rule).

---

## 11. After the session

> *`[confirm]` after the move: where the chargers live, whether the **posted cleaning procedure**
> made the trip and where it is posted, and the booth light/door conventions. **Do not drop a step
> because you cannot find where it now happens — ask the Lab Manager.***

1. **Stop the recording. Confirm all three files saved — `.vhdr`, `.eeg`, `.vmrk`.** Missing
   `.vmrk` means missing triggers; missing `.eeg` means missing data. Check, do not assume.
2. **Copy the data files to the Shared Drive**, into the study's experiment folder — via a mapped
   network drive, or the lab NAS **web portal** (address in the Lab Info Sheet); if you see a
   certificate warning, **stop and ask the Lab Manager** — do not proceed past it. **Credentials are your own account /
   as specified in the Info Sheet — ask the Lab Manager. Do not record any address, code, or
   login in this repo.**
3. **Verify the copy before deleting the local copies.** *Verify* means: the files are present at
   the destination, all three, with plausible sizes — not "the copy dialog closed." **This is the
   single step in the whole session with no undo.** Everything else can be repeated; a deleted,
   never-copied recording is gone.
4. **Thank and debrief the participant** per protocol; handle **compensation or SONA credit**
   before they leave.
5. **Remove electrodes and cap; clean per the posted procedure**; hang to dry.
6. **Recharge the LiveAmp and StimTrak batteries** (LiveAmp goes back on the charger in the
   **Green Booth**).
7. **Restock** gel, syringes, towels, needle tips if low — and **check the Sharps container** is
   not full. Tell the Lab Manager if it is.
8. **Shut down:** log out of **both** computers, booth light **off**, **leave the booth door
   open.**
9. **Complete the log.**

**Raw EEG stays in approved storage. It never enters this repo** — only de-identified derivatives
do, and only through the pipeline (Module 6, `eeg-pipeline-run.md`).

---

## 12. `[confirm]` list (state of this module, 2026-08-20)

**Settled, recorded here so it is not re-raised:** **offline referencing — the average of the
two mastoid channels.** **PI ruling 2026-08-05**; see §8. That ruling is about **the lab's
data** and is unchanged.

**Settled the other way, and also not to be re-raised:** the pipeline's **`reref: "average"`
does *not* denote that pair** — it is MNE's all-channel average, and mastoid referencing is a
separate mode (§8; verified in `eeg_pipeline/io_brainvision.py:63-84`). *This module asserted the
opposite between 2026-08-05 and 2026-08-07 and graded students on it; corrected 2026-08-07
against the source. See the appendix.* **Which reref mode each study's config actually names**
is open, but it is an **analysis-side** question tracked in `RESEARCH_PROFILE.md` — it is not a
Module 5 item and does not block this module.

**`[confirm]` — invalidated by the campus move (see the location note at the top):**
- **Room and location detail** *(which booth is which: **answered 2026-08-20** — Blue = 221A,
  EEG-shielded; Green = 221 Main; see §0)*: where the LiveAmp charges, whether the
  Recorder machine sits outside the booth, whether the **whiteboard electrode-mapping chart** and
  the **posted cleaning procedure** made the trip, where supplies and the **Sharps container**
  live, and the booth light/door conventions. **The runbook is undated and describes the previous
  location.** Walk the room with the Lab Manager; the equipment chain itself is unaffected.

**`[confirm]` — not stated in the runbook, deliberately left blank:**
- Cap **manufacturer**.
- ~~**Number of electrodes in use** vs. the LiveAmp's 8 channels~~ — **answered (PI,
  2026-08-15/16):** 8 in use as currently configured, expandable to 16 or 32; the Cognitive
  Science Program owns the 16-channel expansion hardware (`RESEARCH_PROFILE.md`). *(Closed
  2026-08-20, backlog C-05.)*
- Whether the acquisition montage is the **`standard_1020`** the pipeline config assumes.
- Whether any signal lands on an analog **`AUX`** channel (pipeline drops `AUX`).
- **Exact save path** for Recorder files (the runbook gives two different ones).
- **Participant-log template and location.**
- **Gloves** for electrode insertion/cleanup; **needle-tip** policy beyond Sharps disposal.
- **Per-study deviations** from this runbook — each study may differ; ask before assuming.

*The pipeline values quoted in this module match the current digest, `knowledge/eeg-pipeline.md`,
synced to **v2.2.0** (2026-08-12). Treat the config numbers as current-as-digested, not as
eternal.*

---

## Exercises  *(synthetic scenarios — no real participant data)*

**Exercise 1 — Impedance go / no-go.** Targets: scalp **< 10 kΩ**, mastoids and GND **< 5 kΩ**.
Synthetic readout:

| Site | Impedance (kΩ) |
|---|---|
| GND (forehead) | 6.0 |
| Reference #10 (left mastoid) | 4.2 |
| Right mastoid | 7.5 |
| Fz | 8.0 |
| Cz (#24) | 9.5 |
| Electrode 1 | 14.0 |
| Electrode 2 | 3.0 |

(a) Which sites are **not** ready? (b) Which is the **most urgent**, and why is it more urgent
than the highest number in the table? (c) Which site **passes** but should still be re-gelled
before you start, and why?

**Exercise 2 — Triggers.** You are four minutes into the oddball. The trace looks clean, the
participant is responding, but Recorder has shown **no event markers since the run started**.
(a) Give three plausible causes, in the order you would check them. (b) What do you do now?
(c) Explain in one or two sentences why finding this at minute 4 is a fundamentally different
situation from finding it at minute 45 — and why "I'll check the markers when I stop the
recording" is not an acceptable habit.

**Exercise 3 — Read the trace.** For each, name the most likely artifact and give your first
action:
(a) Fast, dense high-frequency fuzz on the outermost channels, getting worse over the last ten
minutes of a long block.
(b) One channel showing large irregular swings and a strong 60 Hz ripple that the other channels
do not have.
(c) A regular, sharp-ish deflection about **once per second** on the right mastoid channel only.
(d) Large smooth ~300 ms deflections across all the frontal channels, about **15 times a minute**.

**Exercise 4 — Re-gel or re-fit?**
(a) Six of your channels are above 10 kΩ, GND is at 9 kΩ, and you notice the wax cross is about
two centimetres in front of the Cz electrode.
(b) One channel is at 13 kΩ, its neighbours are all under 6 kΩ, and the electrode is clicked in
at the position the chart specifies.
For each: what do you do, and what is the cost of getting it backwards?

**Exercise 5 — Spot the deviations.** A synthetic session log reads:

> "Ran S117. Laid out supplies and opened the alcohol pads while the participant was reading the
> consent form, to save time. Participant was a credit subject — figured I'd sort SONA out later.
> Skipped the audio re-plug check, the Scarlett was already on. Two channels above threshold at
> start (didn't note which). Participant asked for a break in block 3; I told them to push
> through. Never looked at whether triggers were logging. Saved as S117.vhdr in the main Vision
> directory. Copied to the shared drive and deleted the local copies. Left the booth door closed.
> Wrote the booth door code in the log so the next RA has it."

List every problem and, for each, what should have happened.

**Exercise 6 — Order of operations.** Put these in the correct order and mark the one hard line
that must not be crossed: (a) obtain consent signature, (b) fit the cap, (c) open the alcohol
prep pads, (d) welcome the participant and confirm the appointment/SONA credit, (e) explain the
right to withdraw, (f) answer questions, (g) mark the nasion–inion and ear-to-ear cross,
(h) ask the participant for their phone and electronics.

**Exercise 7 — What a config keyword actually denotes.** A newer RA is looking over a study's
pipeline config with you. They point at `reref: "average"` and say, confidently: *"That's the
average of the two mastoids — that's what we reference to, the PI ruled on it."*

(a) **Is the RA right about the keyword?** Say what `reref: "average"` actually does, and **name
where you checked** — not where you heard it.
(b) The lab's offline reference **is** the average of the two mastoid channels (PI ruling,
2026-08-05, and it stands). Your answer to (a) is also true. **Explain in one or two sentences
how both are true at once**, and say what a LUV study config should name instead.
(c) Now suppose you **cannot** check: you have no access to the pipeline source, and the Lab
Manager is unavailable until tomorrow. What do you say to the RA, what do you write down, and
what do you **not** do?
(d) **This module taught the RA's reading — and graded students on it — until 2026-08-07** (see
the appendix). State the general lesson in one sentence, and say **why a config field's name is
weak evidence** about what the code does.

*This exercise replaced an earlier one whose correct answer was the false claim. The point is no
longer "defend the settled answer" — it is **how you establish what a keyword means**, which is
stable no matter how the per-study question comes out.*

---

## Answer key

**Ex. 1.**
(a) **Not ready:** **GND (6.0** — must be < 5), **right mastoid (7.5** — must be < 5), **electrode
1 (14.0** — must be < 10). Fz, Cz, electrode 2 and the reference pass.
(b) **Most urgent: GND and the right mastoid**, even though **electrode 1 (14.0 kΩ)** is the
biggest number. Ground and reference/mastoid sites are **in every channel's signal path** — a bad
one degrades *all* channels and breaks the amplifier's common-mode rejection, so it costs you the
session rather than one channel. Electrode 1 is one channel's problem. *(A mastoid is doubly
expensive: the offline re-reference is the **average of the two mastoid channels** (§8), so a
noisy mastoid propagates into every channel a second time.)*
(c) **Cz (#24) at 9.5 kΩ.** It passes, but it is marginal, and impedances **drift upward** as gel
dries and the participant moves. Marginal at minute 0 is failing at minute 40 — and fixing it
then means interrupting the task.

**Ex. 2.**
(a) In order: **(1) StimTrak** — is it switched on, are the AA batteries alive? **(2) The BNC
cable** — StimTrak BNC OUT → LiveAmp **Trigger** input; the cord rests on the back of the chair
and is easy to knock loose. **(3) The stimulus PC → StimTrak connection**, and whether the
OpenSesame experiment is actually sending triggers.
(b) **Stop, fix, restart the run** (following the protocol's rules for restarts) rather than
continuing. Note it in the participant log. Do not "keep going and sort it out later."
(c) The markers are the **only record of stimulus timing on the EEG clock**; the behavioural file
gives order, not millisecond timing, and the two machines' clocks drift, so timing cannot be
reconstructed afterward — and **ERPs are defined by latency**. At minute 4 you lose four minutes;
at minute 45 you lose the whole session, the participant's hour, and their credit. Checking only
at the end cannot catch a **mid-session** failure either — batteries die and cords get bumped
partway through — which is why the check is **during**, repeatedly, not once.

**Ex. 3.**
(a) **Muscle (EMG)** — worsening late in a block points to fatigue and tension. Ask the
participant to unclench the jaw and drop the shoulders, check the chin strap, **offer a break**.
(b) **A loose or high-impedance electrode on that channel.** A single humming channel is an
impedance clue, not an environment clue. Check its impedance and re-gel/abrade that site.
(c) **Pulse / ECG artifact** — ~1/s matches heart rate, and mastoid sites sit near a vessel. Note
it and reposition that electrode slightly at the next break. **It is not blinking** — 60/min
would be several times a normal blink rate.
(d) **Blinks** — smooth, ~300 ms, frontal, and 15/min is a plausible blink rate. Remind the
participant to blink between trials rather than during stimuli; note that ~15 blinks/min is
exactly where the pipeline's ICA policy kicks in (`knowledge/eeg-pipeline.md`, `ica:`), so
reducing it at source is worth the reminder.

**Ex. 4.**
(a) **Re-fit.** Many channels bad at once **plus** Cz off the wax cross is a **fit** problem. If
Cz is displaced, every electrode is displaced. Re-gelling six sites would burn 20 minutes, risk
over-abrading the participant's skin, and leave the montage wrong anyway — and a uniformly
displaced montage is invisible in the data afterward.
(b) **Re-gel/re-abrade that one site.** Isolated high impedance with good neighbours and a
properly seated electrode is a **contact** problem: more abrasion through the opening, a little
more gel. *Cost of getting it backwards:* re-fitting the whole cap for one channel wastes the
participant's time and your setup slot for a problem fifteen seconds of abrasion would have
fixed. **Clustered = fit; isolated = contact.**

**Ex. 5.** Problems → what should have happened:
1. **Opened the alcohol pads before consent was complete** → open nothing until consent is
   finished; opening supplies pressures someone who has not yet agreed and wastes supplies if
   they decline.
2. **Did not confirm SONA credit before running a credit subject** → confirm the credit email
   **first**; credit that cannot be granted afterward is a harm you cannot undo.
3. **Skipped the audio re-plug check** → do it every session; a device can be selected in
   Settings and still not be streaming, and the participant is the one who discovers it.
4. **Two channels above threshold, not identified** → bring them to target; if any will not come
   down, **log which channel and what value**.
5. **Denied a requested break** → give the break, always. Comfort is the top priority and fatigue
   wrecks data.
6. **Never checked triggers** → confirm markers are logging regularly **during** the run; a
   marker-less session is usually unsalvageable.
7. **Saved in the main directory** → save into the **study's experiment folder**, never the main
   directory, never overwriting existing data.
8. **Deleted local copies without verifying the shared-drive copy** → **verify first** (all three
   files present at the destination). This is the one step with no undo.
9. **Left the booth door closed** → leave the booth door **open** at the end.
10. **Wrote the door code in the log** → **never.** Codes, shared logins and NAS addresses live
    only in the Info Sheet; ask the Lab Manager. Remove it and tell the Lab Manager it was
    written down.
11. *(Also missing:* LiveAmp battery state, cap size, and any note for the next operator.*)*

**Ex. 6.** **d → f → e → a → c → g → b → h.**
Welcome and confirm appointment/SONA (d) → answer questions (f) → explain the right to withdraw
(e) → obtain signature (a) → **only now** open the alcohol pads (c) → mark the nasion–inion and
ear-to-ear cross (g) → fit the cap (b) → ask for phone and electronics before recording (h).
**The hard line: consent is complete before anything is opened, measured, or touched** — (a)
before (c). *(Right-to-withdraw is part of explaining consent, and remains true throughout the
session, not just at signing.)*

**Ex. 7.**
(a) **No.** `reref: "average"` — and its alias `avg` — is MNE's **all-channel** average: the
reference is the mean across every EEG channel in the montage. Mastoid referencing is a
**separate mode** (`mastoids`, `mastoid`, `linked_mastoids`, `linked`, `tp9_tp10`, `p9_p10`),
which references **P9/P10 or TP9/TP10** and **raises an error** if neither pair is present.
**Where to have checked:** the pipeline source, `eeg_pipeline/io_brainvision.py`, the
`reref_mode` branch (lines 63–84) — or, digested, `knowledge/eeg-pipeline.md:285` and
`knowledge/eeg-acquisition.md`, *"Re-referencing"*. Naming the source is half the answer. "I read
it in the training module" is exactly how the wrong version of this spread.
(b) They are **two different claims**: what the lab's *data* are referenced to, and what a
*keyword in a config file* denotes. The PI's 2026-08-05 ruling settled the first — mastoid
average — and nothing about it has changed. It never spoke to the second. **What a LUV study
config should name is a mastoid mode** (`mastoids` / `tp9_tp10` / `p9_p10`), not `average`. If a
study's config says `average`, then that config and the lab's stated referencing disagree — which
is something to **report**, not something to fix.
(c) Say **what you actually know and no more**: "the field is spelled `average`; I don't know
what the pipeline does with it; someone should check before either of us relies on a reading."
Write it in the log or a note to the Lab Manager. **Do not** edit the config — nobody at the
chair edits pipeline settings. **Do not** settle it by which reading sounds more sensible for a
small montage; plausibility is not evidence. And **do not** pass your guess to the RA in a
confident voice — an unsourced answer from someone senior is how this became a graded exercise.
Leaving it open overnight costs nothing. Guessing cost this module two days of teaching a
falsehood.
(d) **A config keyword's plain-English reading is not its behaviour; you settle it by reading the
source or asking someone who has — not by inferring.** Why the name is weak evidence: field names
are chosen for the general case by people who did not have this lab in mind; the same word
("average") names genuinely different operations in different tools; a name says nothing about
the **error branch** (that the mastoid mode *raises* when the channels are missing is behaviour
with no name at all); and a name that matches something true about your lab is the most dangerous
kind, because it confirms what you already believe. **How this one actually happened:** a correct
ruling about the lab's data was over-read into a claim about a keyword, written down, repeated in
five places, and graded — and every step was a reasonable-sounding inference. None of them was a
check. *(For the mastoid-prep connection, which is unaffected: see §8 and Ex. 1(b) — the offline
reference is built from those two channels, so they enter every channel's data, which is why they
carry the stricter **< 5 kΩ** target.)*

---

## Competence check *(PI-verifiable — supervised sign-off)*

Because this is a hands-on, participant-facing skill, the check is a **supervised sign-off**, not
a written quiz alone.

**Written:** the RA passes the exercises above — including **Ex. 7**, which tests whether they can
establish what a config keyword actually does (by source, not by inference), hold apart the lab's
referencing from the keyword that names it, and say "I don't know yet" instead of guessing.

**Supervised, on a practice/pilot volunteer, the RA runs a full session to protocol:**

- **Consent and care:** appointment and SONA credit confirmed **before** running; consent
  completed **before any supply is opened**; every step explained before it is done; comfort
  checked out loud after the chin strap; breaks offered and honoured.
- **Rig:** booth audio verified with the re-plug check; OpenSesame experiment loaded; Recorder up
  with the **display filter off** and baseline correction on; **electrode mapping verified against
  the mapping sheet**; StimTrak on and connected to the LiveAmp Trigger input; LiveAmp battery
  logged.
- **Cap:** size chosen from head circumference with the **round-down** rule; nasion–inion and
  ear-to-ear cross marked; **Cz (#24) on the cross**; mastoids and GND correctly placed.
- **Safety:** needle tip used flat and gently, ≥ 15 s per site, **disposed into the Sharps
  container**; the RA can state the stop conditions (broken skin, blood, participant pain) and
  who to get.
- **Impedances:** **scalp < 10 kΩ, mastoids and GND < 5 kΩ**; the RA can **explain why the
  mastoid/GND threshold is stricter** (shared signal path, common-mode rejection) — not just
  recite it.
- **Triggers:** confirmed **logging during the run**, re-checked at a break; the RA can say what a
  marker-less session costs and why.
- **Live trace:** the RA correctly identifies **at least two** artifact types in real time and
  takes the right first action.
- **Data handling:** `S###.vhdr` into the **study's experiment folder** (not the main directory);
  all three files confirmed; copied to the shared drive and **verified before local copies are
  deleted**; batteries back on charge; both computers logged out; booth light off, **door left
  open**.
- **Log:** complete and **de-identified** — impedances, deviations, trigger status, battery — and
  **containing no codes or logins**.
- **Referencing:** the RA can say that the offline reference is the **average of the two mastoid
  channels** (PI ruling 2026-08-05), that this is why the mastoids carry the stricter target, and
  that **nobody at the chair edits pipeline settings** — questions go to the Lab Manager or PI.
  They can also say that the pipeline's **`reref: "average"` is *not* that** — it is the
  all-channel average, so a LUV config should name a mastoid mode — **and name where they would
  check it.** *(Graded on the distinction and the sourcing, not on recalling the mode list. An RA
  who says "I'd have to look at the source" has passed this item.)*

**The PI (or a designated experienced RA) signs off** on safety, participant handling, and data
quality. **Only after sign-off may the RA run a participant solo.** This sign-off is a
PI-essential check (see `career-task-rotation.md`) — it is **not delegable to an untrained peer.**

---

## Appendix — corrections to this module

### Correction — 2026-08-21: §11 published the NAS address and taught past a certificate warning

**Found during a pre-publication release review (2026-08-21); wrong internally, not just for
the release.** §11 step 2 named the NAS web-portal hostname in this module — violating
this module's own §0 rule ("no codes, no logins, ever, in this repo; NAS addresses live only in
the Lab Info Sheet") and the lab-wide norm — and told students that on seeing a TLS certificate
warning they should *proceed past it to the login screen*. That instruction was wrong on its own
terms: a certificate warning on a credential portal is exactly the situation in which you
**stop and ask the Lab Manager**, because clicking through is how credentials get phished. The
step now routes the address to the Info Sheet and says stop-and-ask. If you trained on the
earlier text: do not click through certificate warnings anywhere in the lab's tooling.

### 🛑 Correction — 2026-08-07: this module taught, and graded, a claim that was false

**If you trained on this module between 2026-08-05 and 2026-08-07, you were told something
untrue, and Exercise 7 marked you on it. Please read this paragraph.**

| What the module said | What is actually true |
|---|---|
| The pipeline config field **`reref: "average"` denotes the average of the two mastoid channels** — asserted in §8, §12, Exercise 7, the Ex. 7 answer key, and this appendix, and presented as following from the PI's ruling | **It does not.** `average`/`avg` map to MNE's **all-channel** average. Mastoid referencing is a **separate mode** — `mastoids`, `mastoid`, `linked_mastoids`, `linked`, `tp9_tp10`, `p9_p10` — which references **P9/P10 or TP9/TP10** and **raises an error** if neither pair is present. Verified in the pipeline source, `eeg_pipeline/io_brainvision.py`, lines 63–84. |

**What did *not* change, and this is the important half.** The lab's data **are** re-referenced
offline to the average of the two mastoid channels. The PI ruled that on **2026-08-05** and the
ruling **stands, unaltered**. Nothing about the lab's referencing is in doubt, and nothing you
learned about *why the mastoids get the stricter < 5 kΩ target* was affected — that reasoning was
correct then and is correct now.

**What went wrong was narrower than it looks.** A correct ruling about **the lab's data** was
over-read into a claim about **what a keyword in a config file denotes** — two different kinds of
fact. The error was written into `knowledge/` on 2026-08-05, propagated into this module, and
retracted in `knowledge/` shortly after; but it had already reached the module, so it kept being
taught after it had been withdrawn upstream. **Consequence for practice:** a LUV study config
should name a **mastoid mode**, not `average`. Which mode each study actually names is open and
is an analysis-side question, tracked in `RESEARCH_PROFILE.md` — not a Module 5 item.

**Why Exercise 7 was rebuilt rather than patched.** Its correct answer *was* the false claim, so
there was no word to substitute. The replacement teaches the lesson this incident actually
carries: **a config keyword's plain-English reading is not its behaviour, and you settle what it
does by reading the source or asking someone who has — not by inferring from the name, however
sensible the inference sounds.** That lesson is stable against the source, not against the state
of a debate — which matters here, because an earlier version of this module had already been
revised in the other direction once.

*Recorded rather than quietly fixed, because students were graded on it. If you have a marked
Ex. 7 from before 2026-08-07, it does not count against you — tell the Lab Manager.*

---

### What changed on 2026-08-05 (diff against the 2026-07-20 draft)

The first draft was written **without the runbook**. If you read it, these are the corrections:

> **A note on how the left column quotes the old draft (2026-08-07).** Where the old draft carried
> a confirm-marker, this table used to reproduce it in its live bracket form. Every such marker in
> this table is **closed** — the right-hand column *is* the answer — so they are now written in
> ⟨angle brackets⟩ instead. Nothing about the history is lost; they simply no longer read as open
> markers to a reader or a search, which was inflating every count of this module's open items.

| The old draft said | Reality (EEG Runbook, 2026-08-05) |
|---|---|
| "amplifier, cap system, electrode count, electrolyte (gel vs. saline), impedance threshold" are all unknown | **LiveAmp 8 + StimTrak + BrainVision Recorder + OpenSesame 4**; **gel** (prefilled syringes) with **needle-tip abrasion**; **scalp < 10 kΩ, mastoids/GND < 5 kΩ**. Cap **sizes** 54/56/58/60. Only the cap manufacturer remains `[confirm]` (electrode count answered 2026-08-15/16: 8 in use, expandable to 16/32 — `RESEARCH_PROFILE.md`). |
| "Confirm the montage is the lab standard, `standard_1020`" *(in the acquisition software)* | That is the **pipeline's** config default (`knowledge/eeg-pipeline.md:284`), not an acquisition step. The real Recorder step is **verifying electrode mapping against the lab's mapping sheet** — and the cap's **numbers do not all match** the channel names. Whether acquisition is `standard_1020` is **`[confirm]`**. |
| "the pipeline later re-references to an **average reference**" — with no statement of what "average" covers | Named explicitly now: the lab's offline reference is the **average of the two mastoid channels** (**PI ruling 2026-08-05**, §8). The old phrasing was **silently ambiguous** — it never mentioned the mastoids at all, which is precisely the fact that makes the < 5 kΩ target matter. ⚠ **This row itself was wrong from 2026-08-05 to 2026-08-07**: it went on to claim the pipeline's `reref: "average"` denotes that pair. It does not. See *Correction — 2026-08-07* above. |
| **`Fp1`** must be clean because it is the blink proxy — built into two exercises, the answer key, **and the competence check** | `blink_proxy_chs: ["Fp1"]` is a **pipeline config default** (`knowledge/eeg-pipeline.md:281`). The runbook **never mentions Fp1**; it names Fz, Cz (#24), the mastoids, GND, electrodes 1, 2 and 10. **Whether Fp1 exists in the montage as fitted is `[confirm]`.** The old module made a pipeline setting into a physical fact and then graded students on it. |
| "~1–2/second frontal deflections are most likely **blinks**" | **1–2/s is 60–120/min** — several times a normal blink rate, and far above the ~15/min that triggers the pipeline's ICA. That pattern reads as **pulse/ECG artifact** or a loose electrode. The old answer key contradicted the pipeline number it cited two paragraphs earlier. |
| "Boot the acquisition system and open the study's acquisition configuration ⟨confirm amplifier/software⟩" — **closed** | **Two machines:** Ubuntu booth PC (OpenSesame 4) inside; Windows laptop (Recorder) outside; StimTrak between; **Scarlett Solo + Blue mic** for audio; **LiveAmp charges in the Green Booth**. |
| "⟨confirm⟩ the lab's trigger path" and "do a quick test trigger if the setup allows" — **closed** | Path is **OpenSesame → StimTrak (AA batteries) → BNC OUT → LiveAmp AUX/Trigger**. The runbook's verification is **confirming markers are logged regularly in Recorder *during* the run** — a pre-run test trigger is **not** in the runbook. |
| "Watch the live trace **if the setup shows one**" | You **always** watch Recorder; monitoring for blinks, movement and muscle noise is a standing guideline. Also new: **turn the display filter OFF** so the trace tells the truth. |
| Generic "clean/gently abrade the scalp as the lab specifies" | **Needle tips**, flat, ≥ 15 s per site, then gel; **Sharps container** disposal. The old draft contained **no sharps or skin-safety content at all** — the most serious omission in it. |
| "Confirm the recording saved with the right **filename/BIDS fields**" | **`S###.vhdr`** (plus `.eeg` and `.vmrk`) into the **study's experiment folder, not the main directory**. **BIDS conversion happens later, in the pipeline** — the operator does not set BIDS fields at save time. |
| "Confirm it saved in approved storage" | **Copy to the shared drive and *verify* before deleting local copies** — the one irreversible step in the session. |
| Nothing about SONA, participant electronics, cap sizing, the wax-pencil cross, chin-strap comfort, the electrode pack clip, water/snacks, battery recharge, booth shutdown, or the participant log | All present now, from the runbook. |
| Nothing about the runbook's provenance | Credited: **adapted from WRAP Lab instructions, originally written by the WRAP Lab's runbook author (2023).** |

**Accurate in the old draft and kept:** consent before prep; comfort over schedule; the pipeline's
artifact numbers (75 µV blink proxy, ±150 µV, > ~15 blinks/min → ICA); 60 Hz notch and source
control; "log every deviation"; raw data never in this repo; and the supervised-sign-off shape of
the competence check.
