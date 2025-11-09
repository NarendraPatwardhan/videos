"""
Natural Group Name: Dot Product as Projection

Educational Objectives:
- To visualize the dot product as a geometric projection operation
- To demonstrate the relationship between dot product and the angle between vectors
- To build intuition for the formula a·b = |a||b|cos(θ)
- To show practical applications in physics and computer science

Story Arc & Intent:
The animation reveals the dot product through geometric projection: one vector
projected onto another. This transforms the abstract algebraic formula into an
intuitive visual process that connects geometry and algebra.

Narrative Flow:
- Hook/Opening: Two vectors in space and the question of their "alignment"
- Development: Project one vector onto another, measure the projection length
- Build-up: Show how the angle affects the projection length
- Climax: The formula a·b = |a||b|cos(θ) emerges from the geometry
- Resolution: Applications to work, orthogonality testing, and similarity

Technical Implementation Notes:
- Scene Classes: IntroduceVectors, GeometricInterpretation, ProjectionFormula, Applications
- Key Visual Elements: Vectors, projections, angles, coordinate grids
- Animation Techniques: Vector drawing, projection lines, angle arcs
- Mathematical Concepts: Dot product, projection, orthogonality, vector components

Dependency Chain:
All scenes use basic manimlib components: Arrow, Line, Dot, Text, Tex, NumberPlane.
No custom utilities required beyond helper functions defined in this file.

Rendering Instructions:
To render these scenes, use the manim command-line tool:
- For a single scene: manimgl dot_product.py IntroduceVectors
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
# - BLUE: First vector (a)
# - YELLOW: Second vector (b)
# - GREEN: Projection result
# - RED: Important points and angles
# - WHITE: Axes and grid
# - GREY_A: De-emphasized elements
#
# Key Manim Constants Used:
# - UP, DOWN, LEFT, RIGHT: Direction vectors
# - ORIGIN: Center point
# - PI: π for angle calculations
# - MED_SMALL_BUFF: Spacing

# Vector configuration
VECTOR_CONFIG = {
    "buff": 0,
    "stroke_width": 5,
    "tip_length": 0.25,
}

# ============================================================
# 3. UTILITY FUNCTIONS
# ============================================================

def create_vector_arrow(start, end, color=BLUE, **kwargs):
    """
    Create a vector arrow from start to end.

    Args:
        start: Starting point (numpy array or list)
        end: Ending point (numpy array or list)
        color: Color of the arrow
        **kwargs: Additional arguments for Arrow

    Returns:
        Arrow mobject
    """
    config = VECTOR_CONFIG.copy()
    config.update(kwargs)
    return Arrow(start, end, color=color, **config)

def get_projection_point(vector_start, vector_end, point_to_project):
    """
    Get the projection of a point onto a line defined by a vector.

    Args:
        vector_start: Start of the vector line
        vector_end: End of the vector line
        point_to_project: Point to project onto the line

    Returns:
        Projected point as numpy array
    """
    # Vector direction
    v = np.array(vector_end) - np.array(vector_start)
    # Point relative to start
    p = np.array(point_to_project) - np.array(vector_start)

    # Projection formula: proj_v(p) = (p·v / v·v) * v
    if np.dot(v, v) == 0:
        return np.array(vector_start)

    projection_scalar = np.dot(p, v) / np.dot(v, v)
    projection = np.array(vector_start) + projection_scalar * v

    return projection

def create_projection_line(start, end, color=GREEN, **kwargs):
    """
    Create a dashed line for projection visualization.

    Args:
        start: Starting point
        end: Ending point
        color: Color of the line
        **kwargs: Additional arguments for Line

    Returns:
        DashedLine mobject
    """
    return DashedLine(start, end, color=color, stroke_width=2, **kwargs)

def get_angle_between_vectors(v1, v2):
    """
    Calculate the angle between two vectors in radians.

    Args:
        v1: First vector (numpy array)
        v2: Second vector (numpy array)

    Returns:
        Angle in radians
    """
    # Handle 2D vectors by padding with 0
    v1 = np.array(v1)
    v2 = np.array(v2)

    # Take only first 2 components for 2D
    v1_2d = v1[:2] if len(v1) >= 2 else v1
    v2_2d = v2[:2] if len(v2) >= 2 else v2

    cos_angle = np.dot(v1_2d, v2_2d) / (np.linalg.norm(v1_2d) * np.linalg.norm(v2_2d))
    # Clamp to [-1, 1] to avoid numerical errors
    cos_angle = np.clip(cos_angle, -1, 1)

    return np.arccos(cos_angle)

def create_angle_arc(center, radius, start_angle, end_angle, color=RED, **kwargs):
    """
    Create an arc to show an angle.

    Args:
        center: Center point of the arc
        radius: Radius of the arc
        start_angle: Starting angle in radians
        end_angle: Ending angle in radians
        color: Color of the arc
        **kwargs: Additional arguments for Arc

    Returns:
        Arc mobject
    """
    return Arc(
        radius=radius,
        start_angle=start_angle,
        angle=end_angle - start_angle,
        color=color,
        stroke_width=2,
        **kwargs
    ).shift(center)

# ============================================================
# 4. SCENE CLASSES
# ============================================================

class IntroduceVectors(Scene):
    """
    Scene 1: Introduce two vectors and pose the question of their relationship.

    This scene introduces two vectors in 2D space and raises the question:
    how can we measure how much these vectors "align" or "point in the same direction"?
    """

    def construct(self):
        # ========================================
        # SETUP: Create coordinate plane
        # ========================================
        plane = NumberPlane(
            x_range=[-6, 6, 1],
            y_range=[-4, 4, 1],
            background_line_style={
                "stroke_color": GREY_A,
                "stroke_width": 1,
            }
        )
        plane.set_opacity(0.3)

        self.play(ShowCreation(plane))
        self.wait()

        # ========================================
        # INTRODUCE: First vector
        # ========================================
        title = Text("The Dot Product", font_size=48)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait()

        # Create first vector
        vector_a = create_vector_arrow(ORIGIN, np.array([3, 2, 0]), color=BLUE)
        label_a = Tex("\\vec{a}", color=BLUE, font_size=36)
        label_a.next_to(vector_a.get_end(), UP)

        self.play(GrowArrow(vector_a))
        self.play(Write(label_a))
        self.wait()

        # ========================================
        # INTRODUCE: Second vector
        # ========================================
        vector_b = create_vector_arrow(ORIGIN, np.array([2, -1, 0]), color=YELLOW)
        label_b = Tex("\\vec{b}", color=YELLOW, font_size=36)
        label_b.next_to(vector_b.get_end(), DOWN)

        self.play(GrowArrow(vector_b))
        self.play(Write(label_b))
        self.wait()

        # ========================================
        # QUESTION: How aligned are they?
        # ========================================
        question = Text(
            "How much do these vectors 'align'?",
            font_size=36,
            color=WHITE
        )
        question.to_edge(DOWN)

        self.play(FadeIn(question, shift=UP))
        self.wait()

        # Show angle between vectors
        angle_arc = create_angle_arc(
            ORIGIN,
            radius=0.8,
            start_angle=np.arctan2(2, 3),
            end_angle=np.arctan2(-1, 2),
            color=RED
        )
        theta_label = Tex("\\theta", color=RED, font_size=32)
        theta_label.move_to(ORIGIN + 1.3 * np.array([np.cos(-0.2), np.sin(-0.2), 0]))

        self.play(ShowCreation(angle_arc))
        self.play(Write(theta_label))
        self.wait()

        # ========================================
        # ALGEBRAIC FORMULA
        # ========================================
        self.play(FadeOut(question))

        formula = Tex(
            "\\vec{a} \\cdot \\vec{b} = a_x b_x + a_y b_y",
            font_size=36
        )
        formula.to_edge(DOWN).shift(UP * 0.5)

        self.play(Write(formula))
        self.wait()

        # Show component values
        components = Tex(
            "= (3)(2) + (2)(-1) = 4",
            font_size=36,
            color=GREEN
        )
        components.next_to(formula, DOWN)

        self.play(Write(components))
        self.wait(2)


class GeometricInterpretation(Scene):
    """
    Scene 2: Show the geometric interpretation through projection.

    This scene visualizes the dot product as the length of one vector's
    projection onto another, multiplied by the length of that other vector.
    """

    def construct(self):
        # ========================================
        # SETUP: Recreate vectors from Scene 1
        # ========================================
        plane = NumberPlane(
            x_range=[-6, 6, 1],
            y_range=[-4, 4, 1],
            background_line_style={
                "stroke_color": GREY_A,
                "stroke_width": 1,
            }
        )
        plane.set_opacity(0.3)

        title = Text("Geometric Interpretation", font_size=42)
        title.to_edge(UP)

        vector_a = create_vector_arrow(ORIGIN, np.array([3, 2, 0]), color=BLUE)
        label_a = Tex("\\vec{a}", color=BLUE, font_size=36)
        label_a.next_to(vector_a.get_end(), UP)

        vector_b = create_vector_arrow(ORIGIN, np.array([2, -1, 0]), color=YELLOW)
        label_b = Tex("\\vec{b}", color=YELLOW, font_size=36)
        label_b.next_to(vector_b.get_end(), DOWN)

        self.add(plane, title, vector_a, label_a, vector_b, label_b)
        self.wait()

        # ========================================
        # PROJECTION: Project b onto a
        # ========================================
        explanation = Text(
            "Project b onto a",
            font_size=32,
            color=GREEN
        )
        explanation.to_edge(DOWN).shift(UP * 0.5)

        self.play(Write(explanation))
        self.wait()

        # Calculate projection point
        a_end = np.array([3, 2, 0])
        b_end = np.array([2, -1, 0])
        proj_point = get_projection_point(ORIGIN, a_end, b_end)

        # Draw projection line (perpendicular from b to a)
        proj_line = create_projection_line(b_end, proj_point, color=GREY_A)
        self.play(ShowCreation(proj_line))
        self.wait()

        # Show projection point
        proj_dot = Dot(proj_point, color=GREEN)
        self.play(FadeIn(proj_dot, scale=0.5))
        self.wait()

        # ========================================
        # PROJECTION VECTOR
        # ========================================
        projection_vector = create_vector_arrow(ORIGIN, proj_point, color=GREEN)
        proj_label = Tex("\\text{proj}_{\\vec{a}}\\vec{b}", color=GREEN, font_size=32)
        proj_label.next_to(proj_point, DOWN, buff=0.3)

        self.play(
            ReplacementTransform(proj_dot, projection_vector),
            Write(proj_label)
        )
        self.wait()

        # ========================================
        # SHOW LENGTHS
        # ========================================
        self.play(FadeOut(explanation))

        # Length of a
        a_length = np.linalg.norm(a_end[:2])
        a_length_label = Tex(
            f"|\\vec{{a}}| = \\sqrt{{13}} \\approx {a_length:.2f}",
            color=BLUE,
            font_size=28
        )
        a_length_label.to_edge(DOWN).shift(UP * 1.5)

        # Length of projection
        proj_length = np.linalg.norm(proj_point[:2])
        proj_length_label = Tex(
            f"|\\text{{proj}}| \\approx {proj_length:.2f}",
            color=GREEN,
            font_size=28
        )
        proj_length_label.next_to(a_length_label, DOWN, buff=0.2)

        self.play(Write(a_length_label))
        self.play(Write(proj_length_label))
        self.wait()

        # ========================================
        # DOT PRODUCT FORMULA
        # ========================================
        dot_formula = Tex(
            "\\vec{a} \\cdot \\vec{b} = |\\vec{a}| \\cdot |\\text{proj}_{\\vec{a}}\\vec{b}|",
            font_size=32
        )
        dot_formula.next_to(proj_length_label, DOWN, buff=0.5)

        self.play(Write(dot_formula))
        self.wait(2)


class ProjectionFormula(Scene):
    """
    Scene 3: Derive the formula a·b = |a||b|cos(θ).

    This scene shows how the projection length relates to the cosine of the
    angle between vectors, leading to the geometric formula.
    """

    def construct(self):
        # ========================================
        # SETUP: Title and vectors
        # ========================================
        title = Text("The Projection Formula", font_size=42)
        title.to_edge(UP)

        plane = NumberPlane(
            x_range=[-1, 5, 1],
            y_range=[-2, 4, 1],
            background_line_style={
                "stroke_color": GREY_A,
                "stroke_width": 1,
            }
        )
        plane.set_opacity(0.3)

        # Use simpler vectors for clearer visualization
        vector_a = create_vector_arrow(ORIGIN, np.array([4, 0, 0]), color=BLUE)
        label_a = Tex("\\vec{a}", color=BLUE, font_size=36)
        label_a.next_to(vector_a.get_end(), DOWN)

        vector_b = create_vector_arrow(ORIGIN, np.array([3, 2, 0]), color=YELLOW)
        label_b = Tex("\\vec{b}", color=YELLOW, font_size=36)
        label_b.next_to(vector_b.get_end(), UP)

        self.add(plane, title, vector_a, label_a, vector_b, label_b)
        self.wait()

        # ========================================
        # ANGLE BETWEEN VECTORS
        # ========================================
        a_end = np.array([4, 0, 0])
        b_end = np.array([3, 2, 0])

        angle = get_angle_between_vectors(a_end, b_end)
        angle_arc = create_angle_arc(
            ORIGIN,
            radius=1.0,
            start_angle=0,
            end_angle=angle,
            color=RED
        )
        theta_label = Tex("\\theta", color=RED, font_size=32)
        theta_label.move_to(ORIGIN + 1.5 * np.array([np.cos(angle/2), np.sin(angle/2), 0]))

        self.play(ShowCreation(angle_arc))
        self.play(Write(theta_label))
        self.wait()

        # ========================================
        # PROJECTION WITH RIGHT TRIANGLE
        # ========================================
        proj_point = get_projection_point(ORIGIN, a_end, b_end)

        # Projection line
        proj_line = create_projection_line(b_end, proj_point, color=GREY_A)
        self.play(ShowCreation(proj_line))
        self.wait()

        # Right angle marker
        right_angle = Square(side_length=0.3, stroke_width=2, color=GREY_A)
        right_angle.move_to(proj_point + np.array([-0.15, 0.15, 0]))

        self.play(ShowCreation(right_angle))
        self.wait()

        # ========================================
        # LABEL LENGTHS
        # ========================================
        # Length of b
        b_length = np.linalg.norm(b_end[:2])
        b_brace = Brace(Line(ORIGIN, b_end), direction=UR, buff=0.1)
        b_label = b_brace.get_text(f"|\\vec{{b}}|", buff=0.1)
        b_label.set_color(YELLOW)

        self.play(GrowFromCenter(b_brace), Write(b_label))
        self.wait()

        # Length of projection
        proj_brace = Brace(Line(ORIGIN, proj_point), direction=DOWN, buff=0.1)
        proj_label = proj_brace.get_text("|\\vec{b}|\\cos\\theta", buff=0.1)
        proj_label.set_color(GREEN)

        self.play(GrowFromCenter(proj_brace), Write(proj_label))
        self.wait()

        # ========================================
        # FORMULA DERIVATION
        # ========================================
        derivation = VGroup(
            Tex("\\text{Projection length} = |\\vec{b}|\\cos\\theta", font_size=32),
            Tex("\\vec{a} \\cdot \\vec{b} = |\\vec{a}| \\times \\text{(projection length)}", font_size=32),
            Tex("\\vec{a} \\cdot \\vec{b} = |\\vec{a}||\\vec{b}|\\cos\\theta", font_size=36, color=GREEN),
        )
        derivation.arrange(DOWN, buff=0.4, aligned_edge=LEFT)
        derivation.to_edge(DOWN).shift(UP * 0.5)

        for line in derivation:
            self.play(Write(line))
            self.wait()

        # Highlight final formula
        box = SurroundingRectangle(derivation[2], buff=0.15, color=GREEN, stroke_width=2)
        self.play(ShowCreation(box))
        self.wait(2)


class Applications(Scene):
    """
    Scene 4: Show practical applications of the dot product.

    This scene demonstrates real-world uses: computing work in physics,
    testing orthogonality, and measuring vector similarity.
    """

    def construct(self):
        # ========================================
        # TITLE
        # ========================================
        title = Text("Applications of Dot Product", font_size=42)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait()

        # ========================================
        # APPLICATION 1: Work in Physics
        # ========================================
        app1_title = Text("1. Work = Force · Displacement", font_size=32, color=BLUE)
        app1_title.next_to(title, DOWN, buff=0.8)

        self.play(Write(app1_title))
        self.wait()

        # Simple diagram
        plane1 = NumberPlane(
            x_range=[-2, 4, 1],
            y_range=[-1, 2, 1],
            background_line_style={"stroke_width": 0.5},
            height=3,
            width=5
        ).set_opacity(0.3)
        plane1.shift(LEFT * 2.5 + DOWN * 0.5)

        force = create_vector_arrow(
            plane1.c2p(0, 0),
            plane1.c2p(2, 1),
            color=RED
        )
        force_label = Tex("\\vec{F}", color=RED, font_size=28)
        force_label.next_to(force.get_end(), UP, buff=0.1)

        displacement = create_vector_arrow(
            plane1.c2p(0, 0),
            plane1.c2p(3, 0.5),
            color=GREEN
        )
        disp_label = Tex("\\vec{d}", color=GREEN, font_size=28)
        disp_label.next_to(displacement.get_end(), DOWN, buff=0.1)

        work_group = VGroup(plane1, force, force_label, displacement, disp_label)

        self.play(FadeIn(work_group))
        self.wait()

        work_formula = Tex(
            "W = \\vec{F} \\cdot \\vec{d}",
            font_size=28
        )
        work_formula.next_to(plane1, RIGHT, buff=0.5)

        self.play(Write(work_formula))
        self.wait(2)

        # ========================================
        # APPLICATION 2: Orthogonality
        # ========================================
        self.play(FadeOut(work_group), FadeOut(work_formula))

        app2_title = Text("2. Testing Orthogonality", font_size=32, color=YELLOW)
        app2_title.move_to(app1_title)

        self.play(ReplacementTransform(app1_title, app2_title))
        self.wait()

        # Orthogonal vectors
        plane2 = NumberPlane(
            x_range=[-3, 3, 1],
            y_range=[-2, 2, 1],
            background_line_style={"stroke_width": 0.5},
            height=3,
            width=5
        ).set_opacity(0.3)
        plane2.shift(LEFT * 2.5 + DOWN * 0.5)

        vec1 = create_vector_arrow(
            plane2.c2p(0, 0),
            plane2.c2p(2, 0),
            color=BLUE
        )
        vec2 = create_vector_arrow(
            plane2.c2p(0, 0),
            plane2.c2p(0, 1.5),
            color=YELLOW
        )

        ortho_group = VGroup(plane2, vec1, vec2)
        self.play(FadeIn(ortho_group))
        self.wait()

        # Right angle symbol
        right_angle = Square(side_length=0.3, stroke_width=2, color=WHITE)
        right_angle.move_to(plane2.c2p(0.15, 0.15))
        self.play(ShowCreation(right_angle))
        self.wait()

        ortho_formula = Tex(
            "\\vec{a} \\cdot \\vec{b} = 0 \\implies \\vec{a} \\perp \\vec{b}",
            font_size=28
        )
        ortho_formula.next_to(plane2, RIGHT, buff=0.5)

        self.play(Write(ortho_formula))
        self.wait(2)

        # ========================================
        # APPLICATION 3: Similarity/Alignment
        # ========================================
        self.play(FadeOut(ortho_group), FadeOut(right_angle), FadeOut(ortho_formula))

        app3_title = Text("3. Measuring Alignment", font_size=32, color=GREEN)
        app3_title.move_to(app2_title)

        self.play(ReplacementTransform(app2_title, app3_title))
        self.wait()

        # Three pairs of vectors showing different alignments
        similarity_text = VGroup(
            Text("Same direction:", font_size=24),
            Tex("\\vec{a} \\cdot \\vec{b} > 0", font_size=24, color=GREEN),
            Text("Perpendicular:", font_size=24),
            Tex("\\vec{a} \\cdot \\vec{b} = 0", font_size=24, color=YELLOW),
            Text("Opposite:", font_size=24),
            Tex("\\vec{a} \\cdot \\vec{b} < 0", font_size=24, color=RED),
        )
        similarity_text.arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        similarity_text.shift(DOWN * 0.5)

        for item in similarity_text:
            self.play(Write(item))
            self.wait(0.5)

        self.wait()

        # ========================================
        # SUMMARY
        # ========================================
        self.play(
            FadeOut(app3_title),
            FadeOut(similarity_text)
        )

        summary = VGroup(
            Text("The dot product measures:", font_size=32),
            Text("• How much vectors align", font_size=28),
            Text("• Projection of one onto another", font_size=28),
            Text("• Component in a direction", font_size=28),
        )
        summary.arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        summary.move_to(ORIGIN)

        for item in summary:
            self.play(FadeIn(item, shift=UP))
            self.wait(0.5)

        self.wait(2)

# ============================================================
# 5. SCENE SUMMARY AND EXECUTION ORDER
# ============================================================
#
# Scene 1 (IntroduceVectors):
#   - Introduces two vectors in 2D space
#   - Shows the algebraic formula a·b = ax*bx + ay*by
#   - Computes a numerical example
#
# Scene 2 (GeometricInterpretation):
#   - Visualizes projection of one vector onto another
#   - Shows the relationship between dot product and projection
#   - Introduces the geometric perspective
#
# Scene 3 (ProjectionFormula):
#   - Derives the formula a·b = |a||b|cos(θ)
#   - Uses right triangle to show projection = |b|cos(θ)
#   - Connects algebraic and geometric formulas
#
# Scene 4 (Applications):
#   - Shows practical uses in physics (work)
#   - Demonstrates orthogonality testing
#   - Explains measuring vector alignment/similarity

SCENE_ORDER = [
    IntroduceVectors,           # Part 1: Introduction and algebraic formula
    GeometricInterpretation,    # Part 2: Geometric view through projection
    ProjectionFormula,          # Part 3: Deriving |a||b|cos(θ)
    Applications,               # Part 4: Real-world applications
]
