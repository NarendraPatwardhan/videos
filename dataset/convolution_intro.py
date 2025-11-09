"""
Natural Group Name: Convolution as Sliding Overlap

Educational Objectives:
- To introduce convolution as a sliding overlap operation
- To build intuition for the flip-and-slide interpretation
- To visualize how convolution combines two functions
- To show applications in signal processing and probability

Story Arc & Intent:
The animation demystifies convolution by showing it as a simple geometric
operation: flip one function, slide it across another, and measure the overlap
at each position. This visual interpretation makes the abstract integral formula
intuitive and reveals why convolution appears in so many applications.

Narrative Flow:
- Hook/Opening: Show two simple functions that we want to combine
- Development: Introduce the flip-and-slide procedure
- Build-up: Animate the sliding process and show overlap area
- Climax: Plot the complete convolution result
- Resolution: Connect to the formula (f*g)(t) = ∫f(τ)g(t-τ)dτ
- Extension: Mention applications (smoothing, blurring, probability)

Technical Implementation Notes:
- Scene Classes: IntroduceFunctions, SlidingProduct, ConvolutionGraph, Applications
- Key Visual Elements: Function graphs, sliding animation, area shading, integral
- Animation Techniques: Function plotting, sliding transformations, area highlighting
- Mathematical Concepts: Convolution integral, function transformation

Dependency Chain:
All scenes are independent. They use Axes, ParametricCurve, and Tex from
manimlib. Utility functions handle convolution calculation and visualization.

Rendering Instructions:
To render these scenes, use the manim command-line tool:
- For a single scene: manimgl convolution_intro.py IntroduceFunctions
- For all scenes in sequence: iterate through SCENE_ORDER
"""

# ============================================================
# 1. IMPORTS
# ============================================================
from manimlib import *
import numpy as np
from scipy import signal

# ============================================================
# 2. CONFIGURATION AND CONSTANTS
# ============================================================
# Axes configuration
X_RANGE = [-3, 6, 1]
Y_RANGE = [-0.5, 1.5, 0.5]

# Colors
FUNCTION_F_COLOR = BLUE
FUNCTION_G_COLOR = GREEN
CONVOLUTION_COLOR = YELLOW
OVERLAP_COLOR = RED

# ============================================================
# 3. UTILITY FUNCTIONS
# ============================================================

def box_function(x, center=0, width=1):
    """
    Box/rectangular function.

    Args:
        x: Input value or array
        center: Center of the box
        width: Width of the box

    Returns:
        1 inside box, 0 outside
    """
    return np.where(np.abs(x - center) <= width/2, 1.0, 0.0)

def triangle_function(x, center=0, width=2):
    """
    Triangle function.

    Args:
        x: Input value or array
        center: Center of triangle
        width: Base width

    Returns:
        Triangle values
    """
    return np.maximum(0, 1 - np.abs(x - center) / (width/2))

def exponential_decay(x):
    """Exponential decay function for x >= 0."""
    return np.where(x >= 0, np.exp(-x), 0)

def compute_convolution(f, g, t_range, dt=0.01):
    """
    Compute discrete convolution of two functions.

    Args:
        f, g: Functions to convolve
        t_range: Range of t values
        dt: Time step

    Returns:
        t_values, convolution_values
    """
    # Create fine grid for integration
    tau_values = np.arange(t_range[0] - 5, t_range[1] + 5, dt)

    # Compute convolution for each t
    t_values = np.arange(t_range[0], t_range[1], dt * 2)
    conv_values = []

    for t in t_values:
        # Evaluate f(τ) * g(t - τ)
        integrand = f(tau_values) * g(t - tau_values)
        # Numerical integration (trapezoidal rule)
        conv_val = np.trapz(integrand, dx=dt)
        conv_values.append(conv_val)

    return t_values, np.array(conv_values)

def create_function_graph(axes, func, x_range, color, stroke_width=3):
    """
    Create a graph of a function.

    Args:
        axes: Axes object
        func: Function to plot
        x_range: Range to plot
        color: Graph color
        stroke_width: Line width

    Returns:
        Graph object
    """
    graph = axes.get_graph(
        func,
        x_range=x_range,
        color=color,
        stroke_width=stroke_width
    )
    return graph

# ============================================================
# 4. BASE CLASSES AND HELPERS
# ============================================================
# No custom base classes needed

# ============================================================
# 5. SCENE IMPLEMENTATIONS
# ============================================================

class IntroduceFunctions(InteractiveScene):
    """
    Part 1: Introduce two functions we want to convolve.

    Narrative purpose:
        To set up the problem by showing two simple functions and
        posing the question of how to combine them meaningfully.

    Mathematical content:
        Displays f(t) as a box function and g(t) as a triangle function
        (or other simple shapes), establishing them as our starting point.

    Visual approach:
        Show clean graphs of both functions side by side or stacked,
        with clear labels and colors.
    """
    def construct(self):
        # ========================================
        # SETUP: Title
        # ========================================
        title = OldTexText("Convolution: Combining Functions", font_size=48)
        title.to_edge(UP)

        self.play(FadeIn(title, shift=DOWN))
        self.wait()

        # ========================================
        # CREATE: Axes for f(t)
        # ========================================
        axes_f = Axes(
            x_range=[-1, 4, 1],
            y_range=[0, 1.2, 0.5],
            width=5,
            height=3,
        )
        axes_f.shift(3 * LEFT + 0.5 * DOWN)

        x_label_f = Tex("t", font_size=32)
        x_label_f.next_to(axes_f.x_axis, RIGHT)

        axes_f_group = VGroup(axes_f, x_label_f)

        # Function f: box function
        f = lambda x: box_function(x, center=1, width=1)
        graph_f = create_function_graph(axes_f, f, [0, 2], FUNCTION_F_COLOR)

        label_f = Tex("f(t)", font_size=36, color=FUNCTION_F_COLOR)
        label_f.next_to(axes_f, UP, buff=0.3)

        self.play(
            ShowCreation(axes_f),
            Write(x_label_f),
            Write(label_f)
        )
        self.wait()

        self.play(ShowCreation(graph_f))
        self.wait()

        # ========================================
        # CREATE: Axes for g(t)
        # ========================================
        axes_g = Axes(
            x_range=[-1, 4, 1],
            y_range=[0, 1.2, 0.5],
            width=5,
            height=3,
        )
        axes_g.shift(3 * RIGHT + 0.5 * DOWN)

        x_label_g = Tex("t", font_size=32)
        x_label_g.next_to(axes_g.x_axis, RIGHT)

        axes_g_group = VGroup(axes_g, x_label_g)

        # Function g: triangle function
        g = lambda x: triangle_function(x, center=1.5, width=2)
        graph_g = create_function_graph(axes_g, g, [0.5, 2.5], FUNCTION_G_COLOR)

        label_g = Tex("g(t)", font_size=36, color=FUNCTION_G_COLOR)
        label_g.next_to(axes_g, UP, buff=0.3)

        self.play(
            ShowCreation(axes_g),
            Write(x_label_g),
            Write(label_g)
        )
        self.wait()

        self.play(ShowCreation(graph_g))
        self.wait()

        # ========================================
        # QUESTION: How to combine?
        # ========================================
        question = OldTexText(
            "How do we combine these functions?",
            font_size=32,
            color=YELLOW
        )
        question.to_edge(DOWN, buff=0.8)

        self.play(Write(question))
        self.wait(2)

        # ========================================
        # ANSWER: Convolution!
        # ========================================
        answer = OldTexText(
            "Convolution: (f * g)(t)",
            font_size=36,
            color=CONVOLUTION_COLOR,
            weight=BOLD
        )
        answer.next_to(question, UP, buff=0.5)

        self.play(FadeIn(answer, shift=UP))
        self.wait(3)

        # ========================================
        # CLEANUP
        # ========================================
        self.play(FadeOut(*self.mobjects), run_time=1)
        self.wait()


class SlidingProduct(InteractiveScene):
    """
    Part 2: Show the flip-and-slide interpretation.

    Narrative purpose:
        To reveal the key insight: convolution flips one function,
        slides it, and measures overlap at each position.

    Mathematical content:
        Shows g(t-τ) is g(τ) flipped and shifted by t. The overlap
        integral ∫f(τ)g(t-τ)dτ gives the convolution value at t.

    Visual approach:
        Animate g being flipped, then sliding across f. At each position,
        show the product f(τ)g(t-τ) and shade the overlap area.
    """
    def construct(self):
        # ========================================
        # SETUP: Title
        # ========================================
        title = OldTexText("The Flip-and-Slide Procedure", font_size=48)
        title.to_edge(UP)

        self.play(FadeIn(title, shift=DOWN))
        self.wait()

        # ========================================
        # CREATE: Single set of axes
        # ========================================
        axes = Axes(
            x_range=[-1, 5, 1],
            y_range=[0, 1.3, 0.5],
            width=10,
            height=4,
        )
        axes.shift(0.8 * DOWN)

        tau_label = Tex(R"\tau", font_size=36)
        tau_label.next_to(axes.x_axis, RIGHT)

        self.play(
            ShowCreation(axes),
            Write(tau_label)
        )
        self.wait()

        # ========================================
        # PLOT: f(τ)
        # ========================================
        f = lambda x: box_function(x, center=1, width=1)
        graph_f = create_function_graph(axes, f, [0, 2], FUNCTION_F_COLOR)

        label_f = Tex(R"f(\tau)", font_size=32, color=FUNCTION_F_COLOR)
        label_f.next_to(axes, UP + LEFT, buff=0.3)

        self.play(
            ShowCreation(graph_f),
            Write(label_f)
        )
        self.wait()

        # ========================================
        # SHOW: Original g(τ)
        # ========================================
        g_orig = lambda x: triangle_function(x, center=1.5, width=2)
        graph_g_orig = create_function_graph(axes, g_orig, [0.5, 2.5],
                                            FUNCTION_G_COLOR, stroke_width=2)
        graph_g_orig.set_stroke(opacity=0.3)

        label_g_orig = Tex(R"g(\tau)", font_size=28, color=FUNCTION_G_COLOR)
        label_g_orig.next_to(label_f, DOWN, buff=0.2)

        self.play(
            ShowCreation(graph_g_orig),
            Write(label_g_orig)
        )
        self.wait()

        # ========================================
        # STEP 1: Flip g to get g(-τ)
        # ========================================
        instruction1 = OldTexText("Step 1: Flip g to get g(-τ)", font_size=28, color=YELLOW)
        instruction1.to_edge(DOWN, buff=1.5)

        self.play(Write(instruction1))
        self.wait()

        # Flipped version
        g_flipped = lambda x: triangle_function(-x, center=1.5, width=2)
        graph_g_flipped = create_function_graph(axes, g_flipped, [-2.5, -0.5],
                                               FUNCTION_G_COLOR)

        label_g_flipped = Tex(R"g(-\tau)", font_size=32, color=FUNCTION_G_COLOR)
        label_g_flipped.move_to(label_g_orig)

        self.play(
            Transform(graph_g_orig, graph_g_flipped),
            Transform(label_g_orig, label_g_flipped)
        )
        self.wait(2)

        # ========================================
        # STEP 2: Slide to get g(t - τ)
        # ========================================
        self.play(FadeOut(instruction1))

        instruction2 = OldTexText("Step 2: Slide to position t", font_size=28, color=YELLOW)
        instruction2.to_edge(DOWN, buff=1.5)

        self.play(Write(instruction2))
        self.wait()

        # Slide through several positions
        t_values = [0, 1, 2, 3]

        for t_val in t_values:
            # g(t - τ) is g flipped and shifted by t
            g_shifted = lambda x, t=t_val: triangle_function(-(x - t), center=1.5, width=2)

            if t_val == 0:
                # Determine range for plotting
                graph_range = [-2.5 + t_val, -0.5 + t_val]
            else:
                graph_range = [-2.5 + t_val, -0.5 + t_val]

            graph_g_shifted = create_function_graph(axes, g_shifted, graph_range,
                                                   FUNCTION_G_COLOR)

            label_g_shifted = Tex(f"g({t_val} - \\tau)", font_size=32,
                                 color=FUNCTION_G_COLOR)
            label_g_shifted.move_to(label_g_orig)

            t_indicator = Tex(f"t = {t_val}", font_size=28, color=YELLOW)
            t_indicator.next_to(instruction2, UP, buff=0.3)

            # Highlight overlap region
            if t_val >= 0.5 and t_val <= 2.5:
                # There's overlap - shade it
                overlap_start = max(0.5, t_val - 1)
                overlap_end = min(2, t_val + 1)

                if overlap_end > overlap_start:
                    # Create filled region
                    overlap_region = axes.get_riemann_rectangles(
                        graph=graph_f,
                        x_range=[overlap_start, overlap_end],
                        dx=0.05,
                        stroke_width=0,
                    )
                    overlap_region.set_fill(OVERLAP_COLOR, opacity=0.5)

                    self.play(
                        Transform(graph_g_orig, graph_g_shifted),
                        Transform(label_g_orig, label_g_shifted),
                        FadeIn(t_indicator),
                        FadeIn(overlap_region),
                        run_time=1.5
                    )
                    self.wait()
                    self.play(FadeOut(overlap_region), FadeOut(t_indicator))
                else:
                    self.play(
                        Transform(graph_g_orig, graph_g_shifted),
                        Transform(label_g_orig, label_g_shifted),
                        FadeIn(t_indicator),
                        run_time=1.5
                    )
                    self.wait()
                    self.play(FadeOut(t_indicator))
            else:
                self.play(
                    Transform(graph_g_orig, graph_g_shifted),
                    Transform(label_g_orig, label_g_shifted),
                    FadeIn(t_indicator),
                    run_time=1.5
                )
                self.wait()
                self.play(FadeOut(t_indicator))

        # ========================================
        # EXPLAIN: The overlap integral
        # ========================================
        self.play(FadeOut(instruction2))

        explanation = Tex(
            R"\text{Convolution} = \int f(\tau) \cdot g(t - \tau) \, d\tau",
            font_size=36,
            color=CONVOLUTION_COLOR
        )
        explanation.to_edge(DOWN, buff=0.8)

        self.play(Write(explanation))
        self.wait(3)

        # ========================================
        # CLEANUP
        # ========================================
        self.play(FadeOut(*self.mobjects), run_time=1)
        self.wait()


class ConvolutionGraph(InteractiveScene):
    """
    Part 3: Plot the complete convolution result.

    Narrative purpose:
        To show the full convolution function obtained by sliding through
        all positions and recording the overlap at each point.

    Mathematical content:
        Computes and displays (f*g)(t) for all t, showing how the output
        function emerges from the sliding overlap process.

    Visual approach:
        Show f and g above, with the convolution result plotted below.
        Optionally animate building up the convolution curve point by point.
    """
    def construct(self):
        # ========================================
        # SETUP: Title
        # ========================================
        title = OldTexText("The Convolution Result", font_size=48)
        title.to_edge(UP)

        self.play(FadeIn(title, shift=DOWN))
        self.wait()

        # ========================================
        # UPPER: Show f and g
        # ========================================
        axes_upper = Axes(
            x_range=[-1, 5, 1],
            y_range=[0, 1.2, 0.5],
            width=8,
            height=2,
        )
        axes_upper.shift(2 * UP)

        f = lambda x: box_function(x, center=1, width=1)
        g = lambda x: triangle_function(x, center=1.5, width=2)

        graph_f = create_function_graph(axes_upper, f, [0, 2], FUNCTION_F_COLOR)
        graph_g = create_function_graph(axes_upper, g, [0.5, 2.5], FUNCTION_G_COLOR)

        label_f = Tex("f(t)", font_size=28, color=FUNCTION_F_COLOR)
        label_g = Tex("g(t)", font_size=28, color=FUNCTION_G_COLOR)
        labels_upper = VGroup(label_f, label_g)
        labels_upper.arrange(RIGHT, buff=0.5)
        labels_upper.next_to(axes_upper, UP, buff=0.2)

        self.play(
            ShowCreation(axes_upper),
            ShowCreation(graph_f),
            ShowCreation(graph_g),
            Write(labels_upper)
        )
        self.wait()

        # ========================================
        # LOWER: Show convolution
        # ========================================
        axes_conv = Axes(
            x_range=[-1, 5, 1],
            y_range=[0, 0.8, 0.2],
            width=8,
            height=3,
        )
        axes_conv.shift(1.2 * DOWN)

        t_label = Tex("t", font_size=32)
        t_label.next_to(axes_conv.x_axis, RIGHT)

        label_conv = Tex("(f * g)(t)", font_size=32, color=CONVOLUTION_COLOR)
        label_conv.next_to(axes_conv, UP, buff=0.2)

        self.play(
            ShowCreation(axes_conv),
            Write(t_label),
            Write(label_conv)
        )
        self.wait()

        # ========================================
        # COMPUTE: Convolution
        # ========================================
        t_vals, conv_vals = compute_convolution(f, g, [-1, 5], dt=0.02)

        # Create convolution graph
        # Since we have discrete points, create parametric curve
        points = [axes_conv.c2p(t, c) for t, c in zip(t_vals, conv_vals)]
        graph_conv = VMobject()
        graph_conv.set_points_smoothly(points)
        graph_conv.set_stroke(CONVOLUTION_COLOR, width=4)

        self.play(ShowCreation(graph_conv), run_time=3)
        self.wait(2)

        # ========================================
        # HIGHLIGHT: Key features
        # ========================================
        observation = OldTexText(
            "The convolution smooths and spreads the functions!",
            font_size=28,
            color=YELLOW
        )
        observation.to_edge(DOWN, buff=0.5)

        self.play(Write(observation))
        self.wait(3)

        # ========================================
        # CLEANUP
        # ========================================
        self.play(FadeOut(*self.mobjects), run_time=1)
        self.wait()


class Applications(InteractiveScene):
    """
    Part 4: Show applications of convolution.

    Narrative purpose:
        To demonstrate why convolution matters by showing its applications
        in signal processing, image processing, and probability.

    Mathematical content:
        Mentions smoothing/filtering, edge detection, probability distributions
        (sum of random variables), and the convolution theorem (Fourier).

    Visual approach:
        List applications with brief visual examples, emphasizing the
        ubiquity and importance of convolution in mathematics and engineering.
    """
    def construct(self):
        # ========================================
        # SETUP: Title
        # ========================================
        title = OldTexText("Applications of Convolution", font_size=48)
        title.to_edge(UP)

        self.play(FadeIn(title, shift=DOWN))
        self.wait()

        # ========================================
        # LIST: Applications
        # ========================================
        apps_title = OldTexText("Where Convolution Appears:", font_size=36, weight=BOLD)
        apps_title.shift(1.5 * UP)

        self.play(Write(apps_title))
        self.wait()

        applications = VGroup(
            OldTexText("• Signal Processing: Filtering and smoothing", font_size=28),
            OldTexText("• Image Processing: Blurring, sharpening, edge detection", font_size=28),
            OldTexText("• Probability: Distribution of sum of random variables", font_size=28),
            OldTexText("• Physics: System response to input (linear systems)", font_size=28),
            OldTexText("• Neural Networks: Convolutional layers", font_size=28),
            OldTexText("• Audio: Reverb and acoustic effects", font_size=28),
        )
        applications.arrange(DOWN, buff=0.4, aligned_edge=LEFT)
        applications.next_to(apps_title, DOWN, buff=0.8)

        self.play(
            LaggedStart(
                *[FadeIn(app, shift=RIGHT) for app in applications],
                lag_ratio=0.4
            ),
            run_time=6
        )
        self.wait(3)

        # ========================================
        # FORMULA: Formal definition
        # ========================================
        self.play(
            FadeOut(apps_title),
            FadeOut(applications)
        )

        formula_title = OldTexText("The Convolution Formula", font_size=36, weight=BOLD)
        formula_title.shift(1.5 * UP)

        self.play(Write(formula_title))
        self.wait()

        # Continuous convolution
        continuous = Tex(
            R"(f * g)(t) = \int_{-\infty}^{\infty} f(\tau) g(t - \tau) \, d\tau",
            font_size=40
        )
        continuous.shift(0.3 * UP)

        continuous_label = OldTexText("Continuous:", font_size=28)
        continuous_label.next_to(continuous, LEFT, buff=0.5)

        self.play(
            Write(continuous_label),
            Write(continuous)
        )
        self.wait(2)

        # Discrete convolution
        discrete = Tex(
            R"(f * g)[n] = \sum_{m=-\infty}^{\infty} f[m] \cdot g[n - m]",
            font_size=40
        )
        discrete.next_to(continuous, DOWN, buff=0.8)

        discrete_label = OldTexText("Discrete:", font_size=28)
        discrete_label.next_to(discrete, LEFT, buff=0.5)

        self.play(
            Write(discrete_label),
            Write(discrete)
        )
        self.wait(3)

        # ========================================
        # KEY PROPERTY: Commutativity
        # ========================================
        property_text = Tex(
            R"f * g = g * f \quad \text{(commutative)}",
            font_size=32,
            color=GREEN
        )
        property_text.to_edge(DOWN, buff=1)

        self.play(Write(property_text))
        self.wait(2)

        # ========================================
        # FINAL MESSAGE
        # ========================================
        self.play(FadeOut(*self.mobjects))

        final = OldTexText(
            "Convolution: a fundamental operation\nthat combines functions through overlap!",
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
# Scene 1 (IntroduceFunctions):
#   - Shows two functions f and g
#   - Poses the question of combination
#   - Introduces convolution notation
#
# Scene 2 (SlidingProduct):
#   - Demonstrates flip-and-slide procedure
#   - Shows g(t-τ) at various positions
#   - Visualizes overlap integral
#
# Scene 3 (ConvolutionGraph):
#   - Plots the complete convolution result
#   - Shows how output emerges from process
#   - Highlights smoothing effect
#
# Scene 4 (Applications):
#   - Lists important applications
#   - Shows formal formulas (continuous/discrete)
#   - Emphasizes practical significance

SCENE_ORDER = [
    IntroduceFunctions,    # Part 1: Setup
    SlidingProduct,        # Part 2: The procedure
    ConvolutionGraph,      # Part 3: The result
    Applications,          # Part 4: Why it matters
]
