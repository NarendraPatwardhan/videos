"""
Natural Group Name: Taylor Series Polynomial Approximation

Educational Objectives:
- To visualize how polynomials approximate smooth functions
- To demonstrate the role of successive derivatives in building approximations
- To show the convergence of Taylor series to the original function
- To build intuition for local vs global approximation behavior

Story Arc & Intent:
The animation reveals how polynomials of increasing degree progressively better
approximate a smooth function near a point. This transforms the abstract concept
of Taylor series into a visual convergence process that builds intuition for
approximation theory.

Narrative Flow:
- Hook/Opening: A curved function and the challenge of approximation
- Development: Linear approximation (tangent line) as first step
- Build-up: Adding quadratic, cubic terms for better fit
- Climax: The general Taylor series formula with derivatives
- Resolution: Convergence behavior and radius of convergence

Technical Implementation Notes:
- Scene Classes: IntroduceFunction, LinearApproximation, HigherOrderTerms, ConvergenceRadius
- Key Visual Elements: Graphs, polynomial approximations, derivative notation
- Animation Techniques: Graph morphing, term-by-term construction
- Mathematical Concepts: Taylor series, derivatives, polynomial approximation

Dependency Chain:
All scenes use basic manimlib components: Axes, graph functions, Tex, Text.
No custom utilities required beyond helper functions defined in this file.

Rendering Instructions:
To render these scenes, use the manim command-line tool:
- For a single scene: manimgl taylor_series.py IntroduceFunction
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
# - BLUE: Original function
# - YELLOW: Linear approximation (1st order)
# - GREEN: Quadratic approximation (2nd order)
# - RED: Cubic approximation (3rd order)
# - PURPLE: Higher order approximations
# - WHITE: Axes and labels
# - GREY_A: De-emphasized elements
#
# Key Manim Constants Used:
# - UP, DOWN, LEFT, RIGHT: Direction vectors
# - ORIGIN: Center point
# - PI: π for trigonometric functions
# - MED_SMALL_BUFF: Spacing

# Axes configuration
AXES_CONFIG = {
    "x_range": [-4, 4, 1],
    "y_range": [-2, 3, 1],
    "width": 10,
    "height": 6,
}

# Point of approximation
APPROX_POINT = 0.0

# ============================================================
# 3. UTILITY FUNCTIONS
# ============================================================

def create_axes(config=None):
    """
    Create axes with standard configuration.

    Args:
        config: Dictionary of axes configuration (optional)

    Returns:
        Axes mobject
    """
    if config is None:
        config = AXES_CONFIG
    return Axes(**config)

def taylor_polynomial(func, derivatives, center, x, order):
    """
    Compute the Taylor polynomial approximation.

    Args:
        func: Original function (not used, kept for interface)
        derivatives: List of derivative values at center [f(a), f'(a), f''(a), ...]
        center: Point of approximation
        x: Point to evaluate at
        order: Order of Taylor polynomial (0, 1, 2, ...)

    Returns:
        Value of Taylor polynomial at x
    """
    result = 0.0
    dx = x - center

    for n in range(order + 1):
        if n < len(derivatives):
            # nth term: f^(n)(a) * (x-a)^n / n!
            factorial_n = np.math.factorial(n)
            result += derivatives[n] * (dx ** n) / factorial_n

    return result

def sin_derivatives(x):
    """
    Return list of derivatives of sin(x) at point x.

    Args:
        x: Point to evaluate derivatives at

    Returns:
        List [sin(x), cos(x), -sin(x), -cos(x), ...] for first 8 derivatives
    """
    return [
        np.sin(x),      # 0th derivative
        np.cos(x),      # 1st derivative
        -np.sin(x),     # 2nd derivative
        -np.cos(x),     # 3rd derivative
        np.sin(x),      # 4th derivative
        np.cos(x),      # 5th derivative
        -np.sin(x),     # 6th derivative
        -np.cos(x),     # 7th derivative
    ]

def exp_derivatives(x):
    """
    Return list of derivatives of e^x at point x.

    Args:
        x: Point to evaluate derivatives at

    Returns:
        List of e^x repeated (all derivatives are e^x)
    """
    ex = np.exp(x)
    return [ex] * 8

def get_taylor_graph(axes, derivatives, center, order, color=YELLOW, **kwargs):
    """
    Create a graph of a Taylor polynomial.

    Args:
        axes: Axes object
        derivatives: List of derivative values at center
        center: Point of approximation
        order: Order of polynomial
        color: Color of the graph
        **kwargs: Additional arguments for graph

    Returns:
        Graph mobject
    """
    def taylor_func(x):
        return taylor_polynomial(None, derivatives, center, x, order)

    return axes.get_graph(
        taylor_func,
        x_range=(axes.x_range[0], axes.x_range[1]),
        color=color,
        **kwargs
    )

# ============================================================
# 4. SCENE CLASSES
# ============================================================

class IntroduceFunction(Scene):
    """
    Scene 1: Introduce a smooth function and the approximation challenge.

    This scene presents sin(x) and asks: can we approximate it with simpler
    functions like polynomials?
    """

    def construct(self):
        # ========================================
        # TITLE
        # ========================================
        title = OldTexText("Taylor Series Approximation", font_size=48)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait()

        # ========================================
        # SETUP: Create axes
        # ========================================
        axes = create_axes()
        axes.shift(DOWN * 0.5)

        self.play(ShowCreation(axes))
        self.wait()

        # ========================================
        # INTRODUCE: The function sin(x)
        # ========================================
        sin_graph = axes.get_graph(
            lambda x: np.sin(x),
            x_range=(-4, 4),
            color=BLUE,
            stroke_width=4
        )

        function_label = Tex("f(x) = \\sin(x)", color=BLUE, font_size=36)
        function_label.next_to(axes, UP, buff=0.3).to_edge(LEFT)

        self.play(ShowCreation(sin_graph), Write(function_label))
        self.wait()

        # ========================================
        # QUESTION: Polynomial approximation?
        # ========================================
        question = OldTexText(
            "Can we approximate this with polynomials?",
            font_size=32,
            color=WHITE
        )
        question.to_edge(DOWN).shift(UP * 0.3)

        self.play(FadeIn(question, shift=UP))
        self.wait()

        # ========================================
        # MARK: Point of approximation
        # ========================================
        center_dot = Dot(axes.c2p(APPROX_POINT, np.sin(APPROX_POINT)), color=YELLOW)
        center_label = Tex("a = 0", color=YELLOW, font_size=32)
        center_label.next_to(center_dot, DOWN, buff=0.3)

        self.play(FadeIn(center_dot, scale=0.5))
        self.play(Write(center_label))
        self.wait()

        # ========================================
        # IDEA: Local approximation
        # ========================================
        self.play(FadeOut(question))

        idea = OldTexText(
            "Idea: Match the function and its derivatives at a point",
            font_size=28,
            color=GREY_A
        )
        idea.to_edge(DOWN).shift(UP * 0.3)

        self.play(FadeIn(idea, shift=UP))
        self.wait(2)


class LinearApproximation(Scene):
    """
    Scene 2: Show the first-order (linear) Taylor approximation.

    This scene demonstrates the tangent line approximation, which matches
    both the value and first derivative at the point.
    """

    def construct(self):
        # ========================================
        # SETUP: Recreate from Scene 1
        # ========================================
        title = OldTexText("Linear Approximation", font_size=42)
        title.to_edge(UP)

        axes = create_axes()
        axes.shift(DOWN * 0.5)

        sin_graph = axes.get_graph(
            lambda x: np.sin(x),
            x_range=(-4, 4),
            color=BLUE,
            stroke_width=4
        )

        function_label = Tex("f(x) = \\sin(x)", color=BLUE, font_size=32)
        function_label.next_to(axes, UP, buff=0.3).to_edge(LEFT)

        self.add(title, axes, sin_graph, function_label)
        self.wait()

        # ========================================
        # DERIVATIVES at x = 0
        # ========================================
        derivatives = sin_derivatives(APPROX_POINT)

        deriv_text = VGroup(
            Tex(f"f(0) = {derivatives[0]:.2f}", font_size=28),
            Tex(f"f'(0) = {derivatives[1]:.2f}", font_size=28, color=YELLOW),
        )
        deriv_text.arrange(DOWN, buff=0.2, aligned_edge=LEFT)
        deriv_text.to_edge(DOWN).shift(UP * 0.3 + RIGHT * 3)

        for text in deriv_text:
            self.play(Write(text))
            self.wait(0.5)

        # ========================================
        # LINEAR APPROXIMATION
        # ========================================
        # P₁(x) = f(0) + f'(0)·x
        linear_graph = get_taylor_graph(
            axes, derivatives, APPROX_POINT, order=1, color=YELLOW
        )

        linear_formula = Tex(
            "P_1(x) = f(0) + f'(0) \\cdot x",
            font_size=32,
            color=YELLOW
        )
        linear_formula.to_edge(DOWN).shift(UP * 0.3 + LEFT * 3)

        self.play(ShowCreation(linear_graph))
        self.play(Write(linear_formula))
        self.wait()

        # ========================================
        # EVALUATION
        # ========================================
        evaluation = Tex(
            "P_1(x) = 0 + 1 \\cdot x = x",
            font_size=28,
            color=YELLOW
        )
        evaluation.next_to(linear_formula, DOWN, buff=0.2)

        self.play(Write(evaluation))
        self.wait()

        # ========================================
        # OBSERVATION: Good near 0, poor far away
        # ========================================
        observation = OldTexText(
            "Good near x=0, but diverges away from it",
            font_size=24,
            color=GREY_A
        )
        observation.next_to(evaluation, DOWN, buff=0.3)

        self.play(FadeIn(observation, shift=UP))
        self.wait(2)


class HigherOrderTerms(Scene):
    """
    Scene 3: Add quadratic and cubic terms for better approximation.

    This scene shows how including higher-order derivatives (curvature, etc.)
    progressively improves the approximation.
    """

    def construct(self):
        # ========================================
        # SETUP: Recreate function and linear approximation
        # ========================================
        title = OldTexText("Adding Higher Order Terms", font_size=42)
        title.to_edge(UP)

        axes = create_axes()
        axes.shift(DOWN * 0.5)

        sin_graph = axes.get_graph(
            lambda x: np.sin(x),
            x_range=(-4, 4),
            color=BLUE,
            stroke_width=4
        )

        self.add(title, axes, sin_graph)
        self.wait()

        derivatives = sin_derivatives(APPROX_POINT)

        # ========================================
        # BUILD: Add terms one by one
        # ========================================
        approximations = []
        colors = [YELLOW, GREEN, RED, PURPLE]
        orders = [1, 3, 5, 7]  # Use odd orders for sin(x)

        for i, (order, color) in enumerate(zip(orders, colors)):
            taylor_graph = get_taylor_graph(
                axes, derivatives, APPROX_POINT, order=order, color=color
            )
            approximations.append(taylor_graph)

            # Label
            if order == 1:
                label_text = "P_1(x) = x"
            elif order == 3:
                label_text = "P_3(x) = x - \\frac{x^3}{6}"
            elif order == 5:
                label_text = "P_5(x) = x - \\frac{x^3}{6} + \\frac{x^5}{120}"
            else:
                label_text = f"P_{{{order}}}(x)"

            label = Tex(label_text, color=color, font_size=28)
            label.to_edge(RIGHT).shift(UP * (2 - i * 0.8))

            if i == 0:
                self.play(ShowCreation(taylor_graph))
                self.play(Write(label))
            else:
                self.play(
                    ShowCreation(taylor_graph),
                    Write(label)
                )

            self.wait(1)

        # ========================================
        # OBSERVATION: Convergence
        # ========================================
        observation = OldTexText(
            "Each term improves the fit!",
            font_size=32,
            color=GREEN
        )
        observation.to_edge(DOWN).shift(UP * 0.3)

        self.play(FadeIn(observation, shift=UP))
        self.wait()

        # ========================================
        # GENERAL FORMULA
        # ========================================
        self.play(FadeOut(observation))

        formula = Tex(
            "P_n(x) = \\sum_{k=0}^{n} \\frac{f^{(k)}(a)}{k!}(x-a)^k",
            font_size=36,
            color=WHITE
        )
        formula.to_edge(DOWN).shift(UP * 0.3)

        self.play(Write(formula))
        self.wait()

        # Explanation of terms
        explanation = VGroup(
            Tex("f^{(k)}(a) = \\text{k-th derivative at } a", font_size=24),
            Tex("k! = \\text{factorial}", font_size=24),
            Tex("(x-a)^k = \\text{power term}", font_size=24),
        )
        explanation.arrange(DOWN, buff=0.2, aligned_edge=LEFT)
        explanation.next_to(formula, DOWN, buff=0.3)

        for item in explanation:
            self.play(FadeIn(item, shift=UP))
            self.wait(0.5)

        self.wait(2)


class ConvergenceRadius(Scene):
    """
    Scene 4: Explore convergence behavior and radius of convergence.

    This scene shows that Taylor series converge well near the expansion point
    but may diverge farther away, introducing the concept of convergence radius.
    """

    def construct(self):
        # ========================================
        # TITLE
        # ========================================
        title = OldTexText("Radius of Convergence", font_size=42)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait()

        # ========================================
        # SETUP: Two examples side by side
        # ========================================
        subtitle = OldTexText(
            "Some functions converge everywhere, others only locally",
            font_size=28,
            color=GREY_A
        )
        subtitle.next_to(title, DOWN, buff=0.3)

        self.play(FadeIn(subtitle, shift=DOWN))
        self.wait()

        # ========================================
        # EXAMPLE 1: sin(x) - converges everywhere
        # ========================================
        axes1 = Axes(
            x_range=[-6, 6, 2],
            y_range=[-2, 2, 1],
            width=6,
            height=3.5,
        )
        axes1.shift(LEFT * 3.5 + UP * 0.5)

        sin_graph = axes1.get_graph(
            lambda x: np.sin(x),
            x_range=(-6, 6),
            color=BLUE,
            stroke_width=3
        )

        sin_label = Tex("\\sin(x)", color=BLUE, font_size=28)
        sin_label.next_to(axes1, UP, buff=0.2)

        self.play(ShowCreation(axes1), Write(sin_label))
        self.play(ShowCreation(sin_graph))
        self.wait()

        # Taylor approximation
        sin_derivs = sin_derivatives(0)
        sin_taylor = get_taylor_graph(
            axes1, sin_derivs, 0, order=7, color=YELLOW, stroke_width=3
        )

        taylor_label1 = Tex("P_7(x)", color=YELLOW, font_size=24)
        taylor_label1.next_to(sin_label, DOWN, buff=0.2)

        self.play(ShowCreation(sin_taylor), Write(taylor_label1))
        self.wait()

        converge_text1 = OldTexText(
            "Converges for all x",
            font_size=22,
            color=GREEN
        )
        converge_text1.next_to(axes1, DOWN, buff=0.2)

        self.play(Write(converge_text1))
        self.wait()

        # ========================================
        # EXAMPLE 2: e^x - also converges everywhere
        # ========================================
        axes2 = Axes(
            x_range=[-2, 2, 1],
            y_range=[-1, 8, 2],
            width=6,
            height=3.5,
        )
        axes2.shift(RIGHT * 3.5 + UP * 0.5)

        exp_graph = axes2.get_graph(
            lambda x: np.exp(x),
            x_range=(-2, 2),
            color=BLUE,
            stroke_width=3
        )

        exp_label = Tex("e^x", color=BLUE, font_size=28)
        exp_label.next_to(axes2, UP, buff=0.2)

        self.play(ShowCreation(axes2), Write(exp_label))
        self.play(ShowCreation(exp_graph))
        self.wait()

        # Taylor approximation
        exp_derivs = exp_derivatives(0)
        exp_taylor = get_taylor_graph(
            axes2, exp_derivs, 0, order=5, color=YELLOW, stroke_width=3
        )

        taylor_label2 = Tex("P_5(x)", color=YELLOW, font_size=24)
        taylor_label2.next_to(exp_label, DOWN, buff=0.2)

        self.play(ShowCreation(exp_taylor), Write(taylor_label2))
        self.wait()

        converge_text2 = OldTexText(
            "Converges for all x",
            font_size=22,
            color=GREEN
        )
        converge_text2.next_to(axes2, DOWN, buff=0.2)

        self.play(Write(converge_text2))
        self.wait()

        # ========================================
        # KEY INSIGHT
        # ========================================
        self.play(
            FadeOut(subtitle),
            FadeOut(converge_text1),
            FadeOut(converge_text2)
        )

        insight = VGroup(
            OldTexText("Key Insights:", font_size=32, color=YELLOW),
            OldTexText("• Taylor series = infinite polynomial", font_size=24),
            OldTexText("• Each term adds a derivative correction", font_size=24),
            OldTexText("• Convergence depends on the function", font_size=24),
            OldTexText("• More terms = better approximation (if converges)", font_size=24),
        )
        insight.arrange(DOWN, buff=0.25, aligned_edge=LEFT)
        insight.to_edge(DOWN).shift(UP * 0.3)

        for item in insight:
            self.play(FadeIn(item, shift=UP))
            self.wait(0.5)

        self.wait(2)

        # ========================================
        # FORMULA REMINDER
        # ========================================
        self.play(FadeOut(insight))

        final_formula = Tex(
            "f(x) = \\sum_{n=0}^{\\infty} \\frac{f^{(n)}(a)}{n!}(x-a)^n",
            font_size=40,
            color=GREEN
        )
        final_formula.move_to(ORIGIN + DOWN * 2.5)

        formula_box = SurroundingRectangle(final_formula, buff=0.2, color=GREEN, stroke_width=2)

        self.play(Write(final_formula))
        self.play(ShowCreation(formula_box))
        self.wait(2)


# ============================================================
# 5. SCENE SUMMARY AND EXECUTION ORDER
# ============================================================
#
# Scene 1 (IntroduceFunction):
#   - Introduces sin(x) as the target function
#   - Poses the approximation challenge
#   - Marks the point of expansion (a = 0)
#
# Scene 2 (LinearApproximation):
#   - Shows the tangent line (1st order Taylor polynomial)
#   - Computes P₁(x) = x for sin(x) at 0
#   - Observes it's good locally but poor globally
#
# Scene 3 (HigherOrderTerms):
#   - Adds quadratic, cubic, quintic, septic terms
#   - Shows progressive improvement in approximation
#   - Presents the general Taylor series formula
#
# Scene 4 (ConvergenceRadius):
#   - Compares sin(x) and e^x Taylor series
#   - Shows both converge everywhere
#   - Summarizes key insights about Taylor series

SCENE_ORDER = [
    IntroduceFunction,         # Part 1: The approximation challenge
    LinearApproximation,       # Part 2: First-order tangent line
    HigherOrderTerms,          # Part 3: Building higher orders
    ConvergenceRadius,         # Part 4: Convergence behavior
]
