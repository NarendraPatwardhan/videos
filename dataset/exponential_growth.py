"""
Natural Group Name: e and Exponential Functions

Educational Objectives:
- To visualize exponential growth and the number e
- To demonstrate e as the limit of (1+1/n)^n as n approaches infinity
- To show the connection between e^x and compound interest
- To reveal the unique property: the derivative of e^x equals itself

Story Arc & Intent:
The animation reveals the mysterious constant e through compound interest and
continuous growth. This transforms the abstract number e ≈ 2.71828 into a
natural consequence of compounding infinitely many times, and shows why e^x
is the most "natural" exponential function.

Narrative Flow:
- Hook/Opening: Exponential growth in nature and finance
- Development: Compound interest with increasing frequency
- Build-up: The limit as compounding becomes continuous
- Climax: e emerges as (1+1/n)^n → e and the derivative property
- Resolution: Why e^x is special and ubiquitous in mathematics

Technical Implementation Notes:
- Scene Classes: DefineExponential, NumberE, CompoundInterest, DerivativeProperty
- Key Visual Elements: Graphs, limits, compound interest visualization
- Animation Techniques: Graph growth, limit convergence, derivative comparison
- Mathematical Concepts: Exponential functions, e, limits, derivatives, compound interest

Dependency Chain:
All scenes use basic manimlib components: Axes, graphs, Tex, Text.
Uses numpy for calculations. No custom utilities required beyond helper
functions defined in this file.

Rendering Instructions:
To render these scenes, use the manim command-line tool:
- For a single scene: manimgl exponential_growth.py DefineExponential
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
# - BLUE: Exponential function e^x
# - YELLOW: Approximations and limits
# - GREEN: Derivatives and special properties
# - RED: Comparisons (other bases)
# - WHITE: Axes and labels
# - GREY_A: De-emphasized elements
#
# Key Manim Constants Used:
# - UP, DOWN, LEFT, RIGHT: Direction vectors
# - ORIGIN: Center point
# - PI: π for calculations
# - MED_SMALL_BUFF: Spacing

# Euler's number
E = np.e

# ============================================================
# 3. UTILITY FUNCTIONS
# ============================================================

def compound_interest_value(principal, rate, n, time):
    """
    Calculate compound interest.

    Args:
        principal: Initial amount
        rate: Annual interest rate (as decimal)
        n: Number of times compounded per year
        time: Time in years

    Returns:
        Final value
    """
    return principal * (1 + rate/n) ** (n * time)

def limit_approximation(n):
    """
    Compute (1 + 1/n)^n as approximation to e.

    Args:
        n: Value to use in the limit

    Returns:
        Approximation value
    """
    return (1 + 1/n) ** n

def create_exp_graph(axes, base=E, color=BLUE, **kwargs):
    """
    Create a graph of an exponential function.

    Args:
        axes: Axes object
        base: Base of exponential (default e)
        color: Color of graph
        **kwargs: Additional arguments

    Returns:
        Graph mobject
    """
    return axes.get_graph(
        lambda x: base ** x,
        color=color,
        **kwargs
    )

# ============================================================
# 4. SCENE CLASSES
# ============================================================

class DefineExponential(Scene):
    """
    Scene 1: Introduce exponential functions and their growth.

    This scene presents exponential functions and shows how they grow
    much faster than polynomial functions.
    """

    def construct(self):
        # ========================================
        # TITLE
        # ========================================
        title = OldTexText("Exponential Growth", font_size=48)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait()

        # ========================================
        # DEFINITION
        # ========================================
        definition = Tex(
            "f(x) = a^x \\quad \\text{(exponential function)}",
            font_size=36
        )
        definition.next_to(title, DOWN, buff=0.6)

        self.play(Write(definition))
        self.wait()

        # ========================================
        # SETUP: Axes
        # ========================================
        axes = Axes(
            x_range=[0, 5, 1],
            y_range=[0, 10, 2],
            width=9,
            height=5,
        )
        axes.shift(DOWN * 0.5)

        self.play(ShowCreation(axes))
        self.wait()

        # ========================================
        # COMPARE: Different bases
        # ========================================
        # Base 2
        exp2_graph = axes.get_graph(
            lambda x: 2 ** x,
            color=YELLOW,
            x_range=(0, 3.3)
        )
        exp2_label = Tex("2^x", color=YELLOW, font_size=28)
        exp2_label.next_to(axes.c2p(3, 2**3), RIGHT, buff=0.2)

        self.play(ShowCreation(exp2_graph), Write(exp2_label))
        self.wait()

        # Base e
        expe_graph = axes.get_graph(
            lambda x: np.exp(x),
            color=BLUE,
            x_range=(0, 2.3)
        )
        expe_label = Tex("e^x", color=BLUE, font_size=28)
        expe_label.next_to(axes.c2p(2, np.exp(2)), RIGHT, buff=0.2)

        self.play(ShowCreation(expe_graph), Write(expe_label))
        self.wait()

        # Base 10
        exp10_graph = axes.get_graph(
            lambda x: 10 ** x,
            color=RED,
            x_range=(0, 1)
        )
        exp10_label = Tex("10^x", color=RED, font_size=28)
        exp10_label.next_to(axes.c2p(1, 10), RIGHT, buff=0.2)

        self.play(ShowCreation(exp10_graph), Write(exp10_label))
        self.wait()

        # ========================================
        # OBSERVATION
        # ========================================
        observation = OldTexText(
            "All grow rapidly, but what makes e special?",
            font_size=28,
            color=WHITE
        )
        observation.to_edge(DOWN).shift(UP * 0.3)

        self.play(FadeIn(observation, shift=UP))
        self.wait(2)


class NumberE(Scene):
    """
    Scene 2: Show e as the limit of (1+1/n)^n.

    This scene demonstrates how e emerges from the limit definition
    and shows numerical approximations converging to e.
    """

    def construct(self):
        # ========================================
        # TITLE
        # ========================================
        title = OldTexText("The Number e", font_size=42)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait()

        # ========================================
        # LIMIT DEFINITION
        # ========================================
        limit_def = Tex(
            "e = \\lim_{n \\to \\infty} \\left(1 + \\frac{1}{n}\\right)^n",
            font_size=40,
            color=BLUE
        )
        limit_def.next_to(title, DOWN, buff=0.8)

        limit_box = SurroundingRectangle(limit_def, buff=0.3, color=BLUE, stroke_width=2)

        self.play(Write(limit_def))
        self.play(ShowCreation(limit_box))
        self.wait()

        # ========================================
        # COMPUTE APPROXIMATIONS
        # ========================================
        approx_title = OldTexText("Computing approximations:", font_size=28)
        approx_title.next_to(limit_box, DOWN, buff=0.8)

        self.play(Write(approx_title))
        self.wait()

        # Create table
        n_values = [1, 2, 5, 10, 100, 1000, 10000]
        approx_values = [(n, limit_approximation(n)) for n in n_values]

        table_entries = VGroup()

        # Header
        header = VGroup(
            OldTexText("n", font_size=24),
            OldTexText("(1 + 1/n)^n", font_size=24, color=YELLOW),
        )
        header.arrange(RIGHT, buff=2.0)
        table_entries.add(header)

        # Data rows
        for n, value in approx_values:
            if n >= 1000:
                n_str = f"{n:,}"
            else:
                n_str = str(n)

            row = VGroup(
                OldTexText(n_str, font_size=22),
                OldTexText(f"{value:.6f}", font_size=22, color=YELLOW),
            )
            row.arrange(RIGHT, buff=2.0)
            # Align with header
            row[0].align_to(header[0], LEFT)
            row[1].align_to(header[1], LEFT)
            table_entries.add(row)

        table_entries.arrange(DOWN, buff=0.25, aligned_edge=LEFT)
        table_entries.next_to(approx_title, DOWN, buff=0.5)
        table_entries.scale(0.9)

        # Animate table
        self.play(Write(header))
        self.wait()

        for i in range(1, len(table_entries)):
            self.play(FadeIn(table_entries[i], shift=UP), run_time=0.4)

        self.wait()

        # ========================================
        # VALUE OF E
        # ========================================
        e_value = Tex(
            f"e \\approx {E:.10f}\\ldots",
            font_size=36,
            color=GREEN
        )
        e_value.to_edge(DOWN).shift(UP * 0.5)

        e_box = SurroundingRectangle(e_value, buff=0.2, color=GREEN, stroke_width=2)

        self.play(Write(e_value))
        self.play(ShowCreation(e_box))
        self.wait(2)


class CompoundInterest(Scene):
    """
    Scene 3: Show e emerging from compound interest.

    This scene demonstrates how e appears when we compound interest
    continuously, connecting abstract math to practical finance.
    """

    def construct(self):
        # ========================================
        # TITLE
        # ========================================
        title = OldTexText("Compound Interest and e", font_size=42)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait()

        # ========================================
        # SCENARIO
        # ========================================
        scenario = VGroup(
            OldTexText("Invest $1 at 100% annual interest", font_size=28),
            OldTexText("How much after 1 year?", font_size=28, color=YELLOW),
        )
        scenario.arrange(DOWN, buff=0.3)
        scenario.next_to(title, DOWN, buff=0.6)

        for line in scenario:
            self.play(Write(line))
            self.wait(0.3)

        # ========================================
        # DIFFERENT COMPOUNDING FREQUENCIES
        # ========================================
        frequencies = [
            ("Annually (n=1)", 1),
            ("Semi-annually (n=2)", 2),
            ("Quarterly (n=4)", 4),
            ("Monthly (n=12)", 12),
            ("Daily (n=365)", 365),
            ("Hourly (n=8760)", 8760),
            ("Continuously (n→∞)", np.inf),
        ]

        results = VGroup()

        for i, (desc, n) in enumerate(frequencies):
            if n == np.inf:
                value = E
                value_str = f"${E:.6f}"
            else:
                value = (1 + 1/n) ** n
                value_str = f"${value:.6f}"

            color = GREEN if n == np.inf else WHITE

            result_line = VGroup(
                OldTexText(desc, font_size=22, color=color),
                OldTexText(value_str, font_size=22, color=color),
            )
            result_line.arrange(RIGHT, buff=1.0)
            results.add(result_line)

        results.arrange(DOWN, buff=0.25, aligned_edge=LEFT)
        results.next_to(scenario, DOWN, buff=0.8)

        # Animate results appearing
        for result in results:
            self.play(FadeIn(result, shift=UP), run_time=0.5)
            self.wait(0.2)

        self.wait()

        # ========================================
        # CONTINUOUS COMPOUNDING
        # ========================================
        continuous = Tex(
            "\\text{Continuous: } A = Pe^{rt}",
            font_size=32,
            color=GREEN
        )
        continuous.to_edge(DOWN).shift(UP * 0.5)

        continuous_box = SurroundingRectangle(continuous, buff=0.2, color=GREEN, stroke_width=2)

        self.play(Write(continuous))
        self.play(ShowCreation(continuous_box))
        self.wait()

        # Explanation
        explanation = Tex(
            "P = \\text{principal}, \\, r = \\text{rate}, \\, t = \\text{time}",
            font_size=24,
            color=GREY_A
        )
        explanation.next_to(continuous, DOWN, buff=0.2)

        self.play(Write(explanation))
        self.wait(2)


class DerivativeProperty(Scene):
    """
    Scene 4: Show the unique property that d/dx[e^x] = e^x.

    This scene demonstrates why e^x is the most natural exponential:
    it's the only function that equals its own derivative.
    """

    def construct(self):
        # ========================================
        # TITLE
        # ========================================
        title = OldTexText("The Unique Property of e^x", font_size=42)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait()

        # ========================================
        # THE PROPERTY
        # ========================================
        property_text = OldTexText("Most important property:", font_size=28)
        property_text.next_to(title, DOWN, buff=0.6)

        self.play(Write(property_text))
        self.wait()

        main_property = Tex(
            "\\frac{d}{dx}\\left[e^x\\right] = e^x",
            font_size=48,
            color=GREEN
        )
        main_property.next_to(property_text, DOWN, buff=0.6)

        property_box = SurroundingRectangle(main_property, buff=0.3, color=GREEN, stroke_width=3)

        self.play(Write(main_property))
        self.play(ShowCreation(property_box))
        self.wait()

        # ========================================
        # VISUALIZATION
        # ========================================
        self.play(FadeOut(property_text))

        viz_text = OldTexText("Visualizing this property:", font_size=26)
        viz_text.next_to(title, DOWN, buff=0.4)

        self.play(Write(viz_text))
        self.wait()

        # Create axes
        axes = Axes(
            x_range=[-2, 2, 1],
            y_range=[0, 8, 2],
            width=8,
            height=4,
        )
        axes.shift(DOWN * 0.5)

        self.play(ShowCreation(axes))
        self.wait()

        # e^x graph
        exp_graph = axes.get_graph(
            lambda x: np.exp(x),
            color=BLUE,
            x_range=(-2, 2)
        )

        exp_label = Tex("f(x) = e^x", color=BLUE, font_size=28)
        exp_label.next_to(axes.c2p(1.5, np.exp(1.5)), UP, buff=0.2)

        self.play(ShowCreation(exp_graph), Write(exp_label))
        self.wait()

        # ========================================
        # SHOW SLOPE = HEIGHT
        # ========================================
        explanation = OldTexText(
            "At any point: slope = height",
            font_size=24,
            color=YELLOW
        )
        explanation.to_edge(DOWN).shift(UP * 1.5)

        self.play(FadeIn(explanation, shift=UP))
        self.wait()

        # Show tangent lines at several points
        x_points = [-1, 0, 1]

        for x_val in x_points:
            y_val = np.exp(x_val)
            slope = np.exp(x_val)  # Derivative = e^x

            point = axes.c2p(x_val, y_val)
            dot = Dot(point, color=YELLOW, radius=0.08)

            # Tangent line
            dx = 0.5
            p1 = axes.c2p(x_val - dx, y_val - slope * dx)
            p2 = axes.c2p(x_val + dx, y_val + slope * dx)
            tangent = Line(p1, p2, color=YELLOW, stroke_width=3)

            # Labels
            height_label = Tex(f"y = {y_val:.2f}", font_size=20, color=BLUE)
            height_label.next_to(dot, LEFT, buff=0.2)

            slope_label = Tex(f"\\text{{slope}} = {slope:.2f}", font_size=20, color=YELLOW)
            slope_label.next_to(dot, RIGHT, buff=0.2)

            self.play(FadeIn(dot, scale=0.5))
            self.play(ShowCreation(tangent))
            self.play(Write(height_label), Write(slope_label))
            self.wait(1.5)

            self.play(
                FadeOut(dot),
                FadeOut(tangent),
                FadeOut(height_label),
                FadeOut(slope_label)
            )

        # ========================================
        # COMPARISON WITH OTHER BASES
        # ========================================
        self.play(FadeOut(explanation), FadeOut(viz_text))

        comparison_title = OldTexText("Comparison with other bases:", font_size=26)
        comparison_title.next_to(title, DOWN, buff=0.4)

        self.play(Write(comparison_title))
        self.wait()

        comparison = VGroup(
            Tex("\\frac{d}{dx}[2^x] = (\\ln 2) \\cdot 2^x \\approx 0.693 \\cdot 2^x", font_size=24),
            Tex("\\frac{d}{dx}[e^x] = 1 \\cdot e^x = e^x", font_size=24, color=GREEN),
            Tex("\\frac{d}{dx}[10^x] = (\\ln 10) \\cdot 10^x \\approx 2.303 \\cdot 10^x", font_size=24),
        )
        comparison.arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        comparison.to_edge(DOWN).shift(UP * 0.3)

        for line in comparison:
            self.play(Write(line))
            self.wait(0.5)

        self.wait()

        # ========================================
        # WHY IT MATTERS
        # ========================================
        self.play(FadeOut(comparison), FadeOut(comparison_title), FadeOut(axes), FadeOut(exp_graph), FadeOut(exp_label))

        matters = VGroup(
            OldTexText("Why this matters:", font_size=32, color=YELLOW),
            OldTexText("• Simplest differential equation: y' = y", font_size=24),
            OldTexText("• Models natural growth/decay processes", font_size=24),
            OldTexText("• Appears in calculus, probability, physics", font_size=24),
            OldTexText("• Foundation of complex exponentials e^(ix)", font_size=24),
            OldTexText("• Key to understanding change over time", font_size=24),
        )
        matters.arrange(DOWN, buff=0.25, aligned_edge=LEFT)
        matters.next_to(title, DOWN, buff=0.6)

        for item in matters:
            self.play(FadeIn(item, shift=UP))
            self.wait(0.4)

        self.wait()

        # ========================================
        # FINAL FORMULA
        # ========================================
        self.play(FadeOut(matters))

        final = Tex(
            "e^x = \\sum_{n=0}^{\\infty} \\frac{x^n}{n!} = 1 + x + \\frac{x^2}{2!} + \\frac{x^3}{3!} + \\cdots",
            font_size=32,
            color=BLUE
        )
        final.move_to(ORIGIN)

        final_box = SurroundingRectangle(final, buff=0.3, color=BLUE, stroke_width=2)

        final_label = OldTexText("Taylor series for e^x:", font_size=28)
        final_label.next_to(final, UP, buff=0.5)

        self.play(Write(final_label))
        self.play(Write(final))
        self.play(ShowCreation(final_box))
        self.wait(2)


# ============================================================
# 5. SCENE SUMMARY AND EXECUTION ORDER
# ============================================================
#
# Scene 1 (DefineExponential):
#   - Introduces exponential functions a^x
#   - Compares different bases (2, e, 10)
#   - Poses the question: what makes e special?
#
# Scene 2 (NumberE):
#   - Shows e as limit of (1+1/n)^n
#   - Computes numerical approximations
#   - Reveals e ≈ 2.71828...
#
# Scene 3 (CompoundInterest):
#   - Connects e to compound interest
#   - Shows different compounding frequencies
#   - Derives continuous compounding formula A = Pe^(rt)
#
# Scene 4 (DerivativeProperty):
#   - Reveals the unique property: d/dx[e^x] = e^x
#   - Visualizes slope equals height
#   - Compares with other bases
#   - Shows Taylor series and applications

SCENE_ORDER = [
    DefineExponential,     # Part 1: Exponential functions
    NumberE,               # Part 2: Defining e through limits
    CompoundInterest,      # Part 3: e in compound interest
    DerivativeProperty,    # Part 4: The unique derivative property
]
