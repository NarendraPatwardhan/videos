"""
Least Squares Linear Regression

This module demonstrates the least squares method for linear regression.
Shows how to fit a line to scattered data by minimizing the sum of squared errors,
including geometric interpretation and the normal equation.

Scenes:
    - IntroduceProblem: Introduction to fitting lines to data
    - ErrorMinimization: Understanding error and minimization
    - NormalEquation: Deriving the normal equation
    - BestFitLine: Computing and visualizing the best fit line
"""

from manimlib import *
import numpy as np


class IntroduceProblem(Scene):
    """
    Introduce the problem of fitting a line to scattered data points.
    """

    def construct(self):
        # Title
        title = Text("Least Squares Linear Regression", font_size=50)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait()

        # The problem
        problem = Text(
            "Given data points, find the best-fitting line",
            font_size=36,
            color=YELLOW
        )
        problem.move_to(UP * 2.5)
        self.play(Write(problem))
        self.wait(2)

        # Create axes
        axes = Axes(
            x_range=[0, 10, 1],
            y_range=[0, 10, 1],
            height=6,
            width=8,
            axis_config={"include_tip": False}
        )
        axes.move_to(DOWN * 0.3)

        x_label = Text("x", font_size=32).next_to(axes.x_axis, RIGHT)
        y_label = Text("y", font_size=32).next_to(axes.y_axis, UP)

        self.play(Create(axes), Write(x_label), Write(y_label))
        self.wait()

        # Sample data points (roughly linear with noise)
        np.random.seed(42)
        x_data = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9])
        y_data = 1.5 * x_data + 2 + np.random.normal(0, 0.8, len(x_data))

        # Plot points
        points = VGroup(*[
            Dot(axes.c2p(x, y), color=BLUE, radius=0.08)
            for x, y in zip(x_data, y_data)
        ])

        self.play(LaggedStart(*[FadeIn(point) for point in points], lag_ratio=0.15))
        self.wait()

        # Show different possible lines
        line1 = axes.get_graph(lambda x: 1.2 * x + 1, x_range=[0, 10], color=RED)
        line1_label = Text("Line 1?", font_size=28, color=RED).move_to(axes.c2p(8, 8))

        self.play(Create(line1), Write(line1_label))
        self.wait()

        line2 = axes.get_graph(lambda x: 1.8 * x + 1.5, x_range=[0, 10], color=GREEN)
        line2_label = Text("Line 2?", font_size=28, color=GREEN).move_to(axes.c2p(7, 9))

        self.play(
            ReplacementTransform(line1, line2),
            ReplacementTransform(line1_label, line2_label)
        )
        self.wait()

        line3 = axes.get_graph(lambda x: 1.5 * x + 2.2, x_range=[0, 10], color=PURPLE)
        line3_label = Text("Line 3?", font_size=28, color=PURPLE).move_to(axes.c2p(6.5, 8.5))

        self.play(
            ReplacementTransform(line2, line3),
            ReplacementTransform(line2_label, line3_label)
        )
        self.wait()

        # Question
        question = Text(
            "Which line is \"best\"?",
            font_size=40,
            color=YELLOW
        )
        question.to_edge(DOWN)
        self.play(Write(question))
        self.wait(2)


class ErrorMinimization(Scene):
    """
    Explain the concept of error and why we minimize squared errors.
    """

    def construct(self):
        # Title
        title = Text("Minimizing Error", font_size=52)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait()

        # Setup
        axes = Axes(
            x_range=[0, 6, 1],
            y_range=[0, 8, 1],
            height=5,
            width=7,
            axis_config={"include_tip": False}
        )
        axes.move_to(LEFT * 2.5 + DOWN * 0.5)

        # Sample points
        data_points = [
            (1, 3),
            (2, 3.5),
            (3, 5),
            (4, 5.5),
            (5, 7)
        ]

        points = VGroup(*[
            Dot(axes.c2p(x, y), color=BLUE, radius=0.1)
            for x, y in data_points
        ])

        # A candidate line: y = 1.2x + 1.5
        line = axes.get_graph(lambda x: 1.2 * x + 1.5, x_range=[0, 6], color=YELLOW)

        self.play(Create(axes))
        self.play(LaggedStart(*[FadeIn(point) for point in points], lag_ratio=0.2))
        self.wait(0.5)
        self.play(Create(line))
        self.wait()

        # Show errors (vertical distances)
        error_lines = VGroup()
        for x, y in data_points:
            y_pred = 1.2 * x + 1.5
            error_line = DashedLine(
                axes.c2p(x, y),
                axes.c2p(x, y_pred),
                color=RED,
                stroke_width=2
            )
            error_lines.add(error_line)

        error_label = Text("Errors (residuals)", font_size=28, color=RED)
        error_label.move_to(axes.c2p(5.5, 2))

        self.play(LaggedStart(*[Create(error) for error in error_lines], lag_ratio=0.2))
        self.wait(0.5)
        self.play(Write(error_label))
        self.wait(2)

        # Explanation on the right
        explanation_title = Text("Why Squared Errors?", font_size=36, color=YELLOW)
        explanation_title.move_to(UP * 2 + RIGHT * 3.5)
        self.play(Write(explanation_title))
        self.wait()

        reasons = VGroup(
            Text("1. Makes errors positive", font_size=26),
            Text("   (avoid cancellation)", font_size=22, color=GREY),
            Text("2. Penalizes large errors more", font_size=26),
            Text("   (outliers have bigger impact)", font_size=22, color=GREY),
            Text("3. Mathematically convenient", font_size=26),
            Text("   (differentiable, unique solution)", font_size=22, color=GREY),
        )
        reasons.arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        reasons.next_to(explanation_title, DOWN, buff=0.5, aligned_edge=LEFT)

        self.play(LaggedStart(*[Write(reason) for reason in reasons], lag_ratio=0.3))
        self.wait(3)

        # Objective function
        self.play(
            FadeOut(error_label),
            FadeOut(reasons)
        )

        objective_title = Text("Objective:", font_size=32, color=GREEN)
        objective_title.move_to(UP * 1.5 + RIGHT * 3.5)
        self.play(Write(objective_title))
        self.wait()

        objective = Tex(
            R"\text{Minimize: } S = \sum_{i=1}^{n} (y_i - \hat{y}_i)^2",
            font_size=36
        )
        objective.next_to(objective_title, DOWN, buff=0.4)
        self.play(Write(objective))
        self.wait()

        # Where hat{y}_i is the predicted value
        prediction = Tex(
            R"\hat{y}_i = mx_i + b",
            font_size=32,
            color=BLUE
        )
        prediction.next_to(objective, DOWN, buff=0.5)
        self.play(Write(prediction))
        self.wait()

        # So we're finding m and b
        goal = Text("Find optimal slope m and intercept b", font_size=28, color=YELLOW)
        goal.next_to(prediction, DOWN, buff=0.5)
        self.play(Write(goal))
        self.wait(3)


class NormalEquation(Scene):
    """
    Derive the normal equation for least squares.
    """

    def construct(self):
        # Title
        title = Text("The Normal Equation", font_size=52)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait()

        # Matrix formulation
        matrix_title = Text("Matrix Formulation:", font_size=36, color=YELLOW)
        matrix_title.move_to(UP * 2.5)
        self.play(Write(matrix_title))
        self.wait()

        # Data in matrix form
        data_eq = Tex(
            R"\mathbf{y} = \mathbf{X}\boldsymbol{\beta} + \boldsymbol{\epsilon}",
            font_size=40
        )
        data_eq.move_to(UP * 1.5)
        self.play(Write(data_eq))
        self.wait()

        # Explain components
        components = VGroup(
            Tex(R"\mathbf{y}: \text{ observed values } (n \times 1)", font_size=28),
            Tex(R"\mathbf{X}: \text{ design matrix } (n \times 2)", font_size=28),
            Tex(R"\boldsymbol{\beta} = \begin{bmatrix} b \\ m \end{bmatrix}: \text{ parameters}", font_size=28),
            Tex(R"\boldsymbol{\epsilon}: \text{ errors}", font_size=28)
        )
        components.arrange(DOWN, aligned_edge=LEFT, buff=0.35)
        components.move_to(UP * 0.1 + LEFT * 1.5)

        self.play(LaggedStart(*[Write(comp) for comp in components], lag_ratio=0.3))
        self.wait(2)

        # Design matrix structure
        X_structure = Tex(
            R"\mathbf{X} = \begin{bmatrix} 1 & x_1 \\ 1 & x_2 \\ \vdots & \vdots \\ 1 & x_n \end{bmatrix}",
            font_size=36
        )
        X_structure.move_to(DOWN * 0.3 + RIGHT * 3.5)
        self.play(Write(X_structure))
        self.wait(2)

        # Objective: minimize ||y - Xβ||²
        self.play(
            FadeOut(components),
            FadeOut(X_structure)
        )

        objective = Tex(
            R"\text{Minimize: } ||\mathbf{y} - \mathbf{X}\boldsymbol{\beta}||^2",
            font_size=40,
            color=BLUE
        )
        objective.move_to(UP * 0.3)
        self.play(Write(objective))
        self.wait()

        # Take derivative and set to zero
        step1 = Text("Take derivative with respect to β and set to 0:", font_size=28)
        step1.next_to(objective, DOWN, buff=0.6)
        self.play(Write(step1))
        self.wait()

        derivative = Tex(
            R"\frac{\partial}{\partial \boldsymbol{\beta}} ||\mathbf{y} - \mathbf{X}\boldsymbol{\beta}||^2 = -2\mathbf{X}^T(\mathbf{y} - \mathbf{X}\boldsymbol{\beta}) = 0",
            font_size=32
        )
        derivative.next_to(step1, DOWN, buff=0.4)
        self.play(Write(derivative))
        self.wait(2)

        # Solve for β
        self.play(FadeOut(step1), FadeOut(derivative))

        step2 = Text("Solve for β:", font_size=28)
        step2.move_to(DOWN * 0.5)
        self.play(Write(step2))
        self.wait()

        solution_steps = VGroup(
            Tex(R"\mathbf{X}^T \mathbf{y} = \mathbf{X}^T \mathbf{X} \boldsymbol{\beta}", font_size=36),
            Tex(R"\boldsymbol{\beta} = (\mathbf{X}^T \mathbf{X})^{-1} \mathbf{X}^T \mathbf{y}", font_size=40, color=GREEN)
        )
        solution_steps.arrange(DOWN, buff=0.5)
        solution_steps.next_to(step2, DOWN, buff=0.4)

        self.play(Write(solution_steps[0]))
        self.wait()
        self.play(Write(solution_steps[1]))
        self.wait()

        # Highlight the normal equation
        box = SurroundingRectangle(solution_steps[1], color=YELLOW, buff=0.2)
        self.play(Create(box))
        self.wait()

        label = Text("The Normal Equation", font_size=32, color=YELLOW)
        label.next_to(box, DOWN, buff=0.3)
        self.play(Write(label))
        self.wait(3)


class BestFitLine(Scene):
    """
    Compute and visualize the best fit line for sample data.
    """

    def construct(self):
        # Title
        title = Text("Computing the Best Fit Line", font_size=50)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait()

        # Create axes
        axes = Axes(
            x_range=[0, 10, 1],
            y_range=[0, 12, 2],
            height=6,
            width=8,
            axis_config={"include_tip": False}
        )
        axes.move_to(LEFT * 2 + DOWN * 0.5)

        x_label = Text("x", font_size=32).next_to(axes.x_axis, RIGHT)
        y_label = Text("y", font_size=32).next_to(axes.y_axis, UP)

        self.play(Create(axes), Write(x_label), Write(y_label))
        self.wait()

        # Sample data
        np.random.seed(42)
        x_data = np.array([1, 2, 3, 4, 5, 6, 7, 8])
        y_data = 1.5 * x_data + 2 + np.random.normal(0, 0.7, len(x_data))

        # Plot points
        points = VGroup(*[
            Dot(axes.c2p(x, y), color=BLUE, radius=0.09)
            for x, y in zip(x_data, y_data)
        ])

        self.play(LaggedStart(*[FadeIn(point) for point in points], lag_ratio=0.15))
        self.wait()

        # Show the calculation on the right
        calc_title = Text("Calculation:", font_size=32, color=YELLOW)
        calc_title.move_to(UP * 2.5 + RIGHT * 4.5)
        self.play(Write(calc_title))
        self.wait()

        # Build X matrix
        X_label = Tex(
            R"\mathbf{X} = \begin{bmatrix} 1 & 1 \\ 1 & 2 \\ \vdots & \vdots \\ 1 & 8 \end{bmatrix}",
            font_size=28
        )
        X_label.move_to(UP * 1.3 + RIGHT * 3.8)
        self.play(Write(X_label))
        self.wait()

        # y vector
        y_label = Tex(
            R"\mathbf{y} = \begin{bmatrix} y_1 \\ y_2 \\ \vdots \\ y_8 \end{bmatrix}",
            font_size=28
        )
        y_label.next_to(X_label, RIGHT, buff=0.8)
        self.play(Write(y_label))
        self.wait()

        # Apply formula
        self.play(FadeOut(X_label), FadeOut(y_label))

        formula = Tex(
            R"\boldsymbol{\beta} = (\mathbf{X}^T \mathbf{X})^{-1} \mathbf{X}^T \mathbf{y}",
            font_size=32
        )
        formula.move_to(UP * 1.5 + RIGHT * 4.5)
        self.play(Write(formula))
        self.wait()

        # Compute least squares solution
        X = np.column_stack([np.ones(len(x_data)), x_data])
        beta = np.linalg.inv(X.T @ X) @ X.T @ y_data
        b, m = beta

        # Show result
        result = Tex(
            f"m \\approx {m:.2f}, \\quad b \\approx {b:.2f}",
            font_size=36,
            color=GREEN
        )
        result.next_to(formula, DOWN, buff=0.5)
        self.play(Write(result))
        self.wait()

        # Equation of line
        line_eq = Tex(
            f"y = {m:.2f}x + {b:.2f}",
            font_size=40,
            color=GREEN
        )
        line_eq.next_to(result, DOWN, buff=0.5)
        self.play(Write(line_eq))
        self.wait()

        # Draw the best fit line
        best_fit = axes.get_graph(
            lambda x: m * x + b,
            x_range=[0.5, 8.5],
            color=GREEN,
            stroke_width=4
        )

        self.play(Create(best_fit), run_time=2)
        self.wait()

        # Show residuals
        residual_lines = VGroup()
        for x, y in zip(x_data, y_data):
            y_pred = m * x + b
            residual = DashedLine(
                axes.c2p(x, y),
                axes.c2p(x, y_pred),
                color=RED,
                stroke_width=2
            )
            residual_lines.add(residual)

        residual_label = Text("Residuals", font_size=28, color=RED)
        residual_label.move_to(axes.c2p(8.5, 3))

        self.play(LaggedStart(*[Create(res) for res in residual_lines], lag_ratio=0.1))
        self.wait(0.5)
        self.play(Write(residual_label))
        self.wait()

        # Compute R²
        y_pred = m * x_data + b
        ss_res = np.sum((y_data - y_pred) ** 2)
        ss_tot = np.sum((y_data - np.mean(y_data)) ** 2)
        r_squared = 1 - ss_res / ss_tot

        r2_text = Tex(
            f"R^2 = {r_squared:.3f}",
            font_size=36,
            color=YELLOW
        )
        r2_text.next_to(line_eq, DOWN, buff=0.6)
        r2_label = Text("(goodness of fit)", font_size=24, color=GREY)
        r2_label.next_to(r2_text, DOWN, buff=0.2)

        self.play(Write(r2_text))
        self.wait(0.5)
        self.play(Write(r2_label))
        self.wait(3)


# Utility functions for least squares

def least_squares_fit(x_data, y_data):
    """
    Compute least squares linear fit.

    Args:
        x_data: Array of x values
        y_data: Array of y values

    Returns:
        (slope, intercept) tuple
    """
    x_data = np.array(x_data)
    y_data = np.array(y_data)

    # Design matrix
    X = np.column_stack([np.ones(len(x_data)), x_data])

    # Normal equation: β = (X^T X)^(-1) X^T y
    beta = np.linalg.inv(X.T @ X) @ X.T @ y_data

    intercept, slope = beta
    return slope, intercept


def compute_r_squared(x_data, y_data, slope, intercept):
    """
    Compute R² (coefficient of determination).

    Args:
        x_data: Array of x values
        y_data: Array of y values
        slope, intercept: Line parameters

    Returns:
        R² value (between 0 and 1)
    """
    x_data = np.array(x_data)
    y_data = np.array(y_data)

    y_pred = slope * x_data + intercept

    ss_res = np.sum((y_data - y_pred) ** 2)  # Residual sum of squares
    ss_tot = np.sum((y_data - np.mean(y_data)) ** 2)  # Total sum of squares

    return 1 - ss_res / ss_tot


def predict(x, slope, intercept):
    """
    Make predictions using fitted line.

    Args:
        x: Input value(s)
        slope, intercept: Line parameters

    Returns:
        Predicted y value(s)
    """
    return slope * np.array(x) + intercept


def residuals(x_data, y_data, slope, intercept):
    """
    Compute residuals (errors).

    Args:
        x_data: Array of x values
        y_data: Array of y values
        slope, intercept: Line parameters

    Returns:
        Array of residuals
    """
    y_pred = predict(x_data, slope, intercept)
    return np.array(y_data) - y_pred


def total_squared_error(x_data, y_data, slope, intercept):
    """
    Compute total squared error (sum of squared residuals).

    Args:
        x_data: Array of x values
        y_data: Array of y values
        slope, intercept: Line parameters

    Returns:
        Sum of squared errors
    """
    res = residuals(x_data, y_data, slope, intercept)
    return np.sum(res ** 2)


def weighted_least_squares(x_data, y_data, weights):
    """
    Compute weighted least squares fit.

    Args:
        x_data: Array of x values
        y_data: Array of y values
        weights: Array of weights for each point

    Returns:
        (slope, intercept) tuple
    """
    x_data = np.array(x_data)
    y_data = np.array(y_data)
    weights = np.array(weights)

    # Design matrix
    X = np.column_stack([np.ones(len(x_data)), x_data])

    # Weight matrix
    W = np.diag(weights)

    # Weighted normal equation: β = (X^T W X)^(-1) X^T W y
    beta = np.linalg.inv(X.T @ W @ X) @ X.T @ W @ y_data

    intercept, slope = beta
    return slope, intercept


def polynomial_least_squares(x_data, y_data, degree):
    """
    Fit a polynomial of given degree using least squares.

    Args:
        x_data: Array of x values
        y_data: Array of y values
        degree: Degree of polynomial

    Returns:
        Array of coefficients [c0, c1, ..., cn] where y = c0 + c1*x + ... + cn*x^n
    """
    x_data = np.array(x_data)
    y_data = np.array(y_data)

    # Design matrix with polynomial terms
    X = np.column_stack([x_data ** i for i in range(degree + 1)])

    # Normal equation
    beta = np.linalg.inv(X.T @ X) @ X.T @ y_data

    return beta
