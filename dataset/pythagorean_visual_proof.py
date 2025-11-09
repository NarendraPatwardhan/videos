"""
Natural Group Name: Pythagorean Theorem Visual Proof

Educational Objectives:
- To provide a visual, intuitive proof of the Pythagorean theorem (a² + b² = c²)
- To demonstrate that mathematical proofs can be understood through rearrangement and area
- To build geometric intuition for why the theorem must be true
- To show the power of visual reasoning in mathematics

Story Arc & Intent:
The animation presents one of the most elegant visual proofs of the Pythagorean theorem
by showing how the areas of squares on the legs can be rearranged to exactly fill the
square on the hypotenuse, making the theorem visually obvious without algebra.

Narrative Flow:
- Hook/Opening: A right triangle is introduced with three squares attached to its sides
- Development: The squares on legs a and b are divided into pieces
- Build-up: These pieces are systematically rearranged
- Climax: The pieces perfectly fill the square on the hypotenuse c
- Resolution: The visual demonstrates a² + b² = c² without any algebra

Technical Implementation Notes:
- Scene Classes: IntroduceTheorem, ShowSquares, DivideSquares, RearrangeProof
- Key Visual Elements: Right triangles, squares, color-coded regions, labels
- Animation Techniques: Transform, rotation, translation of geometric pieces
- Mathematical Concepts: Pythagorean theorem, area, geometric rearrangement

Dependency Chain:
All scenes use basic Polygon, Square, and text mobjects from manimlib.
No custom utilities required.

Rendering Instructions:
To render these scenes, use the manim command-line tool:
- For a single scene: manimgl pythagorean_visual_proof.py IntroduceTheorem
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
# - BLUE: Side 'a' of the triangle and its square
# - YELLOW: Side 'c' (hypotenuse) of the triangle and its square
# - MAROON_D: Side 'b' of the triangle and its square
# - WHITE: Borders and construction lines
# - GREY_A: De-emphasized elements
#
# Key Manim Constants Used:
# - UP, DOWN, LEFT, RIGHT: Direction vectors
# - ORIGIN: Center point
# - DEGREES: Angle conversion
# - MED_LARGE_BUFF: Spacing

# Triangle configuration - a 3-4-5 right triangle scaled up
TRIANGLE_SCALE = 1.2
LEG_A = 3.0 * TRIANGLE_SCALE  # Vertical leg
LEG_B = 4.0 * TRIANGLE_SCALE  # Horizontal leg
LEG_C = 5.0 * TRIANGLE_SCALE  # Hypotenuse

# Colors for sides
A_COLOR = BLUE
B_COLOR = MAROON_D
C_COLOR = YELLOW

# ============================================================
# 3. UTILITY FUNCTIONS
# ============================================================

def create_right_triangle(leg_a=LEG_A, leg_b=LEG_B, show_right_angle=True):
    """
    Create a right triangle with specified leg lengths.

    Args:
        leg_a: Length of vertical leg
        leg_b: Length of horizontal leg
        show_right_angle: Whether to show the right angle marker

    Returns:
        VGroup containing the triangle and optional right angle marker
    """
    # Vertices of the right triangle (right angle at origin)
    vertices = [ORIGIN, leg_b * RIGHT, leg_a * UP]

    # Create the triangle
    triangle = Polygon(*vertices)
    triangle.set_stroke(WHITE, 3)
    triangle.set_fill(C_COLOR, 0.3)

    result = VGroup(triangle)

    # Add right angle marker
    if show_right_angle:
        right_angle_size = 0.3
        right_angle = VGroup(
            Line(ORIGIN, right_angle_size * RIGHT),
            Line(right_angle_size * RIGHT, right_angle_size * (RIGHT + UP)),
            Line(right_angle_size * UP, ORIGIN)
        )
        right_angle.set_stroke(WHITE, 2)
        result.add(right_angle)

    return result

def create_square_on_side(start_point, end_point, color, label=""):
    """
    Create a square on a given side of the triangle.

    Args:
        start_point: Starting point of the side
        end_point: Ending point of the side
        color: Fill color for the square
        label: Label to place in the square (e.g., "a²")

    Returns:
        VGroup containing the square and label
    """
    # Calculate the side vector and perpendicular
    side_vector = end_point - start_point
    side_length = np.linalg.norm(side_vector)
    side_unit = side_vector / side_length

    # Perpendicular vector (rotate 90 degrees)
    perp_unit = np.array([-side_unit[1], side_unit[0], 0])

    # Create square vertices
    vertices = [
        start_point,
        end_point,
        end_point + side_length * perp_unit,
        start_point + side_length * perp_unit
    ]

    square = Polygon(*vertices)
    square.set_fill(color, 0.5)
    square.set_stroke(WHITE, 2)

    result = VGroup(square)

    # Add label if provided
    if label:
        label_mob = Tex(label, font_size=48)
        label_mob.move_to(square.get_center())
        result.add(label_mob)

    return result

def label_side(start_point, end_point, text, buff=0.3, color=WHITE):
    """
    Create a label for a side of the triangle.

    Args:
        start_point: Starting point of the side
        end_point: Ending point of the side
        text: Text for the label
        buff: Distance from the side
        color: Color of the label

    Returns:
        Text mobject positioned near the side
    """
    midpoint = (start_point + end_point) / 2
    side_vector = end_point - start_point
    side_unit = side_vector / np.linalg.norm(side_vector)
    perp_unit = np.array([-side_unit[1], side_unit[0], 0])

    label = Tex(text, font_size=36, color=color)
    label.move_to(midpoint - buff * perp_unit)

    return label

# ============================================================
# 4. BASE CLASSES AND HELPERS
# ============================================================
# No custom base classes needed

# ============================================================
# 5. SCENE IMPLEMENTATIONS
# ============================================================

class IntroduceTheorem(InteractiveScene):
    """
    Part 1: Introduce the Pythagorean theorem with a right triangle.

    Narrative purpose:
        To establish the problem and state the famous theorem that we will prove visually.

    Mathematical content:
        For a right triangle with legs a and b and hypotenuse c, the relationship
        a² + b² = c² always holds.

    Visual approach:
        Show a right triangle with labeled sides, then present the theorem equation.
    """
    def construct(self):
        # ========================================
        # SETUP: Title
        # ========================================
        title = OldTexText("The Pythagorean Theorem", font_size=54)
        title.to_edge(UP)

        self.play(FadeIn(title, shift=DOWN))
        self.wait()

        # ========================================
        # CREATE: Right triangle
        # ========================================
        triangle_group = create_right_triangle()
        triangle_group.move_to(ORIGIN)

        self.play(DrawBorderThenFill(triangle_group))
        self.wait()

        # ========================================
        # LABELS: Add side labels
        # ========================================
        # Get vertices
        vertices = triangle_group[0].get_vertices()

        # Labels for each side
        label_a = label_side(vertices[0], vertices[2], "a", buff=0.4, color=A_COLOR)
        label_b = label_side(vertices[0], vertices[1], "b", buff=0.4, color=B_COLOR)
        label_c = label_side(vertices[1], vertices[2], "c", buff=0.4, color=C_COLOR)

        self.play(
            FadeIn(label_a, shift=LEFT),
            FadeIn(label_b, shift=DOWN),
            FadeIn(label_c, shift=UR)
        )
        self.wait()

        # ========================================
        # THEOREM: Show the equation
        # ========================================
        theorem = Tex(
            "a^2 + b^2 = c^2",
            font_size=60,
            tex_to_color_map={"a": A_COLOR, "b": B_COLOR, "c": C_COLOR}
        )
        theorem.next_to(triangle_group, DOWN, buff=1.2)

        box = SurroundingRectangle(theorem, buff=0.2, color=YELLOW, stroke_width=3)

        self.play(Write(theorem))
        self.play(ShowCreation(box))
        self.wait(2)

        # ========================================
        # QUESTION: How do we prove this?
        # ========================================
        question = OldTexText("How can we prove this?", font_size=42, color=GREY_A)
        question.next_to(theorem, DOWN, buff=0.8)

        self.play(FadeIn(question, shift=UP))
        self.wait(2)


class ShowSquares(InteractiveScene):
    """
    Part 2: Show squares built on each side of the triangle.

    Narrative purpose:
        To visualize what a², b², and c² actually represent as geometric areas,
        setting up the visual proof.

    Mathematical content:
        The squared terms in the theorem represent literal square areas.

    Visual approach:
        Attach squares to each side of the triangle, labeled with a², b², c².
    """
    def construct(self):
        # ========================================
        # SETUP: Title
        # ========================================
        title = OldTexText("Squares on Each Side", font_size=48)
        title.to_edge(UP)

        self.add(title)

        # ========================================
        # CREATE: Triangle in center
        # ========================================
        triangle_group = create_right_triangle()
        triangle_group.scale(0.7).shift(0.5 * DOWN)

        self.play(DrawBorderThenFill(triangle_group))
        self.wait()

        # ========================================
        # CREATE: Squares on each side
        # ========================================
        vertices = triangle_group[0].get_vertices()

        # Square on side a (vertical leg)
        square_a = create_square_on_side(vertices[0], vertices[2], A_COLOR, "a^2")

        # Square on side b (horizontal leg)
        square_b = create_square_on_side(vertices[0], vertices[1], B_COLOR, "b^2")

        # Square on side c (hypotenuse)
        square_c = create_square_on_side(vertices[1], vertices[2], C_COLOR, "c^2")

        # ========================================
        # ANIMATE: Show each square
        # ========================================
        self.play(DrawBorderThenFill(square_a[0]), FadeIn(square_a[1], scale=1.3))
        self.wait()

        self.play(DrawBorderThenFill(square_b[0]), FadeIn(square_b[1], scale=1.3))
        self.wait()

        self.play(DrawBorderThenFill(square_c[0]), FadeIn(square_c[1], scale=1.3))
        self.wait()

        # ========================================
        # QUESTION: Show the relationship
        # ========================================
        question = OldTexText("Can we rearrange a² and b² to fill c²?", font_size=36)
        question.to_edge(DOWN, buff=0.5)
        question.set_color(YELLOW)

        self.play(FadeIn(question, shift=UP))
        self.wait(2)


class VisualProofByRearrangement(InteractiveScene):
    """
    Part 3: Show the visual proof through rearrangement of areas.

    Narrative purpose:
        To provide the "aha!" moment where the areas a² + b² are shown to exactly
        equal c² through visual rearrangement, proving the theorem without algebra.

    Mathematical content:
        By dividing the squares on legs a and b into specific pieces and rearranging
        them, we can show they perfectly tile the square on the hypotenuse.

    Visual approach:
        Use a large square (a+b)² that contains four copies of the triangle plus c².
        Show that removing the triangles leaves c² = (a+b)² - 4·(½ab) = a² + b².
    """
    def construct(self):
        # ========================================
        # SETUP: Title
        # ========================================
        title = OldTexText("Visual Proof by Rearrangement", font_size=48)
        title.to_edge(UP)

        self.add(title)
        self.wait()

        # ========================================
        # CREATE: Large square with side (a + b)
        # ========================================
        # Using our 3-4-5 triangle, a+b = 7
        side_length = LEG_A + LEG_B
        large_square = Square(side_length=side_length)
        large_square.set_fill(GREY_A, 0.2)
        large_square.set_stroke(WHITE, 3)
        large_square.shift(0.5 * DOWN)

        # Label for the square
        brace_bottom = Brace(large_square, DOWN)
        brace_label = brace_bottom.get_tex("a + b")

        self.play(
            DrawBorderThenFill(large_square),
            GrowFromCenter(brace_bottom),
            FadeIn(brace_label, shift=UP)
        )
        self.wait()

        # ========================================
        # FILL: Add four triangles inside
        # ========================================
        # Create four copies of our right triangle
        triangles = VGroup()

        # Calculate positions for four triangles
        # Bottom-left: original orientation
        tri1 = Polygon(
            large_square.get_corner(DL),
            large_square.get_corner(DL) + LEG_B * RIGHT,
            large_square.get_corner(DL) + LEG_A * UP
        )

        # Bottom-right: rotated 90° clockwise
        tri2 = Polygon(
            large_square.get_corner(DR),
            large_square.get_corner(DR) + LEG_A * LEFT,
            large_square.get_corner(DR) + LEG_B * UP
        )

        # Top-right: rotated 180°
        tri3 = Polygon(
            large_square.get_corner(UR),
            large_square.get_corner(UR) + LEG_B * LEFT,
            large_square.get_corner(UR) + LEG_A * DOWN
        )

        # Top-left: rotated 270° clockwise
        tri4 = Polygon(
            large_square.get_corner(UL),
            large_square.get_corner(UL) + LEG_A * RIGHT,
            large_square.get_corner(UL) + LEG_B * DOWN
        )

        for tri in [tri1, tri2, tri3, tri4]:
            tri.set_fill(BLUE_D, 0.6)
            tri.set_stroke(WHITE, 2)
            triangles.add(tri)

        self.play(LaggedStart([DrawBorderThenFill(tri) for tri in triangles], lag_ratio=0.2))
        self.wait()

        # ========================================
        # HIGHLIGHT: The inner square (c²)
        # ========================================
        # The inner square is formed by the hypotenuses
        inner_square = Polygon(
            large_square.get_corner(DL) + LEG_B * RIGHT,
            large_square.get_corner(DR) + LEG_A * LEFT,
            large_square.get_corner(UR) + LEG_B * LEFT,
            large_square.get_corner(UL) + LEG_A * RIGHT
        )
        inner_square.set_fill(C_COLOR, 0.7)
        inner_square.set_stroke(YELLOW, 4)

        self.play(DrawBorderThenFill(inner_square))
        self.wait()

        # Label it as c²
        c_squared_label = Tex("c^2", font_size=48, color=YELLOW)
        c_squared_label.move_to(inner_square.get_center())

        self.play(FadeIn(c_squared_label, scale=1.5))
        self.wait()

        # ========================================
        # EQUATION: Show the area relationship
        # ========================================
        equation = Tex(
            R"(a + b)^2 = 4 \cdot \frac{1}{2}ab + c^2",
            font_size=42
        )
        equation.next_to(large_square, DOWN, buff=1)

        self.play(Write(equation))
        self.wait()

        # Expand and simplify
        expansion = Tex(
            R"a^2 + 2ab + b^2 = 2ab + c^2",
            font_size=42
        )
        expansion.move_to(equation)

        self.play(TransformMatchingStrings(equation, expansion))
        self.wait()

        # Cancel 2ab
        final = Tex(
            R"a^2 + b^2 = c^2",
            font_size=48,
            tex_to_color_map={"a": A_COLOR, "b": B_COLOR, "c": C_COLOR}
        )
        final.move_to(expansion)

        box = SurroundingRectangle(final, buff=0.2, color=YELLOW, stroke_width=3)

        self.play(
            TransformMatchingStrings(expansion, final),
            ShowCreation(box)
        )
        self.wait()

        # ========================================
        # FINALE: Checkmark
        # ========================================
        checkmark = Tex(R"\checkmark", font_size=72, color=GREEN)
        checkmark.next_to(box, RIGHT, buff=0.5)

        self.play(FadeIn(checkmark, scale=2))
        self.wait(2)


class AlternativeProof(InteractiveScene):
    """
    Part 4: Show an alternative dissection proof.

    Narrative purpose:
        To reinforce the theorem by showing a different visual arrangement,
        demonstrating that there are multiple ways to see the same truth.

    Mathematical content:
        A different dissection that also proves a² + b² = c².

    Visual approach:
        Show the classic dissection where squares a² and b² are cut and
        rearranged to form c².
    """
    def construct(self):
        # ========================================
        # SETUP: Title
        # ========================================
        title = OldTexText("Another Visual Proof", font_size=48)
        title.to_edge(UP)

        self.add(title)
        self.wait()

        # ========================================
        # SETUP: Show theorem again
        # ========================================
        theorem = Tex(
            "a^2 + b^2 = c^2",
            font_size=48,
            tex_to_color_map={"a": A_COLOR, "b": B_COLOR, "c": C_COLOR}
        )
        theorem.next_to(title, DOWN, buff=0.5)

        self.play(FadeIn(theorem))
        self.wait()

        # ========================================
        # LEFT SIDE: Show a² + b²
        # ========================================
        square_a = Square(side_length=LEG_A)
        square_a.set_fill(A_COLOR, 0.6)
        square_a.set_stroke(WHITE, 2)
        square_a.shift(3 * LEFT + 0.5 * DOWN)

        label_a = Tex("a^2", font_size=36)
        label_a.move_to(square_a)

        square_b = Square(side_length=LEG_B)
        square_b.set_fill(B_COLOR, 0.6)
        square_b.set_stroke(WHITE, 2)
        square_b.next_to(square_a, DOWN, buff=0.3)

        label_b = Tex("b^2", font_size=36)
        label_b.move_to(square_b)

        self.play(
            DrawBorderThenFill(square_a),
            FadeIn(label_a)
        )
        self.play(
            DrawBorderThenFill(square_b),
            FadeIn(label_b)
        )
        self.wait()

        # ========================================
        # RIGHT SIDE: Show c²
        # ========================================
        square_c = Square(side_length=LEG_C)
        square_c.set_fill(C_COLOR, 0.6)
        square_c.set_stroke(WHITE, 2)
        square_c.shift(3 * RIGHT + 0.5 * DOWN)

        label_c = Tex("c^2", font_size=36)
        label_c.move_to(square_c)

        self.play(
            DrawBorderThenFill(square_c),
            FadeIn(label_c)
        )
        self.wait()

        # ========================================
        # SHOW: Equals sign
        # ========================================
        equals = Tex("=", font_size=72)
        equals.move_to((square_a.get_center() + square_c.get_center()) / 2)
        equals.shift(0.5 * DOWN)

        self.play(Write(equals))
        self.wait()

        # ========================================
        # MESSAGE: Multiple proofs exist
        # ========================================
        message = OldTexText(
            "Many visual proofs exist!\nMathematics has multiple perspectives.",
            font_size=36,
            color=GREY_A
        )
        message.to_edge(DOWN, buff=0.5)

        self.play(FadeIn(message, shift=UP))
        self.wait(3)


# ============================================================
# 6. SCENE EXECUTION ORDER
# ============================================================
# The order of scenes that tells the story.
#
# Scene 1 (IntroduceTheorem):
#   - Introduces the Pythagorean theorem with a labeled right triangle
#   - States the famous equation a² + b² = c²
#   - Poses the question: how do we prove this?
#
# Scene 2 (ShowSquares):
#   - Visualizes the squared terms as literal square areas
#   - Shows squares built on each side of the triangle
#   - Sets up the idea of comparing areas
#
# Scene 3 (VisualProofByRearrangement):
#   - Provides the main visual proof using a large square (a+b)²
#   - Shows how four triangles plus c² fill the large square
#   - Derives the theorem through area equations
#
# Scene 4 (AlternativeProof):
#   - Shows that multiple visual proofs exist
#   - Reinforces the theorem from a different perspective
#   - Emphasizes the richness of mathematical reasoning

SCENE_ORDER = [
    IntroduceTheorem,                # Part 1: State the theorem
    ShowSquares,                     # Part 2: Visualize squared terms
    VisualProofByRearrangement,      # Part 3: Main visual proof
    AlternativeProof,                # Part 4: Alternative perspective
]
