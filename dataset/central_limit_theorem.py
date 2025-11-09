"""
Natural Group Name: Central Limit Theorem Demonstration

Educational Objectives:
- To visualize how the sum of random variables approaches a normal distribution
- To demonstrate the universality of the Central Limit Theorem
- To show that the theorem works regardless of the original distribution
- To build intuition for why the normal distribution appears everywhere

Story Arc & Intent:
The animation reveals the Central Limit Theorem through visual sampling: starting
with any distribution (uniform, exponential, etc.), the sums of samples magically
converge to a bell curve. This transforms an abstract statistical theorem into
a visible, universal phenomenon.

Narrative Flow:
- Hook/Opening: Different probability distributions (not normal)
- Development: Taking samples and computing their sums
- Build-up: The distribution of sums taking shape as a bell curve
- Climax: The emergence of the normal distribution from chaos
- Resolution: The universality and power of the CLT

Technical Implementation Notes:
- Scene Classes: MultipleSamples, SumDistribution, EmergentNormal, UniversalPhenomenon
- Key Visual Elements: Histograms, probability distributions, sampling animation
- Animation Techniques: Histogram building, distribution morphing, sampling
- Mathematical Concepts: Central Limit Theorem, normal distribution, sampling

Dependency Chain:
All scenes use basic manimlib components: Axes, Bar charts, distributions.
Uses numpy for random sampling and statistics. No custom utilities required
beyond helper functions defined in this file.

Rendering Instructions:
To render these scenes, use the manim command-line tool:
- For a single scene: manimgl central_limit_theorem.py MultipleSamples
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
# - BLUE: Original distribution
# - YELLOW: Sample points
# - GREEN: Sum distribution (emerging normal)
# - RED: Theoretical normal curve
# - WHITE: Axes and labels
# - GREY_A: De-emphasized elements
#
# Key Manim Constants Used:
# - UP, DOWN, LEFT, RIGHT: Direction vectors
# - ORIGIN: Center point
# - PI: π for calculations
# - MED_SMALL_BUFF: Spacing

# Axes configuration
AXES_CONFIG = {
    "x_range": [0, 10, 1],
    "y_range": [0, 1.2, 0.2],
    "width": 8,
    "height": 5,
}

# Sampling parameters
NUM_SAMPLES = 1000
SAMPLE_SIZE = 30

# ============================================================
# 3. UTILITY FUNCTIONS
# ============================================================

def uniform_distribution(x):
    """
    Uniform distribution on [2, 8].

    Args:
        x: Input value

    Returns:
        Probability density
    """
    if 2 <= x <= 8:
        return 1.0 / 6.0
    return 0.0

def create_histogram(axes, data, num_bins=30, color=BLUE, **kwargs):
    """
    Create a histogram from data.

    Args:
        axes: Axes object
        data: Array of data points
        num_bins: Number of bins
        color: Color of bars
        **kwargs: Additional arguments

    Returns:
        VGroup of rectangles representing histogram
    """
    hist, bin_edges = np.histogram(data, bins=num_bins, density=True)

    bars = VGroup()
    for i in range(len(hist)):
        bar_height = hist[i]
        bar_width = bin_edges[i+1] - bin_edges[i]
        bin_center = (bin_edges[i] + bin_edges[i+1]) / 2

        if bar_height > 0:
            bar = Rectangle(
                width=axes.x_axis.unit_size * bar_width * 0.9,
                height=axes.y_axis.unit_size * bar_height,
                color=color,
                fill_opacity=0.7,
                stroke_width=1,
                **kwargs
            )
            bar.move_to(axes.c2p(bin_center, bar_height / 2))
            bars.add(bar)

    return bars

def gaussian(x, mu, sigma):
    """
    Gaussian (normal) distribution.

    Args:
        x: Input value
        mu: Mean
        sigma: Standard deviation

    Returns:
        Probability density
    """
    return (1.0 / (sigma * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x - mu) / sigma) ** 2)

def create_gaussian_curve(axes, mu, sigma, color=RED, **kwargs):
    """
    Create a Gaussian curve.

    Args:
        axes: Axes object
        mu: Mean
        sigma: Standard deviation
        color: Color of curve
        **kwargs: Additional arguments

    Returns:
        Graph mobject
    """
    return axes.get_graph(
        lambda x: gaussian(x, mu, sigma),
        x_range=(mu - 4*sigma, mu + 4*sigma),
        color=color,
        stroke_width=4,
        **kwargs
    )

# ============================================================
# 4. SCENE CLASSES
# ============================================================

class MultipleSamples(Scene):
    """
    Scene 1: Introduce different distributions and the sampling process.

    This scene shows several non-normal distributions and introduces the
    idea of taking multiple samples from them.
    """

    def construct(self):
        # ========================================
        # TITLE
        # ========================================
        title = OldTexText("The Central Limit Theorem", font_size=48)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait()

        # ========================================
        # SHOW: A non-normal distribution
        # ========================================
        subtitle = OldTexText(
            "Start with any distribution (not necessarily normal)",
            font_size=28,
            color=GREY_A
        )
        subtitle.next_to(title, DOWN, buff=0.3)

        self.play(FadeIn(subtitle, shift=DOWN))
        self.wait()

        # Create axes
        axes = Axes(
            x_range=[0, 10, 2],
            y_range=[0, 0.3, 0.1],
            width=8,
            height=4,
        )
        axes.shift(DOWN * 0.5)

        self.play(ShowCreation(axes))
        self.wait()

        # Uniform distribution
        uniform_graph = axes.get_graph(
            lambda x: 1.0/6.0 if 2 <= x <= 8 else 0,
            x_range=(0, 10),
            color=BLUE,
            stroke_width=0
        )

        # Create as filled region
        uniform_region = axes.get_riemann_rectangles(
            uniform_graph,
            x_range=[2, 8],
            dx=0.1,
            color=BLUE,
            fill_opacity=0.7,
            stroke_width=1
        )

        distribution_label = Tex("\\text{Uniform Distribution}", color=BLUE, font_size=32)
        distribution_label.next_to(axes, UP, buff=0.3)

        self.play(ShowCreation(uniform_region), Write(distribution_label))
        self.wait()

        # ========================================
        # SAMPLING: Show individual samples
        # ========================================
        self.play(FadeOut(subtitle))

        sampling_text = OldTexText("Take random samples from this distribution", font_size=26)
        sampling_text.to_edge(DOWN).shift(UP * 0.3)

        self.play(FadeIn(sampling_text, shift=UP))
        self.wait()

        # Generate and show some sample points
        np.random.seed(42)
        samples = np.random.uniform(2, 8, size=15)

        sample_dots = VGroup()
        for sample in samples:
            dot = Dot(axes.c2p(sample, 0), color=YELLOW, radius=0.06)
            sample_dots.add(dot)

        self.play(
            LaggedStart([FadeIn(dot, scale=0.5) for dot in sample_dots], lag_ratio=0.1)
        )
        self.wait()

        # ========================================
        # IDEA: Take many samples
        # ========================================
        self.play(FadeOut(sampling_text))

        idea = OldTexText(
            "Now take MANY samples and add them up",
            font_size=28,
            color=YELLOW
        )
        idea.to_edge(DOWN).shift(UP * 0.3)

        self.play(FadeIn(idea, shift=UP))
        self.wait()

        # Show equation
        sum_equation = Tex(
            "S = X_1 + X_2 + \\cdots + X_n",
            font_size=32
        )
        sum_equation.next_to(idea, DOWN, buff=0.2)

        self.play(Write(sum_equation))
        self.wait(2)


class SumDistribution(Scene):
    """
    Scene 2: Show the distribution of sums forming.

    This scene takes samples from a uniform distribution, computes their
    sums, and builds a histogram showing the distribution of sums.
    """

    def construct(self):
        # ========================================
        # TITLE
        # ========================================
        title = OldTexText("Distribution of Sums", font_size=42)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait()

        # ========================================
        # SETUP: Axes for histogram
        # ========================================
        axes = Axes(
            x_range=[100, 200, 20],
            y_range=[0, 0.08, 0.02],
            width=9,
            height=5,
        )
        axes.shift(DOWN * 0.5)

        x_label = Tex("\\text{Sum of 30 samples}", font_size=28)
        x_label.next_to(axes, DOWN, buff=0.3)

        self.play(ShowCreation(axes), Write(x_label))
        self.wait()

        # ========================================
        # GENERATE: Sum samples
        # ========================================
        info = OldTexText("Taking 1000 samples, each sum of 30 values...", font_size=24, color=GREY_A)
        info.next_to(title, DOWN, buff=0.3)

        self.play(FadeIn(info, shift=DOWN))
        self.wait()

        # Generate data
        np.random.seed(42)
        sample_size = 30
        num_experiments = 1000

        sums = []
        for _ in range(num_experiments):
            samples = np.random.uniform(2, 8, size=sample_size)
            sums.append(np.sum(samples))

        sums = np.array(sums)

        # ========================================
        # BUILD: Histogram
        # ========================================
        self.play(FadeOut(info))

        building = OldTexText("Building histogram...", font_size=24, color=YELLOW)
        building.next_to(title, DOWN, buff=0.3)

        self.play(FadeIn(building, shift=DOWN))
        self.wait()

        # Create histogram
        histogram = create_histogram(axes, sums, num_bins=40, color=GREEN)

        self.play(
            LaggedStart([FadeIn(bar, shift=UP) for bar in histogram], lag_ratio=0.01),
            run_time=3
        )
        self.wait()

        # ========================================
        # OBSERVATION: Bell shape
        # ========================================
        self.play(FadeOut(building))

        observation = OldTexText(
            "A bell curve is emerging!",
            font_size=32,
            color=GREEN
        )
        observation.next_to(title, DOWN, buff=0.3)

        self.play(FadeIn(observation, shift=DOWN))
        self.wait()

        # ========================================
        # OVERLAY: Theoretical normal
        # ========================================
        # Calculate mean and std
        mean_sum = np.mean(sums)
        std_sum = np.std(sums)

        normal_curve = create_gaussian_curve(axes, mean_sum, std_sum, color=RED)

        theory_label = Tex(
            "\\text{Theoretical Normal Distribution}",
            color=RED,
            font_size=24
        )
        theory_label.to_edge(DOWN).shift(UP * 0.3)

        self.play(ShowCreation(normal_curve))
        self.play(Write(theory_label))
        self.wait()

        # Show statistics
        stats = Tex(
            f"\\mu \\approx {mean_sum:.1f}, \\quad \\sigma \\approx {std_sum:.1f}",
            font_size=24
        )
        stats.next_to(theory_label, DOWN, buff=0.2)

        self.play(Write(stats))
        self.wait(2)


class EmergentNormal(Scene):
    """
    Scene 3: Show how the normal emerges with increasing sample size.

    This scene demonstrates that as we increase the number of samples in
    each sum, the distribution becomes more and more normal.
    """

    def construct(self):
        # ========================================
        # TITLE
        # ========================================
        title = OldTexText("Emergence of the Normal", font_size=42)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait()

        # ========================================
        # EXPLANATION
        # ========================================
        explanation = OldTexText(
            "As sample size increases, the distribution becomes more normal",
            font_size=26,
            color=GREY_A
        )
        explanation.next_to(title, DOWN, buff=0.3)

        self.play(FadeIn(explanation, shift=DOWN))
        self.wait()

        # ========================================
        # SHOW: Multiple sample sizes
        # ========================================
        axes = Axes(
            x_range=[100, 200, 20],
            y_range=[0, 0.10, 0.02],
            width=8,
            height=4,
        )
        axes.shift(DOWN * 1.0)

        self.play(ShowCreation(axes))
        self.wait()

        # Different sample sizes
        sample_sizes = [2, 5, 10, 30]
        colors = [BLUE, YELLOW, GREEN, RED]

        np.random.seed(42)

        for i, (n, color) in enumerate(zip(sample_sizes, colors)):
            # Generate sums
            sums = []
            for _ in range(500):
                samples = np.random.uniform(2, 8, size=n)
                sums.append(np.sum(samples))

            sums = np.array(sums)

            # Create histogram
            histogram = create_histogram(axes, sums, num_bins=30, color=color)

            # Label
            label = Tex(f"n = {n}", color=color, font_size=28)
            label.to_edge(RIGHT).shift(UP * (1.5 - i * 0.8))

            if i == 0:
                self.play(
                    LaggedStart([FadeIn(bar, shift=UP) for bar in histogram], lag_ratio=0.01),
                    Write(label),
                    run_time=2
                )
            else:
                # Fade out previous
                self.play(
                    FadeOut(previous_histogram),
                    run_time=0.5
                )
                self.play(
                    LaggedStart([FadeIn(bar, shift=UP) for bar in histogram], lag_ratio=0.01),
                    Write(label),
                    run_time=2
                )

            self.wait()

            previous_histogram = histogram

        # ========================================
        # FINAL: Perfect bell curve
        # ========================================
        mean_sum = np.mean(sums)
        std_sum = np.std(sums)

        normal_curve = create_gaussian_curve(axes, mean_sum, std_sum, color=WHITE)
        normal_curve.set_stroke(width=5)

        self.play(ShowCreation(normal_curve))
        self.wait()

        final_text = OldTexText(
            "Perfect bell curve with n = 30!",
            font_size=28,
            color=WHITE
        )
        final_text.to_edge(DOWN).shift(UP * 0.3)

        self.play(FadeIn(final_text, shift=UP))
        self.wait(2)


class UniversalPhenomenon(Scene):
    """
    Scene 4: Show the universality of the CLT with different distributions.

    This scene demonstrates that the CLT works regardless of the original
    distribution - uniform, exponential, or any other.
    """

    def construct(self):
        # ========================================
        # TITLE
        # ========================================
        title = OldTexText("The Universal Phenomenon", font_size=42)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait()

        # ========================================
        # STATEMENT
        # ========================================
        statement = VGroup(
            OldTexText("The Central Limit Theorem states:", font_size=28),
            Tex(
                "\\text{The sum of } n \\text{ independent random variables}",
                font_size=24
            ),
            Tex(
                "\\text{approaches a normal distribution as } n \\to \\infty",
                font_size=24
            ),
        )
        statement.arrange(DOWN, buff=0.3)
        statement.next_to(title, DOWN, buff=0.5)

        for line in statement:
            self.play(Write(line))
            self.wait(0.5)

        self.wait()

        # ========================================
        # UNIVERSALITY
        # ========================================
        self.play(FadeOut(statement))

        universal = OldTexText(
            "This works for ANY distribution!",
            font_size=32,
            color=YELLOW
        )
        universal.next_to(title, DOWN, buff=0.5)

        self.play(FadeIn(universal, shift=DOWN))
        self.wait()

        # ========================================
        # EXAMPLES
        # ========================================
        examples = VGroup(
            OldTexText("Examples of original distributions:", font_size=26),
            OldTexText("• Uniform (like dice)", font_size=22),
            OldTexText("• Exponential (like radioactive decay)", font_size=22),
            OldTexText("• Binomial (like coin flips)", font_size=22),
            OldTexText("• Any finite-variance distribution!", font_size=22, color=GREEN),
        )
        examples.arrange(DOWN, buff=0.25, aligned_edge=LEFT)
        examples.next_to(universal, DOWN, buff=0.6)

        for item in examples:
            self.play(FadeIn(item, shift=UP))
            self.wait(0.3)

        self.wait()

        # ========================================
        # APPLICATIONS
        # ========================================
        self.play(FadeOut(universal), FadeOut(examples))

        applications_title = OldTexText("Why does this matter?", font_size=32, color=BLUE)
        applications_title.next_to(title, DOWN, buff=0.5)

        applications = VGroup(
            OldTexText("• Explains why the normal distribution is everywhere", font_size=24),
            OldTexText("• Foundation of statistical inference", font_size=24),
            OldTexText("• Enables hypothesis testing and confidence intervals", font_size=24),
            OldTexText("• Justifies many approximations in science", font_size=24),
            OldTexText("• Heights, test scores, measurement errors...", font_size=24, color=GREY_A),
        )
        applications.arrange(DOWN, buff=0.25, aligned_edge=LEFT)
        applications.next_to(applications_title, DOWN, buff=0.5)

        self.play(Write(applications_title))
        self.wait()

        for item in applications:
            self.play(FadeIn(item, shift=UP))
            self.wait(0.4)

        self.wait()

        # ========================================
        # FORMULA
        # ========================================
        self.play(FadeOut(applications_title), FadeOut(applications))

        formula_title = OldTexText("The Formal Statement", font_size=32, color=GREEN)
        formula_title.next_to(title, DOWN, buff=0.5)

        formula = Tex(
            "\\frac{\\bar{X} - \\mu}{\\sigma / \\sqrt{n}} \\xrightarrow{d} N(0, 1)",
            font_size=36
        )
        formula.next_to(formula_title, DOWN, buff=0.6)

        formula_box = SurroundingRectangle(formula, buff=0.3, color=GREEN, stroke_width=2)

        self.play(Write(formula_title))
        self.play(Write(formula))
        self.play(ShowCreation(formula_box))
        self.wait()

        # Explanation
        explanation_parts = VGroup(
            Tex("\\bar{X} = \\text{sample mean}", font_size=24),
            Tex("\\mu = \\text{population mean}", font_size=24),
            Tex("\\sigma = \\text{population standard deviation}", font_size=24),
            Tex("n = \\text{sample size}", font_size=24),
            Tex("N(0, 1) = \\text{standard normal distribution}", font_size=24),
        )
        explanation_parts.arrange(DOWN, buff=0.2, aligned_edge=LEFT)
        explanation_parts.to_edge(DOWN).shift(UP * 0.3)

        for part in explanation_parts:
            self.play(FadeIn(part, shift=UP), run_time=0.5)

        self.wait(2)


# ============================================================
# 5. SCENE SUMMARY AND EXECUTION ORDER
# ============================================================
#
# Scene 1 (MultipleSamples):
#   - Introduces a non-normal distribution (uniform)
#   - Shows random sampling from this distribution
#   - Introduces the idea of summing multiple samples
#
# Scene 2 (SumDistribution):
#   - Takes 1000 sums of 30 samples each
#   - Builds a histogram of these sums
#   - Shows emergence of bell curve shape
#   - Overlays theoretical normal distribution
#
# Scene 3 (EmergentNormal):
#   - Shows how distribution changes with sample size
#   - Demonstrates n=2, 5, 10, 30
#   - Shows convergence to perfect normal
#
# Scene 4 (UniversalPhenomenon):
#   - States the Central Limit Theorem formally
#   - Emphasizes universality (works for any distribution)
#   - Shows applications and importance
#   - Presents the formal mathematical statement

SCENE_ORDER = [
    MultipleSamples,           # Part 1: Sampling from a distribution
    SumDistribution,           # Part 2: Distribution of sums
    EmergentNormal,            # Part 3: Convergence with sample size
    UniversalPhenomenon,       # Part 4: Universality and applications
]
