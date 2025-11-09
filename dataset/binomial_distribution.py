"""
Binomial Distribution

This module demonstrates the binomial distribution, which models the number of successes
in a fixed number of independent trials. Covers the binomial formula, distribution shape,
connection to Pascal's triangle, and approximation by the normal distribution.

Scenes:
    - CoinFlips: Introduction using coin flips
    - BinomialFormula: Derive and explain the binomial formula
    - DistributionShape: Visualize how the distribution shape changes
    - NormalApproximation: Show convergence to normal distribution
"""

from manimlib import *
import numpy as np
import math


def binomial_coefficient(n, k):
    """Compute binomial coefficient C(n, k) = n! / (k! * (n-k)!)"""
    if k < 0 or k > n:
        return 0
    if k == 0 or k == n:
        return 1
    k = min(k, n - k)  # Take advantage of symmetry
    result = 1
    for i in range(k):
        result = result * (n - i) // (i + 1)
    return result


class CoinFlips(Scene):
    """
    Introduce the binomial distribution through coin flips.
    """

    def construct(self):
        # Title
        title = Text("The Binomial Distribution", font_size=52)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait()

        # Setup the question
        question = Text("Flip a fair coin 5 times", font_size=40, color=YELLOW)
        question.move_to(2 * UP)
        self.play(Write(question))
        self.wait()

        subquestion = Text(
            "How many heads will you get?",
            font_size=36,
            color=GREY
        )
        subquestion.next_to(question, DOWN, buff=0.4)
        self.play(Write(subquestion))
        self.wait(2)

        # Show possible outcomes
        self.play(FadeOut(subquestion))

        outcomes_label = Text("Possible outcomes:", font_size=32)
        outcomes_label.move_to(UP * 0.8 + LEFT * 4)
        self.play(Write(outcomes_label))
        self.wait()

        # Show some example sequences
        examples = VGroup(
            Text("HHHTT → 3 heads", font_size=28, color=BLUE),
            Text("THHHT → 3 heads", font_size=28, color=BLUE),
            Text("HTHTH → 3 heads", font_size=28, color=BLUE),
            Text("HTTTT → 1 head", font_size=28, color=RED),
            Text("HHHHH → 5 heads", font_size=28, color=GREEN)
        )
        examples.arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        examples.next_to(outcomes_label, DOWN, buff=0.4, aligned_edge=LEFT)

        self.play(LaggedStart(*[Write(ex) for ex in examples], lag_ratio=0.3))
        self.wait(2)

        # Key observation
        observation = Text(
            "Different sequences can give the same number of heads!",
            font_size=30,
            color=YELLOW
        )
        observation.move_to(DOWN * 1.5)
        self.play(Write(observation))
        self.wait(2)

        # Show distribution
        self.play(
            FadeOut(examples),
            FadeOut(outcomes_label),
            FadeOut(observation)
        )

        dist_title = Text("Distribution of outcomes (n=5):", font_size=32)
        dist_title.move_to(UP * 0.8)
        self.play(Write(dist_title))
        self.wait()

        # Create bar chart
        axes = Axes(
            x_range=[-0.5, 5.5, 1],
            y_range=[0, 0.35, 0.1],
            height=4,
            width=8,
            axis_config={"include_tip": False}
        )
        axes.move_to(DOWN * 1.3)

        x_label = Text("Number of Heads", font_size=28).next_to(axes.x_axis, DOWN)
        y_label = Text("Probability", font_size=28).next_to(axes.y_axis, LEFT).rotate(PI/2)

        self.play(Create(axes))
        self.play(Write(x_label), Write(y_label))
        self.wait()

        # Binomial probabilities for n=5, p=0.5
        n = 5
        p = 0.5
        probs = [binomial_coefficient(n, k) * (p**k) * ((1-p)**(n-k)) for k in range(n+1)]

        bars = VGroup()
        prob_labels = VGroup()

        for k, prob in enumerate(probs):
            bar = Rectangle(
                height=prob * 10,
                width=0.6,
                fill_opacity=0.7,
                fill_color=BLUE,
                stroke_width=2,
                stroke_color=WHITE
            )
            bar.move_to(axes.c2p(k, prob/2))
            bars.add(bar)

            # Probability label
            label = Tex(f"{prob:.3f}", font_size=20)
            label.next_to(bar, UP, buff=0.1)
            prob_labels.add(label)

        self.play(LaggedStart(*[FadeIn(bar) for bar in bars], lag_ratio=0.2))
        self.wait(0.5)
        self.play(LaggedStart(*[Write(label) for label in prob_labels], lag_ratio=0.2))
        self.wait(2)

        # Highlight the peak (most likely outcome)
        peak_arrow = Arrow(
            axes.c2p(2.5, 0.35),
            bars[2].get_top() + UP * 0.15,
            color=YELLOW
        )
        peak_label = Text("Most likely: 2-3 heads", font_size=28, color=YELLOW)
        peak_label.next_to(peak_arrow, RIGHT, buff=0.2)

        self.play(Create(peak_arrow), Write(peak_label))
        self.wait(2)


class BinomialFormula(Scene):
    """
    Derive and explain the binomial probability formula.
    """

    def construct(self):
        # Title
        title = Text("The Binomial Formula", font_size=52)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait()

        # Setup
        setup_title = Text("Setup:", font_size=36, color=YELLOW)
        setup_title.move_to(2.2 * UP + LEFT * 4.5)

        setup = VGroup(
            Tex(R"n \text{ trials}", font_size=32),
            Tex(R"p = \text{probability of success}", font_size=32),
            Tex(R"k = \text{number of successes}", font_size=32)
        )
        setup.arrange(DOWN, aligned_edge=LEFT, buff=0.4)
        setup.next_to(setup_title, DOWN, buff=0.4, aligned_edge=LEFT)

        self.play(Write(setup_title))
        self.wait(0.5)
        self.play(LaggedStart(*[Write(item) for item in setup], lag_ratio=0.3))
        self.wait(2)

        # Build the formula step by step
        question = Text("P(exactly k successes) = ?", font_size=36, color=BLUE)
        question.move_to(UP * 0.8 + RIGHT * 2.5)
        self.play(Write(question))
        self.wait()

        # Step 1: Probability of specific sequence
        step1_label = Text("Step 1: Probability of one specific sequence", font_size=28)
        step1_label.move_to(RIGHT * 2.5)

        step1 = Tex(
            R"p^k \cdot (1-p)^{n-k}",
            font_size=36,
            color=GREEN
        )
        step1.next_to(step1_label, DOWN, buff=0.3)

        step1_note = Text("(k successes, n-k failures)", font_size=24, color=GREY)
        step1_note.next_to(step1, DOWN, buff=0.2)

        self.play(Write(step1_label))
        self.wait(0.5)
        self.play(Write(step1))
        self.wait(0.5)
        self.play(Write(step1_note))
        self.wait(2)

        # Step 2: Number of ways to arrange
        self.play(
            FadeOut(step1_label),
            FadeOut(step1),
            FadeOut(step1_note)
        )

        step2_label = Text("Step 2: How many such sequences?", font_size=28)
        step2_label.move_to(RIGHT * 2.5)

        step2 = Tex(
            R"\binom{n}{k} = \frac{n!}{k!(n-k)!}",
            font_size=36,
            color=PURPLE
        )
        step2.next_to(step2_label, DOWN, buff=0.3)

        step2_note = Text("(Choose k positions for successes)", font_size=24, color=GREY)
        step2_note.next_to(step2, DOWN, buff=0.2)

        self.play(Write(step2_label))
        self.wait(0.5)
        self.play(Write(step2))
        self.wait(0.5)
        self.play(Write(step2_note))
        self.wait(2)

        # Combine
        self.play(
            FadeOut(question),
            FadeOut(step2_label),
            FadeOut(step2),
            FadeOut(step2_note)
        )

        formula_label = Text("The Binomial Formula:", font_size=36, color=YELLOW)
        formula_label.move_to(UP * 0.8 + RIGHT * 2.5)

        formula = Tex(
            R"P(X = k) = \binom{n}{k} p^k (1-p)^{n-k}",
            font_size=44,
            color=GREEN
        )
        formula.next_to(formula_label, DOWN, buff=0.5)

        formula_box = SurroundingRectangle(formula, color=YELLOW, buff=0.2)

        self.play(Write(formula_label))
        self.wait(0.5)
        self.play(Write(formula))
        self.wait()
        self.play(Create(formula_box))
        self.wait(2)

        # Example
        example_title = Text("Example: n=5, p=0.5, k=3", font_size=32, color=BLUE)
        example_title.move_to(DOWN * 1.5 + RIGHT * 2.5)

        example_calc = Tex(
            R"P(X=3) = \binom{5}{3} (0.5)^3 (0.5)^2 = 10 \cdot \frac{1}{32} = \frac{10}{32}",
            font_size=28
        )
        example_calc.next_to(example_title, DOWN, buff=0.4)

        self.play(Write(example_title))
        self.wait(0.5)
        self.play(Write(example_calc))
        self.wait(3)


class DistributionShape(Scene):
    """
    Show how the binomial distribution shape changes with parameters.
    """

    def construct(self):
        # Title
        title = Text("Shape of Binomial Distribution", font_size=52)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait()

        # Create axes
        axes = Axes(
            x_range=[-0.5, 20.5, 5],
            y_range=[0, 0.25, 0.05],
            height=5,
            width=10,
            axis_config={"include_tip": False}
        )
        axes.move_to(DOWN * 0.5)

        x_label = Text("k", font_size=32).next_to(axes.x_axis, RIGHT)
        y_label = Text("P(X=k)", font_size=32).next_to(axes.y_axis, UP)

        self.play(Create(axes), Write(x_label), Write(y_label))
        self.wait()

        # Function to create bars for binomial distribution
        def create_binomial_bars(n, p, color):
            probs = [binomial_coefficient(n, k) * (p**k) * ((1-p)**(n-k)) for k in range(n+1)]
            bars = VGroup()
            for k, prob in enumerate(probs):
                if prob > 0.001:  # Only show significant probabilities
                    bar = Rectangle(
                        height=max(prob * 20, 0.01),
                        width=0.4,
                        fill_opacity=0.7,
                        fill_color=color,
                        stroke_width=1,
                        stroke_color=WHITE
                    )
                    bar.move_to(axes.c2p(k, prob * 10))
                    bars.add(bar)
            return bars

        # Case 1: n=20, p=0.5 (symmetric)
        params1 = Tex("n=20, p=0.5", font_size=36, color=BLUE)
        params1.to_corner(UR).shift(LEFT * 0.5 + DOWN * 1)
        self.play(Write(params1))
        self.wait()

        bars1 = create_binomial_bars(20, 0.5, BLUE)
        self.play(LaggedStart(*[FadeIn(bar) for bar in bars1], lag_ratio=0.05))
        self.wait()

        note1 = Text("Symmetric around n/2", font_size=28, color=GREY)
        note1.next_to(params1, DOWN, buff=0.3, aligned_edge=LEFT)
        self.play(Write(note1))
        self.wait(2)

        # Case 2: n=20, p=0.3 (skewed)
        self.play(
            FadeOut(bars1),
            FadeOut(params1),
            FadeOut(note1)
        )

        params2 = Tex("n=20, p=0.3", font_size=36, color=GREEN)
        params2.to_corner(UR).shift(LEFT * 0.5 + DOWN * 1)
        self.play(Write(params2))
        self.wait()

        bars2 = create_binomial_bars(20, 0.3, GREEN)
        self.play(LaggedStart(*[FadeIn(bar) for bar in bars2], lag_ratio=0.05))
        self.wait()

        note2 = Text("Skewed when p ≠ 0.5", font_size=28, color=GREY)
        note2.next_to(params2, DOWN, buff=0.3, aligned_edge=LEFT)
        self.play(Write(note2))
        self.wait(2)

        # Case 3: n=20, p=0.1 (highly skewed)
        self.play(
            FadeOut(bars2),
            FadeOut(params2),
            FadeOut(note2)
        )

        params3 = Tex("n=20, p=0.1", font_size=36, color=RED)
        params3.to_corner(UR).shift(LEFT * 0.5 + DOWN * 1)
        self.play(Write(params3))
        self.wait()

        bars3 = create_binomial_bars(20, 0.1, RED)
        self.play(LaggedStart(*[FadeIn(bar) for bar in bars3], lag_ratio=0.05))
        self.wait()

        note3 = Text("Highly skewed for extreme p", font_size=28, color=GREY)
        note3.next_to(params3, DOWN, buff=0.3, aligned_edge=LEFT)
        self.play(Write(note3))
        self.wait(2)

        # Properties
        self.play(
            FadeOut(bars3),
            FadeOut(params3),
            FadeOut(note3)
        )

        properties_title = Text("Key Properties:", font_size=36, color=YELLOW)
        properties_title.to_corner(UR).shift(LEFT * 0.5 + DOWN * 1)

        properties = VGroup(
            Tex(R"\text{Mean: } \mu = np", font_size=32),
            Tex(R"\text{Variance: } \sigma^2 = np(1-p)", font_size=32),
            Tex(R"\text{Std Dev: } \sigma = \sqrt{np(1-p)}", font_size=32)
        )
        properties.arrange(DOWN, aligned_edge=LEFT, buff=0.4)
        properties.next_to(properties_title, DOWN, buff=0.4, aligned_edge=LEFT)

        self.play(Write(properties_title))
        self.wait(0.5)
        self.play(LaggedStart(*[Write(prop) for prop in properties], lag_ratio=0.3))
        self.wait(3)


class NormalApproximation(Scene):
    """
    Show that binomial distribution approaches normal distribution for large n.
    """

    def construct(self):
        # Title
        title = Text("Normal Approximation", font_size=52)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait()

        # Subtitle
        subtitle = Text(
            "As n increases, binomial → normal",
            font_size=36,
            color=GREY
        )
        subtitle.next_to(title, DOWN, buff=0.3)
        self.play(Write(subtitle))
        self.wait(2)

        # Create axes
        axes = Axes(
            x_range=[-0.5, 50.5, 10],
            y_range=[0, 0.12, 0.02],
            height=5,
            width=10,
            axis_config={"include_tip": False}
        )
        axes.move_to(DOWN * 0.5)

        x_label = Text("k", font_size=32).next_to(axes.x_axis, RIGHT)
        y_label = Text("P(X=k)", font_size=32).next_to(axes.y_axis, UP)

        self.play(Create(axes), Write(x_label), Write(y_label))
        self.wait()

        # Show progression: n = 10, 30, 50
        n_values = [10, 30, 50]
        colors = [BLUE, GREEN, YELLOW]
        p = 0.5

        for i, (n, color) in enumerate(zip(n_values, colors)):
            # Parameters
            params = Tex(f"n={n}, p=0.5", font_size=36, color=color)
            params.to_corner(UR).shift(LEFT * 0.5 + DOWN * 1.2)

            # Create bars
            probs = [binomial_coefficient(n, k) * (p**k) * ((1-p)**(n-k)) for k in range(n+1)]
            bars = VGroup()
            for k, prob in enumerate(probs):
                if prob > 0.001:
                    bar = Rectangle(
                        height=max(prob * 40, 0.01),
                        width=50/n * 0.8,  # Adjust width based on n
                        fill_opacity=0.5,
                        fill_color=color,
                        stroke_width=1,
                        stroke_color=color
                    )
                    bar.move_to(axes.c2p(k, prob * 20))
                    bars.add(bar)

            # Normal curve overlay
            mu = n * p
            sigma = np.sqrt(n * p * (1 - p))

            def normal_pdf(x):
                return (1 / (sigma * np.sqrt(2 * PI))) * np.exp(-0.5 * ((x - mu) / sigma) ** 2)

            normal_curve = axes.get_graph(
                normal_pdf,
                x_range=[max(0, mu - 3*sigma), min(n, mu + 3*sigma)],
                color=color,
                stroke_width=3
            )

            if i == 0:
                self.play(Write(params))
                self.play(LaggedStart(*[FadeIn(bar) for bar in bars], lag_ratio=0.03))
                self.wait()
            else:
                self.play(
                    ReplacementTransform(prev_params, params),
                    ReplacementTransform(prev_bars, bars)
                )
                self.wait()

            # Add normal curve for last iteration
            if i == len(n_values) - 1:
                curve_label = Text("Normal curve overlay", font_size=28, color=YELLOW)
                curve_label.next_to(params, DOWN, buff=0.4, aligned_edge=LEFT)
                self.play(Write(curve_label))
                self.play(Create(normal_curve), run_time=2)
                self.wait(2)

            prev_params = params
            prev_bars = bars

        # Formula for normal approximation
        self.play(
            FadeOut(prev_params),
            FadeOut(curve_label),
            FadeOut(subtitle)
        )

        formula_title = Text("Normal Approximation:", font_size=32, color=GREEN)
        formula_title.to_corner(UR).shift(LEFT * 0.5 + DOWN * 1.2)

        formula = Tex(
            R"X \sim N(\mu = np, \sigma^2 = np(1-p))",
            font_size=32
        )
        formula.next_to(formula_title, DOWN, buff=0.3, aligned_edge=LEFT)

        condition = Text("When np > 5 and n(1-p) > 5", font_size=24, color=GREY)
        condition.next_to(formula, DOWN, buff=0.3, aligned_edge=LEFT)

        self.play(Write(formula_title))
        self.wait(0.5)
        self.play(Write(formula))
        self.wait(0.5)
        self.play(Write(condition))
        self.wait(3)


# Utility functions for binomial distribution

def binomial_pmf(n, p, k):
    """
    Compute binomial probability mass function.

    Args:
        n: Number of trials
        p: Probability of success
        k: Number of successes

    Returns:
        P(X = k)
    """
    return binomial_coefficient(n, k) * (p ** k) * ((1 - p) ** (n - k))


def binomial_cdf(n, p, k):
    """
    Compute binomial cumulative distribution function.

    Args:
        n: Number of trials
        p: Probability of success
        k: Maximum number of successes

    Returns:
        P(X <= k)
    """
    return sum(binomial_pmf(n, p, i) for i in range(k + 1))


def binomial_mean(n, p):
    """
    Compute mean of binomial distribution.

    Args:
        n: Number of trials
        p: Probability of success

    Returns:
        Mean (expected value)
    """
    return n * p


def binomial_variance(n, p):
    """
    Compute variance of binomial distribution.

    Args:
        n: Number of trials
        p: Probability of success

    Returns:
        Variance
    """
    return n * p * (1 - p)


def generate_binomial_samples(n, p, num_samples):
    """
    Generate random samples from binomial distribution.

    Args:
        n: Number of trials
        p: Probability of success
        num_samples: Number of samples to generate

    Returns:
        Array of samples
    """
    return np.random.binomial(n, p, num_samples)


def normal_approximation_to_binomial(n, p, k):
    """
    Approximate binomial probability using normal distribution.

    Args:
        n: Number of trials
        p: Probability of success
        k: Number of successes

    Returns:
        Approximate P(X = k) using continuity correction
    """
    mu = n * p
    sigma = np.sqrt(n * p * (1 - p))

    # Continuity correction: use interval [k - 0.5, k + 0.5]
    z_lower = (k - 0.5 - mu) / sigma
    z_upper = (k + 0.5 - mu) / sigma

    # Standard normal CDF approximation
    from math import erf
    norm_cdf = lambda z: 0.5 * (1 + erf(z / np.sqrt(2)))

    return norm_cdf(z_upper) - norm_cdf(z_lower)
