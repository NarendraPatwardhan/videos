"""
Natural Group Name: Basel Problem - Sum of Reciprocal Squares

Educational Objectives:
- To introduce the Basel problem: sum of 1/n² equals π²/6
- To show partial sums converging to the limit
- To build intuition for why π appears in this series
- To demonstrate one of mathematics' most beautiful results

Story Arc & Intent:
The animation presents one of mathematics' most surprising results: the sum
of reciprocals of perfect squares equals exactly π²/6. By showing the convergence
and providing geometric intuition, we reveal why this seemingly arbitrary sum
produces such an elegant answer involving π.

Narrative Flow:
- Hook/Opening: Pose the series summation question
- Development: Show partial sums converging slowly
- Build-up: Reveal the surprising limit π²/6
- Climax: Provide geometric/visual intuition for why π appears
- Resolution: Show Euler's connection to the sine function
- Extension: Mention generalizations (Riemann zeta function)

Technical Implementation Notes:
- Scene Classes: IntroduceSeries, PartialSums, SurprisingResult, VisualIntuition
- Key Visual Elements: Series terms, partial sum graphs, π visualization
- Animation Techniques: Series summation, convergence animation, geometric diagrams
- Mathematical Concepts: Infinite series, convergence, Fourier analysis

Dependency Chain:
All scenes are independent. They use Axes, ParametricCurve, and Tex from
manimlib. Utility functions handle series calculation and visualization.

Rendering Instructions:
To render these scenes, use the manim command-line tool:
- For a single scene: manimgl basel_problem.py IntroduceSeries
- For all scenes in sequence: iterate through SCENE_ORDER
"""

# ============================================================
# 1. IMPORTS
# ============================================================
from manimlib import *
import numpy as np

# ============================================================
# 2. CONFIGURATION AND CONSTANTS
# ============================================================
# Series configuration
MAX_TERMS_DISPLAY = 10
MAX_TERMS_COMPUTE = 1000

# Colors
SERIES_COLOR = BLUE
SUM_COLOR = GREEN
LIMIT_COLOR = YELLOW
PI_COLOR = RED

# Known value
BASEL_SUM = np.pi**2 / 6

# ============================================================
# 3. UTILITY FUNCTIONS
# ============================================================

def basel_partial_sum(n):
    """
    Calculate nth partial sum of Basel series.

    Args:
        n: Number of terms

    Returns:
        Sum of 1/1² + 1/2² + ... + 1/n²
    """
    return sum(1/k**2 for k in range(1, n+1))

def basel_term(n):
    """
    Get nth term of Basel series.

    Args:
        n: Term index (starting from 1)

    Returns:
        1/n²
    """
    return 1 / n**2

def format_fraction(n):
    """Format term as fraction for display."""
    return f"\\frac{{1}}{{{n}^2}}"

# ============================================================
# 4. BASE CLASSES AND HELPERS
# ============================================================
# No custom base classes needed

# ============================================================
# 5. SCENE IMPLEMENTATIONS
# ============================================================

class IntroduceSeries(InteractiveScene):
    """
    Part 1: Introduce the Basel problem.

    Narrative purpose:
        To pose the famous question: what is the sum of the reciprocals
        of the perfect squares?

    Mathematical content:
        Presents the series 1/1² + 1/2² + 1/3² + 1/4² + ...
        and asks for its sum.

    Visual approach:
        Display the series with first several terms explicitly shown,
        then pose the summation question as a mathematical mystery.
    """
    def construct(self):
        # ========================================
        # SETUP: Title
        # ========================================
        title = OldTexText("The Basel Problem", font_size=48)
        title.to_edge(UP)

        self.play(FadeIn(title, shift=DOWN))
        self.wait()

        # ========================================
        # INTRODUCE: The series
        # ========================================
        series_title = OldTexText("Sum of reciprocal squares:", font_size=36)
        series_title.shift(1.5 * UP)

        self.play(Write(series_title))
        self.wait()

        # ========================================
        # SHOW: First few terms
        # ========================================
        terms = Tex(
            R"1 + \frac{1}{4} + \frac{1}{9} + \frac{1}{16} + \frac{1}{25} + \cdots",
            font_size=48,
            color=SERIES_COLOR
        )
        terms.next_to(series_title, DOWN, buff=0.7)

        self.play(Write(terms))
        self.wait(2)

        # Alternative notation
        sigma_notation = Tex(
            R"\sum_{n=1}^{\infty} \frac{1}{n^2} = \, ?",
            font_size=48,
            color=SERIES_COLOR
        )
        sigma_notation.next_to(terms, DOWN, buff=0.8)

        self.play(Write(sigma_notation))
        self.wait(2)

        # ========================================
        # HISTORY: Famous problem
        # ========================================
        history = VGroup(
            OldTexText("• Posed in 1644", font_size=28),
            OldTexText("• Resisted many mathematicians", font_size=28),
            OldTexText("• Solved by Euler in 1734", font_size=28, color=YELLOW),
        )
        history.arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        history.to_edge(DOWN, buff=1)

        self.play(
            LaggedStart(
                *[FadeIn(line, shift=RIGHT) for line in history],
                lag_ratio=0.5
            )
        )
        self.wait(3)

        # ========================================
        # QUESTION: What's the sum?
        # ========================================
        question = OldTexText(
            "What does this sum equal?",
            font_size=36,
            color=YELLOW,
            weight=BOLD
        )
        question.next_to(history, UP, buff=0.7)

        self.play(Write(question))
        self.wait(3)

        # ========================================
        # CLEANUP
        # ========================================
        self.play(FadeOut(*self.mobjects), run_time=1)
        self.wait()


class PartialSums(InteractiveScene):
    """
    Part 2: Show partial sums converging.

    Narrative purpose:
        To demonstrate that the series converges by showing partial
        sums approaching a limit, building suspense for the exact value.

    Mathematical content:
        Computes S_n = sum from k=1 to n of 1/k² for increasing n,
        showing convergence to approximately 1.645...

    Visual approach:
        Plot partial sums as points or as a graph, showing them
        approaching a horizontal asymptote near 1.645.
    """
    def construct(self):
        # ========================================
        # SETUP: Title
        # ========================================
        title = OldTexText("Partial Sums", font_size=48)
        title.to_edge(UP)

        self.play(FadeIn(title, shift=DOWN))
        self.wait()

        # ========================================
        # CREATE: Table of partial sums
        # ========================================
        table_title = OldTexText("Computing partial sums:", font_size=32)
        table_title.shift(2 * UP + 3 * LEFT)

        self.play(Write(table_title))
        self.wait()

        # Calculate several partial sums
        n_values = [1, 2, 3, 4, 5, 10, 50, 100, 1000]
        partial_sums = [basel_partial_sum(n) for n in n_values]

        # Create table
        table_entries = []
        for i, (n, s) in enumerate(zip(n_values, partial_sums)):
            entry = VGroup(
                Tex(f"S_{{{n}}} =", font_size=24),
                Tex(f"{s:.6f}", font_size=24, color=SUM_COLOR)
            )
            entry.arrange(RIGHT, buff=0.3)
            table_entries.append(entry)

        table = VGroup(*table_entries)
        table.arrange(DOWN, buff=0.25, aligned_edge=LEFT)
        table.next_to(table_title, DOWN, buff=0.5, aligned_edge=LEFT)

        self.play(
            LaggedStart(
                *[FadeIn(entry, shift=DOWN) for entry in table_entries],
                lag_ratio=0.3
            ),
            run_time=5
        )
        self.wait(2)

        # ========================================
        # OBSERVATION
        # ========================================
        observation = OldTexText(
            "Converging to approximately 1.6449...",
            font_size=28,
            color=YELLOW
        )
        observation.next_to(table, DOWN, buff=0.7)

        self.play(Write(observation))
        self.wait(2)

        # ========================================
        # GRAPH: Visual convergence
        # ========================================
        self.play(
            FadeOut(table_title),
            FadeOut(table),
            FadeOut(observation)
        )

        # Create axes
        axes = Axes(
            x_range=[0, 100, 20],
            y_range=[1, 1.7, 0.2],
            width=9,
            height=5,
        )
        axes.shift(0.5 * DOWN)

        x_label = OldTexText("n (number of terms)", font_size=24)
        x_label.next_to(axes.x_axis, DOWN, buff=0.3)

        y_label = Tex("S_n", font_size=28)
        y_label.next_to(axes.y_axis, LEFT, buff=0.3)

        self.play(
            ShowCreation(axes),
            Write(x_label),
            Write(y_label)
        )
        self.wait()

        # Plot partial sums
        n_range = list(range(1, 101))
        sum_values = [basel_partial_sum(n) for n in n_range]
        points = [axes.c2p(n, s) for n, s in zip(n_range, sum_values)]

        dots = VGroup(*[
            Dot(point, radius=0.03, color=SUM_COLOR)
            for point in points[::5]  # Show every 5th point
        ])

        # Connect with curve
        curve = VMobject()
        curve.set_points_smoothly(points)
        curve.set_stroke(SERIES_COLOR, width=3)

        self.play(ShowCreation(curve), run_time=3)
        self.play(FadeIn(dots))
        self.wait()

        # Show limit line
        limit_line = DashedLine(
            axes.c2p(0, BASEL_SUM),
            axes.c2p(100, BASEL_SUM),
            color=LIMIT_COLOR,
            stroke_width=3
        )

        limit_label = Tex(
            R"\text{Limit} \approx 1.6449",
            font_size=28,
            color=LIMIT_COLOR
        )
        limit_label.next_to(limit_line, RIGHT, buff=0.2)

        self.play(
            ShowCreation(limit_line),
            Write(limit_label)
        )
        self.wait(3)

        # ========================================
        # CLEANUP
        # ========================================
        self.play(FadeOut(*self.mobjects), run_time=1)
        self.wait()


class SurprisingResult(InteractiveScene):
    """
    Part 3: Reveal the exact answer π²/6.

    Narrative purpose:
        To dramatically reveal Euler's surprising discovery that the
        sum equals exactly π²/6, making the connection to π.

    Mathematical content:
        States Euler's result: sum from n=1 to infinity of 1/n² = π²/6.
        Verifies numerically that π²/6 ≈ 1.6449...

    Visual approach:
        Build suspense, then reveal the formula with dramatic effect.
        Show numerical verification. Emphasize the surprising appearance of π.
    """
    def construct(self):
        # ========================================
        # SETUP: Title
        # ========================================
        title = OldTexText("Euler's Remarkable Discovery", font_size=48)
        title.to_edge(UP)

        self.play(FadeIn(title, shift=DOWN))
        self.wait()

        # ========================================
        # BUILD: Suspense
        # ========================================
        question = Tex(
            R"\sum_{n=1}^{\infty} \frac{1}{n^2} = \, ?",
            font_size=56,
            color=SERIES_COLOR
        )
        question.shift(0.5 * UP)

        self.play(Write(question))
        self.wait(2)

        # ========================================
        # REVEAL: The answer
        # ========================================
        answer = Tex(
            R"= \frac{\pi^2}{6}",
            font_size=72,
            color=PI_COLOR
        )
        answer.next_to(question, RIGHT, buff=0.5)

        box = SurroundingRectangle(answer, buff=0.4, color=PI_COLOR, stroke_width=4)

        self.play(
            Write(answer),
            ShowCreation(box),
            run_time=2
        )
        self.wait(2)

        # Flash effect
        self.play(
            Flash(answer, color=YELLOW, line_length=0.3, flash_radius=1.5, run_time=1.5)
        )
        self.wait()

        # ========================================
        # VERIFY: Numerical check
        # ========================================
        verification = Tex(
            R"\frac{\pi^2}{6} \approx 1.6449340668...",
            font_size=36,
            color=YELLOW
        )
        verification.next_to(question, DOWN, buff=1.2)

        checkmark = Tex(R"\checkmark", font_size=60, color=GREEN)
        checkmark.next_to(verification, RIGHT, buff=0.5)

        self.play(
            Write(verification),
            FadeIn(checkmark, scale=2)
        )
        self.wait(3)

        # ========================================
        # SURPRISE: Why π?
        # ========================================
        surprise = OldTexText(
            "But why does π appear in a sum of fractions?!",
            font_size=32,
            color=YELLOW,
            weight=BOLD
        )
        surprise.to_edge(DOWN, buff=1)

        self.play(Write(surprise))
        self.wait(4)

        # ========================================
        # CLEANUP
        # ========================================
        self.play(FadeOut(*self.mobjects), run_time=1)
        self.wait()


class VisualIntuition(InteractiveScene):
    """
    Part 4: Provide geometric intuition and Euler's proof idea.

    Narrative purpose:
        To give some insight into why π appears, connecting to Fourier
        analysis and the sine function's infinite product.

    Mathematical content:
        Mentions Euler's approach via sin(x)/x infinite product.
        Discusses connection to Fourier series. Shows the Riemann zeta
        function generalization.

    Visual approach:
        Show key proof ideas visually without full rigor. Emphasize
        the beauty of the connection. List generalizations.
    """
    def construct(self):
        # ========================================
        # SETUP: Title
        # ========================================
        title = OldTexText("Why Does π Appear?", font_size=48)
        title.to_edge(UP)

        self.play(FadeIn(title, shift=DOWN))
        self.wait()

        # ========================================
        # EULER'S APPROACH: Via sine function
        # ========================================
        approach_title = OldTexText("Euler's Brilliant Insight:", font_size=36, weight=BOLD)
        approach_title.shift(1.5 * UP)

        self.play(Write(approach_title))
        self.wait()

        # Show sine function expansion
        sine_expansion = Tex(
            R"\frac{\sin x}{x} = 1 - \frac{x^2}{3!} + \frac{x^4}{5!} - \cdots",
            font_size=32
        )
        sine_expansion.next_to(approach_title, DOWN, buff=0.7)

        self.play(Write(sine_expansion))
        self.wait(2)

        # Infinite product
        infinite_product = Tex(
            R"\frac{\sin x}{x} = \left(1 - \frac{x^2}{\pi^2}\right)"
            R"\left(1 - \frac{x^2}{4\pi^2}\right)"
            R"\left(1 - \frac{x^2}{9\pi^2}\right) \cdots",
            font_size=28
        )
        infinite_product.next_to(sine_expansion, DOWN, buff=0.7)

        product_label = OldTexText(
            "Infinite product (roots at ±nπ)",
            font_size=24,
            color=GREY_A
        )
        product_label.next_to(infinite_product, DOWN, buff=0.3)

        self.play(
            Write(infinite_product),
            Write(product_label)
        )
        self.wait(3)

        # ========================================
        # KEY STEP: Compare coefficients
        # ========================================
        self.play(
            FadeOut(sine_expansion),
            FadeOut(infinite_product),
            FadeOut(product_label)
        )

        key_idea = OldTexText("Key: Compare x² coefficients!", font_size=32, color=YELLOW)
        key_idea.next_to(approach_title, DOWN, buff=0.7)

        self.play(Write(key_idea))
        self.wait()

        # From Taylor series
        taylor_coef = Tex(
            R"\text{Taylor: } -\frac{1}{6}",
            font_size=32
        )
        taylor_coef.next_to(key_idea, DOWN, buff=0.7).shift(2 * LEFT)

        # From product
        product_coef = Tex(
            R"\text{Product: } -\frac{1}{\pi^2}\left(1 + \frac{1}{4} + \frac{1}{9} + \cdots\right)",
            font_size=28
        )
        product_coef.next_to(taylor_coef, DOWN, buff=0.5, aligned_edge=LEFT)

        self.play(
            Write(taylor_coef),
            Write(product_coef)
        )
        self.wait(3)

        # Conclusion
        conclusion = Tex(
            R"\Rightarrow \quad \sum_{n=1}^{\infty} \frac{1}{n^2} = \frac{\pi^2}{6}",
            font_size=36,
            color=GREEN
        )
        conclusion.next_to(product_coef, DOWN, buff=0.8)

        self.play(Write(conclusion))
        self.wait(3)

        # ========================================
        # GENERALIZATIONS
        # ========================================
        self.play(FadeOut(*self.mobjects[2:]))  # Keep title and approach_title

        gen_title = OldTexText("Generalizations:", font_size=36, weight=BOLD)
        gen_title.move_to(approach_title)

        self.play(Transform(approach_title, gen_title))
        self.wait()

        generalizations = VGroup(
            Tex(R"\zeta(s) = \sum_{n=1}^{\infty} \frac{1}{n^s} \quad \text{(Riemann zeta function)}",
                font_size=30),
            Tex(R"\zeta(2) = \frac{\pi^2}{6} \approx 1.645", font_size=28),
            Tex(R"\zeta(4) = \frac{\pi^4}{90} \approx 1.082", font_size=28),
            Tex(R"\zeta(6) = \frac{\pi^6}{945} \approx 1.017", font_size=28),
            OldTexText("All even integers have closed forms involving π!", font_size=26, color=YELLOW),
            OldTexText("Odd integers (except 1) remain mysterious...", font_size=26, color=RED),
        )
        generalizations.arrange(DOWN, buff=0.4, aligned_edge=LEFT)
        generalizations.next_to(approach_title, DOWN, buff=0.8)

        self.play(
            LaggedStart(
                *[FadeIn(gen, shift=RIGHT) for gen in generalizations],
                lag_ratio=0.4
            ),
            run_time=6
        )
        self.wait(4)

        # ========================================
        # FINAL MESSAGE
        # ========================================
        self.play(FadeOut(*self.mobjects))

        final = VGroup(
            OldTexText("The Basel Problem:", font_size=36, weight=BOLD),
            Tex(R"\sum_{n=1}^{\infty} \frac{1}{n^2} = \frac{\pi^2}{6}", font_size=48, color=PI_COLOR),
            OldTexText("One of mathematics' most beautiful surprises!", font_size=32, color=YELLOW),
        )
        final.arrange(DOWN, buff=0.5)
        final.move_to(ORIGIN)

        self.play(
            LaggedStart(
                *[FadeIn(line, scale=1.2) for line in final],
                lag_ratio=0.5
            ),
            run_time=3
        )
        self.wait(5)

        self.play(FadeOut(final))
        self.wait()


# ============================================================
# 6. SCENE EXECUTION ORDER
# ============================================================
# The order of scenes that tells the story.
#
# Scene 1 (IntroduceSeries):
#   - Introduces the Basel problem
#   - Shows the series notation
#   - Provides historical context
#
# Scene 2 (PartialSums):
#   - Computes partial sums
#   - Shows convergence graphically
#   - Reveals approximate limit 1.6449...
#
# Scene 3 (SurprisingResult):
#   - Dramatically reveals π²/6
#   - Verifies numerically
#   - Emphasizes surprising appearance of π
#
# Scene 4 (VisualIntuition):
#   - Sketches Euler's proof via sin(x)/x
#   - Explains why π appears
#   - Discusses generalizations (zeta function)
#   - Celebrates the beauty of the result

SCENE_ORDER = [
    IntroduceSeries,       # Part 1: The problem
    PartialSums,           # Part 2: Convergence
    SurprisingResult,      # Part 3: The answer
    VisualIntuition,       # Part 4: The insight
]
