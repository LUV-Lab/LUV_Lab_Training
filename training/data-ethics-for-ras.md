<!-- Public mirror of the LUV Lab training corpus (luv-lab.info).
     Published from the lab's internal repository @ 867e294 on 2026-08-26.
     Materials: CC BY 4.0 · Scripts: MIT (see repository README).
     Internal cross-references (roster, handbook, project analyses) may not resolve here. -->

# Module 0 — Data ethics & privacy for RAs  *(PREREQUISITE)*

---

## Start here — CITI training, in 60 seconds

**Most LUV Lab undergraduates have already completed the CITI training this lab requires.**
If you took **PSY 2050** and completed **Core Lab 2: Research Ethics & CITI Training**, you
did it there — and Core Lab 2 treats that certification as **valid for three years**. You do
not redo it.

**→ You have current CITI certification (completed within the last three years).**
You are compliant. Two steps and you are done with this part:

1. **Send your CITI Completion Reports (PDF) to the Lab Manager or the PI.** Download them any
   time from CITI's **My Records** tab. Include the completion dates so currency can be tracked.
2. **Ask the Lab Manager or the PI about CAYUSE** (Villanova's IRB system). Enrollment follows
   CITI completion — provide requested information promptly.

Then keep reading from §1. CITI is the *university's* requirement; §§1–7 below are the
*lab's* data rules. They are different things and both apply.

**→ You do not have it, it is older than three years, or you are unsure.**
**§8** has the exact path — registration, the course selections, the modules, what to send.
Budget **2.5–4 hours**, and start it in week 1: **completed CITI is the gate on LabArchives
edit access, CAYUSE, NAS/GPU accounts, and booth scheduling** (§8.5).

---

**Purpose.** Before you touch any human-subjects data — recorded speech *or* EEG — you
must know (1) what counts as participant data and why it is identifiable, (2) what may and
may not enter this repository, (3) why an IRB "exempt" determination does **not** make a
study ethics-exempt, (4) exactly what to do when you are unsure, and (5) the university
training (CITI) that gates every lab resource — and whether you already have it. This is a
**hard prerequisite for every human-subjects work package in the lab.** No data access is
granted until you pass the competence check at the bottom.

**~Time to complete:** 2–3 hours for this module, front-loaded into week 1. Read the module,
do the five exercises, check yourself against the key, then take the PI's short quiz and sign
the data-use agreement. **CITI is separate and additional (§8): ~2.5–4 hours — but only if you
have not already done it,** and most students here have.

**What this module puts into practice.** The lab's standing privacy rules: anonymization is
load-bearing, and identifiable participant material never enters the lab's code repository.
§§1–7 are those rules; §8 is the university's separate training requirement.

---

## 1. What counts as human-subjects data (and why it is identifiable)

**Recorded speech is identifiable in several ways at once:**
- The **voice itself** is biometric — a recording can identify a speaker.
- The **content** names people, places, employers, schools, dates, and events.
- In a **small or tight-knit community**, even "de-identified" details can re-identify
  someone by triangulation (the only person who worked at X and moved in year Y).

**EEG is identifiable too — this surprises people.** A raw EEG recording is not "just
squiggles":
- It is tied to a specific **participant ID, session date/time, and demographics**, and it
  travels with behavioral logs and scheduling information.
- Raw EEG files and their **BIDS `sourcedata/`** are treated as identifiable by the lab and
  **never enter this repo** (`knowledge/eeg-pipeline.md`).
- The **linking file** that maps a participant ID to a real name is the single most
  sensitive artifact in any study. It lives only in approved storage, never here.

Take-home: "identifiable" is broader than "has a name attached." When in doubt, treat it as
identifiable.

---

## 2. The golden rule: what may and may not enter this repo

This repository holds **code, de-identified derivatives, and summaries — nothing else.**

**NEVER commit, paste, upload, or email into this repo:**
- Raw audio (`.wav`, `.mp3`) or video.
- Un-anonymized transcripts.
- Raw EEG: BrainVision (`.vhdr` / `.vmrk` / `.eeg`) or EEGLAB (`.set` / `.fdt`), and BIDS
  `sourcedata/`.
- The participant **key / linking file** (ID ↔ name), consent forms, or signed documents.
- Identifiable metadata: names, dates of birth, addresses, contact info, photos, or
  scheduling that names participants.

**MAY live in the repo (de-identified only):**
- De-identified measurement tables (e.g., formant tables) with no identifiers.
- The EEG pipeline's **group-level derivatives**: `desc-summary_qc.tsv`,
  `desc-erp_metrics.tsv`, `desc-tfr_metrics.tsv`, `desc-erp_timeseries.parquet`, a
  **de-identified grand-average `.fif`**, and figures (per `knowledge/eeg-pipeline.md`).
- The study `config.yaml` (a de-identified text file — safe to commit).
- Analysis code and READMEs.

Anything **upstream of the committable derivatives** — raw files, per-subject data still
tied to one person, the linking key — stays in the PI's approved external storage. If you
cannot tell which side of the line a file is on, it goes in the "ask first" pile
(Section 5).

---

## 3. Raw vs. de-identified vs. anonymized — telling them apart

- **Raw** — as collected, fully identifiable (the `.wav`, the `.vhdr`, the signed consent).
- **De-identified** — direct identifiers removed/replaced so the working file no longer
  names the person (a formant table keyed to `sub-07`; a QC table). A separate key still
  exists elsewhere, so de-identified data is **not anonymous** — re-identification is
  possible for whoever holds the key. This is what you normally work with.
- **Anonymized** — no key exists anywhere; re-identification is impossible even in
  principle. Genuinely anonymized data is rarer than people assume.

You almost always handle **de-identified derivatives.** Treat them with care anyway: the key
exists, and small-community context can re-identify.

---

## 4. IRB-exempt ≠ ethics-exempt

An IRB **"exempt"** determination is a *regulatory* category — it means a study's risk
profile lets it skip continuing IRB review. It is **not** a waiver of ethics. An exempt
study still requires, as applicable: appropriate **consent/assent**, **confidentiality and
secure storage**, **de-identification**, honoring a participant's right to **withdraw**, and
every privacy rule in this module. "Exempt" changes the paperwork, not your obligations.

Two rules follow, and they are absolute:
1. **You never decide scope or exemption status.** Whether a study is exempt, approved, or
   pending — and what that permits — is the PI's call, confirmed in writing.
2. **No data contact until the PI confirms IRB status** for *your* study, in writing, and
   your data-use agreement is signed. This applies to de-identified derivatives too.

---

## 5. Your role, and the one rule that covers everything you forget

Your job with data is **check status, then handle with care** — not interpret, not decide.

Before touching data, all four must be true:
- You have **passed this module** and signed the **data-use agreement**.
- The PI has **confirmed IRB status in writing** for your study.
- You are accessing **only** the de-identified derivatives you were explicitly granted.
- **Your current CITI completion reports are on file with the Lab Manager** (§8) — required
  if you will participate in data collection, and the gate on LabArchives edit access,
  CAYUSE, NAS/GPU accounts, and booth scheduling.

CITI and this module are **not substitutes for each other**, in either direction: CITI is the
university's training requirement, §§1–7 are the lab's data rules. And holding CITI
certification **authorizes nothing by itself** — it opens the door to resources; the PI's IRB
confirmation and data-access grant are what let you use them.

**The rule that covers every case you didn't anticipate: when unsure, STOP and ask the PI
*before* you act** — before writing a file, before moving or copying data, before emailing
or pasting anything, before committing. An honest "I wasn't sure, so I stopped and asked" is
exactly right and never counts against you. Guessing with participant data is the mistake.

---

## 6. Confidentiality (participants, students, referee materials)

- **Participants:** do not discuss identifiable details outside the study team. Remember the
  small-community re-identification risk even for "de-identified" facts.
- **Student & personnel records and recommendation-letter material** live **only** in
  gitignored `people/confidential/` paths — never in tracked files. If you ever have reason
  to place something there, verify it is ignored first: `git check-ignore <path>` must print
  the path.
- **Manuscripts the PI is refereeing** are confidential and live only in gitignored
  `inbox/`/`confidential/` paths, deleted when done. Not RA-facing, but know the boundary.

---

## 7. Practical do / don't (the day-to-day)

- **Do** keep raw data in approved lab storage; **don't** copy it to a personal laptop,
  personal cloud (Gmail/Drive/Dropbox), or a USB stick.
- **Don't** email or Slack raw recordings, transcripts, EEG files, or the linking key —
  even "just to yourself."
- **Don't** screenshot identifiable data into chats, slides, or issue trackers.
- **Do** double-check a folder before committing: if you see a `.wav`, `.vhdr`, a real name,
  or a `sourcedata/` directory, stop and ask.
- **Do** ask the Lab Manager or PI when a file's status is unclear. That is the job working
  as intended.

---

## 8. CITI training — the university requirement, and what it unlocks

Sections 1–7 are the **lab's** rules. This section is the **university's** requirement. Both
apply, neither replaces the other. **If you already have current CITI certification, you have
met this section** — see "Start here" at the top, send your certificates, and read on only if
you want to know what your certification covers and why.

**Villanova's Office of Research Protections is the live authority on what training is
required.** If its current list and this section ever disagree, follow the ORP list — it is
linked, with its full address, in §8.2.

### 8.1 Who needs what — the Villanova role matrix

For a **Graduate or Undergraduate Research Assistant** — the role essentially every reader of
this module holds — the Villanova training matrix reads:

| Training | Requirement for a Graduate or Undergraduate Research Assistant |
|---|---|
| **Responsible Conduct of Research** | **Required** |
| **Human Subjects Research** | Required **if named on a Human Subjects research protocol** |
| **Conflicts of Interest** | **Dependent on project role** |
| **Research Security** | **May be required for sponsored research, depending on project role** |
| **Safe Research Environments** | Required for **NSF research with an off-campus component** — **not triggered here**; see the note below |
| **Animal Research** | Required **only if named on such a protocol** — **not applicable** to this lab's work |
| **Research with Biohazards** | Required **only if named on such a protocol** — **not applicable** to this lab's work |

That table is the **university's** minimum, transcribed as supplied. The lab asks for more:

> ### The LUV Lab requires two extra courses of **every** RA
>
> **Whatever your project role, you complete Conflicts of Interest and Information Privacy
> Security (IPS for Researchers).** Conflicts of Interest appears above as conditional, and
> Information Privacy Security does not appear in the university matrix at all — in this lab,
> both are required of everyone. We would rather over-cover than find a gap in the middle of a
> study, when it is too late to fix cheaply.
>
> This is a **LUV Lab requirement**, not a statement of Villanova policy. It is already built
> into the course selections in §8.2 (#3 and #6) and the course list in §8.3 — follow those and
> you have met it without doing anything extra.

Two things follow from reading the matrix against Core Lab 2:

**Core Lab 2 covers more than the matrix minimum — including both lab-required courses.** It
has every student take Conflicts of Interest, Research Security (**Basic**), and Information
Privacy Security regardless of project role, and take the Human Subjects Research course
whether or not they are yet named on a protocol. So if you completed Core Lab 2, you have met
the matrix *and* the lab requirement above — including Human Subjects Research, ahead of ever
being added to a CAYUSE protocol. For the rows that do not apply to this lab's work — Safe
Research Environments, Animal Research, Research with Biohazards — Core Lab 2 has you answer
*No*.

> **Safe Research Environments — not required here.** Core Lab 2 instructs students to answer
> **No** to Safe Research Environments, and the matrix attaches that course to **NSF research
> with an off-campus component**. As this lab's work is currently scoped, no NSF activity here
> has an off-campus component — including the lab's **planned NSF CAREER program**. **Safe
> Research Environments is therefore not required for this lab's RAs as things stand, and a
> Core Lab 2 completer is not missing anything.**
>
> **Standing condition — the requirement attaches to the off-campus component, not to the
> program.** So it can return if the work changes: **if off-campus data collection is ever added
> to an NSF-funded study here, this course becomes required for the RAs on that study, and
> certifications completed beforehand would not cover it.** That is something to catch when a
> project is scoped — not a gap in anyone's present training. Do not enroll in the course on
> your own initiative; if you hear that off-campus collection is being planned, mention it to
> the PI.

### 8.2 Registering with CITI and selecting courses

1. **Review Villanova's own pages first** — they explain which modules apply to the research
   you will actually be doing:
   - Responsible Conduct of Research — [responsible conduct of research page](https://www1.villanova.edu/university/research-scholarship/responsible-conduct.html)
     `https://www1.villanova.edu/university/research-scholarship/responsible-conduct.html`
   - Villanova Regulatory Training — [Office of Research Protections training requirements page](https://www1.villanova.edu/villanova/provost/research-administration/research-protections/training.html)
     `https://www1.villanova.edu/villanova/provost/research-administration/research-protections/training.html`
2. **Register** at the [CITI Program](https://about.citiprogram.org/) —
   `https://about.citiprogram.org/`. Select **Villanova
   University** as your **organizational affiliation**, and **use your Villanova email
   address** when creating the account. Log in with your Villanova credentials.
3. When prompted to **add a course**, you are asked a series of questions. Answer them exactly
   as follows:

| # | Course category | Selection |
|---|---|---|
| 1 | Research Security Course | **Basic** |
| 2 | Human Subjects Research | **Social and Behavioral Research Investigators** |
| 3 | Conflicts of Interest | **Yes** — Core Lab 2's instruction: *"required for all researchers at Villanova"* |
| 4 | Responsible Conduct of Research | **Social and Behavioral Sciences** |
| 5 | Safe Research Environments | **No** — correct for this lab; see the standing condition in §8.1 |
| 6 | Information Privacy Security | **IPS for Researchers** |
| 7 | Export Controls | **Not at this time** |
| 8 | Laboratory Animal Research | **No** |
| 9 | Biosafety/Biosecurity | **No** |
| 10 | IRB Administration | **Not at this time** |
| 11 | GCP – SBR Advanced Refresher | **Not at this time** |
| 12 | Good Clinical Practice Refresher | **Not at this time** |

### 8.3 The courses to complete, and the quizzes

**You complete five courses.** Four of them sit in the **Social & Behavioral Research – Basic**
track:

- Social and Behavioral Responsible Conduct of Research
- Information Privacy Security (IPS) for Researchers
- CITI Conflicts of Interest
- Social & Behavioral Research – Basic

**The fifth is Research Security (Basic)** — selection #1 in §8.2. It is enrolled separately
and is its own course, not part of the track above. **Complete it as well.** It is the one
students most often miss, precisely because it sits outside the track.

**Not required for this lab:** *Basic Biosafety Training* and *Working with the IACUC Course*.
Core Lab 2 flags them for students who anticipate working with biohazards, chemicals, or
animals; the LUV Lab does none of these, which is the same conclusion the matrix reaches in
§8.1.

**Quizzes.** Each module ends with a quiz. You need **80% or higher to pass a quiz**, and
**retakes are permitted** — you pass a module once you have scored 80% or higher on every quiz
in it. The quizzes are open-book and meant to reinforce the material; you may consult the
module text while taking them. *(Practical tip from Core Lab 2: duplicate your browser tab so
the module stays open beside the quiz.)*

**Total time: approximately 2.5–4 hours.**

### 8.4 Proof of completion — what the lab needs

Download your **Completion Reports (PDF)** when you finish. They are also available any time
from the **My Records** tab, so a lost file is never a reason to redo a module.

**The lab's requirement is one step: send your completion reports to the Lab Manager or the
PI.** Include the completion dates, so the three-year expiry can be tracked. **Ask the Lab
Manager or the PI how they want them sent** — one email, a particular filename, or an upload
somewhere.

**Not lab procedure — do not go looking for a lab equivalent.** Core Lab 2's submission
mechanics (uploading to Blackboard, renaming reports `LASTNAME_Course.pdf`, zipping them to
`LASTNAME_CITI.zip`, and the CARITAS grading component) are **PSY 2050 course requirements**.
They govern your grade in that course and have nothing to do with the lab. The lab needs the
certificates; that is all.

**Then CAYUSE.** After CITI is complete, the Lab Manager works to add you to **CAYUSE**,
Villanova's IRB system. Provide requested information promptly so you can be added.

### 8.5 What CITI unlocks — training is the gate on every resource

This is why week 1 matters. Completed CITI is not a formality here; it is the precondition on
essentially everything you will need:

| Resource | What CITI has to do with it |
|---|---|
| **[LabArchives](https://mynotebook.labarchives.com/login) — *edit* access** — `https://mynotebook.labarchives.com/login` (experiment SOPs and runbooks, analysis runbooks, project descriptions, presentation templates, and IRB materials: protocols, recruitment materials, informed-consent documents) | Read access comes with being on the lab mailing list. **Edit access requires completed CITI training** plus active lab membership. |
| **CAYUSE enrollment** (Villanova's IRB system) | Happens **after** CITI; the Lab Manager enrolls you. |
| **NAS account** (lab storage: training exercises, experimental data, computational simulations, corpora) and **GPU account** (statistical modeling, simulations) | Restricted to lab personnel who have **completed CITI training** and are actively conducting research; the PI provisions the accounts. |
| **Sound-booth scheduling** (per-booth calendars — LUV and WRAP labs; booth time requested from the Lab Manager or the PI) | Restricted to those with **updated CITI training** who are actively conducting research. |

Note the word **"updated."** Currency matters, not just having done it once: Core Lab 2 puts
the certification's validity at **three years**. A lapsed certificate does not hold these doors
open. **Ask the Lab Manager or the PI which refresher course to take and how far ahead to start
it** — do not wait for the expiry date to find out.

### 8.6 Who this applies to

The lab's onboarding materials scope CITI to students who **plan to participate in data
collection** — and they gate
**LabArchives edit access, NAS, and GPU** on completed CITI as well, so in practice
it reaches nearly every active RA, including analysis-side students who never run a participant
but do need lab storage or compute.

If you work **only** from de-identified files already in the lab's repository and never need
NAS, GPU, CAYUSE, or a booth, **ask the Lab Manager or the PI whether CITI is still required of
you** — do not assume you are exempt. That is Section 5's rule applied to your own paperwork.

---

## Exercises  *(synthetic/practice data only — never real participant data)*

**Exercise 1 — Sort the files.** For each, mark **REPO-OK** or **NEVER**:
1. `sub-04_task-oddball_eeg.vhdr`
2. `desc-summary_qc.tsv` (group QC table, no names)
3. `interview_maria_raw.wav`
4. `config.yaml` (study parameters, no identifiers)
5. `participant_key.xlsx` (ID → name, DOB)
6. `grand-average_ave.fif` (de-identified, group-level)
7. `consent_signed_scan.pdf`
8. `formants_deidentified.csv` (keyed to `sub-01`…`sub-12`, no names)

**Exercise 2 — Spot the identifier.** In this synthetic transcript line, name every residual
identifier a de-identification pass must remove:
> "So after I graduated from Roman Catholic High in 2019, my mom Rosa and I moved from the
> block by Lighthouse Field to my aunt's place, and I started at Temple that fall."

**Exercise 3 — IRB-exempt reasoning.** True or false, with a one-line reason each:
(a) "The study is IRB-exempt, so I don't need to bother with consent or secure storage."
(b) "Exempt means the de-identified QC table is fine to commit to the repo."
(c) "I can decide the study is exempt if it looks low-risk."

**Exercise 4 — When unsure.** You are asked to "grab the EEG data for sub-08 and drop it in
the project folder so the team can see it." You notice the source files are `.vhdr`/`.eeg`.
What do you do, in one sentence?

**Exercise 5 — CITI status.** For each RA, state what they should do next, in one line:
(a) Took PSY 2050 last spring and completed Core Lab 2; has the completion reports saved.
(b) Transferred in, never took PSY 2050, joining the Cognition cohort to run participants.
(c) Completed Core Lab 2 in 2022; joining the lab now, in 2026.
(d) Completed Core Lab 2 this term; hears in a project meeting that a new NSF-funded study
    might collect data at a community site off campus. Is their certification incomplete?
(e) Has current CITI on file and wants to upload a revised consent document to LabArchives —
    but the PI has not yet confirmed IRB status in writing for their study.

---

## Answer key

**Ex. 1.** REPO-OK: 2, 4, 6, 8. NEVER: 1 (raw EEG), 3 (raw audio), 5 (linking key — the most
sensitive file), 7 (signed consent). Rule of thumb: group-level de-identified derivatives,
tables, config, and code are OK; anything raw, per-person-identifiable, or a key is NEVER.

**Ex. 2.** Residual identifiers: **"Roman Catholic High"** (specific school), **"2019"**
(graduation year — a date that narrows identity), **"Rosa"** (named relative),
**"Lighthouse Field"** (specific place/landmark), **"Temple"** (specific institution), and
**"my aunt"** + the move together (relational/geographic triangulation). In a small
community these combine to re-identify even though no full legal name appears — that is the
point of Section 1.

**Ex. 3.** (a) **False** — exempt is a regulatory category, not an ethics waiver; consent
(as applicable) and secure storage still apply. (b) **False for the wrong reason** — a
de-identified group QC table is generally repo-OK, but *because it is de-identified*, not
*because the study is exempt*; exemption status is irrelevant to the repo rule. (c) **False**
— you never determine exemption; the PI/IRB does, confirmed in writing.

**Ex. 4.** Stop and ask the PI/Lab Manager: `.vhdr`/`.eeg` are **raw EEG** and must never
enter the repo — only de-identified derivatives may, and only after IRB status is confirmed.
("When unsure, stop and ask before acting.")

**Ex. 5.** (a) **Nothing to redo** — send the completion reports (with dates) to the Lab
Manager or the PI and ask about CAYUSE; Core Lab 2 treats certification as valid **three
years**.
(b) **The full path in §8** — register with a Villanova email and Villanova University
affiliation, make the twelve course selections, complete the four Social & Behavioral Research
– Basic modules **plus Research Security (Basic)** — five courses — at ≥80% per quiz,
download from **My Records**, send to the Lab Manager or the PI; ~2.5–4 hours, week 1.
(c) **Not current** — 2022 plus three years has lapsed, so the resources in §8.5 stay closed
until it is renewed. **Ask the Lab Manager or the PI how to renew** — do not assume the old
certificate still counts, and do not assume a full retake is needed.
(d) **Their certification is complete as things stand — and what they heard is exactly the
thing to pass on.** Safe Research Environments is not required for this lab's work as it is
currently scoped, so nothing is missing from what they have already done (§8.1). But the
requirement attaches to the *off-campus component*: if that study does add off-campus
collection, the course becomes required for the RAs on it, and certifications completed
beforehand would not cover it.
Mention it to the PI when the study is scoped; don't enroll on your own, and don't treat
yourself as out of compliance in the meantime.
(e) **Two different gates, and neither one is satisfied.** CITI unlocks LabArchives *edit
access*; it does not authorize the action. Editing an IRB protocol document is not an RA's call
in any case, and nothing proceeds before the PI confirms IRB status in writing (§4, §5). Stop
and ask.

---

## Competence check *(PI-verifiable in minutes)*

- **Short quiz, ≥ 90% to pass** (drawn from the five exercises) **and** a **signed data-use
  agreement** on file.
- **CITI status verified:** current completion reports on file with the Lab Manager — or, for a
  student who has not yet done it, a stated start date and a week-1 plan (§8).
- Unprompted, the RA can state: (1) the **repo rule** — code + de-identified derivatives +
  summaries only, nothing raw or identifiable; (2) the **when-unsure rule** — stop and ask
  before acting; (3) that **IRB-exempt ≠ ethics-exempt**; and (4) that **completed CITI is what
  unlocks LabArchives edit access, CAYUSE, NAS/GPU accounts, and booth scheduling — while
  authorizing no data contact by itself.**
- **No data access — speech or EEG — is granted until this check is passed.** The PI (or a
  delegate the PI names, e.g. the Lab Manager) records the pass.
