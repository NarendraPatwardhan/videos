"""
Brachistochrone Problem

This module demonstrates the brachistochrone problem - finding the curve of fastest descent
between two points. The solution is a cycloid curve, which is derived using calculus of
variations. This is a classic problem in physics and mathematics.

Scenes:
    - IntroduceProblem: Set up the brachistochrone problem
    - CompareRamps: Compare different path shapes (straight, arc, cycloid)
    - CycloidSolution: Show that the cycloid is the optimal solution
    - PhysicsExplanation: Explain the physics and calculus of variations
"""

from manimlib import *
import numpy as np


class IntroduceProblem(Scene):
    """
    Introduce the brachistochrone problem: what curve gives the fastest descent?
    """

    def construct(self):
        # Title
        title = Text("The Brachistochrone Problem", font_size=56)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait()

        # Etymology
        etymology = Text(
            "From Greek: brachistos (shortest) + chronos (time)",
            font_size=28,
            color=GREY
        )
        etymology.next_to(title, DOWN, buff=0.3)
        self.play(Write(etymology))
        self.wait(2)
        self.play(FadeOut(etymology))

        # The question
        question = Text(
            "What curve gives the fastest descent between two points?",
            font_size=40,
            color=YELLOW
        )
        question.move_to(2.5 * UP)
        self.play(Write(question))
        self.wait(2)

        # Set up the scene
        start_point = np.array([-4, 1, 0])
        end_point = np.array([4, -2, 0])

        start_dot = Dot(start_point, color=GREEN, radius=0.12)
        end_dot = Dot(end_point, color=RED, radius=0.12)

        start_label = Text("Start", font_size=28, color=GREEN)
        start_label.next_to(start_dot, UP)

        end_label = Text("Finish", font_size=28, color=RED)
        end_label.next_to(end_dot, DOWN)

        self.play(
            FadeIn(start_dot),
            FadeIn(end_dot),
            Write(start_label),
            Write(end_label)
        )
        self.wait()

        # Show different possible paths
        straight_line = Line(start_point, end_point, color=BLUE, stroke_width=4)
        straight_label = Text("Straight line?", font_size=32, color=BLUE)
        straight_label.move_to(DOWN * 2.5)

        self.play(Create(straight_line))
        self.wait(0.5)
        self.play(Write(straight_label))
        self.wait()

        # Steep then flat curve
        def steep_curve(t):
            # Quick drop then gentle slope
            x = start_point[0] + (end_point[0] - start_point[0]) * t
            y_start, y_end = start_point[1], end_point[1]
            # Make it drop fast initially
            y = y_start + (y_end - y_start) * (1.5 * t - 0.5 * t**2)
            return np.array([x, y, 0])

        steep_path = ParametricCurve(
            steep_curve,
            t_range=[0, 1],
            color=PURPLE,
            stroke_width=4
        )

        steep_label = Text("Steep drop first?", font_size=32, color=PURPLE)
        steep_label.move_to(DOWN * 2.5)

        self.play(
            ReplacementTransform(straight_line, steep_path),
            ReplacementTransform(straight_label, steep_label)
        )
        self.wait(2)

        # Show the mystery - what's optimal?
        mystery = Text("What is the optimal curve?", font_size=40, color=YELLOW)
        mystery.move_to(DOWN * 2.5)

        self.play(
            FadeOut(steep_path),
            ReplacementTransform(steep_label, mystery)
        )
        self.wait(2)


class CompareRamps(Scene):
    """
    Compare different ramp shapes and race balls down them.
    """

    def construct(self):
        # Title
        title = Text("Racing Different Paths", font_size=50)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait()

        # Define start and end points
        start = np.array([-5, 2, 0])
        end = np.array([5, -1.5, 0])

        # Create three different paths
        # 1. Straight line
        def straight_path(t):
            return start + t * (end - start)

        # 2. Circular arc (shallow)
        def arc_path(t):
            x = start[0] + t * (end[0] - start[0])
            # Quadratic curve
            progress = t
            y = start[1] + (end[1] - start[1]) * progress - 0.8 * progress * (1 - progress)
            return np.array([x, y, 0])

        # 3. Cycloid (optimal)
        def cycloid_path(t):
            # Parametric cycloid equations
            # Scaled and positioned to match start and end
            theta = t * 2.5  # Parameter for cycloid
            x = start[0] + (end[0] - start[0]) * (theta - 0.4 * np.sin(theta)) / 2.5
            y = start[1] + (end[1] - start[1]) * (1 - 0.5 * np.cos(theta)) / (1 - 0.5 * np.cos(2.5))
            return np.array([x, y, 0])

        # Create the curves
        straight = ParametricCurve(straight_path, t_range=[0, 1], color=BLUE, stroke_width=3)
        arc = ParametricCurve(arc_path, t_range=[0, 1], color=GREEN, stroke_width=3)
        cycloid = ParametricCurve(cycloid_path, t_range=[0, 1], color=RED, stroke_width=3)

        # Shift them vertically to separate
        straight.shift(UP * 1.5)
        arc.shift(UP * 0)
        cycloid.shift(DOWN * 1.5)

        # Labels
        straight_label = Text("Straight", font_size=28, color=BLUE).next_to(straight, LEFT)
        arc_label = Text("Circular Arc", font_size=28, color=GREEN).next_to(arc, LEFT)
        cycloid_label = Text("Cycloid", font_size=28, color=RED).next_to(cycloid, LEFT)

        # Draw all paths
        self.play(
            Create(straight),
            Create(arc),
            Create(cycloid),
            Write(straight_label),
            Write(arc_label),
            Write(cycloid_label)
        )
        self.wait()

        # Create balls
        ball_straight = Dot(straight.get_start(), color=BLUE, radius=0.08)
        ball_arc = Dot(arc.get_start(), color=GREEN, radius=0.08)
        ball_cycloid = Dot(cycloid.get_start(), color=RED, radius=0.08)

        self.play(
            FadeIn(ball_straight),
            FadeIn(ball_arc),
            FadeIn(ball_cycloid)
        )
        self.wait()

        # Race announcement
        announcement = Text("Ready... Set... Go!", font_size=40, color=YELLOW)
        announcement.to_edge(DOWN)
        self.play(Write(announcement))
        self.wait(0.5)
        self.play(FadeOut(announcement))

        # Animate the race with different timings
        # Cycloid is fastest, then arc, then straight
        self.play(
            MoveAlongPath(ball_straight, straight.copy().shift(DOWN * 1.5)),
            MoveAlongPath(ball_arc, arc.copy()),
            MoveAlongPath(ball_cycloid, cycloid.copy().shift(UP * 1.5)),
            run_time=3,
            rate_func=lambda t: smooth(t**0.5)  # Simulate acceleration
        )
        self.wait()

        # Highlight the winner
        winner = Text("Cycloid Wins!", font_size=48, color=RED)
        winner.to_edge(DOWN)
        self.play(Write(winner))

        # Flash the cycloid
        self.play(
            cycloid.animate.set_stroke(width=6),
            Flash(ball_cycloid, color=RED, flash_radius=0.3)
        )
        self.wait(2)


class CycloidSolution(Scene):
    """
    Show that the cycloid is the solution and explain what a cycloid is.
    """

    def construct(self):
        # Title
        title = Text("The Cycloid: Nature's Speed Demon", font_size=50)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait()

        # What is a cycloid?
        definition = Text("What is a cycloid?", font_size=40, color=YELLOW)
        definition.move_to(2 * UP)
        self.play(Write(definition))
        self.wait()

        explanation = Text(
            "The path traced by a point on a rolling circle",
            font_size=32,
            color=GREY
        )
        explanation.next_to(definition, DOWN)
        self.play(Write(explanation))
        self.wait(2)

        # Demonstrate cycloid generation
        # Create a line representing the ground
        ground = Line(LEFT * 7, RIGHT * 7, color=WHITE)
        ground.move_to(DOWN * 1)

        # Rolling circle
        radius = 0.8
        circle = Circle(radius=radius, color=BLUE)
        circle.move_to(LEFT * 5 + DOWN * 1 + UP * radius)

        # Point on the circle
        dot = Dot(circle.get_bottom(), color=RED, radius=0.08)

        # Path traced
        path_points = []

        self.play(Create(ground))
        self.play(Create(circle), FadeIn(dot))
        self.wait()

        # Animate rolling
        angle_tracker = ValueTracker(0)

        def update_circle(mob):
            angle = angle_tracker.get_value()
            # Move circle horizontally
            x_pos = -5 + radius * angle
            mob.move_to(np.array([x_pos, -1 + radius, 0]))

        def update_dot(mob):
            angle = angle_tracker.get_value()
            x_pos = -5 + radius * angle
            # Point rotates around circle
            x = x_pos - radius * np.sin(angle)
            y = -1 + radius * (1 - np.cos(angle))
            mob.move_to(np.array([x, y, 0]))
            path_points.append(np.array([x, y, 0]))

        circle.add_updater(update_circle)
        dot.add_updater(update_dot)

        # Create the traced path
        traced_path = VMobject(color=RED, stroke_width=3)
        traced_path.set_points_as_corners([dot.get_center(), dot.get_center()])

        def update_path(mob):
            if len(path_points) > 1:
                mob.set_points_as_corners(path_points)

        traced_path.add_updater(update_path)
        self.add(traced_path)

        # Roll the circle
        self.play(
            angle_tracker.animate.set_value(2 * PI),
            run_time=4,
            rate_func=linear
        )

        circle.clear_updaters()
        dot.clear_updaters()
        traced_path.clear_updaters()
        self.wait()

        # Show the parametric equations
        self.play(
            FadeOut(circle),
            FadeOut(dot),
            FadeOut(ground),
            FadeOut(definition),
            FadeOut(explanation)
        )

        equations_title = Text("Parametric Equations", font_size=40, color=YELLOW)
        equations_title.move_to(2 * UP)

        equations = Tex(
            R"x(\theta) &= r(\theta - \sin\theta) \\ y(\theta) &= r(1 - \cos\theta)",
            font_size=40
        )
        equations.next_to(equations_title, DOWN, buff=0.5)

        self.play(
            traced_path.animate.move_to(DOWN * 1.5).scale(0.8),
            Write(equations_title)
        )
        self.wait(0.5)
        self.play(Write(equations))
        self.wait(2)

        # Historical note
        historical = Text(
            "Solved by Johann Bernoulli (1696)",
            font_size=32,
            color=GREY
        )
        historical.to_edge(DOWN)
        self.play(Write(historical))
        self.wait(2)


class PhysicsExplanation(Scene):
    """
    Explain the physics behind why the cycloid is optimal.
    """

    def construct(self):
        # Title
        title = Text("Why is the Cycloid Fastest?", font_size=52)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait()

        # Key insight
        insight = Text("Key Insight: Trade height for speed early", font_size=36, color=YELLOW)
        insight.move_to(2.2 * UP)
        self.play(Write(insight))
        self.wait(2)

        # Energy considerations
        energy_title = Text("Energy Consideration", font_size=40, color=BLUE)
        energy_title.move_to(0.8 * UP)

        energy_eq = Tex(
            R"v = \sqrt{2gh}",
            font_size=44
        )
        energy_eq.next_to(energy_title, DOWN, buff=0.4)

        energy_note = Text(
            "Speed increases with height lost",
            font_size=28,
            color=GREY
        )
        energy_note.next_to(energy_eq, DOWN, buff=0.3)

        self.play(Write(energy_title))
        self.wait(0.5)
        self.play(Write(energy_eq))
        self.wait(0.5)
        self.play(Write(energy_note))
        self.wait(2)

        # Time minimization
        time_title = Text("Minimize Total Time", font_size=40, color=GREEN)
        time_title.move_to(1.2 * DOWN)

        time_eq = Tex(
            R"T = \int \frac{ds}{v} = \int \frac{\sqrt{1 + (y')^2}}{\ sqrt{2gy}} \, dx",
            font_size=36
        )
        time_eq.next_to(time_title, DOWN, buff=0.4)

        self.play(Write(time_title))
        self.wait(0.5)
        self.play(Write(time_eq))
        self.wait(2)

        # Calculus of variations
        self.play(
            FadeOut(insight),
            FadeOut(energy_title),
            FadeOut(energy_eq),
            FadeOut(energy_note),
            FadeOut(time_title),
            FadeOut(time_eq)
        )

        cov_title = Text("Calculus of Variations", font_size=48, color=YELLOW)
        cov_title.move_to(1.5 * UP)

        explanation = Text(
            "Find the function y(x) that minimizes the integral",
            font_size=32
        )
        explanation.next_to(cov_title, DOWN, buff=0.5)

        self.play(Write(cov_title))
        self.wait(0.5)
        self.play(Write(explanation))
        self.wait()

        # Euler-Lagrange equation
        el_eq = Tex(
            R"\frac{\partial F}{\partial y} - \frac{d}{dx}\frac{\partial F}{\partial y'} = 0",
            font_size=40
        )
        el_eq.move_to(DOWN * 0.2)

        el_label = Text("Euler-Lagrange Equation", font_size=28, color=GREY)
        el_label.next_to(el_eq, DOWN, buff=0.3)

        self.play(Write(el_eq))
        self.wait(0.5)
        self.play(Write(el_label))
        self.wait(2)

        # Result
        result_box = Rectangle(height=1.5, width=10, color=YELLOW)
        result_box.move_to(DOWN * 2.3)

        result_text = Text("Solution: Cycloid Curve", font_size=40, color=YELLOW)
        result_text.move_to(result_box.get_center())

        self.play(Create(result_box))
        self.play(Write(result_text))
        self.wait(2)

        # Final note
        note = Text(
            "Also called the 'tautochrone' - same descent time from any starting point!",
            font_size=28,
            color=GREY
        )
        note.to_edge(DOWN)
        self.play(Write(note))
        self.wait(3)


# Utility functions for brachistochrone curves

def cycloid_parametric(theta, r=1, offset=(0, 0)):
    """
    Generate cycloid curve from parametric equations.

    Args:
        theta: Parameter (typically 0 to 2π for one arch)
        r: Radius of the generating circle
        offset: (x, y) offset for positioning

    Returns:
        (x, y) coordinates on the cycloid
    """
    x = r * (theta - np.sin(theta)) + offset[0]
    y = r * (1 - np.cos(theta)) + offset[1]
    return x, y


def cycloid_arc_length(theta, r=1):
    """
    Compute arc length along cycloid from 0 to theta.

    Args:
        theta: Parameter value
        r: Radius of generating circle

    Returns:
        Arc length from 0 to theta
    """
    # Arc length formula for cycloid: s = 4r(1 - cos(theta/2))
    return 4 * r * (1 - np.cos(theta / 2))


def descent_time_numerical(y_func, x_range, num_points=1000, g=9.8):
    """
    Numerically compute descent time for a given curve.

    Args:
        y_func: Function y(x) describing the curve
        x_range: (x_start, x_end) range
        num_points: Number of points for numerical integration
        g: Gravitational acceleration

    Returns:
        Total descent time
    """
    x = np.linspace(x_range[0], x_range[1], num_points)
    y = np.array([y_func(xi) for xi in x])

    # Compute derivatives
    dx = x[1] - x[0]
    dy = np.gradient(y, dx)

    # Initial height
    y0 = y[0]

    # Speed at each point from energy conservation: v = sqrt(2g(y0 - y))
    # Handle the starting point specially
    heights_dropped = y0 - y
    heights_dropped[0] = dx  # Avoid division by zero at start

    speeds = np.sqrt(2 * g * heights_dropped)
    speeds[0] = np.sqrt(2 * g * dx)  # Initial speed

    # Arc length elements
    ds = np.sqrt(1 + dy**2) * dx

    # Time elements
    dt = ds / speeds

    # Total time
    total_time = np.sum(dt)

    return total_time


def compare_descent_times(curves, x_range=(0, 10), g=9.8):
    """
    Compare descent times for multiple curves.

    Args:
        curves: Dictionary of {name: y_func} for different curves
        x_range: (x_start, x_end) range
        g: Gravitational acceleration

    Returns:
        Dictionary of {name: time} for each curve
    """
    times = {}
    for name, y_func in curves.items():
        times[name] = descent_time_numerical(y_func, x_range, g=g)
    return times
