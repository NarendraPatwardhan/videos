"""
Natural Group Name: Determinants as Area Scaling

Educational Objectives:
- To visualize determinants as measuring how matrices scale areas
- To build geometric intuition for the determinant concept
- To show how linear transformations affect areas and volumes
- To connect abstract linear algebra to concrete geometric reasoning

Story Arc & Intent:
The animation transforms the abstract concept of determinants into something
visual and intuitive: they measure how much a linear transformation scales
areas (in 2D) or volumes (in 3D). This geometric perspective makes determinants
meaningful and memorable.

Narrative Flow:
- Hook/Opening: Show a unit square and ask what happens when transformed
- Development: Apply various matrix transformations and measure resulting areas
- Build-up: Show that det(M) always equals the scaling factor
- Climax: Demonstrate negative determinants (orientation reversal)
- Resolution: State the general principle clearly
- Extension: Mention 3D case and other applications

Technical Implementation Notes:
- Scene Classes: UnitSquare, LinearTransform, MeasureArea, GeneralPrinciple
- Key Visual Elements: 2D grids, unit square, transformed shapes, area labels
- Animation Techniques: Matrix transformations, grid deformation, area highlighting
- Mathematical Concepts: Linear transformations, determinants, area scaling

Dependency Chain:
All scenes are independent. They use NumberPlane, Polygon, Matrix, and Tex
from manimlib. Utility functions handle matrix transformations and area calculations.

Rendering Instructions:
To render these scenes, use the manim command-line tool:
- For a single scene: manimgl determinants_area.py UnitSquare
- For all scenes in sequence: iterate through SCENE_ORDER
"""

# ============================================================
# 1. IMPORTS
# ============================================================
from manimlib import *
import numpy as np

# ============================================================
# 2. CONFIGURATION AND CONSTANTS
# ============================================================
# Grid and plane configuration
GRID_CONFIG = {
    "x_range": (-5, 5, 1),
    "y_range": (-5, 5, 1),
    "width": 10,
    "height": 10,
}

# Colors
UNIT_SQUARE_COLOR = BLUE
TRANSFORMED_SQUARE_COLOR = YELLOW
GRID_COLOR = GREY_B
MATRIX_COLOR = GREEN
DETERMINANT_COLOR = RED

# Animation parameters
TRANSFORM_RUN_TIME = 3

# ============================================================
# 3. UTILITY FUNCTIONS
# ============================================================

def create_unit_square():
    """
    Create a unit square at the origin.

    Returns:
        Polygon representing unit square
    """
    square = Polygon(
        ORIGIN,
        RIGHT,
        RIGHT + UP,
        UP
    )
    square.set_fill(UNIT_SQUARE_COLOR, opacity=0.5)
    square.set_stroke(UNIT_SQUARE_COLOR, width=3)
    return square

def apply_matrix_to_mobject(mobject, matrix):
    """
    Apply a 2x2 matrix transformation to a mobject.

    Args:
        mobject: The mobject to transform
        matrix: 2x2 numpy array

    Returns:
        Transformed mobject
    """
    # Apply the linear transformation
    def transform_func(point):
        x, y = point[0], point[1]
        new_x = matrix[0, 0] * x + matrix[0, 1] * y
        new_y = matrix[1, 0] * x + matrix[1, 1] * y
        return np.array([new_x, new_y, 0])

    return mobject.copy().apply_function(lambda p: transform_func(p))

def calculate_determinant(matrix):
    """
    Calculate determinant of 2x2 matrix.

    Args:
        matrix: 2x2 numpy array

    Returns:
        Determinant value
    """
    return matrix[0, 0] * matrix[1, 1] - matrix[0, 1] * matrix[1, 0]

def calculate_parallelogram_area(v1, v2):
    """
    Calculate area of parallelogram formed by two vectors.

    Args:
        v1, v2: 2D vectors

    Returns:
        Area (absolute value of cross product)
    """
    return abs(v1[0] * v2[1] - v1[1] * v2[0])

def create_matrix_tex(matrix, font_size=40):
    """
    Create a nice Tex representation of a 2x2 matrix.

    Args:
        matrix: 2x2 numpy array
        font_size: Font size

    Returns:
        Tex object
    """
    a, b = matrix[0, 0], matrix[0, 1]
    c, d = matrix[1, 0], matrix[1, 1]

    # Format numbers nicely
    def fmt(x):
        if x == int(x):
            return str(int(x))
        return f"{x:.1f}"

    tex = Tex(
        R"\begin{bmatrix} " + fmt(a) + R" & " + fmt(b) + R" \\ " +
        fmt(c) + R" & " + fmt(d) + R" \end{bmatrix}",
        font_size=font_size
    )
    return tex

# ============================================================
# 4. BASE CLASSES AND HELPERS
# ============================================================
# No custom base classes needed

# ============================================================
# 5. SCENE IMPLEMENTATIONS
# ============================================================

class UnitSquare(InteractiveScene):
    """
    Part 1: Introduce the unit square and grid.

    Narrative purpose:
        To establish the baseline: a unit square with area 1 on a grid,
        which we'll transform and measure in subsequent scenes.

    Mathematical content:
        Shows the standard basis vectors and unit square, establishing
        that it has area 1.

    Visual approach:
        Display a coordinate grid, highlight the unit square formed by
        basis vectors, and explicitly label its area.
    """
    def construct(self):
        # ========================================
        # SETUP: Title
        # ========================================
        title = Text("Determinants Measure Area Scaling", font_size=44)
        title.to_edge(UP)

        self.play(FadeIn(title, shift=DOWN))
        self.wait()

        # ========================================
        # CREATE: Coordinate plane
        # ========================================
        plane = NumberPlane(**GRID_CONFIG)
        plane.set_stroke(GRID_COLOR, width=1, opacity=0.5)

        self.play(ShowCreation(plane))
        self.wait()

        # ========================================
        # CREATE: Basis vectors
        # ========================================
        i_hat = Arrow(ORIGIN, RIGHT, buff=0, color=GREEN, stroke_width=6)
        j_hat = Arrow(ORIGIN, UP, buff=0, color=RED, stroke_width=6)

        i_label = Tex(R"\hat{\imath}", font_size=36, color=GREEN)
        i_label.next_to(i_hat, DOWN, buff=0.1)

        j_label = Tex(R"\hat{\jmath}", font_size=36, color=RED)
        j_label.next_to(j_hat, LEFT, buff=0.1)

        self.play(
            GrowArrow(i_hat),
            GrowArrow(j_hat),
            Write(i_label),
            Write(j_label)
        )
        self.wait()

        # ========================================
        # CREATE: Unit square
        # ========================================
        square = create_unit_square()

        self.play(DrawBorderThenFill(square))
        self.wait()

        # ========================================
        # LABEL: Area = 1
        # ========================================
        area_label = Tex(R"\text{Area} = 1", font_size=40, color=YELLOW)
        area_label.move_to(square.get_center())

        self.play(FadeIn(area_label, scale=1.3))
        self.wait(2)

        # ========================================
        # MESSAGE: What happens when we transform?
        # ========================================
        question = Text(
            "What happens to the area under a linear transformation?",
            font_size=32
        )
        question.to_edge(DOWN, buff=0.5)

        self.play(Write(question))
        self.wait(3)

        # ========================================
        # CLEANUP
        # ========================================
        self.play(FadeOut(*self.mobjects), run_time=1)
        self.wait()


class LinearTransform(InteractiveScene):
    """
    Part 2: Apply a linear transformation and observe.

    Narrative purpose:
        To show concretely how a matrix transformation changes the unit
        square and its area, setting up the determinant interpretation.

    Mathematical content:
        Applies a specific matrix transformation (e.g., [[2, 1], [0, 2]])
        and shows how the unit square becomes a parallelogram.

    Visual approach:
        Animate the grid and square transforming, measure the new area,
        and calculate the determinant to show they match.
    """
    def construct(self):
        # ========================================
        # SETUP: Title and plane
        # ========================================
        title = Text("Applying a Linear Transformation", font_size=44)
        title.to_edge(UP)

        plane = NumberPlane(**GRID_CONFIG)
        plane.set_stroke(GRID_COLOR, width=1, opacity=0.5)

        self.add(plane)
        self.play(FadeIn(title, shift=DOWN))
        self.wait()

        # ========================================
        # CREATE: Unit square
        # ========================================
        square = create_unit_square()
        square.save_state()

        area_label = Tex(R"\text{Area} = 1", font_size=36, color=BLUE)
        area_label.move_to(square.get_center())

        self.play(
            DrawBorderThenFill(square),
            Write(area_label)
        )
        self.wait()

        # ========================================
        # DEFINE: Matrix transformation
        # ========================================
        matrix = np.array([[2, 1], [0, 2]], dtype=float)

        matrix_tex = create_matrix_tex(matrix)
        matrix_tex.to_corner(UL, buff=0.8)
        matrix_tex.shift(0.8 * DOWN)

        matrix_label = Text("Matrix M:", font_size=32)
        matrix_label.next_to(matrix_tex, UP, buff=0.3, aligned_edge=LEFT)

        self.play(
            Write(matrix_label),
            Write(matrix_tex)
        )
        self.wait()

        # ========================================
        # APPLY: Transformation
        # ========================================
        # Transform the entire plane
        self.play(
            plane.animate.apply_matrix(matrix),
            square.animate.apply_matrix(matrix),
            FadeOut(area_label),
            run_time=TRANSFORM_RUN_TIME
        )
        self.wait()

        # ========================================
        # MEASURE: New area
        # ========================================
        # The new vertices are at (0,0), (2,0), (3,2), (1,2)
        det = calculate_determinant(matrix)

        new_area_label = Tex(
            f"\\text{{New Area}} = {det:.0f}",
            font_size=36,
            color=YELLOW
        )
        # Position at transformed square center
        transformed_center = matrix @ np.array([0.5, 0.5])
        new_area_label.move_to([transformed_center[0], transformed_center[1], 0])

        self.play(Write(new_area_label))
        self.wait(2)

        # ========================================
        # CALCULATE: Determinant
        # ========================================
        det_calc = Tex(
            R"\det(M) = 2 \cdot 2 - 1 \cdot 0 = 4",
            font_size=36,
            color=DETERMINANT_COLOR
        )
        det_calc.to_edge(DOWN, buff=0.8)

        self.play(Write(det_calc))
        self.wait(2)

        # ========================================
        # OBSERVE: They match!
        # ========================================
        observation = Text(
            "The determinant equals the area scaling factor!",
            font_size=32,
            color=GREEN
        )
        observation.next_to(det_calc, UP, buff=0.5)

        self.play(FadeIn(observation, shift=UP))
        self.wait(3)

        # ========================================
        # CLEANUP
        # ========================================
        self.play(FadeOut(*self.mobjects), run_time=1)
        self.wait()


class MeasureArea(InteractiveScene):
    """
    Part 3: Test with multiple transformations.

    Narrative purpose:
        To verify the determinant-area relationship holds for various
        transformations, including scaling, rotation, and shear.

    Mathematical content:
        Shows several different matrices and verifies that in each case,
        det(M) equals the area scaling factor.

    Visual approach:
        For each transformation, show the matrix, apply it, measure the
        new area, and compare to the determinant.
    """
    def construct(self):
        # ========================================
        # SETUP: Title
        # ========================================
        title = Text("Testing Multiple Transformations", font_size=44)
        title.to_edge(UP)

        self.play(FadeIn(title, shift=DOWN))
        self.wait()

        # ========================================
        # TEST 1: Scaling matrix
        # ========================================
        self.test_transformation(
            matrix=np.array([[3, 0], [0, 2]], dtype=float),
            name="Scaling"
        )

        # ========================================
        # TEST 2: Shear matrix
        # ========================================
        self.test_transformation(
            matrix=np.array([[1, 2], [0, 1]], dtype=float),
            name="Shear"
        )

        # ========================================
        # TEST 3: Rotation + scaling
        # ========================================
        # 45-degree rotation times sqrt(2) scaling
        angle = PI / 4
        scale = np.sqrt(2)
        matrix = scale * np.array([
            [np.cos(angle), -np.sin(angle)],
            [np.sin(angle), np.cos(angle)]
        ])
        self.test_transformation(
            matrix=matrix,
            name="Rotation + Scale"
        )

        # ========================================
        # CONCLUSION
        # ========================================
        self.play(FadeOut(*self.mobjects))

        conclusion = Text(
            "In every case:\ndet(M) = Area Scaling Factor",
            font_size=40,
            color=YELLOW,
            weight=BOLD
        )
        conclusion.move_to(ORIGIN)

        self.play(FadeIn(conclusion, scale=1.3))
        self.wait(4)

        self.play(FadeOut(conclusion))
        self.wait()

    def test_transformation(self, matrix, name):
        """Helper to test a specific transformation."""
        # Setup plane and square
        plane = NumberPlane(**GRID_CONFIG)
        plane.set_stroke(GRID_COLOR, width=1, opacity=0.3)

        square = create_unit_square()

        # Labels
        test_label = Text(f"Test: {name}", font_size=32)
        test_label.to_corner(UL, buff=0.5)

        matrix_tex = create_matrix_tex(matrix, font_size=32)
        matrix_tex.next_to(test_label, DOWN, buff=0.3, aligned_edge=LEFT)

        det = calculate_determinant(matrix)
        det_label = Tex(
            f"\\det(M) = {det:.2f}",
            font_size=32,
            color=DETERMINANT_COLOR
        )
        det_label.next_to(matrix_tex, DOWN, buff=0.3, aligned_edge=LEFT)

        # Show setup
        self.play(
            ShowCreation(plane),
            DrawBorderThenFill(square),
            Write(test_label),
            Write(matrix_tex),
            Write(det_label)
        )
        self.wait()

        # Apply transformation
        self.play(
            plane.animate.apply_matrix(matrix),
            square.animate.apply_matrix(matrix).set_color(TRANSFORMED_SQUARE_COLOR),
            run_time=2
        )
        self.wait()

        # Show area
        area_label = Tex(
            f"\\text{{Area}} = {abs(det):.2f}",
            font_size=32,
            color=YELLOW
        )
        area_label.next_to(det_label, DOWN, buff=0.3, aligned_edge=LEFT)

        self.play(Write(area_label))
        self.wait()

        # Checkmark
        check = Tex(R"\checkmark", font_size=48, color=GREEN)
        check.next_to(area_label, RIGHT, buff=0.5)

        self.play(FadeIn(check, scale=2))
        self.wait(2)

        # Cleanup
        self.play(
            FadeOut(plane),
            FadeOut(square),
            FadeOut(test_label),
            FadeOut(matrix_tex),
            FadeOut(det_label),
            FadeOut(area_label),
            FadeOut(check)
        )


class GeneralPrinciple(InteractiveScene):
    """
    Part 4: State the general principle and discuss implications.

    Narrative purpose:
        To formalize the geometric interpretation of determinants and
        discuss important cases like negative determinants and det=0.

    Mathematical content:
        States that det(M) represents the signed area scaling factor.
        Negative determinants indicate orientation reversal. Zero
        determinant means area collapses to zero (singular matrix).

    Visual approach:
        Show examples of positive/negative/zero determinants with
        clear visual explanations of what each means geometrically.
    """
    def construct(self):
        # ========================================
        # SETUP: Title
        # ========================================
        title = Text("The General Principle", font_size=48)
        title.to_edge(UP)

        self.play(FadeIn(title, shift=DOWN))
        self.wait()

        # ========================================
        # STATE: Main principle
        # ========================================
        principle = Tex(
            R"\det(M) = \text{signed area scaling factor}",
            font_size=48,
            color=YELLOW
        )
        principle.shift(1.5 * UP)

        box = SurroundingRectangle(principle, buff=0.4, color=YELLOW, stroke_width=4)

        self.play(
            Write(principle),
            ShowCreation(box)
        )
        self.wait(2)

        # ========================================
        # CASE 1: Positive determinant
        # ========================================
        case1 = VGroup(
            Tex(R"\det(M) > 0", font_size=36, color=GREEN),
            Text("→ Preserves orientation", font_size=28),
            Text("Area scaled by |det(M)|", font_size=28)
        )
        case1.arrange(DOWN, buff=0.2, aligned_edge=LEFT)
        case1.shift(0.3 * UP + 3 * LEFT)

        self.play(FadeIn(case1, shift=RIGHT))
        self.wait(2)

        # ========================================
        # CASE 2: Negative determinant
        # ========================================
        case2 = VGroup(
            Tex(R"\det(M) < 0", font_size=36, color=RED),
            Text("→ Reverses orientation", font_size=28),
            Text("Area scaled by |det(M)|", font_size=28)
        )
        case2.arrange(DOWN, buff=0.2, aligned_edge=LEFT)
        case2.shift(0.3 * UP + 3 * RIGHT)

        self.play(FadeIn(case2, shift=LEFT))
        self.wait(2)

        # ========================================
        # CASE 3: Zero determinant
        # ========================================
        case3 = VGroup(
            Tex(R"\det(M) = 0", font_size=36, color=GREY_A),
            Text("→ Collapses to lower dimension", font_size=28),
            Text("Area becomes zero (singular)", font_size=28)
        )
        case3.arrange(DOWN, buff=0.2, aligned_edge=LEFT)
        case3.shift(1.5 * DOWN)

        self.play(FadeIn(case3, shift=UP))
        self.wait(3)

        # ========================================
        # VISUAL EXAMPLE: Negative determinant
        # ========================================
        self.play(
            FadeOut(case1),
            FadeOut(case2),
            FadeOut(case3),
            VGroup(principle, box).animate.scale(0.6).to_corner(UL, buff=0.5)
        )

        example_title = Text("Example: Negative Determinant", font_size=36)
        example_title.shift(1.5 * UP)

        self.play(Write(example_title))
        self.wait()

        # Matrix with negative determinant (reflection)
        neg_matrix = np.array([[1, 0], [0, -1]], dtype=float)

        plane = NumberPlane(**GRID_CONFIG)
        plane.set_stroke(GRID_COLOR, width=1, opacity=0.3)
        plane.scale(0.4).shift(2 * DOWN)

        square = create_unit_square()
        square.scale(0.4).shift(2 * DOWN)

        # Label original orientation
        orientation_before = Text("Before: ↺", font_size=28, color=BLUE)
        orientation_before.next_to(square, UP, buff=0.3)

        self.play(
            ShowCreation(plane),
            DrawBorderThenFill(square),
            Write(orientation_before)
        )
        self.wait()

        # Apply transformation
        self.play(
            plane.animate.apply_matrix(neg_matrix),
            square.animate.apply_matrix(neg_matrix).set_color(RED),
            run_time=2
        )

        # Label new orientation
        orientation_after = Text("After: ↻ (reversed!)", font_size=28, color=RED)
        orientation_after.move_to(orientation_before)

        self.play(
            FadeOut(orientation_before),
            Write(orientation_after)
        )
        self.wait(2)

        det_neg = Tex(R"\det(M) = -1", font_size=32, color=RED)
        det_neg.next_to(plane, RIGHT, buff=1)

        self.play(Write(det_neg))
        self.wait(3)

        # ========================================
        # FINAL MESSAGE
        # ========================================
        self.play(FadeOut(*self.mobjects))

        final = Text(
            "Determinants give us geometric insight\ninto linear transformations!",
            font_size=40,
            color=YELLOW,
            weight=BOLD
        )
        final.move_to(ORIGIN)

        self.play(FadeIn(final, scale=1.2))
        self.wait(4)

        self.play(FadeOut(final))
        self.wait()


# ============================================================
# 6. SCENE EXECUTION ORDER
# ============================================================
# The order of scenes that tells the story.
#
# Scene 1 (UnitSquare):
#   - Introduces the unit square with area 1
#   - Sets up the coordinate system
#   - Poses the transformation question
#
# Scene 2 (LinearTransform):
#   - Applies a specific matrix transformation
#   - Shows area change matches determinant
#   - Demonstrates the core insight
#
# Scene 3 (MeasureArea):
#   - Tests multiple different transformations
#   - Verifies det(M) = scaling factor in each case
#   - Builds confidence in the principle
#
# Scene 4 (GeneralPrinciple):
#   - States the general principle formally
#   - Discusses positive/negative/zero cases
#   - Shows orientation reversal example
#   - Emphasizes geometric interpretation

SCENE_ORDER = [
    UnitSquare,            # Part 1: Setup
    LinearTransform,       # Part 2: First example
    MeasureArea,           # Part 3: Multiple tests
    GeneralPrinciple,      # Part 4: General theory
]
