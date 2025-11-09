"""
Natural Group Name: Vector Addition and Parallelogram Law

Educational Objectives:
- To visualize vectors as arrows representing magnitude and direction
- To demonstrate vector addition using the tip-to-tail method
- To show the parallelogram law of vector addition
- To build geometric intuition for vector operations

Story Arc & Intent:
The animation reveals the geometric nature of vector addition, showing how vectors
combine through two equivalent methods: tip-to-tail and the parallelogram law.
This transforms abstract vector arithmetic into intuitive geometric operations.

Narrative Flow:
- Hook/Opening: Introduce vectors as arrows with magnitude and direction
- Development: Show tip-to-tail addition of two vectors
- Build-up: Demonstrate the parallelogram construction
- Climax: Both methods yield the same result, revealing geometric equivalence
- Resolution: Extend to vector subtraction and multiple vectors

Technical Implementation Notes:
- Scene Classes: IntroduceVectors, VectorAddition, ParallelogramLaw, VectorSubtraction
- Key Visual Elements: Arrows, coordinate plane, dashed construction lines, labels
- Animation Techniques: Arrow growth, translation, parallelogram construction
- Mathematical Concepts: Vector addition, parallelogram law, vector components

Dependency Chain:
All scenes use basic Arrow, NumberPlane, Text, and Tex mobjects from manimlib.
No custom utilities required.

Rendering Instructions:
To render these scenes, use the manim command-line tool:
- For a single scene: manimgl vector_addition.py IntroduceVectors
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
# - BLUE: First vector (vector a)
# - YELLOW: Second vector (vector b)
# - GREEN: Resultant vector (sum)
# - RED: Construction lines and guides
# - WHITE: Axes and grid
# - GREY_A: De-emphasized elements
#
# Key Manim Constants Used:
# - UP, DOWN, LEFT, RIGHT: Direction vectors
# - ORIGIN: Starting point (0, 0, 0)
# - DEGREES: Angle conversion
# - MED_SMALL_BUFF: Spacing

# Vector styling
VECTOR_CONFIG = {
    "buff": 0,
    "stroke_width": 5,
    "max_tip_length_to_length_ratio": 0.2,
}

# Plane configuration
PLANE_CONFIG = {
    "x_range": (-6, 6, 1),
    "y_range": (-4, 4, 1),
    "width": 12,
    "height": 8,
}

# ============================================================
# 3. UTILITY FUNCTIONS
# ============================================================

def create_vector_arrow(start, end, color=BLUE, **kwargs):
    """
    Create a vector arrow from start to end point.

    Args:
        start: Starting point (3D numpy array)
        end: Ending point (3D numpy array)
        color: Color of the vector
        **kwargs: Additional arguments for Arrow

    Returns:
        Arrow mobject representing the vector
    """
    config = VECTOR_CONFIG.copy()
    config.update(kwargs)

    return Arrow(
        start,
        end,
        color=color,
        **config
    )

def create_vector_label(vector, text, direction=UR, buff=0.1, **kwargs):
    """
    Create a label for a vector.

    Args:
        vector: Arrow mobject
        text: Text to display
        direction: Direction to place label relative to vector
        buff: Buffer from the vector
        **kwargs: Additional arguments for Tex

    Returns:
        Tex mobject positioned near the vector
    """
    label = Tex(text, **kwargs)
    label.next_to(vector.get_center(), direction, buff=buff)

    return label

def get_vector_endpoint(start, direction_vector):
    """
    Get the endpoint of a vector given start and direction.

    Args:
        start: Starting point (3D numpy array)
        direction_vector: Direction and magnitude (3D numpy array)

    Returns:
        Endpoint (3D numpy array)
    """
    return start + direction_vector

# ============================================================
# 4. BASE CLASSES AND HELPERS
# ============================================================
# No custom base classes needed

# ============================================================
# 5. SCENE IMPLEMENTATIONS
# ============================================================

class IntroduceVectors(InteractiveScene):
    """
    Part 1: Introduce vectors as arrows with magnitude and direction.

    Narrative purpose:
        To establish what vectors are geometrically - arrows that have both
        magnitude (length) and direction (orientation in space).

    Mathematical content:
        Vectors are mathematical objects with magnitude and direction,
        represented geometrically as arrows from origin to a point.

    Visual approach:
        Show several vectors on a coordinate plane, emphasizing their
        magnitude and direction with clear labels.
    """
    def construct(self):
        # ========================================
        # SETUP: Title
        # ========================================
        title = OldTexText("Vectors: Magnitude and Direction", font_size=48)
        title.to_edge(UP)

        self.play(FadeIn(title, shift=DOWN))
        self.wait()

        # ========================================
        # CREATE: Coordinate plane
        # ========================================
        plane = NumberPlane(**PLANE_CONFIG)
        plane.add_coordinates()

        self.play(ShowCreation(plane), run_time=1.5)
        self.wait()

        # ========================================
        # CREATE: First vector
        # ========================================
        vec_a_dir = np.array([3, 2, 0])
        vec_a = create_vector_arrow(ORIGIN, vec_a_dir, color=BLUE)

        label_a = Tex("\\vec{a}", font_size=42, color=BLUE)
        label_a.next_to(vec_a.get_end(), UR, buff=0.2)

        self.play(GrowArrow(vec_a))
        self.play(FadeIn(label_a, scale=1.3))
        self.wait()

        # ========================================
        # HIGHLIGHT: Magnitude and direction
        # ========================================
        # Show magnitude (length)
        magnitude_brace = Brace(vec_a, direction=vec_a.copy().rotate(-PI/2).get_unit_vector())
        magnitude_label = magnitude_brace.get_text("Magnitude", font_size=28)

        self.play(
            GrowFromCenter(magnitude_brace),
            FadeIn(magnitude_label, shift=DOWN)
        )
        self.wait()

        # Show direction (angle)
        angle_arc = Arc(
            start_angle=0,
            angle=np.arctan2(vec_a_dir[1], vec_a_dir[0]),
            radius=1.0,
            color=YELLOW,
            stroke_width=3
        )

        direction_label = OldTexText("Direction", font_size=28, color=YELLOW)
        direction_label.next_to(angle_arc, RIGHT, buff=0.3)

        self.play(
            ShowCreation(angle_arc),
            FadeIn(direction_label, shift=LEFT)
        )
        self.wait(2)

        # ========================================
        # CREATE: Second vector for comparison
        # ========================================
        self.play(
            FadeOut(magnitude_brace),
            FadeOut(magnitude_label),
            FadeOut(angle_arc),
            FadeOut(direction_label)
        )

        vec_b_dir = np.array([1, 3, 0])
        vec_b = create_vector_arrow(ORIGIN, vec_b_dir, color=YELLOW)

        label_b = Tex("\\vec{b}", font_size=42, color=YELLOW)
        label_b.next_to(vec_b.get_end(), UP, buff=0.2)

        self.play(GrowArrow(vec_b))
        self.play(FadeIn(label_b, scale=1.3))
        self.wait()

        # ========================================
        # QUESTION: How do we add these?
        # ========================================
        question = OldTexText("How do we add vectors?", font_size=36, color=GREY_A)
        question.to_edge(DOWN, buff=0.5)

        self.play(FadeIn(question, shift=UP))
        self.wait(2)


class VectorAddition(InteractiveScene):
    """
    Part 2: Demonstrate tip-to-tail vector addition.

    Narrative purpose:
        To show the fundamental method of adding vectors: place the tail
        of the second vector at the tip of the first.

    Mathematical content:
        Vector addition a + b is performed by translating b to start where
        a ends, then drawing the resultant from the original start to the new end.

    Visual approach:
        Start with vector a, then translate vector b to start at a's tip,
        then show the resultant vector from origin to the final point.
    """
    def construct(self):
        # ========================================
        # SETUP: Title
        # ========================================
        title = OldTexText("Vector Addition: Tip-to-Tail Method", font_size=48)
        title.to_edge(UP)

        self.add(title)

        # ========================================
        # CREATE: Coordinate plane
        # ========================================
        plane = NumberPlane(**PLANE_CONFIG)
        plane.add_coordinates()

        self.add(plane)

        # ========================================
        # CREATE: Vector a
        # ========================================
        vec_a_dir = np.array([3, 2, 0])
        vec_a = create_vector_arrow(ORIGIN, vec_a_dir, color=BLUE)

        label_a = Tex("\\vec{a}", font_size=42, color=BLUE)
        label_a.next_to(vec_a.get_end(), UR, buff=0.2)

        self.play(GrowArrow(vec_a))
        self.play(FadeIn(label_a, scale=1.2))
        self.wait()

        # ========================================
        # CREATE: Vector b (initially at origin)
        # ========================================
        vec_b_dir = np.array([1, 3, 0])
        vec_b_initial = create_vector_arrow(ORIGIN, vec_b_dir, color=YELLOW)

        label_b_initial = Tex("\\vec{b}", font_size=42, color=YELLOW)
        label_b_initial.next_to(vec_b_initial.get_end(), UP, buff=0.2)

        self.play(GrowArrow(vec_b_initial))
        self.play(FadeIn(label_b_initial, scale=1.2))
        self.wait()

        # ========================================
        # TRANSLATE: Move b to the tip of a
        # ========================================
        instruction = OldTexText("Place tail of b at tip of a", font_size=32, color=GREY_A)
        instruction.to_edge(DOWN, buff=0.8)

        self.play(FadeIn(instruction, shift=UP))
        self.wait()

        # Create vector b starting at tip of a
        vec_b = create_vector_arrow(vec_a_dir, vec_a_dir + vec_b_dir, color=YELLOW)

        label_b = Tex("\\vec{b}", font_size=42, color=YELLOW)
        label_b.next_to(vec_b.get_end(), UP, buff=0.2)

        self.play(
            Transform(vec_b_initial, vec_b),
            Transform(label_b_initial, label_b),
            run_time=2
        )
        self.wait()

        # ========================================
        # RESULTANT: Show a + b
        # ========================================
        self.play(FadeOut(instruction))

        result_dir = vec_a_dir + vec_b_dir
        vec_result = create_vector_arrow(ORIGIN, result_dir, color=GREEN, stroke_width=6)

        label_result = Tex("\\vec{a} + \\vec{b}", font_size=42, color=GREEN)
        label_result.next_to(vec_result.get_center(), LEFT, buff=0.3)

        self.play(GrowArrow(vec_result), run_time=1.5)
        self.play(FadeIn(label_result, scale=1.3))
        self.wait()

        # ========================================
        # EQUATION: Show the addition
        # ========================================
        equation = Tex(
            "\\vec{a} + \\vec{b} = \\vec{c}",
            font_size=48,
            tex_to_color_map={"\\vec{a}": BLUE, "\\vec{b}": YELLOW, "\\vec{c}": GREEN}
        )
        equation.to_edge(DOWN, buff=0.5)

        box = SurroundingRectangle(equation, buff=0.2, color=GREEN, stroke_width=2)

        self.play(Write(equation))
        self.play(ShowCreation(box))
        self.wait(2)


class ParallelogramLaw(InteractiveScene):
    """
    Part 3: Demonstrate the parallelogram law of vector addition.

    Narrative purpose:
        To show an alternative, equivalent method for vector addition that
        reveals beautiful geometric structure: the parallelogram.

    Mathematical content:
        When vectors a and b are drawn from the same origin, their sum is
        the diagonal of the parallelogram formed by a and b as adjacent sides.

    Visual approach:
        Draw both vectors from origin, construct the parallelogram, and
        show the diagonal equals the vector sum.
    """
    def construct(self):
        # ========================================
        # SETUP: Title
        # ========================================
        title = OldTexText("Parallelogram Law", font_size=48)
        title.to_edge(UP)

        self.add(title)

        # ========================================
        # CREATE: Coordinate plane
        # ========================================
        plane = NumberPlane(**PLANE_CONFIG)
        plane.add_coordinates()

        self.add(plane)

        # ========================================
        # CREATE: Both vectors from origin
        # ========================================
        vec_a_dir = np.array([3, 2, 0])
        vec_b_dir = np.array([1, 3, 0])

        vec_a = create_vector_arrow(ORIGIN, vec_a_dir, color=BLUE)
        vec_b = create_vector_arrow(ORIGIN, vec_b_dir, color=YELLOW)

        label_a = Tex("\\vec{a}", font_size=42, color=BLUE)
        label_a.next_to(vec_a.get_end(), DR, buff=0.2)

        label_b = Tex("\\vec{b}", font_size=42, color=YELLOW)
        label_b.next_to(vec_b.get_end(), UL, buff=0.2)

        self.play(
            GrowArrow(vec_a),
            GrowArrow(vec_b)
        )
        self.play(
            FadeIn(label_a),
            FadeIn(label_b)
        )
        self.wait()

        # ========================================
        # CONSTRUCT: Parallelogram
        # ========================================
        instruction = OldTexText("Complete the parallelogram", font_size=32, color=GREY_A)
        instruction.to_edge(DOWN, buff=0.8)

        self.play(FadeIn(instruction, shift=UP))
        self.wait()

        # Dashed lines to complete parallelogram
        line_parallel_a = DashedLine(
            vec_b_dir,
            vec_b_dir + vec_a_dir,
            color=BLUE,
            stroke_width=3
        )

        line_parallel_b = DashedLine(
            vec_a_dir,
            vec_a_dir + vec_b_dir,
            color=YELLOW,
            stroke_width=3
        )

        self.play(
            ShowCreation(line_parallel_a),
            ShowCreation(line_parallel_b),
            run_time=2
        )
        self.wait()

        # ========================================
        # DIAGONAL: Show the resultant
        # ========================================
        self.play(FadeOut(instruction))

        result_dir = vec_a_dir + vec_b_dir
        vec_result = create_vector_arrow(ORIGIN, result_dir, color=GREEN, stroke_width=6)

        label_result = Tex("\\vec{a} + \\vec{b}", font_size=42, color=GREEN)
        label_result.next_to(vec_result.get_center(), UP, buff=0.3)

        diagonal_text = OldTexText("The diagonal is the sum!", font_size=36, color=GREEN)
        diagonal_text.to_edge(DOWN, buff=0.5)

        self.play(GrowArrow(vec_result), run_time=1.5)
        self.play(FadeIn(label_result, scale=1.3))
        self.play(FadeIn(diagonal_text, shift=UP))
        self.wait(2)

        # ========================================
        # HIGHLIGHT: The parallelogram
        # ========================================
        parallelogram = Polygon(
            ORIGIN,
            vec_a_dir,
            vec_a_dir + vec_b_dir,
            vec_b_dir,
            stroke_width=0,
            fill_color=GREEN,
            fill_opacity=0.2
        )

        self.play(FadeIn(parallelogram))
        self.wait(2)


class VectorSubtraction(InteractiveScene):
    """
    Part 4: Demonstrate vector subtraction.

    Narrative purpose:
        To extend the addition concept to subtraction, showing how
        subtracting a vector is equivalent to adding its negative.

    Mathematical content:
        Vector subtraction a - b = a + (-b), where -b has the same
        magnitude as b but opposite direction.

    Visual approach:
        Show vector -b as the opposite of b, then add it to a using
        tip-to-tail method to get the difference.
    """
    def construct(self):
        # ========================================
        # SETUP: Title
        # ========================================
        title = OldTexText("Vector Subtraction", font_size=48)
        title.to_edge(UP)

        self.add(title)

        # ========================================
        # CREATE: Coordinate plane
        # ========================================
        plane = NumberPlane(**PLANE_CONFIG)
        plane.add_coordinates()

        self.add(plane)

        # ========================================
        # CREATE: Vectors a and b
        # ========================================
        vec_a_dir = np.array([3, 2, 0])
        vec_b_dir = np.array([1, 3, 0])

        vec_a = create_vector_arrow(ORIGIN, vec_a_dir, color=BLUE)
        vec_b = create_vector_arrow(ORIGIN, vec_b_dir, color=YELLOW)

        label_a = Tex("\\vec{a}", font_size=42, color=BLUE)
        label_a.next_to(vec_a.get_end(), UR, buff=0.2)

        label_b = Tex("\\vec{b}", font_size=42, color=YELLOW)
        label_b.next_to(vec_b.get_end(), UP, buff=0.2)

        self.play(
            GrowArrow(vec_a),
            GrowArrow(vec_b)
        )
        self.play(
            FadeIn(label_a),
            FadeIn(label_b)
        )
        self.wait()

        # ========================================
        # QUESTION: What is a - b?
        # ========================================
        question = Tex("\\vec{a} - \\vec{b} = \\, ?", font_size=42)
        question.to_edge(DOWN, buff=1.5)

        self.play(Write(question))
        self.wait()

        # ========================================
        # CREATE: -b (negative of b)
        # ========================================
        explanation = Tex("\\vec{a} - \\vec{b} = \\vec{a} + (-\\vec{b})", font_size=36)
        explanation.next_to(question, UP, buff=0.5)

        self.play(Write(explanation))
        self.wait()

        # Show -b
        vec_neg_b = create_vector_arrow(ORIGIN, -vec_b_dir, color=RED)

        label_neg_b = Tex("-\\vec{b}", font_size=42, color=RED)
        label_neg_b.next_to(vec_neg_b.get_end(), DOWN, buff=0.2)

        self.play(
            vec_b.animate.set_opacity(0.3),
            label_b.animate.set_opacity(0.3)
        )
        self.play(GrowArrow(vec_neg_b))
        self.play(FadeIn(label_neg_b, scale=1.2))
        self.wait()

        # ========================================
        # ADD: a + (-b) using tip-to-tail
        # ========================================
        self.play(
            FadeOut(vec_b),
            FadeOut(label_b)
        )

        # Move -b to tip of a
        vec_neg_b_translated = create_vector_arrow(
            vec_a_dir,
            vec_a_dir - vec_b_dir,
            color=RED
        )

        label_neg_b_new = Tex("-\\vec{b}", font_size=42, color=RED)
        label_neg_b_new.next_to(vec_neg_b_translated.get_center(), RIGHT, buff=0.2)

        self.play(
            Transform(vec_neg_b, vec_neg_b_translated),
            Transform(label_neg_b, label_neg_b_new),
            run_time=2
        )
        self.wait()

        # ========================================
        # RESULTANT: Show a - b
        # ========================================
        result_dir = vec_a_dir - vec_b_dir
        vec_result = create_vector_arrow(ORIGIN, result_dir, color=GREEN, stroke_width=6)

        label_result = Tex("\\vec{a} - \\vec{b}", font_size=42, color=GREEN)
        label_result.next_to(vec_result.get_end(), DR, buff=0.2)

        self.play(GrowArrow(vec_result), run_time=1.5)
        self.play(FadeIn(label_result, scale=1.3))
        self.wait()

        # ========================================
        # FINALE: Emphasize the result
        # ========================================
        checkmark = Tex("\\checkmark", font_size=72, color=GREEN)
        checkmark.next_to(question, LEFT, buff=0.5)

        self.play(FadeIn(checkmark, scale=2))
        self.wait(2)


# ============================================================
# 6. SCENE EXECUTION ORDER
# ============================================================
# The order of scenes that tells the story.
#
# Scene 1 (IntroduceVectors):
#   - Introduces vectors as arrows with magnitude and direction
#   - Shows examples on a coordinate plane
#   - Establishes the question: how do we add vectors?
#
# Scene 2 (VectorAddition):
#   - Demonstrates the tip-to-tail method of vector addition
#   - Shows how to translate the second vector to the tip of the first
#   - Reveals the resultant vector from origin to final point
#
# Scene 3 (ParallelogramLaw):
#   - Shows the alternative parallelogram construction
#   - Demonstrates that the diagonal equals the sum
#   - Reveals the beautiful geometric structure
#
# Scene 4 (VectorSubtraction):
#   - Extends to vector subtraction
#   - Shows that a - b = a + (-b)
#   - Completes the picture of vector operations

SCENE_ORDER = [
    IntroduceVectors,       # Part 1: What are vectors?
    VectorAddition,         # Part 2: Tip-to-tail addition
    ParallelogramLaw,       # Part 3: Parallelogram construction
    VectorSubtraction,      # Part 4: Subtraction as adding negatives
]
