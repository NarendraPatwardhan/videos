"""
Natural Group Name: Bayes' Theorem Visualization

Educational Objectives:
- To introduce Bayes' theorem and conditional probability
- To build intuition through visual representations (tree diagrams and areas)
- To demonstrate with the classic medical test example
- To show how prior probabilities affect posterior probabilities

Story Arc & Intent:
The animation makes Bayes' theorem intuitive by showing how we update our
beliefs based on new evidence. Using the medical test example, we see how
even accurate tests can give misleading results when base rates are low,
making this crucial theorem both understandable and memorable.

Narrative Flow:
- Hook/Opening: Pose a probability puzzle (positive test result)
- Development: Introduce conditional probability concepts
- Build-up: Show tree diagrams and area representations
- Climax: Derive and apply Bayes' theorem to the medical test
- Resolution: Reveal the surprising answer and explain the intuition
- Extension: Discuss base rate neglect and practical importance

Technical Implementation Notes:
- Scene Classes: ProbabilityIntro, ConditionalProbability, BayesFormula, MedicalTest
- Key Visual Elements: Tree diagrams, area rectangles, probability labels, equations
- Animation Techniques: Tree construction, area subdivision, highlighting
- Mathematical Concepts: Conditional probability, Bayes' theorem, base rates

Dependency Chain:
All scenes are independent. They use Rectangle, Tree diagrams (via lines/arrows),
and Tex from manimlib. Utility functions handle probability calculations.

Rendering Instructions:
To render these scenes, use the manim command-line tool:
- For a single scene: manimgl bayes_theorem.py ProbabilityIntro
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
# Colors for probability visualization
DISEASE_COLOR = RED
NO_DISEASE_COLOR = GREEN
POSITIVE_TEST_COLOR = YELLOW
NEGATIVE_TEST_COLOR = BLUE

# Tree diagram configuration
TREE_X_SPACING = 3.5
TREE_Y_SPACING = 2.0

# ============================================================
# 3. UTILITY FUNCTIONS
# ============================================================

def format_probability(p):
    """
    Format probability as percentage or fraction.

    Args:
        p: Probability value (0 to 1)

    Returns:
        Formatted string
    """
    if p < 0.01:
        return f"{p:.3f}"
    elif p < 1:
        return f"{p:.2%}"
    else:
        return "100%"

def create_prob_label(text, prob, color=WHITE, font_size=28):
    """
    Create a probability label with text and value.

    Args:
        text: Description text
        prob: Probability value
        color: Text color
        font_size: Font size

    Returns:
        VGroup with text and probability
    """
    label = VGroup(
        Text(text, font_size=font_size, color=color),
        Tex(f"= {format_probability(prob)}", font_size=font_size, color=color)
    )
    label.arrange(RIGHT, buff=0.3)
    return label

def bayes_theorem(prior, likelihood, evidence):
    """
    Calculate posterior probability using Bayes' theorem.

    P(A|B) = P(B|A) * P(A) / P(B)

    Args:
        prior: P(A) - prior probability
        likelihood: P(B|A) - likelihood
        evidence: P(B) - probability of evidence

    Returns:
        Posterior probability P(A|B)
    """
    return (likelihood * prior) / evidence

# ============================================================
# 4. BASE CLASSES AND HELPERS
# ============================================================
# No custom base classes needed

# ============================================================
# 5. SCENE IMPLEMENTATIONS
# ============================================================

class ProbabilityIntro(InteractiveScene):
    """
    Part 1: Introduce the medical test problem.

    Narrative purpose:
        To pose an intriguing probability puzzle that will motivate
        learning Bayes' theorem: interpreting a positive medical test.

    Mathematical content:
        Sets up the scenario: rare disease (1% prevalence), accurate test
        (95% sensitivity, 90% specificity). What if you test positive?

    Visual approach:
        Present the scenario clearly with visual aids, pose the question,
        and set up the framework for solving it.
    """
    def construct(self):
        # ========================================
        # SETUP: Title
        # ========================================
        title = Text("Bayes' Theorem", font_size=48)
        title.to_edge(UP)

        self.play(FadeIn(title, shift=DOWN))
        self.wait()

        # ========================================
        # SCENARIO: Medical test problem
        # ========================================
        scenario_title = Text("Medical Test Scenario", font_size=36, weight=BOLD)
        scenario_title.shift(1.5 * UP)

        self.play(Write(scenario_title))
        self.wait()

        # ========================================
        # FACTS: Set up the problem
        # ========================================
        facts = VGroup(
            Text("• Disease prevalence: 1% of population", font_size=28),
            Text("• Test sensitivity: 95% (detects disease when present)", font_size=28),
            Text("• Test specificity: 90% (negative when disease absent)", font_size=28),
            Text("", font_size=20),
            Text("You test POSITIVE. What's the probability you have the disease?",
                 font_size=28, color=YELLOW, weight=BOLD),
        )
        facts.arrange(DOWN, buff=0.4, aligned_edge=LEFT)
        facts.next_to(scenario_title, DOWN, buff=0.8)

        self.play(
            LaggedStart(
                *[FadeIn(fact, shift=RIGHT) for fact in facts],
                lag_ratio=0.5
            ),
            run_time=5
        )
        self.wait(3)

        # ========================================
        # INTUITION: Common wrong answer
        # ========================================
        wrong_answer = Text(
            "Common intuition: ~95% (test is 95% accurate)",
            font_size=28,
            color=RED
        )
        wrong_answer.to_edge(DOWN, buff=1.5)

        question_mark = Tex("?", font_size=60, color=RED)
        question_mark.next_to(wrong_answer, RIGHT, buff=0.5)

        self.play(
            Write(wrong_answer),
            FadeIn(question_mark, scale=2)
        )
        self.wait(3)

        # ========================================
        # PREVIEW: Actual answer is surprising
        # ========================================
        hint = Text(
            "The actual answer might surprise you...",
            font_size=32,
            color=GREEN
        )
        hint.next_to(wrong_answer, UP, buff=0.5)

        self.play(Write(hint))
        self.wait(3)

        # ========================================
        # CLEANUP
        # ========================================
        self.play(FadeOut(*self.mobjects), run_time=1)
        self.wait()


class ConditionalProbability(InteractiveScene):
    """
    Part 2: Explain conditional probability with tree diagram.

    Narrative purpose:
        To introduce conditional probability notation and use a tree
        diagram to organize the information systematically.

    Mathematical content:
        Shows P(D) = 0.01, P(~D) = 0.99
        P(+|D) = 0.95, P(-|D) = 0.05
        P(+|~D) = 0.10, P(-|~D) = 0.90
        Calculates all joint probabilities.

    Visual approach:
        Build a probability tree showing all branches and outcomes,
        labeling each with appropriate probabilities.
    """
    def construct(self):
        # ========================================
        # SETUP: Title
        # ========================================
        title = Text("Probability Tree Diagram", font_size=48)
        title.to_edge(UP)

        self.play(FadeIn(title, shift=DOWN))
        self.wait()

        # ========================================
        # NOTATION: Define events
        # ========================================
        notation = VGroup(
            Tex(R"D = \text{has disease}", font_size=28, color=DISEASE_COLOR),
            Tex(R"\sim D = \text{no disease}", font_size=28, color=NO_DISEASE_COLOR),
            Tex(R"+ = \text{positive test}", font_size=28, color=POSITIVE_TEST_COLOR),
            Tex(R"- = \text{negative test}", font_size=28, color=NEGATIVE_TEST_COLOR),
        )
        notation.arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        notation.to_corner(UL, buff=0.7)

        self.play(
            LaggedStart(
                *[FadeIn(n, shift=DOWN) for n in notation],
                lag_ratio=0.3
            )
        )
        self.wait(2)

        # ========================================
        # BUILD: Probability tree
        # ========================================
        # Start point
        start = Dot(ORIGIN, radius=0.1, color=WHITE)
        start.shift(4 * LEFT)

        self.play(FadeIn(start))
        self.wait()

        # First level: Disease or No Disease
        # Branch to D
        d_point = Dot(color=DISEASE_COLOR, radius=0.1)
        d_point.shift(2 * LEFT + 1.5 * UP)

        d_line = Line(start.get_center(), d_point.get_center(), color=DISEASE_COLOR, stroke_width=3)
        d_label = Tex("D", font_size=32, color=DISEASE_COLOR)
        d_label.next_to(d_point, LEFT, buff=0.2)
        d_prob = Tex("0.01", font_size=24, color=DISEASE_COLOR)
        d_prob.next_to(d_line, UP, buff=0.1)

        self.play(
            ShowCreation(d_line),
            FadeIn(d_point),
            Write(d_label),
            Write(d_prob)
        )
        self.wait()

        # Branch to ~D
        nd_point = Dot(color=NO_DISEASE_COLOR, radius=0.1)
        nd_point.shift(2 * LEFT + 1.5 * DOWN)

        nd_line = Line(start.get_center(), nd_point.get_center(), color=NO_DISEASE_COLOR, stroke_width=3)
        nd_label = Tex(R"\sim D", font_size=32, color=NO_DISEASE_COLOR)
        nd_label.next_to(nd_point, LEFT, buff=0.2)
        nd_prob = Tex("0.99", font_size=24, color=NO_DISEASE_COLOR)
        nd_prob.next_to(nd_line, DOWN, buff=0.1)

        self.play(
            ShowCreation(nd_line),
            FadeIn(nd_point),
            Write(nd_label),
            Write(nd_prob)
        )
        self.wait()

        # ========================================
        # Second level: Test results given D
        # ========================================
        # D -> + (True Positive)
        d_pos_point = Dot(color=POSITIVE_TEST_COLOR, radius=0.08)
        d_pos_point.shift(1.5 * RIGHT + 2 * UP)

        d_pos_line = Line(d_point.get_center(), d_pos_point.get_center(),
                         color=POSITIVE_TEST_COLOR, stroke_width=2)
        d_pos_label = Tex("+", font_size=28, color=POSITIVE_TEST_COLOR)
        d_pos_label.next_to(d_pos_point, RIGHT, buff=0.15)
        d_pos_prob = Tex("0.95", font_size=20, color=POSITIVE_TEST_COLOR)
        d_pos_prob.next_to(d_pos_line, UP, buff=0.05)

        # D -> - (False Negative)
        d_neg_point = Dot(color=NEGATIVE_TEST_COLOR, radius=0.08)
        d_neg_point.shift(1.5 * RIGHT + 1 * UP)

        d_neg_line = Line(d_point.get_center(), d_neg_point.get_center(),
                         color=NEGATIVE_TEST_COLOR, stroke_width=2)
        d_neg_label = Tex("-", font_size=28, color=NEGATIVE_TEST_COLOR)
        d_neg_label.next_to(d_neg_point, RIGHT, buff=0.15)
        d_neg_prob = Tex("0.05", font_size=20, color=NEGATIVE_TEST_COLOR)
        d_neg_prob.next_to(d_neg_line, DOWN, buff=0.05)

        self.play(
            ShowCreation(d_pos_line),
            ShowCreation(d_neg_line),
            FadeIn(d_pos_point),
            FadeIn(d_neg_point),
            Write(d_pos_label),
            Write(d_neg_label),
            Write(d_pos_prob),
            Write(d_neg_prob)
        )
        self.wait()

        # ========================================
        # Second level: Test results given ~D
        # ========================================
        # ~D -> + (False Positive)
        nd_pos_point = Dot(color=POSITIVE_TEST_COLOR, radius=0.08)
        nd_pos_point.shift(1.5 * RIGHT + 1 * DOWN)

        nd_pos_line = Line(nd_point.get_center(), nd_pos_point.get_center(),
                          color=POSITIVE_TEST_COLOR, stroke_width=2)
        nd_pos_label = Tex("+", font_size=28, color=POSITIVE_TEST_COLOR)
        nd_pos_label.next_to(nd_pos_point, RIGHT, buff=0.15)
        nd_pos_prob = Tex("0.10", font_size=20, color=POSITIVE_TEST_COLOR)
        nd_pos_prob.next_to(nd_pos_line, UP, buff=0.05)

        # ~D -> - (True Negative)
        nd_neg_point = Dot(color=NEGATIVE_TEST_COLOR, radius=0.08)
        nd_neg_point.shift(1.5 * RIGHT + 2 * DOWN)

        nd_neg_line = Line(nd_point.get_center(), nd_neg_point.get_center(),
                          color=NEGATIVE_TEST_COLOR, stroke_width=2)
        nd_neg_label = Tex("-", font_size=28, color=NEGATIVE_TEST_COLOR)
        nd_neg_label.next_to(nd_neg_point, RIGHT, buff=0.15)
        nd_neg_prob = Tex("0.90", font_size=20, color=NEGATIVE_TEST_COLOR)
        nd_neg_prob.next_to(nd_neg_line, DOWN, buff=0.05)

        self.play(
            ShowCreation(nd_pos_line),
            ShowCreation(nd_neg_line),
            FadeIn(nd_pos_point),
            FadeIn(nd_neg_point),
            Write(nd_pos_label),
            Write(nd_neg_label),
            Write(nd_pos_prob),
            Write(nd_neg_prob)
        )
        self.wait(2)

        # ========================================
        # HIGHLIGHT: Joint probabilities
        # ========================================
        joint_title = Text("Joint Probabilities (multiply along paths):", font_size=24)
        joint_title.to_edge(DOWN, buff=2)

        joint_calcs = VGroup(
            Tex(R"P(D \text{ and } +) = 0.01 \times 0.95 = 0.0095", font_size=22),
            Tex(R"P(\sim D \text{ and } +) = 0.99 \times 0.10 = 0.099", font_size=22),
        )
        joint_calcs.arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        joint_calcs.next_to(joint_title, DOWN, buff=0.3)

        self.play(
            Write(joint_title),
            LaggedStart(
                *[Write(calc) for calc in joint_calcs],
                lag_ratio=0.5
            )
        )
        self.wait(3)

        # ========================================
        # CLEANUP
        # ========================================
        self.play(FadeOut(*self.mobjects), run_time=1)
        self.wait()


class BayesFormula(InteractiveScene):
    """
    Part 3: Derive and state Bayes' theorem.

    Narrative purpose:
        To formally introduce Bayes' theorem and show how it's derived
        from the definition of conditional probability.

    Mathematical content:
        Derives P(A|B) = P(B|A) * P(A) / P(B) from P(A and B) = P(B|A) * P(A)
        Shows the expanded form with law of total probability.

    Visual approach:
        Step-by-step algebraic derivation with clear highlighting,
        then present the final formula in a prominent box.
    """
    def construct(self):
        # ========================================
        # SETUP: Title
        # ========================================
        title = Text("Deriving Bayes' Theorem", font_size=48)
        title.to_edge(UP)

        self.play(FadeIn(title, shift=DOWN))
        self.wait()

        # ========================================
        # START: Conditional probability definition
        # ========================================
        step1 = Tex(
            R"P(A|B) = \frac{P(A \text{ and } B)}{P(B)}",
            font_size=40
        )
        step1.shift(1.5 * UP)

        step1_label = Text("Definition of conditional probability", font_size=24, color=GREY_A)
        step1_label.next_to(step1, DOWN, buff=0.3)

        self.play(
            Write(step1),
            Write(step1_label)
        )
        self.wait(2)

        # ========================================
        # SUBSTITUTE: P(A and B)
        # ========================================
        step2 = Tex(
            R"P(A \text{ and } B) = P(B|A) \cdot P(A)",
            font_size=36
        )
        step2.next_to(step1_label, DOWN, buff=0.7)

        step2_label = Text("Also from conditional probability", font_size=24, color=GREY_A)
        step2_label.next_to(step2, DOWN, buff=0.3)

        self.play(
            Write(step2),
            Write(step2_label)
        )
        self.wait(2)

        # ========================================
        # COMBINE: Get Bayes' theorem
        # ========================================
        step3 = Tex(
            R"P(A|B) = \frac{P(B|A) \cdot P(A)}{P(B)}",
            font_size=44,
            color=YELLOW
        )
        step3.next_to(step2_label, DOWN, buff=0.9)

        box = SurroundingRectangle(step3, buff=0.3, color=YELLOW, stroke_width=4)

        bayes_label = Text("Bayes' Theorem!", font_size=32, color=YELLOW, weight=BOLD)
        bayes_label.next_to(box, DOWN, buff=0.4)

        self.play(
            Write(step3),
            ShowCreation(box),
            Write(bayes_label)
        )
        self.wait(3)

        # ========================================
        # INTERPRET: Each term
        # ========================================
        self.play(
            FadeOut(step1),
            FadeOut(step1_label),
            FadeOut(step2),
            FadeOut(step2_label),
            VGroup(step3, box, bayes_label).animate.shift(2 * UP)
        )

        interpretations = VGroup(
            Tex(R"P(A|B) = \text{posterior (what we want)}", font_size=28),
            Tex(R"P(B|A) = \text{likelihood (test accuracy)}", font_size=28),
            Tex(R"P(A) = \text{prior (base rate)}", font_size=28),
            Tex(R"P(B) = \text{evidence (total probability of } B)", font_size=28),
        )
        interpretations.arrange(DOWN, buff=0.4, aligned_edge=LEFT)
        interpretations.shift(0.5 * DOWN)

        self.play(
            LaggedStart(
                *[FadeIn(interp, shift=RIGHT) for interp in interpretations],
                lag_ratio=0.4
            ),
            run_time=4
        )
        self.wait(4)

        # ========================================
        # CLEANUP
        # ========================================
        self.play(FadeOut(*self.mobjects), run_time=1)
        self.wait()


class MedicalTest(InteractiveScene):
    """
    Part 4: Solve the medical test problem using Bayes' theorem.

    Narrative purpose:
        To apply Bayes' theorem to our original question and reveal
        the surprising answer, explaining why intuition often fails.

    Mathematical content:
        P(D|+) = P(+|D) * P(D) / P(+)
        Where P(+) = P(+|D)*P(D) + P(+|~D)*P(~D)
        Calculate: 0.95 * 0.01 / (0.95*0.01 + 0.10*0.99) ≈ 0.087 or 8.7%

    Visual approach:
        Show the calculation step-by-step with clear visuals, then
        explain why the answer is so much lower than expected (base rate).
    """
    def construct(self):
        # ========================================
        # SETUP: Title
        # ========================================
        title = Text("Solving the Medical Test Problem", font_size=48)
        title.to_edge(UP)

        self.play(FadeIn(title, shift=DOWN))
        self.wait()

        # ========================================
        # REMIND: The question
        # ========================================
        question = Text(
            "You tested positive. What's P(Disease | Positive)?",
            font_size=32,
            color=YELLOW
        )
        question.next_to(title, DOWN, buff=0.7)

        self.play(Write(question))
        self.wait(2)

        # ========================================
        # FORMULA: Apply Bayes
        # ========================================
        formula = Tex(
            R"P(D|+) = \frac{P(+|D) \cdot P(D)}{P(+)}",
            font_size=40
        )
        formula.shift(1 * UP)

        self.play(Write(formula))
        self.wait()

        # ========================================
        # CALCULATE: Numerator
        # ========================================
        numerator = Tex(
            R"P(+|D) \cdot P(D) = 0.95 \times 0.01 = 0.0095",
            font_size=32
        )
        numerator.next_to(formula, DOWN, buff=0.7)

        self.play(Write(numerator))
        self.wait(2)

        # ========================================
        # CALCULATE: Denominator (total probability)
        # ========================================
        denominator_formula = Tex(
            R"P(+) = P(+|D) \cdot P(D) + P(+|\sim D) \cdot P(\sim D)",
            font_size=28
        )
        denominator_formula.next_to(numerator, DOWN, buff=0.5)

        self.play(Write(denominator_formula))
        self.wait()

        denominator_calc = Tex(
            R"= 0.95 \times 0.01 + 0.10 \times 0.99 = 0.0095 + 0.099 = 0.1085",
            font_size=28
        )
        denominator_calc.next_to(denominator_formula, DOWN, buff=0.3)

        self.play(Write(denominator_calc))
        self.wait(2)

        # ========================================
        # FINAL ANSWER
        # ========================================
        final_calc = Tex(
            R"P(D|+) = \frac{0.0095}{0.1085} \approx 0.0876",
            font_size=36
        )
        final_calc.next_to(denominator_calc, DOWN, buff=0.7)

        self.play(Write(final_calc))
        self.wait()

        answer = Tex(
            R"\approx 8.8\%",
            font_size=60,
            color=GREEN
        )
        answer.next_to(final_calc, DOWN, buff=0.5)

        answer_box = SurroundingRectangle(answer, buff=0.3, color=GREEN, stroke_width=4)

        self.play(
            Write(answer),
            ShowCreation(answer_box)
        )
        self.wait(3)

        # ========================================
        # SURPRISE: Much lower than expected!
        # ========================================
        surprise = Text(
            "Only 8.8%, not 95%!",
            font_size=36,
            color=RED,
            weight=BOLD
        )
        surprise.to_edge(DOWN, buff=1)

        self.play(FadeIn(surprise, scale=1.3))
        self.wait(2)

        # ========================================
        # EXPLAIN: Why so low?
        # ========================================
        self.play(FadeOut(*self.mobjects[2:]))  # Keep title and question

        explanation_title = Text("Why So Low?", font_size=40, weight=BOLD)
        explanation_title.shift(1.5 * UP)

        self.play(Write(explanation_title))
        self.wait()

        # Visual representation with areas
        disease_area = Rectangle(width=0.5, height=3)
        disease_area.set_fill(DISEASE_COLOR, opacity=0.7)
        disease_area.set_stroke(WHITE, 2)
        disease_area.shift(2.5 * LEFT)

        disease_label = Tex("1\\%\n\\text{have disease}", font_size=24)
        disease_label.next_to(disease_area, UP, buff=0.2)

        no_disease_area = Rectangle(width=4.5, height=3)
        no_disease_area.set_fill(NO_DISEASE_COLOR, opacity=0.7)
        no_disease_area.set_stroke(WHITE, 2)
        no_disease_area.shift(0.75 * RIGHT)

        no_disease_label = Tex("99\\%\n\\text{don't have disease}", font_size=24)
        no_disease_label.next_to(no_disease_area, UP, buff=0.2)

        self.play(
            DrawBorderThenFill(disease_area),
            DrawBorderThenFill(no_disease_area),
            Write(disease_label),
            Write(no_disease_label)
        )
        self.wait()

        # Show positive tests in each group
        true_pos = Rectangle(width=0.475, height=2.85)
        true_pos.set_fill(POSITIVE_TEST_COLOR, opacity=0.5)
        true_pos.set_stroke(YELLOW, 2)
        true_pos.move_to(disease_area)

        tp_label = Text("95% test +", font_size=18, color=YELLOW)
        tp_label.move_to(true_pos)

        false_pos = Rectangle(width=0.45, height=2.85)
        false_pos.set_fill(POSITIVE_TEST_COLOR, opacity=0.5)
        false_pos.set_stroke(YELLOW, 2)
        false_pos.move_to(no_disease_area).shift(1.575 * LEFT)

        fp_label = Text("10% test +", font_size=18, color=YELLOW)
        fp_label.move_to(false_pos)

        self.play(
            FadeIn(true_pos),
            FadeIn(false_pos),
            Write(tp_label),
            Write(fp_label)
        )
        self.wait(2)

        # The key insight
        insight = VGroup(
            Text("Key insight:", font_size=28, weight=BOLD),
            Text("Even though the test is accurate, the disease is rare!", font_size=24),
            Text("So most positive tests are false positives.", font_size=24),
        )
        insight.arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        insight.to_edge(DOWN, buff=0.5)

        self.play(
            LaggedStart(
                *[FadeIn(line, shift=UP) for line in insight],
                lag_ratio=0.5
            )
        )
        self.wait(4)

        # ========================================
        # FINAL MESSAGE
        # ========================================
        self.play(FadeOut(*self.mobjects))

        final_message = Text(
            "Bayes' theorem helps us reason correctly\nabout probability and evidence!",
            font_size=40,
            color=YELLOW,
            weight=BOLD
        )
        final_message.move_to(ORIGIN)

        self.play(FadeIn(final_message, scale=1.2))
        self.wait(4)

        self.play(FadeOut(final_message))
        self.wait()


# ============================================================
# 6. SCENE EXECUTION ORDER
# ============================================================
# The order of scenes that tells the story.
#
# Scene 1 (ProbabilityIntro):
#   - Poses the medical test puzzle
#   - Sets up the scenario with numbers
#   - Teases that intuition is wrong
#
# Scene 2 (ConditionalProbability):
#   - Introduces probability tree diagram
#   - Shows all conditional probabilities
#   - Calculates joint probabilities
#
# Scene 3 (BayesFormula):
#   - Derives Bayes' theorem from first principles
#   - Explains each component
#   - Presents the formula clearly
#
# Scene 4 (MedicalTest):
#   - Applies Bayes' theorem to solve the problem
#   - Reveals surprising answer (8.8%)
#   - Explains why via base rate visualization
#   - Emphasizes importance of considering priors

SCENE_ORDER = [
    ProbabilityIntro,          # Part 1: The puzzle
    ConditionalProbability,    # Part 2: Tree diagram
    BayesFormula,              # Part 3: The theorem
    MedicalTest,               # Part 4: The solution
]
