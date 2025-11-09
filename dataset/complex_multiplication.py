"""
Natural Group Name: Complex Number Multiplication

Educational Objectives:
- To visualize complex numbers as points in the complex plane
- To demonstrate that multiplying by a complex number combines rotation and scaling
- To build geometric intuition for complex multiplication
- To connect algebraic operations to geometric transformations

Story Arc & Intent:
The animation reveals the beautiful geometric interpretation of complex multiplication:
multiplying by a complex number rotates and scales simultaneously. This transforms
an abstract algebraic operation into an intuitive geometric transformation.

Narrative Flow:
- Hook/Opening: Complex numbers plotted as points in the plane
- Development: Show multiplication by simple complex numbers (i, -1, 2+i)
- Build-up: Demonstrate the rotation and scaling effects
- Climax: General pattern - multiply by r·e^(iθ) rotates by θ and scales by r
- Resolution: Connect back to polar form and Euler's formula

Technical Implementation Notes:
- Scene Classes: IntroduceComplexPlane, MultiplyByI, GeneralMultiplication, PolarForm
- Key Visual Elements: Complex plane, vectors, rotation arcs, scaling animations
- Animation Techniques: Rotation, scaling, vector field transformations
- Mathematical Concepts: Complex numbers, polar coordinates, Euler's formula

Dependency Chain:
All scenes use basic manimlib components: NumberPlane, Arrow, Dot, Text, Tex.
No custom utilities required.

Rendering Instructions:
To render these scenes, use the manim command-line tool:
- For a single scene: manimgl complex_multiplication.py IntroduceComplexPlane
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
# - BLUE: Original vectors/points
# - YELLOW: Transformed vectors/points after multiplication
# - GREEN: Multiplication factor (the complex number we're multiplying by)
# - RED: Rotation arc
# - WHITE: Axes and grid
# - GREY_A: De-emphasized elements
#
# Key Manim Constants Used:
# - UP, DOWN, LEFT, RIGHT: Direction vectors
# - ORIGIN: Complex number 0
# - TAU: 2π for angle calculations
# - DEGREES: Angle conversion

# Plane configuration
PLANE_CONFIG = {
    "x_range": (-4, 4, 1),
    "y_range": (-4, 4, 1),
    "width": 10,
    "height": 10,
}

# Vector styling
VECTOR_CONFIG = {
    "buff": 0,
    "stroke_width": 4,
    "max_tip_length_to_length_ratio": 0.15,
}

# ============================================================
# 3. UTILITY FUNCTIONS
# ============================================================

def complex_to_point(z):
    """
    Convert a complex number to a point in the plane.

    Args:
        z: Complex number

    Returns:
        3D numpy array representing the point
    """
    return np.array([z.real, z.imag, 0])

def point_to_complex(point):
    """
    Convert a point to a complex number.

    Args:
        point: 3D numpy array

    Returns:
        Complex number
    """
    return complex(point[0], point[1])

def create_complex_vector(plane, z, color=BLUE, **kwargs):
    """
    Create a vector representing a complex number.

    Args:
        plane: NumberPlane object
        z: Complex number
        color: Color of the vector
        **kwargs: Additional arguments for Arrow

    Returns:
        Arrow from origin to z
    """
    config = VECTOR_CONFIG.copy()
    config.update(kwargs)

    return Arrow(
        plane.n2p(0),
        plane.n2p(z),
        color=color,
        **config
    )

def create_complex_label(plane, z, text=None, direction=UR, buff=0.1, **kwargs):
    """
    Create a label for a complex number.

    Args:
        plane: NumberPlane object
        z: Complex number
        text: Text to display (None = auto-format)
        direction: Direction to place label
        buff: Buffer from the point
        **kwargs: Additional arguments for Tex

    Returns:
        Tex mobject positioned near z
    """
    if text is None:
        # Auto-format based on the complex number
        if z.imag == 0:
            text = f"{z.real:.1f}"
        elif z.real == 0:
            if z.imag == 1:
                text = "i"
            elif z.imag == -1:
                text = "-i"
            else:
                text = f"{z.imag:.1f}i"
        else:
            sign = "+" if z.imag >= 0 else "-"
            text = f"{z.real:.1f} {sign} {abs(z.imag):.1f}i"

    label = Tex(text, **kwargs)
    label.next_to(plane.n2p(z), direction, buff=buff)

    return label

def get_polar_form_text(r, theta):
    """
    Create text for polar form of complex number.

    Args:
        r: Magnitude
        theta: Angle in radians

    Returns:
        Tex mobject with polar form
    """
    theta_deg = int(np.degrees(theta))
    return Tex(f"{r:.1f} \\cdot e^{{i \\cdot {theta_deg}^\\circ}}")

# ============================================================
# 4. BASE CLASSES AND HELPERS
# ============================================================
# No custom base classes needed

# ============================================================
# 5. SCENE IMPLEMENTATIONS
# ============================================================

class IntroduceComplexPlane(InteractiveScene):
    """
    Part 1: Introduce the complex plane and plot complex numbers.

    Narrative purpose:
        To establish the complex plane as a geometric space where complex numbers
        are points, setting up the geometric interpretation.

    Mathematical content:
        Complex numbers z = a + bi are points (a, b) in the plane,
        with real part on x-axis and imaginary part on y-axis.

    Visual approach:
        Show the plane, plot several complex numbers, and label the axes clearly.
    """
    def construct(self):
        # ========================================
        # SETUP: Title
        # ========================================
        title = Text("The Complex Plane", font_size=48)
        title.to_edge(UP)

        self.play(FadeIn(title, shift=DOWN))
        self.wait()

        # ========================================
        # CREATE: Complex plane
        # ========================================
        plane = NumberPlane(**PLANE_CONFIG)
        plane.add_coordinates()

        # Axis labels
        real_label = Tex("\\text{Real}", font_size=36)
        real_label.next_to(plane.x_axis.get_right(), DOWN)

        imag_label = Tex("\\text{Imaginary}", font_size=36)
        imag_label.next_to(plane.y_axis.get_top(), RIGHT)

        self.play(
            ShowCreation(plane),
            run_time=2
        )
        self.play(
            FadeIn(real_label, shift=UP),
            FadeIn(imag_label, shift=LEFT)
        )
        self.wait()

        # ========================================
        # PLOT: Several complex numbers
        # ========================================
        numbers = [
            (2 + 1j, BLUE, "2+i"),
            (-1 + 2j, TEAL, "-1+2i"),
            (1 - 1.5j, YELLOW, "1-1.5i"),
            (-2 - 1j, GREEN, "-2-i"),
        ]

        dots = VGroup()
        labels = VGroup()

        for z, color, text in numbers:
            # Create dot
            dot = Dot(plane.n2p(z), color=color)
            dot.set_sheen(-0.3, DR)

            # Create label
            label = Tex(text, font_size=28, color=color)
            direction = UR if z.real > 0 else UL
            label.next_to(dot, direction, buff=0.15)

            dots.add(dot)
            labels.add(label)

        self.play(
            LaggedStart(*[GrowFromCenter(dot) for dot in dots], lag_ratio=0.3),
            LaggedStart(*[FadeIn(label) for label in labels], lag_ratio=0.3),
            run_time=2
        )
        self.wait(2)

        # ========================================
        # MESSAGE: Complex numbers as points
        # ========================================
        message = Text(
            "Complex numbers are points in the plane",
            font_size=36,
            color=GREY_A
        )
        message.to_edge(DOWN, buff=0.5)

        self.play(FadeIn(message, shift=UP))
        self.wait(2)


class MultiplyByI(InteractiveScene):
    """
    Part 2: Show what happens when we multiply by i.

    Narrative purpose:
        To introduce the geometric effect of complex multiplication with the
        simplest non-trivial example: multiplying by i rotates by 90°.

    Mathematical content:
        Multiplying any complex number by i = e^(iπ/2) rotates it 90° counterclockwise.
        Example: (2+i) * i = 2i + i² = -1 + 2i

    Visual approach:
        Show a vector, multiply it by i, and animate the rotation.
    """
    def construct(self):
        # ========================================
        # SETUP: Title
        # ========================================
        title = Text("Multiplying by i", font_size=48)
        title.to_edge(UP)

        self.add(title)

        # ========================================
        # CREATE: Plane and initial vector
        # ========================================
        plane = NumberPlane(**PLANE_CONFIG)
        plane.add_coordinates()

        self.add(plane)

        # Initial complex number
        z1 = 2 + 1j
        vector1 = create_complex_vector(plane, z1, color=BLUE)
        label1 = create_complex_label(plane, z1, "2+i", font_size=36, color=BLUE)

        self.play(
            GrowArrow(vector1),
            FadeIn(label1)
        )
        self.wait()

        # ========================================
        # SHOW: Multiplication by i
        # ========================================
        equation = Tex("(2+i) \\times i = ?", font_size=42)
        equation.to_edge(DOWN, buff=1)

        self.play(Write(equation))
        self.wait()

        # ========================================
        # RESULT: After multiplication
        # ========================================
        z2 = z1 * 1j  # -1 + 2i
        vector2 = create_complex_vector(plane, z2, color=YELLOW)
        label2 = create_complex_label(plane, z2, "-1+2i", font_size=36, color=YELLOW)

        # Show rotation arc
        arc = Arc(
            start_angle=np.angle(z1),
            angle=PI/2,
            radius=abs(z1),
            color=RED,
            stroke_width=3
        )
        arc.shift(plane.n2p(0))

        self.play(
            Rotate(vector1, angle=PI/2, about_point=plane.n2p(0)),
            ShowCreation(arc),
            vector1.animate.set_color(YELLOW),
            label1.animate.become(label2),
            run_time=2
        )
        self.wait()

        # ========================================
        # RESULT: Show answer
        # ========================================
        answer = Tex("(2+i) \\times i = -1+2i", font_size=42)
        answer.move_to(equation)

        self.play(TransformMatchingStrings(equation, answer))
        self.wait()

        # ========================================
        # INSIGHT: Rotation by 90°
        # ========================================
        insight = Text(
            "Multiplying by i rotates 90° counterclockwise",
            font_size=36,
            color=GREEN
        )
        insight.next_to(answer, DOWN, buff=0.5)

        self.play(FadeIn(insight, shift=UP))
        self.wait(2)


class GeneralMultiplication(InteractiveScene):
    """
    Part 3: Show general multiplication combines rotation and scaling.

    Narrative purpose:
        To reveal the full geometric pattern: multiplying by any complex number
        both rotates and scales the input.

    Mathematical content:
        Multiplying by z = r·e^(iθ) scales by r and rotates by θ.

    Visual approach:
        Show several examples with different magnitudes and angles,
        demonstrating the combined rotation and scaling effect.
    """
    def construct(self):
        # ========================================
        # SETUP: Title
        # ========================================
        title = Text("General Complex Multiplication", font_size=48)
        title.to_edge(UP)

        self.add(title)

        # ========================================
        # CREATE: Plane
        # ========================================
        plane = NumberPlane(**PLANE_CONFIG)
        plane.add_coordinates()

        self.add(plane)

        # ========================================
        # EXAMPLE: Multiply 1+0i by 2e^(i·60°)
        # ========================================
        z_initial = 1 + 0j
        z_multiplier = 2 * np.exp(1j * PI/3)  # 2·e^(i·60°)

        # Initial vector
        vec_init = create_complex_vector(plane, z_initial, color=BLUE)
        label_init = create_complex_label(plane, z_initial, "1", font_size=36, color=BLUE)

        self.play(
            GrowArrow(vec_init),
            FadeIn(label_init)
        )
        self.wait()

        # Show multiplier
        multiplier_text = Tex(
            "\\times (1 + \\sqrt{3}i)",
            font_size=42,
            color=GREEN
        )
        multiplier_text.to_edge(DOWN, buff=1.5)

        self.play(Write(multiplier_text))
        self.wait()

        # ========================================
        # ANIMATE: Rotation and scaling
        # ========================================
        z_result = z_initial * z_multiplier
        vec_result = create_complex_vector(plane, z_result, color=YELLOW)

        # Show rotation arc
        arc = Arc(
            start_angle=0,
            angle=PI/3,
            radius=abs(z_initial),
            color=RED,
            stroke_width=3
        )
        arc.shift(plane.n2p(0))

        # Combined animation: rotate and scale
        self.play(
            Rotate(vec_init, angle=PI/3, about_point=plane.n2p(0)),
            vec_init.animate.scale(2, about_point=plane.n2p(0)).set_color(YELLOW),
            ShowCreation(arc),
            FadeOut(label_init),
            run_time=2.5
        )
        self.wait()

        # Label result
        label_result = create_complex_label(
            plane, z_result,
            "1 + \\sqrt{3}i",
            font_size=36,
            color=YELLOW
        )
        self.play(FadeIn(label_result))
        self.wait()

        # ========================================
        # INSIGHT: Rotation + Scaling
        # ========================================
        rotation_text = Text("Rotates by 60°", font_size=32, color=RED)
        rotation_text.next_to(arc, LEFT, buff=0.3)

        scaling_text = Text("Scales by 2×", font_size=32, color=BLUE)
        scaling_text.next_to(multiplier_text, DOWN, buff=0.3)

        self.play(
            FadeIn(rotation_text, shift=RIGHT),
            FadeIn(scaling_text, shift=UP)
        )
        self.wait(2)

        # ========================================
        # GENERAL PATTERN
        # ========================================
        general = Tex(
            "\\text{Multiply by } r e^{i\\theta} \\rightarrow \\text{ Scale by } r, \\text{ Rotate by } \\theta",
            font_size=36,
            color=YELLOW
        )
        general.to_edge(DOWN, buff=0.3)

        self.play(
            FadeOut(multiplier_text),
            FadeOut(scaling_text),
            FadeOut(rotation_text),
            FadeIn(general, shift=UP)
        )
        self.wait(3)


class PolarForm(InteractiveScene):
    """
    Part 4: Connect to polar form and Euler's formula.

    Narrative purpose:
        To tie together the geometric interpretation with the algebraic polar form,
        completing the conceptual picture.

    Mathematical content:
        z = r·e^(iθ) = r(cos θ + i sin θ)
        Multiplication in polar form: (r₁e^(iθ₁))(r₂e^(iθ₂)) = r₁r₂·e^(i(θ₁+θ₂))

    Visual approach:
        Show polar coordinates, Euler's formula, and how multiplication becomes
        simple in polar form.
    """
    def construct(self):
        # ========================================
        # SETUP: Title
        # ========================================
        title = Text("Polar Form & Euler's Formula", font_size=48)
        title.to_edge(UP)

        self.add(title)

        # ========================================
        # SHOW: A complex number in polar form
        # ========================================
        plane = NumberPlane(**PLANE_CONFIG)
        plane.add_coordinates()

        self.add(plane)

        # Example complex number
        r = 2.5
        theta = PI/3
        z = r * np.exp(1j * theta)

        # Vector
        vec = create_complex_vector(plane, z, color=BLUE)

        # Radius line
        radius_line = DashedLine(plane.n2p(0), plane.n2p(z), color=GREY_A)

        # Angle arc
        angle_arc = Arc(
            start_angle=0,
            angle=theta,
            radius=0.8,
            color=YELLOW,
            stroke_width=3
        )
        angle_arc.shift(plane.n2p(0))

        # Labels
        r_label = Tex("r", font_size=36, color=GREY_A)
        r_label.next_to(radius_line.get_center(), UL, buff=0.1)

        theta_label = Tex("\\theta", font_size=36, color=YELLOW)
        theta_label.next_to(angle_arc, RIGHT, buff=0.2)

        self.play(
            GrowArrow(vec),
            ShowCreation(radius_line),
            ShowCreation(angle_arc),
        )
        self.play(
            FadeIn(r_label),
            FadeIn(theta_label)
        )
        self.wait()

        # ========================================
        # EULER'S FORMULA
        # ========================================
        euler = Tex(
            "z = r e^{i\\theta} = r(\\cos\\theta + i\\sin\\theta)",
            font_size=42
        )
        euler.to_edge(DOWN, buff=1.5)

        box = SurroundingRectangle(euler, buff=0.2, color=YELLOW, stroke_width=2)

        self.play(
            Write(euler),
            ShowCreation(box)
        )
        self.wait(2)

        # ========================================
        # MULTIPLICATION RULE
        # ========================================
        mult_rule = Tex(
            "(r_1 e^{i\\theta_1})(r_2 e^{i\\theta_2}) = r_1 r_2 \\cdot e^{i(\\theta_1 + \\theta_2)}",
            font_size=38
        )
        mult_rule.next_to(euler, UP, buff=0.5)

        self.play(FadeIn(mult_rule, shift=DOWN))
        self.wait()

        # ========================================
        # INSIGHT: Why it works
        # ========================================
        insight = Text(
            "Magnitudes multiply, angles add!",
            font_size=40,
            color=GREEN
        )
        insight.next_to(mult_rule, UP, buff=0.5)

        self.play(FadeIn(insight, scale=1.3))
        self.wait(3)


# ============================================================
# 6. SCENE EXECUTION ORDER
# ============================================================
# The order of scenes that tells the story.
#
# Scene 1 (IntroduceComplexPlane):
#   - Introduces the complex plane as a geometric space
#   - Plots several complex numbers as points
#   - Establishes the coordinate system
#
# Scene 2 (MultiplyByI):
#   - Shows the simplest example: multiplication by i
#   - Demonstrates 90° rotation
#   - Builds intuition for rotation in complex multiplication
#
# Scene 3 (GeneralMultiplication):
#   - Shows that multiplication combines rotation and scaling
#   - Demonstrates with a concrete example
#   - Reveals the general pattern
#
# Scene 4 (PolarForm):
#   - Connects to polar form and Euler's formula
#   - Shows the multiplication rule in polar coordinates
#   - Completes the conceptual picture

SCENE_ORDER = [
    IntroduceComplexPlane,      # Part 1: The complex plane
    MultiplyByI,                # Part 2: Multiply by i (rotate 90°)
    GeneralMultiplication,      # Part 3: General case (rotate + scale)
    PolarForm,                  # Part 4: Polar form and Euler's formula
]
