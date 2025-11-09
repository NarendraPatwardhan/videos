"""
Natural Group Name: Simple Harmonic Motion and Circular Motion

Educational Objectives:
- To visualize simple harmonic motion as the projection of circular motion
- To demonstrate the connection between pendulums and circular motion
- To derive the equation x(t) = A cos(ωt) geometrically
- To build intuition for sinusoidal oscillation

Story Arc & Intent:
The animation reveals a beautiful connection: simple harmonic motion (like a
pendulum or spring) is simply the shadow of uniform circular motion. This
geometric insight unifies oscillation and rotation, making the sinusoidal
equation x(t) = A cos(ωt) visually obvious.

Narrative Flow:
- Hook/Opening: A pendulum swinging back and forth
- Development: Introduce circular motion at constant speed
- Build-up: Project the circular motion onto a line
- Climax: The projection exactly matches simple harmonic motion
- Resolution: Derive x(t) = A cos(ωt) from the geometry

Technical Implementation Notes:
- Scene Classes: IntroducePendulum, CircularMotion, ProjectionToSHM, Equation
- Key Visual Elements: Pendulum, circle, rotating point, projection lines
- Animation Techniques: Synchronized motion, projection visualization, graph plotting
- Mathematical Concepts: SHM, circular motion, trigonometry, periodic functions

Dependency Chain:
All scenes use basic manimlib components: Circle, Dot, Line, Axes, graphs, Text, Tex.
No custom utilities required.

Rendering Instructions:
To render these scenes, use the manim command-line tool:
- For a single scene: manimgl simple_harmonic_motion.py IntroducePendulum
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
# - BLUE: Pendulum and SHM
# - YELLOW: Circular motion
# - GREEN: Projection and connection
# - RED: Position indicator
# - WHITE: Axes and construction lines
# - GREY_A: De-emphasized elements
#
# Key Manim Constants Used:
# - UP, DOWN, LEFT, RIGHT: Direction vectors
# - ORIGIN: Center of circle
# - TAU: 2π for full rotation
# - PI: π for half rotation

# Motion parameters
AMPLITUDE = 2.0
ANGULAR_FREQ = 1.5
PERIOD = TAU / ANGULAR_FREQ

# Pendulum configuration
PENDULUM_LENGTH = 2.5
PENDULUM_AMPLITUDE = 1.2  # Max horizontal displacement

# ============================================================
# 3. UTILITY FUNCTIONS
# ============================================================

def create_pendulum(length=PENDULUM_LENGTH, angle=0, pivot_point=ORIGIN):
    """
    Create a pendulum at a given angle.

    Args:
        length: Length of the pendulum
        angle: Angle from vertical (in radians, positive = right)
        pivot_point: Location of the pivot

    Returns:
        VGroup containing the rod and bob
    """
    # Rod endpoint
    end_point = pivot_point + length * np.array([np.sin(angle), -np.cos(angle), 0])

    # Rod
    rod = Line(pivot_point, end_point, color=GREY_A, stroke_width=2)

    # Bob
    bob = Dot(end_point, radius=0.15, color=BLUE)
    bob.set_sheen(-0.3, DR)

    return VGroup(rod, bob)

def shm_position(t, amplitude=AMPLITUDE, omega=ANGULAR_FREQ, phase=0):
    """
    Position in simple harmonic motion.

    Args:
        t: Time
        amplitude: Amplitude
        omega: Angular frequency
        phase: Phase shift

    Returns:
        Position x(t) = A cos(ωt + φ)
    """
    return amplitude * np.cos(omega * t + phase)

def circular_position(t, radius=AMPLITUDE, omega=ANGULAR_FREQ, phase=0):
    """
    Position on a circle.

    Args:
        t: Time
        radius: Radius of circle
        omega: Angular frequency
        phase: Phase shift

    Returns:
        2D position as [x, y, 0]
    """
    angle = omega * t + phase
    return np.array([radius * np.cos(angle), radius * np.sin(angle), 0])

# ============================================================
# 4. BASE CLASSES AND HELPERS
# ============================================================
# No custom base classes needed

# ============================================================
# 5. SCENE IMPLEMENTATIONS
# ============================================================

class IntroducePendulum(InteractiveScene):
    """
    Part 1: Introduce a swinging pendulum as an example of SHM.

    Narrative purpose:
        To establish simple harmonic motion through a familiar example:
        a pendulum swinging back and forth in a regular pattern.

    Mathematical content:
        A pendulum (for small angles) exhibits simple harmonic motion,
        oscillating sinusoidally with a constant period.

    Visual approach:
        Show a pendulum swinging, emphasizing the smooth, periodic motion
        and the back-and-forth oscillation.
    """
    def construct(self):
        # ========================================
        # SETUP: Title
        # ========================================
        title = OldTexText("Simple Harmonic Motion", font_size=48)
        title.to_edge(UP)

        self.play(FadeIn(title, shift=DOWN))
        self.wait()

        # ========================================
        # CREATE: Pendulum pivot
        # ========================================
        pivot = Dot(2 * UP, radius=0.08, color=WHITE)

        self.play(GrowFromCenter(pivot))
        self.wait()

        # ========================================
        # CREATE: Swinging pendulum
        # ========================================
        # Time tracker for animation
        time_tracker = ValueTracker(0)

        # Dynamic pendulum
        pendulum = always_redraw(lambda: create_pendulum(
            length=PENDULUM_LENGTH,
            angle=0.5 * np.sin(ANGULAR_FREQ * time_tracker.get_value()),
            pivot_point=pivot.get_center()
        ))

        self.add(pendulum)
        self.wait()

        # ========================================
        # ANIMATE: Swinging
        # ========================================
        instruction = OldTexText(
            "The pendulum swings back and forth periodically",
            font_size=32,
            color=GREY_A
        )
        instruction.to_edge(DOWN, buff=0.8)

        self.play(FadeIn(instruction, shift=UP))
        self.wait()

        # Swing for two periods
        self.play(
            time_tracker.animate.set_value(2 * PERIOD),
            run_time=6,
            rate_func=linear
        )
        self.wait()

        # ========================================
        # OBSERVATION: Regular pattern
        # ========================================
        self.play(FadeOut(instruction))

        observation = OldTexText(
            "This is called Simple Harmonic Motion (SHM)",
            font_size=36,
            color=YELLOW
        )
        observation.to_edge(DOWN, buff=0.5)

        self.play(FadeIn(observation, shift=UP))

        # Continue swinging in background
        self.play(
            time_tracker.animate.set_value(2 * PERIOD + PERIOD),
            run_time=3,
            rate_func=linear
        )
        self.wait()


class CircularMotion(InteractiveScene):
    """
    Part 2: Introduce uniform circular motion.

    Narrative purpose:
        To present circular motion as a separate concept that will
        soon be connected to simple harmonic motion.

    Mathematical content:
        Uniform circular motion: a point moves around a circle at
        constant angular velocity ω.

    Visual approach:
        Show a point moving around a circle at constant speed,
        emphasizing the uniform, steady rotation.
    """
    def construct(self):
        # ========================================
        # SETUP: Title
        # ========================================
        title = OldTexText("Uniform Circular Motion", font_size=48)
        title.to_edge(UP)

        self.add(title)

        # ========================================
        # CREATE: Circle
        # ========================================
        circle = Circle(radius=AMPLITUDE, color=YELLOW, stroke_width=3)
        circle.move_to(ORIGIN)

        self.play(ShowCreation(circle))
        self.wait()

        # ========================================
        # CREATE: Rotating point
        # ========================================
        time_tracker = ValueTracker(0)

        # Point on circle
        moving_dot = always_redraw(lambda: Dot(
            circular_position(time_tracker.get_value()),
            radius=0.12,
            color=RED
        ).set_sheen(-0.3, DR))

        # Radius line
        radius_line = always_redraw(lambda: Line(
            ORIGIN,
            circular_position(time_tracker.get_value()),
            color=GREY_A,
            stroke_width=2
        ))

        self.play(
            GrowFromCenter(moving_dot),
            ShowCreation(radius_line)
        )
        self.wait()

        # ========================================
        # ANIMATE: Rotation
        # ========================================
        instruction = OldTexText(
            "The point moves at constant angular velocity",
            font_size=32,
            color=GREY_A
        )
        instruction.to_edge(DOWN, buff=0.8)

        self.play(FadeIn(instruction, shift=UP))
        self.wait()

        # Rotate for two periods
        self.play(
            time_tracker.animate.set_value(2 * PERIOD),
            run_time=6,
            rate_func=linear
        )
        self.wait()

        # ========================================
        # LABEL: Parameters
        # ========================================
        self.play(FadeOut(instruction))

        parameters = VGroup(
            Tex("\\text{Radius: } A", font_size=32, color=YELLOW),
            Tex("\\text{Angular velocity: } \\omega", font_size=32, color=YELLOW)
        )
        parameters.arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        parameters.to_edge(DOWN, buff=0.8)

        self.play(FadeIn(parameters, shift=UP))

        # Continue rotating
        self.play(
            time_tracker.animate.set_value(2 * PERIOD + PERIOD),
            run_time=3,
            rate_func=linear
        )
        self.wait()


class ProjectionToSHM(InteractiveScene):
    """
    Part 3: Show that SHM is the projection of circular motion.

    Narrative purpose:
        To reveal the key insight: simple harmonic motion is simply
        the horizontal (or vertical) component of circular motion.

    Mathematical content:
        If a point moves on a circle with radius A and angular velocity ω,
        its x-coordinate is x(t) = A cos(ωt), which is SHM.

    Visual approach:
        Show circular motion and SHM side by side, with a projection
        line connecting them, demonstrating their perfect synchronization.
    """
    def construct(self):
        # ========================================
        # SETUP: Title
        # ========================================
        title = OldTexText("The Connection", font_size=48)
        title.to_edge(UP)

        self.add(title)

        # ========================================
        # CREATE: Circle (on left)
        # ========================================
        circle = Circle(radius=AMPLITUDE, color=YELLOW, stroke_width=3)
        circle.shift(3 * LEFT)

        self.play(ShowCreation(circle))
        self.wait()

        # ========================================
        # CREATE: Horizontal track (on right)
        # ========================================
        track_center = 3 * RIGHT
        track = Line(
            track_center + AMPLITUDE * LEFT,
            track_center + AMPLITUDE * RIGHT,
            color=BLUE,
            stroke_width=4
        )

        self.play(ShowCreation(track))
        self.wait()

        # ========================================
        # CREATE: Moving points
        # ========================================
        time_tracker = ValueTracker(0)

        # Point on circle
        circle_dot = always_redraw(lambda: Dot(
            circle.get_center() + circular_position(time_tracker.get_value()),
            radius=0.12,
            color=RED
        ).set_sheen(-0.3, DR))

        # Point on track (SHM)
        track_dot = always_redraw(lambda: Dot(
            track_center + shm_position(time_tracker.get_value()) * RIGHT,
            radius=0.12,
            color=RED
        ).set_sheen(-0.3, DR))

        # Projection line
        projection = always_redraw(lambda: DashedLine(
            circle.get_center() + circular_position(time_tracker.get_value()),
            track_center + shm_position(time_tracker.get_value()) * RIGHT,
            color=GREEN,
            stroke_width=2
        ))

        self.play(
            GrowFromCenter(circle_dot),
            GrowFromCenter(track_dot),
            ShowCreation(projection)
        )
        self.wait()

        # ========================================
        # LABEL: The projection
        # ========================================
        label = OldTexText(
            "The horizontal projection matches SHM!",
            font_size=32,
            color=GREEN
        )
        label.to_edge(DOWN, buff=0.8)

        self.play(FadeIn(label, shift=UP))
        self.wait()

        # ========================================
        # ANIMATE: Synchronized motion
        # ========================================
        # Move for several periods to show synchronization
        self.play(
            time_tracker.animate.set_value(3 * PERIOD),
            run_time=9,
            rate_func=linear
        )
        self.wait()

        # ========================================
        # HIGHLIGHT: Perfect match
        # ========================================
        self.play(FadeOut(label))

        highlight = OldTexText(
            "They move in perfect synchronization!",
            font_size=36,
            color=YELLOW
        )
        highlight.to_edge(DOWN, buff=0.5)

        self.play(FadeIn(highlight, shift=UP))
        self.wait(2)


class Equation(InteractiveScene):
    """
    Part 4: Derive the SHM equation x(t) = A cos(ωt).

    Narrative purpose:
        To connect the visual insight to the mathematical equation,
        showing how the geometry directly gives us the formula.

    Mathematical content:
        From circular motion with radius A and angular velocity ω,
        the x-coordinate is x(t) = A cos(ωt), the SHM equation.

    Visual approach:
        Show the circle with labeled radius and angle, derive the
        x-coordinate using trigonometry, and present the final equation.
    """
    def construct(self):
        # ========================================
        # SETUP: Title
        # ========================================
        title = OldTexText("The Equation of SHM", font_size=48)
        title.to_edge(UP)

        self.add(title)

        # ========================================
        # CREATE: Circle with geometry
        # ========================================
        circle = Circle(radius=AMPLITUDE, color=YELLOW, stroke_width=3)
        circle.shift(2.5 * LEFT)

        self.add(circle)

        # Static angle for illustration
        angle = PI / 4
        point = circle.get_center() + circular_position(0, phase=angle)

        # Radius line
        radius = Line(circle.get_center(), point, color=GREY_A, stroke_width=2)

        # Point
        dot = Dot(point, radius=0.12, color=RED)
        dot.set_sheen(-0.3, DR)

        # Angle arc
        angle_arc = Arc(
            start_angle=0,
            angle=angle,
            radius=0.6,
            arc_center=circle.get_center(),
            color=GREEN,
            stroke_width=3
        )

        # Labels
        radius_label = Tex("A", font_size=36, color=YELLOW)
        radius_label.next_to(radius.get_center(), UL, buff=0.1)

        angle_label = Tex("\\omega t", font_size=32, color=GREEN)
        angle_label.next_to(angle_arc, RIGHT, buff=0.2)

        self.play(
            ShowCreation(radius),
            GrowFromCenter(dot),
            ShowCreation(angle_arc)
        )
        self.play(
            FadeIn(radius_label),
            FadeIn(angle_label)
        )
        self.wait()

        # ========================================
        # SHOW: Horizontal component
        # ========================================
        # Vertical and horizontal projections
        x_projection = DashedLine(
            point,
            circle.get_center() + (point[0] - circle.get_center()[0]) * RIGHT,
            color=BLUE,
            stroke_width=2
        )

        y_projection = DashedLine(
            circle.get_center() + (point[0] - circle.get_center()[0]) * RIGHT,
            circle.get_center(),
            color=GREY_A,
            stroke_width=2
        )

        x_label = Tex("x", font_size=36, color=BLUE)
        x_label.next_to(y_projection.get_center(), DOWN, buff=0.2)

        self.play(
            ShowCreation(x_projection),
            ShowCreation(y_projection)
        )
        self.play(FadeIn(x_label))
        self.wait()

        # ========================================
        # DERIVE: Using trigonometry
        # ========================================
        derivation = VGroup(
            Tex("\\text{From trigonometry:}", font_size=32),
            Tex("x = A \\cos(\\omega t)", font_size=40, color=BLUE),
        )
        derivation.arrange(DOWN, buff=0.4)
        derivation.shift(3 * RIGHT + 0.5 * UP)

        self.play(FadeIn(derivation, shift=LEFT, lag_ratio=0.3))
        self.wait()

        # ========================================
        # FINAL: The SHM equation
        # ========================================
        final_equation = Tex(
            "x(t) = A \\cos(\\omega t)",
            font_size=56,
            color=GREEN
        )
        final_equation.shift(3 * RIGHT + 1.5 * DOWN)

        box = SurroundingRectangle(final_equation, buff=0.3, color=GREEN, stroke_width=3)

        self.play(Write(final_equation), run_time=1.5)
        self.play(ShowCreation(box))
        self.wait()

        # ========================================
        # EXPLAIN: Parameters
        # ========================================
        parameters = VGroup(
            Tex("A = \\text{amplitude}", font_size=28),
            Tex("\\omega = \\text{angular frequency}", font_size=28),
            Tex("T = \\frac{2\\pi}{\\omega} = \\text{period}", font_size=28)
        )
        parameters.arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        parameters.next_to(box, DOWN, buff=0.5)

        self.play(FadeIn(parameters, shift=UP, lag_ratio=0.2))
        self.wait(2)

        # ========================================
        # FINALE: Checkmark
        # ========================================
        checkmark = Tex("\\checkmark", font_size=72, color=GREEN)
        checkmark.next_to(box, LEFT, buff=0.5)

        self.play(FadeIn(checkmark, scale=2))
        self.wait(2)


# ============================================================
# 6. SCENE EXECUTION ORDER
# ============================================================
# The order of scenes that tells the story.
#
# Scene 1 (IntroducePendulum):
#   - Introduces simple harmonic motion with a swinging pendulum
#   - Shows the smooth, periodic oscillation
#   - Establishes SHM as the phenomenon to understand
#
# Scene 2 (CircularMotion):
#   - Introduces uniform circular motion separately
#   - Shows a point rotating at constant angular velocity
#   - Sets up the upcoming connection
#
# Scene 3 (ProjectionToSHM):
#   - Reveals that SHM is the projection of circular motion
#   - Shows synchronized circular and linear motion
#   - Demonstrates the geometric connection
#
# Scene 4 (Equation):
#   - Derives the equation x(t) = A cos(ωt) from geometry
#   - Uses trigonometry to extract the x-coordinate
#   - Presents the final SHM equation with parameters

SCENE_ORDER = [
    IntroducePendulum,       # Part 1: Pendulum swinging (SHM)
    CircularMotion,          # Part 2: Point on circle
    ProjectionToSHM,         # Part 3: Projection connection
    Equation,                # Part 4: Derive x(t) = A cos(ωt)
]
