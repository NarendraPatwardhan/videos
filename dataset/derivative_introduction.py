"""
Natural Group Name: Introduction to Derivatives

Educational Objectives:
- To visualize the derivative as the slope of a tangent line
- To demonstrate how secant lines approach the tangent as h → 0
- To build intuition for the limit definition of the derivative
- To connect the geometric and algebraic concepts of rate of change

Story Arc & Intent:
The animation reveals the derivative through visual limiting process: secant lines
(average rates of change) gradually approach the tangent line (instantaneous rate).
This transforms the abstract limit definition into an intuitive geometric process.

Narrative Flow:
- Hook/Opening: A smooth curve and the question of "steepness" at a point
- Development: Secant lines through two nearby points on the curve
- Build-up: As the points get closer, the secant approaches the tangent
- Climax: The limit as h → 0 gives the derivative (slope of tangent)
- Resolution: Connect to the algebraic limit definition f'(x) = lim[h→0] (f(x+h)-f(x))/h

Technical Implementation Notes:
- Scene Classes: IntroduceFunction, SecantLines, LimitToTangent, DerivativeDefinition
- Key Visual Elements: Graphs, secant lines, tangent line, limit notation
- Animation Techniques: Line interpolation, point movement, limit visualization
- Mathematical Concepts: Derivatives, limits, tangent lines, rates of change

Dependency Chain:
All scenes use basic manimlib components: Axes, ParametricCurve, Line, Dot, Text, Tex.
No custom utilities required.

Rendering Instructions:
To render these scenes, use the manim command-line tool:
- For a single scene: manimgl derivative_introduction.py IntroduceFunction
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
# - BLUE: The function curve f(x)
# - YELLOW: Secant lines (average rate of change)
# - GREEN: Tangent line (instantaneous rate of change)
# - RED: Points on the curve
# - WHITE: Axes and grid
# - GREY_A: De-emphasized elements
#
# Key Manim Constants Used:
# - UP, DOWN, LEFT, RIGHT: Direction vectors
# - ORIGIN: Center point
# - PI: π for mathematical functions
# - MED_SMALL_BUFF: Spacing

# Axes configuration
AXES_CONFIG = {
    "x_range": (-1, 5, 1),
    "y_range": (-1, 5, 1),
    "width": 10,
    "height": 6,
}

# Example function: f(x) = x^2 / 4
def example_function(x):
    """Example function for demonstration."""
    return x**2 / 4

def example_derivative(x):
    """Derivative of example function: f'(x) = x / 2."""
    return x / 2

# ============================================================
# 3. UTILITY FUNCTIONS
# ============================================================

def create_function_graph(axes, func, x_range=None, color=BLUE, **kwargs):
    """
    Create a graph of a function on given axes.

    Args:
        axes: Axes object
        func: Function to graph (takes x, returns y)
        x_range: Tuple of (x_min, x_max) or None to use axes range
        color: Color of the graph
        **kwargs: Additional arguments for graph

    Returns:
        Graph mobject
    """
    if x_range is None:
        x_range = (axes.x_range[0], axes.x_range[1])

    return axes.get_graph(
        func,
        x_range=x_range,
        color=color,
        **kwargs
    )

def create_secant_line(axes, func, x1, x2, color=YELLOW, **kwargs):
    """
    Create a secant line between two points on a function.

    Args:
        axes: Axes object
        func: Function
        x1: First x-coordinate
        x2: Second x-coordinate
        color: Color of the secant line
        **kwargs: Additional arguments for Line

    Returns:
        Line mobject representing the secant
    """
    p1 = axes.c2p(x1, func(x1))
    p2 = axes.c2p(x2, func(x2))

    return Line(p1, p2, color=color, stroke_width=3, **kwargs)

def create_tangent_line(axes, func, derivative_func, x, length=4, color=GREEN, **kwargs):
    """
    Create a tangent line at a point on a function.

    Args:
        axes: Axes object
        func: Function
        derivative_func: Derivative function
        x: x-coordinate where tangent is drawn
        length: Length of the tangent line to draw
        color: Color of the tangent line
        **kwargs: Additional arguments for Line

    Returns:
        Line mobject representing the tangent
    """
    point = axes.c2p(x, func(x))
    slope = derivative_func(x)

    # Calculate endpoints of tangent line
    dx = length / 2
    p1 = axes.c2p(x - dx, func(x) - slope * dx)
    p2 = axes.c2p(x + dx, func(x) + slope * dx)

    return Line(p1, p2, color=color, stroke_width=4, **kwargs)

def get_slope(func, x1, x2):
    """
    Calculate the slope of the secant line.

    Args:
        func: Function
        x1: First x-coordinate
        x2: Second x-coordinate

    Returns:
        Slope (rise over run)
    """
    if abs(x2 - x1) < 1e-10:
        return 0
    return (func(x2) - func(x1)) / (x2 - x1)

# ============================================================
# 4. BASE CLASSES AND HELPERS
# ============================================================
# No custom base classes needed

# ============================================================
# 5. SCENE IMPLEMENTATIONS
# ============================================================

class IntroduceFunction(InteractiveScene):
    """
    Part 1: Introduce a function and the concept of steepness at a point.

    Narrative purpose:
        To establish the fundamental question: how steep is the curve at a
        specific point? This motivates the need for derivatives.

    Mathematical content:
        A smooth function f(x) has varying steepness along its curve.
        We want to measure the steepness (slope) at any given point.

    Visual approach:
        Show a parabola f(x) = x²/4, mark a point, and pose the question
        of how to measure steepness at that exact point.
    """
    def construct(self):
        # ========================================
        # SETUP: Title
        # ========================================
        title = OldTexText("What is the Slope at a Point?", font_size=48)
        title.to_edge(UP)

        self.play(FadeIn(title, shift=DOWN))
        self.wait()

        # ========================================
        # CREATE: Axes and function
        # ========================================
        axes = Axes(**AXES_CONFIG)
        axes.add_coordinates()

        # Function label
        func_label = Tex("f(x) = \\frac{x^2}{4}", font_size=42)
        func_label.next_to(axes.y_axis.get_top(), RIGHT, buff=0.5)

        self.play(ShowCreation(axes), run_time=1.5)
        self.play(FadeIn(func_label, shift=DOWN))
        self.wait()

        # ========================================
        # GRAPH: Draw the function
        # ========================================
        graph = create_function_graph(axes, example_function, color=BLUE)

        self.play(ShowCreation(graph), run_time=2)
        self.wait()

        # ========================================
        # MARK: A specific point
        # ========================================
        x_point = 2
        point = Dot(axes.c2p(x_point, example_function(x_point)), color=RED)
        point.set_sheen(-0.3, DR)

        point_label = Tex(f"({x_point}, {example_function(x_point)})", font_size=32, color=RED)
        point_label.next_to(point, UR, buff=0.2)

        self.play(GrowFromCenter(point))
        self.play(FadeIn(point_label, shift=DL))
        self.wait()

        # ========================================
        # QUESTION: What is the slope here?
        # ========================================
        question = OldTexText(
            "What is the slope of the curve at this point?",
            font_size=36,
            color=YELLOW
        )
        question.to_edge(DOWN, buff=0.5)

        self.play(FadeIn(question, shift=UP))
        self.wait(2)

        # ========================================
        # HINT: Need a tangent line
        # ========================================
        hint = OldTexText(
            "We need the tangent line...",
            font_size=32,
            color=GREY_A
        )
        hint.next_to(question, UP, buff=0.3)

        self.play(FadeIn(hint, shift=UP))
        self.wait(2)


class SecantLines(InteractiveScene):
    """
    Part 2: Show secant lines approximating the tangent.

    Narrative purpose:
        To demonstrate the concept of average rate of change using secant lines,
        setting up the idea that we can approximate the instantaneous rate.

    Mathematical content:
        A secant line through points (x, f(x)) and (x+h, f(x+h)) has slope
        [f(x+h) - f(x)] / h, which is the average rate of change.

    Visual approach:
        Draw several secant lines with different values of h, showing how
        they provide approximations to the slope at a point.
    """
    def construct(self):
        # ========================================
        # SETUP: Title
        # ========================================
        title = OldTexText("Secant Lines: Average Rate of Change", font_size=48)
        title.to_edge(UP)

        self.add(title)

        # ========================================
        # CREATE: Axes and function
        # ========================================
        axes = Axes(**AXES_CONFIG)
        axes.add_coordinates()

        graph = create_function_graph(axes, example_function, color=BLUE)

        self.add(axes, graph)

        # ========================================
        # MARK: The point of interest
        # ========================================
        x_point = 2
        point_a = Dot(axes.c2p(x_point, example_function(x_point)), color=RED)
        point_a.set_sheen(-0.3, DR)

        label_a = Tex("x", font_size=36, color=RED)
        label_a.next_to(point_a, DOWN, buff=0.2)

        self.play(GrowFromCenter(point_a))
        self.play(FadeIn(label_a))
        self.wait()

        # ========================================
        # CREATE: First secant line (large h)
        # ========================================
        h1 = 2.0
        x2 = x_point + h1

        point_b = Dot(axes.c2p(x2, example_function(x2)), color=RED)
        point_b.set_sheen(-0.3, DR)

        label_b = Tex("x + h", font_size=36, color=RED)
        label_b.next_to(point_b, UR, buff=0.2)

        self.play(GrowFromCenter(point_b))
        self.play(FadeIn(label_b))
        self.wait()

        # Draw secant line
        secant1 = create_secant_line(axes, example_function, x_point, x2, color=YELLOW)

        self.play(ShowCreation(secant1))
        self.wait()

        # Show the slope
        slope1 = get_slope(example_function, x_point, x2)
        slope_text1 = Tex(
            f"\\text{{Slope}} = \\frac{{f(x+h) - f(x)}}{{h}} \\approx {slope1:.2f}",
            font_size=36
        )
        slope_text1.to_edge(DOWN, buff=0.8)

        self.play(Write(slope_text1))
        self.wait()

        # ========================================
        # CREATE: Smaller h values
        # ========================================
        h_values = [1.0, 0.5, 0.25]

        for h in h_values:
            x2_new = x_point + h
            point_b_new = Dot(axes.c2p(x2_new, example_function(x2_new)), color=RED)
            point_b_new.set_sheen(-0.3, DR)

            label_b_new = Tex("x + h", font_size=36, color=RED)
            label_b_new.next_to(point_b_new, UR, buff=0.2)

            secant_new = create_secant_line(axes, example_function, x_point, x2_new, color=YELLOW)

            slope_new = get_slope(example_function, x_point, x2_new)
            slope_text_new = Tex(
                f"\\text{{Slope}} \\approx {slope_new:.2f}",
                font_size=36
            )
            slope_text_new.to_edge(DOWN, buff=0.8)

            self.play(
                Transform(point_b, point_b_new),
                Transform(label_b, label_b_new),
                Transform(secant1, secant_new),
                Transform(slope_text1, slope_text_new),
                run_time=1.5
            )
            self.wait()

        # ========================================
        # INSIGHT: As h gets smaller...
        # ========================================
        insight = OldTexText(
            "As h → 0, we approach the true slope!",
            font_size=36,
            color=GREEN
        )
        insight.next_to(slope_text1, UP, buff=0.5)

        self.play(FadeIn(insight, shift=UP))
        self.wait(2)


class LimitToTangent(InteractiveScene):
    """
    Part 3: Show the limiting process to the tangent line.

    Narrative purpose:
        To visualize the key idea of calculus: as h approaches 0, the secant
        line approaches the tangent line, giving the instantaneous rate.

    Mathematical content:
        The derivative f'(x) = lim[h→0] [f(x+h) - f(x)] / h is the slope
        of the tangent line, obtained as the limit of secant slopes.

    Visual approach:
        Animate h continuously decreasing to 0, showing the secant line
        morphing into the tangent line.
    """
    def construct(self):
        # ========================================
        # SETUP: Title
        # ========================================
        title = OldTexText("The Limit: Tangent Line", font_size=48)
        title.to_edge(UP)

        self.add(title)

        # ========================================
        # CREATE: Axes and function
        # ========================================
        axes = Axes(**AXES_CONFIG)
        axes.add_coordinates()

        graph = create_function_graph(axes, example_function, color=BLUE)

        self.add(axes, graph)

        # ========================================
        # SETUP: Point and initial secant
        # ========================================
        x_point = 2
        h_tracker = ValueTracker(1.5)

        point_a = Dot(axes.c2p(x_point, example_function(x_point)), color=RED)
        point_a.set_sheen(-0.3, DR)

        self.add(point_a)

        # Dynamic point b
        point_b = always_redraw(lambda: Dot(
            axes.c2p(
                x_point + h_tracker.get_value(),
                example_function(x_point + h_tracker.get_value())
            ),
            color=RED
        ).set_sheen(-0.3, DR))

        # Dynamic secant line
        secant = always_redraw(lambda: create_secant_line(
            axes,
            example_function,
            x_point,
            x_point + h_tracker.get_value(),
            color=YELLOW
        ))

        # Dynamic slope display
        slope_text = always_redraw(lambda: Tex(
            f"h = {h_tracker.get_value():.2f}, \\quad \\text{{Slope}} = {get_slope(example_function, x_point, x_point + h_tracker.get_value()):.3f}",
            font_size=36
        ).to_edge(DOWN, buff=0.8))

        self.add(point_b, secant, slope_text)
        self.wait()

        # ========================================
        # ANIMATE: h → 0
        # ========================================
        instruction = OldTexText("Watch as h → 0...", font_size=36, color=GREY_A)
        instruction.next_to(slope_text, UP, buff=0.5)

        self.play(FadeIn(instruction, shift=UP))
        self.wait()

        # Gradually decrease h to 0
        self.play(
            h_tracker.animate.set_value(0.05),
            run_time=4,
            rate_func=smooth
        )
        self.wait()

        # ========================================
        # REVEAL: The tangent line
        # ========================================
        self.play(FadeOut(instruction))

        tangent = create_tangent_line(
            axes,
            example_function,
            example_derivative,
            x_point,
            length=4,
            color=GREEN
        )

        final_slope = example_derivative(x_point)
        final_text = Tex(
            f"f'({x_point}) = {final_slope}",
            font_size=42,
            color=GREEN
        )
        final_text.to_edge(DOWN, buff=0.8)

        box = SurroundingRectangle(final_text, buff=0.2, color=GREEN, stroke_width=3)

        self.play(
            FadeOut(point_b),
            secant.animate.set_color(GREEN).set_stroke(width=4),
            Transform(slope_text, final_text),
        )
        self.play(ShowCreation(box))
        self.wait()

        # ========================================
        # LABEL: Tangent line
        # ========================================
        tangent_label = OldTexText("Tangent Line", font_size=32, color=GREEN)
        tangent_label.next_to(tangent.get_end(), UR, buff=0.2)

        self.play(FadeIn(tangent_label, shift=DL))
        self.wait(2)


class DerivativeDefinition(InteractiveScene):
    """
    Part 4: Present the formal limit definition of the derivative.

    Narrative purpose:
        To connect the visual intuition to the formal mathematical definition,
        completing the conceptual picture of what a derivative is.

    Mathematical content:
        The derivative is defined as f'(x) = lim[h→0] [f(x+h) - f(x)] / h,
        representing the instantaneous rate of change.

    Visual approach:
        Show the limit definition, connect each part to the visual elements,
        and emphasize that this gives the slope of the tangent line.
    """
    def construct(self):
        # ========================================
        # SETUP: Title
        # ========================================
        title = OldTexText("The Derivative: Formal Definition", font_size=48)
        title.to_edge(UP)

        self.add(title)

        # ========================================
        # DEFINITION: Limit formula
        # ========================================
        definition = Tex(
            "f'(x) = \\lim_{h \\to 0} \\frac{f(x+h) - f(x)}{h}",
            font_size=60
        )
        definition.shift(1 * UP)

        box = SurroundingRectangle(definition, buff=0.3, color=YELLOW, stroke_width=3)

        self.play(Write(definition), run_time=2)
        self.play(ShowCreation(box))
        self.wait()

        # ========================================
        # EXPLANATION: Break down the formula
        # ========================================
        # Highlight numerator
        numerator_explain = OldTexText(
            "Change in f(x)",
            font_size=32,
            color=BLUE
        )
        numerator_explain.next_to(definition, DOWN, buff=1)

        self.play(FadeIn(numerator_explain, shift=UP))
        self.wait()

        # Highlight denominator
        denominator_explain = OldTexText(
            "Change in x",
            font_size=32,
            color=TEAL
        )
        denominator_explain.next_to(numerator_explain, DOWN, buff=0.3)

        self.play(FadeIn(denominator_explain, shift=UP))
        self.wait()

        # Ratio meaning
        ratio_explain = OldTexText(
            "Ratio = Average rate of change",
            font_size=32,
            color=YELLOW
        )
        ratio_explain.next_to(denominator_explain, DOWN, buff=0.3)

        self.play(FadeIn(ratio_explain, shift=UP))
        self.wait()

        # Limit meaning
        limit_explain = OldTexText(
            "Limit as h → 0 = Instantaneous rate",
            font_size=32,
            color=GREEN
        )
        limit_explain.next_to(ratio_explain, DOWN, buff=0.3)

        self.play(FadeIn(limit_explain, shift=UP))
        self.wait(2)

        # ========================================
        # EXAMPLE: Compute derivative
        # ========================================
        explanations = VGroup(numerator_explain, denominator_explain, ratio_explain, limit_explain)
        self.play(FadeOut(explanations))

        example = Tex(
            "\\text{For } f(x) = \\frac{x^2}{4}:",
            font_size=36
        )
        example.next_to(definition, DOWN, buff=1.2)

        self.play(Write(example))
        self.wait()

        # Derivative result
        derivative_result = Tex(
            "f'(x) = \\frac{x}{2}",
            font_size=48,
            color=GREEN
        )
        derivative_result.next_to(example, DOWN, buff=0.5)

        result_box = SurroundingRectangle(derivative_result, buff=0.2, color=GREEN, stroke_width=2)

        self.play(Write(derivative_result))
        self.play(ShowCreation(result_box))
        self.wait()

        # ========================================
        # MEANING: Slope of tangent
        # ========================================
        meaning = OldTexText(
            "This is the slope of the tangent line at any point x",
            font_size=32,
            color=GREY_A
        )
        meaning.to_edge(DOWN, buff=0.5)

        self.play(FadeIn(meaning, shift=UP))
        self.wait(2)

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
# Scene 1 (IntroduceFunction):
#   - Introduces a smooth function f(x) = x²/4
#   - Marks a specific point on the curve
#   - Poses the question: what is the slope at this point?
#
# Scene 2 (SecantLines):
#   - Shows secant lines with different h values
#   - Demonstrates average rate of change
#   - Shows that smaller h gives better approximations
#
# Scene 3 (LimitToTangent):
#   - Animates the limiting process as h → 0
#   - Shows secant line morphing into tangent line
#   - Reveals the derivative as the slope of the tangent
#
# Scene 4 (DerivativeDefinition):
#   - Presents the formal limit definition
#   - Breaks down each component of the formula
#   - Computes the derivative for the example function

SCENE_ORDER = [
    IntroduceFunction,       # Part 1: The question - slope at a point
    SecantLines,             # Part 2: Secant lines as approximations
    LimitToTangent,          # Part 3: The limit to the tangent
    DerivativeDefinition,    # Part 4: Formal definition and computation
]
