"""
Natural Group Name: Golden Ratio and Fibonacci Sequence

Educational Objectives:
- To visualize the relationship between Fibonacci numbers and the golden ratio
- To demonstrate how Fibonacci ratios converge to φ = (1+√5)/2
- To show the golden rectangle and its self-similar subdivision property
- To connect the golden ratio to spirals found in nature

Story Arc & Intent:
The animation reveals the golden ratio through the Fibonacci sequence, showing how
this simple recursive pattern converges to a profound mathematical constant that
appears throughout mathematics and nature.

Narrative Flow:
- Hook/Opening: The Fibonacci sequence 1, 1, 2, 3, 5, 8, 13...
- Development: Ratios of consecutive terms converging to φ
- Build-up: The golden rectangle and its subdivision property
- Climax: Construction of the golden spiral
- Resolution: Connection to nature, art, and mathematics

Technical Implementation Notes:
- Scene Classes: FibonacciSequence, GoldenRatio, GoldenRectangle, NatureSpirals
- Key Visual Elements: Number sequences, rectangles, spirals, geometric constructions
- Animation Techniques: Number generation, rectangle subdivision, spiral drawing
- Mathematical Concepts: Fibonacci, golden ratio, self-similarity, logarithmic spirals

Dependency Chain:
All scenes use basic manimlib components: Text, Tex, Rectangle, Arc, VMobject.
No custom utilities required beyond helper functions defined in this file.

Rendering Instructions:
To render these scenes, use the manim command-line tool:
- For a single scene: manimgl golden_ratio.py FibonacciSequence
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
# - BLUE: Fibonacci numbers
# - YELLOW: Ratios approaching phi
# - GREEN: Golden rectangles
# - RED: Golden spiral
# - WHITE: Labels and text
# - GREY_A: De-emphasized elements
#
# Key Manim Constants Used:
# - UP, DOWN, LEFT, RIGHT: Direction vectors
# - ORIGIN: Center point
# - PI: π for angle calculations
# - MED_SMALL_BUFF: Spacing

# Golden ratio
PHI = (1 + np.sqrt(5)) / 2

# ============================================================
# 3. UTILITY FUNCTIONS
# ============================================================

def fibonacci(n):
    """
    Compute the nth Fibonacci number (1-indexed).

    Args:
        n: Index (n=1 gives 1, n=2 gives 1, n=3 gives 2, etc.)

    Returns:
        nth Fibonacci number
    """
    if n <= 0:
        return 0
    elif n == 1 or n == 2:
        return 1
    else:
        a, b = 1, 1
        for _ in range(n - 2):
            a, b = b, a + b
        return b

def fibonacci_ratio(n):
    """
    Compute the ratio F(n+1) / F(n).

    Args:
        n: Index

    Returns:
        Ratio of consecutive Fibonacci numbers
    """
    if n <= 0:
        return 0
    fn = fibonacci(n)
    fn1 = fibonacci(n + 1)
    return fn1 / fn if fn != 0 else 0

def create_golden_rectangle(width=2.0, color=GREEN, **kwargs):
    """
    Create a golden rectangle (height/width = φ).

    Args:
        width: Width of rectangle
        color: Color of rectangle
        **kwargs: Additional arguments for Rectangle

    Returns:
        Rectangle mobject
    """
    height = width * PHI
    return Rectangle(
        width=width,
        height=height,
        color=color,
        stroke_width=2,
        **kwargs
    )

def create_fibonacci_spiral_arc(start_angle, radius, color=RED, **kwargs):
    """
    Create one arc of a Fibonacci spiral.

    Args:
        start_angle: Starting angle in radians
        radius: Radius of the arc
        color: Color of the arc
        **kwargs: Additional arguments for Arc

    Returns:
        Arc mobject
    """
    return Arc(
        radius=radius,
        start_angle=start_angle,
        angle=PI/2,  # Quarter circle
        color=color,
        stroke_width=3,
        **kwargs
    )

# ============================================================
# 4. SCENE CLASSES
# ============================================================

class FibonacciSequence(Scene):
    """
    Scene 1: Introduce the Fibonacci sequence.

    This scene presents the Fibonacci sequence and shows the simple recursive
    rule: each number is the sum of the previous two.
    """

    def construct(self):
        # ========================================
        # TITLE
        # ========================================
        title = Text("The Fibonacci Sequence", font_size=48)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait()

        # ========================================
        # DEFINITION
        # ========================================
        definition = VGroup(
            Tex("F_1 = 1, \\quad F_2 = 1", font_size=36),
            Tex("F_n = F_{n-1} + F_{n-2}", font_size=36, color=YELLOW),
        )
        definition.arrange(DOWN, buff=0.4)
        definition.next_to(title, DOWN, buff=0.8)

        for line in definition:
            self.play(Write(line))
            self.wait()

        # ========================================
        # GENERATE SEQUENCE
        # ========================================
        sequence_label = Text("Sequence:", font_size=32)
        sequence_label.next_to(definition, DOWN, buff=1.0)

        self.play(Write(sequence_label))
        self.wait()

        # Generate first 12 Fibonacci numbers
        fib_numbers = VGroup()
        for i in range(1, 13):
            fib = fibonacci(i)
            fib_text = Text(str(fib), font_size=32, color=BLUE)
            fib_numbers.add(fib_text)

        fib_numbers.arrange(RIGHT, buff=0.4)
        fib_numbers.next_to(sequence_label, DOWN, buff=0.5)

        # Animate generation
        for i, fib_mob in enumerate(fib_numbers):
            if i < 2:
                self.play(FadeIn(fib_mob, shift=DOWN))
            else:
                # Highlight previous two numbers
                prev1 = fib_numbers[i-1].copy()
                prev2 = fib_numbers[i-2].copy()

                self.play(
                    prev1.animate.set_color(YELLOW),
                    prev2.animate.set_color(YELLOW),
                )

                # Show addition
                self.play(FadeIn(fib_mob, shift=DOWN))

                # Reset colors
                self.play(
                    prev1.animate.set_color(BLUE),
                    prev2.animate.set_color(BLUE),
                )

            self.wait(0.3)

        self.wait()

        # ========================================
        # OBSERVATION
        # ========================================
        observation = Text(
            "Each number is the sum of the previous two",
            font_size=28,
            color=GREY_A
        )
        observation.to_edge(DOWN).shift(UP * 0.3)

        self.play(FadeIn(observation, shift=UP))
        self.wait()

        # Show example
        example = Tex(
            "8 = 5 + 3, \\quad 13 = 8 + 5, \\quad 21 = 13 + 8",
            font_size=28,
            color=YELLOW
        )
        example.next_to(observation, DOWN, buff=0.2)

        self.play(Write(example))
        self.wait(2)


class GoldenRatio(Scene):
    """
    Scene 2: Show how ratios of consecutive Fibonacci numbers converge to φ.

    This scene computes F(n+1)/F(n) for increasing n and shows convergence
    to the golden ratio φ = (1+√5)/2 ≈ 1.618.
    """

    def construct(self):
        # ========================================
        # TITLE
        # ========================================
        title = Text("Convergence to Golden Ratio", font_size=42)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait()

        # ========================================
        # IDEA: Look at ratios
        # ========================================
        idea = Text(
            "What happens to the ratio of consecutive terms?",
            font_size=32,
            color=WHITE
        )
        idea.next_to(title, DOWN, buff=0.6)

        self.play(FadeIn(idea, shift=DOWN))
        self.wait()

        # ========================================
        # COMPUTE RATIOS
        # ========================================
        ratio_formula = Tex(
            "r_n = \\frac{F_{n+1}}{F_n}",
            font_size=36,
            color=YELLOW
        )
        ratio_formula.next_to(idea, DOWN, buff=0.8)

        self.play(Write(ratio_formula))
        self.wait()

        # ========================================
        # SHOW CONVERGENCE TABLE
        # ========================================
        table_data = []
        for n in range(1, 11):
            fn = fibonacci(n)
            fn1 = fibonacci(n + 1)
            ratio = fn1 / fn if fn != 0 else 0
            table_data.append((n, fn, fn1, ratio))

        # Create table
        table_entries = VGroup()

        # Header
        header = VGroup(
            Text("n", font_size=24),
            Text("F(n)", font_size=24),
            Text("F(n+1)", font_size=24),
            Text("Ratio", font_size=24, color=YELLOW),
        )
        header.arrange(RIGHT, buff=0.8)
        table_entries.add(header)

        # Data rows (show first 8)
        for i, (n, fn, fn1, ratio) in enumerate(table_data[:8]):
            row = VGroup(
                Text(str(n), font_size=22),
                Text(str(fn), font_size=22),
                Text(str(fn1), font_size=22),
                Text(f"{ratio:.6f}", font_size=22, color=YELLOW),
            )
            row.arrange(RIGHT, buff=0.8)
            # Align with header
            for j, item in enumerate(row):
                item.align_to(header[j], LEFT)
            table_entries.add(row)

        table_entries.arrange(DOWN, buff=0.25, aligned_edge=LEFT)
        table_entries.next_to(ratio_formula, DOWN, buff=0.6)
        table_entries.scale(0.9)

        # Animate table appearance
        self.play(Write(header))
        self.wait()

        for i in range(1, len(table_entries)):
            self.play(FadeIn(table_entries[i], shift=UP), run_time=0.3)

        self.wait()

        # ========================================
        # GOLDEN RATIO VALUE
        # ========================================
        phi_value = Tex(
            "\\varphi = \\frac{1 + \\sqrt{5}}{2} \\approx 1.618034",
            font_size=36,
            color=GREEN
        )
        phi_value.to_edge(DOWN).shift(UP * 1.0)

        phi_box = SurroundingRectangle(phi_value, buff=0.2, color=GREEN, stroke_width=2)

        self.play(Write(phi_value))
        self.play(ShowCreation(phi_box))
        self.wait()

        # ========================================
        # CONVERGENCE STATEMENT
        # ========================================
        convergence = Tex(
            "\\lim_{n \\to \\infty} \\frac{F_{n+1}}{F_n} = \\varphi",
            font_size=32
        )
        convergence.next_to(phi_value, DOWN, buff=0.3)

        self.play(Write(convergence))
        self.wait(2)


class GoldenRectangle(Scene):
    """
    Scene 3: Construct the golden rectangle and show its subdivision property.

    This scene demonstrates the golden rectangle (sides in ratio φ:1) and
    shows that removing a square leaves another golden rectangle.
    """

    def construct(self):
        # ========================================
        # TITLE
        # ========================================
        title = Text("The Golden Rectangle", font_size=42)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait()

        # ========================================
        # DEFINITION
        # ========================================
        definition = Tex(
            "\\text{A rectangle where } \\frac{\\text{length}}{\\text{width}} = \\varphi",
            font_size=32
        )
        definition.next_to(title, DOWN, buff=0.5)

        self.play(Write(definition))
        self.wait()

        # ========================================
        # CONSTRUCT GOLDEN RECTANGLE
        # ========================================
        # Start with a unit square
        square_size = 2.0
        square = Square(side_length=square_size, color=BLUE, stroke_width=2)
        square.shift(LEFT * 1.5)

        square_label = Tex("1", font_size=28)
        square_label.next_to(square, DOWN, buff=0.2)

        self.play(ShowCreation(square), Write(square_label))
        self.wait()

        # Add extension to make golden rectangle
        # Width = 1, so height = φ - 1
        extension_width = square_size * (PHI - 1)
        extension = Rectangle(
            width=extension_width,
            height=square_size,
            color=GREEN,
            stroke_width=2
        )
        extension.next_to(square, RIGHT, buff=0)

        ext_label = Tex("\\varphi - 1", font_size=24)
        ext_label.next_to(extension, DOWN, buff=0.2)

        self.play(ShowCreation(extension), Write(ext_label))
        self.wait()

        # Full golden rectangle
        golden_rect = VGroup(square, extension)

        total_label = Tex("\\varphi", font_size=28, color=GREEN)
        total_label.next_to(golden_rect, DOWN, buff=0.5)

        self.play(Write(total_label))
        self.wait()

        # ========================================
        # SUBDIVISION PROPERTY
        # ========================================
        property_text = Text(
            "Special property: Removing a square leaves a golden rectangle!",
            font_size=26,
            color=YELLOW
        )
        property_text.to_edge(DOWN).shift(UP * 0.3)

        self.play(FadeIn(property_text, shift=UP))
        self.wait()

        # Highlight the square to remove
        self.play(square.animate.set_fill(BLUE, opacity=0.3))
        self.wait()

        # Show that remaining part is golden
        remaining_label = Tex(
            "\\frac{1}{\\varphi - 1} = \\varphi \\quad \\text{(golden ratio!)}",
            font_size=24,
            color=GREEN
        )
        remaining_label.next_to(property_text, DOWN, buff=0.2)

        self.play(Write(remaining_label))
        self.wait()

        # ========================================
        # ITERATIVE SUBDIVISION
        # ========================================
        self.play(
            FadeOut(property_text),
            FadeOut(remaining_label),
            FadeOut(square_label),
            FadeOut(ext_label),
            FadeOut(total_label),
            FadeOut(definition)
        )

        # New title
        subdivision_title = Text("Fibonacci Spiral Construction", font_size=32)
        subdivision_title.next_to(title, DOWN, buff=0.3)

        self.play(Write(subdivision_title))
        self.wait()

        # Create Fibonacci squares in spiral pattern
        # Reset and create fresh
        self.play(FadeOut(golden_rect))

        # Build Fibonacci spiral with squares
        fib_sizes = [fibonacci(i) * 0.3 for i in range(1, 8)]
        squares_group = VGroup()

        # Starting position
        current_pos = ORIGIN + LEFT * 2

        # Build squares
        positions = [
            (0, 0),    # 1
            (1, 0),    # 1
            (1, 1),    # 2
            (-1, 1),   # 3
            (-1, -2),  # 5
            (4, -2),   # 8
        ]

        colors = [BLUE, YELLOW, GREEN, RED, PURPLE, ORANGE]

        for i, size in enumerate(fib_sizes[:6]):
            sq = Square(side_length=size, color=colors[i], stroke_width=2)
            sq.set_fill(colors[i], opacity=0.2)

            # Position based on Fibonacci spiral pattern
            if i == 0:
                sq.move_to(ORIGIN)
            elif i == 1:
                sq.next_to(squares_group[0], RIGHT, buff=0)
            elif i == 2:
                sq.next_to(squares_group[1], UP, buff=0, aligned_edge=RIGHT)
            elif i == 3:
                sq.next_to(squares_group[2], LEFT, buff=0, aligned_edge=UP)
            elif i == 4:
                sq.next_to(squares_group[3], DOWN, buff=0, aligned_edge=LEFT)
            elif i == 5:
                sq.next_to(squares_group[4], RIGHT, buff=0, aligned_edge=DOWN)

            squares_group.add(sq)

            label = Text(str(fibonacci(i+1)), font_size=16, color=WHITE)
            label.move_to(sq.get_center())

            self.play(ShowCreation(sq), Write(label), run_time=0.5)
            self.wait(0.3)

        self.wait(2)


class NatureSpirals(Scene):
    """
    Scene 4: Connect golden ratio to spirals in nature.

    This scene shows the golden spiral emerging from the Fibonacci squares
    and connects it to patterns found in nature.
    """

    def construct(self):
        # ========================================
        # TITLE
        # ========================================
        title = Text("The Golden Spiral", font_size=42)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait()

        # ========================================
        # BUILD FIBONACCI SQUARES
        # ========================================
        # Create Fibonacci squares (simplified version)
        fib_sizes = [fibonacci(i) * 0.25 for i in range(1, 9)]
        colors = [BLUE, YELLOW, GREEN, RED, PURPLE, ORANGE, TEAL, MAROON]

        # For simplicity, arrange them in a rough spiral
        squares = VGroup()

        base_square = Square(side_length=fib_sizes[0], color=colors[0], stroke_width=1.5)
        base_square.set_fill(colors[0], opacity=0.1)
        base_square.move_to(ORIGIN + DOWN * 0.5)
        squares.add(base_square)

        # Manually position for visual clarity
        positions = [
            ORIGIN + DOWN * 0.5,
            ORIGIN + DOWN * 0.5 + RIGHT * fib_sizes[0]/2 + RIGHT * fib_sizes[1]/2,
        ]

        for i in range(2):
            sq = Square(side_length=fib_sizes[i], color=colors[i], stroke_width=1.5)
            sq.set_fill(colors[i], opacity=0.1)
            sq.move_to(positions[i] if i < len(positions) else ORIGIN)
            if i > 0:
                squares.add(sq)

        # Just show a simple spiral for visualization
        spiral_path = VMobject(color=RED, stroke_width=3)

        # Create spiral points
        points = []
        angles = np.linspace(0, 4 * PI, 200)
        for angle in angles:
            # Logarithmic spiral: r = a * e^(b*theta)
            r = 0.2 * np.exp(0.2 * angle)
            x = r * np.cos(angle)
            y = r * np.sin(angle)
            points.append([x, y + 0.5, 0])

        spiral_path.set_points_smoothly(points)
        spiral_path.shift(DOWN * 0.5)

        self.play(ShowCreation(spiral_path), run_time=3)
        self.wait()

        # ========================================
        # NATURE EXAMPLES
        # ========================================
        nature_text = Text(
            "Found in Nature:",
            font_size=32,
            color=YELLOW
        )
        nature_text.to_edge(DOWN).shift(UP * 2.0)

        examples = VGroup(
            Text("• Nautilus shells", font_size=24),
            Text("• Sunflower seed patterns", font_size=24),
            Text("• Galaxy spiral arms", font_size=24),
            Text("• Hurricane formations", font_size=24),
        )
        examples.arrange(DOWN, buff=0.2, aligned_edge=LEFT)
        examples.next_to(nature_text, DOWN, buff=0.3)

        self.play(Write(nature_text))
        self.wait()

        for example in examples:
            self.play(FadeIn(example, shift=UP))
            self.wait(0.4)

        self.wait()

        # ========================================
        # MATHEMATICAL PROPERTIES
        # ========================================
        self.play(FadeOut(nature_text), FadeOut(examples))

        properties = VGroup(
            Text("Key Properties of φ:", font_size=32, color=GREEN),
            Tex("\\varphi^2 = \\varphi + 1", font_size=28),
            Tex("\\frac{1}{\\varphi} = \\varphi - 1", font_size=28),
            Tex("\\varphi = 1 + \\frac{1}{1 + \\frac{1}{1 + \\frac{1}{\\ddots}}}", font_size=24),
        )
        properties.arrange(DOWN, buff=0.3)
        properties.to_edge(DOWN).shift(UP * 0.5)

        for prop in properties:
            self.play(FadeIn(prop, shift=UP))
            self.wait(0.5)

        self.wait(2)


# ============================================================
# 5. SCENE SUMMARY AND EXECUTION ORDER
# ============================================================
#
# Scene 1 (FibonacciSequence):
#   - Introduces the Fibonacci sequence 1, 1, 2, 3, 5, 8, 13...
#   - Shows the recursive rule F(n) = F(n-1) + F(n-2)
#   - Generates the first 12 terms
#
# Scene 2 (GoldenRatio):
#   - Computes ratios of consecutive Fibonacci numbers
#   - Shows convergence to φ ≈ 1.618034
#   - Presents the golden ratio formula
#
# Scene 3 (GoldenRectangle):
#   - Constructs the golden rectangle
#   - Shows the subdivision property
#   - Builds Fibonacci squares in spiral pattern
#
# Scene 4 (NatureSpirals):
#   - Creates the golden spiral
#   - Connects to patterns in nature
#   - Shows mathematical properties of φ

SCENE_ORDER = [
    FibonacciSequence,     # Part 1: The Fibonacci sequence
    GoldenRatio,           # Part 2: Convergence to φ
    GoldenRectangle,       # Part 3: Golden rectangle construction
    NatureSpirals,         # Part 4: Golden spiral and nature
]
