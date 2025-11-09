"""
Implicit Differentiation

This module demonstrates implicit differentiation, a technique for finding derivatives
when the relationship between variables is given implicitly rather than explicitly.
Covers various examples including circles, ellipses, and the folium of Descartes.

Scenes:
    - IntroduceImplicitCurve: Introduction to implicit vs explicit functions
    - ExplicitVsImplicit: Comparing explicit y=f(x) with implicit F(x,y)=0
    - DerivativeFormula: Deriving the implicit differentiation formula
    - CircleExample: Detailed example using a circle equation
"""

from manimlib import *
import numpy as np


class IntroduceImplicitCurve(Scene):
    """
    Introduce the concept of implicit curves and why we need implicit differentiation.
    """

    def construct(self):
        # Title
        title = OldTexText("Implicit Differentiation", font_size=60)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait()

        # Show examples of explicit vs implicit
        explicit_label = OldTexText("Explicit Function:", font_size=36, color=BLUE)
        explicit_label.move_to(3 * UP + 3 * LEFT)
        explicit_eq = Tex(R"y = \sqrt{1 - x^2}", font_size=40)
        explicit_eq.next_to(explicit_label, DOWN)

        implicit_label = OldTexText("Implicit Function:", font_size=36, color=GREEN)
        implicit_label.move_to(3 * UP + 3 * RIGHT)
        implicit_eq = Tex(R"x^2 + y^2 = 1", font_size=40)
        implicit_eq.next_to(implicit_label, DOWN)

        self.play(
            Write(explicit_label),
            Write(implicit_label)
        )
        self.wait(0.5)
        self.play(
            Write(explicit_eq),
            Write(implicit_eq)
        )
        self.wait(2)

        # Create coordinate plane
        plane = NumberPlane(
            x_range=[-2, 2, 0.5],
            y_range=[-2, 2, 0.5],
            height=5,
            width=5,
            background_line_style={
                "stroke_color": BLUE_E,
                "stroke_width": 1,
            }
        )
        plane.shift(DOWN * 0.5)

        # Draw the circle using implicit equation
        circle = Circle(radius=1.5, color=YELLOW)
        circle.move_to(plane.c2p(0, 0))

        # Clear and show the circle
        self.play(
            FadeOut(explicit_label),
            FadeOut(explicit_eq),
            FadeOut(implicit_label),
            FadeOut(implicit_eq)
        )
        self.play(ShowCreation(plane))
        self.wait(0.5)

        # Show the equation
        equation = Tex(R"x^2 + y^2 = 1", font_size=48, color=YELLOW)
        equation.next_to(plane, RIGHT, buff=1)

        self.play(Write(equation))
        self.play(ShowCreation(circle), run_time=2)
        self.wait()

        # Show a point on the circle
        t_value = ValueTracker(PI / 4)
        dot = always_redraw(lambda: Dot(
            plane.c2p(1.5 * np.cos(t_value.get_value()), 1.5 * np.sin(t_value.get_value())),
            color=RED,
            radius=0.08
        ))

        # Tangent line
        def get_tangent_line():
            t = t_value.get_value()
            x0, y0 = 1.5 * np.cos(t), 1.5 * np.sin(t)
            # For circle x^2 + y^2 = r^2, slope is -x/y
            if abs(y0) > 0.01:
                slope = -x0 / y0
                x_range = np.array([-0.8, 0.8])
                y_range = y0 + slope * x_range
                points = [plane.c2p(x0 + dx, y) for dx, y in zip(x_range, y_range)]
                return Line(points[0], points[1], color=RED, stroke_width=3)
            else:
                return Line(
                    plane.c2p(x0, -0.8),
                    plane.c2p(x0, 0.8),
                    color=RED,
                    stroke_width=3
                )

        tangent = always_redraw(get_tangent_line)

        self.play(FadeIn(dot))
        self.wait(0.5)
        self.play(ShowCreation(tangent))
        self.wait()

        # Question
        question = OldTexText("What is the slope of the tangent?", font_size=32, color=RED)
        question.next_to(equation, DOWN, buff=0.5)
        self.play(Write(question))
        self.wait()

        # Animate the point moving around the circle
        self.play(t_value.animate.set_value(3 * PI / 4), run_time=3, rate_func=linear)
        self.wait(0.5)
        self.play(t_value.animate.set_value(5 * PI / 4), run_time=2, rate_func=linear)
        self.wait(0.5)
        self.play(t_value.animate.set_value(PI / 4), run_time=2, rate_func=linear)
        self.wait(2)


class ExplicitVsImplicit(Scene):
    """
    Compare explicit and implicit representations and their derivatives.
    """

    def construct(self):
        # Title
        title = OldTexText("Explicit vs Implicit", font_size=52)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait()

        # Left side: Explicit
        explicit_title = OldTexText("Explicit Form", font_size=40, color=BLUE)
        explicit_title.move_to(3 * UP + 3.5 * LEFT)

        explicit_eq = Tex(R"y = f(x)", font_size=44)
        explicit_eq.next_to(explicit_title, DOWN, buff=0.5)

        explicit_example = Tex(R"y = x^2 + 3x", font_size=38)
        explicit_example.next_to(explicit_eq, DOWN, buff=0.7)

        explicit_deriv = Tex(R"\frac{dy}{dx} = 2x + 3", font_size=38, color=BLUE)
        explicit_deriv.next_to(explicit_example, DOWN, buff=0.5)

        explicit_label = OldTexText("Direct differentiation", font_size=28, color=GREY)
        explicit_label.next_to(explicit_deriv, DOWN, buff=0.3)

        explicit_group = VGroup(
            explicit_title, explicit_eq, explicit_example, explicit_deriv, explicit_label
        )

        # Right side: Implicit
        implicit_title = OldTexText("Implicit Form", font_size=40, color=GREEN)
        implicit_title.move_to(3 * UP + 3.5 * RIGHT)

        implicit_eq = Tex(R"F(x, y) = 0", font_size=44)
        implicit_eq.next_to(implicit_title, DOWN, buff=0.5)

        implicit_example = Tex(R"x^2 + y^2 = 25", font_size=38)
        implicit_example.next_to(implicit_eq, DOWN, buff=0.7)

        implicit_deriv = Tex(
            R"\frac{dy}{dx} = -\frac{\frac{\partial F}{\partial x}}{\frac{\partial F}{\partial y}}",
            font_size=38,
            color=GREEN
        )
        implicit_deriv.next_to(implicit_example, DOWN, buff=0.5)

        implicit_label = OldTexText("Implicit differentiation", font_size=28, color=GREY)
        implicit_label.next_to(implicit_deriv, DOWN, buff=0.3)

        implicit_group = VGroup(
            implicit_title, implicit_eq, implicit_example, implicit_deriv, implicit_label
        )

        # Animate both sides
        self.play(Write(explicit_title), Write(implicit_title))
        self.wait(0.5)
        self.play(Write(explicit_eq), Write(implicit_eq))
        self.wait()
        self.play(Write(explicit_example), Write(implicit_example))
        self.wait()

        # Highlight the challenge
        challenge = OldTexText(
            "Sometimes y cannot be solved explicitly!",
            font_size=36,
            color=YELLOW
        )
        challenge.move_to(DOWN * 0.5)

        examples = VGroup(
            Tex(R"x^3 + y^3 = 6xy", font_size=32),
            Tex(R"e^y + xy = x^2", font_size=32),
            Tex(R"\sin(xy) + y = x", font_size=32)
        )
        examples.arrange(RIGHT, buff=1.0)
        examples.next_to(challenge, DOWN, buff=0.5)

        self.play(Write(challenge))
        self.wait(0.5)
        self.play(LaggedStart([Write(ex) for ex in examples], lag_ratio=0.3))
        self.wait(2)

        # Clear and show derivatives
        self.play(
            FadeOut(challenge),
            FadeOut(examples)
        )
        self.play(Write(explicit_deriv), Write(implicit_deriv))
        self.wait(0.5)
        self.play(Write(explicit_label), Write(implicit_label))
        self.wait(2)

        # Highlight the implicit derivative formula
        box = SurroundingRectangle(implicit_deriv, color=YELLOW, buff=0.15)
        self.play(ShowCreation(box))
        self.wait(2)


class DerivativeFormula(Scene):
    """
    Derive the implicit differentiation formula step by step.
    """

    def construct(self):
        # Title
        title = OldTexText("The Implicit Differentiation Formula", font_size=50)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait()

        # Start with an implicit equation
        step1 = Tex(R"F(x, y) = 0", font_size=48)
        step1.move_to(2.5 * UP)
        self.play(Write(step1))
        self.wait()

        # Explain that y is a function of x
        note = OldTexText("y is implicitly a function of x: y = y(x)", font_size=32, color=GREY)
        note.next_to(step1, DOWN, buff=0.4)
        self.play(Write(note))
        self.wait(2)
        self.play(FadeOut(note))

        # Take derivative with respect to x
        step2_label = OldTexText("Differentiate both sides with respect to x:", font_size=32)
        step2_label.move_to(1.2 * UP)

        step2 = Tex(
            R"\frac{d}{dx}[F(x, y)] = \frac{d}{dx}[0]",
            font_size=44
        )
        step2.next_to(step2_label, DOWN, buff=0.3)

        self.play(Write(step2_label))
        self.wait(0.5)
        self.play(TransformFromCopy(step1, step2))
        self.wait()

        # Apply chain rule
        step3_label = OldTexText("Apply the chain rule:", font_size=32)
        step3_label.move_to(0.2 * DOWN)

        step3 = Tex(
            R"\frac{\partial F}{\partial x} + \frac{\partial F}{\partial y} \cdot \frac{dy}{dx} = 0",
            font_size=44
        )
        step3.next_to(step3_label, DOWN, buff=0.3)

        self.play(Write(step3_label))
        self.wait(0.5)
        self.play(Write(step3))
        self.wait(2)

        # Highlight the dy/dx term
        box1 = SurroundingRectangle(step3[0][19:24], color=YELLOW, buff=0.05)
        self.play(ShowCreation(box1))
        self.wait()
        self.play(FadeOut(box1))

        # Solve for dy/dx
        step4_label = OldTexText("Solve for dy/dx:", font_size=32)
        step4_label.move_to(1.8 * DOWN)

        step4 = Tex(
            R"\frac{dy}{dx} = -\frac{\frac{\partial F}{\partial x}}{\frac{\partial F}{\partial y}}",
            font_size=48,
            color=GREEN
        )
        step4.next_to(step4_label, DOWN, buff=0.3)

        self.play(Write(step4_label))
        self.wait(0.5)
        self.play(Write(step4))
        self.wait()

        # Highlight the final formula
        box2 = SurroundingRectangle(step4, color=YELLOW, buff=0.2)
        self.play(ShowCreation(box2))
        self.wait(2)

        # Alternative notation
        alt_note = OldTexText("Also written as:", font_size=28, color=GREY)
        alt_note.move_to(3.2 * DOWN + 3 * LEFT)

        alt_form = Tex(
            R"\frac{dy}{dx} = -\frac{F_x}{F_y}",
            font_size=40
        )
        alt_form.next_to(alt_note, RIGHT, buff=0.5)

        self.play(Write(alt_note), Write(alt_form))
        self.wait(3)


class CircleExample(Scene):
    """
    Detailed example of implicit differentiation applied to a circle.
    """

    def construct(self):
        # Title
        title = OldTexText("Example: Circle", font_size=52)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait()

        # The equation
        equation = Tex(R"x^2 + y^2 = 25", font_size=48)
        equation.next_to(title, DOWN, buff=0.5)
        self.play(Write(equation))
        self.wait()

        # Identify F(x,y)
        F_label = Tex(R"F(x, y) = x^2 + y^2 - 25", font_size=40)
        F_label.next_to(equation, DOWN, buff=0.7)
        self.play(Write(F_label))
        self.wait()

        # Compute partial derivatives
        partial_x = Tex(
            R"\frac{\partial F}{\partial x} = 2x",
            font_size=40,
            color=BLUE
        )
        partial_x.move_to(0.5 * UP + 3 * LEFT)

        partial_y = Tex(
            R"\frac{\partial F}{\partial y} = 2y",
            font_size=40,
            color=RED
        )
        partial_y.move_to(0.5 * UP + 3 * RIGHT)

        self.play(Write(partial_x), Write(partial_y))
        self.wait()

        # Apply the formula
        formula_label = OldTexText("Apply the formula:", font_size=32)
        formula_label.move_to(0.8 * DOWN)

        formula = Tex(
            R"\frac{dy}{dx} = -\frac{2x}{2y} = -\frac{x}{y}",
            font_size=44,
            color=GREEN
        )
        formula.next_to(formula_label, DOWN, buff=0.4)

        self.play(Write(formula_label))
        self.wait(0.5)
        self.play(Write(formula))
        self.wait(2)

        # Highlight the result
        box = SurroundingRectangle(formula, color=YELLOW, buff=0.15)
        self.play(ShowCreation(box))
        self.wait()

        # Specific example
        self.play(
            FadeOut(formula_label),
            FadeOut(box)
        )

        example_label = OldTexText("At point (3, 4):", font_size=36)
        example_label.move_to(2.5 * DOWN + 3 * LEFT)

        slope_calc = Tex(
            R"\frac{dy}{dx}\bigg|_{(3,4)} = -\frac{3}{4}",
            font_size=40,
            color=YELLOW
        )
        slope_calc.next_to(example_label, RIGHT, buff=0.5)

        self.play(Write(example_label), Write(slope_calc))
        self.wait(2)

        # Visual representation
        plane = NumberPlane(
            x_range=[-6, 6, 1],
            y_range=[-6, 6, 1],
            height=4,
            width=4,
            background_line_style={
                "stroke_color": BLUE_E,
                "stroke_width": 1,
            }
        )
        plane.scale(0.5).to_corner(DR)

        circle = Circle(radius=2.5, color=YELLOW)
        circle.move_to(plane.c2p(0, 0))

        # Point (3, 4) on the circle of radius 5
        # Scale to plane: radius 5 -> 2.5 on plane
        point = Dot(plane.c2p(3 * 0.5, 4 * 0.5), color=RED, radius=0.06)

        # Tangent line with slope -3/4
        tangent = Line(
            plane.c2p(3 * 0.5 - 1, 4 * 0.5 + 0.75),
            plane.c2p(3 * 0.5 + 1, 4 * 0.5 - 0.75),
            color=RED,
            stroke_width=2
        )

        self.play(ShowCreation(plane), run_time=0.5)
        self.play(ShowCreation(circle), run_time=1)
        self.play(FadeIn(point))
        self.play(ShowCreation(tangent))
        self.wait(3)


# Additional utility functions for implicit curves

def evaluate_implicit_curve(func, x_range, y_range, resolution=100):
    """
    Evaluate an implicit function F(x,y) = 0 over a grid.

    Args:
        func: Function that takes (x, y) and returns F(x, y)
        x_range: Tuple (x_min, x_max)
        y_range: Tuple (y_min, y_max)
        resolution: Number of points in each direction

    Returns:
        x, y, z arrays for contour plotting
    """
    x = np.linspace(x_range[0], x_range[1], resolution)
    y = np.linspace(y_range[0], y_range[1], resolution)
    X, Y = np.meshgrid(x, y)
    Z = func(X, Y)
    return X, Y, Z


def folium_of_descartes(a=1):
    """
    Create the folium of Descartes curve: x^3 + y^3 = 3axy

    Args:
        a: Parameter controlling the size of the loop

    Returns:
        Function that evaluates the implicit equation
    """
    return lambda x, y: x**3 + y**3 - 3*a*x*y


def implicit_derivative_numerical(func, x, y, dx=1e-6):
    """
    Numerically compute dy/dx for implicit function F(x,y) = 0.

    Args:
        func: Function F(x, y)
        x, y: Point at which to evaluate the derivative
        dx: Small increment for numerical differentiation

    Returns:
        dy/dx at the point (x, y)
    """
    F_x = (func(x + dx, y) - func(x - dx, y)) / (2 * dx)
    F_y = (func(x, y + dx) - func(x, y - dx)) / (2 * dx)

    if abs(F_y) < 1e-10:
        return np.inf if F_y >= 0 else -np.inf

    return -F_x / F_y
