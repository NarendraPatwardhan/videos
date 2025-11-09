"""
Natural Group Name: Moser's Circle Problem

Educational Objectives:
- To demonstrate the surprising pattern in the number of regions formed by chords
- To show how patterns can be deceptive in mathematics
- To build intuition about combinatorial counting in geometric contexts
- To illustrate the importance of proof over pattern observation

Story Arc & Intent:
The animation explores one of mathematics' most famous "misleading patterns" - Moser's
circle problem. It appears that connecting n points on a circle creates 2^(n-1) regions,
but this breaks down at n=6. This teaches a valuable lesson about mathematical reasoning.

Narrative Flow:
- Hook/Opening: Draw points on a circle and connect them with chords
- Development: Count regions for increasing numbers of points
- Build-up: The pattern appears to be powers of 2
- Climax: The pattern breaks at n=6 (we get 31 regions, not 32)
- Resolution: Explain why the pattern fails and show the correct formula
- Extension: Discuss the importance of proof over pattern recognition

Technical Implementation Notes:
- Scene Classes: IntroduceCircle, DrawChords, CountRegions, SurprisingPattern
- Key Visual Elements: Circle, points, chords, region highlighting, formulas
- Animation Techniques: Dynamic chord drawing, region counting, highlighting
- Mathematical Concepts: Combinatorics, binomial coefficients, planar graphs

Dependency Chain:
All scenes are independent. They use basic Circle, Dot, Line, and Tex mobjects from
manimlib. Utility functions help with chord intersection calculation.

Rendering Instructions:
To render these scenes, use the manim command-line tool:
- For a single scene: manimgl moser_circle_problem.py IntroduceCircle
- For all scenes in sequence: iterate through SCENE_ORDER
"""

# ============================================================
# 1. IMPORTS
# ============================================================
from manimlib import *
import numpy as np
from itertools import combinations

# ============================================================
# 2. CONFIGURATION AND CONSTANTS
# ============================================================
# Circle configuration
CIRCLE_RADIUS = 2.5
POINT_RADIUS = 0.08
CHORD_STROKE_WIDTH = 2
REGION_FILL_OPACITY = 0.3

# Color scheme
CIRCLE_COLOR = WHITE
POINT_COLOR = YELLOW
CHORD_COLOR = BLUE
REGION_COLORS = [BLUE, GREEN, YELLOW, RED, PURPLE, TEAL, MAROON, PINK]

# Layout
CIRCLE_CENTER = ORIGIN

# ============================================================
# 3. UTILITY FUNCTIONS
# ============================================================

def get_circle_points(n, radius=CIRCLE_RADIUS, center=ORIGIN):
    """
    Get n equally spaced points on a circle.

    Args:
        n: Number of points
        radius: Circle radius
        center: Circle center

    Returns:
        List of n points on the circle
    """
    angles = np.linspace(0, 2 * np.pi, n, endpoint=False)
    # Start from top and go clockwise
    angles = angles + np.pi / 2
    points = [
        center + radius * np.array([np.cos(angle), np.sin(angle), 0])
        for angle in angles
    ]
    return points

def count_regions(n):
    """
    Calculate the actual number of regions for n points using the correct formula.

    The formula is: C(n,0) + C(n,2) + C(n,4)
    which simplifies to: 1 + C(n,2) + C(n,4)
    or more generally: 1 + n(n-1)/2 + C(n,4)

    For the full formula:
    R(n) = C(n,0) + C(n,2) + C(n,4) = 1 + n(n-1)/2 + n(n-1)(n-2)(n-3)/24

    Args:
        n: Number of points on circle

    Returns:
        Number of regions
    """
    if n < 2:
        return 1

    # Use the closed form
    term0 = 1
    term2 = n * (n - 1) // 2 if n >= 2 else 0
    term4 = n * (n - 1) * (n - 2) * (n - 3) // 24 if n >= 4 else 0

    return term0 + term2 + term4

def create_chord(p1, p2, color=CHORD_COLOR, stroke_width=CHORD_STROKE_WIDTH):
    """
    Create a line segment (chord) between two points.

    Args:
        p1: First point
        p2: Second point
        color: Chord color
        stroke_width: Line width

    Returns:
        Line object
    """
    line = Line(p1, p2)
    line.set_stroke(color, stroke_width)
    return line

# ============================================================
# 4. BASE CLASSES AND HELPERS
# ============================================================
# No custom base classes needed

# ============================================================
# 5. SCENE IMPLEMENTATIONS
# ============================================================

class IntroduceCircle(InteractiveScene):
    """
    Part 1: Introduce the problem setup.

    Narrative purpose:
        To set up the problem by showing how we place points on a circle and
        connect them with chords, establishing the basic question.

    Mathematical content:
        Introduces the concept of connecting all pairs of points on a circle
        with chords, creating regions in the interior.

    Visual approach:
        Start with an empty circle, add points one by one, and show how
        connecting them creates chords and divides the circle into regions.
    """
    def construct(self):
        # ========================================
        # SETUP: Title
        # ========================================
        title = OldTexText("Moser's Circle Problem", font_size=48)
        title.to_edge(UP)

        self.play(FadeIn(title, shift=DOWN))
        self.wait()

        # ========================================
        # INTRODUCE: The circle
        # ========================================
        circle = Circle(radius=CIRCLE_RADIUS)
        circle.set_stroke(CIRCLE_COLOR, 3)
        circle.move_to(CIRCLE_CENTER)

        question = OldTexText(
            "How many regions are created by connecting\nn points on a circle?",
            font_size=32
        )
        question.to_edge(DOWN, buff=0.5)

        self.play(
            ShowCreation(circle),
            FadeIn(question, shift=UP)
        )
        self.wait(2)

        # ========================================
        # DEMONSTRATE: Simple cases
        # ========================================
        # Case n=1: One point, one region
        point1_pos = get_circle_points(1)[0]
        point1 = Dot(point1_pos, radius=POINT_RADIUS, color=POINT_COLOR)

        label1 = Tex("n = 1", font_size=36)
        label1.next_to(circle, LEFT, buff=1)

        regions1 = Tex("\\text{Regions: } 1", font_size=36)
        regions1.next_to(label1, DOWN, buff=0.5)

        self.play(
            FadeIn(point1, scale=1.5),
            Write(label1),
            Write(regions1)
        )
        self.wait(2)

        # ========================================
        # CASE n=2: Two points, one chord, two regions
        # ========================================
        self.play(FadeOut(point1), FadeOut(label1), FadeOut(regions1))

        points2_pos = get_circle_points(2)
        points2 = VGroup(*[
            Dot(pos, radius=POINT_RADIUS, color=POINT_COLOR)
            for pos in points2_pos
        ])

        chord2 = create_chord(points2_pos[0], points2_pos[1])

        label2 = Tex("n = 2", font_size=36)
        label2.next_to(circle, LEFT, buff=1)

        regions2 = Tex("\\text{Regions: } 2", font_size=36)
        regions2.next_to(label2, DOWN, buff=0.5)

        self.play(
            LaggedStart(
                *[FadeIn(pt, scale=1.5) for pt in points2],
                lag_ratio=0.3
            ),
            Write(label2)
        )
        self.wait()

        self.play(ShowCreation(chord2))
        self.wait()

        self.play(Write(regions2))
        self.wait(2)

        # ========================================
        # TRANSITION
        # ========================================
        transition_text = OldTexText(
            "Let's see what happens as we add more points...",
            font_size=32,
            color=YELLOW
        )
        transition_text.to_edge(DOWN, buff=0.5)

        self.play(
            FadeOut(question),
            FadeIn(transition_text, shift=UP)
        )
        self.wait(2)

        # ========================================
        # CLEANUP
        # ========================================
        everything = VGroup(
            circle, points2, chord2, label2, regions2,
            title, transition_text
        )
        self.play(FadeOut(everything), run_time=1)
        self.wait()


class DrawChords(InteractiveScene):
    """
    Part 2: Draw all chords for increasing n and count regions.

    Narrative purpose:
        To show the pattern emerging for n = 3, 4, 5 which suggests the
        number of regions follows 2^(n-1).

    Mathematical content:
        Demonstrates systematic chord construction and region counting,
        revealing what appears to be an exponential pattern.

    Visual approach:
        For each n from 3 to 5, draw all chords and highlight the regions,
        displaying the count prominently.
    """
    def construct(self):
        # ========================================
        # SETUP: Title and table
        # ========================================
        title = OldTexText("Drawing All Chords", font_size=48)
        title.to_edge(UP)

        self.play(FadeIn(title, shift=DOWN))
        self.wait()

        # Create table to track pattern
        table_entries = []

        # ========================================
        # CASE n=3: 4 regions
        # ========================================
        self.show_case(3, table_entries)

        # ========================================
        # CASE n=4: 8 regions
        # ========================================
        self.show_case(4, table_entries)

        # ========================================
        # CASE n=5: 16 regions
        # ========================================
        self.show_case(5, table_entries)

        # ========================================
        # SHOW PATTERN TABLE
        # ========================================
        self.play(FadeOut(*self.mobjects))

        title2 = OldTexText("The Pattern So Far", font_size=48)
        title2.to_edge(UP)
        self.play(FadeIn(title2, shift=DOWN))

        # Create summary table
        table_data = [
            ["n", "Regions", "Pattern"],
            ["1", "1", "2^0"],
            ["2", "2", "2^1"],
            ["3", "4", "2^2"],
            ["4", "8", "2^3"],
            ["5", "16", "2^4"],
        ]

        table = VGroup()
        for i, row in enumerate(table_data):
            row_mob = VGroup()
            for j, entry in enumerate(row):
                if i == 0:
                    cell = OldTexText(entry, font_size=32, weight=BOLD)
                else:
                    cell = Tex(entry, font_size=32)

                cell.move_to(2 * j * RIGHT + i * 0.7 * DOWN)
                row_mob.add(cell)
            table.add(row_mob)

        table.move_to(ORIGIN)

        self.play(LaggedStart(
            *[FadeIn(row, shift=DOWN) for row in table],
            lag_ratio=0.2
        ))
        self.wait(2)

        # ========================================
        # CONJECTURE
        # ========================================
        conjecture = Tex(
            R"\text{Conjecture: } R(n) = 2^{n-1}",
            font_size=42,
            color=YELLOW
        )
        conjecture.to_edge(DOWN, buff=1)

        question_mark = Tex("?", font_size=72, color=RED)
        question_mark.next_to(conjecture, RIGHT, buff=0.5)

        self.play(
            Write(conjecture),
            FadeIn(question_mark, scale=2)
        )
        self.wait(3)

        self.play(FadeOut(*self.mobjects))

    def show_case(self, n, table_entries):
        """Helper method to show a specific case."""
        # Create circle
        circle = Circle(radius=CIRCLE_RADIUS)
        circle.set_stroke(CIRCLE_COLOR, 3)
        circle.move_to(CIRCLE_CENTER)

        # Create points
        points_pos = get_circle_points(n)
        points = VGroup(*[
            Dot(pos, radius=POINT_RADIUS, color=POINT_COLOR)
            for pos in points_pos
        ])

        # Label
        label = Tex(f"n = {n}", font_size=42)
        label.to_corner(UL, buff=0.8)
        label.shift(0.5 * DOWN)

        self.play(
            ShowCreation(circle),
            LaggedStart(
                *[FadeIn(pt, scale=1.5) for pt in points],
                lag_ratio=0.2
            ),
            FadeIn(label)
        )
        self.wait()

        # Draw all chords
        chords = VGroup()
        for i, j in combinations(range(n), 2):
            chord = create_chord(points_pos[i], points_pos[j])
            chords.add(chord)

        self.play(
            LaggedStart(
                *[ShowCreation(chord) for chord in chords],
                lag_ratio=0.1
            ),
            run_time=2
        )
        self.wait()

        # Show region count
        region_count = count_regions(n)
        count_label = Tex(
            f"\\text{{Regions: }} {region_count}",
            font_size=42,
            color=YELLOW
        )
        count_label.next_to(label, DOWN, buff=0.5)

        self.play(Write(count_label))
        self.wait(2)

        # Cleanup for next case
        self.play(
            FadeOut(circle),
            FadeOut(points),
            FadeOut(chords),
            FadeOut(label),
            FadeOut(count_label)
        )


class CountRegions(InteractiveScene):
    """
    Part 3: Test the pattern with n=6.

    Narrative purpose:
        To reveal the surprising breakdown of the pattern at n=6, showing
        that pattern recognition alone is insufficient for mathematical truth.

    Mathematical content:
        Shows that for n=6, we get 31 regions, not 32 as the pattern predicts,
        demonstrating the need for rigorous proof.

    Visual approach:
        Carefully draw all chords for n=6, count the regions explicitly,
        and dramatically reveal the discrepancy.
    """
    def construct(self):
        # ========================================
        # SETUP: Build suspense
        # ========================================
        title = OldTexText("Testing the Pattern: n = 6", font_size=48)
        title.to_edge(UP)

        self.play(FadeIn(title, shift=DOWN))
        self.wait()

        # Show prediction
        prediction = Tex(
            R"\text{If } R(n) = 2^{n-1}, \text{ then } R(6) = 2^5 = 32",
            font_size=36
        )
        prediction.to_edge(DOWN, buff=2)

        self.play(Write(prediction))
        self.wait(2)

        # ========================================
        # DRAW: n=6 configuration
        # ========================================
        circle = Circle(radius=CIRCLE_RADIUS)
        circle.set_stroke(CIRCLE_COLOR, 3)
        circle.move_to(CIRCLE_CENTER)

        points_pos = get_circle_points(6)
        points = VGroup(*[
            Dot(pos, radius=POINT_RADIUS, color=POINT_COLOR)
            for pos in points_pos
        ])

        self.play(
            ShowCreation(circle),
            LaggedStart(
                *[FadeIn(pt, scale=1.5) for pt in points],
                lag_ratio=0.2
            )
        )
        self.wait()

        # Draw all chords
        chords = VGroup()
        for i, j in combinations(range(6), 2):
            chord = create_chord(points_pos[i], points_pos[j])
            chords.add(chord)

        self.play(
            LaggedStart(
                *[ShowCreation(chord) for chord in chords],
                lag_ratio=0.05
            ),
            run_time=3
        )
        self.wait(2)

        # ========================================
        # COUNT: The actual number of regions
        # ========================================
        counting_text = OldTexText("Counting regions...", font_size=32, color=YELLOW)
        counting_text.next_to(prediction, UP, buff=0.5)

        self.play(FadeIn(counting_text))
        self.wait(2)

        # Actual count
        actual_count = count_regions(6)  # Returns 31
        result = Tex(
            f"\\text{{Actual regions: }} {actual_count}",
            font_size=42,
            color=RED
        )
        result.next_to(prediction, UP, buff=1)

        self.play(
            FadeOut(counting_text),
            Write(result)
        )
        self.wait(2)

        # ========================================
        # REVEAL: The pattern breaks!
        # ========================================
        exclamation = Tex("\\neq 32 !", font_size=60, color=RED)
        exclamation.next_to(result, RIGHT, buff=0.5)

        self.play(
            FadeIn(exclamation, scale=2),
            Indicate(result, scale_factor=1.2, color=RED)
        )
        self.wait(2)

        # ========================================
        # LESSON
        # ========================================
        lesson = OldTexText(
            "Patterns can be misleading!\nWe need proof, not just observation.",
            font_size=32,
            color=YELLOW
        )
        lesson.to_edge(DOWN, buff=0.5)

        self.play(
            FadeOut(prediction),
            FadeIn(lesson, shift=UP)
        )
        self.wait(3)

        # ========================================
        # CLEANUP
        # ========================================
        self.play(FadeOut(*self.mobjects), run_time=1)
        self.wait()


class SurprisingPattern(InteractiveScene):
    """
    Part 4: Explain the correct formula and why the pattern breaks.

    Narrative purpose:
        To provide the correct formula and mathematical insight into why
        the simple pattern fails, emphasizing combinatorial reasoning.

    Mathematical content:
        The correct formula is R(n) = C(n,4) + C(n,2) + 1, which counts
        regions based on chord intersections. Explains why this differs
        from 2^(n-1) for n≥6.

    Visual approach:
        Show the correct formula, compute it for various n, and explain
        the combinatorial interpretation (4 points determine an intersection).
    """
    def construct(self):
        # ========================================
        # SETUP: Title
        # ========================================
        title = OldTexText("The True Formula", font_size=48)
        title.to_edge(UP)

        self.play(FadeIn(title, shift=DOWN))
        self.wait()

        # ========================================
        # SHOW: The correct formula
        # ========================================
        correct_formula = Tex(
            R"R(n) = \binom{n}{4} + \binom{n}{2} + 1",
            font_size=48,
            color=GREEN
        )
        correct_formula.shift(UP)

        box = SurroundingRectangle(correct_formula, buff=0.3, color=GREEN, stroke_width=3)

        self.play(
            Write(correct_formula),
            ShowCreation(box)
        )
        self.wait(2)

        # ========================================
        # EXPLAIN: What each term means
        # ========================================
        explanation = VGroup(
            Tex(R"\binom{n}{4} = \text{interior intersections}", font_size=32),
            Tex(R"\binom{n}{2} = \text{chords (edges)}", font_size=32),
            Tex(R"1 = \text{exterior region}", font_size=32)
        )
        explanation.arrange(DOWN, buff=0.4, aligned_edge=LEFT)
        explanation.next_to(correct_formula, DOWN, buff=1)

        self.play(
            LaggedStart(
                *[FadeIn(exp, shift=RIGHT) for exp in explanation],
                lag_ratio=0.5
            )
        )
        self.wait(3)

        # ========================================
        # VERIFY: Check n=6
        # ========================================
        self.play(
            FadeOut(explanation),
            VGroup(correct_formula, box).animate.shift(1.5 * UP)
        )

        verification = Tex(
            R"R(6) &= \binom{6}{4} + \binom{6}{2} + 1 \\",
            R"&= 15 + 15 + 1 \\",
            R"&= 31 \quad \checkmark",
            font_size=40
        )
        verification.next_to(correct_formula, DOWN, buff=1)

        self.play(Write(verification[0]))
        self.wait()
        self.play(Write(verification[1]))
        self.wait()
        self.play(Write(verification[2]))
        self.wait(2)

        # ========================================
        # COMPARE: Show full table
        # ========================================
        self.play(FadeOut(verification))

        comparison_title = OldTexText("Complete Comparison", font_size=36)
        comparison_title.next_to(correct_formula, DOWN, buff=0.8)

        table_data = [
            ["n", "2^{n-1}", "\\text{Actual}", "\\text{Match?}"],
            ["1", "1", "1", "✓"],
            ["2", "2", "2", "✓"],
            ["3", "4", "4", "✓"],
            ["4", "8", "8", "✓"],
            ["5", "16", "16", "✓"],
            ["6", "32", "31", "✗"],
        ]

        table = VGroup()
        for i, row in enumerate(table_data):
            row_mob = VGroup()
            for j, entry in enumerate(row):
                if i == 0:
                    cell = Tex(entry, font_size=28, color=YELLOW)
                elif i == 6 and j >= 1:  # Highlight the n=6 row
                    cell = Tex(entry, font_size=28, color=RED)
                else:
                    cell = Tex(entry, font_size=28)

                cell.move_to(2 * j * RIGHT + i * 0.5 * DOWN)
                row_mob.add(cell)
            table.add(row_mob)

        table.next_to(comparison_title, DOWN, buff=0.5)

        self.play(Write(comparison_title))
        self.play(
            LaggedStart(
                *[FadeIn(row, shift=DOWN) for row in table],
                lag_ratio=0.2
            )
        )
        self.wait(3)

        # ========================================
        # MORAL
        # ========================================
        moral = OldTexText(
            "Mathematical truth requires proof,\nnot just pattern observation!",
            font_size=36,
            color=YELLOW,
            weight=BOLD
        )
        moral.to_edge(DOWN, buff=0.5)

        self.play(FadeIn(moral, shift=UP))
        self.wait(4)

        # ========================================
        # CLEANUP
        # ========================================
        self.play(FadeOut(*self.mobjects), run_time=1)
        self.wait()


# ============================================================
# 6. SCENE EXECUTION ORDER
# ============================================================
# The order of scenes that tells the story.
#
# Scene 1 (IntroduceCircle):
#   - Introduces the problem setup
#   - Shows simple cases n=1 and n=2
#   - Establishes the question
#
# Scene 2 (DrawChords):
#   - Shows cases n=3, 4, 5
#   - Reveals apparent pattern: 2^(n-1)
#   - Builds anticipation
#
# Scene 3 (CountRegions):
#   - Tests pattern with n=6
#   - Reveals surprising breakdown (31 ≠ 32)
#   - Emphasizes need for proof
#
# Scene 4 (SurprisingPattern):
#   - Presents correct formula: C(n,4) + C(n,2) + 1
#   - Explains combinatorial interpretation
#   - Compares predictions vs. reality
#   - Delivers moral about mathematical reasoning

SCENE_ORDER = [
    IntroduceCircle,       # Part 1: Problem setup
    DrawChords,            # Part 2: Pattern emerges
    CountRegions,          # Part 3: Pattern breaks
    SurprisingPattern,     # Part 4: True formula
]
