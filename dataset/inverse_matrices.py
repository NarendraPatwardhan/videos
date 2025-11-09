"""
Natural Group Name: Matrix Inverse and Solving Systems

Educational Objectives:
- To visualize the matrix inverse as undoing a transformation
- To demonstrate AA⁻¹ = I geometrically
- To show how matrix inverse solves linear systems Ax = b
- To illustrate when matrices are invertible vs singular

Story Arc & Intent:
The animation reveals the matrix inverse through the concept of reversing a
transformation: if A transforms space, then A⁻¹ reverses that transformation
back to the original. This transforms the abstract algebraic operation into
a visual, intuitive process of undoing geometric changes.

Narrative Flow:
- Hook/Opening: A matrix transforms vectors in space
- Development: The inverse transformation that undoes the change
- Build-up: AA⁻¹ = I means A⁻¹ perfectly reverses A
- Climax: Using A⁻¹ to solve Ax = b by computing x = A⁻¹b
- Resolution: When inverse exists (invertible) vs doesn't exist (singular)

Technical Implementation Notes:
- Scene Classes: IntroduceSystem, InverseTransform, SolvingEquations, NonInvertible
- Key Visual Elements: Grids, transformations, vectors, systems of equations
- Animation Techniques: Grid transformation, vector tracking, matrix visualization
- Mathematical Concepts: Matrix inverse, linear systems, determinant, singularity

Dependency Chain:
All scenes use basic manimlib components: NumberPlane, Matrix, Vector, Tex.
Matrix operations use numpy. No custom utilities required beyond helper
functions defined in this file.

Rendering Instructions:
To render these scenes, use the manim command-line tool:
- For a single scene: manimgl inverse_matrices.py IntroduceSystem
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
# - BLUE: Original vectors/space
# - YELLOW: Transformed vectors/space
# - GREEN: Identity transformation / Solutions
# - RED: Singular/non-invertible matrices
# - WHITE: Grid and labels
# - GREY_A: De-emphasized elements
#
# Key Manim Constants Used:
# - UP, DOWN, LEFT, RIGHT: Direction vectors
# - ORIGIN: Center point
# - PI: π for calculations
# - MED_SMALL_BUFF: Spacing

# Example matrix (invertible)
MATRIX_A = np.array([
    [2, 1],
    [1, 2]
])

# Inverse of A
MATRIX_A_INV = np.linalg.inv(MATRIX_A)

# Singular matrix example
SINGULAR_MATRIX = np.array([
    [2, 4],
    [1, 2]
])

# ============================================================
# 3. UTILITY FUNCTIONS
# ============================================================

def create_grid(color=BLUE, opacity=0.3, **kwargs):
    """
    Create a number plane grid.

    Args:
        color: Color of grid lines
        opacity: Opacity of grid
        **kwargs: Additional arguments

    Returns:
        NumberPlane mobject
    """
    plane = NumberPlane(
        x_range=[-4, 4, 1],
        y_range=[-4, 4, 1],
        background_line_style={
            "stroke_color": color,
            "stroke_width": 1,
            "stroke_opacity": opacity,
        },
        **kwargs
    )
    return plane

def apply_matrix_to_plane(plane, matrix):
    """
    Apply a matrix transformation to a plane.

    Args:
        plane: NumberPlane object
        matrix: 2x2 numpy array

    Returns:
        Animation applying the transformation
    """
    return ApplyMatrix(matrix, plane)

def create_matrix_display(matrix, color=WHITE, **kwargs):
    """
    Create a visual display of a matrix.

    Args:
        matrix: 2x2 numpy array
        color: Color of the matrix
        **kwargs: Additional arguments

    Returns:
        Matrix mobject
    """
    entries = [[DecimalNumber(matrix[i][j], num_decimal_places=2) for j in range(2)] for i in range(2)]

    mat = Matrix(entries, **kwargs)
    mat.set_color(color)

    return mat

def create_vector_arrow(vec, color=YELLOW, **kwargs):
    """
    Create an arrow representing a vector.

    Args:
        vec: 2D vector [x, y]
        color: Color of arrow
        **kwargs: Additional arguments

    Returns:
        Arrow mobject
    """
    return Arrow(
        ORIGIN,
        np.array([vec[0], vec[1], 0]),
        color=color,
        buff=0,
        stroke_width=5,
        tip_length=0.3,
        **kwargs
    )

# ============================================================
# 4. SCENE CLASSES
# ============================================================

class IntroduceSystem(Scene):
    """
    Scene 1: Introduce a linear system and matrix transformation.

    This scene presents a system of linear equations Ax = b and shows
    how the matrix A transforms vectors in the plane.
    """

    def construct(self):
        # ========================================
        # TITLE
        # ========================================
        title = OldTexText("Matrix Inverse and Linear Systems", font_size=42)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait()

        # ========================================
        # LINEAR SYSTEM
        # ========================================
        system_label = OldTexText("System of equations:", font_size=28)
        system_label.next_to(title, DOWN, buff=0.6)

        system = VGroup(
            Tex("2x + y = 5", font_size=32),
            Tex("x + 2y = 4", font_size=32),
        )
        system.arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        system.next_to(system_label, DOWN, buff=0.4)

        self.play(Write(system_label))
        for eq in system:
            self.play(Write(eq))
            self.wait(0.3)

        self.wait()

        # ========================================
        # MATRIX FORM
        # ========================================
        matrix_label = OldTexText("Matrix form:", font_size=28)
        matrix_label.next_to(system, DOWN, buff=0.8)

        # Create matrix equation
        A_entries = [[OldTexText("2"), OldTexText("1")], [OldTexText("1"), OldTexText("2")]]
        A_matrix = Matrix(A_entries, bracket_h_buff=0.1, bracket_v_buff=0.1)
        A_matrix.set_color(BLUE)

        x_vec = Matrix([[OldTexText("x")], [OldTexText("y")]], bracket_h_buff=0.05, bracket_v_buff=0.1)

        equals = Tex("=")

        b_vec = Matrix([[OldTexText("5")], [OldTexText("4")]], bracket_h_buff=0.05, bracket_v_buff=0.1)
        b_vec.set_color(GREEN)

        matrix_eq = VGroup(A_matrix, x_vec, equals, b_vec)
        matrix_eq.arrange(RIGHT, buff=0.3)
        matrix_eq.next_to(matrix_label, DOWN, buff=0.4)

        self.play(Write(matrix_label))
        self.play(
            Write(A_matrix),
            Write(x_vec),
            Write(equals),
            Write(b_vec)
        )
        self.wait()

        # ========================================
        # NOTATION
        # ========================================
        notation = Tex("A\\vec{x} = \\vec{b}", font_size=36, color=YELLOW)
        notation.next_to(matrix_eq, DOWN, buff=0.6)

        self.play(Write(notation))
        self.wait()

        # ========================================
        # QUESTION
        # ========================================
        question = OldTexText(
            "How do we solve for x?",
            font_size=28,
            color=WHITE
        )
        question.to_edge(DOWN).shift(UP * 0.5)

        self.play(FadeIn(question, shift=UP))
        self.wait(2)


class InverseTransform(Scene):
    """
    Scene 2: Show the inverse transformation geometrically.

    This scene visualizes the matrix A as transforming the grid, and
    A⁻¹ as the transformation that reverses it back.
    """

    def construct(self):
        # ========================================
        # TITLE
        # ========================================
        title = OldTexText("The Inverse Transformation", font_size=42)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait()

        # ========================================
        # ORIGINAL GRID
        # ========================================
        original_grid = create_grid(color=BLUE, opacity=0.5)

        grid_label = OldTexText("Original space", font_size=24, color=BLUE)
        grid_label.to_edge(DOWN).shift(UP * 0.5)

        self.play(ShowCreation(original_grid))
        self.play(Write(grid_label))
        self.wait()

        # Show basis vectors
        i_hat = create_vector_arrow([1, 0], color=GREEN)
        j_hat = create_vector_arrow([0, 1], color=RED)

        i_label = Tex("\\hat{i}", color=GREEN, font_size=28)
        i_label.next_to(i_hat.get_end(), RIGHT, buff=0.1)

        j_label = Tex("\\hat{j}", color=RED, font_size=28)
        j_label.next_to(j_hat.get_end(), UP, buff=0.1)

        self.play(GrowArrow(i_hat), GrowArrow(j_hat))
        self.play(Write(i_label), Write(j_label))
        self.wait()

        # ========================================
        # APPLY MATRIX A
        # ========================================
        self.play(FadeOut(grid_label))

        transform_label = Tex(
            "\\text{Apply } A = \\begin{bmatrix} 2 & 1 \\\\ 1 & 2 \\end{bmatrix}",
            font_size=28,
            color=YELLOW
        )
        transform_label.to_edge(DOWN).shift(UP * 0.5)

        self.play(Write(transform_label))
        self.wait()

        # Transform grid and vectors
        self.play(
            ApplyMatrix(MATRIX_A, original_grid),
            ApplyMatrix(MATRIX_A, i_hat),
            ApplyMatrix(MATRIX_A, j_hat),
            i_label.animate.move_to(MATRIX_A @ np.array([1, 0, 0]) + RIGHT * 0.5),
            j_label.animate.move_to(MATRIX_A @ np.array([0, 1, 0]) + UP * 0.5),
            run_time=2
        )
        self.wait()

        # ========================================
        # SHOW INVERSE
        # ========================================
        self.play(FadeOut(transform_label))

        inverse_label = Tex(
            "\\text{Apply } A^{-1} \\text{ to reverse}",
            font_size=28,
            color=GREEN
        )
        inverse_label.to_edge(DOWN).shift(UP * 0.5)

        self.play(Write(inverse_label))
        self.wait()

        # Apply inverse transformation
        self.play(
            ApplyMatrix(MATRIX_A_INV, original_grid),
            ApplyMatrix(MATRIX_A_INV, i_hat),
            ApplyMatrix(MATRIX_A_INV, j_hat),
            i_label.animate.move_to(np.array([1, 0, 0]) + RIGHT * 0.3),
            j_label.animate.move_to(np.array([0, 1, 0]) + UP * 0.3),
            run_time=2
        )
        self.wait()

        # ========================================
        # BACK TO ORIGINAL
        # ========================================
        self.play(FadeOut(inverse_label))

        result = OldTexText(
            "Back to the original space!",
            font_size=28,
            color=GREEN
        )
        result.to_edge(DOWN).shift(UP * 0.5)

        self.play(FadeIn(result, shift=UP))
        self.wait()

        # ========================================
        # IDENTITY PROPERTY
        # ========================================
        identity = Tex(
            "A A^{-1} = I = \\begin{bmatrix} 1 & 0 \\\\ 0 & 1 \\end{bmatrix}",
            font_size=32,
            color=WHITE
        )
        identity.next_to(title, DOWN, buff=0.5)

        self.play(Write(identity))
        self.wait(2)


class SolvingEquations(Scene):
    """
    Scene 3: Use the inverse to solve Ax = b.

    This scene shows how multiplying both sides by A⁻¹ gives x = A⁻¹b,
    solving the linear system.
    """

    def construct(self):
        # ========================================
        # TITLE
        # ========================================
        title = OldTexText("Solving with the Inverse", font_size=42)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait()

        # ========================================
        # ORIGINAL EQUATION
        # ========================================
        original = Tex(
            "A\\vec{x} = \\vec{b}",
            font_size=40
        )
        original.next_to(title, DOWN, buff=0.8)

        self.play(Write(original))
        self.wait()

        # ========================================
        # MULTIPLY BY A⁻¹
        # ========================================
        step1_text = OldTexText("Multiply both sides by A⁻¹:", font_size=28)
        step1_text.next_to(original, DOWN, buff=0.6)

        self.play(FadeIn(step1_text, shift=DOWN))
        self.wait()

        step1 = Tex(
            "A^{-1} A \\vec{x} = A^{-1} \\vec{b}",
            font_size=36
        )
        step1.next_to(step1_text, DOWN, buff=0.4)

        self.play(Write(step1))
        self.wait()

        # ========================================
        # SIMPLIFY: A⁻¹A = I
        # ========================================
        step2_text = OldTexText("Since A⁻¹A = I:", font_size=28)
        step2_text.next_to(step1, DOWN, buff=0.6)

        self.play(FadeIn(step2_text, shift=DOWN))
        self.wait()

        step2 = Tex(
            "I \\vec{x} = A^{-1} \\vec{b}",
            font_size=36
        )
        step2.next_to(step2_text, DOWN, buff=0.4)

        self.play(Write(step2))
        self.wait()

        # ========================================
        # FINAL: x = A⁻¹b
        # ========================================
        step3_text = OldTexText("And Ix = x, so:", font_size=28)
        step3_text.next_to(step2, DOWN, buff=0.6)

        self.play(FadeIn(step3_text, shift=DOWN))
        self.wait()

        solution = Tex(
            "\\vec{x} = A^{-1} \\vec{b}",
            font_size=44,
            color=GREEN
        )
        solution.next_to(step3_text, DOWN, buff=0.4)

        solution_box = SurroundingRectangle(solution, buff=0.3, color=GREEN, stroke_width=3)

        self.play(Write(solution))
        self.play(ShowCreation(solution_box))
        self.wait()

        # ========================================
        # CONCRETE EXAMPLE
        # ========================================
        self.play(
            FadeOut(original),
            FadeOut(step1_text),
            FadeOut(step1),
            FadeOut(step2_text),
            FadeOut(step2),
            FadeOut(step3_text)
        )

        example_title = OldTexText("Example:", font_size=32, color=YELLOW)
        example_title.next_to(title, DOWN, buff=0.6)

        self.play(
            solution.animate.next_to(example_title, DOWN, buff=0.4),
            solution_box.animate.next_to(example_title, DOWN, buff=0.4),
            Write(example_title)
        )
        self.wait()

        # Compute A⁻¹
        A_inv_display = Tex(
            "A^{-1} = \\frac{1}{3}\\begin{bmatrix} 2 & -1 \\\\ -1 & 2 \\end{bmatrix}",
            font_size=28
        )
        A_inv_display.next_to(solution_box, DOWN, buff=0.6)

        self.play(Write(A_inv_display))
        self.wait()

        # Given b = [5, 4]
        b_given = Tex(
            "\\vec{b} = \\begin{bmatrix} 5 \\\\ 4 \\end{bmatrix}",
            font_size=28
        )
        b_given.next_to(A_inv_display, DOWN, buff=0.4)

        self.play(Write(b_given))
        self.wait()

        # Compute x
        computation = Tex(
            "\\vec{x} = \\frac{1}{3}\\begin{bmatrix} 2 & -1 \\\\ -1 & 2 \\end{bmatrix} \\begin{bmatrix} 5 \\\\ 4 \\end{bmatrix} = \\frac{1}{3}\\begin{bmatrix} 6 \\\\ 3 \\end{bmatrix} = \\begin{bmatrix} 2 \\\\ 1 \\end{bmatrix}",
            font_size=24
        )
        computation.next_to(b_given, DOWN, buff=0.5)

        self.play(Write(computation))
        self.wait()

        # Answer
        answer = Tex(
            "\\text{Solution: } x = 2, \\, y = 1",
            font_size=32,
            color=GREEN
        )
        answer.to_edge(DOWN).shift(UP * 0.5)

        self.play(FadeIn(answer, shift=UP))
        self.wait(2)


class NonInvertible(Scene):
    """
    Scene 4: Show when a matrix is NOT invertible (singular).

    This scene demonstrates that some matrices don't have inverses,
    specifically when they collapse space into a lower dimension.
    """

    def construct(self):
        # ========================================
        # TITLE
        # ========================================
        title = OldTexText("When is a Matrix NOT Invertible?", font_size=38)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait()

        # ========================================
        # INVERTIBLE CONDITION
        # ========================================
        condition = OldTexText(
            "A matrix is invertible if and only if det(A) ≠ 0",
            font_size=28,
            color=YELLOW
        )
        condition.next_to(title, DOWN, buff=0.5)

        self.play(Write(condition))
        self.wait()

        # ========================================
        # SINGULAR MATRIX EXAMPLE
        # ========================================
        singular_title = OldTexText("Singular (non-invertible) matrix:", font_size=26, color=RED)
        singular_title.next_to(condition, DOWN, buff=0.8)

        singular_display = Tex(
            "A = \\begin{bmatrix} 2 & 4 \\\\ 1 & 2 \\end{bmatrix}",
            font_size=32,
            color=RED
        )
        singular_display.next_to(singular_title, DOWN, buff=0.3)

        self.play(Write(singular_title))
        self.play(Write(singular_display))
        self.wait()

        # Determinant
        det_calc = Tex(
            "\\det(A) = (2)(2) - (4)(1) = 0",
            font_size=28
        )
        det_calc.next_to(singular_display, DOWN, buff=0.4)

        self.play(Write(det_calc))
        self.wait()

        # ========================================
        # GEOMETRIC INTERPRETATION
        # ========================================
        self.play(
            FadeOut(singular_title),
            FadeOut(singular_display),
            FadeOut(det_calc)
        )

        geo_title = OldTexText("Geometric interpretation:", font_size=28)
        geo_title.next_to(condition, DOWN, buff=0.6)

        self.play(Write(geo_title))
        self.wait()

        # Create grid
        grid = create_grid(color=BLUE, opacity=0.4)
        grid.scale(0.7)
        grid.shift(DOWN * 0.5)

        self.play(ShowCreation(grid))
        self.wait()

        # Show transformation collapsing to a line
        collapse_text = OldTexText(
            "This matrix collapses 2D space onto a line!",
            font_size=24,
            color=RED
        )
        collapse_text.to_edge(DOWN).shift(UP * 0.5)

        self.play(Write(collapse_text))
        self.wait()

        self.play(
            ApplyMatrix(SINGULAR_MATRIX, grid),
            run_time=2.5
        )
        self.wait()

        # ========================================
        # CONSEQUENCE
        # ========================================
        self.play(FadeOut(collapse_text))

        consequence = VGroup(
            OldTexText("Consequences:", font_size=26, color=WHITE),
            OldTexText("• Cannot reverse this transformation", font_size=22),
            OldTexText("• Lost information (flattened dimension)", font_size=22),
            OldTexText("• No unique solution to Ax = b", font_size=22),
            OldTexText("• Either no solution or infinite solutions", font_size=22),
        )
        consequence.arrange(DOWN, buff=0.25, aligned_edge=LEFT)
        consequence.to_edge(DOWN).shift(UP * 0.3)

        for item in consequence:
            self.play(FadeIn(item, shift=UP))
            self.wait(0.4)

        self.wait()

        # ========================================
        # SUMMARY
        # ========================================
        self.play(FadeOut(grid), FadeOut(geo_title), FadeOut(consequence))

        summary = VGroup(
            OldTexText("Summary:", font_size=32, color=GREEN),
            OldTexText("Invertible (det ≠ 0):", font_size=24),
            OldTexText("  • Unique solution x = A⁻¹b", font_size=22),
            OldTexText("  • Transformation is reversible", font_size=22),
            OldTexText("Non-invertible (det = 0):", font_size=24, color=RED),
            OldTexText("  • No inverse exists", font_size=22),
            OldTexText("  • Collapses space", font_size=22),
            OldTexText("  • No unique solution", font_size=22),
        )
        summary.arrange(DOWN, buff=0.2, aligned_edge=LEFT)
        summary.next_to(condition, DOWN, buff=0.6)

        for item in summary:
            self.play(FadeIn(item, shift=UP), run_time=0.3)

        self.wait(2)


# ============================================================
# 5. SCENE SUMMARY AND EXECUTION ORDER
# ============================================================
#
# Scene 1 (IntroduceSystem):
#   - Introduces a system of linear equations
#   - Shows matrix form Ax = b
#   - Poses the question of solving for x
#
# Scene 2 (InverseTransform):
#   - Visualizes matrix A as a geometric transformation
#   - Shows A⁻¹ as the reverse transformation
#   - Demonstrates AA⁻¹ = I geometrically
#
# Scene 3 (SolvingEquations):
#   - Derives x = A⁻¹b algebraically
#   - Computes a concrete example
#   - Shows the solution process
#
# Scene 4 (NonInvertible):
#   - Shows when matrices are NOT invertible
#   - Demonstrates det = 0 condition
#   - Visualizes collapse of dimensions
#   - Explains consequences for solutions

SCENE_ORDER = [
    IntroduceSystem,       # Part 1: The linear system problem
    InverseTransform,      # Part 2: Inverse as reverse transformation
    SolvingEquations,      # Part 3: Using inverse to solve
    NonInvertible,         # Part 4: When inverse doesn't exist
]
