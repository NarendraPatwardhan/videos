"""
Computing Pi from Elastic Collisions

This module demonstrates the surprising connection between elastic collisions and π.
When a small block collides with a large block (and a wall), the number of collisions
equals the digits of π for specific mass ratios. This is one of 3Blue1Brown's most
famous animations.

Scenes:
    - SetupBlocks: Introduce the setup with two blocks and a wall
    - CountCollisions: Count collisions for different mass ratios
    - SurprisingPattern: Reveal the connection to π
    - PhaseSpace: Explain using phase space geometry
"""

from manimlib import *
import numpy as np


class SetupBlocks(Scene):
    """
    Set up the blocks and wall system and explain the rules.
    """

    def construct(self):
        # Title
        title = OldTexText("Computing π from Colliding Blocks", font_size=52)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait()

        # Subtitle
        subtitle = OldTexText("A surprising connection", font_size=32, color=GREY, slant=ITALIC)
        subtitle.next_to(title, DOWN, buff=0.3)
        self.play(Write(subtitle))
        self.wait(2)
        self.play(FadeOut(subtitle))

        # Draw the ground and wall
        ground = Line(LEFT * 7, RIGHT * 7, color=WHITE)
        ground.move_to(DOWN * 2)

        wall = Line(DOWN * 2, UP * 2, color=WHITE, stroke_width=6)
        wall.move_to(LEFT * 6 + DOWN * 0.5)

        self.play(ShowCreation(ground), ShowCreation(wall))
        self.wait()

        # Create blocks
        # Small block (mass m)
        small_block = Square(side_length=0.8, color=BLUE, fill_opacity=0.7)
        small_block.move_to(LEFT * 2 + UP * 0.4)

        small_label = Tex("m", font_size=36, color=WHITE)
        small_label.move_to(small_block.get_center())

        # Large block (mass M)
        large_block = Square(side_length=1.6, color=RED, fill_opacity=0.7)
        large_block.move_to(RIGHT * 2 + UP * 0.8)

        large_label = Tex("M", font_size=48, color=WHITE)
        large_label.move_to(large_block.get_center())

        self.play(
            FadeIn(small_block),
            FadeIn(large_block),
            Write(small_label),
            Write(large_label)
        )
        self.wait()

        # Show velocities
        small_velocity = Arrow(
            small_block.get_right(),
            small_block.get_right() + RIGHT * 1.5,
            color=BLUE,
            buff=0
        )
        small_v_label = Tex("v_1 = 0", font_size=28, color=BLUE)
        small_v_label.next_to(small_velocity, UP, buff=0.1)

        large_velocity = Arrow(
            large_block.get_right(),
            large_block.get_right() + LEFT * 1.5,
            color=RED,
            buff=0
        )
        large_v_label = Tex("v_2 < 0", font_size=28, color=RED)
        large_v_label.next_to(large_velocity, UP, buff=0.1)

        self.play(
            ShowCreation(large_velocity),
            Write(large_v_label)
        )
        self.wait()
        self.play(
            ShowCreation(small_velocity),
            Write(small_v_label)
        )
        self.wait()

        # Rules
        self.play(
            FadeOut(small_velocity),
            FadeOut(large_velocity),
            FadeOut(small_v_label),
            FadeOut(large_v_label)
        )

        rules_title = OldTexText("Rules:", font_size=36, color=YELLOW)
        rules_title.move_to(UP * 2 + RIGHT * 4)

        rules = VGroup(
            OldTexText("1. Elastic collisions (no energy loss)", font_size=26),
            OldTexText("2. Frictionless surface", font_size=26),
            OldTexText("3. Count all collisions", font_size=26),
        )
        rules.arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        rules.next_to(rules_title, DOWN, buff=0.4, aligned_edge=LEFT)

        self.play(Write(rules_title))
        self.wait(0.5)
        self.play(LaggedStart([Write(rule) for rule in rules], lag_ratio=0.3))
        self.wait(2)

        # Question
        question = OldTexText(
            "How many collisions occur?",
            font_size=40,
            color=YELLOW
        )
        question.to_edge(DOWN)
        self.play(Write(question))
        self.wait(2)


class CountCollisions(Scene):
    """
    Simulate collisions for different mass ratios and count them.
    """

    def construct(self):
        # Title
        title = OldTexText("Counting Collisions", font_size=52)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait()

        # Draw setup
        ground = Line(LEFT * 7, RIGHT * 7, color=WHITE, stroke_width=2)
        ground.move_to(DOWN * 1.5)

        wall = Line(DOWN * 1.5, UP * 3, color=WHITE, stroke_width=6)
        wall.move_to(LEFT * 6 + DOWN * 0)

        self.play(ShowCreation(ground), ShowCreation(wall))
        self.wait()

        # Counter
        counter_label = OldTexText("Collisions:", font_size=32, color=YELLOW)
        counter_label.move_to(UP * 2.5 + RIGHT * 4.5)

        counter = Integer(0, font_size=48, color=GREEN)
        counter.next_to(counter_label, DOWN, buff=0.3)

        self.play(Write(counter_label), Write(counter))
        self.wait()

        # First example: M = m (equal masses)
        mass_ratio_text = Tex("M = m", font_size=36, color=BLUE)
        mass_ratio_text.next_to(counter, DOWN, buff=0.8)
        self.play(Write(mass_ratio_text))
        self.wait()

        # Create blocks
        small_size = 0.6
        large_size = 0.6

        small_block = Square(side_length=small_size, color=BLUE, fill_opacity=0.7)
        small_block.move_to(LEFT * 3 + UP * (small_size/2 - 1.5))

        large_block = Square(side_length=large_size, color=RED, fill_opacity=0.7)
        large_block.move_to(RIGHT * 1 + UP * (large_size/2 - 1.5))

        self.play(FadeIn(small_block), FadeIn(large_block))
        self.wait()

        # Simulate simple collision (M = m)
        # Initial: small at rest, large moving left
        # After collision: they exchange velocities (elastic collision equal masses)
        # Large stops, small moves left, hits wall, bounces back
        # Then they separate - 3 collisions total

        collision_count = 0

        # Large moves toward small
        self.play(large_block.animate.move_to(LEFT * 2 + UP * (large_size/2 - 1.5)), run_time=1)

        # Collision 1: blocks collide
        collision_count += 1
        counter.set_value(collision_count)
        self.play(
            Flash(large_block.get_center(), color=YELLOW, flash_radius=0.3),
            counter.animate.set_value(collision_count),
            run_time=0.3
        )
        self.wait(0.3)

        # After collision: small moves left, large stops
        self.play(
            small_block.animate.move_to(LEFT * 5 + UP * (small_size/2 - 1.5)),
            run_time=1
        )

        # Collision 2: small hits wall
        collision_count += 1
        self.play(
            Flash(small_block.get_left(), color=YELLOW, flash_radius=0.3),
            counter.animate.set_value(collision_count),
            run_time=0.3
        )
        self.wait(0.3)

        # Small bounces back
        self.play(small_block.animate.move_to(LEFT * 1.5 + UP * (small_size/2 - 1.5)), run_time=1)

        # Collision 3: small hits large again
        collision_count += 1
        self.play(
            Flash(large_block.get_left(), color=YELLOW, flash_radius=0.3),
            counter.animate.set_value(collision_count),
            run_time=0.3
        )
        self.wait(0.3)

        # Both move right, separating
        self.play(
            small_block.animate.move_to(RIGHT * 2 + UP * (small_size/2 - 1.5)),
            large_block.animate.move_to(RIGHT * 4 + UP * (large_size/2 - 1.5)),
            run_time=1.5
        )
        self.wait()

        result1 = Tex("3 \\text{ collisions}", font_size=32, color=GREEN)
        result1.next_to(mass_ratio_text, DOWN, buff=0.4)
        self.play(Write(result1))
        self.wait(2)

        # Next example: M = 100m
        self.play(
            FadeOut(small_block),
            FadeOut(large_block),
            FadeOut(mass_ratio_text),
            FadeOut(result1),
            counter.animate.set_value(0)
        )

        mass_ratio_text2 = Tex("M = 100m", font_size=36, color=BLUE)
        mass_ratio_text2.next_to(counter, DOWN, buff=0.8)
        self.play(Write(mass_ratio_text2))
        self.wait()

        # Create new blocks (large one bigger)
        small_size2 = 0.5
        large_size2 = 1.5

        small_block2 = Square(side_length=small_size2, color=BLUE, fill_opacity=0.7)
        small_block2.move_to(LEFT * 2 + UP * (small_size2/2 - 1.5))

        large_block2 = Square(side_length=large_size2, color=RED, fill_opacity=0.7)
        large_block2.move_to(RIGHT * 2 + UP * (large_size2/2 - 1.5))

        self.play(FadeIn(small_block2), FadeIn(large_block2))
        self.wait()

        # Show that there will be many collisions
        note = OldTexText("(Many collisions...)", font_size=28, color=GREY, slant=ITALIC)
        note.next_to(mass_ratio_text2, DOWN, buff=0.4)
        self.play(Write(note))
        self.wait()

        # Fast forward animation
        self.play(
            large_block2.animate.shift(LEFT * 3),
            counter.animate.set_value(31),
            run_time=2
        )
        self.wait()

        result2 = Tex("31 \\text{ collisions}", font_size=32, color=GREEN)
        result2.move_to(note.get_center())
        self.play(ReplacementTransform(note, result2))
        self.wait(2)


class SurprisingPattern(Scene):
    """
    Reveal the pattern: number of collisions relates to digits of π.
    """

    def construct(self):
        # Title
        title = OldTexText("The Surprising Pattern", font_size=52)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait()

        # Show results for different mass ratios
        results_title = OldTexText("Number of Collisions:", font_size=36, color=YELLOW)
        results_title.move_to(2 * UP)
        self.play(Write(results_title))
        self.wait()

        # Create table
        table_data = [
            (R"M = m", R"1 = 10^0", "3"),
            (R"M = 100m", R"100 = 10^2", "31"),
            (R"M = 10000m", R"10^4", "314"),
            (R"M = 1000000m", R"10^6", "3141"),
            (R"M = 100000000m", R"10^8", "31415"),
        ]

        rows = VGroup()
        for mass, power, count in table_data:
            row = VGroup(
                Tex(mass, font_size=32),
                Tex(power, font_size=32),
                Tex(count, font_size=32, color=GREEN)
            )
            row.arrange(RIGHT, buff=1.2)
            rows.add(row)

        rows.arrange(DOWN, buff=0.4)
        rows.move_to(UP * 0.2)

        # Headers
        headers = VGroup(
            OldTexText("Mass Ratio", font_size=28, color=GREY),
            OldTexText("Power of 10", font_size=28, color=GREY),
            OldTexText("Collisions", font_size=28, color=GREY)
        )
        headers.arrange(RIGHT, buff=0.7)
        headers.move_to(rows[0].get_center() + UP * 0.6)
        headers.align_to(rows[0], LEFT)

        self.play(Write(headers))
        self.wait(0.5)

        for row in rows:
            self.play(Write(row), run_time=0.6)
            self.wait(0.4)

        self.wait()

        # Highlight the pattern
        highlight_boxes = VGroup(*[
            SurroundingRectangle(row[2], color=YELLOW, buff=0.1)
            for row in rows
        ])

        self.play(LaggedStart([ShowCreation(box) for box in highlight_boxes], lag_ratio=0.2))
        self.wait()

        # Reveal: it's π!
        pi_reveal = Tex(R"\pi = 3.14159\ldots", font_size=60, color=YELLOW)
        pi_reveal.move_to(DOWN * 2.3)

        self.play(Write(pi_reveal))
        self.wait()

        # Show the pattern more clearly
        pattern = Tex(
            R"\text{For } M = 10^{2n} m \text{: collisions} = \lfloor \pi \times 10^n \rfloor",
            font_size=36,
            color=GREEN
        )
        pattern.move_to(DOWN * 3.2)

        self.play(Write(pattern))
        self.wait(3)

        # Amazement
        amazement = OldTexText("But why?!", font_size=48, color=RED)
        amazement.to_corner(DR)
        self.play(Write(amazement))
        self.wait(2)


class PhaseSpace(Scene):
    """
    Explain the π connection using phase space geometry.
    """

    def construct(self):
        # Title
        title = OldTexText("Phase Space Explanation", font_size=52)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait()

        # Intro to phase space
        intro = OldTexText("The secret lies in phase space...", font_size=36, color=YELLOW)
        intro.move_to(2 * UP)
        self.play(Write(intro))
        self.wait(2)
        self.play(FadeOut(intro))

        # Phase space axes
        axes = Axes(
            x_range=[0, 5, 1],
            y_range=[0, 5, 1],
            height=5,
            width=5,
            axis_config={"include_tip": True}
        )
        axes.move_to(LEFT * 2.5 + DOWN * 0.3)

        x_label = Tex(R"\sqrt{m} v_1", font_size=32).next_to(axes.x_axis, RIGHT)
        y_label = Tex(R"\sqrt{M} v_2", font_size=32).next_to(axes.y_axis, UP)

        self.play(ShowCreation(axes), Write(x_label), Write(y_label))
        self.wait()

        # Explanation
        explanation_title = OldTexText("Key Insights:", font_size=32, color=BLUE)
        explanation_title.move_to(UP * 2 + RIGHT * 3.5)

        insights = VGroup(
            OldTexText("• Energy conservation", font_size=24),
            OldTexText("  → points move on circles", font_size=22, color=GREY),
            OldTexText("• Momentum conservation", font_size=24),
            OldTexText("  → reflections across lines", font_size=22, color=GREY),
            OldTexText("• Arc length ∝ collisions", font_size=24),
            OldTexText("• Circle sector angle", font_size=24),
            OldTexText("  involves arctan(√(M/m))", font_size=22, color=GREY)
        )
        insights.arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        insights.next_to(explanation_title, DOWN, buff=0.4, aligned_edge=LEFT)

        self.play(Write(explanation_title))
        self.wait(0.5)
        self.play(LaggedStart([Write(insight) for insight in insights], lag_ratio=0.3))
        self.wait(2)

        # Draw a circular arc (energy conservation)
        circle = Circle(radius=2, color=YELLOW)
        circle.move_to(axes.c2p(0, 0))

        arc = Arc(
            radius=2,
            start_angle=0,
            angle=PI/3,
            color=YELLOW,
            stroke_width=4
        )
        arc.move_arc_center_to(axes.c2p(0, 0))

        self.play(ShowCreation(arc))
        self.wait()

        # Boundary line (wall collision: v1 = 0)
        wall_line = Line(
            axes.c2p(0, 0),
            axes.c2p(0, 5),
            color=WHITE,
            stroke_width=3
        )
        self.play(ShowCreation(wall_line))
        self.wait()

        # Block collision line (slope depends on mass ratio)
        # When blocks collide: conservation gives a line through origin
        collision_line = Line(
            axes.c2p(0, 0),
            axes.c2p(5, 5 * np.sqrt(100)),  # For M = 100m
            color=RED,
            stroke_width=3
        )
        self.play(ShowCreation(collision_line))
        self.wait(2)

        # The key formula
        self.play(FadeOut(insights))

        formula_box = Rectangle(height=2, width=5, color=GREEN)
        formula_box.move_to(RIGHT * 3.8 + DOWN * 0.5)

        formula_title = OldTexText("The Connection:", font_size=28, color=GREEN)
        formula_title.next_to(formula_box, UP, buff=0.2)

        formula = Tex(
            R"\text{Sector angle} = \frac{\pi}{2\arctan\sqrt{M/m}}",
            font_size=28
        )
        formula.move_to(formula_box.get_center() + UP * 0.3)

        pi_note = OldTexText("When M/m = 10^(2n), this gives π!", font_size=22, color=YELLOW)
        pi_note.move_to(formula_box.get_center() + DOWN * 0.4)

        self.play(ShowCreation(formula_box), Write(formula_title))
        self.wait(0.5)
        self.play(Write(formula))
        self.wait()
        self.play(Write(pi_note))
        self.wait(3)

        # Final note
        final_note = OldTexText(
            "A beautiful connection between mechanics and geometry!",
            font_size=30,
            color=GREY,
            slant=ITALIC
        )
        final_note.to_edge(DOWN)
        self.play(Write(final_note))
        self.wait(3)


# Utility functions for collision physics

def elastic_collision_1d(m1, v1, m2, v2):
    """
    Compute velocities after elastic collision in 1D.

    Args:
        m1, m2: Masses of the two objects
        v1, v2: Initial velocities

    Returns:
        (v1_final, v2_final) velocities after collision
    """
    v1_final = ((m1 - m2) * v1 + 2 * m2 * v2) / (m1 + m2)
    v2_final = ((m2 - m1) * v2 + 2 * m1 * v1) / (m1 + m2)
    return v1_final, v2_final


def simulate_block_collisions(m1, m2, v1_init=0, v2_init=-1, wall_pos=-10):
    """
    Simulate the colliding blocks system and count collisions.

    Args:
        m1: Mass of small block
        m2: Mass of large block
        v1_init: Initial velocity of small block
        v2_init: Initial velocity of large block (should be negative)
        wall_pos: Position of the wall

    Returns:
        Number of collisions
    """
    x1, v1 = wall_pos + 1, v1_init  # Small block position and velocity
    x2, v2 = wall_pos + 5, v2_init  # Large block position and velocity

    collision_count = 0
    max_iterations = 10000
    dt = 0.001

    for _ in range(max_iterations):
        # Update positions
        x1 += v1 * dt
        x2 += v2 * dt

        # Check for collision with wall
        if x1 <= wall_pos:
            v1 = -v1  # Bounce off wall
            x1 = wall_pos
            collision_count += 1

        # Check for collision between blocks
        if x1 >= x2:
            v1, v2 = elastic_collision_1d(m1, v1, m2, v2)
            collision_count += 1
            # Separate blocks slightly to avoid multiple counting
            x1 = x2 - 0.01

        # Stop if both blocks moving away from wall
        if v1 > 0 and v2 > 0 and x1 > x2:
            break

    return collision_count


def compute_pi_digits(n_digits):
    """
    Compute digits of π using the block collision method.

    Args:
        n_digits: Number of digits to compute

    Returns:
        Number of collisions for mass ratio 10^(2*(n_digits-1))
    """
    mass_ratio = 10 ** (2 * (n_digits - 1))
    return simulate_block_collisions(m1=1, m2=mass_ratio)


def phase_space_trajectory(m1, m2, v1_init, v2_init, num_points=1000):
    """
    Compute phase space trajectory for the colliding blocks.

    Args:
        m1, m2: Masses
        v1_init, v2_init: Initial velocities
        num_points: Number of points to compute

    Returns:
        Arrays of (sqrt(m1)*v1, sqrt(m2)*v2) coordinates
    """
    v1, v2 = v1_init, v2_init
    trajectory = [(np.sqrt(m1) * v1, np.sqrt(m2) * v2)]

    wall_pos = 0
    x1, x2 = wall_pos + 1, wall_pos + 5

    dt = 0.01

    for _ in range(num_points):
        x1 += v1 * dt
        x2 += v2 * dt

        # Wall collision
        if x1 <= wall_pos:
            v1 = -v1
            x1 = wall_pos

        # Block collision
        if x1 >= x2:
            v1, v2 = elastic_collision_1d(m1, v1, m2, v2)
            x1 = x2 - 0.01

        trajectory.append((np.sqrt(m1) * v1, np.sqrt(m2) * v2))

        # Stop condition
        if v1 > 0 and v2 > 0 and x1 > x2 and abs(v1) < 0.01:
            break

    return np.array(trajectory)
