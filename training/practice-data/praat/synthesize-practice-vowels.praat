# synthesize-practice-vowels.praat
#
# Convenience script for Module 2, Exercise 1 (people/training/praat-acoustics.md).
#
# WHAT IT DOES. Synthesizes five vowels whose F1/F2 you specify below, so you
# can measure them back with Praat's formant tracker and see how close your
# measurement lands. The ground truth is whatever you typed in -- that is the
# whole point. Nothing is downloaded and no recording is involved.
#
# ------------------------------------------------------------------------
# THE CALL, AND WHAT ITS ARGUMENTS MEAN
#
# Verified against Praat's own manual page (PI-supplied, 2026-08-29). The
# command takes TWELVE arguments, in this order:
#
#   Create KlattGrid from vowel: name$, duration, pitch,
#                                F1, B1, F2, B2, F3, B3,
#                                F4, bandwidthFraction, formantFrequencyInterval
#
#   Praat's documented example:  "a", 0.3, 125, 800, 80, 1200, 80, 2300, 100,
#                                2800, 0.05, 1000
#
# Three things worth understanding rather than copying:
#
#   * F1-F4 are frequencies, and a NON-POSITIVE frequency means that formant
#     is simply not used. B1-B3 are explicit bandwidths, for the first three
#     formants ONLY.
#   * F4 has no bandwidth argument of its own. Its bandwidth is
#     bandwidthFraction x F4 -- the fraction is the inverse of the quality
#     factor Q. At 0.05 and F4 = 3600 Hz that is 180 Hz, i.e. Q = 20.
#   * formantFrequencyInterval sets the spacing of F5 and above
#     (F5 = F4 + interval, F6 = F5 + interval, ...). ~1000 Hz is conventional
#     for an average male voice and ~1100 Hz for an average female voice; a
#     non-positive value suppresses those higher formants entirely.
#
# There is also a GUI route, if you would rather not run a script at all:
#     New > Sound > Create Sound from VowelEditor...
# You set F1/F2 there by hand, which gives you the same known ground truth.
# Measuring back is identical either way.
# ------------------------------------------------------------------------
#
# HOW TO RUN.  Praat > Open Praat script... > this file > Run > Run.
# Exactly five Sound objects appear in the Objects list, each named for its
# true F1 and F2. The KlattGrid each Sound is made from is removed on the way
# out, so there is nothing in the list you have to ignore.
#
# RUN SUCCESSFULLY IN PRAAT BY THE PI, 2026-08-29: the script executed and
# produced those five Sound objects.
#
# Confirmed working in the lab's Praat by that run, and worth reusing when you
# write the next script here: indexed string arrays (`vowelLabel$ [i]`);
# capturing object ids from menu commands (`x = Create ...`, `s = To Sound`);
# `removeObject:` / `selectObject:` with those ids; `string$ (...)` with a space
# before the parenthesis; `...` continuation lines inside a long argument list;
# and trailing `; comments` on settings lines.

# --- The practice vowels: label, true F1, true F2 ------------------------
# These span a vowel space wide enough that a tracker error is visible.
# Change them freely -- the exercise works with any values you can defend.

numberOfVowels = 5

vowelLabel$ [1] = "FLEECE"
f1 [1] =  350
f2 [1] = 2400

vowelLabel$ [2] = "KIT"
f1 [2] =  480
f2 [2] = 2000

vowelLabel$ [3] = "DRESS"
f1 [3] =  620
f2 [3] = 1850

vowelLabel$ [4] = "TRAP"
f1 [4] =  800
f2 [4] = 1700

vowelLabel$ [5] = "LOT"
f1 [5] =  750
f2 [5] = 1200

# --- Fixed synthesis settings -------------------------------------------
duration    = 0.40     ; seconds
pitch       = 120      ; Hz -- a mid adult F0
bandwidth1  = 50       ; Hz
bandwidth2  = 70       ; Hz
f3          = 2800     ; Hz, held constant
bandwidth3  = 110      ; Hz
f4          = 3600     ; Hz
bandwidthFraction = 0.05   ; F4 bandwidth = fraction x F4 = 180 Hz, i.e. Q = 20
                           ; (Praat's documented example value; sharper and more
                           ;  speech-like than a wider fraction, and it only
                           ;  affects F4 and above -- F1-F3 carry the explicit
                           ;  bandwidths set above)
formantInterval   = 1000   ; Hz spacing for F5 and up (F5 = F4 + interval, ...)

for i from 1 to numberOfVowels
    # Build the object name once, and use it for both the KlattGrid and the Sound.
    name$ = "syn_" + vowelLabel$ [i] + "_F1-" + string$ (f1 [i]) + "_F2-" + string$ (f2 [i])

    # Twelve arguments; see the header for what each one does.
    klattGrid = Create KlattGrid from vowel: name$, duration, pitch,
    ... f1 [i], bandwidth1, f2 [i], bandwidth2, f3, bandwidth3,
    ... f4, bandwidthFraction, formantInterval

    sound = To Sound
    Rename: name$

    # The KlattGrid has done its job. Remove it, so the Objects list ends up
    # holding the five Sounds and nothing else.
    removeObject: klattGrid
    selectObject: sound
endfor

writeInfoLine: "Synthesized ", numberOfVowels, " practice vowels."
appendInfoLine: "Each Sound object is named with its TRUE F1 and F2."
appendInfoLine: ""
appendInfoLine: "Now measure them back:"
appendInfoLine: "  1. Select a Sound, click View & Edit."
appendInfoLine: "  2. Formant > Show formants, then Formant > Formant settings..."
appendInfoLine: "  3. Set a formant ceiling, select the steady middle of the vowel,"
appendInfoLine: "     and read F1/F2 off the Formant listing."
appendInfoLine: "  4. Log measured vs. true in measurement-log.csv."
appendInfoLine: ""
appendInfoLine: "Then repeat with a deliberately wrong ceiling and watch it break."
