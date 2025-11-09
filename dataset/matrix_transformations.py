"""
Natural Group Name: 2D Linear Transformations with Matrices

Educational Objectives:
- To visualize matrices as linear transformations of the plane
- To demonstrate how matrices transform space through grid deformation
- To show specific transformations: shear, rotation, scaling, reflection
- To build intuition for matrix multiplication as composition of transformations

Story Arc & Intent:
The animation reveals matrices as geometric transformations rather than arrays
of numbers. By watching how a grid deforms under various transformations, the
abstract matrix operations become concrete geometric actions on the plane.

Narrative Flow:
- Hook/Opening: A regular grid representing the coordinate plane
- Development: Apply shear transformation, showing how space distorts
- Build-up: Show rotation preserving lengths and angles
- Climax: Demonstrate composition of transformations (matrix multiplication)
- Resolution: General principle - matrices transform space in specific ways

Technical Implementation Notes:
- Scene Classes: IntroduceGrid, ShearTransform, RotationTransform, ComposedTransforms
- Key Visual Elements: Number plane grid, basis vectors, transformed vectors
- Animation Techniques: Grid deformation, vector transformation, sequential composition
- Mathematical Concepts: Linear transformations, basis vectors, matrix multiplication

Dependency Chain:
All scenes use basic manimlib components: NumberPlane, Vector, Arrow, Text, Tex.
No custom utilities required.

Rendering Instructions:
To render these scenes, use the manim command-line tool:
- For a single scene: manimgl matrix_transformations.py IntroduceGrid
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
# - GREEN: i-hat (x-axis basis vector)
# - RED: j-hat (y-axis basis vector)
# - YELLOW: Transformed vectors
# - BLUE: Grid lines
# - WHITE: Axes and labels
# - GREY_A: De-emphasized elements
#
# Key Manim Constants Used:
# - UP, DOWN, LEFT, RIGHT: Direction vectors
# - ORIGIN: Center point
# - PI: π for rotations
# - DEGREES: Angle conversion

# Grid configuration
GRID_CONFIG = {
    "x_range": (-5, 5, 1),
    "y_range": (-5, 5, 1),
    "width": 10,
    "height": 10,
}

# Vector styling
VECTOR_CONFIG = {
    "buff": 0,
    "stroke_width": 5,
    "max_tip_length_to_length_ratio": 0.2,
}

# Basis vector colors
I_HAT_COLOR = GREEN
J_HAT_COLOR = RED

# ============================================================
# 3. UTILITY FUNCTIONS
# ============================================================

def create_basis_vectors(plane, i_color=I_HAT_COLOR, j_color=J_HAT_COLOR):
    """
    Create the standard basis vectors i-hat and j-hat.

    Args:
        plane: NumberPlane object
        i_color: Color for i-hat
        j_color: Color for j-hat

    Returns:
        VGroup containing i-hat and j-hat
    """
    i_hat = Arrow(
        plane.c2p(0, 0),
        plane.c2p(1, 0),
        color=i_color,
        **VECTOR_CONFIG
    )

    j_hat = Arrow(
        plane.c2p(0, 0),
        plane.c2p(0, 1),
        color=j_color,
        **VECTOR_CONFIG
    )

    return VGroup(i_hat, j_hat)

def create_basis_labels(plane, i_hat, j_hat):
    """
    Create labels for basis vectors.

    Args:
        plane: NumberPlane object
        i_hat: i-hat arrow
        j_hat: j-hat arrow

    Returns:
        VGroup containing labels
    """
    i_label = Tex("\\hat{i}", font_size=36, color=I_HAT_COLOR)
    i_label.next_to(i_hat.get_end(), DR, buff=0.1)

    j_label = Tex("\\hat{j}", font_size=36, color=J_HAT_COLOR)
    j_label.next_to(j_hat.get_end(), UL, buff=0.1)

    return VGroup(i_label, j_label)

def get_matrix_text(matrix, position=ORIGIN):
    """
    Create a matrix display.

    Args:
        matrix: 2x2 numpy array
        position: Position for the matrix

    Returns:
        Tex mobject showing the matrix
    """
    a, b = matrix[0]
    c, d = matrix[1]

    matrix_tex = Tex(
        f"\\begin{{bmatrix}} {a:.1f} & {b:.1f} \\\\ {c:.1f} & {d:.1f} \\end{{bmatrix}}",
        font_size=48
    )
    matrix_tex.move_to(position)

    return matrix_tex

def apply_matrix_to_plane(plane, matrix):
    """
    Apply a matrix transformation to a plane.

    Args:
        plane: NumberPlane object
        matrix: 2x2 transformation matrix

    Returns:
        Animation that applies the transformation
    """
    return plane.animate.apply_matrix(matrix)

# ============================================================
# 4. BASE CLASSES AND HELPERS
# ============================================================
# No custom base classes needed

# ============================================================
# 5. SCENE IMPLEMENTATIONS
# ============================================================

class IntroduceGrid(InteractiveScene):
    """
    Part 1: Introduce the coordinate grid and basis vectors.

    Narrative purpose:
        To establish the coordinate system and basis vectors as the
        foundation for understanding linear transformations.

    Mathematical content:
        The standard basis vectors i-hat = (1,0) and j-hat = (0,1)
        define the coordinate system. Any vector can be written as
        a linear combination of these basis vectors.

    Visual approach:
        Show a grid, highlight the basis vectors, and explain that
        transformations will move these vectors (and the entire grid).
    """
    def construct(self):
        # ========================================
        # SETUP: Title
        # ========================================
        title = OldTexText("Linear Transformations", font_size=48)
        title.to_edge(UP)

        self.play(FadeIn(title, shift=DOWN))
        self.wait()

        # ========================================
        # CREATE: Grid
        # ========================================
        plane = NumberPlane(**GRID_CONFIG)
        plane.add_coordinates()

        self.play(ShowCreation(plane), run_time=2)
        self.wait()

        # ========================================
        # CREATE: Basis vectors
        # ========================================
        basis_vectors = create_basis_vectors(plane)
        i_hat, j_hat = basis_vectors

        basis_labels = create_basis_labels(plane, i_hat, j_hat)
        i_label, j_label = basis_labels

        self.play(
            GrowArrow(i_hat),
            GrowArrow(j_hat)
        )
        self.play(
            FadeIn(i_label, shift=UL),
            FadeIn(j_label, shift=DR)
        )
        self.wait()

        # ========================================
        # EXPLAIN: Basis vectors
        # ========================================
        explanation = OldTexText(
            "These basis vectors define our coordinate system",
            font_size=32,
            color=GREY_A
        )
        explanation.to_edge(DOWN, buff=0.8)

        self.play(FadeIn(explanation, shift=UP))
        self.wait()

        # ========================================
        # EXAMPLE: Show a general vector
        # ========================================
        self.play(FadeOut(explanation))

        example_vector = Arrow(
            plane.c2p(0, 0),
            plane.c2p(3, 2),
            color=YELLOW,
            **VECTOR_CONFIG
        )

        vector_label = Tex("\\vec{v} = 3\\hat{i} + 2\\hat{j}", font_size=36, color=YELLOW)
        vector_label.next_to(example_vector.get_end(), UR, buff=0.2)

        self.play(GrowArrow(example_vector))
        self.play(FadeIn(vector_label, shift=DL))
        self.wait()

        # ========================================
        # QUESTION: What happens when we transform?
        # ========================================
        question = OldTexText(
            "What happens when we transform the space?",
            font_size=36,
            color=YELLOW
        )
        question.to_edge(DOWN, buff=0.5)

        self.play(FadeIn(question, shift=UP))
        self.wait(2)


class ShearTransform(InteractiveScene):
    """
    Part 2: Demonstrate a shear transformation.

    Narrative purpose:
        To show a concrete example of a linear transformation that
        distorts the grid while keeping lines straight and parallel.

    Mathematical content:
        Shear transformation matrix [[1, 1], [0, 1]] keeps i-hat fixed
        but moves j-hat to (1, 1), causing a horizontal shear effect.

    Visual approach:
        Apply shear transformation to the grid, showing how it deforms.
        Track the basis vectors to show where they end up.
    """
    def construct(self):
        # ========================================
        # SETUP: Title
        # ========================================
        title = OldTexText("Shear Transformation", font_size=48)
        title.to_edge(UP)

        self.add(title)

        # ========================================
        # CREATE: Grid and basis vectors
        # ========================================
        plane = NumberPlane(**GRID_CONFIG)
        plane.add_coordinates()

        basis_vectors = create_basis_vectors(plane)
        i_hat, j_hat = basis_vectors

        basis_labels = create_basis_labels(plane, i_hat, j_hat)

        self.add(plane, i_hat, j_hat, basis_labels[0], basis_labels[1])

        # ========================================
        # SHOW: Transformation matrix
        # ========================================
        shear_matrix = np.array([[1, 1], [0, 1]])

        matrix_display = get_matrix_text(shear_matrix)
        matrix_display.to_corner(UL, buff=0.8)
        matrix_display.shift(0.5 * DOWN)

        matrix_label = OldTexText("Shear Matrix:", font_size=32)
        matrix_label.next_to(matrix_display, UP, buff=0.3)

        self.play(
            FadeIn(matrix_label, shift=DOWN),
            Write(matrix_display)
        )
        self.wait()

        # ========================================
        # EXPLAIN: What it does
        # ========================================
        explanation = VGroup(
            Tex("\\hat{i} \\to (1, 0)", font_size=28, color=I_HAT_COLOR),
            Tex("\\hat{j} \\to (1, 1)", font_size=28, color=J_HAT_COLOR)
        )
        explanation.arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        explanation.next_to(matrix_display, DOWN, buff=0.5)

        self.play(FadeIn(explanation, shift=UP))
        self.wait()

        # ========================================
        # APPLY: Transformation
        # ========================================
        instruction = OldTexText("Watch the grid transform...", font_size=32, color=GREY_A)
        instruction.to_edge(DOWN, buff=0.5)

        self.play(FadeIn(instruction, shift=UP))
        self.wait()

        # New positions for basis vectors
        new_i_hat = Arrow(
            plane.c2p(0, 0),
            plane.c2p(1, 0),
            color=I_HAT_COLOR,
            **VECTOR_CONFIG
        )

        new_j_hat = Arrow(
            plane.c2p(0, 0),
            plane.c2p(1, 1),
            color=J_HAT_COLOR,
            **VECTOR_CONFIG
        )

        self.play(
            plane.animate.apply_matrix(shear_matrix),
            Transform(i_hat, new_i_hat),
            Transform(j_hat, new_j_hat),
            run_time=3
        )
        self.wait(2)

        # ========================================
        # HIGHLIGHT: The effect
        # ========================================
        self.play(FadeOut(instruction))

        result_text = OldTexText(
            "Space has been sheared horizontally!",
            font_size=36,
            color=YELLOW
        )
        result_text.to_edge(DOWN, buff=0.5)

        self.play(FadeIn(result_text, shift=UP))
        self.wait(2)


class RotationTransform(InteractiveScene):
    """
    Part 3: Demonstrate a rotation transformation.

    Narrative purpose:
        To show a transformation that preserves distances and angles,
        rotating the entire plane by a fixed angle.

    Mathematical content:
        Rotation by θ has matrix [[cos(θ), -sin(θ)], [sin(θ), cos(θ)]].
        For θ = 90°, this becomes [[0, -1], [1, 0]].

    Visual approach:
        Apply a 90° rotation, showing the grid rotating while maintaining
        its structure (preserving distances and angles).
    """
    def construct(self):
        # ========================================
        # SETUP: Title
        # ========================================
        title = OldTexText("Rotation Transformation", font_size=48)
        title.to_edge(UP)

        self.add(title)

        # ========================================
        # CREATE: Grid and basis vectors
        # ========================================
        plane = NumberPlane(**GRID_CONFIG)
        plane.add_coordinates()

        basis_vectors = create_basis_vectors(plane)
        i_hat, j_hat = basis_vectors

        basis_labels = create_basis_labels(plane, i_hat, j_hat)

        self.add(plane, i_hat, j_hat, basis_labels[0], basis_labels[1])

        # ========================================
        # SHOW: Rotation matrix (90 degrees)
        # ========================================
        angle = PI / 2
        rotation_matrix = np.array([
            [np.cos(angle), -np.sin(angle)],
            [np.sin(angle), np.cos(angle)]
        ])

        matrix_display = get_matrix_text(rotation_matrix)
        matrix_display.to_corner(UL, buff=0.8)
        matrix_display.shift(0.5 * DOWN)

        matrix_label = OldTexText("90° Rotation Matrix:", font_size=32)
        matrix_label.next_to(matrix_display, UP, buff=0.3)

        self.play(
            FadeIn(matrix_label, shift=DOWN),
            Write(matrix_display)
        )
        self.wait()

        # ========================================
        # EXPLAIN: What it does
        # ========================================
        explanation = VGroup(
            Tex("\\hat{i} \\to (0, 1)", font_size=28, color=I_HAT_COLOR),
            Tex("\\hat{j} \\to (-1, 0)", font_size=28, color=J_HAT_COLOR)
        )
        explanation.arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        explanation.next_to(matrix_display, DOWN, buff=0.5)

        self.play(FadeIn(explanation, shift=UP))
        self.wait()

        # ========================================
        # APPLY: Rotation
        # ========================================
        instruction = OldTexText("Rotating 90° counterclockwise...", font_size=32, color=GREY_A)
        instruction.to_edge(DOWN, buff=0.5)

        self.play(FadeIn(instruction, shift=UP))
        self.wait()

        # New basis vectors after rotation
        new_i_hat = Arrow(
            plane.c2p(0, 0),
            plane.c2p(0, 1),
            color=I_HAT_COLOR,
            **VECTOR_CONFIG
        )

        new_j_hat = Arrow(
            plane.c2p(0, 0),
            plane.c2p(-1, 0),
            color=J_HAT_COLOR,
            **VECTOR_CONFIG
        )

        self.play(
            Rotate(plane, angle=angle, about_point=plane.c2p(0, 0)),
            Transform(i_hat, new_i_hat),
            Transform(j_hat, new_j_hat),
            run_time=3
        )
        self.wait(2)

        # ========================================
        # HIGHLIGHT: Properties preserved
        # ========================================
        self.play(FadeOut(instruction))

        result_text = OldTexText(
            "Rotation preserves distances and angles!",
            font_size=36,
            color=GREEN
        )
        result_text.to_edge(DOWN, buff=0.5)

        self.play(FadeIn(result_text, shift=UP))
        self.wait(2)


class ComposedTransforms(InteractiveScene):
    """
    Part 4: Demonstrate composition of transformations (matrix multiplication).

    Narrative purpose:
        To show that applying multiple transformations sequentially
        corresponds to matrix multiplication, revealing why we multiply
        matrices the way we do.

    Mathematical content:
        Applying transformation B then A is equivalent to applying
        the single transformation AB (matrix product).

    Visual approach:
        Apply two transformations in sequence (rotation then shear),
        then show this is equivalent to their matrix product.
    """
    def construct(self):
        # ========================================
        # SETUP: Title
        # ========================================
        title = OldTexText("Composed Transformations", font_size=48)
        title.to_edge(UP)

        self.add(title)

        # ========================================
        # CREATE: Grid and basis vectors
        # ========================================
        plane = NumberPlane(**GRID_CONFIG)
        plane.add_coordinates()

        basis_vectors = create_basis_vectors(plane)
        i_hat, j_hat = basis_vectors

        self.add(plane, i_hat, j_hat)

        # ========================================
        # SHOW: Two transformations
        # ========================================
        shear_matrix = np.array([[1, 1], [0, 1]])
        rotation_matrix = np.array([[0, -1], [1, 0]])

        matrices_display = VGroup(
            Tex("\\text{First: Shear}", font_size=32),
            get_matrix_text(shear_matrix),
            Tex("\\text{Then: Rotate 90°}", font_size=32),
            get_matrix_text(rotation_matrix)
        )
        matrices_display.arrange(DOWN, buff=0.3)
        matrices_display.to_corner(UL, buff=0.5)

        self.play(FadeIn(matrices_display, shift=RIGHT))
        self.wait()

        # ========================================
        # APPLY: First transformation (shear)
        # ========================================
        step1_text = OldTexText("Step 1: Shear", font_size=32, color=YELLOW)
        step1_text.to_edge(DOWN, buff=0.8)

        self.play(FadeIn(step1_text, shift=UP))
        self.wait()

        # Apply shear
        new_i_hat_1 = Arrow(
            plane.c2p(0, 0),
            plane.c2p(1, 0),
            color=I_HAT_COLOR,
            **VECTOR_CONFIG
        )

        new_j_hat_1 = Arrow(
            plane.c2p(0, 0),
            plane.c2p(1, 1),
            color=J_HAT_COLOR,
            **VECTOR_CONFIG
        )

        self.play(
            plane.animate.apply_matrix(shear_matrix),
            Transform(i_hat, new_i_hat_1),
            Transform(j_hat, new_j_hat_1),
            run_time=2
        )
        self.wait()

        # ========================================
        # APPLY: Second transformation (rotation)
        # ========================================
        step2_text = OldTexText("Step 2: Rotate 90°", font_size=32, color=YELLOW)
        step2_text.to_edge(DOWN, buff=0.8)

        self.play(Transform(step1_text, step2_text))
        self.wait()

        # Calculate final positions: rotation applied to sheared basis
        # After shear: i_hat = (1, 0), j_hat = (1, 1)
        # After rotation: i_hat_final = rotation @ (1, 0) = (0, 1)
        #                 j_hat_final = rotation @ (1, 1) = (-1, 1)

        final_i = rotation_matrix @ np.array([1, 0])
        final_j = rotation_matrix @ np.array([1, 1])

        new_i_hat_2 = Arrow(
            plane.c2p(0, 0),
            plane.c2p(final_i[0], final_i[1]),
            color=I_HAT_COLOR,
            **VECTOR_CONFIG
        )

        new_j_hat_2 = Arrow(
            plane.c2p(0, 0),
            plane.c2p(final_j[0], final_j[1]),
            color=J_HAT_COLOR,
            **VECTOR_CONFIG
        )

        self.play(
            Rotate(plane, angle=PI/2, about_point=plane.c2p(0, 0)),
            Transform(i_hat, new_i_hat_2),
            Transform(j_hat, new_j_hat_2),
            run_time=2
        )
        self.wait()

        # ========================================
        # SHOW: Equivalent to matrix product
        # ========================================
        self.play(FadeOut(step1_text))

        # Calculate product
        product_matrix = rotation_matrix @ shear_matrix

        product_display = VGroup(
            OldTexText("Equivalent to single transformation:", font_size=28),
            get_matrix_text(product_matrix, ORIGIN)
        )
        product_display.arrange(DOWN, buff=0.3)
        product_display.to_edge(DOWN, buff=0.5)

        box = SurroundingRectangle(product_display[1], buff=0.2, color=GREEN, stroke_width=3)

        self.play(FadeIn(product_display, shift=UP))
        self.play(ShowCreation(box))
        self.wait()

        # ========================================
        # INSIGHT: Matrix multiplication
        # ========================================
        insight = OldTexText(
            "This is why we multiply matrices!",
            font_size=36,
            color=GREEN
        )
        insight.next_to(product_display, DOWN, buff=0.5)

        self.play(FadeIn(insight, shift=UP))
        self.wait(3)


# ============================================================
# 6. SCENE EXECUTION ORDER
# ============================================================
# The order of scenes that tells the story.
#
# Scene 1 (IntroduceGrid):
#   - Introduces the coordinate grid and basis vectors
#   - Establishes i-hat and j-hat as the foundation
#   - Sets up the question of transformation
#
# Scene 2 (ShearTransform):
#   - Demonstrates a shear transformation
#   - Shows how the grid deforms under the transformation
#   - Tracks where basis vectors move
#
# Scene 3 (RotationTransform):
#   - Demonstrates a 90° rotation
#   - Shows how rotation preserves structure
#   - Highlights distance and angle preservation
#
# Scene 4 (ComposedTransforms):
#   - Shows composition of transformations
#   - Demonstrates that sequential application equals matrix multiplication
#   - Reveals the geometric meaning of matrix multiplication

SCENE_ORDER = [
    IntroduceGrid,          # Part 1: Basis vectors and grid
    ShearTransform,         # Part 2: Shear transformation
    RotationTransform,      # Part 3: Rotation transformation
    ComposedTransforms,     # Part 4: Composition and multiplication
]
