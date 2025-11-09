"""
Change of Basis in Linear Algebra

This module demonstrates the concept of change of basis in linear algebra.
Shows how the same vector can be represented in different coordinate systems
and how to construct change of basis matrices.

Scenes:
    - DifferentBases: Introduction to different coordinate systems
    - TransformationMatrix: Constructing the change of basis matrix
    - SameVectorDifferentCoords: Same vector, different representations
    - Applications: Practical applications of change of basis
"""

from manimlib import *
import numpy as np


class DifferentBases(Scene):
    """
    Introduce the concept of different bases for the same vector space.
    """

    def construct(self):
        # Title
        title = Text("Change of Basis", font_size=52)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait()

        # Key idea
        key_idea = Text(
            "Same vector, different coordinate systems",
            font_size=36,
            color=YELLOW
        )
        key_idea.next_to(title, DOWN, buff=0.4)
        self.play(Write(key_idea))
        self.wait(2)
        self.play(FadeOut(key_idea))

        # Create coordinate plane with standard basis
        plane1 = NumberPlane(
            x_range=[-3, 3, 1],
            y_range=[-3, 3, 1],
            height=6,
            width=6,
            background_line_style={
                "stroke_color": BLUE_E,
                "stroke_width": 1,
            }
        )
        plane1.shift(LEFT * 3.5)

        # Standard basis vectors
        e1 = Arrow(
            plane1.c2p(0, 0),
            plane1.c2p(1, 0),
            color=GREEN,
            buff=0,
            stroke_width=5
        )
        e2 = Arrow(
            plane1.c2p(0, 0),
            plane1.c2p(0, 1),
            color=RED,
            buff=0,
            stroke_width=5
        )

        e1_label = Tex(R"\vec{e}_1", font_size=32, color=GREEN).next_to(e1, DOWN, buff=0.1)
        e2_label = Tex(R"\vec{e}_2", font_size=32, color=RED).next_to(e2, LEFT, buff=0.1)

        standard_label = Text("Standard Basis", font_size=32, color=BLUE)
        standard_label.next_to(plane1, DOWN, buff=0.4)

        self.play(Create(plane1))
        self.wait(0.5)
        self.play(
            Create(e1),
            Create(e2),
            Write(e1_label),
            Write(e2_label)
        )
        self.wait(0.5)
        self.play(Write(standard_label))
        self.wait()

        # A vector in standard coordinates
        v_standard = Arrow(
            plane1.c2p(0, 0),
            plane1.c2p(2, 1),
            color=YELLOW,
            buff=0,
            stroke_width=6
        )
        v_label1 = Tex(R"\vec{v}", font_size=36, color=YELLOW).next_to(v_standard, UP, buff=0.1)

        v_coords1 = Tex(
            R"\vec{v} = \begin{bmatrix} 2 \\ 1 \end{bmatrix}_{\text{standard}}",
            font_size=32,
            color=YELLOW
        )
        v_coords1.move_to(plane1.get_bottom() + DOWN * 1.2)

        self.play(Create(v_standard), Write(v_label1))
        self.wait(0.5)
        self.play(Write(v_coords1))
        self.wait(2)

        # Alternative basis
        plane2 = NumberPlane(
            x_range=[-3, 3, 1],
            y_range=[-3, 3, 1],
            height=6,
            width=6,
            background_line_style={
                "stroke_color": PURPLE_E,
                "stroke_width": 1,
            }
        )
        plane2.shift(RIGHT * 3.5)

        # Alternative basis vectors
        b1 = Arrow(
            plane2.c2p(0, 0),
            plane2.c2p(1, 1),
            color=GREEN,
            buff=0,
            stroke_width=5
        )
        b2 = Arrow(
            plane2.c2p(0, 0),
            plane2.c2p(-0.5, 1),
            color=RED,
            buff=0,
            stroke_width=5
        )

        b1_label = Tex(R"\vec{b}_1", font_size=32, color=GREEN).next_to(b1, RIGHT, buff=0.1)
        b2_label = Tex(R"\vec{b}_2", font_size=32, color=RED).next_to(b2, UP, buff=0.1)

        alt_label = Text("Alternative Basis", font_size=32, color=PURPLE)
        alt_label.next_to(plane2, DOWN, buff=0.4)

        self.play(Create(plane2))
        self.wait(0.5)
        self.play(
            Create(b1),
            Create(b2),
            Write(b1_label),
            Write(b2_label)
        )
        self.wait(0.5)
        self.play(Write(alt_label))
        self.wait()

        # Same vector in alternative basis
        # v = 2*e1 + 1*e2 = 2*(1,0) + 1*(0,1) = (2,1) in standard
        # Need to find coefficients: v = c1*b1 + c2*b2
        # (2,1) = c1*(1,1) + c2*(-0.5,1)
        # c1 - 0.5*c2 = 2, c1 + c2 = 1  =>  c1 = 2/3, c2 = 1/3  (approximately)
        # Actually: c1 = 10/3, c2 = -7/3 for exact solution
        # Let me recalculate: 2 = c1 - 0.5*c2, 1 = c1 + c2
        # From second: c1 = 1 - c2
        # Substitute: 2 = 1 - c2 - 0.5*c2 = 1 - 1.5*c2  =>  c2 = -2/3, c1 = 5/3

        v_alt = Arrow(
            plane2.c2p(0, 0),
            plane2.c2p(2, 1),
            color=YELLOW,
            buff=0,
            stroke_width=6
        )
        v_label2 = Tex(R"\vec{v}", font_size=36, color=YELLOW).next_to(v_alt, UP, buff=0.1)

        v_coords2 = Tex(
            R"\vec{v} = \begin{bmatrix} 5/3 \\ -2/3 \end{bmatrix}_{\text{alt}}",
            font_size=32,
            color=YELLOW
        )
        v_coords2.move_to(plane2.get_bottom() + DOWN * 1.2)

        self.play(Create(v_alt), Write(v_label2))
        self.wait(0.5)
        self.play(Write(v_coords2))
        self.wait(2)

        # Emphasize: same vector!
        same_vec = Text("Same vector!", font_size=40, color=YELLOW)
        same_vec.move_to(UP * 3.5)
        self.play(Write(same_vec))
        self.wait(2)


class TransformationMatrix(Scene):
    """
    Show how to construct the change of basis matrix.
    """

    def construct(self):
        # Title
        title = Text("Change of Basis Matrix", font_size=52)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait()

        # Setup: two bases
        setup_title = Text("Given two bases:", font_size=36, color=YELLOW)
        setup_title.move_to(2.3 * UP)
        self.play(Write(setup_title))
        self.wait()

        # Standard basis
        standard = Tex(
            R"E = \{\vec{e}_1, \vec{e}_2\} = \left\{\begin{bmatrix} 1 \\ 0 \end{bmatrix}, \begin{bmatrix} 0 \\ 1 \end{bmatrix}\right\}",
            font_size=32
        )
        standard.move_to(UP * 1.3 + LEFT * 0.5)
        self.play(Write(standard))
        self.wait()

        # Alternative basis
        alt = Tex(
            R"B = \{\vec{b}_1, \vec{b}_2\} = \left\{\begin{bmatrix} 1 \\ 1 \end{bmatrix}, \begin{bmatrix} -1 \\ 2 \end{bmatrix}\right\}",
            font_size=32
        )
        alt.next_to(standard, DOWN, buff=0.5)
        self.play(Write(alt))
        self.wait(2)

        # Goal
        goal = Text("Goal: Convert coordinates from basis B to basis E", font_size=32, color=BLUE)
        goal.move_to(DOWN * 0.2)
        self.play(Write(goal))
        self.wait()

        # The key insight
        self.play(FadeOut(goal))

        insight_title = Text("Key Insight:", font_size=32, color=GREEN)
        insight_title.move_to(DOWN * 0.1)
        self.play(Write(insight_title))
        self.wait()

        insight = Text(
            "The columns of P are the basis vectors written in standard coordinates",
            font_size=28,
            color=GREY
        )
        insight.next_to(insight_title, DOWN, buff=0.4)
        self.play(Write(insight))
        self.wait(2)

        # The matrix
        matrix_label = Tex(R"P = ", font_size=40)
        matrix_label.move_to(DOWN * 1.5 + LEFT * 2)

        P_matrix = Matrix(
            [["1", "-1"],
             ["1", "2"]],
            h_buff=1.0
        )
        P_matrix.next_to(matrix_label, RIGHT, buff=0.3)

        col_labels = VGroup(
            Tex(R"\vec{b}_1", font_size=24, color=GREEN),
            Tex(R"\vec{b}_2", font_size=24, color=RED)
        )
        col_labels.arrange(RIGHT, buff=1.5)
        col_labels.next_to(P_matrix, DOWN, buff=0.3)

        self.play(Write(matrix_label), Write(P_matrix))
        self.wait(0.5)
        self.play(Write(col_labels))
        self.wait()

        # Box around matrix
        matrix_box = SurroundingRectangle(
            VGroup(matrix_label, P_matrix),
            color=YELLOW,
            buff=0.2
        )
        self.play(Create(matrix_box))
        self.wait(2)

        # Conversion formula
        self.play(
            FadeOut(insight_title),
            FadeOut(insight),
            FadeOut(col_labels)
        )

        formula_title = Text("Conversion Formula:", font_size=32, color=BLUE)
        formula_title.move_to(DOWN * 0.3 + LEFT * 3.5)
        self.play(Write(formula_title))
        self.wait()

        formula = Tex(
            R"[\vec{v}]_E = P [\vec{v}]_B",
            font_size=40
        )
        formula.next_to(formula_title, DOWN, buff=0.4)
        self.play(Write(formula))
        self.wait()

        explanation = VGroup(
            Tex(R"[\vec{v}]_B \text{: coordinates in basis } B", font_size=26),
            Tex(R"[\vec{v}]_E \text{: coordinates in basis } E", font_size=26)
        )
        explanation.arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        explanation.next_to(formula, DOWN, buff=0.5, aligned_edge=LEFT)
        self.play(Write(explanation))
        self.wait(3)


class SameVectorDifferentCoords(Scene):
    """
    Demonstrate converting a specific vector between bases.
    """

    def construct(self):
        # Title
        title = Text("Same Vector, Different Coordinates", font_size=48)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait()

        # The bases
        bases = VGroup(
            Tex(R"B = \left\{\begin{bmatrix} 1 \\ 1 \end{bmatrix}, \begin{bmatrix} -1 \\ 2 \end{bmatrix}\right\}", font_size=32),
            Tex(R"E = \left\{\begin{bmatrix} 1 \\ 0 \end{bmatrix}, \begin{bmatrix} 0 \\ 1 \end{bmatrix}\right\}", font_size=32)
        )
        bases.arrange(RIGHT, buff=1.5)
        bases.move_to(UP * 2.3)
        self.play(Write(bases))
        self.wait()

        # Vector in B coordinates
        v_B_label = Text("Vector in basis B:", font_size=32, color=BLUE)
        v_B_label.move_to(UP * 1.2 + LEFT * 3.5)

        v_B = Tex(
            R"[\vec{v}]_B = \begin{bmatrix} 2 \\ 3 \end{bmatrix}",
            font_size=36,
            color=BLUE
        )
        v_B.next_to(v_B_label, DOWN, buff=0.4)

        self.play(Write(v_B_label))
        self.wait(0.5)
        self.play(Write(v_B))
        self.wait()

        # Conversion matrix
        P_label = Tex(R"P = ", font_size=36)
        P_label.move_to(UP * 0.5 + LEFT * 3.5)

        P = Matrix(
            [["1", "-1"],
             ["1", "2"]],
            h_buff=0.8
        )
        P.next_to(P_label, RIGHT, buff=0.3)

        self.play(Write(P_label), Write(P))
        self.wait()

        # Computation
        comp_title = Text("Computation:", font_size=32, color=GREEN)
        comp_title.move_to(DOWN * 0.5 + LEFT * 3.5)
        self.play(Write(comp_title))
        self.wait()

        computation = Tex(
            R"""[\vec{v}]_E = P [\vec{v}]_B = \begin{bmatrix} 1 & -1 \\ 1 & 2 \end{bmatrix}
            \begin{bmatrix} 2 \\ 3 \end{bmatrix}""",
            font_size=32
        )
        computation.next_to(comp_title, DOWN, buff=0.4)
        self.play(Write(computation))
        self.wait(2)

        # Calculation steps
        step1 = Tex(
            R"= \begin{bmatrix} 1(2) + (-1)(3) \\ 1(2) + 2(3) \end{bmatrix}",
            font_size=32
        )
        step1.next_to(computation, DOWN, buff=0.4)
        self.play(Write(step1))
        self.wait()

        step2 = Tex(
            R"= \begin{bmatrix} -1 \\ 8 \end{bmatrix}",
            font_size=36,
            color=GREEN
        )
        step2.next_to(step1, DOWN, buff=0.4)
        self.play(Write(step2))
        self.wait()

        # Result
        result_box = SurroundingRectangle(step2, color=YELLOW, buff=0.15)
        self.play(Create(result_box))
        self.wait()

        # Visual representation
        plane = NumberPlane(
            x_range=[-2, 2, 1],
            y_range=[-1, 9, 2],
            height=5,
            width=4,
            background_line_style={
                "stroke_color": BLUE_E,
                "stroke_width": 1,
            }
        )
        plane.shift(RIGHT * 3.5 + DOWN * 0.5)

        # The vector
        vector = Arrow(
            plane.c2p(0, 0),
            plane.c2p(-1, 8),
            color=YELLOW,
            buff=0,
            stroke_width=6
        )

        vec_label = Tex(R"\vec{v} = \begin{bmatrix} -1 \\ 8 \end{bmatrix}", font_size=28, color=YELLOW)
        vec_label.next_to(vector, RIGHT, buff=0.2)

        visual_title = Text("Visual:", font_size=28, color=GREY)
        visual_title.next_to(plane, UP, buff=0.3)

        self.play(Write(visual_title))
        self.play(Create(plane))
        self.wait(0.5)
        self.play(Create(vector), Write(vec_label))
        self.wait(2)

        # Interpretation
        interpretation = Text(
            "v = 2·b₁ + 3·b₂ = -1·e₁ + 8·e₂",
            font_size=28,
            color=GREY
        )
        interpretation.to_edge(DOWN)
        self.play(Write(interpretation))
        self.wait(3)


class Applications(Scene):
    """
    Show practical applications of change of basis.
    """

    def construct(self):
        # Title
        title = Text("Applications of Change of Basis", font_size=52)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait()

        # Application 1: Diagonalization
        app1_title = Text("1. Diagonalization", font_size=40, color=BLUE)
        app1_title.move_to(UP * 2)
        self.play(Write(app1_title))
        self.wait()

        app1_desc = Text(
            "Transform matrix to diagonal form using eigenvector basis",
            font_size=28,
            color=GREY
        )
        app1_desc.next_to(app1_title, DOWN, buff=0.4)
        self.play(Write(app1_desc))
        self.wait()

        # Formula
        diag_formula = Tex(
            R"A = P D P^{-1}",
            font_size=44
        )
        diag_formula.next_to(app1_desc, DOWN, buff=0.5)
        self.play(Write(diag_formula))
        self.wait()

        explanation1 = VGroup(
            Tex(R"A: \text{original matrix}", font_size=28),
            Tex(R"D: \text{diagonal matrix of eigenvalues}", font_size=28),
            Tex(R"P: \text{matrix of eigenvectors}", font_size=28)
        )
        explanation1.arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        explanation1.next_to(diag_formula, DOWN, buff=0.5)
        self.play(LaggedStart(*[Write(ex) for ex in explanation1], lag_ratio=0.3))
        self.wait(3)

        # Application 2: Coordinate transformations
        self.play(
            FadeOut(app1_desc),
            FadeOut(diag_formula),
            FadeOut(explanation1)
        )

        app2_title = Text("2. Coordinate Transformations", font_size=40, color=GREEN)
        app2_title.move_to(UP * 2)
        self.play(ReplacementTransform(app1_title, app2_title))
        self.wait()

        app2_desc = Text(
            "Simplify problems by choosing convenient coordinate systems",
            font_size=28,
            color=GREY
        )
        app2_desc.next_to(app2_title, DOWN, buff=0.4)
        self.play(Write(app2_desc))
        self.wait()

        examples = VGroup(
            Text("• Rotating to align with principal axes", font_size=26),
            Text("• Converting between Cartesian and polar", font_size=26),
            Text("• Simplifying differential equations", font_size=26)
        )
        examples.arrange(DOWN, aligned_edge=LEFT, buff=0.4)
        examples.next_to(app2_desc, DOWN, buff=0.6)
        self.play(LaggedStart(*[Write(ex) for ex in examples], lag_ratio=0.3))
        self.wait(3)

        # Application 3: Computer graphics
        self.play(
            FadeOut(app2_desc),
            FadeOut(examples)
        )

        app3_title = Text("3. Computer Graphics", font_size=40, color=PURPLE)
        app3_title.move_to(UP * 2)
        self.play(ReplacementTransform(app2_title, app3_title))
        self.wait()

        app3_desc = Text(
            "Transforming between world, camera, and screen coordinates",
            font_size=28,
            color=GREY
        )
        app3_desc.next_to(app3_title, DOWN, buff=0.4)
        self.play(Write(app3_desc))
        self.wait()

        graphics_ex = VGroup(
            Text("• World coordinates → Camera coordinates", font_size=26),
            Text("• Camera coordinates → Screen coordinates", font_size=26),
            Text("• Each transformation uses change of basis", font_size=26)
        )
        graphics_ex.arrange(DOWN, aligned_edge=LEFT, buff=0.4)
        graphics_ex.next_to(app3_desc, DOWN, buff=0.6)
        self.play(LaggedStart(*[Write(ex) for ex in graphics_ex], lag_ratio=0.3))
        self.wait(3)

        # Key takeaway
        self.play(
            FadeOut(app3_title),
            FadeOut(app3_desc),
            FadeOut(graphics_ex)
        )

        takeaway = Text(
            "Change of basis is fundamental to linear algebra!",
            font_size=40,
            color=YELLOW
        )
        takeaway.move_to(UP * 0.5)
        self.play(Write(takeaway))
        self.wait()

        points = VGroup(
            Text("✓ Same vector, different representations", font_size=32),
            Text("✓ Choose basis that simplifies the problem", font_size=32),
            Text("✓ Essential for eigenvalues, graphics, physics", font_size=32)
        )
        points.arrange(DOWN, aligned_edge=LEFT, buff=0.5)
        points.next_to(takeaway, DOWN, buff=0.8)
        self.play(LaggedStart(*[Write(pt) for pt in points], lag_ratio=0.4))
        self.wait(3)


# Utility functions for change of basis

def construct_change_of_basis_matrix(new_basis_vectors):
    """
    Construct change of basis matrix from new basis vectors.

    Args:
        new_basis_vectors: List of basis vectors as columns

    Returns:
        Change of basis matrix P (columns are the new basis vectors)
    """
    return np.column_stack(new_basis_vectors)


def convert_coordinates(vector, change_matrix):
    """
    Convert vector coordinates using change of basis matrix.

    Args:
        vector: Vector in new basis coordinates
        change_matrix: Change of basis matrix P

    Returns:
        Vector in standard basis coordinates
    """
    return change_matrix @ vector


def inverse_change_of_basis(change_matrix):
    """
    Compute inverse change of basis matrix.

    Args:
        change_matrix: Change of basis matrix P

    Returns:
        Inverse matrix P^(-1) for converting back
    """
    return np.linalg.inv(change_matrix)


def is_valid_basis(vectors, tolerance=1e-10):
    """
    Check if a set of vectors forms a valid basis.

    Args:
        vectors: List of vectors
        tolerance: Numerical tolerance for linear independence check

    Returns:
        True if vectors are linearly independent (form a basis)
    """
    matrix = np.column_stack(vectors)
    return abs(np.linalg.det(matrix)) > tolerance


def change_basis_for_matrix(matrix, P):
    """
    Change the basis for a linear transformation matrix.

    Args:
        matrix: Original matrix A in standard basis
        P: Change of basis matrix

    Returns:
        Matrix A' in new basis: A' = P^(-1) A P
    """
    P_inv = np.linalg.inv(P)
    return P_inv @ matrix @ P


def orthonormalize_basis(vectors):
    """
    Apply Gram-Schmidt to create an orthonormal basis.

    Args:
        vectors: List of linearly independent vectors

    Returns:
        List of orthonormal vectors spanning the same space
    """
    orthonormal = []

    for v in vectors:
        # Subtract projections onto previous vectors
        u = v.copy()
        for e in orthonormal:
            u = u - np.dot(v, e) * e

        # Normalize
        norm = np.linalg.norm(u)
        if norm > 1e-10:
            orthonormal.append(u / norm)

    return orthonormal
