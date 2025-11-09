"""
Natural Group Name: Null Space and Kernel of Transformation

Educational Objectives:
- To visualize the null space as vectors that map to zero
- To demonstrate the geometric meaning of the kernel
- To show the relationship between null space and linear independence
- To connect null space to the rank-nullity theorem

Story Arc & Intent:
The animation reveals the null space through geometric transformation: some
vectors get "crushed" to zero when a matrix is applied. This transforms the
abstract algebraic concept into a visual process of finding which directions
disappear under transformation.

Narrative Flow:
- Hook/Opening: A matrix transformation and vectors mapping to zero
- Development: Finding all vectors in the null space
- Build-up: Geometric interpretation as a subspace
- Climax: The rank-nullity theorem connecting dimensions
- Resolution: Applications to solving homogeneous systems

Technical Implementation Notes:
- Scene Classes: IntroduceTransformation, VectorsToZero, GeometricMeaning, RankNullity
- Key Visual Elements: Grids, transformations, vectors, subspaces
- Animation Techniques: Grid transformation, vector highlighting, dimension visualization
- Mathematical Concepts: Null space, kernel, rank, nullity, dimension

Dependency Chain:
All scenes use basic manimlib components: NumberPlane, vectors, Matrix, Tex.
Matrix operations use numpy. No custom utilities required beyond helper
functions defined in this file.

Rendering Instructions:
To render these scenes, use the manim command-line tool:
- For a single scene: manimgl null_space.py IntroduceTransformation
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
# - YELLOW: Transformed vectors
# - GREEN: Null space vectors
# - RED: Zero vector
# - WHITE: Grid and labels
# - GREY_A: De-emphasized elements
#
# Key Manim Constants Used:
# - UP, DOWN, LEFT, RIGHT: Direction vectors
# - ORIGIN: Center point
# - PI: π for calculations
# - MED_SMALL_BUFF: Spacing

# Example matrix with non-trivial null space
# This matrix has rank 1 (projects onto a line)
MATRIX_A = np.array([
    [2, 4],
    [1, 2]
])

# Null space basis: [-2, 1]
NULL_BASIS = np.array([-2, 1])

# ============================================================
# 3. UTILITY FUNCTIONS
# ============================================================

def create_vector_arrow(vec, color=BLUE, **kwargs):
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
        stroke_width=4,
        tip_length=0.25,
        **kwargs
    )

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

def is_in_null_space(vec, matrix, tolerance=1e-6):
    """
    Check if a vector is in the null space of a matrix.

    Args:
        vec: Vector to check
        matrix: Matrix
        tolerance: Numerical tolerance

    Returns:
        True if Av ≈ 0
    """
    result = matrix @ vec
    return np.linalg.norm(result) < tolerance

# ============================================================
# 4. SCENE CLASSES
# ============================================================

class IntroduceTransformation(Scene):
    """
    Scene 1: Introduce a matrix transformation and the zero vector.

    This scene shows how a matrix transforms vectors, and asks: which
    vectors get mapped to zero?
    """

    def construct(self):
        # ========================================
        # TITLE
        # ========================================
        title = Text("Null Space (Kernel) of a Matrix", font_size=42)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait()

        # ========================================
        # MATRIX
        # ========================================
        matrix_label = Text("Consider the transformation:", font_size=28)
        matrix_label.next_to(title, DOWN, buff=0.5)

        # Display matrix
        A_entries = [[Text("2"), Text("4")], [Text("1"), Text("2")]]
        A_matrix = Matrix(A_entries, bracket_h_buff=0.1, bracket_v_buff=0.1)
        A_matrix.set_color(BLUE)

        matrix_display = VGroup(
            Tex("A = "),
            A_matrix
        )
        matrix_display.arrange(RIGHT, buff=0.2)
        matrix_display.next_to(matrix_label, DOWN, buff=0.4)

        self.play(Write(matrix_label))
        self.play(Write(matrix_display))
        self.wait()

        # ========================================
        # GRID VISUALIZATION
        # ========================================
        grid = create_grid(color=BLUE, opacity=0.4)
        grid.scale(0.7)
        grid.shift(DOWN * 0.5)

        self.play(ShowCreation(grid))
        self.wait()

        # Show a few vectors
        vec1 = create_vector_arrow([1, 0], color=YELLOW)
        vec2 = create_vector_arrow([0, 1], color=YELLOW)
        vec3 = create_vector_arrow([1, 1], color=YELLOW)

        vectors = VGroup(vec1, vec2, vec3)

        for vec in vectors:
            vec.scale(0.7)
            vec.shift(DOWN * 0.5)

        self.play(*[GrowArrow(vec) for vec in vectors])
        self.wait()

        # ========================================
        # QUESTION
        # ========================================
        question = Text(
            "Which vectors map to zero?",
            font_size=28,
            color=GREEN
        )
        question.to_edge(DOWN).shift(UP * 0.5)

        self.play(FadeIn(question, shift=UP))
        self.wait()

        # Show definition
        definition = Tex(
            "\\text{Null}(A) = \\{\\vec{v} : A\\vec{v} = \\vec{0}\\}",
            font_size=32,
            color=GREEN
        )
        definition.next_to(question, DOWN, buff=0.3)

        self.play(Write(definition))
        self.wait(2)


class VectorsToZero(Scene):
    """
    Scene 2: Find vectors that map to zero.

    This scene shows how to solve Av = 0 and find the null space basis.
    """

    def construct(self):
        # ========================================
        # TITLE
        # ========================================
        title = Text("Finding the Null Space", font_size=42)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait()

        # ========================================
        # EQUATION
        # ========================================
        equation = Tex(
            "A\\vec{v} = \\vec{0}",
            font_size=36
        )
        equation.next_to(title, DOWN, buff=0.6)

        self.play(Write(equation))
        self.wait()

        # ========================================
        # SYSTEM
        # ========================================
        system_label = Text("This gives the system:", font_size=28)
        system_label.next_to(equation, DOWN, buff=0.6)

        system = VGroup(
            Tex("2x + 4y = 0", font_size=30),
            Tex("x + 2y = 0", font_size=30),
        )
        system.arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        system.next_to(system_label, DOWN, buff=0.4)

        self.play(Write(system_label))
        for eq in system:
            self.play(Write(eq))
            self.wait(0.3)

        # ========================================
        # OBSERVE: Dependent equations
        # ========================================
        observation = Text(
            "Notice: Second equation = first equation ÷ 2",
            font_size=24,
            color=YELLOW
        )
        observation.next_to(system, DOWN, buff=0.5)

        self.play(FadeIn(observation, shift=UP))
        self.wait()

        # ========================================
        # SOLVE
        # ========================================
        self.play(FadeOut(observation))

        solving = Text("From 2x + 4y = 0:", font_size=26)
        solving.next_to(system, DOWN, buff=0.5)

        self.play(Write(solving))
        self.wait()

        solution_step1 = Tex("x = -2y", font_size=28, color=GREEN)
        solution_step1.next_to(solving, DOWN, buff=0.3)

        self.play(Write(solution_step1))
        self.wait()

        # ========================================
        # PARAMETRIC FORM
        # ========================================
        parametric = Text("Parametric form (let y = t):", font_size=26)
        parametric.next_to(solution_step1, DOWN, buff=0.5)

        self.play(Write(parametric))
        self.wait()

        parametric_form = Tex(
            "\\vec{v} = \\begin{bmatrix} -2t \\\\ t \\end{bmatrix} = t \\begin{bmatrix} -2 \\\\ 1 \\end{bmatrix}",
            font_size=32,
            color=GREEN
        )
        parametric_form.next_to(parametric, DOWN, buff=0.4)

        self.play(Write(parametric_form))
        self.wait()

        # ========================================
        # BASIS
        # ========================================
        basis = Tex(
            "\\text{Null space basis: } \\begin{bmatrix} -2 \\\\ 1 \\end{bmatrix}",
            font_size=32,
            color=GREEN
        )
        basis.to_edge(DOWN).shift(UP * 0.5)

        basis_box = SurroundingRectangle(basis, buff=0.2, color=GREEN, stroke_width=2)

        self.play(Write(basis))
        self.play(ShowCreation(basis_box))
        self.wait(2)


class GeometricMeaning(Scene):
    """
    Scene 3: Show the geometric meaning of the null space.

    This scene visualizes the null space as a line (or subspace) that
    gets collapsed to zero under the transformation.
    """

    def construct(self):
        # ========================================
        # TITLE
        # ========================================
        title = Text("Geometric Interpretation", font_size=42)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait()

        # ========================================
        # SETUP: Grid
        # ========================================
        grid = create_grid(color=BLUE, opacity=0.4)

        self.play(ShowCreation(grid))
        self.wait()

        # ========================================
        # NULL SPACE LINE
        # ========================================
        null_space_label = Text(
            "Null space: all vectors along this line",
            font_size=26,
            color=GREEN
        )
        null_space_label.next_to(title, DOWN, buff=0.4)

        self.play(Write(null_space_label))
        self.wait()

        # Draw the null space line
        null_line = Line(
            4 * np.array([NULL_BASIS[0], NULL_BASIS[1], 0]),
            -4 * np.array([NULL_BASIS[0], NULL_BASIS[1], 0]),
            color=GREEN,
            stroke_width=4
        )

        self.play(ShowCreation(null_line))
        self.wait()

        # Show several vectors in null space
        null_vectors = VGroup()
        scalars = [-1.5, -0.75, 0.75, 1.5]

        for t in scalars:
            vec = create_vector_arrow(t * NULL_BASIS, color=GREEN)
            null_vectors.add(vec)

        self.play(*[GrowArrow(vec) for vec in null_vectors])
        self.wait()

        # ========================================
        # TRANSFORMATION
        # ========================================
        self.play(FadeOut(null_space_label))

        transform_label = Text(
            "Apply transformation A",
            font_size=26,
            color=YELLOW
        )
        transform_label.next_to(title, DOWN, buff=0.4)

        self.play(Write(transform_label))
        self.wait()

        # Transform everything
        self.play(
            ApplyMatrix(MATRIX_A, grid),
            *[ApplyMatrix(MATRIX_A, vec) for vec in null_vectors],
            ApplyMatrix(MATRIX_A, null_line),
            run_time=2.5
        )
        self.wait()

        # ========================================
        # RESULT: Collapsed to zero
        # ========================================
        self.play(FadeOut(transform_label))

        result = Text(
            "Null space vectors all map to zero!",
            font_size=28,
            color=RED
        )
        result.next_to(title, DOWN, buff=0.4)

        self.play(Write(result))
        self.wait()

        # Highlight the origin
        zero_dot = Dot(ORIGIN, color=RED, radius=0.15)
        zero_label = Tex("\\vec{0}", color=RED, font_size=32)
        zero_label.next_to(zero_dot, DOWN, buff=0.3)

        self.play(FadeIn(zero_dot, scale=0.5))
        self.play(Write(zero_label))
        self.wait()

        # ========================================
        # DIMENSION
        # ========================================
        dimension = VGroup(
            Text("Null space is a 1D subspace (a line)", font_size=24),
            Tex("\\text{dim}(\\text{Null}(A)) = 1", font_size=28, color=GREEN),
        )
        dimension.arrange(DOWN, buff=0.3)
        dimension.to_edge(DOWN).shift(UP * 0.5)

        for line in dimension:
            self.play(FadeIn(line, shift=UP))
            self.wait(0.5)

        self.wait(2)


class RankNullity(Scene):
    """
    Scene 4: Present the rank-nullity theorem.

    This scene shows the relationship between rank and nullity,
    connecting the dimensions of column space and null space.
    """

    def construct(self):
        # ========================================
        # TITLE
        # ========================================
        title = Text("The Rank-Nullity Theorem", font_size=42)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait()

        # ========================================
        # DEFINITIONS
        # ========================================
        definitions = VGroup(
            Tex("\\text{Rank}(A) = \\text{dimension of column space}", font_size=28),
            Tex("\\text{Nullity}(A) = \\text{dimension of null space}", font_size=28),
        )
        definitions.arrange(DOWN, buff=0.4, aligned_edge=LEFT)
        definitions.next_to(title, DOWN, buff=0.8)

        for defn in definitions:
            self.play(Write(defn))
            self.wait(0.5)

        # ========================================
        # THE THEOREM
        # ========================================
        theorem_label = Text("Rank-Nullity Theorem:", font_size=32, color=YELLOW)
        theorem_label.next_to(definitions, DOWN, buff=0.8)

        theorem = Tex(
            "\\text{Rank}(A) + \\text{Nullity}(A) = n",
            font_size=40,
            color=YELLOW
        )
        theorem.next_to(theorem_label, DOWN, buff=0.5)

        theorem_box = SurroundingRectangle(theorem, buff=0.3, color=YELLOW, stroke_width=3)

        self.play(Write(theorem_label))
        self.play(Write(theorem))
        self.play(ShowCreation(theorem_box))
        self.wait()

        # Explanation
        explanation = Tex(
            "n = \\text{number of columns (dimension of domain)}",
            font_size=24,
            color=GREY_A
        )
        explanation.next_to(theorem, DOWN, buff=0.4)

        self.play(Write(explanation))
        self.wait()

        # ========================================
        # EXAMPLE
        # ========================================
        self.play(
            FadeOut(definitions),
            FadeOut(theorem_label),
            FadeOut(explanation)
        )

        example_title = Text("Our example:", font_size=28, color=BLUE)
        example_title.next_to(title, DOWN, buff=0.6)

        self.play(Write(example_title))
        self.wait()

        example = VGroup(
            Tex("A = \\begin{bmatrix} 2 & 4 \\\\ 1 & 2 \\end{bmatrix}", font_size=32),
            Tex("\\text{Rank}(A) = 1 \\text{ (columns are dependent)}", font_size=26),
            Tex("\\text{Nullity}(A) = 1 \\text{ (1D null space)}", font_size=26),
            Tex("1 + 1 = 2 \\text{ (number of columns)} \\checkmark", font_size=26, color=GREEN),
        )
        example.arrange(DOWN, buff=0.4, aligned_edge=LEFT)
        example.next_to(example_title, DOWN, buff=0.5)

        for line in example:
            self.play(Write(line))
            self.wait(0.5)

        self.wait()

        # ========================================
        # APPLICATIONS
        # ========================================
        self.play(FadeOut(example_title), FadeOut(example))

        applications_title = Text("Applications:", font_size=32, color=WHITE)
        applications_title.next_to(title, DOWN, buff=0.6)

        applications = VGroup(
            Text("• Solving homogeneous systems Ax = 0", font_size=24),
            Text("• Determining linear independence", font_size=24),
            Text("• Finding free variables in systems", font_size=24),
            Text("• Understanding dimension relationships", font_size=24),
            Text("• Characterizing invertibility (null space = {0})", font_size=24),
        )
        applications.arrange(DOWN, buff=0.25, aligned_edge=LEFT)
        applications.next_to(applications_title, DOWN, buff=0.5)

        self.play(Write(applications_title))
        self.wait()

        for item in applications:
            self.play(FadeIn(item, shift=UP))
            self.wait(0.4)

        self.wait()

        # ========================================
        # KEY INSIGHT
        # ========================================
        self.play(FadeOut(applications_title), FadeOut(applications))

        insight = VGroup(
            Text("Key Insight:", font_size=32, color=GREEN),
            Text("The null space tells us which directions", font_size=26),
            Text("get 'lost' or 'collapsed' by the transformation", font_size=26),
        )
        insight.arrange(DOWN, buff=0.3)
        insight.move_to(ORIGIN)

        for line in insight:
            self.play(FadeIn(line, shift=UP))
            self.wait(0.5)

        self.wait(2)


# ============================================================
# 5. SCENE SUMMARY AND EXECUTION ORDER
# ============================================================
#
# Scene 1 (IntroduceTransformation):
#   - Introduces a matrix transformation
#   - Poses the question: which vectors map to zero?
#   - Defines the null space as {v : Av = 0}
#
# Scene 2 (VectorsToZero):
#   - Solves Av = 0 to find null space
#   - Shows system of equations
#   - Finds parametric form and basis
#
# Scene 3 (GeometricMeaning):
#   - Visualizes null space as a line
#   - Shows transformation collapsing it to zero
#   - Demonstrates dimension of null space
#
# Scene 4 (RankNullity):
#   - Presents rank-nullity theorem
#   - Shows example calculation
#   - Discusses applications and key insights

SCENE_ORDER = [
    IntroduceTransformation,   # Part 1: The null space question
    VectorsToZero,             # Part 2: Finding the null space
    GeometricMeaning,          # Part 3: Geometric visualization
    RankNullity,               # Part 4: Rank-nullity theorem
]
