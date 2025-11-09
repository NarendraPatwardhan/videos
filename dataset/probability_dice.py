"""
Natural Group Name: Probability Distributions with Dice

Educational Objectives:
- To visualize probability distributions using dice as a concrete example
- To demonstrate how sum of two dice creates a triangle distribution
- To build intuition for why certain outcomes are more likely than others
- To introduce the Central Limit Theorem concept informally

Story Arc & Intent:
The animation reveals probability through the familiar example of dice: a
single die has uniform probability, but the sum of two dice creates a
triangle-shaped distribution. This shows how combining random variables
changes the probability landscape and hints at the Central Limit Theorem.

Narrative Flow:
- Hook/Opening: Rolling a single die - all outcomes equally likely
- Development: Rolling two dice and looking at their sum
- Build-up: Count the ways to get each sum, revealing different probabilities
- Climax: The triangle distribution emerges from the count
- Resolution: Hint at the Central Limit Theorem for many dice

Technical Implementation Notes:
- Scene Classes: SingleDie, TwoDiceSum, DistributionShape, CentralLimitHint
- Key Visual Elements: Die faces, bar charts, probability distributions
- Animation Techniques: Bar growth, counting visualization, distribution shaping
- Mathematical Concepts: Probability, discrete distributions, convolution, CLT

Dependency Chain:
All scenes use basic manimlib components: Rectangle, Text, Tex, Axes, bars.
No custom utilities required.

Rendering Instructions:
To render these scenes, use the manim command-line tool:
- For a single scene: manimgl probability_dice.py SingleDie
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
# - BLUE: Single die probabilities
# - YELLOW: Two dice probabilities
# - GREEN: Highlighted outcomes
# - RED: Die dots/pips
# - WHITE: Text and labels
# - GREY_A: De-emphasized elements
#
# Key Manim Constants Used:
# - UP, DOWN, LEFT, RIGHT: Direction vectors
# - ORIGIN: Center point
# - DEGREES: Angle conversion

# Die configuration
DIE_SIZE = 1.0
DOT_RADIUS = 0.08

# Probability bar chart configuration
BAR_WIDTH = 0.4
MAX_BAR_HEIGHT = 3.0

# ============================================================
# 3. UTILITY FUNCTIONS
# ============================================================

def create_die_face(value, size=DIE_SIZE, die_color=WHITE, dot_color=RED):
    """
    Create a die face showing a specific value (1-6).

    Args:
        value: Die value (1, 2, 3, 4, 5, or 6)
        size: Size of the die face
        die_color: Color of the die square
        dot_color: Color of the dots

    Returns:
        VGroup containing the die face
    """
    # Die square
    square = Square(side_length=size, color=die_color, stroke_width=3)
    square.set_fill(die_color, opacity=0.1)

    # Dot positions for each value
    dot_positions = {
        1: [(0, 0)],
        2: [(-0.25, 0.25), (0.25, -0.25)],
        3: [(-0.25, 0.25), (0, 0), (0.25, -0.25)],
        4: [(-0.25, 0.25), (0.25, 0.25), (-0.25, -0.25), (0.25, -0.25)],
        5: [(-0.25, 0.25), (0.25, 0.25), (0, 0), (-0.25, -0.25), (0.25, -0.25)],
        6: [(-0.25, 0.25), (0.25, 0.25), (-0.25, 0), (0.25, 0), (-0.25, -0.25), (0.25, -0.25)]
    }

    # Create dots
    dots = VGroup()
    for x, y in dot_positions[value]:
        dot = Dot(np.array([x * size, y * size, 0]), radius=DOT_RADIUS, color=dot_color)
        dot.set_fill(dot_color, opacity=1)
        dots.add(dot)

    return VGroup(square, dots)

def create_probability_bar(height, width=BAR_WIDTH, color=BLUE):
    """
    Create a probability bar for a bar chart.

    Args:
        height: Height of the bar (probability)
        width: Width of the bar
        color: Color of the bar

    Returns:
        Rectangle mobject
    """
    bar = Rectangle(
        width=width,
        height=height,
        stroke_width=2,
        stroke_color=color,
        fill_color=color,
        fill_opacity=0.7
    )
    bar.align_to(ORIGIN, DOWN)

    return bar

def count_ways_to_sum(target_sum):
    """
    Count the number of ways to get a sum with two dice.

    Args:
        target_sum: Target sum (2 through 12)

    Returns:
        Number of ways to achieve that sum
    """
    count = 0
    for die1 in range(1, 7):
        for die2 in range(1, 7):
            if die1 + die2 == target_sum:
                count += 1
    return count

def get_two_dice_probability(target_sum):
    """
    Get probability of a sum with two dice.

    Args:
        target_sum: Target sum (2 through 12)

    Returns:
        Probability (between 0 and 1)
    """
    return count_ways_to_sum(target_sum) / 36

# ============================================================
# 4. BASE CLASSES AND HELPERS
# ============================================================
# No custom base classes needed

# ============================================================
# 5. SCENE IMPLEMENTATIONS
# ============================================================

class SingleDie(InteractiveScene):
    """
    Part 1: Show the probability distribution for a single die.

    Narrative purpose:
        To establish the concept of a uniform probability distribution
        using the familiar example of a fair six-sided die.

    Mathematical content:
        A fair die has probability 1/6 for each outcome (1, 2, 3, 4, 5, 6).
        This is a discrete uniform distribution.

    Visual approach:
        Show all six die faces, then display a bar chart showing equal
        probability (1/6) for each outcome.
    """
    def construct(self):
        # ========================================
        # SETUP: Title
        # ========================================
        title = Text("Probability: Rolling a Die", font_size=48)
        title.to_edge(UP)

        self.play(FadeIn(title, shift=DOWN))
        self.wait()

        # ========================================
        # SHOW: All six die faces
        # ========================================
        dice_faces = VGroup(*[create_die_face(i, size=0.8) for i in range(1, 7)])
        dice_faces.arrange(RIGHT, buff=0.5)
        dice_faces.shift(1.5 * UP)

        self.play(LaggedStart(*[FadeIn(die, scale=0.5) for die in dice_faces], lag_ratio=0.2))
        self.wait()

        # ========================================
        # EXPLAIN: Equal probability
        # ========================================
        explanation = Text(
            "Each outcome has equal probability",
            font_size=32,
            color=GREY_A
        )
        explanation.next_to(dice_faces, DOWN, buff=0.5)

        self.play(FadeIn(explanation, shift=UP))
        self.wait()

        # ========================================
        # SHOW: Probability bar chart
        # ========================================
        self.play(FadeOut(explanation))

        # Create bars
        prob = 1 / 6
        bar_height = prob * MAX_BAR_HEIGHT

        bars = VGroup()
        labels = VGroup()

        for i in range(1, 7):
            bar = create_probability_bar(bar_height, color=BLUE)
            bar.shift((i - 3.5) * (BAR_WIDTH + 0.2) * RIGHT + 1 * DOWN)
            bars.add(bar)

            label = Text(str(i), font_size=24)
            label.next_to(bar, DOWN, buff=0.2)
            labels.add(label)

        self.play(
            LaggedStart(*[GrowFromEdge(bar, DOWN) for bar in bars], lag_ratio=0.1),
            LaggedStart(*[FadeIn(label) for label in labels], lag_ratio=0.1),
            run_time=2
        )
        self.wait()

        # ========================================
        # LABEL: The probability
        # ========================================
        prob_label = Tex(
            f"P(\\text{{each}}) = \\frac{{1}}{{6}} \\approx {prob:.3f}",
            font_size=36,
            color=BLUE
        )
        prob_label.to_edge(DOWN, buff=0.8)

        self.play(Write(prob_label))
        self.wait(2)

        # ========================================
        # OBSERVATION: Uniform
        # ========================================
        observation = Text(
            "This is a uniform distribution",
            font_size=32,
            color=GREY_A
        )
        observation.next_to(prob_label, DOWN, buff=0.3)

        self.play(FadeIn(observation, shift=UP))
        self.wait(2)


class TwoDiceSum(InteractiveScene):
    """
    Part 2: Show the sum of two dice and count the ways.

    Narrative purpose:
        To demonstrate that when we sum two dice, different outcomes
        have different numbers of ways to occur, creating unequal probabilities.

    Mathematical content:
        Sum of two dice ranges from 2 to 12. The number of ways to
        achieve each sum varies: 7 is most likely (6 ways), 2 and 12
        are least likely (1 way each).

    Visual approach:
        Show two dice, then systematically count the ways to get each
        possible sum (2 through 12).
    """
    def construct(self):
        # ========================================
        # SETUP: Title
        # ========================================
        title = Text("Sum of Two Dice", font_size=48)
        title.to_edge(UP)

        self.add(title)

        # ========================================
        # SHOW: Two dice
        # ========================================
        die1 = create_die_face(3, size=1.2)
        die2 = create_die_face(4, size=1.2)

        dice = VGroup(die1, die2)
        dice.arrange(RIGHT, buff=1)
        dice.shift(1.5 * UP)

        plus = Tex("+", font_size=72)
        plus.move_to((die1.get_center() + die2.get_center()) / 2)

        self.play(
            FadeIn(die1, scale=0.5),
            FadeIn(die2, scale=0.5)
        )
        self.play(Write(plus))
        self.wait()

        # ========================================
        # SHOW: The sum
        # ========================================
        sum_value = 7  # 3 + 4
        sum_text = Tex(f"= {sum_value}", font_size=72, color=GREEN)
        sum_text.next_to(dice, RIGHT, buff=0.5)

        self.play(Write(sum_text))
        self.wait()

        # ========================================
        # QUESTION: What are all possible sums?
        # ========================================
        question = Text(
            "What are all the possible sums?",
            font_size=32,
            color=GREY_A
        )
        question.shift(0.5 * DOWN)

        self.play(FadeIn(question, shift=UP))
        self.wait()

        # ========================================
        # SHOW: Range of sums
        # ========================================
        self.play(FadeOut(question))

        range_text = Text(
            "Possible sums: 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12",
            font_size=32,
            color=YELLOW
        )
        range_text.shift(0.5 * DOWN)

        self.play(FadeIn(range_text, shift=UP))
        self.wait()

        # ========================================
        # COUNT: Ways to get sum = 7
        # ========================================
        self.play(FadeOut(range_text))

        count_label = Text(
            f"How many ways to get {sum_value}?",
            font_size=32,
            color=GREY_A
        )
        count_label.shift(0.5 * DOWN)

        self.play(FadeIn(count_label, shift=UP))
        self.wait()

        # Show the combinations
        combinations = [
            (1, 6), (2, 5), (3, 4), (4, 3), (5, 2), (6, 1)
        ]

        combo_text = Tex(
            "(1,6), (2,5), (3,4), (4,3), (5,2), (6,1)",
            font_size=28,
            color=GREEN
        )
        combo_text.next_to(count_label, DOWN, buff=0.3)

        self.play(Write(combo_text))
        self.wait()

        # Count
        count_result = Tex(
            f"\\text{{{len(combinations)} ways}}",
            font_size=36,
            color=GREEN
        )
        count_result.next_to(combo_text, DOWN, buff=0.3)

        self.play(FadeIn(count_result, scale=1.3))
        self.wait(2)


class DistributionShape(InteractiveScene):
    """
    Part 3: Show the complete probability distribution (triangle shape).

    Narrative purpose:
        To reveal the beautiful triangle-shaped distribution that emerges
        when we count all the ways to achieve each sum.

    Mathematical content:
        P(sum = k) = (ways to get k) / 36
        The distribution is symmetric around 7, with probabilities
        increasing then decreasing, forming a triangle.

    Visual approach:
        Display a bar chart with all sums (2-12), showing the
        characteristic triangle shape of the distribution.
    """
    def construct(self):
        # ========================================
        # SETUP: Title
        # ========================================
        title = Text("Probability Distribution", font_size=48)
        title.to_edge(UP)

        self.add(title)

        # ========================================
        # CREATE: Full probability distribution
        # ========================================
        sums = list(range(2, 13))  # 2 through 12
        ways = [count_ways_to_sum(s) for s in sums]
        probs = [w / 36 for w in ways]

        # Create bars
        bars = VGroup()
        labels = VGroup()
        prob_labels = VGroup()

        for i, (s, w, p) in enumerate(zip(sums, ways, probs)):
            # Bar height proportional to probability
            bar_height = p * MAX_BAR_HEIGHT * 2

            bar = create_probability_bar(bar_height, color=YELLOW, width=0.35)
            bar.shift((i - 5) * 0.5 * RIGHT + 0.5 * DOWN)
            bars.add(bar)

            # Sum label
            label = Text(str(s), font_size=20)
            label.next_to(bar, DOWN, buff=0.15)
            labels.add(label)

            # Ways label (on top of bar)
            ways_label = Text(f"{w}", font_size=18, color=WHITE)
            ways_label.next_to(bar, UP, buff=0.1)
            prob_labels.add(ways_label)

        # ========================================
        # ANIMATE: Build the distribution
        # ========================================
        self.play(
            LaggedStart(*[GrowFromEdge(bar, DOWN) for bar in bars], lag_ratio=0.08),
            LaggedStart(*[FadeIn(label) for label in labels], lag_ratio=0.08),
            run_time=3
        )
        self.wait()

        self.play(
            LaggedStart(*[FadeIn(pl, shift=DOWN) for pl in prob_labels], lag_ratio=0.08),
            run_time=2
        )
        self.wait()

        # ========================================
        # HIGHLIGHT: The shape
        # ========================================
        shape_label = Text(
            "Triangle Distribution!",
            font_size=40,
            color=GREEN
        )
        shape_label.to_edge(DOWN, buff=0.8)

        arrow1 = Arrow(shape_label.get_top(), bars[5].get_bottom(), color=GREEN, stroke_width=3)

        self.play(
            FadeIn(shape_label, scale=1.3),
            GrowArrow(arrow1)
        )
        self.wait()

        # ========================================
        # EXPLAIN: Why this shape?
        # ========================================
        self.play(
            FadeOut(arrow1),
            FadeOut(shape_label)
        )

        explanation = VGroup(
            Text("Why this shape?", font_size=32, weight=BOLD),
            Text("• More ways to get middle values (like 7)", font_size=26),
            Text("• Fewer ways to get extremes (like 2 or 12)", font_size=26),
            Text("• Symmetric around the center", font_size=26)
        )
        explanation.arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        explanation.to_edge(DOWN, buff=0.3)

        self.play(FadeIn(explanation, shift=UP, lag_ratio=0.2))
        self.wait(3)


class CentralLimitHint(InteractiveScene):
    """
    Part 4: Hint at the Central Limit Theorem with many dice.

    Narrative purpose:
        To extend the pattern and hint at the Central Limit Theorem:
        as we sum more dice, the distribution approaches a bell curve.

    Mathematical content:
        Central Limit Theorem (informal): The sum of many independent
        random variables approaches a normal (Gaussian) distribution.

    Visual approach:
        Show how the distribution evolves: 1 die (uniform), 2 dice (triangle),
        3+ dice (approaching bell curve), introducing the CLT concept.
    """
    def construct(self):
        # ========================================
        # SETUP: Title
        # ========================================
        title = Text("What About More Dice?", font_size=48)
        title.to_edge(UP)

        self.add(title)

        # ========================================
        # SHOW: Evolution of distributions
        # ========================================
        distributions_label = VGroup(
            Text("1 die: Uniform", font_size=32),
            Text("2 dice: Triangle", font_size=32),
            Text("3+ dice: Bell curve!", font_size=32, color=GREEN)
        )
        distributions_label.arrange(DOWN, aligned_edge=LEFT, buff=0.4)
        distributions_label.shift(2 * UP + 3 * LEFT)

        self.play(FadeIn(distributions_label, shift=RIGHT, lag_ratio=0.3))
        self.wait()

        # ========================================
        # DRAW: Stylized bell curve
        # ========================================
        # Simple bell curve illustration
        axes = Axes(
            x_range=(0, 10, 1),
            y_range=(0, 1, 0.5),
            width=6,
            height=3,
            axis_config={"include_tip": False}
        )
        axes.shift(1.5 * RIGHT + 0.3 * DOWN)

        bell_curve = axes.get_graph(
            lambda x: 0.8 * np.exp(-0.5 * ((x - 5) / 1.5) ** 2),
            x_range=(1, 9),
            color=GREEN
        )

        bell_label = Text("Normal Distribution", font_size=28, color=GREEN)
        bell_label.next_to(bell_curve, UP, buff=0.3)

        self.play(
            ShowCreation(axes),
            ShowCreation(bell_curve),
            run_time=2
        )
        self.play(FadeIn(bell_label, shift=DOWN))
        self.wait()

        # ========================================
        # THEOREM: Central Limit Theorem
        # ========================================
        theorem_box = VGroup(
            Text("Central Limit Theorem", font_size=36, weight=BOLD, color=YELLOW),
            Text("The sum of many random variables", font_size=26),
            Text("approaches a normal distribution", font_size=26),
            Text("(regardless of the original distribution!)", font_size=24, color=GREY_A)
        )
        theorem_box.arrange(DOWN, buff=0.25)
        theorem_box.to_edge(DOWN, buff=0.5)

        box = SurroundingRectangle(theorem_box, buff=0.3, color=YELLOW, stroke_width=3)

        self.play(
            FadeIn(theorem_box, shift=UP, lag_ratio=0.2),
            ShowCreation(box)
        )
        self.wait(3)

        # ========================================
        # FINALE: Checkmark
        # ========================================
        checkmark = Tex("\\checkmark", font_size=72, color=GREEN)
        checkmark.next_to(box, RIGHT, buff=0.5)

        self.play(FadeIn(checkmark, scale=2))
        self.wait(2)


# ============================================================
# 6. SCENE EXECUTION ORDER
# ============================================================
# The order of scenes that tells the story.
#
# Scene 1 (SingleDie):
#   - Shows probability distribution for a single die
#   - Demonstrates uniform distribution (equal probabilities)
#   - Establishes P = 1/6 for each outcome
#
# Scene 2 (TwoDiceSum):
#   - Introduces the sum of two dice
#   - Shows that different sums have different numbers of ways to occur
#   - Counts ways to get sum = 7 as an example
#
# Scene 3 (DistributionShape):
#   - Shows complete probability distribution for two dice
#   - Reveals the triangle shape
#   - Explains why middle values are more likely
#
# Scene 4 (CentralLimitHint):
#   - Shows progression: uniform → triangle → bell curve
#   - Introduces the Central Limit Theorem concept
#   - Demonstrates that sums approach normal distribution

SCENE_ORDER = [
    SingleDie,              # Part 1: Single die (uniform)
    TwoDiceSum,             # Part 2: Sum of two dice
    DistributionShape,      # Part 3: Triangle distribution
    CentralLimitHint,       # Part 4: Central Limit Theorem
]
