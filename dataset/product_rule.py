"""
Natural Group Name: Product Rule for Derivatives

Educational Objectives:
- To visualize the derivative of a product using area of a rectangle
- To demonstrate the product rule through geometric intuition
- To derive the formula d/dx[f(x)g(x)] = f'(x)g(x) + f(x)g'(x)
- To show applications of the product rule in calculus

Story Arc & Intent:
The animation reveals the product rule through the visual analogy of an expanding
rectangle: when both dimensions change, the total area change comes from two
separate contributions. This transforms the abstract formula into an intuitive
geometric process.

Narrative Flow:
- Hook/Opening: The challenge of differentiating a product
- Development: Rectangle with changing dimensions f(x) and g(x)
- Build-up: How area changes when both dimensions change
- Climax: The two terms of the product rule emerge from geometry
- Resolution: Formula and applications

Technical Implementation Notes:
- Scene Classes: IntroduceProduct, AreaRectangle, ProductRuleFormula, Examples
- Key Visual Elements: Rectangles, area changes, graphs, derivatives
- Animation Techniques: Rectangle transformation, area highlighting
- Mathematical Concepts: Derivatives, product rule, rates of change

Dependency Chain:
All scenes use basic manimlib components: Rectangle, Axes, graphs, Tex.
No custom utilities required beyond helper functions defined in this file.

Rendering Instructions:
To render these scenes, use the manim command-line tool:
- For a single scene: manimgl product_rule.py IntroduceProduct
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
# - BLUE: Function f(x)
# - YELLOW: Function g(x)
# - GREEN: Product f(x)g(x)
# - RED: Changes/increments
# - WHITE: Axes and labels
# - GREY_A: De-emphasized elements
#
# Key Manim Constants Used:
# - UP, DOWN, LEFT, RIGHT: Direction vectors
# - ORIGIN: Center point
# - PI: π for calculations
# - MED_SMALL_BUFF: Spacing

# Example functions
def f_func(x):
    """Example function f(x)."""
    return 2 + 0.5 * x

def g_func(x):
    """Example function g(x)."""
    return 1 + 0.3 * x

def f_derivative(x):
    """Derivative of f(x)."""
    return 0.5

def g_derivative(x):
    """Derivative of g(x)."""
    return 0.3

def product_func(x):
    """Product f(x) * g(x)."""
    return f_func(x) * g_func(x)

# ============================================================
# 3. UTILITY FUNCTIONS
# ============================================================

def create_labeled_rectangle(width, height, color=BLUE, label=None, **kwargs):
    """
    Create a rectangle with optional label.

    Args:
        width: Width of rectangle
        height: Height of rectangle
        color: Color of rectangle
        label: Text label (optional)
        **kwargs: Additional arguments

    Returns:
        VGroup containing rectangle and label
    """
    rect = Rectangle(
        width=width,
        height=height,
        color=color,
        stroke_width=2,
        **kwargs
    )

    if label:
        label_mob = Tex(label, color=color, font_size=28)
        group = VGroup(rect, label_mob)
        return group
    else:
        return VGroup(rect)

def create_dimension_label(start, end, text, direction=DOWN, color=WHITE, **kwargs):
    """
    Create a dimension label with arrows.

    Args:
        start: Start point
        end: End point
        text: Label text
        direction: Direction for label placement
        color: Color
        **kwargs: Additional arguments

    Returns:
        VGroup of brace and label
    """
    line = Line(start, end)
    brace = Brace(line, direction=direction, **kwargs)
    label = brace.get_text(text)
    label.set_color(color)

    return VGroup(brace, label)

# ============================================================
# 4. SCENE CLASSES
# ============================================================

class IntroduceProduct(Scene):
    """
    Scene 1: Introduce the problem of differentiating a product.

    This scene poses the question: if we know how to differentiate f(x) and g(x),
    how do we differentiate their product f(x)g(x)?
    """

    def construct(self):
        # ========================================
        # TITLE
        # ========================================
        title = Text("The Product Rule", font_size=48)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait()

        # ========================================
        # QUESTION
        # ========================================
        question = Text(
            "How do we differentiate a product?",
            font_size=32,
            color=WHITE
        )
        question.next_to(title, DOWN, buff=0.6)

        self.play(FadeIn(question, shift=DOWN))
        self.wait()

        # ========================================
        # SETUP: Two functions
        # ========================================
        functions = VGroup(
            Tex("f(x) = 2 + 0.5x", color=BLUE, font_size=32),
            Tex("g(x) = 1 + 0.3x", color=YELLOW, font_size=32),
        )
        functions.arrange(RIGHT, buff=1.5)
        functions.next_to(question, DOWN, buff=0.8)

        for func in functions:
            self.play(Write(func))
            self.wait(0.5)

        # ========================================
        # THEIR DERIVATIVES
        # ========================================
        derivatives = VGroup(
            Tex("f'(x) = 0.5", color=BLUE, font_size=28),
            Tex("g'(x) = 0.3", color=YELLOW, font_size=28),
        )
        derivatives.arrange(RIGHT, buff=1.5)
        derivatives.next_to(functions, DOWN, buff=0.5)

        for deriv in derivatives:
            self.play(Write(deriv))
            self.wait(0.5)

        # ========================================
        # PRODUCT
        # ========================================
        product = Tex(
            "h(x) = f(x) \\cdot g(x)",
            font_size=36,
            color=GREEN
        )
        product.next_to(derivatives, DOWN, buff=1.0)

        self.play(Write(product))
        self.wait()

        # ========================================
        # CHALLENGE
        # ========================================
        challenge = Tex(
            "h'(x) = \\, ?",
            font_size=40,
            color=RED
        )
        challenge.next_to(product, DOWN, buff=0.6)

        challenge_box = SurroundingRectangle(challenge, buff=0.2, color=RED, stroke_width=2)

        self.play(Write(challenge))
        self.play(ShowCreation(challenge_box))
        self.wait()

        # ========================================
        # WRONG GUESS
        # ========================================
        wrong = Tex(
            "h'(x) = f'(x) \\cdot g'(x) \\quad \\text{?}",
            font_size=32,
            color=GREY_A
        )
        wrong.to_edge(DOWN).shift(UP * 0.5)

        self.play(FadeIn(wrong, shift=UP))
        self.wait()

        # Cross it out
        cross = Cross(wrong, stroke_width=8, color=RED)
        self.play(ShowCreation(cross))
        self.wait()

        no_text = Text("NO!", font_size=36, color=RED)
        no_text.next_to(cross, RIGHT, buff=0.5)

        self.play(Write(no_text))
        self.wait(2)


class AreaRectangle(Scene):
    """
    Scene 2: Use area of a rectangle to visualize the product.

    This scene shows f(x) and g(x) as dimensions of a rectangle, so their
    product is the area. Then we see how the area changes.
    """

    def construct(self):
        # ========================================
        # TITLE
        # ========================================
        title = Text("Geometric Intuition", font_size=42)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait()

        # ========================================
        # IDEA: Area = f × g
        # ========================================
        idea = Text(
            "Think of f(x) and g(x) as dimensions of a rectangle",
            font_size=28,
            color=GREY_A
        )
        idea.next_to(title, DOWN, buff=0.3)

        self.play(FadeIn(idea, shift=DOWN))
        self.wait()

        # ========================================
        # RECTANGLE at x = 2
        # ========================================
        x_val = 2.0
        f_val = f_func(x_val)
        g_val = g_func(x_val)

        # Create rectangle
        rect_width = f_val
        rect_height = g_val

        rectangle = Rectangle(
            width=rect_width,
            height=rect_height,
            color=GREEN,
            fill_opacity=0.3,
            stroke_width=2
        )
        rectangle.move_to(ORIGIN)

        self.play(ShowCreation(rectangle))
        self.wait()

        # ========================================
        # LABEL DIMENSIONS
        # ========================================
        # Bottom dimension
        bottom_brace = Brace(rectangle, DOWN)
        bottom_label = bottom_brace.get_text("f(x)", buff=0.1)
        bottom_label.set_color(BLUE)

        # Side dimension
        side_brace = Brace(rectangle, LEFT)
        side_label = side_brace.get_text("g(x)", buff=0.1)
        side_label.set_color(YELLOW)

        self.play(
            GrowFromCenter(bottom_brace),
            Write(bottom_label)
        )
        self.play(
            GrowFromCenter(side_brace),
            Write(side_label)
        )
        self.wait()

        # ========================================
        # AREA LABEL
        # ========================================
        area_label = Tex(
            "\\text{Area} = f(x) \\cdot g(x)",
            font_size=32,
            color=GREEN
        )
        area_label.move_to(rectangle.get_center())

        self.play(Write(area_label))
        self.wait()

        # ========================================
        # INCREASE x BY dx
        # ========================================
        self.play(FadeOut(idea))

        change_text = Text(
            "Now increase x by a small amount dx",
            font_size=28,
            color=RED
        )
        change_text.next_to(title, DOWN, buff=0.3)

        self.play(FadeIn(change_text, shift=DOWN))
        self.wait()

        # ========================================
        # NEW RECTANGLE
        # ========================================
        dx = 1.0
        new_x = x_val + dx

        new_f = f_func(new_x)
        new_g = g_func(new_x)

        df = new_f - f_val
        dg = new_g - g_val

        # Extensions
        # Right extension (f changes)
        right_extension = Rectangle(
            width=df,
            height=g_val,
            color=BLUE,
            fill_opacity=0.5,
            stroke_width=2
        )
        right_extension.next_to(rectangle, RIGHT, buff=0)

        # Top extension (g changes)
        top_extension = Rectangle(
            width=f_val,
            height=dg,
            color=YELLOW,
            fill_opacity=0.5,
            stroke_width=2
        )
        top_extension.next_to(rectangle, UP, buff=0, aligned_edge=LEFT)

        # Corner piece (both change)
        corner = Rectangle(
            width=df,
            height=dg,
            color=RED,
            fill_opacity=0.5,
            stroke_width=2
        )
        corner.next_to(rectangle, UP + RIGHT, buff=0)

        self.play(FadeOut(area_label))
        self.play(ShowCreation(right_extension))
        self.wait()

        self.play(ShowCreation(top_extension))
        self.wait()

        self.play(ShowCreation(corner))
        self.wait()

        # ========================================
        # LABEL CHANGES
        # ========================================
        # Label right extension
        right_label = Tex("g(x) \\cdot df", font_size=24, color=BLUE)
        right_label.move_to(right_extension.get_center())

        # Label top extension
        top_label = Tex("f(x) \\cdot dg", font_size=24, color=YELLOW)
        top_label.move_to(top_extension.get_center())

        # Label corner
        corner_label = Tex("df \\cdot dg", font_size=20, color=RED)
        corner_label.move_to(corner.get_center())

        self.play(Write(right_label), Write(top_label), Write(corner_label))
        self.wait()

        # ========================================
        # TOTAL CHANGE
        # ========================================
        self.play(FadeOut(change_text))

        total_change = Tex(
            "d(\\text{Area}) = g \\cdot df + f \\cdot dg + df \\cdot dg",
            font_size=28
        )
        total_change.to_edge(DOWN).shift(UP * 1.0)

        self.play(Write(total_change))
        self.wait()

        # ========================================
        # IGNORE SMALL TERM
        # ========================================
        ignore = Text(
            "As dx → 0, the corner term df·dg becomes negligible",
            font_size=24,
            color=GREY_A
        )
        ignore.next_to(total_change, DOWN, buff=0.3)

        self.play(FadeIn(ignore, shift=UP))
        self.play(corner.animate.set_fill(opacity=0.1))
        self.wait(2)


class ProductRuleFormula(Scene):
    """
    Scene 3: Derive the product rule formula.

    This scene formalizes the geometric insight into the algebraic formula
    for the product rule.
    """

    def construct(self):
        # ========================================
        # TITLE
        # ========================================
        title = Text("The Product Rule Formula", font_size=42)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait()

        # ========================================
        # FROM GEOMETRY
        # ========================================
        geometry_recap = Tex(
            "d(fg) = g \\cdot df + f \\cdot dg + df \\cdot dg",
            font_size=32
        )
        geometry_recap.next_to(title, DOWN, buff=0.8)

        self.play(Write(geometry_recap))
        self.wait()

        # ========================================
        # DIVIDE BY dx
        # ========================================
        divide_text = Text("Divide both sides by dx:", font_size=28)
        divide_text.next_to(geometry_recap, DOWN, buff=0.6)

        self.play(FadeIn(divide_text, shift=DOWN))
        self.wait()

        division = Tex(
            "\\frac{d(fg)}{dx} = g \\cdot \\frac{df}{dx} + f \\cdot \\frac{dg}{dx} + \\frac{df}{dx} \\cdot dg",
            font_size=30
        )
        division.next_to(divide_text, DOWN, buff=0.5)

        self.play(Write(division))
        self.wait()

        # ========================================
        # AS dx → 0
        # ========================================
        limit_text = Text("As dx → 0, the last term vanishes:", font_size=26)
        limit_text.next_to(division, DOWN, buff=0.6)

        self.play(FadeIn(limit_text, shift=DOWN))
        self.wait()

        # Highlight the term that vanishes
        vanish_box = SurroundingRectangle(
            division[-8:],  # Last term
            color=RED,
            stroke_width=2
        )
        self.play(ShowCreation(vanish_box))
        self.wait()

        self.play(FadeOut(vanish_box))

        # ========================================
        # FINAL FORMULA
        # ========================================
        self.play(
            FadeOut(geometry_recap),
            FadeOut(divide_text),
            FadeOut(division),
            FadeOut(limit_text)
        )

        formula_label = Text("Product Rule:", font_size=32, color=GREEN)
        formula_label.next_to(title, DOWN, buff=1.0)

        formula = Tex(
            "\\frac{d}{dx}[f(x) \\cdot g(x)] = f'(x) \\cdot g(x) + f(x) \\cdot g'(x)",
            font_size=40,
            color=GREEN
        )
        formula.next_to(formula_label, DOWN, buff=0.6)

        formula_box = SurroundingRectangle(formula, buff=0.3, color=GREEN, stroke_width=3)

        self.play(Write(formula_label))
        self.play(Write(formula))
        self.play(ShowCreation(formula_box))
        self.wait()

        # ========================================
        # ALTERNATIVE NOTATION
        # ========================================
        alternative = Tex(
            "(fg)' = f'g + fg'",
            font_size=36,
            color=YELLOW
        )
        alternative.next_to(formula, DOWN, buff=0.8)

        alt_label = Text("Shorthand:", font_size=24, color=GREY_A)
        alt_label.next_to(alternative, UP, buff=0.3)

        self.play(Write(alt_label))
        self.play(Write(alternative))
        self.wait()

        # ========================================
        # MEMORY AID
        # ========================================
        memory = VGroup(
            Text("Memory aid:", font_size=26),
            Text("\"Derivative of first times second", font_size=22),
            Text("plus first times derivative of second\"", font_size=22),
        )
        memory.arrange(DOWN, buff=0.2, aligned_edge=LEFT)
        memory.to_edge(DOWN).shift(UP * 0.5)

        for line in memory:
            self.play(FadeIn(line, shift=UP))
            self.wait(0.4)

        self.wait(2)


class Examples(Scene):
    """
    Scene 4: Show concrete examples of the product rule.

    This scene applies the product rule to several examples to demonstrate
    how to use it in practice.
    """

    def construct(self):
        # ========================================
        # TITLE
        # ========================================
        title = Text("Examples", font_size=42)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait()

        # ========================================
        # FORMULA REMINDER
        # ========================================
        formula = Tex(
            "(fg)' = f'g + fg'",
            font_size=32,
            color=GREY_A
        )
        formula.next_to(title, DOWN, buff=0.3)

        self.play(Write(formula))
        self.wait()

        # ========================================
        # EXAMPLE 1: x² · x³
        # ========================================
        ex1_title = Text("Example 1:", font_size=28, color=BLUE)
        ex1_title.next_to(formula, DOWN, buff=0.8)

        ex1 = Tex(
            "\\frac{d}{dx}[x^2 \\cdot x^3]",
            font_size=32
        )
        ex1.next_to(ex1_title, DOWN, buff=0.3)

        self.play(Write(ex1_title), Write(ex1))
        self.wait()

        # Apply product rule
        ex1_step1 = Tex(
            "= (2x) \\cdot x^3 + x^2 \\cdot (3x^2)",
            font_size=32
        )
        ex1_step1.next_to(ex1, DOWN, buff=0.2, aligned_edge=LEFT)

        self.play(Write(ex1_step1))
        self.wait()

        # Simplify
        ex1_step2 = Tex(
            "= 2x^4 + 3x^4 = 5x^4",
            font_size=32,
            color=GREEN
        )
        ex1_step2.next_to(ex1_step1, DOWN, buff=0.2, aligned_edge=LEFT)

        self.play(Write(ex1_step2))
        self.wait()

        # Note
        note1 = Text(
            "(Same as d/dx[x⁵] = 5x⁴ from power rule)",
            font_size=20,
            color=GREY_A
        )
        note1.next_to(ex1_step2, DOWN, buff=0.2, aligned_edge=LEFT)

        self.play(FadeIn(note1, shift=UP))
        self.wait(2)

        # ========================================
        # EXAMPLE 2: x · sin(x)
        # ========================================
        self.play(
            FadeOut(ex1_title),
            FadeOut(ex1),
            FadeOut(ex1_step1),
            FadeOut(ex1_step2),
            FadeOut(note1)
        )

        ex2_title = Text("Example 2:", font_size=28, color=YELLOW)
        ex2_title.next_to(formula, DOWN, buff=0.8)

        ex2 = Tex(
            "\\frac{d}{dx}[x \\cdot \\sin(x)]",
            font_size=32
        )
        ex2.next_to(ex2_title, DOWN, buff=0.3)

        self.play(Write(ex2_title), Write(ex2))
        self.wait()

        # Identify f and g
        identify = VGroup(
            Tex("f(x) = x, \\quad f'(x) = 1", font_size=26),
            Tex("g(x) = \\sin(x), \\quad g'(x) = \\cos(x)", font_size=26),
        )
        identify.arrange(DOWN, buff=0.2, aligned_edge=LEFT)
        identify.next_to(ex2, DOWN, buff=0.4)

        for line in identify:
            self.play(Write(line))
            self.wait(0.3)

        # Apply product rule
        ex2_step1 = Tex(
            "= (1) \\cdot \\sin(x) + x \\cdot \\cos(x)",
            font_size=32
        )
        ex2_step1.next_to(identify, DOWN, buff=0.4, aligned_edge=LEFT)

        self.play(Write(ex2_step1))
        self.wait()

        # Simplify
        ex2_step2 = Tex(
            "= \\sin(x) + x\\cos(x)",
            font_size=32,
            color=GREEN
        )
        ex2_step2.next_to(ex2_step1, DOWN, buff=0.2, aligned_edge=LEFT)

        self.play(Write(ex2_step2))
        self.wait(2)

        # ========================================
        # EXAMPLE 3: e^x · x²
        # ========================================
        self.play(
            FadeOut(ex2_title),
            FadeOut(ex2),
            FadeOut(identify),
            FadeOut(ex2_step1),
            FadeOut(ex2_step2)
        )

        ex3_title = Text("Example 3:", font_size=28, color=RED)
        ex3_title.next_to(formula, DOWN, buff=0.8)

        ex3 = Tex(
            "\\frac{d}{dx}[e^x \\cdot x^2]",
            font_size=32
        )
        ex3.next_to(ex3_title, DOWN, buff=0.3)

        self.play(Write(ex3_title), Write(ex3))
        self.wait()

        # Apply product rule
        ex3_step1 = Tex(
            "= e^x \\cdot x^2 + e^x \\cdot 2x",
            font_size=32
        )
        ex3_step1.next_to(ex3, DOWN, buff=0.2, aligned_edge=LEFT)

        self.play(Write(ex3_step1))
        self.wait()

        # Factor
        ex3_step2 = Tex(
            "= e^x(x^2 + 2x)",
            font_size=32,
            color=GREEN
        )
        ex3_step2.next_to(ex3_step1, DOWN, buff=0.2, aligned_edge=LEFT)

        self.play(Write(ex3_step2))
        self.wait()

        # ========================================
        # SUMMARY
        # ========================================
        self.play(
            FadeOut(ex3_title),
            FadeOut(ex3),
            FadeOut(ex3_step1),
            FadeOut(ex3_step2)
        )

        summary = VGroup(
            Text("Key Points:", font_size=28, color=WHITE),
            Text("• Product rule: (fg)' = f'g + fg'", font_size=24),
            Text("• Two terms, one for each function's derivative", font_size=24),
            Text("• Essential for differentiating products", font_size=24),
            Text("• Combines with chain rule for complex expressions", font_size=24),
        )
        summary.arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        summary.next_to(formula, DOWN, buff=0.8)

        for item in summary:
            self.play(FadeIn(item, shift=UP))
            self.wait(0.4)

        self.wait(2)


# ============================================================
# 5. SCENE SUMMARY AND EXECUTION ORDER
# ============================================================
#
# Scene 1 (IntroduceProduct):
#   - Introduces two functions f(x) and g(x)
#   - Poses the question of differentiating their product
#   - Shows that (fg)' ≠ f'g' in general
#
# Scene 2 (AreaRectangle):
#   - Uses area of rectangle to visualize product
#   - Shows how area changes when both dimensions change
#   - Identifies two main terms plus small corner term
#
# Scene 3 (ProductRuleFormula):
#   - Formalizes the geometric insight
#   - Derives (fg)' = f'g + fg'
#   - Presents the formula and memory aid
#
# Scene 4 (Examples):
#   - Shows three concrete examples
#   - Demonstrates how to apply the product rule
#   - Summarizes key points

SCENE_ORDER = [
    IntroduceProduct,      # Part 1: The problem
    AreaRectangle,         # Part 2: Geometric visualization
    ProductRuleFormula,    # Part 3: The formula
    Examples,              # Part 4: Applications
]
