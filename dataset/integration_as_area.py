"""
Natural Group Name: Integration as Area Under a Curve

Educational Objectives:
- To visualize integration as computing the area under a curve
- To demonstrate Riemann sums as approximations to the integral
- To show how increasing rectangles improves the approximation
- To connect to the Fundamental Theorem of Calculus

Story Arc & Intent:
The animation reveals integration through visual area approximation: rectangular
strips (Riemann sums) progressively fill the region under a curve, and as the
number of rectangles increases, the approximation becomes exact. This makes the
abstract integral concrete and geometric.

Narrative Flow:
- Hook/Opening: The problem of finding area under a curved boundary
- Development: Approximate with rectangles (Riemann sums)
- Build-up: Increase the number of rectangles for better approximations
- Climax: As n → ∞, the sum approaches the exact integral
- Resolution: Connect to the Fundamental Theorem and antiderivatives

Technical Implementation Notes:
- Scene Classes: AreaProblem, RiemannSums, IncreasingRectangles, FundamentalTheorem
- Key Visual Elements: Curves, rectangles, area shading, limit notation
- Animation Techniques: Rectangle creation, progressive refinement, area highlighting
- Mathematical Concepts: Riemann sums, definite integrals, limits, FTC

Dependency Chain:
All scenes use basic manimlib components: Axes, graphs, Rectangle, Text, Tex.
No custom utilities required.

Rendering Instructions:
To render these scenes, use the manim command-line tool:
- For a single scene: manimgl integration_as_area.py AreaProblem
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
# - BLUE: The function curve
# - YELLOW: Rectangles (Riemann sum)
# - GREEN: Filled area / exact integral
# - RED: Boundaries (a and b)
# - WHITE: Axes and grid
# - GREY_A: De-emphasized elements
#
# Key Manim Constants Used:
# - UP, DOWN, LEFT, RIGHT: Direction vectors
# - ORIGIN: Center point
# - PI: π for mathematical functions
# - DEGREES: Angle conversion

# Axes configuration
AXES_CONFIG = {
    "x_range": (0, 4, 1),
    "y_range": (0, 3, 1),
    "width": 10,
    "height": 6,
}

# Integration bounds
A_BOUND = 0.5
B_BOUND = 3.5

# Example function: f(x) = 1 + 0.5*sin(2x)
def example_function(x):
    """Example function for integration."""
    return 1 + 0.5 * np.sin(2 * x)

def example_antiderivative(x):
    """Antiderivative of example function."""
    return x - 0.25 * np.cos(2 * x)

# ============================================================
# 3. UTILITY FUNCTIONS
# ============================================================

def get_riemann_rectangles(axes, func, x_min, x_max, n, stroke_width=1, stroke_color=WHITE, fill_opacity=0.7, color=YELLOW):
    """
    Create Riemann sum rectangles for a function.

    Args:
        axes: Axes object
        func: Function to integrate
        x_min: Left bound
        x_max: Right bound
        n: Number of rectangles
        stroke_width: Width of rectangle borders
        stroke_color: Color of rectangle borders
        fill_opacity: Opacity of fill
        color: Fill color

    Returns:
        VGroup of Rectangle mobjects
    """
    rectangles = VGroup()
    dx = (x_max - x_min) / n

    for i in range(n):
        x_left = x_min + i * dx
        x_right = x_left + dx
        x_mid = (x_left + x_right) / 2

        # Use midpoint rule for height
        height = func(x_mid)

        # Create rectangle
        rect = Rectangle(
            width=axes.x_axis.unit_size * dx,
            height=axes.y_axis.unit_size * height,
            stroke_width=stroke_width,
            stroke_color=stroke_color,
            fill_color=color,
            fill_opacity=fill_opacity
        )

        # Position rectangle
        bottom_left = axes.c2p(x_left, 0)
        rect.align_to(bottom_left, DL)

        rectangles.add(rect)

    return rectangles

def calculate_riemann_sum(func, x_min, x_max, n):
    """
    Calculate the Riemann sum value.

    Args:
        func: Function to integrate
        x_min: Left bound
        x_max: Right bound
        n: Number of rectangles

    Returns:
        Approximate integral value
    """
    dx = (x_max - x_min) / n
    total = 0

    for i in range(n):
        x_mid = x_min + (i + 0.5) * dx
        total += func(x_mid) * dx

    return total

def calculate_exact_integral(antiderivative, a, b):
    """
    Calculate exact integral using antiderivative.

    Args:
        antiderivative: Antiderivative function
        a: Lower bound
        b: Upper bound

    Returns:
        Exact integral value
    """
    return antiderivative(b) - antiderivative(a)

# ============================================================
# 4. BASE CLASSES AND HELPERS
# ============================================================
# No custom base classes needed

# ============================================================
# 5. SCENE IMPLEMENTATIONS
# ============================================================

class AreaProblem(InteractiveScene):
    """
    Part 1: Introduce the problem of finding area under a curve.

    Narrative purpose:
        To establish the fundamental question: how do we find the area
        under a curve between two bounds? This motivates integration.

    Mathematical content:
        Unlike simple shapes, curved regions don't have elementary area formulas.
        We need a systematic method to compute such areas.

    Visual approach:
        Show a smooth curve with shaded region underneath between bounds a and b,
        posing the question of how to calculate this area.
    """
    def construct(self):
        # ========================================
        # SETUP: Title
        # ========================================
        title = OldTexText("Area Under a Curve", font_size=48)
        title.to_edge(UP)

        self.play(FadeIn(title, shift=DOWN))
        self.wait()

        # ========================================
        # CREATE: Axes and function
        # ========================================
        axes = Axes(**AXES_CONFIG)
        axes.add_coordinates()

        self.play(ShowCreation(axes), run_time=1.5)
        self.wait()

        # Function graph
        graph = axes.get_graph(
            example_function,
            x_range=(AXES_CONFIG["x_range"][0], AXES_CONFIG["x_range"][1]),
            color=BLUE
        )

        func_label = Tex("y = f(x)", font_size=36, color=BLUE)
        func_label.next_to(graph.get_end(), UP, buff=0.2)

        self.play(ShowCreation(graph), run_time=2)
        self.play(FadeIn(func_label, shift=DOWN))
        self.wait()

        # ========================================
        # MARK: Integration bounds
        # ========================================
        # Vertical lines at a and b
        line_a = DashedLine(
            axes.c2p(A_BOUND, 0),
            axes.c2p(A_BOUND, example_function(A_BOUND)),
            color=RED,
            stroke_width=3
        )

        line_b = DashedLine(
            axes.c2p(B_BOUND, 0),
            axes.c2p(B_BOUND, example_function(B_BOUND)),
            color=RED,
            stroke_width=3
        )

        label_a = Tex("a", font_size=36, color=RED)
        label_a.next_to(axes.c2p(A_BOUND, 0), DOWN, buff=0.2)

        label_b = Tex("b", font_size=36, color=RED)
        label_b.next_to(axes.c2p(B_BOUND, 0), DOWN, buff=0.2)

        self.play(
            ShowCreation(line_a),
            ShowCreation(line_b)
        )
        self.play(
            FadeIn(label_a, shift=UP),
            FadeIn(label_b, shift=UP)
        )
        self.wait()

        # ========================================
        # SHADE: The region
        # ========================================
        area = axes.get_riemann_rectangles(
            graph,
            x_range=(A_BOUND, B_BOUND),
            dx=0.01,
            stroke_width=0,
            fill_opacity=0.5,
            color=GREEN
        )

        area_label = Tex("\\text{Area} = \\, ?", font_size=42, color=GREEN)
        area_label.move_to(axes.c2p(2, 0.5))

        self.play(FadeIn(area), run_time=1.5)
        self.play(FadeIn(area_label, scale=1.3))
        self.wait()

        # ========================================
        # QUESTION: How to calculate?
        # ========================================
        question = OldTexText(
            "How do we calculate this area?",
            font_size=36,
            color=YELLOW
        )
        question.to_edge(DOWN, buff=0.5)

        self.play(FadeIn(question, shift=UP))
        self.wait(2)


class RiemannSums(InteractiveScene):
    """
    Part 2: Introduce Riemann sums as rectangular approximations.

    Narrative purpose:
        To present the key insight: approximate the curved area with rectangles,
        which have known area formulas.

    Mathematical content:
        Divide [a,b] into n subintervals, create rectangles with width Δx
        and height f(x_i), sum the areas: Σ f(x_i)Δx.

    Visual approach:
        Show a moderate number of rectangles (e.g., n=6) approximating the area,
        clearly showing that some area is missed and some is over-counted.
    """
    def construct(self):
        # ========================================
        # SETUP: Title
        # ========================================
        title = OldTexText("Approximation with Rectangles", font_size=48)
        title.to_edge(UP)

        self.add(title)

        # ========================================
        # CREATE: Axes and function
        # ========================================
        axes = Axes(**AXES_CONFIG)
        axes.add_coordinates()

        graph = axes.get_graph(
            example_function,
            x_range=(AXES_CONFIG["x_range"][0], AXES_CONFIG["x_range"][1]),
            color=BLUE
        )

        self.add(axes, graph)

        # ========================================
        # CREATE: Riemann rectangles (n=6)
        # ========================================
        n_rects = 6
        rectangles = get_riemann_rectangles(
            axes,
            example_function,
            A_BOUND,
            B_BOUND,
            n_rects,
            color=YELLOW,
            fill_opacity=0.6
        )

        self.play(LaggedStart([DrawBorderThenFill(rect) for rect in rectangles], lag_ratio=0.1))
        self.wait()

        # ========================================
        # SHOW: Width and height
        # ========================================
        # Highlight one rectangle
        highlight_rect = rectangles[2].copy()
        highlight_rect.set_stroke(RED, width=4)

        self.play(ShowCreation(highlight_rect))
        self.wait()

        # Width label
        dx = (B_BOUND - A_BOUND) / n_rects
        width_brace = Brace(highlight_rect, DOWN, buff=0.1)
        width_label = width_brace.get_tex("\\Delta x")

        self.play(
            GrowFromCenter(width_brace),
            FadeIn(width_label, shift=UP)
        )
        self.wait()

        # Height label
        height_brace = Brace(highlight_rect, LEFT, buff=0.1)
        height_label = height_brace.get_tex("f(x_i)")

        self.play(
            GrowFromCenter(height_brace),
            FadeIn(height_label, shift=RIGHT)
        )
        self.wait()

        # ========================================
        # FORMULA: Riemann sum
        # ========================================
        self.play(
            FadeOut(highlight_rect),
            FadeOut(width_brace),
            FadeOut(width_label),
            FadeOut(height_brace),
            FadeOut(height_label)
        )

        riemann_formula = Tex(
            "\\text{Area} \\approx \\sum_{i=1}^{n} f(x_i) \\Delta x",
            font_size=42
        )
        riemann_formula.to_edge(DOWN, buff=1)

        self.play(Write(riemann_formula))
        self.wait()

        # Calculate and show value
        approx_value = calculate_riemann_sum(example_function, A_BOUND, B_BOUND, n_rects)
        value_text = Tex(
            f"\\approx {approx_value:.3f}",
            font_size=36,
            color=YELLOW
        )
        value_text.next_to(riemann_formula, DOWN, buff=0.3)

        self.play(FadeIn(value_text, shift=UP))
        self.wait()

        # ========================================
        # INSIGHT: Not exact
        # ========================================
        insight = OldTexText(
            "This is only an approximation...",
            font_size=32,
            color=GREY_A
        )
        insight.next_to(value_text, DOWN, buff=0.3)

        self.play(FadeIn(insight, shift=UP))
        self.wait(2)


class IncreasingRectangles(InteractiveScene):
    """
    Part 3: Show how increasing n improves the approximation.

    Narrative purpose:
        To reveal the limiting process: as n → ∞, the Riemann sum
        converges to the exact area (the definite integral).

    Mathematical content:
        ∫[a to b] f(x)dx = lim[n→∞] Σ f(x_i)Δx.
        More rectangles means smaller Δx and better approximation.

    Visual approach:
        Progressively increase the number of rectangles (6, 12, 24, 48),
        showing the approximation getting better and better.
    """
    def construct(self):
        # ========================================
        # SETUP: Title
        # ========================================
        title = OldTexText("As n → ∞, We Get the Exact Area", font_size=48)
        title.to_edge(UP)

        self.add(title)

        # ========================================
        # CREATE: Axes and function
        # ========================================
        axes = Axes(**AXES_CONFIG)
        axes.add_coordinates()

        graph = axes.get_graph(
            example_function,
            x_range=(AXES_CONFIG["x_range"][0], AXES_CONFIG["x_range"][1]),
            color=BLUE
        )

        self.add(axes, graph)

        # ========================================
        # PROGRESSIVE: Increase number of rectangles
        # ========================================
        n_values = [6, 12, 24, 48]

        rectangles = None
        sum_text = None

        for n in n_values:
            # Create new rectangles
            new_rectangles = get_riemann_rectangles(
                axes,
                example_function,
                A_BOUND,
                B_BOUND,
                n,
                color=YELLOW,
                fill_opacity=0.6
            )

            # Calculate sum
            approx_value = calculate_riemann_sum(example_function, A_BOUND, B_BOUND, n)
            new_sum_text = Tex(
                f"n = {n}, \\quad \\sum f(x_i)\\Delta x \\approx {approx_value:.4f}",
                font_size=36
            )
            new_sum_text.to_edge(DOWN, buff=0.8)

            # Animate transition
            if rectangles is None:
                self.play(
                    LaggedStart([DrawBorderThenFill(rect) for rect in new_rectangles], lag_ratio=0.02),
                    run_time=1.5
                )
                self.play(Write(new_sum_text))
            else:
                self.play(
                    Transform(rectangles, new_rectangles),
                    Transform(sum_text, new_sum_text),
                    run_time=1.5
                )

            rectangles = new_rectangles if rectangles is None else rectangles
            sum_text = new_sum_text if sum_text is None else sum_text

            self.wait()

        # ========================================
        # LIMIT: Show the exact integral
        # ========================================
        exact_value = calculate_exact_integral(example_antiderivative, A_BOUND, B_BOUND)
        limit_text = Tex(
            f"\\lim_{{n \\to \\infty}} \\sum f(x_i)\\Delta x = {exact_value:.4f}",
            font_size=42,
            color=GREEN
        )
        limit_text.to_edge(DOWN, buff=0.8)

        box = SurroundingRectangle(limit_text, buff=0.2, color=GREEN, stroke_width=3)

        self.play(Transform(sum_text, limit_text))
        self.play(ShowCreation(box))
        self.wait()

        # ========================================
        # DEFINITION: The definite integral
        # ========================================
        integral_def = Tex(
            "\\int_a^b f(x) \\, dx",
            font_size=48,
            color=GREEN
        )
        integral_def.next_to(limit_text, UP, buff=0.8)

        self.play(FadeIn(integral_def, shift=DOWN))
        self.wait(2)


class FundamentalTheorem(InteractiveScene):
    """
    Part 4: Connect to the Fundamental Theorem of Calculus.

    Narrative purpose:
        To complete the picture by showing that integration (area) is the
        inverse of differentiation (slopes), via the Fundamental Theorem.

    Mathematical content:
        If F'(x) = f(x), then ∫[a to b] f(x)dx = F(b) - F(a).
        This provides a practical way to compute integrals.

    Visual approach:
        State the Fundamental Theorem, show how to use an antiderivative
        to compute the exact area, and emphasize the connection to derivatives.
    """
    def construct(self):
        # ========================================
        # SETUP: Title
        # ========================================
        title = OldTexText("The Fundamental Theorem of Calculus", font_size=48)
        title.to_edge(UP)

        self.add(title)

        # ========================================
        # THEOREM: Statement
        # ========================================
        theorem = Tex(
            "\\text{If } F'(x) = f(x), \\text{ then } \\int_a^b f(x) \\, dx = F(b) - F(a)",
            font_size=40
        )
        theorem.shift(1.5 * UP)

        box = SurroundingRectangle(theorem, buff=0.3, color=YELLOW, stroke_width=3)

        self.play(Write(theorem), run_time=2)
        self.play(ShowCreation(box))
        self.wait(2)

        # ========================================
        # EXPLANATION: Connection
        # ========================================
        explanation = OldTexText(
            "Integration is the inverse of differentiation!",
            font_size=36,
            color=GREEN
        )
        explanation.next_to(theorem, DOWN, buff=0.8)

        self.play(FadeIn(explanation, shift=UP))
        self.wait()

        # ========================================
        # EXAMPLE: Apply to our function
        # ========================================
        example_intro = Tex(
            "\\text{Example: } f(x) = 1 + \\frac{1}{2}\\sin(2x)",
            font_size=36
        )
        example_intro.next_to(explanation, DOWN, buff=1)

        self.play(Write(example_intro))
        self.wait()

        # Antiderivative
        antideriv = Tex(
            "F(x) = x - \\frac{1}{4}\\cos(2x)",
            font_size=36
        )
        antideriv.next_to(example_intro, DOWN, buff=0.4)

        self.play(Write(antideriv))
        self.wait()

        # Computation
        computation = Tex(
            f"\\int_{{{A_BOUND:.1f}}}^{{{B_BOUND:.1f}}} f(x) \\, dx = F({B_BOUND:.1f}) - F({A_BOUND:.1f})",
            font_size=36
        )
        computation.next_to(antideriv, DOWN, buff=0.5)

        self.play(Write(computation))
        self.wait()

        # Result
        exact_value = calculate_exact_integral(example_antiderivative, A_BOUND, B_BOUND)
        result = Tex(
            f"= {exact_value:.4f}",
            font_size=42,
            color=GREEN
        )
        result.next_to(computation, RIGHT, buff=0.3)

        result_box = SurroundingRectangle(result, buff=0.2, color=GREEN, stroke_width=2)

        self.play(Write(result))
        self.play(ShowCreation(result_box))
        self.wait()

        # ========================================
        # FINALE: Checkmark
        # ========================================
        checkmark = Tex("\\checkmark", font_size=72, color=GREEN)
        checkmark.next_to(result_box, RIGHT, buff=0.5)

        self.play(FadeIn(checkmark, scale=2))
        self.wait(2)


# ============================================================
# 6. SCENE EXECUTION ORDER
# ============================================================
# The order of scenes that tells the story.
#
# Scene 1 (AreaProblem):
#   - Introduces the problem of finding area under a curve
#   - Shows a function with shaded region between bounds
#   - Poses the fundamental question
#
# Scene 2 (RiemannSums):
#   - Introduces rectangular approximations (Riemann sums)
#   - Shows how to calculate the sum of rectangle areas
#   - Notes that this is only an approximation
#
# Scene 3 (IncreasingRectangles):
#   - Shows progressive refinement with more rectangles
#   - Demonstrates convergence to the exact value
#   - Introduces the definite integral as a limit
#
# Scene 4 (FundamentalTheorem):
#   - States the Fundamental Theorem of Calculus
#   - Shows how to compute integrals using antiderivatives
#   - Completes the connection between integration and differentiation

SCENE_ORDER = [
    AreaProblem,             # Part 1: The area problem
    RiemannSums,             # Part 2: Rectangular approximations
    IncreasingRectangles,    # Part 3: Limit as n → ∞
    FundamentalTheorem,      # Part 4: FTC and antiderivatives
]
