"""
Quaternions for 3D Rotations

This module demonstrates quaternions, a 4D number system used for representing
3D rotations in computer graphics, robotics, and physics. Covers quaternion
arithmetic, rotation representation, and advantages over other methods.

Scenes:
    - IntroduceQuaternions: Introduction to quaternions as extension of complex numbers
    - MultiplicationRule: Quaternion multiplication and the famous identity
    - ThreeDRotations: Using quaternions for 3D rotations (uses ThreeDScene)
    - AvoidGimbalLock: Advantages over Euler angles
"""

from manimlib import *
import numpy as np


class IntroduceQuaternions(Scene):
    """
    Introduce quaternions as an extension of complex numbers to 4D.
    """

    def construct(self):
        # Title
        title = OldTexText("Quaternions", font_size=56)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait()

        # Subtitle
        subtitle = OldTexText("A 4D number system", font_size=36, color=GREY)
        subtitle.next_to(title, DOWN, buff=0.3)
        self.play(Write(subtitle))
        self.wait(2)
        self.play(FadeOut(subtitle))

        # Historical context
        history = OldTexText(
            "Discovered by William Rowan Hamilton (1843)",
            font_size=32,
            color=GREY,
            slant=ITALIC
        )
        history.move_to(UP * 2.5)
        self.play(Write(history))
        self.wait(2)
        self.play(FadeOut(history))

        # Build up from real to complex to quaternions
        progression_title = OldTexText("Number System Evolution:", font_size=36, color=YELLOW)
        progression_title.move_to(UP * 2.3)
        self.play(Write(progression_title))
        self.wait()

        # Real numbers
        reals = VGroup(
            OldTexText("Real Numbers", font_size=32, color=BLUE),
            Tex(R"\mathbb{R}: a", font_size=32),
            OldTexText("1 dimension", font_size=24, color=GREY)
        )
        reals.arrange(DOWN, buff=0.3)
        reals.move_to(UP * 0.8 + LEFT * 4)
        self.play(Write(reals))
        self.wait()

        # Complex numbers
        complex_nums = VGroup(
            OldTexText("Complex Numbers", font_size=32, color=GREEN),
            Tex(R"\mathbb{C}: a + bi", font_size=32),
            Tex(R"i^2 = -1", font_size=28, color=GREY),
            OldTexText("2 dimensions", font_size=24, color=GREY)
        )
        complex_nums.arrange(DOWN, buff=0.3)
        complex_nums.move_to(UP * 0.8)
        self.play(Write(complex_nums))
        self.wait()

        # Quaternions
        quaternions = VGroup(
            OldTexText("Quaternions", font_size=32, color=RED),
            Tex(R"\mathbb{H}: a + bi + cj + dk", font_size=28),
            Tex(R"i^2 = j^2 = k^2 = ijk = -1", font_size=24, color=GREY),
            OldTexText("4 dimensions", font_size=24, color=GREY)
        )
        quaternions.arrange(DOWN, buff=0.3)
        quaternions.move_to(UP * 0.8 + RIGHT * 4.2)
        self.play(Write(quaternions))
        self.wait(2)

        # Highlight the defining identity
        self.play(
            FadeOut(reals),
            FadeOut(complex_nums),
            FadeOut(progression_title)
        )

        identity_title = OldTexText("The Fundamental Identity:", font_size=40, color=YELLOW)
        identity_title.move_to(UP * 1.5)
        self.play(
            quaternions.animate.move_to(ORIGIN),
            Write(identity_title)
        )
        self.wait()

        # Highlight the identity
        identity = Tex(R"i^2 = j^2 = k^2 = ijk = -1", font_size=52, color=RED)
        identity.move_to(DOWN * 1)

        identity_box = SurroundingRectangle(identity, color=YELLOW, buff=0.25)

        self.play(
            FadeOut(quaternions),
            Write(identity)
        )
        self.wait(0.5)
        self.play(ShowCreation(identity_box))
        self.wait(2)

        # General form
        self.play(
            FadeOut(identity),
            FadeOut(identity_box),
            FadeOut(identity_title)
        )

        form_title = OldTexText("General Quaternion:", font_size=40, color=BLUE)
        form_title.move_to(UP * 1.8)
        self.play(Write(form_title))
        self.wait()

        general_form = Tex(
            R"q = a + bi + cj + dk",
            font_size=48
        )
        general_form.move_to(UP * 0.5)
        self.play(Write(general_form))
        self.wait()

        # Components
        components = VGroup(
            Tex(R"a, b, c, d \in \mathbb{R}", font_size=36),
            Tex(R"\text{Scalar part: } a", font_size=32, color=GREEN),
            Tex(R"\text{Vector part: } bi + cj + dk", font_size=32, color=PURPLE)
        )
        components.arrange(DOWN, buff=0.5)
        components.move_to(DOWN * 1.2)
        self.play(LaggedStart([Write(comp) for comp in components], lag_ratio=0.4))
        self.wait(3)


class MultiplicationRule(Scene):
    """
    Explain quaternion multiplication rules.
    """

    def construct(self):
        # Title
        title = OldTexText("Quaternion Multiplication", font_size=52)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait()

        # The fundamental rules
        rules_title = OldTexText("Multiplication Rules:", font_size=36, color=YELLOW)
        rules_title.move_to(UP * 2.3)
        self.play(Write(rules_title))
        self.wait()

        # Basic identities
        basic_rules = VGroup(
            Tex(R"i^2 = j^2 = k^2 = -1", font_size=36),
            Tex(R"ij = k, \quad jk = i, \quad ki = j", font_size=36, color=BLUE),
            Tex(R"ji = -k, \quad kj = -i, \quad ik = -j", font_size=36, color=RED)
        )
        basic_rules.arrange(DOWN, buff=0.5)
        basic_rules.move_to(UP * 0.6)

        self.play(LaggedStart([Write(rule) for rule in basic_rules], lag_ratio=0.5))
        self.wait(2)

        # Highlight non-commutativity
        note = OldTexText(
            "Note: Multiplication is NOT commutative!",
            font_size=32,
            color=YELLOW
        )
        note.next_to(basic_rules, DOWN, buff=0.6)
        self.play(Write(note))
        self.wait()

        example = Tex(R"ij = k \neq -k = ji", font_size=36, color=RED)
        example.next_to(note, DOWN, buff=0.4)
        self.play(Write(example))
        self.wait(2)

        # Memory aid: cyclic pattern
        self.play(
            FadeOut(note),
            FadeOut(example)
        )

        memory_title = OldTexText("Memory Aid - Cyclic Pattern:", font_size=32, color=GREEN)
        memory_title.move_to(DOWN * 0.8)
        self.play(Write(memory_title))
        self.wait()

        # Draw a circle with i, j, k
        circle = Circle(radius=1.5, color=WHITE)
        circle.move_to(DOWN * 2.5)

        # Place i, j, k around circle
        i_pos = circle.point_at_angle(PI/2)
        j_pos = circle.point_at_angle(PI/2 + 2*PI/3)
        k_pos = circle.point_at_angle(PI/2 + 4*PI/3)

        i_label = Tex("i", font_size=40, color=BLUE).move_to(i_pos + UP * 0.3)
        j_label = Tex("j", font_size=40, color=GREEN).move_to(j_pos + LEFT * 0.4 + DOWN * 0.2)
        k_label = Tex("k", font_size=40, color=RED).move_to(k_pos + RIGHT * 0.4 + DOWN * 0.2)

        # Arrows showing direction
        arrow1 = CurvedArrow(
            i_pos + RIGHT * 0.2,
            j_pos + UP * 0.3,
            angle=-PI/3,
            color=YELLOW
        )
        arrow2 = CurvedArrow(
            j_pos + DOWN * 0.3 + RIGHT * 0.1,
            k_pos + DOWN * 0.2 + LEFT * 0.2,
            angle=-PI/3,
            color=YELLOW
        )
        arrow3 = CurvedArrow(
            k_pos + LEFT * 0.2 + UP * 0.1,
            i_pos + RIGHT * 0.2 + DOWN * 0.3,
            angle=-PI/3,
            color=YELLOW
        )

        self.play(ShowCreation(circle))
        self.play(Write(i_label), Write(j_label), Write(k_label))
        self.wait()
        self.play(ShowCreation(arrow1), ShowCreation(arrow2), ShowCreation(arrow3))
        self.wait()

        cyclic_note = OldTexText("Clockwise: positive, Counter-clockwise: negative", font_size=24, color=GREY)
        cyclic_note.next_to(circle, DOWN, buff=0.5)
        self.play(Write(cyclic_note))
        self.wait(3)


class ThreeDRotations(ThreeDScene):
    """
    Demonstrate using quaternions for 3D rotations.
    """

    def construct(self):
        # Title (2D, doesn't rotate with camera)
        title = OldTexText("Quaternions for 3D Rotations", font_size=48)
        title.to_edge(UP)
        title.fix_in_frame()
        self.play(Write(title))
        self.wait()

        # Set up 3D axes
        axes = ThreeDAxes(
            x_range=[-3, 3, 1],
            y_range=[-3, 3, 1],
            z_range=[-3, 3, 1],
        )
        axes.set_stroke(width=2)

        # Labels
        x_label = Tex("x", font_size=36).next_to(axes.x_axis, RIGHT)
        y_label = Tex("y", font_size=36).next_to(axes.y_axis, UP)
        z_label = Tex("z", font_size=36).next_to(axes.z_axis, OUT)

        self.add(axes, x_label, y_label, z_label)
        self.wait()

        # Initial camera position
        self.set_camera_orientation(phi=70 * DEGREES, theta=-45 * DEGREES)
        self.wait()

        # Create a 3D object to rotate (a vector/arrow)
        vector = Arrow3D(
            start=ORIGIN,
            end=2 * RIGHT + UP,
            color=BLUE,
            thickness=0.02
        )
        self.play(ShowCreation(vector))
        self.wait()

        # Explanation text (fixed in frame)
        explanation = OldTexText(
            "Rotation quaternion: q = cos(θ/2) + sin(θ/2)(ui + vj + wk)",
            font_size=24,
            color=YELLOW
        )
        explanation.to_edge(DOWN)
        explanation.fix_in_frame()
        self.play(Write(explanation))
        self.wait(2)

        # Example rotation: 90 degrees around z-axis
        rotation_info = OldTexText(
            "Rotate 90° around z-axis",
            font_size=28,
            color=GREEN
        )
        rotation_info.next_to(explanation, UP, buff=0.3)
        rotation_info.fix_in_frame()
        self.play(Write(rotation_info))
        self.wait()

        # Axis of rotation
        rotation_axis = Arrow3D(
            start=ORIGIN,
            end=2 * OUT,
            color=GREEN,
            thickness=0.015
        )
        self.play(ShowCreation(rotation_axis))
        self.wait()

        # Perform rotation
        # For z-axis rotation by 90 degrees:
        # q = cos(45°) + sin(45°)k = 0.707 + 0.707k
        rotated_vector = Arrow3D(
            start=ORIGIN,
            end=2 * UP - RIGHT,  # Result of rotating (2,1,0) by 90° around z
            color=RED,
            thickness=0.02
        )

        self.play(
            Transform(vector, rotated_vector),
            Rotate(vector, angle=PI/2, axis=OUT),
            run_time=2
        )
        self.wait(2)

        # Show the rotation from different angles
        self.play(FadeOut(rotation_info), FadeOut(explanation))

        camera_note = OldTexText("View from different angles", font_size=28, color=YELLOW)
        camera_note.to_edge(DOWN)
        camera_note.fix_in_frame()
        self.play(Write(camera_note))

        # Rotate camera
        self.begin_ambient_camera_rotation(rate=0.3)
        self.wait(5)
        self.stop_ambient_camera_rotation()
        self.wait()

        # Formula for rotation
        self.play(FadeOut(camera_note))
        formula_text = OldTexText("Rotation formula:", font_size=28, color=BLUE)
        formula_text.to_edge(DOWN).shift(UP * 0.5)
        formula_text.fix_in_frame()

        formula = Tex(
            R"v' = qvq^{-1}",
            font_size=36,
            color=BLUE
        )
        formula.next_to(formula_text, DOWN, buff=0.3)
        formula.fix_in_frame()

        self.play(Write(formula_text), Write(formula))
        self.wait(3)


class AvoidGimbalLock(Scene):
    """
    Explain advantages of quaternions over Euler angles, especially gimbal lock.
    """

    def construct(self):
        # Title
        title = OldTexText("Why Use Quaternions?", font_size=52)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait()

        # Comparison table
        comparison_title = OldTexText("Quaternions vs Euler Angles", font_size=36, color=YELLOW)
        comparison_title.move_to(UP * 2.5)
        self.play(Write(comparison_title))
        self.wait()

        # Euler angles problems
        euler_title = OldTexText("Euler Angles:", font_size=32, color=RED)
        euler_title.move_to(UP * 1.2 + LEFT * 3.5)

        euler_problems = VGroup(
            OldTexText("✗ Gimbal lock", font_size=28, color=RED),
            OldTexText("✗ Singularities", font_size=28, color=RED),
            OldTexText("✗ Interpolation issues", font_size=28, color=RED),
            OldTexText("✗ Order dependent", font_size=28, color=RED)
        )
        euler_problems.arrange(DOWN, aligned_edge=LEFT, buff=0.35)
        euler_problems.next_to(euler_title, DOWN, buff=0.4, aligned_edge=LEFT)

        self.play(Write(euler_title))
        self.wait(0.5)
        self.play(LaggedStart([Write(prob) for prob in euler_problems], lag_ratio=0.3))
        self.wait(2)

        # Quaternion advantages
        quat_title = OldTexText("Quaternions:", font_size=32, color=GREEN)
        quat_title.move_to(UP * 1.2 + RIGHT * 3.5)

        quat_advantages = VGroup(
            OldTexText("✓ No gimbal lock", font_size=28, color=GREEN),
            OldTexText("✓ No singularities", font_size=28, color=GREEN),
            OldTexText("✓ Smooth interpolation (SLERP)", font_size=28, color=GREEN),
            OldTexText("✓ Compact representation", font_size=28, color=GREEN)
        )
        quat_advantages.arrange(DOWN, aligned_edge=LEFT, buff=0.35)
        quat_advantages.next_to(quat_title, DOWN, buff=0.4, aligned_edge=LEFT)

        self.play(Write(quat_title))
        self.wait(0.5)
        self.play(LaggedStart([Write(adv) for adv in quat_advantages], lag_ratio=0.3))
        self.wait(3)

        # Explain gimbal lock
        self.play(
            FadeOut(euler_title),
            FadeOut(euler_problems),
            FadeOut(quat_title),
            FadeOut(quat_advantages),
            FadeOut(comparison_title)
        )

        gimbal_title = OldTexText("What is Gimbal Lock?", font_size=44, color=YELLOW)
        gimbal_title.move_to(UP * 2.5)
        self.play(Write(gimbal_title))
        self.wait()

        explanation = OldTexText(
            "Loss of one degree of freedom when two rotation axes align",
            font_size=30,
            color=GREY
        )
        explanation.next_to(gimbal_title, DOWN, buff=0.4)
        self.play(Write(explanation))
        self.wait(2)

        # Simple diagram
        diagram_title = OldTexText("Example: Aircraft rotation (pitch = 90°)", font_size=28)
        diagram_title.move_to(UP * 0.5)
        self.play(Write(diagram_title))
        self.wait()

        problem_text = VGroup(
            OldTexText("When pitch = 90°:", font_size=26, color=RED),
            OldTexText("• Roll and yaw axes become parallel", font_size=24),
            OldTexText("• Cannot distinguish between them", font_size=24),
            OldTexText("• Lost one degree of freedom!", font_size=24, color=RED)
        )
        problem_text.arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        problem_text.move_to(DOWN * 1)
        self.play(LaggedStart([Write(text) for text in problem_text], lag_ratio=0.3))
        self.wait(3)

        # Solution
        self.play(
            FadeOut(diagram_title),
            FadeOut(problem_text),
            FadeOut(explanation)
        )

        solution = OldTexText("Quaternions avoid this problem!", font_size=40, color=GREEN)
        solution.move_to(UP * 0.8)
        self.play(Write(solution))
        self.wait()

        why = VGroup(
            OldTexText("• No Euler angle decomposition", font_size=28),
            OldTexText("• 4D representation has no singularities", font_size=28),
            OldTexText("• All rotations are equally valid", font_size=28),
        )
        why.arrange(DOWN, aligned_edge=LEFT, buff=0.4)
        why.next_to(solution, DOWN, buff=0.6)
        self.play(LaggedStart([Write(w) for w in why], lag_ratio=0.3))
        self.wait(2)

        # Applications
        self.play(FadeOut(solution), FadeOut(why), FadeOut(gimbal_title))

        app_title = OldTexText("Applications:", font_size=40, color=BLUE)
        app_title.move_to(UP * 1.8)
        self.play(Write(app_title))
        self.wait()

        applications = VGroup(
            OldTexText("• Computer graphics and animation", font_size=30),
            OldTexText("• Robotics and spacecraft orientation", font_size=30),
            OldTexText("• Virtual reality and game engines", font_size=30),
            OldTexText("• Physics simulations", font_size=30),
        )
        applications.arrange(DOWN, aligned_edge=LEFT, buff=0.5)
        applications.move_to(DOWN * 0.3)
        self.play(LaggedStart([Write(app) for app in applications], lag_ratio=0.3))
        self.wait(3)


# Utility functions for quaternions

class Quaternion:
    """
    Simple quaternion class for computations.
    """

    def __init__(self, w=0, x=0, y=0, z=0):
        """
        Create a quaternion q = w + xi + yj + zk.

        Args:
            w: Scalar (real) part
            x, y, z: Vector (imaginary) parts
        """
        self.w = w
        self.x = x
        self.y = y
        self.z = z

    def __mul__(self, other):
        """Quaternion multiplication."""
        if isinstance(other, Quaternion):
            w = self.w * other.w - self.x * other.x - self.y * other.y - self.z * other.z
            x = self.w * other.x + self.x * other.w + self.y * other.z - self.z * other.y
            y = self.w * other.y - self.x * other.z + self.y * other.w + self.z * other.x
            z = self.w * other.z + self.x * other.y - self.y * other.x + self.z * other.w
            return Quaternion(w, x, y, z)
        else:
            # Scalar multiplication
            return Quaternion(self.w * other, self.x * other, self.y * other, self.z * other)

    def conjugate(self):
        """Return quaternion conjugate."""
        return Quaternion(self.w, -self.x, -self.y, -self.z)

    def norm(self):
        """Return quaternion norm."""
        return np.sqrt(self.w**2 + self.x**2 + self.y**2 + self.z**2)

    def normalize(self):
        """Return normalized (unit) quaternion."""
        n = self.norm()
        if n > 0:
            return Quaternion(self.w / n, self.x / n, self.y / n, self.z / n)
        return self

    def inverse(self):
        """Return quaternion inverse."""
        conj = self.conjugate()
        norm_sq = self.norm() ** 2
        return Quaternion(conj.w / norm_sq, conj.x / norm_sq, conj.y / norm_sq, conj.z / norm_sq)

    def to_array(self):
        """Convert to numpy array [w, x, y, z]."""
        return np.array([self.w, self.x, self.y, self.z])


def rotation_quaternion(angle, axis):
    """
    Create a quaternion representing rotation by angle around axis.

    Args:
        angle: Rotation angle in radians
        axis: Rotation axis as [x, y, z] (will be normalized)

    Returns:
        Quaternion representing the rotation
    """
    axis = np.array(axis)
    axis = axis / np.linalg.norm(axis)

    half_angle = angle / 2
    w = np.cos(half_angle)
    x, y, z = np.sin(half_angle) * axis

    return Quaternion(w, x, y, z)


def rotate_vector_by_quaternion(vector, quaternion):
    """
    Rotate a 3D vector using a quaternion.

    Args:
        vector: 3D vector as [x, y, z]
        quaternion: Rotation quaternion (should be unit quaternion)

    Returns:
        Rotated vector
    """
    # Represent vector as quaternion with w=0
    v_quat = Quaternion(0, vector[0], vector[1], vector[2])

    # Compute q * v * q^(-1)
    rotated = quaternion * v_quat * quaternion.inverse()

    return np.array([rotated.x, rotated.y, rotated.z])


def quaternion_to_rotation_matrix(q):
    """
    Convert quaternion to 3x3 rotation matrix.

    Args:
        q: Quaternion

    Returns:
        3x3 rotation matrix
    """
    w, x, y, z = q.w, q.x, q.y, q.z

    return np.array([
        [1 - 2*y**2 - 2*z**2, 2*x*y - 2*w*z, 2*x*z + 2*w*y],
        [2*x*y + 2*w*z, 1 - 2*x**2 - 2*z**2, 2*y*z - 2*w*x],
        [2*x*z - 2*w*y, 2*y*z + 2*w*x, 1 - 2*x**2 - 2*y**2]
    ])


def slerp(q1, q2, t):
    """
    Spherical linear interpolation between two quaternions.

    Args:
        q1, q2: Quaternions to interpolate between
        t: Interpolation parameter in [0, 1]

    Returns:
        Interpolated quaternion
    """
    # Compute dot product
    dot = q1.w * q2.w + q1.x * q2.x + q1.y * q2.y + q1.z * q2.z

    # If dot is negative, negate one quaternion to take shorter path
    if dot < 0:
        q2 = Quaternion(-q2.w, -q2.x, -q2.y, -q2.z)
        dot = -dot

    # Clamp dot to [-1, 1]
    dot = np.clip(dot, -1, 1)

    # Compute angle
    theta = np.arccos(dot)

    # Handle close quaternions
    if abs(theta) < 1e-6:
        return q1

    # Compute interpolation
    sin_theta = np.sin(theta)
    w1 = np.sin((1 - t) * theta) / sin_theta
    w2 = np.sin(t * theta) / sin_theta

    return Quaternion(
        w1 * q1.w + w2 * q2.w,
        w1 * q1.x + w2 * q2.x,
        w1 * q1.y + w2 * q2.y,
        w1 * q1.z + w2 * q2.z
    )
