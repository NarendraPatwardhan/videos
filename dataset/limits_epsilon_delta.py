"""
Natural Group Name: Epsilon-Delta Limit Definition

Educational Objectives:
- To introduce the formal epsilon-delta definition of limits
- To build intuition for the logical structure of limit statements
- To visualize the "challenge-response" game between epsilon and delta
- To work through a concrete proof using the definition

Story Arc & Intent:
The animation demystifies the formal limit definition by framing it as a game:
given any challenge epsilon (how close to L), we can find a response delta
(how close to a) that works. This interactive perspective makes the quantifiers
and logic clear and memorable.

Narrative Flow:
- Hook/Opening: Review informal limit concept
- Development: Introduce the need for precise definition
- Build-up: Present epsilon-delta definition with visual interpretation
- Climax: Work through a complete proof for lim(x→2) x² = 4
- Resolution: Show how epsilon and delta interact geometrically
- Extension: Discuss the logical structure and why it matters

Technical Implementation Notes:
- Scene Classes: InformalLimit, EpsilonDelta, VisualProof, WorkingExample
- Key Visual Elements: Function graphs, epsilon/delta neighborhoods, bands
- Animation Techniques: Zooming, band highlighting, challenge-response animation
- Mathematical Concepts: Limits, formal logic, quantifiers, proofs

Dependency Chain:
All scenes are independent. They use Axes, ParametricCurve, Rectangle, and
Tex from manimlib. Utility functions handle epsilon-delta visualization.

Rendering Instructions:
To render these scenes, use the manim command-line tool:
- For a single scene: manimgl limits_epsilon_delta.py InformalLimit
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
# Axes configuration
X_RANGE = [0, 4, 1]
Y_RANGE = [0, 8, 2]

# Colors
FUNCTION_COLOR = BLUE
LIMIT_POINT_COLOR = RED
EPSILON_COLOR = YELLOW
DELTA_COLOR = GREEN
BAND_COLOR = PURPLE

# ============================================================
# 3. UTILITY FUNCTIONS
# ============================================================

def create_epsilon_band(axes, y_center, epsilon, x_range, color=EPSILON_COLOR):
    """
    Create horizontal band for epsilon neighborhood.

    Args:
        axes: Axes object
        y_center: Y-value at center (limit L)
        epsilon: Half-height of band
        x_range: X range for band
        color: Band color

    Returns:
        Rectangle representing band
    """
    # Get coordinates
    lower_left = axes.c2p(x_range[0], y_center - epsilon)
    upper_right = axes.c2p(x_range[1], y_center + epsilon)

    width = upper_right[0] - lower_left[0]
    height = upper_right[1] - lower_left[1]

    band = Rectangle(width=width, height=height)
    band.move_to(axes.c2p((x_range[0] + x_range[1])/2, y_center))
    band.set_fill(color, opacity=0.3)
    band.set_stroke(color, width=2)

    return band

def create_delta_band(axes, x_center, delta, y_range, color=DELTA_COLOR):
    """
    Create vertical band for delta neighborhood.

    Args:
        axes: Axes object
        x_center: X-value at center (point a)
        delta: Half-width of band
        y_range: Y range for band
        color: Band color

    Returns:
        Rectangle representing band
    """
    lower_left = axes.c2p(x_center - delta, y_range[0])
    upper_right = axes.c2p(x_center + delta, y_range[1])

    width = upper_right[0] - lower_left[0]
    height = upper_right[1] - lower_left[1]

    band = Rectangle(width=width, height=height)
    band.move_to(axes.c2p(x_center, (y_range[0] + y_range[1])/2))
    band.set_fill(color, opacity=0.3)
    band.set_stroke(color, width=2)

    return band

def find_delta_for_epsilon(func, a, L, epsilon):
    """
    For linear/quadratic functions, estimate delta for given epsilon.

    This is problem-specific. For f(x) = x², lim(x→2) = 4:
    We need |x² - 4| < ε when |x - 2| < δ
    |x² - 4| = |x - 2||x + 2|
    If |x - 2| < 1, then |x + 2| < 5
    So |x - 2| < ε/5 works

    Args:
        func: Function
        a: Point approaching
        L: Limit value
        epsilon: Given epsilon

    Returns:
        Suitable delta value
    """
    # For x², we use δ = min(1, ε/5)
    # This is specific to our example
    return min(1, epsilon / 5)

# ============================================================
# 4. BASE CLASSES AND HELPERS
# ============================================================
# No custom base classes needed

# ============================================================
# 5. SCENE IMPLEMENTATIONS
# ============================================================

class InformalLimit(InteractiveScene):
    """
    Part 1: Review informal limit concept.

    Narrative purpose:
        To remind viewers of the intuitive limit concept before
        introducing the formal definition.

    Mathematical content:
        Shows that as x approaches a, f(x) approaches L. Uses
        the example lim(x→2) x² = 4 with visual demonstration.

    Visual approach:
        Plot f(x) = x², show x approaching 2 from both sides,
        with f(x) approaching 4. Emphasize "getting arbitrarily close."
    """
    def construct(self):
        # ========================================
        # SETUP: Title
        # ========================================
        title = Text("What is a Limit?", font_size=48)
        title.to_edge(UP)

        self.play(FadeIn(title, shift=DOWN))
        self.wait()

        # ========================================
        # CREATE: Axes and function
        # ========================================
        axes = Axes(
            x_range=[0, 4, 1],
            y_range=[0, 8, 2],
            width=8,
            height=6,
        )
        axes.shift(0.5 * DOWN)

        x_label = Tex("x", font_size=32)
        x_label.next_to(axes.x_axis, RIGHT)
        y_label = Tex("y", font_size=32)
        y_label.next_to(axes.y_axis, UP)

        self.play(
            ShowCreation(axes),
            Write(x_label),
            Write(y_label)
        )
        self.wait()

        # ========================================
        # PLOT: f(x) = x²
        # ========================================
        func = lambda x: x**2
        graph = axes.get_graph(func, x_range=[0, 3.5], color=FUNCTION_COLOR, stroke_width=3)

        func_label = Tex("f(x) = x^2", font_size=36, color=FUNCTION_COLOR)
        func_label.next_to(axes, UP + RIGHT, buff=0.5)

        self.play(
            ShowCreation(graph),
            Write(func_label)
        )
        self.wait()

        # ========================================
        # SHOW: Limit point
        # ========================================
        a = 2
        L = 4

        # Point on graph
        limit_point = Dot(axes.c2p(a, L), radius=0.1, color=LIMIT_POINT_COLOR)

        # Dashed lines
        v_line = DashedLine(axes.c2p(a, 0), axes.c2p(a, L), color=LIMIT_POINT_COLOR)
        h_line = DashedLine(axes.c2p(0, L), axes.c2p(a, L), color=LIMIT_POINT_COLOR)

        # Labels
        a_label = Tex("x = 2", font_size=28, color=LIMIT_POINT_COLOR)
        a_label.next_to(axes.c2p(a, 0), DOWN, buff=0.2)

        L_label = Tex("y = 4", font_size=28, color=LIMIT_POINT_COLOR)
        L_label.next_to(axes.c2p(0, L), LEFT, buff=0.2)

        self.play(
            ShowCreation(v_line),
            ShowCreation(h_line),
            FadeIn(limit_point, scale=1.5),
            Write(a_label),
            Write(L_label)
        )
        self.wait()

        # ========================================
        # INFORMAL: Statement
        # ========================================
        informal_statement = Tex(
            R"\lim_{x \to 2} x^2 = 4",
            font_size=48,
            color=YELLOW
        )
        informal_statement.to_edge(DOWN, buff=1.5)

        self.play(Write(informal_statement))
        self.wait(2)

        # ========================================
        # EXPLANATION
        # ========================================
        explanation = Text(
            "As x gets closer to 2, x² gets closer to 4",
            font_size=28
        )
        explanation.next_to(informal_statement, DOWN, buff=0.3)

        self.play(Write(explanation))
        self.wait(2)

        # ========================================
        # QUESTION: How to make this precise?
        # ========================================
        question = Text(
            'But what does "closer" mean precisely?',
            font_size=32,
            color=RED
        )
        question.next_to(explanation, DOWN, buff=0.5)

        self.play(Write(question))
        self.wait(3)

        # ========================================
        # CLEANUP
        # ========================================
        self.play(FadeOut(*self.mobjects), run_time=1)
        self.wait()


class EpsilonDelta(InteractiveScene):
    """
    Part 2: Introduce epsilon-delta definition.

    Narrative purpose:
        To present the formal definition clearly, emphasizing the
        logical structure and the "challenge-response" interpretation.

    Mathematical content:
        States: lim(x→a) f(x) = L means
        ∀ε > 0, ∃δ > 0 such that |x - a| < δ ⇒ |f(x) - L| < ε

    Visual approach:
        Display the definition with careful highlighting of each part.
        Explain the quantifiers and the logical flow.
    """
    def construct(self):
        # ========================================
        # SETUP: Title
        # ========================================
        title = Text("The Epsilon-Delta Definition", font_size=48)
        title.to_edge(UP)

        self.play(FadeIn(title, shift=DOWN))
        self.wait()

        # ========================================
        # STATEMENT: The formal definition
        # ========================================
        definition = Tex(
            R"\lim_{x \to a} f(x) = L",
            font_size=44
        )
        definition.shift(1.5 * UP)

        self.play(Write(definition))
        self.wait()

        means_text = Text("means:", font_size=32)
        means_text.next_to(definition, DOWN, buff=0.5)

        self.play(Write(means_text))
        self.wait()

        # ========================================
        # FORMAL: Epsilon-delta statement
        # ========================================
        formal = Tex(
            R"\forall \varepsilon > 0, \, \exists \delta > 0 \text{ such that}",
            R"\quad 0 < |x - a| < \delta \implies |f(x) - L| < \varepsilon",
            font_size=32
        )
        formal.arrange(DOWN, buff=0.3)
        formal.next_to(means_text, DOWN, buff=0.7)

        self.play(
            LaggedStart(
                *[Write(part) for part in formal],
                lag_ratio=0.8
            ),
            run_time=3
        )
        self.wait(3)

        # ========================================
        # EXPLAIN: Each part
        # ========================================
        self.play(
            VGroup(definition, means_text, formal).animate.scale(0.7).to_corner(UL, buff=0.5)
        )

        explanation_title = Text("Breaking it down:", font_size=36, weight=BOLD)
        explanation_title.shift(1.5 * UP)

        self.play(Write(explanation_title))
        self.wait()

        explanations = VGroup(
            Text("∀ε > 0: For ANY distance ε from the limit L", font_size=26),
            Text("∃δ > 0: We can find a distance δ from a", font_size=26),
            Text("Such that: Whenever x is within δ of a...", font_size=26),
            Text("Then: f(x) is within ε of L", font_size=26),
        )
        explanations.arrange(DOWN, buff=0.4, aligned_edge=LEFT)
        explanations.next_to(explanation_title, DOWN, buff=0.7)

        # Color code
        explanations[0].set_color(EPSILON_COLOR)
        explanations[1].set_color(DELTA_COLOR)

        self.play(
            LaggedStart(
                *[FadeIn(exp, shift=RIGHT) for exp in explanations],
                lag_ratio=0.5
            ),
            run_time=4
        )
        self.wait(3)

        # ========================================
        # ANALOGY: Challenge-response game
        # ========================================
        self.play(FadeOut(explanations))

        analogy_title = Text("Think of it as a game:", font_size=32, weight=BOLD)
        analogy_title.next_to(explanation_title, DOWN, buff=0.7)

        self.play(Write(analogy_title))
        self.wait()

        game_steps = VGroup(
            Text("1. Challenger picks any ε > 0 (how close to L)", font_size=26, color=EPSILON_COLOR),
            Text("2. You must respond with δ > 0 (how close to a)", font_size=26, color=DELTA_COLOR),
            Text("3. If x is within δ of a, then f(x) is within ε of L", font_size=26),
            Text("4. You win if you can always respond successfully!", font_size=26, color=GREEN),
        )
        game_steps.arrange(DOWN, buff=0.4, aligned_edge=LEFT)
        game_steps.next_to(analogy_title, DOWN, buff=0.5)

        self.play(
            LaggedStart(
                *[FadeIn(step, shift=RIGHT) for step in game_steps],
                lag_ratio=0.4
            ),
            run_time=4
        )
        self.wait(4)

        # ========================================
        # CLEANUP
        # ========================================
        self.play(FadeOut(*self.mobjects), run_time=1)
        self.wait()


class VisualProof(InteractiveScene):
    """
    Part 3: Visualize epsilon-delta bands.

    Narrative purpose:
        To show geometrically what the epsilon-delta definition means
        by drawing the neighborhoods around a and L.

    Mathematical content:
        For lim(x→2) x² = 4, shows how given an ε-band around y=4,
        we can find a δ-band around x=2 such that the graph stays
        within the ε-band when x is in the δ-band.

    Visual approach:
        Draw horizontal ε-band, then show corresponding vertical δ-band.
        Animate for different values of ε to show it works for any ε.
    """
    def construct(self):
        # ========================================
        # SETUP: Title
        # ========================================
        title = Text("Visualizing Epsilon and Delta", font_size=48)
        title.to_edge(UP)

        self.play(FadeIn(title, shift=DOWN))
        self.wait()

        # ========================================
        # CREATE: Axes and function
        # ========================================
        axes = Axes(
            x_range=[0, 4, 1],
            y_range=[0, 8, 2],
            width=7,
            height=5.5,
        )
        axes.shift(0.5 * DOWN + 0.5 * RIGHT)

        func = lambda x: x**2
        graph = axes.get_graph(func, x_range=[0.5, 3.5], color=FUNCTION_COLOR, stroke_width=3)

        func_label = Tex("f(x) = x^2", font_size=28, color=FUNCTION_COLOR)
        func_label.to_corner(UR, buff=0.5)

        self.play(
            ShowCreation(axes),
            ShowCreation(graph),
            Write(func_label)
        )
        self.wait()

        # ========================================
        # SHOW: Limit point
        # ========================================
        a = 2
        L = 4

        point = Dot(axes.c2p(a, L), radius=0.08, color=LIMIT_POINT_COLOR)
        point_label = Tex("(2, 4)", font_size=24, color=LIMIT_POINT_COLOR)
        point_label.next_to(point, UR, buff=0.1)

        self.play(
            FadeIn(point, scale=1.5),
            Write(point_label)
        )
        self.wait()

        # ========================================
        # EPSILON: Horizontal band
        # ========================================
        epsilon = 1.5

        eps_band = create_epsilon_band(axes, L, epsilon, [0, 4], EPSILON_COLOR)

        eps_label = Tex(f"\\varepsilon = {epsilon}", font_size=28, color=EPSILON_COLOR)
        eps_label.to_corner(UL, buff=0.7)

        eps_lines = VGroup(
            DashedLine(axes.c2p(0, L + epsilon), axes.c2p(4, L + epsilon),
                      color=EPSILON_COLOR, stroke_width=2),
            DashedLine(axes.c2p(0, L - epsilon), axes.c2p(4, L - epsilon),
                      color=EPSILON_COLOR, stroke_width=2)
        )

        self.play(
            FadeIn(eps_band),
            ShowCreation(eps_lines),
            Write(eps_label)
        )
        self.wait(2)

        # ========================================
        # DELTA: Vertical band
        # ========================================
        # Find suitable delta
        delta = find_delta_for_epsilon(func, a, L, epsilon)

        delta_band = create_delta_band(axes, a, delta, [0, 8], DELTA_COLOR)

        delta_label = Tex(f"\\delta \\approx {delta:.2f}", font_size=28, color=DELTA_COLOR)
        delta_label.next_to(eps_label, DOWN, buff=0.3, aligned_edge=LEFT)

        delta_lines = VGroup(
            DashedLine(axes.c2p(a - delta, 0), axes.c2p(a - delta, 8),
                      color=DELTA_COLOR, stroke_width=2),
            DashedLine(axes.c2p(a + delta, 0), axes.c2p(a + delta, 8),
                      color=DELTA_COLOR, stroke_width=2)
        )

        self.play(
            FadeIn(delta_band),
            ShowCreation(delta_lines),
            Write(delta_label)
        )
        self.wait(2)

        # ========================================
        # OBSERVE: Graph stays in epsilon band
        # ========================================
        observation = Text(
            "When x is in δ-band, f(x) stays in ε-band!",
            font_size=26,
            color=GREEN
        )
        observation.to_edge(DOWN, buff=0.5)

        # Highlight the relevant portion of the graph
        restricted_graph = axes.get_graph(
            func,
            x_range=[a - delta, a + delta],
            color=GREEN,
            stroke_width=6
        )

        self.play(
            ShowCreation(restricted_graph),
            Write(observation)
        )
        self.wait(3)

        # ========================================
        # SHRINK: Try smaller epsilon
        # ========================================
        self.play(FadeOut(observation))

        shrink_text = Text(
            "Works for smaller ε too!",
            font_size=26,
            color=YELLOW
        )
        shrink_text.to_edge(DOWN, buff=0.5)

        self.play(Write(shrink_text))

        epsilon2 = 0.5
        delta2 = find_delta_for_epsilon(func, a, L, epsilon2)

        eps_band2 = create_epsilon_band(axes, L, epsilon2, [0, 4], EPSILON_COLOR)
        delta_band2 = create_delta_band(axes, a, delta2, [0, 8], DELTA_COLOR)

        eps_label2 = Tex(f"\\varepsilon = {epsilon2}", font_size=28, color=EPSILON_COLOR)
        eps_label2.move_to(eps_label)

        delta_label2 = Tex(f"\\delta \\approx {delta2:.2f}", font_size=28, color=DELTA_COLOR)
        delta_label2.move_to(delta_label)

        eps_lines2 = VGroup(
            DashedLine(axes.c2p(0, L + epsilon2), axes.c2p(4, L + epsilon2),
                      color=EPSILON_COLOR, stroke_width=2),
            DashedLine(axes.c2p(0, L - epsilon2), axes.c2p(4, L - epsilon2),
                      color=EPSILON_COLOR, stroke_width=2)
        )

        delta_lines2 = VGroup(
            DashedLine(axes.c2p(a - delta2, 0), axes.c2p(a - delta2, 8),
                      color=DELTA_COLOR, stroke_width=2),
            DashedLine(axes.c2p(a + delta2, 0), axes.c2p(a + delta2, 8),
                      color=DELTA_COLOR, stroke_width=2)
        )

        self.play(
            Transform(eps_band, eps_band2),
            Transform(delta_band, delta_band2),
            Transform(eps_label, eps_label2),
            Transform(delta_label, delta_label2),
            Transform(eps_lines, eps_lines2),
            Transform(delta_lines, delta_lines2),
            run_time=2
        )
        self.wait(3)

        # ========================================
        # CLEANUP
        # ========================================
        self.play(FadeOut(*self.mobjects), run_time=1)
        self.wait()


class WorkingExample(InteractiveScene):
    """
    Part 4: Work through complete algebraic proof.

    Narrative purpose:
        To show a rigorous proof using the epsilon-delta definition,
        demonstrating how to find delta in terms of epsilon algebraically.

    Mathematical content:
        Proves lim(x→2) x² = 4 by showing:
        Given ε > 0, choose δ = min(1, ε/5)
        Then |x - 2| < δ implies |x² - 4| < ε

    Visual approach:
        Step-by-step algebraic proof with clear highlighting and
        explanations of each step.
    """
    def construct(self):
        # ========================================
        # SETUP: Title
        # ========================================
        title = Text("Complete Proof Example", font_size=48)
        title.to_edge(UP)

        self.play(FadeIn(title, shift=DOWN))
        self.wait()

        # ========================================
        # STATEMENT: What we're proving
        # ========================================
        statement = Tex(
            R"\text{Prove: } \lim_{x \to 2} x^2 = 4",
            font_size=40,
            color=YELLOW
        )
        statement.shift(2 * UP)

        self.play(Write(statement))
        self.wait(2)

        # ========================================
        # PROOF: Step by step
        # ========================================
        proof_title = Text("Proof:", font_size=32, weight=BOLD)
        proof_title.next_to(statement, DOWN, buff=0.7, aligned_edge=LEFT)
        proof_title.shift(0.5 * LEFT)

        self.play(Write(proof_title))
        self.wait()

        # Step 1
        step1 = Tex(
            R"\text{Let } \varepsilon > 0 \text{ be given.}",
            font_size=28
        )
        step1.next_to(proof_title, DOWN, buff=0.4, aligned_edge=LEFT)

        self.play(Write(step1))
        self.wait()

        # Step 2
        step2 = Tex(
            R"\text{We need } |x^2 - 4| < \varepsilon \text{ when } |x - 2| < \delta.",
            font_size=28
        )
        step2.next_to(step1, DOWN, buff=0.3, aligned_edge=LEFT)

        self.play(Write(step2))
        self.wait()

        # Step 3
        step3 = Tex(
            R"|x^2 - 4| = |x - 2||x + 2|",
            font_size=28
        )
        step3.next_to(step2, DOWN, buff=0.4, aligned_edge=LEFT)

        self.play(Write(step3))
        self.wait()

        # Step 4
        step4 = Tex(
            R"\text{If } |x - 2| < 1, \text{ then } 1 < x < 3, \text{ so } 3 < x + 2 < 5.",
            font_size=26
        )
        step4.next_to(step3, DOWN, buff=0.3, aligned_edge=LEFT)

        self.play(Write(step4))
        self.wait(2)

        # Step 5
        step5 = Tex(
            R"\text{Thus } |x + 2| < 5 \text{ when } |x - 2| < 1.",
            font_size=26
        )
        step5.next_to(step4, DOWN, buff=0.3, aligned_edge=LEFT)

        self.play(Write(step5))
        self.wait()

        # Step 6
        step6 = Tex(
            R"|x^2 - 4| = |x - 2||x + 2| < 5|x - 2|",
            font_size=28
        )
        step6.next_to(step5, DOWN, buff=0.4, aligned_edge=LEFT)

        self.play(Write(step6))
        self.wait()

        # Step 7
        step7 = Tex(
            R"\text{So if } |x - 2| < \frac{\varepsilon}{5}, \text{ then } |x^2 - 4| < \varepsilon.",
            font_size=28
        )
        step7.next_to(step6, DOWN, buff=0.3, aligned_edge=LEFT)

        self.play(Write(step7))
        self.wait(2)

        # Step 8: Conclusion
        step8 = Tex(
            R"\text{Choose } \delta = \min\left(1, \frac{\varepsilon}{5}\right). \quad \square",
            font_size=30,
            color=GREEN
        )
        step8.next_to(step7, DOWN, buff=0.5, aligned_edge=LEFT)

        box = SurroundingRectangle(step8, buff=0.2, color=GREEN, stroke_width=2)

        self.play(
            Write(step8),
            ShowCreation(box)
        )
        self.wait(3)

        # ========================================
        # SUMMARY
        # ========================================
        self.play(FadeOut(*self.mobjects[2:]))  # Keep title and statement

        summary_title = Text("Key Insight:", font_size=36, weight=BOLD)
        summary_title.shift(0.5 * UP)

        self.play(Write(summary_title))
        self.wait()

        summary = VGroup(
            Text("We factored |x² - 4| to relate it to |x - 2|", font_size=26),
            Text("We bounded |x + 2| by assuming |x - 2| < 1", font_size=26),
            Text("This gave us δ = min(1, ε/5)", font_size=26),
            Text("The min ensures both conditions are satisfied", font_size=26),
        )
        summary.arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        summary.next_to(summary_title, DOWN, buff=0.5)

        self.play(
            LaggedStart(
                *[FadeIn(line, shift=RIGHT) for line in summary],
                lag_ratio=0.4
            ),
            run_time=4
        )
        self.wait(4)

        # ========================================
        # FINAL MESSAGE
        # ========================================
        self.play(FadeOut(*self.mobjects))

        final = Text(
            "The ε-δ definition makes limits\nrigorous and precise!",
            font_size=40,
            color=YELLOW,
            weight=BOLD
        )
        final.move_to(ORIGIN)

        self.play(FadeIn(final, scale=1.2))
        self.wait(4)

        self.play(FadeOut(final))
        self.wait()


# ============================================================
# 6. SCENE EXECUTION ORDER
# ============================================================
# The order of scenes that tells the story.
#
# Scene 1 (InformalLimit):
#   - Reviews intuitive limit concept
#   - Shows lim(x→2) x² = 4 informally
#   - Poses precision question
#
# Scene 2 (EpsilonDelta):
#   - States formal ε-δ definition
#   - Explains quantifier structure
#   - Presents challenge-response game analogy
#
# Scene 3 (VisualProof):
#   - Visualizes ε and δ neighborhoods
#   - Shows bands on graph
#   - Demonstrates for multiple ε values
#
# Scene 4 (WorkingExample):
#   - Complete algebraic proof
#   - Shows how to find δ given ε
#   - Explains key techniques

SCENE_ORDER = [
    InformalLimit,         # Part 1: Intuition
    EpsilonDelta,          # Part 2: Definition
    VisualProof,           # Part 3: Visualization
    WorkingExample,        # Part 4: Rigorous proof
]
