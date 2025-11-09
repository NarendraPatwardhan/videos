"""
Natural Group Name: Gradient Descent Optimization

Educational Objectives:
- To visualize gradient descent as a ball rolling down a surface
- To demonstrate how the gradient points in the direction of steepest ascent
- To show the iterative nature of the optimization process
- To illustrate the effect of learning rate and local minima

Story Arc & Intent:
The animation reveals gradient descent through the physical analogy of a ball
rolling downhill. This transforms the abstract optimization algorithm into an
intuitive process of following the slope to find the lowest point.

Narrative Flow:
- Hook/Opening: A loss landscape and the challenge of finding the minimum
- Development: The gradient as the direction of steepest ascent
- Build-up: Iterative steps following negative gradient
- Climax: Convergence to minimum and role of learning rate
- Resolution: Connection to machine learning and local minima issue

Technical Implementation Notes:
- Scene Classes: IntroduceLoss, GradientDirection, IterativeSteps, LocalMinima
- Key Visual Elements: 3D surfaces, contour plots, gradient vectors, paths
- Animation Techniques: Surface plots, vector fields, iterative animation
- Mathematical Concepts: Gradients, optimization, learning rate, convergence

Dependency Chain:
All scenes use basic manimlib components: Axes, graphs, arrows, text.
No custom utilities required beyond helper functions defined in this file.

Rendering Instructions:
To render these scenes, use the manim command-line tool:
- For a single scene: manimgl gradient_descent.py IntroduceLoss
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
# - BLUE: Loss function surface/curve
# - YELLOW: Current position during optimization
# - GREEN: Gradient vectors and path
# - RED: Minimum point
# - WHITE: Axes and grid
# - GREY_A: De-emphasized elements
#
# Key Manim Constants Used:
# - UP, DOWN, LEFT, RIGHT: Direction vectors
# - ORIGIN: Center point
# - PI: π for mathematical functions
# - MED_SMALL_BUFF: Spacing

# Loss function: simple quadratic bowl
def loss_function(x, y):
    """
    A simple quadratic loss function (bowl shape).

    Args:
        x, y: Coordinates

    Returns:
        Loss value
    """
    return x**2 + y**2

def loss_1d(x):
    """
    1D loss function for visualization.

    Args:
        x: Input value

    Returns:
        Loss value
    """
    return (x - 1)**2 + 0.5

def loss_gradient_1d(x):
    """
    Gradient of 1D loss function.

    Args:
        x: Input value

    Returns:
        Gradient value
    """
    return 2 * (x - 1)

# ============================================================
# 3. UTILITY FUNCTIONS
# ============================================================

def compute_gradient_2d(x, y, epsilon=0.001):
    """
    Numerically compute gradient of loss function.

    Args:
        x, y: Point to compute gradient at
        epsilon: Small value for numerical derivative

    Returns:
        Tuple (grad_x, grad_y)
    """
    grad_x = (loss_function(x + epsilon, y) - loss_function(x - epsilon, y)) / (2 * epsilon)
    grad_y = (loss_function(x, y + epsilon) - loss_function(x, y - epsilon)) / (2 * epsilon)

    return grad_x, grad_y

def gradient_descent_step(x, y, learning_rate=0.1):
    """
    Perform one step of gradient descent.

    Args:
        x, y: Current position
        learning_rate: Step size

    Returns:
        Tuple (new_x, new_y)
    """
    grad_x, grad_y = compute_gradient_2d(x, y)

    new_x = x - learning_rate * grad_x
    new_y = y - learning_rate * grad_y

    return new_x, new_y

def create_contour_plot(axes, func, levels=10, color=BLUE, **kwargs):
    """
    Create a simple contour representation using circles.

    Args:
        axes: Axes object
        func: Function to plot
        levels: Number of contour levels
        color: Color of contours
        **kwargs: Additional arguments

    Returns:
        VGroup of contour lines
    """
    contours = VGroup()

    for i in range(1, levels + 1):
        radius = i * 0.5
        circle = Circle(radius=radius, color=color, stroke_width=1, stroke_opacity=0.3)
        circle.move_to(axes.c2p(0, 0))
        contours.add(circle)

    return contours

# ============================================================
# 4. SCENE CLASSES
# ============================================================

class IntroduceLoss(Scene):
    """
    Scene 1: Introduce the concept of a loss landscape.

    This scene presents a loss function and poses the optimization problem:
    how do we find the minimum?
    """

    def construct(self):
        # ========================================
        # TITLE
        # ========================================
        title = Text("Gradient Descent Optimization", font_size=48)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait()

        # ========================================
        # SETUP: Create axes and loss function
        # ========================================
        axes = Axes(
            x_range=[-1, 4, 1],
            y_range=[-0.5, 4, 1],
            width=10,
            height=6,
        )
        axes.shift(DOWN * 0.5)

        self.play(ShowCreation(axes))
        self.wait()

        # Loss function graph
        loss_graph = axes.get_graph(
            loss_1d,
            x_range=(-0.5, 3.5),
            color=BLUE,
            stroke_width=4
        )

        loss_label = Tex("L(\\theta) = \\text{Loss Function}", color=BLUE, font_size=32)
        loss_label.next_to(axes, UP, buff=0.3).to_edge(LEFT)

        self.play(ShowCreation(loss_graph), Write(loss_label))
        self.wait()

        # ========================================
        # GOAL: Find the minimum
        # ========================================
        goal = Text(
            "Goal: Find θ that minimizes L(θ)",
            font_size=32,
            color=WHITE
        )
        goal.to_edge(DOWN).shift(UP * 0.3)

        self.play(FadeIn(goal, shift=UP))
        self.wait()

        # Mark the minimum
        min_x = 1.0
        min_y = loss_1d(min_x)
        min_point = axes.c2p(min_x, min_y)

        min_dot = Dot(min_point, color=RED, radius=0.08)
        min_label = Tex("\\theta^*", color=RED, font_size=28)
        min_label.next_to(min_dot, DOWN, buff=0.2)

        self.play(FadeIn(min_dot, scale=0.5))
        self.play(Write(min_label))
        self.wait()

        # ========================================
        # CHALLENGE: How to find it?
        # ========================================
        self.play(FadeOut(goal))

        challenge = Text(
            "But we don't know where the minimum is!",
            font_size=28,
            color=GREY_A
        )
        challenge.to_edge(DOWN).shift(UP * 0.3)

        self.play(FadeIn(challenge, shift=UP))
        self.wait()

        # Show random starting point
        start_x = 3.0
        start_y = loss_1d(start_x)
        start_point = axes.c2p(start_x, start_y)

        start_dot = Dot(start_point, color=YELLOW, radius=0.08)
        start_label = Tex("\\theta_0", color=YELLOW, font_size=28)
        start_label.next_to(start_dot, UP, buff=0.2)

        self.play(FadeIn(start_dot, scale=0.5))
        self.play(Write(start_label))
        self.wait()

        # ========================================
        # IDEA: Follow the slope
        # ========================================
        self.play(FadeOut(challenge))

        idea = Text(
            "Idea: Follow the slope downhill!",
            font_size=32,
            color=GREEN
        )
        idea.to_edge(DOWN).shift(UP * 0.3)

        self.play(FadeIn(idea, shift=UP))
        self.wait(2)


class GradientDirection(Scene):
    """
    Scene 2: Show that the gradient points uphill (steepest ascent).

    This scene visualizes the gradient as a vector field and shows that
    we need to go in the OPPOSITE direction to descend.
    """

    def construct(self):
        # ========================================
        # TITLE
        # ========================================
        title = Text("The Gradient Direction", font_size=42)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait()

        # ========================================
        # SETUP: 2D contour plot
        # ========================================
        axes = Axes(
            x_range=[-3, 3, 1],
            y_range=[-3, 3, 1],
            width=8,
            height=8,
        )

        self.play(ShowCreation(axes))
        self.wait()

        # Contour lines
        contours = create_contour_plot(axes, loss_function, levels=8, color=BLUE)
        self.play(ShowCreation(contours))
        self.wait()

        # Center (minimum)
        center_dot = Dot(axes.c2p(0, 0), color=RED, radius=0.08)
        center_label = Tex("\\text{min}", color=RED, font_size=24)
        center_label.next_to(center_dot, DOWN, buff=0.2)

        self.play(FadeIn(center_dot, scale=0.5), Write(center_label))
        self.wait()

        # ========================================
        # GRADIENT VECTORS
        # ========================================
        explanation = Text(
            "Gradient points in direction of steepest ASCENT",
            font_size=28,
            color=GREEN
        )
        explanation.to_edge(DOWN).shift(UP * 0.3)

        self.play(FadeIn(explanation, shift=UP))
        self.wait()

        # Show several gradient vectors
        gradient_points = [
            (2, 1),
            (-1.5, 1.5),
            (1, -2),
            (-2, -1),
        ]

        gradient_arrows = VGroup()

        for x, y in gradient_points:
            point = axes.c2p(x, y)
            grad_x, grad_y = compute_gradient_2d(x, y)

            # Normalize and scale for visualization
            mag = np.sqrt(grad_x**2 + grad_y**2)
            if mag > 0:
                grad_x /= mag
                grad_y /= mag

            scale = 0.6
            end_point = axes.c2p(x + scale * grad_x, y + scale * grad_y)

            arrow = Arrow(
                point, end_point,
                color=GREEN,
                buff=0,
                stroke_width=3,
                tip_length=0.15
            )
            gradient_arrows.add(arrow)

        self.play(LaggedStart(*[GrowArrow(arrow) for arrow in gradient_arrows], lag_ratio=0.2))
        self.wait()

        # ========================================
        # NEGATIVE GRADIENT
        # ========================================
        self.play(FadeOut(explanation))

        negative_explanation = Text(
            "So we go in the NEGATIVE gradient direction",
            font_size=28,
            color=YELLOW
        )
        negative_explanation.to_edge(DOWN).shift(UP * 0.3)

        self.play(FadeIn(negative_explanation, shift=UP))
        self.wait()

        # Show negative gradient arrows
        neg_gradient_arrows = VGroup()

        for x, y in gradient_points:
            point = axes.c2p(x, y)
            grad_x, grad_y = compute_gradient_2d(x, y)

            # Normalize and scale, but negative
            mag = np.sqrt(grad_x**2 + grad_y**2)
            if mag > 0:
                grad_x /= mag
                grad_y /= mag

            scale = 0.6
            end_point = axes.c2p(x - scale * grad_x, y - scale * grad_y)

            arrow = Arrow(
                point, end_point,
                color=YELLOW,
                buff=0,
                stroke_width=3,
                tip_length=0.15
            )
            neg_gradient_arrows.add(arrow)

        self.play(
            *[Transform(gradient_arrows[i], neg_gradient_arrows[i])
              for i in range(len(gradient_arrows))]
        )
        self.wait()

        # ========================================
        # FORMULA
        # ========================================
        self.play(FadeOut(negative_explanation))

        formula = Tex(
            "\\theta_{\\text{new}} = \\theta_{\\text{old}} - \\alpha \\nabla L(\\theta)",
            font_size=36
        )
        formula.to_edge(DOWN).shift(UP * 0.3)

        self.play(Write(formula))
        self.wait()

        # Label components
        alpha_label = Tex("\\alpha = \\text{learning rate}", font_size=24, color=GREY_A)
        alpha_label.next_to(formula, DOWN, buff=0.2)

        self.play(Write(alpha_label))
        self.wait(2)


class IterativeSteps(Scene):
    """
    Scene 3: Show the iterative process of gradient descent.

    This scene animates the step-by-step descent from a starting point
    to the minimum, showing how the learning rate affects convergence.
    """

    def construct(self):
        # ========================================
        # TITLE
        # ========================================
        title = Text("Iterative Descent", font_size=42)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait()

        # ========================================
        # SETUP: Loss function
        # ========================================
        axes = Axes(
            x_range=[-1, 4, 1],
            y_range=[-0.5, 4, 1],
            width=10,
            height=6,
        )
        axes.shift(DOWN * 0.5)

        loss_graph = axes.get_graph(
            loss_1d,
            x_range=(-0.5, 3.5),
            color=BLUE,
            stroke_width=4
        )

        self.add(axes, loss_graph)
        self.wait()

        # ========================================
        # GRADIENT DESCENT ANIMATION
        # ========================================
        # Starting point
        theta = 3.5
        learning_rate = 0.3

        # Track path
        path_points = [axes.c2p(theta, loss_1d(theta))]

        # Current position dot
        current_dot = Dot(path_points[0], color=YELLOW, radius=0.08)
        self.play(FadeIn(current_dot, scale=0.5))
        self.wait()

        # Perform steps
        num_steps = 15

        for step in range(num_steps):
            # Show gradient at current position
            gradient = loss_gradient_1d(theta)

            # Gradient arrow
            current_point = axes.c2p(theta, loss_1d(theta))
            gradient_direction = -1 if gradient > 0 else 1
            gradient_end = axes.c2p(theta + gradient_direction * 0.3, loss_1d(theta))

            gradient_arrow = Arrow(
                current_point,
                gradient_end,
                color=GREEN,
                buff=0,
                stroke_width=2,
                tip_length=0.1
            )

            if step < 3:  # Only show gradient arrows for first few steps
                self.play(GrowArrow(gradient_arrow))
                self.wait(0.3)

            # Update theta
            theta_new = theta - learning_rate * gradient

            # New position
            new_point = axes.c2p(theta_new, loss_1d(theta_new))
            path_points.append(new_point)

            # Animate movement
            self.play(
                current_dot.animate.move_to(new_point),
                FadeOut(gradient_arrow) if step < 3 else Wait(0.1),
                run_time=0.5
            )

            theta = theta_new

            # Stop if converged
            if abs(gradient) < 0.01:
                break

        self.wait()

        # ========================================
        # SHOW PATH
        # ========================================
        path = VMobject(color=YELLOW, stroke_width=2)
        path.set_points_smoothly([p for p in path_points])

        self.play(ShowCreation(path))
        self.wait()

        # ========================================
        # CONVERGENCE
        # ========================================
        convergence = Text(
            "Converged to minimum!",
            font_size=32,
            color=GREEN
        )
        convergence.to_edge(DOWN).shift(UP * 0.3)

        self.play(FadeIn(convergence, shift=UP))
        self.wait()

        # Final value
        final_value = Tex(
            f"\\theta^* \\approx {theta:.3f}",
            font_size=28,
            color=YELLOW
        )
        final_value.next_to(convergence, DOWN, buff=0.2)

        self.play(Write(final_value))
        self.wait(2)


class LocalMinima(Scene):
    """
    Scene 4: Illustrate the challenge of local minima.

    This scene shows that gradient descent can get stuck in local minima
    and discusses the connection to neural network training.
    """

    def construct(self):
        # ========================================
        # TITLE
        # ========================================
        title = Text("Local Minima Challenge", font_size=42)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait()

        # ========================================
        # SETUP: Function with local minimum
        # ========================================
        def complex_loss(x):
            return 0.1 * (x - 1)**4 - 0.5 * (x - 1)**2 + 0.5 * np.sin(3 * x) + 1

        axes = Axes(
            x_range=[-1, 3, 1],
            y_range=[-1, 3, 1],
            width=10,
            height=6,
        )
        axes.shift(DOWN * 0.5)

        complex_graph = axes.get_graph(
            complex_loss,
            x_range=(-0.5, 2.5),
            color=BLUE,
            stroke_width=4
        )

        self.play(ShowCreation(axes))
        self.play(ShowCreation(complex_graph))
        self.wait()

        # ========================================
        # MARK LOCAL AND GLOBAL MINIMA
        # ========================================
        # Local minimum (approximate)
        local_min_x = 0.5
        local_min_point = axes.c2p(local_min_x, complex_loss(local_min_x))

        local_min_dot = Dot(local_min_point, color=YELLOW, radius=0.08)
        local_min_label = Text("Local\nMinimum", font_size=20, color=YELLOW)
        local_min_label.next_to(local_min_dot, DOWN, buff=0.2)

        # Global minimum (approximate)
        global_min_x = 1.8
        global_min_point = axes.c2p(global_min_x, complex_loss(global_min_x))

        global_min_dot = Dot(global_min_point, color=GREEN, radius=0.08)
        global_min_label = Text("Global\nMinimum", font_size=20, color=GREEN)
        global_min_label.next_to(global_min_dot, DOWN, buff=0.2)

        self.play(
            FadeIn(local_min_dot, scale=0.5),
            Write(local_min_label)
        )
        self.wait()

        self.play(
            FadeIn(global_min_dot, scale=0.5),
            Write(global_min_label)
        )
        self.wait()

        # ========================================
        # PROBLEM: Can get stuck
        # ========================================
        problem = Text(
            "Gradient descent can get stuck in local minima",
            font_size=28,
            color=RED
        )
        problem.to_edge(DOWN).shift(UP * 1.2)

        self.play(FadeIn(problem, shift=UP))
        self.wait()

        # Show getting stuck
        stuck_start = axes.c2p(0.3, complex_loss(0.3))
        stuck_dot = Dot(stuck_start, color=RED, radius=0.08)

        self.play(FadeIn(stuck_dot, scale=0.5))
        self.wait()

        # Animate to local minimum
        self.play(stuck_dot.animate.move_to(local_min_point), run_time=2)
        self.wait()

        # ========================================
        # SOLUTIONS
        # ========================================
        self.play(FadeOut(problem))

        solutions = VGroup(
            Text("Solutions:", font_size=28, color=WHITE),
            Text("• Random restarts", font_size=22),
            Text("• Momentum methods", font_size=22),
            Text("• Stochastic gradient descent", font_size=22),
            Text("• Adaptive learning rates", font_size=22),
        )
        solutions.arrange(DOWN, buff=0.2, aligned_edge=LEFT)
        solutions.to_edge(DOWN).shift(UP * 0.3)

        for item in solutions:
            self.play(FadeIn(item, shift=UP))
            self.wait(0.4)

        self.wait()

        # ========================================
        # NEURAL NETWORKS CONNECTION
        # ========================================
        self.play(FadeOut(solutions), FadeOut(stuck_dot))

        connection = VGroup(
            Text("In Neural Networks:", font_size=32, color=YELLOW),
            Tex("\\text{Loss} = L(w_1, w_2, \\ldots, w_n)", font_size=28),
            Text("Millions of parameters!", font_size=24, color=GREY_A),
            Tex("\\nabla L = \\left(\\frac{\\partial L}{\\partial w_1}, \\frac{\\partial L}{\\partial w_2}, \\ldots\\right)", font_size=24),
            Text("Backpropagation computes this gradient", font_size=24),
        )
        connection.arrange(DOWN, buff=0.3)
        connection.to_edge(DOWN).shift(UP * 0.3)

        for item in connection:
            self.play(FadeIn(item, shift=UP))
            self.wait(0.5)

        self.wait(2)


# ============================================================
# 5. SCENE SUMMARY AND EXECUTION ORDER
# ============================================================
#
# Scene 1 (IntroduceLoss):
#   - Introduces the loss function landscape
#   - Poses the optimization problem
#   - Shows starting point and goal (minimum)
#
# Scene 2 (GradientDirection):
#   - Visualizes gradient as direction of steepest ascent
#   - Shows that we go in negative gradient direction
#   - Presents the update formula θ_new = θ_old - α∇L
#
# Scene 3 (IterativeSteps):
#   - Animates iterative gradient descent steps
#   - Shows convergence to minimum
#   - Illustrates the path taken
#
# Scene 4 (LocalMinima):
#   - Demonstrates the local minima problem
#   - Shows that descent can get stuck
#   - Discusses solutions and connection to neural networks

SCENE_ORDER = [
    IntroduceLoss,         # Part 1: The optimization problem
    GradientDirection,     # Part 2: Understanding the gradient
    IterativeSteps,        # Part 3: The iterative process
    LocalMinima,           # Part 4: Challenges and applications
]
