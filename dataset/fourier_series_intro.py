"""
Natural Group Name: Fourier Series Building a Square Wave

Educational Objectives:
- To visualize how sine waves combine to approximate a square wave
- To demonstrate the Fourier series decomposition of periodic functions
- To build intuition for frequency domain representation
- To show convergence as more terms are added to the series

Story Arc & Intent:
The animation reveals the remarkable Fourier series result: infinitely many
sine waves, when combined with the right amplitudes and frequencies, can
build any periodic function, including discontinuous ones like a square wave.

Narrative Flow:
- Hook/Opening: Present a target square wave to approximate
- Development: Show individual sine wave harmonics with odd frequencies
- Build-up: Add harmonics one by one, watching the approximation improve
- Climax: Many harmonics combine to closely match the square wave
- Resolution: General principle of Fourier decomposition

Technical Implementation Notes:
- Scene Classes: TargetWave, AddSineWaves, ConvergenceToSquare, GeneralPrinciple
- Key Visual Elements: Graphs of waves, sum curves, amplitude spectrum
- Animation Techniques: Function graphing, additive combination, convergence animation
- Mathematical Concepts: Fourier series, harmonics, frequency decomposition

Dependency Chain:
All scenes use basic manimlib components: Axes, graphs, Text, Tex.
No custom utilities required.

Rendering Instructions:
To render these scenes, use the manim command-line tool:
- For a single scene: manimgl fourier_series_intro.py TargetWave
- For all scenes: iterate through SCENE_ORDER
"""

# ============================================================
# 1. IMPORTS
# ============================================================
from manimlib import *
import numpy as np

# ============================================================
# 2. CONFIGURATION AND CONSTANTS
# ============================================================
# All constants are from manimlib.constants and used directly in the scenes.
#
# Color Scheme:
# - BLUE: Target square wave
# - YELLOW: Fundamental frequency (first harmonic)
# - GREEN: Sum of harmonics (approximation)
# - RED: Individual harmonic being added
# - TEAL, MAROON, PURPLE: Additional harmonics
# - WHITE: Axes and grid
# - GREY_A: De-emphasized elements
#
# Key Manim Constants Used:
# - UP, DOWN, LEFT, RIGHT: Direction vectors
# - ORIGIN: Center point
# - TAU: 2π for periodic functions
# - PI: π for wave calculations

# Axes configuration
AXES_CONFIG = {
    "x_range": (0, 4 * PI, PI),
    "y_range": (-1.5, 1.5, 0.5),
    "width": 12,
    "height": 6,
}

# Wave colors for different harmonics
HARMONIC_COLORS = [YELLOW, TEAL, MAROON_B, PURPLE_B, PINK, GOLD, BLUE_D]

# ============================================================
# 3. UTILITY FUNCTIONS
# ============================================================

def square_wave(x, amplitude=1.0):
    """
    Square wave function with period 2π.

    Args:
        x: Input value
        amplitude: Amplitude of the wave

    Returns:
        Square wave value (+amplitude or -amplitude)
    """
    return amplitude * np.sign(np.sin(x))

def fourier_square_wave(x, n_terms):
    """
    Fourier series approximation of square wave.

    The Fourier series for a square wave is:
    f(x) = (4/π) * Σ[k=0 to ∞] sin((2k+1)x) / (2k+1)

    Args:
        x: Input value
        n_terms: Number of terms in the series

    Returns:
        Approximation value
    """
    result = 0
    for k in range(n_terms):
        n = 2 * k + 1  # Odd harmonics only
        result += np.sin(n * x) / n

    return (4 / PI) * result

def get_harmonic(k):
    """
    Get the kth harmonic function.

    Args:
        k: Harmonic index (0 = fundamental)

    Returns:
        Function for the kth harmonic
    """
    n = 2 * k + 1
    amplitude = (4 / PI) / n

    def harmonic(x):
        return amplitude * np.sin(n * x)

    return harmonic

# ============================================================
# 4. BASE CLASSES AND HELPERS
# ============================================================
# No custom base classes needed

# ============================================================
# 5. SCENE IMPLEMENTATIONS
# ============================================================

class TargetWave(InteractiveScene):
    """
    Part 1: Introduce the square wave as our target function.

    Narrative purpose:
        To establish the challenge: can we build this discontinuous,
        sharp-cornered square wave from smooth sine waves?

    Mathematical content:
        A square wave alternates between +1 and -1 with period 2π.
        It seems impossible to build from smooth functions.

    Visual approach:
        Show the square wave clearly, emphasizing its discontinuities
        and sharp transitions, posing the question of decomposition.
    """
    def construct(self):
        # ========================================
        # SETUP: Title
        # ========================================
        title = OldTexText("Fourier Series: Building a Square Wave", font_size=48)
        title.to_edge(UP)

        self.play(FadeIn(title, shift=DOWN))
        self.wait()

        # ========================================
        # CREATE: Axes
        # ========================================
        axes = Axes(**AXES_CONFIG)
        axes.add_coordinates()

        self.play(ShowCreation(axes), run_time=1.5)
        self.wait()

        # ========================================
        # DRAW: Square wave
        # ========================================
        square = axes.get_graph(
            lambda x: square_wave(x),
            x_range=(0.01, 4 * PI - 0.01),
            color=BLUE,
            discontinuities=[PI, 2*PI, 3*PI],
            dt=0.01
        )

        wave_label = Tex("\\text{Square Wave}", font_size=36, color=BLUE)
        wave_label.next_to(square.get_end(), UR, buff=0.3)

        self.play(ShowCreation(square), run_time=2)
        self.play(FadeIn(wave_label, shift=DL))
        self.wait()

        # ========================================
        # HIGHLIGHT: Properties
        # ========================================
        properties = VGroup(
            OldTexText("• Discontinuous jumps", font_size=28),
            OldTexText("• Sharp corners", font_size=28),
            OldTexText("• Period = 2π", font_size=28)
        )
        properties.arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        properties.to_edge(LEFT, buff=1)
        properties.shift(DOWN)

        self.play(FadeIn(properties, shift=RIGHT, lag_ratio=0.3))
        self.wait()

        # ========================================
        # QUESTION: Can we build this?
        # ========================================
        question = OldTexText(
            "Can we build this from smooth sine waves?",
            font_size=36,
            color=YELLOW
        )
        question.to_edge(DOWN, buff=0.5)

        self.play(FadeIn(question, shift=UP))
        self.wait(2)


class AddSineWaves(InteractiveScene):
    """
    Part 2: Show individual sine wave harmonics.

    Narrative purpose:
        To introduce the building blocks: sine waves with odd multiples
        of the fundamental frequency, each with decreasing amplitude.

    Mathematical content:
        Fourier series for square wave uses only odd harmonics:
        sin(x), sin(3x)/3, sin(5x)/5, sin(7x)/7, ...

    Visual approach:
        Display the first few harmonics individually, showing their
        frequencies and amplitudes, before combining them.
    """
    def construct(self):
        # ========================================
        # SETUP: Title
        # ========================================
        title = OldTexText("The Harmonics", font_size=48)
        title.to_edge(UP)

        self.add(title)

        # ========================================
        # CREATE: Axes
        # ========================================
        axes = Axes(**AXES_CONFIG)
        axes.add_coordinates()

        self.add(axes)

        # ========================================
        # SHOW: First few harmonics
        # ========================================
        harmonics_to_show = [0, 1, 2, 3]  # k = 0, 1, 2, 3

        for k in harmonics_to_show:
            n = 2 * k + 1
            harmonic_func = get_harmonic(k)
            color = HARMONIC_COLORS[k % len(HARMONIC_COLORS)]

            # Graph the harmonic
            graph = axes.get_graph(
                harmonic_func,
                x_range=(0, 4 * PI),
                color=color
            )

            # Label
            amplitude = (4 / PI) / n
            label = Tex(
                f"\\frac{{{4/PI:.2f}}}{{{n}}} \\sin({n}x)",
                font_size=36,
                color=color
            )
            label.to_corner(UR, buff=0.5)

            self.play(ShowCreation(graph), run_time=1.5)
            self.play(FadeIn(label, shift=DOWN))
            self.wait()

            # Fade out for next one
            if k < harmonics_to_show[-1]:
                self.play(
                    FadeOut(graph),
                    FadeOut(label)
                )

        # ========================================
        # INSIGHT: Pattern
        # ========================================
        pattern = OldTexText(
            "Only odd frequencies: 1, 3, 5, 7, ...\nAmplitudes decrease: 1, 1/3, 1/5, 1/7, ...",
            font_size=28,
            color=GREY_A
        )
        pattern.to_edge(DOWN, buff=0.5)

        self.play(FadeIn(pattern, shift=UP))
        self.wait(2)


class ConvergenceToSquare(InteractiveScene):
    """
    Part 3: Show convergence as harmonics are added.

    Narrative purpose:
        To demonstrate the remarkable convergence: adding more harmonics
        progressively builds a better approximation to the square wave.

    Mathematical content:
        Partial sum S_n(x) = (4/π) Σ[k=0 to n-1] sin((2k+1)x)/(2k+1)
        converges to the square wave as n → ∞.

    Visual approach:
        Start with n=1, progressively add harmonics, showing the sum
        curve getting closer to the square wave target.
    """
    def construct(self):
        # ========================================
        # SETUP: Title
        # ========================================
        title = OldTexText("Building the Square Wave", font_size=48)
        title.to_edge(UP)

        self.add(title)

        # ========================================
        # CREATE: Axes
        # ========================================
        axes = Axes(**AXES_CONFIG)
        axes.add_coordinates()

        self.add(axes)

        # ========================================
        # SHOW: Target square wave (faint)
        # ========================================
        target = axes.get_graph(
            lambda x: square_wave(x),
            x_range=(0.01, 4 * PI - 0.01),
            color=BLUE,
            discontinuities=[PI, 2*PI, 3*PI],
            dt=0.01,
            stroke_opacity=0.3
        )

        target_label = OldTexText("Target", font_size=28, color=BLUE)
        target_label.to_corner(UL, buff=0.5)
        target_label.shift(0.5 * DOWN)

        self.play(ShowCreation(target))
        self.play(FadeIn(target_label))
        self.wait()

        # ========================================
        # PROGRESSIVE: Add harmonics
        # ========================================
        n_values = [1, 2, 3, 5, 7, 11]

        approximation = None
        n_text = None

        for n in n_values:
            # Create new approximation
            new_approx = axes.get_graph(
                lambda x: fourier_square_wave(x, n),
                x_range=(0, 4 * PI),
                color=GREEN
            )

            # Label
            new_n_text = Tex(
                f"n = {n} \\text{{ terms}}",
                font_size=36,
                color=GREEN
            )
            new_n_text.to_corner(UR, buff=0.5)

            # Animate
            if approximation is None:
                self.play(ShowCreation(new_approx), run_time=1.5)
                self.play(Write(new_n_text))
            else:
                self.play(
                    Transform(approximation, new_approx),
                    Transform(n_text, new_n_text),
                    run_time=1.5
                )

            approximation = new_approx if approximation is None else approximation
            n_text = new_n_text if n_text is None else n_text

            self.wait()

        # ========================================
        # FINALE: Very close!
        # ========================================
        result = OldTexText(
            "As n → ∞, we get the exact square wave!",
            font_size=36,
            color=YELLOW
        )
        result.to_edge(DOWN, buff=0.5)

        self.play(FadeIn(result, shift=UP))
        self.wait(2)


class GeneralPrinciple(InteractiveScene):
    """
    Part 4: State the general Fourier series principle.

    Narrative purpose:
        To generalize beyond the square wave, showing that any periodic
        function can be decomposed into a sum of sines and cosines.

    Mathematical content:
        Fourier series: f(x) = a₀/2 + Σ[n=1 to ∞] (aₙcos(nx) + bₙsin(nx))
        Any periodic function can be represented this way.

    Visual approach:
        Present the general formula, emphasize its universality,
        and highlight the power of frequency domain thinking.
    """
    def construct(self):
        # ========================================
        # SETUP: Title
        # ========================================
        title = OldTexText("The Fourier Series", font_size=48)
        title.to_edge(UP)

        self.add(title)

        # ========================================
        # FORMULA: General Fourier series
        # ========================================
        formula = Tex(
            "f(x) = \\frac{a_0}{2} + \\sum_{n=1}^{\\infty} \\left( a_n \\cos(nx) + b_n \\sin(nx) \\right)",
            font_size=44
        )
        formula.shift(1 * UP)

        box = SurroundingRectangle(formula, buff=0.3, color=YELLOW, stroke_width=3)

        self.play(Write(formula), run_time=2.5)
        self.play(ShowCreation(box))
        self.wait()

        # ========================================
        # EXPLANATION: What this means
        # ========================================
        explanation = OldTexText(
            "Any periodic function can be written\nas a sum of sines and cosines!",
            font_size=32,
            color=GREEN
        )
        explanation.next_to(formula, DOWN, buff=1)

        self.play(FadeIn(explanation, shift=UP))
        self.wait(2)

        # ========================================
        # SQUARE WAVE: Specific case
        # ========================================
        square_formula = Tex(
            "\\text{Square wave: } f(x) = \\frac{4}{\\pi} \\sum_{k=0}^{\\infty} \\frac{\\sin((2k+1)x)}{2k+1}",
            font_size=36
        )
        square_formula.next_to(explanation, DOWN, buff=1)

        self.play(FadeIn(square_formula, shift=UP))
        self.wait()

        # ========================================
        # APPLICATIONS: Why this matters
        # ========================================
        applications = VGroup(
            OldTexText("Applications:", font_size=32, weight=BOLD),
            OldTexText("• Signal processing", font_size=28),
            OldTexText("• Audio compression (MP3)", font_size=28),
            OldTexText("• Image compression (JPEG)", font_size=28),
            OldTexText("• Solving differential equations", font_size=28),
            OldTexText("• Quantum mechanics", font_size=28)
        )
        applications.arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        applications.to_edge(DOWN, buff=0.5)

        self.play(FadeIn(applications, shift=UP, lag_ratio=0.2))
        self.wait(3)

        # ========================================
        # FINALE: Checkmark
        # ========================================
        checkmark = Tex("\\checkmark", font_size=72, color=GREEN)
        checkmark.next_to(box, RIGHT, buff=0.5)

        self.play(FadeIn(checkmark, scale=2))
        self.wait(2)


# ============================================================
# 6. SCENE EXECUTION ORDER
# ============================================================
# The order of scenes that tells the story.
#
# Scene 1 (TargetWave):
#   - Introduces the square wave as the target function
#   - Highlights its discontinuous, sharp-cornered nature
#   - Poses the challenge of building it from smooth waves
#
# Scene 2 (AddSineWaves):
#   - Shows the individual harmonics used in the series
#   - Displays odd-frequency sine waves with decreasing amplitudes
#   - Reveals the pattern: 1, 3, 5, 7, ... with amplitudes 1/n
#
# Scene 3 (ConvergenceToSquare):
#   - Demonstrates progressive convergence
#   - Shows sum of harmonics approaching the square wave
#   - Illustrates the limit as n → ∞
#
# Scene 4 (GeneralPrinciple):
#   - States the general Fourier series formula
#   - Shows the square wave as a specific case
#   - Lists important applications of Fourier analysis

SCENE_ORDER = [
    TargetWave,              # Part 1: The square wave target
    AddSineWaves,            # Part 2: Individual harmonics
    ConvergenceToSquare,     # Part 3: Progressive convergence
    GeneralPrinciple,        # Part 4: General Fourier series
]
