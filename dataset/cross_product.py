"""
Natural Group Name: Cross Product in 3D Geometry

Educational Objectives:
- To introduce the cross product as producing a perpendicular vector
- To visualize the right-hand rule for determining direction
- To show that magnitude equals parallelogram area
- To demonstrate key properties and applications

Story Arc & Intent:
The animation makes the cross product intuitive by showing it geometrically:
given two vectors, the cross product produces a third vector perpendicular
to both, with magnitude equal to the area of the parallelogram they span.
This geometric perspective reveals why the cross product is so useful.

Narrative Flow:
- Hook/Opening: Show two vectors in 3D space
- Development: Introduce the need for a perpendicular vector
- Build-up: Show the right-hand rule for finding direction
- Climax: Reveal magnitude equals parallelogram area
- Resolution: State the formula and key properties
- Extension: Mention applications (torque, angular momentum, normals)

Technical Implementation Notes:
- Scene Classes: IntroduceVectors, RightHandRule, AreaParallelogram, Properties
- Key Visual Elements: 3D vectors, parallelogram, perpendicular vector, formulas
- Animation Techniques: 3D rotation, vector animation, area highlighting
- Mathematical Concepts: Cross product, determinants, vector geometry

Dependency Chain:
All scenes use ThreeDScene for 3D visualization. Basic vectors and shapes
from manimlib. Utility functions handle cross product calculation.

Rendering Instructions:
To render these scenes, use the manim command-line tool:
- For a single scene: manimgl cross_product.py IntroduceVectors
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
# 3D configuration
VECTOR_SCALE = 2.0

# Colors
VECTOR_A_COLOR = BLUE
VECTOR_B_COLOR = GREEN
CROSS_PRODUCT_COLOR = RED
PARALLELOGRAM_COLOR = YELLOW

# ============================================================
# 3. UTILITY FUNCTIONS
# ============================================================

def create_3d_vector_arrow(vector, color=BLUE, **kwargs):
    """
    Create a 3D vector arrow from origin.

    Args:
        vector: 3D vector [x, y, z]
        color: Arrow color
        **kwargs: Additional Arrow3D parameters

    Returns:
        Arrow3D object
    """
    arrow = Arrow3D(
        start=ORIGIN,
        end=vector,
        color=color,
        **kwargs
    )
    return arrow

def calculate_cross_product(a, b):
    """
    Calculate cross product a × b.

    Args:
        a, b: 3D vectors

    Returns:
        Cross product vector
    """
    return np.cross(a, b)

def calculate_parallelogram_area(a, b):
    """
    Calculate area of parallelogram spanned by vectors a and b.

    Args:
        a, b: 3D vectors

    Returns:
        Area (magnitude of cross product)
    """
    cross = np.cross(a, b)
    return np.linalg.norm(cross)

def create_parallelogram(v1, v2, color=PARALLELOGRAM_COLOR):
    """
    Create a parallelogram spanned by two vectors.

    Args:
        v1, v2: Vectors from origin
        color: Fill color

    Returns:
        Polygon object
    """
    parallelogram = Polygon(
        ORIGIN,
        v1,
        v1 + v2,
        v2
    )
    parallelogram.set_fill(color, opacity=0.5)
    parallelogram.set_stroke(color, width=2)
    return parallelogram

# ============================================================
# 4. BASE CLASSES AND HELPERS
# ============================================================
# No custom base classes needed

# ============================================================
# 5. SCENE IMPLEMENTATIONS
# ============================================================

class IntroduceVectors(ThreeDScene):
    """
    Part 1: Introduce two vectors in 3D space.

    Narrative purpose:
        To set up the problem by showing two vectors and posing
        the question of how to find a perpendicular vector.

    Mathematical content:
        Displays two 3D vectors a and b, establishing them as our
        starting point for the cross product operation.

    Visual approach:
        Show 3D coordinate axes with two vectors clearly displayed.
        Rotate view to show 3D nature. Pose the perpendicularity question.
    """
    def construct(self):
        # ========================================
        # SETUP: Title (2D overlay)
        # ========================================
        title = OldTexText("The Cross Product", font_size=48)
        title.to_edge(UP)
        title.fix_in_frame()

        self.add(title)
        self.wait()

        # ========================================
        # CREATE: 3D axes
        # ========================================
        axes = ThreeDAxes(
            x_range=[-3, 3, 1],
            y_range=[-3, 3, 1],
            z_range=[-3, 3, 1],
        )

        # Set camera angle
        frame = self.camera.frame
        frame.set_euler_angles(theta=70 * DEGREES, phi=75 * DEGREES)

        self.play(ShowCreation(axes))
        self.wait()

        # ========================================
        # CREATE: Two vectors
        # ========================================
        # Vector a
        vec_a = np.array([2, 1, 0])
        arrow_a = create_3d_vector_arrow(vec_a, VECTOR_A_COLOR, thickness=0.02)

        label_a = Tex(R"\vec{a}", font_size=36, color=VECTOR_A_COLOR)
        label_a.fix_in_frame()
        label_a.to_edge(LEFT, buff=1).shift(1.5 * UP)

        self.play(
            GrowArrow(arrow_a),
            Write(label_a)
        )
        self.wait()

        # Vector b
        vec_b = np.array([0, 2, 1])
        arrow_b = create_3d_vector_arrow(vec_b, VECTOR_B_COLOR, thickness=0.02)

        label_b = Tex(R"\vec{b}", font_size=36, color=VECTOR_B_COLOR)
        label_b.fix_in_frame()
        label_b.next_to(label_a, DOWN, buff=0.3)

        self.play(
            GrowArrow(arrow_b),
            Write(label_b)
        )
        self.wait()

        # ========================================
        # ROTATE: Show 3D nature
        # ========================================
        self.play(
            Rotate(frame, angle=2*PI, axis=OUT, run_time=4, rate_func=linear)
        )
        self.wait()

        # ========================================
        # QUESTION: Find perpendicular vector
        # ========================================
        question = OldTexText(
            "How to find a vector perpendicular to both?",
            font_size=32,
            color=YELLOW
        )
        question.fix_in_frame()
        question.to_edge(DOWN, buff=1)

        self.play(Write(question))
        self.wait(3)

        # ========================================
        # ANSWER: Cross product!
        # ========================================
        answer = Tex(
            R"\vec{a} \times \vec{b}",
            font_size=48,
            color=CROSS_PRODUCT_COLOR
        )
        answer.fix_in_frame()
        answer.next_to(question, UP, buff=0.5)

        self.play(FadeIn(answer, scale=1.3))
        self.wait(2)

        # ========================================
        # CLEANUP
        # ========================================
        self.play(
            FadeOut(question),
            FadeOut(answer),
            FadeOut(title),
            FadeOut(label_a),
            FadeOut(label_b),
            FadeOut(axes),
            FadeOut(arrow_a),
            FadeOut(arrow_b)
        )
        self.wait()


class RightHandRule(ThreeDScene):
    """
    Part 2: Show the right-hand rule for cross product direction.

    Narrative purpose:
        To demonstrate how to determine the direction of the cross
        product using the right-hand rule.

    Mathematical content:
        Shows that a × b points in the direction determined by the
        right-hand rule: fingers curl from a to b, thumb points in
        direction of a × b.

    Visual approach:
        Visualize the right-hand rule with annotations. Show the
        cross product vector appearing perpendicular to both a and b.
    """
    def construct(self):
        # ========================================
        # SETUP: Title
        # ========================================
        title = OldTexText("The Right-Hand Rule", font_size=48)
        title.to_edge(UP)
        title.fix_in_frame()

        self.add(title)
        self.wait()

        # ========================================
        # CREATE: Axes and vectors
        # ========================================
        axes = ThreeDAxes(
            x_range=[-3, 3, 1],
            y_range=[-3, 3, 1],
            z_range=[-3, 3, 1],
        )

        frame = self.camera.frame
        frame.set_euler_angles(theta=70 * DEGREES, phi=75 * DEGREES)

        vec_a = np.array([2, 1, 0])
        vec_b = np.array([0, 2, 1])

        arrow_a = create_3d_vector_arrow(vec_a, VECTOR_A_COLOR, thickness=0.02)
        arrow_b = create_3d_vector_arrow(vec_b, VECTOR_B_COLOR, thickness=0.02)

        label_a = Tex(R"\vec{a}", font_size=32, color=VECTOR_A_COLOR)
        label_a.move_to(vec_a).shift(0.3 * RIGHT)

        label_b = Tex(R"\vec{b}", font_size=32, color=VECTOR_B_COLOR)
        label_b.move_to(vec_b).shift(0.3 * UP)

        self.play(
            ShowCreation(axes),
            GrowArrow(arrow_a),
            GrowArrow(arrow_b),
            Write(label_a),
            Write(label_b)
        )
        self.wait()

        # ========================================
        # COMPUTE: Cross product
        # ========================================
        vec_cross = calculate_cross_product(vec_a, vec_b)
        arrow_cross = create_3d_vector_arrow(vec_cross, CROSS_PRODUCT_COLOR, thickness=0.03)

        label_cross = Tex(R"\vec{a} \times \vec{b}", font_size=32, color=CROSS_PRODUCT_COLOR)
        label_cross.move_to(vec_cross).shift(0.5 * OUT)

        cross_label_fixed = Tex(
            R"\vec{a} \times \vec{b}",
            font_size=36,
            color=CROSS_PRODUCT_COLOR
        )
        cross_label_fixed.fix_in_frame()
        cross_label_fixed.to_edge(LEFT, buff=1).shift(UP)

        self.play(
            GrowArrow(arrow_cross),
            Write(label_cross),
            Write(cross_label_fixed)
        )
        self.wait(2)

        # ========================================
        # EXPLAIN: Right-hand rule
        # ========================================
        explanation = VGroup(
            OldTexText("Right-Hand Rule:", font_size=28, weight=BOLD),
            OldTexText("• Point fingers along  a", font_size=24, color=VECTOR_A_COLOR),
            OldTexText("• Curl toward  b", font_size=24, color=VECTOR_B_COLOR),
            OldTexText("• Thumb points along  a × b", font_size=24, color=CROSS_PRODUCT_COLOR),
        )
        explanation.arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        explanation.fix_in_frame()
        explanation.to_edge(DOWN, buff=0.5)

        self.play(
            LaggedStart(
                *[FadeIn(line, shift=RIGHT) for line in explanation],
                lag_ratio=0.5
            ),
            run_time=3
        )
        self.wait(3)

        # ========================================
        # ROTATE: Show perpendicularity
        # ========================================
        self.play(FadeOut(explanation))

        perp_text = OldTexText(
            "Perpendicular to both!",
            font_size=32,
            color=YELLOW
        )
        perp_text.fix_in_frame()
        perp_text.to_edge(DOWN, buff=1)

        self.play(Write(perp_text))

        # Rotate to show from different angles
        self.play(
            Rotate(frame, angle=PI, axis=OUT, run_time=3)
        )
        self.wait(2)

        # ========================================
        # CLEANUP
        # ========================================
        self.play(FadeOut(*self.mobjects))
        self.wait()


class AreaParallelogram(ThreeDScene):
    """
    Part 3: Show that magnitude equals parallelogram area.

    Narrative purpose:
        To reveal the geometric meaning of the cross product magnitude:
        it equals the area of the parallelogram spanned by the vectors.

    Mathematical content:
        Shows |a × b| = area of parallelogram with sides a and b.
        Connects to the formula |a||b|sin(θ).

    Visual approach:
        Draw the parallelogram spanned by a and b, calculate its area,
        show it equals |a × b|.
    """
    def construct(self):
        # ========================================
        # SETUP: Title
        # ========================================
        title = OldTexText("Magnitude = Parallelogram Area", font_size=44)
        title.to_edge(UP)
        title.fix_in_frame()

        self.add(title)
        self.wait()

        # ========================================
        # CREATE: Axes and vectors
        # ========================================
        axes = ThreeDAxes(
            x_range=[-3, 3, 1],
            y_range=[-3, 3, 1],
            z_range=[-3, 3, 1],
        )

        frame = self.camera.frame
        frame.set_euler_angles(theta=70 * DEGREES, phi=75 * DEGREES)

        vec_a = np.array([2, 1, 0])
        vec_b = np.array([0, 2, 1])

        arrow_a = create_3d_vector_arrow(vec_a, VECTOR_A_COLOR, thickness=0.02)
        arrow_b = create_3d_vector_arrow(vec_b, VECTOR_B_COLOR, thickness=0.02)

        self.play(
            ShowCreation(axes),
            GrowArrow(arrow_a),
            GrowArrow(arrow_b)
        )
        self.wait()

        # ========================================
        # CREATE: Parallelogram
        # ========================================
        parallelogram = create_parallelogram(vec_a, vec_b, PARALLELOGRAM_COLOR)

        para_label = OldTexText(
            "Parallelogram spanned by a and b",
            font_size=28,
            color=PARALLELOGRAM_COLOR
        )
        para_label.fix_in_frame()
        para_label.to_edge(LEFT, buff=0.5).shift(1.5 * UP)

        self.play(
            DrawBorderThenFill(parallelogram),
            Write(para_label)
        )
        self.wait(2)

        # ========================================
        # CALCULATE: Area
        # ========================================
        area = calculate_parallelogram_area(vec_a, vec_b)

        area_calc = Tex(
            f"\\text{{Area}} = |\\vec{{a}} \\times \\vec{{b}}| \\approx {area:.2f}",
            font_size=32,
            color=YELLOW
        )
        area_calc.fix_in_frame()
        area_calc.next_to(para_label, DOWN, buff=0.5, aligned_edge=LEFT)

        self.play(Write(area_calc))
        self.wait(2)

        # ========================================
        # SHOW: Cross product vector
        # ========================================
        vec_cross = calculate_cross_product(vec_a, vec_b)
        arrow_cross = create_3d_vector_arrow(vec_cross, CROSS_PRODUCT_COLOR, thickness=0.03)

        cross_label = Tex(
            R"\vec{a} \times \vec{b}",
            font_size=32,
            color=CROSS_PRODUCT_COLOR
        )
        cross_label.fix_in_frame()
        cross_label.next_to(area_calc, DOWN, buff=0.5, aligned_edge=LEFT)

        self.play(
            GrowArrow(arrow_cross),
            Write(cross_label)
        )
        self.wait(2)

        # ========================================
        # FORMULA: Alternative form
        # ========================================
        formula = Tex(
            R"|\vec{a} \times \vec{b}| = |\vec{a}| \cdot |\vec{b}| \cdot \sin\theta",
            font_size=32
        )
        formula.fix_in_frame()
        formula.to_edge(DOWN, buff=1)

        angle_note = OldTexText(
            "θ = angle between vectors",
            font_size=24,
            color=GREY_A
        )
        angle_note.fix_in_frame()
        angle_note.next_to(formula, DOWN, buff=0.2)

        self.play(
            Write(formula),
            Write(angle_note)
        )
        self.wait(3)

        # ========================================
        # INSIGHT
        # ========================================
        self.play(
            FadeOut(angle_note),
            formula.animate.shift(0.3 * UP)
        )

        insight = OldTexText(
            "This is why parallel vectors have zero cross product!",
            font_size=26,
            color=GREEN
        )
        insight.fix_in_frame()
        insight.next_to(formula, DOWN, buff=0.3)

        self.play(Write(insight))
        self.wait(3)

        # ========================================
        # CLEANUP
        # ========================================
        self.play(FadeOut(*self.mobjects))
        self.wait()


class Properties(InteractiveScene):
    """
    Part 4: State formula and key properties.

    Narrative purpose:
        To summarize the cross product formula, key properties,
        and mention important applications.

    Mathematical content:
        Shows determinant formula, anti-commutativity, distributivity.
        Mentions applications in physics and graphics.

    Visual approach:
        List properties clearly with examples. Show formula using
        determinant notation. Emphasize practical importance.
    """
    def construct(self):
        # ========================================
        # SETUP: Title
        # ========================================
        title = OldTexText("Cross Product: Formula & Properties", font_size=44)
        title.to_edge(UP)

        self.play(FadeIn(title, shift=DOWN))
        self.wait()

        # ========================================
        # FORMULA: Determinant form
        # ========================================
        formula_title = OldTexText("Formula (Determinant Form):", font_size=32, weight=BOLD)
        formula_title.shift(1.8 * UP)

        self.play(Write(formula_title))
        self.wait()

        formula = Tex(
            R"\vec{a} \times \vec{b} = \begin{vmatrix} "
            R"\vec{i} & \vec{j} & \vec{k} \\ "
            R"a_x & a_y & a_z \\ "
            R"b_x & b_y & b_z "
            R"\end{vmatrix}",
            font_size=36
        )
        formula.next_to(formula_title, DOWN, buff=0.5)

        self.play(Write(formula))
        self.wait(2)

        # Expanded form
        expanded = Tex(
            R"= (a_y b_z - a_z b_y)\vec{i} - (a_x b_z - a_z b_x)\vec{j} + (a_x b_y - a_y b_x)\vec{k}",
            font_size=28
        )
        expanded.next_to(formula, DOWN, buff=0.4)

        self.play(Write(expanded))
        self.wait(2)

        # ========================================
        # PROPERTIES
        # ========================================
        self.play(
            FadeOut(formula),
            FadeOut(expanded),
            formula_title.animate.shift(2.5 * UP).scale(0.8)
        )

        props_title = OldTexText("Key Properties:", font_size=32, weight=BOLD)
        props_title.shift(1 * UP)

        self.play(Write(props_title))
        self.wait()

        properties = VGroup(
            Tex(R"1. \quad \vec{a} \times \vec{b} = -(\vec{b} \times \vec{a}) "
                R"\quad \text{(anti-commutative)}", font_size=26),
            Tex(R"2. \quad \vec{a} \times \vec{a} = \vec{0}", font_size=26),
            Tex(R"3. \quad \vec{a} \times (\vec{b} + \vec{c}) = "
                R"\vec{a} \times \vec{b} + \vec{a} \times \vec{c} "
                R"\quad \text{(distributive)}", font_size=26),
            Tex(R"4. \quad (c\vec{a}) \times \vec{b} = c(\vec{a} \times \vec{b})", font_size=26),
            Tex(R"5. \quad \vec{a} \cdot (\vec{a} \times \vec{b}) = 0 "
                R"\quad \text{(perpendicularity)}", font_size=26),
        )
        properties.arrange(DOWN, buff=0.4, aligned_edge=LEFT)
        properties.next_to(props_title, DOWN, buff=0.6)

        self.play(
            LaggedStart(
                *[FadeIn(prop, shift=RIGHT) for prop in properties],
                lag_ratio=0.4
            ),
            run_time=5
        )
        self.wait(3)

        # ========================================
        # APPLICATIONS
        # ========================================
        self.play(
            FadeOut(properties),
            FadeOut(props_title)
        )

        apps_title = OldTexText("Applications:", font_size=36, weight=BOLD)
        apps_title.shift(1.5 * UP)

        self.play(Write(apps_title))
        self.wait()

        applications = VGroup(
            OldTexText("• Physics: Torque = r × F", font_size=28),
            OldTexText("• Angular momentum: L = r × p", font_size=28),
            OldTexText("• Magnetic force: F = q(v × B)", font_size=28),
            OldTexText("• Computer Graphics: Surface normals", font_size=28),
            OldTexText("• Rotation: Angular velocity vectors", font_size=28),
            OldTexText("• Geometry: Area calculations", font_size=28),
        )
        applications.arrange(DOWN, buff=0.35, aligned_edge=LEFT)
        applications.next_to(apps_title, DOWN, buff=0.7)

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

        final = OldTexText(
            "The cross product: a fundamental tool\nfor 3D geometry and physics!",
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
# Scene 1 (IntroduceVectors):
#   - Shows two 3D vectors
#   - Poses perpendicularity question
#   - Introduces cross product notation
#
# Scene 2 (RightHandRule):
#   - Demonstrates right-hand rule
#   - Shows cross product direction
#   - Emphasizes perpendicularity
#
# Scene 3 (AreaParallelogram):
#   - Shows parallelogram spanned by vectors
#   - Reveals magnitude equals area
#   - Gives formula |a||b|sin(θ)
#
# Scene 4 (Properties):
#   - Shows determinant formula
#   - Lists key properties
#   - Mentions applications

SCENE_ORDER = [
    IntroduceVectors,      # Part 1: Setup
    RightHandRule,         # Part 2: Direction
    AreaParallelogram,     # Part 3: Magnitude
    Properties,            # Part 4: Formula & uses
]
