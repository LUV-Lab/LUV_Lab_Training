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
# [confirm] BEFORE FIRST STUDENT USE
#
# Praat's scripting syntax for `Create KlattGrid from vowel` has varied
# across versions (the older form uses `...` and spaces, the modern form
# uses `:` and commas, and the argument list has not been identical in every
# release). VERIFY THE ARGUMENT ORDER against your own Praat's Help before
# handing this to a student:  Help > Search Praat manual > "KlattGrid".
#
# THE EXERCISE DOES NOT DEPEND ON THIS SCRIPT. If the script errors on your
# version, use the GUI route in the module instead:
#     New > Sound > Create Sound from VowelEditor...
# You set F1/F2 there by hand, which gives you the same known ground truth
# with no scripting at all. Measuring back is identical either way.
# ------------------------------------------------------------------------
#
# HOW TO RUN.  Praat > Open Praat script... > this file > Run > Run.
# Five Sound objects appear in the Objects list, named for their true values.

# --- The practice vowels: label, true F1, true F2 ------------------------
# These span a vowel space wide enough that a tracker error is visible.
# Change them freely -- the exercise works with any values you can defend.

vowelLabels$ = "FLEECE KIT DRESS TRAP LOT"
numberOfVowels = 5

f1 [1] =  350
f2 [1] = 2400
f1 [2] =  480
f2 [2] = 2000
f1 [3] =  620
f2 [3] = 1850
f1 [4] =  800
f2 [4] = 1700
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

for i from 1 to numberOfVowels
    label$ = Extract word$: vowelLabels$, i

    # [confirm] argument order against your Praat version -- see header.
    Create KlattGrid from vowel: "syn_" + label$ + "_F1-" + string$ (f1 [i])
    ... + "_F2-" + string$ (f2 [i]),
    ... duration, pitch,
    ... f1 [i], bandwidth1,
    ... f2 [i], bandwidth2,
    ... f3, bandwidth3,
    ... f4, 0.1, 1000

    To Sound
    Rename: "syn_" + label$ + "_F1-" + string$ (f1 [i]) + "_F2-" + string$ (f2 [i])
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
