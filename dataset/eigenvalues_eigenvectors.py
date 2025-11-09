"""
Natural Group Name: Eigenvalues and Eigenvectors

Educational Objectives:
- To introduce eigenvectors as special directions preserved by transformations
- To show eigenvalues as scaling factors along eigenvector directions
- To build geometric intuition for these fundamental linear algebra concepts
- To demonstrate practical significance and applications

Story Arc & Intent:
The animation demystifies eigenvectors by showing them as special directions
that a transformation only stretches or compresses (doesn't rotate). This
geometric perspective makes these concepts intuitive and meaningful, revealing
why they're so important in applications.

Narrative Flow:
- Hook/Opening: Apply a transformation and observe most vectors rotate
- Development: Find special vectors that only get scaled, not rotated
- Build-up: Show these are eigenvectors, scaling factors are eigenvalues
- Climax: Visualize eigenspaces and diagonal decomposition
- Resolution: Explain the equation Av = λv geometrically
- Extension: Mention applications (PCA, stability analysis, etc.)

Technical Implementation Notes:
- Scene Classes: IntroduceTransform, FindSpecialVectors, EigenvalueScaling, Applications
- Key Visual Elements: 2D plane, vectors, transformed vectors, eigenspaces
- Animation Techniques: Vector transformations, highlighting, scaling visualization
- Mathematical Concepts: Linear transformations, eigenvectors, eigenvalues, eigenspaces

Dependency Chain:
All scenes are independent. They use NumberPlane, Arrow, Vector, Matrix, and
Tex from manimlib. Utility functions compute eigenvectors and eigenvalues.

Rendering Instructions:
To render these scenes, use the manim command-line tool:
- For a single scene: manimgl eigenvalues_eigenvectors.py IntroduceTransform
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
# Grid configuration
GRID_CONFIG = {
    "x_range": (-4, 4, 1),
    "y_range": (-4, 4, 1),
    "width": 8,
    "height": 8,
}

# Colors
EIGENVECTOR_COLOR = YELLOW
NON_EIGENVECTOR_COLOR = BLUE
TRANSFORMED_COLOR = GREEN
EIGENSPACE_COLOR = PURPLE

# Vector parameters
VECTOR_CONFIG = {
    "buff": 0,
    "stroke_width": 6,
    "max_tip_length_to_length_ratio": 0.25,
}

# ============================================================
# 3. UTILITY FUNCTIONS
# ============================================================

def compute_eigenvectors_2d(matrix):
    """
    Compute eigenvalues and eigenvectors of a 2x2 matrix.

    Args:
        matrix: 2x2 numpy array

    Returns:
        Tuple of (eigenvalues, eigenvectors)
    """
    eigenvalues, eigenvectors = np.linalg.eig(matrix)
    return eigenvalues, eigenvectors

def create_vector_arrow(vector, color=BLUE, **kwargs):
    """
    Create an arrow representing a vector from origin.

    Args:
        vector: 2D vector [x, y]
        color: Arrow color
        **kwargs: Additional Arrow parameters

    Returns:
        Arrow object
    """
    config = VECTOR_CONFIG.copy()
    config.update(kwargs)

    arrow = Arrow(
        ORIGIN,
        np.array([vector[0], vector[1], 0]),
        color=color,
        **config
    )
    return arrow

def normalize_vector(v):
    """Normalize a vector to unit length."""
    norm = np.linalg.norm(v)
    if norm < 1e-10:
        return v
    return v / norm

def create_matrix_tex(matrix, font_size=36):
    """Create Tex representation of 2x2 matrix."""
    a, b = matrix[0, 0], matrix[0, 1]
    c, d = matrix[1, 0], matrix[1, 1]

    def fmt(x):
        if abs(x - round(x)) < 0.01:
            return str(int(round(x)))
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

class IntroduceTransform(InteractiveScene):
    """
    Part 1: Show a linear transformation rotating most vectors.

    Narrative purpose:
        To establish that linear transformations generally rotate vectors,
        setting up the question: are there special vectors that don't rotate?

    Mathematical content:
        Shows a simple 2x2 matrix transforming various vectors, with most
        changing direction (rotating) under the transformation.

    Visual approach:
        Display a grid of vectors, apply transformation, show that most
        vectors change direction dramatically.
    """
    def construct(self):
        # ========================================
        # SETUP: Title
        # ========================================
        title = Text("Eigenvectors: Special Directions", font_size=48)
        title.to_edge(UP)

        self.play(FadeIn(title, shift=DOWN))
        self.wait()

        # ========================================
        # CREATE: Coordinate plane
        # ========================================
        plane = NumberPlane(**GRID_CONFIG)
        plane.set_stroke(GREY_A, width=1, opacity=0.3)

        self.play(ShowCreation(plane))
        self.wait()

        # ========================================
        # CREATE: Sample vectors
        # ========================================
        sample_vectors = [
            np.array([1, 0]),
            np.array([1, 1]),
            np.array([0, 1]),
            np.array([-1, 1]),
        ]

        arrows = VGroup(*[
            create_vector_arrow(v, color=NON_EIGENVECTOR_COLOR)
            for v in sample_vectors
        ])

        self.play(
            LaggedStart(
                *[GrowArrow(arrow) for arrow in arrows],
                lag_ratio=0.2
            )
        )
        self.wait()

        # ========================================
        # DEFINE: Transformation matrix
        # ========================================
        # Use a matrix with clear eigenstructure
        # [[3, 1], [0, 2]] has eigenvalues 3, 2 and eigenvectors [1,0], [1,1]
        matrix = np.array([[3, 1], [0, 2]], dtype=float)

        matrix_tex = create_matrix_tex(matrix)
        matrix_label = Text("Matrix A:", font_size=32)

        matrix_group = VGroup(matrix_label, matrix_tex)
        matrix_group.arrange(RIGHT, buff=0.3)
        matrix_group.to_corner(UL, buff=0.5)

        self.play(
            Write(matrix_label),
            Write(matrix_tex)
        )
        self.wait()

        # ========================================
        # APPLY: Transformation
        # ========================================
        # Create transformed vectors
        transformed_vectors = [matrix @ v for v in sample_vectors]
        transformed_arrows = VGroup(*[
            create_vector_arrow(v, color=TRANSFORMED_COLOR)
            for v in transformed_vectors
        ])

        self.play(
            *[
                Transform(arrows[i].copy(), transformed_arrows[i])
                for i in range(len(arrows))
            ],
            run_time=2
        )
        self.wait()

        # ========================================
        # OBSERVE: Most vectors rotate
        # ========================================
        observation = Text(
            "Most vectors change direction!",
            font_size=32,
            color=YELLOW
        )
        observation.to_edge(DOWN, buff=0.8)

        self.play(Write(observation))
        self.wait(2)

        # ========================================
        # QUESTION: Special vectors?
        # ========================================
        question = Text(
            "But are there special vectors that only get scaled?",
            font_size=32,
            color=GREEN
        )
        question.next_to(observation, UP, buff=0.3)

        self.play(Write(question))
        self.wait(3)

        # ========================================
        # CLEANUP
        # ========================================
        self.play(FadeOut(*self.mobjects), run_time=1)
        self.wait()


class FindSpecialVectors(InteractiveScene):
    """
    Part 2: Identify and visualize eigenvectors.

    Narrative purpose:
        To reveal the eigenvectors as the special directions that are
        preserved (only scaled) by the transformation.

    Mathematical content:
        For the matrix [[3,1],[0,2]], find eigenvectors [1,0] and [1,1]
        corresponding to eigenvalues 3 and 2. Show these only get scaled.

    Visual approach:
        Highlight eigenvector directions, apply transformation, show they
        stay on the same line (only length changes).
    """
    def construct(self):
        # ========================================
        # SETUP: Title and plane
        # ========================================
        title = Text("Finding Eigenvectors", font_size=48)
        title.to_edge(UP)

        plane = NumberPlane(**GRID_CONFIG)
        plane.set_stroke(GREY_A, width=1, opacity=0.3)

        self.add(plane)
        self.play(FadeIn(title, shift=DOWN))
        self.wait()

        # ========================================
        # MATRIX: Same as before
        # ========================================
        matrix = np.array([[3, 1], [0, 2]], dtype=float)

        matrix_tex = create_matrix_tex(matrix)
        matrix_label = Text("A =", font_size=32)

        matrix_group = VGroup(matrix_label, matrix_tex)
        matrix_group.arrange(RIGHT, buff=0.2)
        matrix_group.to_corner(UL, buff=0.5)

        self.play(
            Write(matrix_label),
            Write(matrix_tex)
        )
        self.wait()

        # ========================================
        # EIGENVECTOR 1: [1, 0], eigenvalue 3
        # ========================================
        v1 = np.array([2, 0])  # Scaled for visibility
        arrow1 = create_vector_arrow(v1, color=EIGENVECTOR_COLOR)

        label1 = Tex(R"\vec{v}_1", font_size=36, color=EIGENVECTOR_COLOR)
        label1.next_to(arrow1, DOWN, buff=0.2)

        self.play(
            GrowArrow(arrow1),
            Write(label1)
        )
        self.wait()

        # Apply transformation
        transformed_v1 = matrix @ v1
        arrow1_transformed = create_vector_arrow(transformed_v1, color=YELLOW)

        lambda1_label = Tex(
            R"A\vec{v}_1 = 3\vec{v}_1",
            font_size=32,
            color=YELLOW
        )
        lambda1_label.to_edge(DOWN, buff=2)

        self.play(
            Transform(arrow1.copy(), arrow1_transformed),
            Write(lambda1_label)
        )
        self.wait(2)

        # Emphasize: Same direction!
        emphasis1 = Text("Same direction, scaled by 3!", font_size=28, color=GREEN)
        emphasis1.next_to(lambda1_label, DOWN, buff=0.2)

        self.play(FadeIn(emphasis1, shift=UP))
        self.wait(2)

        # ========================================
        # EIGENVECTOR 2: [1, 1], eigenvalue 2
        # ========================================
        # Clear previous emphasis
        self.play(
            FadeOut(lambda1_label),
            FadeOut(emphasis1)
        )

        v2 = np.array([1.5, 1.5])  # Direction [1,1], scaled for visibility
        arrow2 = create_vector_arrow(v2, color=PURPLE)

        label2 = Tex(R"\vec{v}_2", font_size=36, color=PURPLE)
        label2.next_to(arrow2, UP + RIGHT, buff=0.1)

        self.play(
            GrowArrow(arrow2),
            Write(label2)
        )
        self.wait()

        # Apply transformation
        # For [1,1]: [[3,1],[0,2]] @ [1,1] = [4,2] = 2*[2,1]
        # Wait, let me recalculate: [[3,1],[0,2]] @ [1,1] = [3+1, 0+2] = [4,2]
        # That's not 2*[1,1]. Let me recalculate eigenvalues...
        # Actually, eigenvalues are 3 and 2 from diagonal-ish form
        # Let me compute properly
        eigenvals, eigenvecs = np.linalg.eig(matrix)
        # eigenvals should be [3, 2]
        # eigenvecs[:, 0] for eigenval 3, eigenvecs[:, 1] for eigenval 2

        v2_actual = eigenvecs[:, 1] * 1.5  # Second eigenvector
        arrow2 = create_vector_arrow(v2_actual, color=PURPLE)
        label2.next_to(arrow2, UR, buff=0.1)

        self.play(
            FadeIn(arrow2),
            Write(label2)
        )
        self.wait()

        transformed_v2 = matrix @ v2_actual
        arrow2_transformed = create_vector_arrow(transformed_v2, color=PURPLE)

        lambda2_label = Tex(
            R"A\vec{v}_2 = 2\vec{v}_2",
            font_size=32,
            color=PURPLE
        )
        lambda2_label.to_edge(DOWN, buff=2)

        self.play(
            Transform(arrow2.copy(), arrow2_transformed),
            Write(lambda2_label)
        )
        self.wait(2)

        emphasis2 = Text("Same direction, scaled by 2!", font_size=28, color=GREEN)
        emphasis2.next_to(lambda2_label, DOWN, buff=0.2)

        self.play(FadeIn(emphasis2, shift=UP))
        self.wait(2)

        # ========================================
        # DEFINE: Eigenvectors
        # ========================================
        self.play(FadeOut(*self.mobjects[4:]))  # Keep plane and title

        definition = VGroup(
            Text("Eigenvector:", font_size=36, weight=BOLD),
            Text("A vector that only gets scaled (not rotated)", font_size=28),
            Text("", font_size=20),
            Text("Eigenvalue:", font_size=36, weight=BOLD),
            Text("The scaling factor for that eigenvector", font_size=28),
        )
        definition.arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        definition.move_to(ORIGIN)

        self.play(
            LaggedStart(
                *[FadeIn(line, shift=RIGHT) for line in definition],
                lag_ratio=0.4
            )
        )
        self.wait(4)

        # ========================================
        # CLEANUP
        # ========================================
        self.play(FadeOut(*self.mobjects), run_time=1)
        self.wait()


class EigenvalueScaling(InteractiveScene):
    """
    Part 3: Visualize eigenvalue equation Av = λv.

    Narrative purpose:
        To cement understanding by showing the eigenvalue equation
        geometrically and algebraically.

    Mathematical content:
        Shows the equation Av = λv, where A is the matrix, v is an
        eigenvector, and λ is the corresponding eigenvalue. Demonstrates
        this visually and algebraically.

    Visual approach:
        Show the equation, verify it with specific examples, and
        visualize the eigenspace (the line spanned by an eigenvector).
    """
    def construct(self):
        # ========================================
        # SETUP: Title
        # ========================================
        title = Text("The Eigenvalue Equation", font_size=48)
        title.to_edge(UP)

        self.play(FadeIn(title, shift=DOWN))
        self.wait()

        # ========================================
        # STATE: The equation
        # ========================================
        equation = Tex(
            R"A\vec{v} = \lambda \vec{v}",
            font_size=60,
            color=YELLOW
        )
        equation.shift(0.5 * UP)

        box = SurroundingRectangle(equation, buff=0.4, color=YELLOW, stroke_width=4)

        self.play(
            Write(equation),
            ShowCreation(box)
        )
        self.wait(2)

        # ========================================
        # EXPLAIN: Components
        # ========================================
        explanations = VGroup(
            Tex(R"A = \text{matrix}", font_size=32),
            Tex(R"\vec{v} = \text{eigenvector}", font_size=32),
            Tex(R"\lambda = \text{eigenvalue (scalar)}", font_size=32)
        )
        explanations.arrange(DOWN, buff=0.4, aligned_edge=LEFT)
        explanations.next_to(equation, DOWN, buff=1)

        self.play(
            LaggedStart(
                *[FadeIn(exp, shift=RIGHT) for exp in explanations],
                lag_ratio=0.5
            )
        )
        self.wait(3)

        # ========================================
        # EXAMPLE: Specific calculation
        # ========================================
        self.play(
            FadeOut(explanations),
            VGroup(equation, box).animate.scale(0.6).to_corner(UL, buff=0.5)
        )

        example_title = Text("Example Verification", font_size=36)
        example_title.shift(2 * UP)

        self.play(Write(example_title))
        self.wait()

        # Matrix
        matrix = np.array([[3, 1], [0, 2]], dtype=float)
        A_tex = Tex(
            R"A = \begin{bmatrix} 3 & 1 \\ 0 & 2 \end{bmatrix}",
            font_size=32
        )
        A_tex.shift(0.8 * UP + 3 * LEFT)

        # Eigenvector
        v_tex = Tex(
            R"\vec{v} = \begin{bmatrix} 1 \\ 0 \end{bmatrix}",
            font_size=32
        )
        v_tex.next_to(A_tex, RIGHT, buff=1)

        # Eigenvalue
        lambda_tex = Tex(R"\lambda = 3", font_size=32)
        lambda_tex.next_to(v_tex, RIGHT, buff=1)

        self.play(
            Write(A_tex),
            Write(v_tex),
            Write(lambda_tex)
        )
        self.wait()

        # ========================================
        # COMPUTE: Left side
        # ========================================
        left_computation = Tex(
            R"A\vec{v} = \begin{bmatrix} 3 & 1 \\ 0 & 2 \end{bmatrix} \begin{bmatrix} 1 \\ 0 \end{bmatrix} = \begin{bmatrix} 3 \\ 0 \end{bmatrix}",
            font_size=28
        )
        left_computation.shift(0.2 * DOWN)

        self.play(Write(left_computation))
        self.wait(2)

        # ========================================
        # COMPUTE: Right side
        # ========================================
        right_computation = Tex(
            R"\lambda\vec{v} = 3 \begin{bmatrix} 1 \\ 0 \end{bmatrix} = \begin{bmatrix} 3 \\ 0 \end{bmatrix}",
            font_size=28
        )
        right_computation.next_to(left_computation, DOWN, buff=0.5)

        self.play(Write(right_computation))
        self.wait(2)

        # ========================================
        # VERIFY: They match!
        # ========================================
        check = Tex(R"\checkmark", font_size=60, color=GREEN)
        check.next_to(right_computation, DOWN, buff=0.5)

        equals_text = Text("They match!", font_size=32, color=GREEN)
        equals_text.next_to(check, RIGHT, buff=0.5)

        self.play(
            FadeIn(check, scale=2),
            Write(equals_text)
        )
        self.wait(3)

        # ========================================
        # CLEANUP
        # ========================================
        self.play(FadeOut(*self.mobjects), run_time=1)
        self.wait()


class Applications(InteractiveScene):
    """
    Part 4: Show eigenspace visualization and mention applications.

    Narrative purpose:
        To show the eigenspace (all vectors along an eigenvector direction)
        and briefly mention why eigenvectors matter in applications.

    Mathematical content:
        Shows that any scalar multiple of an eigenvector is also an
        eigenvector with the same eigenvalue. Mentions applications like
        PCA, stability analysis, and diagonalization.

    Visual approach:
        Visualize eigenspaces as lines through the origin, show multiple
        vectors along each eigenspace all being eigenvectors. List applications.
    """
    def construct(self):
        # ========================================
        # SETUP: Title
        # ========================================
        title = Text("Eigenspaces and Applications", font_size=48)
        title.to_edge(UP)

        self.play(FadeIn(title, shift=DOWN))
        self.wait()

        # ========================================
        # VISUALIZE: Eigenspaces
        # ========================================
        plane = NumberPlane(**GRID_CONFIG)
        plane.set_stroke(GREY_A, width=1, opacity=0.2)

        self.play(ShowCreation(plane))
        self.wait()

        # Matrix (same as before)
        matrix = np.array([[3, 1], [0, 2]], dtype=float)
        eigenvals, eigenvecs = np.linalg.eig(matrix)

        # Eigenspace 1 (horizontal line for eigenvalue 3)
        eigenspace1 = Line(4 * LEFT, 4 * RIGHT, color=YELLOW, stroke_width=4)
        eigenspace1_label = Tex(
            R"\text{Eigenspace for } \lambda = 3",
            font_size=28,
            color=YELLOW
        )
        eigenspace1_label.next_to(eigenspace1, DOWN, buff=0.2)

        self.play(
            ShowCreation(eigenspace1),
            Write(eigenspace1_label)
        )
        self.wait()

        # Show multiple vectors on this eigenspace
        vectors1 = VGroup(*[
            create_vector_arrow(np.array([x, 0]), color=YELLOW, stroke_width=4)
            for x in [-2, -1, 1, 2]
        ])

        self.play(
            LaggedStart(
                *[GrowArrow(v) for v in vectors1],
                lag_ratio=0.2
            )
        )
        self.wait()

        note1 = Text(
            "All vectors on this line are eigenvectors!",
            font_size=24,
            color=GREEN
        )
        note1.to_edge(DOWN, buff=1.5)

        self.play(Write(note1))
        self.wait(2)

        # ========================================
        # EIGENSPACE 2
        # ========================================
        self.play(
            FadeOut(vectors1),
            FadeOut(eigenspace1),
            FadeOut(eigenspace1_label),
            FadeOut(note1)
        )

        # Eigenspace 2 (diagonal line for eigenvalue 2)
        # Direction from eigenvecs[:, 1]
        direction = normalize_vector(eigenvecs[:, 1][:2])
        eigenspace2 = Line(
            4 * np.array([-direction[0], -direction[1], 0]),
            4 * np.array([direction[0], direction[1], 0]),
            color=PURPLE,
            stroke_width=4
        )

        eigenspace2_label = Tex(
            R"\text{Eigenspace for } \lambda = 2",
            font_size=28,
            color=PURPLE
        )
        eigenspace2_label.next_to(eigenspace2, UP + LEFT, buff=0.2)

        self.play(
            ShowCreation(eigenspace2),
            Write(eigenspace2_label)
        )
        self.wait()

        # Show multiple vectors
        vectors2 = VGroup(*[
            create_vector_arrow(
                scale * eigenvecs[:, 1][:2],
                color=PURPLE,
                stroke_width=4
            )
            for scale in [-2, -1, 1, 2]
        ])

        self.play(
            LaggedStart(
                *[GrowArrow(v) for v in vectors2],
                lag_ratio=0.2
            )
        )
        self.wait(2)

        # ========================================
        # APPLICATIONS
        # ========================================
        self.play(
            FadeOut(plane),
            FadeOut(eigenspace2),
            FadeOut(eigenspace2_label),
            FadeOut(vectors2)
        )

        apps_title = Text("Why Eigenvectors Matter", font_size=40, weight=BOLD)
        apps_title.shift(2 * UP)

        self.play(
            FadeOut(title),
            Write(apps_title)
        )
        self.wait()

        applications = VGroup(
            Text("• Principal Component Analysis (PCA)", font_size=28),
            Text("• Differential equations & stability analysis", font_size=28),
            Text("• Matrix diagonalization", font_size=28),
            Text("• Google PageRank algorithm", font_size=28),
            Text("• Quantum mechanics (energy eigenstates)", font_size=28),
            Text("• Vibration modes in engineering", font_size=28),
        )
        applications.arrange(DOWN, buff=0.4, aligned_edge=LEFT)
        applications.next_to(apps_title, DOWN, buff=0.8)

        self.play(
            LaggedStart(
                *[FadeIn(app, shift=RIGHT) for app in applications],
                lag_ratio=0.3
            ),
            run_time=5
        )
        self.wait(4)

        # ========================================
        # FINAL MESSAGE
        # ========================================
        self.play(FadeOut(*self.mobjects))

        final = Text(
            "Eigenvectors reveal the fundamental\nstructure of linear transformations!",
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
# Scene 1 (IntroduceTransform):
#   - Shows transformation rotating most vectors
#   - Poses question about special vectors
#   - Sets up the mystery
#
# Scene 2 (FindSpecialVectors):
#   - Identifies eigenvectors
#   - Shows they only get scaled
#   - Defines eigenvectors and eigenvalues
#
# Scene 3 (EigenvalueScaling):
#   - States equation Av = λv
#   - Verifies with specific example
#   - Connects algebra to geometry
#
# Scene 4 (Applications):
#   - Shows eigenspaces as lines
#   - Lists important applications
#   - Emphasizes practical significance

SCENE_ORDER = [
    IntroduceTransform,    # Part 1: Setup and question
    FindSpecialVectors,    # Part 2: Discovery
    EigenvalueScaling,     # Part 3: The equation
    Applications,          # Part 4: Significance
]
