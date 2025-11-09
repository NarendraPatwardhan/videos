"""
Natural Group Name: Ulam Spiral and Prime Number Patterns

Educational Objectives:
- To visualize the Ulam spiral construction method
- To demonstrate unexpected diagonal patterns in prime number distribution
- To build intuition for structure within seeming randomness
- To show how visualization reveals mathematical patterns

Story Arc & Intent:
The animation reveals a stunning discovery: when integers are arranged in a
spiral and primes are highlighted, diagonal lines emerge. This unexpected
regularity in prime distribution shows that visualization can reveal hidden
mathematical structure.

Narrative Flow:
- Hook/Opening: Arrange integers in an outward spiral pattern
- Development: Highlight prime numbers in the spiral
- Build-up: Diagonal patterns emerge where primes cluster
- Climax: The patterns become clear and undeniable
- Resolution: Connect to polynomial expressions and number theory

Technical Implementation Notes:
- Scene Classes: SpiralConstruction, HighlightPrimes, DiagonalPatterns, PrimeDistribution
- Key Visual Elements: Spiral of dots, highlighted primes, diagonal lines
- Animation Techniques: Spiral positioning, prime highlighting, pattern emphasis
- Mathematical Concepts: Prime numbers, Ulam spiral, polynomial patterns

Dependency Chain:
All scenes use basic manimlib components: Dot, Text, Tex, Line.
No custom utilities required.

Rendering Instructions:
To render these scenes, use the manim command-line tool:
- For a single scene: manimgl prime_spirals.py SpiralConstruction
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
# - BLUE: Regular numbers (composites)
# - YELLOW: Prime numbers
# - GREEN: Diagonal patterns
# - RED: Highlighted specific primes
# - WHITE: Text and labels
# - GREY_A: De-emphasized elements
#
# Key Manim Constants Used:
# - UP, DOWN, LEFT, RIGHT: Direction vectors
# - ORIGIN: Center of spiral (where 1 is placed)
# - DEGREES: Angle conversion

# Spiral configuration
DOT_RADIUS = 0.08
SPACING = 0.4
MAX_NUMBER = 121  # Show numbers 1 to 121 (11x11 grid worth)

# ============================================================
# 3. UTILITY FUNCTIONS
# ============================================================

def is_prime(n):
    """
    Check if a number is prime.

    Args:
        n: Integer to check

    Returns:
        True if n is prime, False otherwise
    """
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False

    for i in range(3, int(np.sqrt(n)) + 1, 2):
        if n % i == 0:
            return False

    return True

def get_ulam_spiral_position(n, spacing=SPACING):
    """
    Get the position of number n in the Ulam spiral.

    The Ulam spiral starts at the center with 1, then spirals
    counterclockwise outward: 2 is to the right, 3 up, 4-5 left, etc.

    Args:
        n: The number (1, 2, 3, ...)
        spacing: Distance between adjacent numbers

    Returns:
        2D numpy array [x, y, 0] for the position
    """
    if n == 1:
        return np.array([0, 0, 0])

    # Determine which "ring" of the spiral we're in
    # Ring k contains numbers from (2k-1)² + 1 to (2k+1)²
    k = int(np.ceil((np.sqrt(n) - 1) / 2))

    # Starting number of this ring
    start = (2 * k - 1) ** 2 + 1

    # Position within the ring
    offset = n - start

    # Side length of this ring
    side = 2 * k

    # Starting position (bottom-right of previous ring)
    x = k * spacing
    y = -(k - 1) * spacing

    # Move around the ring
    if offset < side:  # Right side, moving up
        y += offset * spacing
    elif offset < 2 * side:  # Top side, moving left
        y += side * spacing
        x -= (offset - side) * spacing
    elif offset < 3 * side:  # Left side, moving down
        y += side * spacing
        x -= side * spacing
        y -= (offset - 2 * side) * spacing
    else:  # Bottom side, moving right
        x -= side * spacing
        y -= (offset - 3 * side) * spacing

    return np.array([x, y, 0])

def create_spiral_dots(max_n, spacing=SPACING, composite_color=BLUE, prime_color=YELLOW):
    """
    Create dots for the Ulam spiral.

    Args:
        max_n: Maximum number to include
        spacing: Distance between adjacent numbers
        composite_color: Color for composite numbers
        prime_color: Color for prime numbers

    Returns:
        VGroup of Dot mobjects
    """
    dots = VGroup()

    for n in range(1, max_n + 1):
        pos = get_ulam_spiral_position(n, spacing)
        color = prime_color if is_prime(n) else composite_color

        dot = Dot(pos, radius=DOT_RADIUS, color=color)
        dot.set_sheen(-0.2, DR)

        dots.add(dot)

    return dots

def get_primes_up_to(max_n):
    """
    Get list of prime numbers up to max_n.

    Args:
        max_n: Maximum number

    Returns:
        List of primes
    """
    return [n for n in range(2, max_n + 1) if is_prime(n)]

# ============================================================
# 4. BASE CLASSES AND HELPERS
# ============================================================
# No custom base classes needed

# ============================================================
# 5. SCENE IMPLEMENTATIONS
# ============================================================

class SpiralConstruction(InteractiveScene):
    """
    Part 1: Construct the Ulam spiral with integers.

    Narrative purpose:
        To introduce the Ulam spiral construction method, showing how
        integers are arranged in an outward spiral pattern.

    Mathematical content:
        The Ulam spiral places 1 at the center, then spirals outward
        counterclockwise: 2 right, 3 up, 4-5 left, 6-7-8 down, etc.

    Visual approach:
        Animate the construction of the spiral, showing numbers being
        placed one by one, revealing the spiral pattern.
    """
    def construct(self):
        # ========================================
        # SETUP: Title
        # ========================================
        title = OldTexText("The Ulam Spiral", font_size=48)
        title.to_edge(UP)

        self.play(FadeIn(title, shift=DOWN))
        self.wait()

        # ========================================
        # EXPLAIN: The construction
        # ========================================
        explanation = OldTexText(
            "Arrange integers in a spiral, starting from 1",
            font_size=32,
            color=GREY_A
        )
        explanation.to_edge(DOWN, buff=0.8)

        self.play(FadeIn(explanation, shift=UP))
        self.wait()

        # ========================================
        # CREATE: First few numbers with labels
        # ========================================
        numbers_to_show = 25  # Show 1-25 with labels

        dots_with_labels = VGroup()

        for n in range(1, numbers_to_show + 1):
            pos = get_ulam_spiral_position(n, spacing=0.6)

            dot = Dot(pos, radius=0.1, color=BLUE)
            label = OldTexText(str(n), font_size=20)
            label.move_to(pos)

            dots_with_labels.add(VGroup(dot, label))

        # Animate creation in spiral order
        self.play(
            LaggedStart(
                *[FadeIn(item, scale=0.5) for item in dots_with_labels],
                lag_ratio=0.1
            ),
            run_time=4
        )
        self.wait(2)

        # ========================================
        # EXTEND: Show more numbers (without labels)
        # ========================================
        self.play(FadeOut(explanation))

        more_explanation = OldTexText(
            "Extending to 121 numbers...",
            font_size=32,
            color=GREY_A
        )
        more_explanation.to_edge(DOWN, buff=0.8)

        self.play(FadeIn(more_explanation, shift=UP))
        self.wait()

        # Create full spiral without labels
        full_dots = create_spiral_dots(MAX_NUMBER, spacing=0.35, composite_color=BLUE, prime_color=BLUE)

        # Scale down the labeled version
        self.play(
            dots_with_labels.animate.scale(0.58).set_opacity(0),
            run_time=1
        )
        self.play(
            FadeIn(full_dots),
            FadeOut(dots_with_labels),
            FadeOut(more_explanation)
        )
        self.wait()

        # ========================================
        # QUESTION: What about primes?
        # ========================================
        question = OldTexText(
            "What happens if we highlight the prime numbers?",
            font_size=36,
            color=YELLOW
        )
        question.to_edge(DOWN, buff=0.5)

        self.play(FadeIn(question, shift=UP))
        self.wait(2)


class HighlightPrimes(InteractiveScene):
    """
    Part 2: Highlight prime numbers in the spiral.

    Narrative purpose:
        To reveal the surprising pattern: primes tend to align along
        diagonal lines, showing unexpected structure.

    Mathematical content:
        When primes are highlighted in the Ulam spiral, diagonal
        patterns emerge, suggesting polynomial relationships.

    Visual approach:
        Transform the spiral so primes are in a different color,
        making the diagonal patterns visually apparent.
    """
    def construct(self):
        # ========================================
        # SETUP: Title
        # ========================================
        title = OldTexText("Highlighting Prime Numbers", font_size=48)
        title.to_edge(UP)

        self.add(title)

        # ========================================
        # CREATE: Spiral with all blue dots
        # ========================================
        all_dots = create_spiral_dots(MAX_NUMBER, spacing=0.35, composite_color=BLUE, prime_color=BLUE)

        self.add(all_dots)
        self.wait()

        # ========================================
        # HIGHLIGHT: Change prime colors
        # ========================================
        instruction = OldTexText(
            "Primes will appear in yellow...",
            font_size=32,
            color=GREY_A
        )
        instruction.to_edge(DOWN, buff=0.8)

        self.play(FadeIn(instruction, shift=UP))
        self.wait()

        # Create new spiral with primes highlighted
        highlighted_dots = create_spiral_dots(MAX_NUMBER, spacing=0.35, composite_color=BLUE, prime_color=YELLOW)

        self.play(
            Transform(all_dots, highlighted_dots),
            run_time=2
        )
        self.wait()

        # ========================================
        # OBSERVE: Patterns emerge
        # ========================================
        self.play(FadeOut(instruction))

        observation = OldTexText(
            "Notice the diagonal patterns!",
            font_size=36,
            color=GREEN
        )
        observation.to_edge(DOWN, buff=0.5)

        self.play(FadeIn(observation, shift=UP))
        self.wait(3)


class DiagonalPatterns(InteractiveScene):
    """
    Part 3: Emphasize and explain the diagonal patterns.

    Narrative purpose:
        To make the diagonal patterns undeniable by drawing lines
        through clusters of primes, revealing the structure.

    Mathematical content:
        Diagonals in the Ulam spiral correspond to quadratic polynomials.
        Some polynomials (like n² + n + 41) produce many primes.

    Visual approach:
        Draw diagonal lines through prime clusters, label them with
        the corresponding polynomial expressions.
    """
    def construct(self):
        # ========================================
        # SETUP: Title
        # ========================================
        title = OldTexText("Diagonal Patterns", font_size=48)
        title.to_edge(UP)

        self.add(title)

        # ========================================
        # CREATE: Spiral with primes highlighted
        # ========================================
        dots = create_spiral_dots(MAX_NUMBER, spacing=0.35, composite_color=BLUE, prime_color=YELLOW)

        self.add(dots)

        # ========================================
        # DRAW: Diagonal lines through primes
        # ========================================
        explanation = OldTexText(
            "Drawing lines through prime clusters...",
            font_size=32,
            color=GREY_A
        )
        explanation.to_edge(DOWN, buff=0.8)

        self.play(FadeIn(explanation, shift=UP))
        self.wait()

        # Example diagonals (manually identified)
        # These are approximate positions for visual effect
        diagonal_lines = VGroup(
            Line(
                get_ulam_spiral_position(3, 0.35),
                get_ulam_spiral_position(97, 0.35),
                color=GREEN,
                stroke_width=2
            ),
            Line(
                get_ulam_spiral_position(7, 0.35),
                get_ulam_spiral_position(109, 0.35),
                color=GREEN,
                stroke_width=2
            ),
            Line(
                get_ulam_spiral_position(5, 0.35),
                get_ulam_spiral_position(101, 0.35),
                color=GREEN,
                stroke_width=2
            ),
        )

        self.play(
            LaggedStart([ShowCreation(line) for line in diagonal_lines], lag_ratio=0.3),
            run_time=2
        )
        self.wait()

        # ========================================
        # EXPLAIN: Polynomial connection
        # ========================================
        self.play(FadeOut(explanation))

        polynomial_explanation = VGroup(
            OldTexText("Each diagonal corresponds to a polynomial:", font_size=28),
            Tex("n^2 + n + 41", font_size=32, color=GREEN),
            Tex("n^2 + n + 17", font_size=32, color=GREEN),
            Tex("n^2 - n + 41", font_size=32, color=GREEN),
            OldTexText("These produce many primes!", font_size=28, color=YELLOW)
        )
        polynomial_explanation.arrange(DOWN, buff=0.3)
        polynomial_explanation.to_edge(DOWN, buff=0.3)

        self.play(FadeIn(polynomial_explanation, shift=UP, lag_ratio=0.2))
        self.wait(3)


class PrimeDistribution(InteractiveScene):
    """
    Part 4: Discuss the significance for prime distribution.

    Narrative purpose:
        To contextualize the Ulam spiral within the broader question
        of prime distribution and the patterns (or lack thereof) in primes.

    Mathematical content:
        While primes seem randomly distributed, the Ulam spiral reveals
        structure. Quadratic polynomials along diagonals produce primes
        more frequently than random chance would predict.

    Visual approach:
        Show statistics, discuss the mystery of prime distribution,
        and emphasize that visualization revealed this hidden structure.
    """
    def construct(self):
        # ========================================
        # SETUP: Title
        # ========================================
        title = OldTexText("Prime Distribution Mystery", font_size=48)
        title.to_edge(UP)

        self.add(title)

        # ========================================
        # SHOW: Spiral
        # ========================================
        dots = create_spiral_dots(MAX_NUMBER, spacing=0.28, composite_color=BLUE, prime_color=YELLOW)
        dots.shift(2 * LEFT)

        self.add(dots)

        # ========================================
        # FACTS: About the pattern
        # ========================================
        facts = VGroup(
            OldTexText("Ulam's Discovery (1963):", font_size=32, weight=BOLD),
            OldTexText("• Primes show diagonal structure", font_size=26),
            OldTexText("• Diagonals = quadratic polynomials", font_size=26),
            OldTexText("• Some polynomials favor primes", font_size=26),
            OldTexText("• Not fully understood!", font_size=26, color=YELLOW),
        )
        facts.arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        facts.to_edge(RIGHT, buff=1)
        facts.shift(0.5 * UP)

        self.play(FadeIn(facts, shift=LEFT, lag_ratio=0.3))
        self.wait(2)

        # ========================================
        # EXAMPLE: Famous polynomial
        # ========================================
        example = VGroup(
            OldTexText("Example:", font_size=28, weight=BOLD),
            Tex("n^2 + n + 41", font_size=36, color=GREEN),
            OldTexText("produces primes for", font_size=24),
            OldTexText("n = 0, 1, 2, ..., 39", font_size=24, color=GREEN),
            OldTexText("(40 consecutive values!)", font_size=24, color=YELLOW)
        )
        example.arrange(DOWN, buff=0.2)
        example.to_edge(RIGHT, buff=1)
        example.shift(1.5 * DOWN)

        self.play(FadeIn(example, shift=UP, lag_ratio=0.2))
        self.wait(2)

        # ========================================
        # MESSAGE: Power of visualization
        # ========================================
        message = OldTexText(
            "Visualization reveals hidden mathematical structure",
            font_size=32,
            color=GREEN
        )
        message.to_edge(DOWN, buff=0.5)

        self.play(FadeIn(message, shift=UP))
        self.wait(3)


# ============================================================
# 6. SCENE EXECUTION ORDER
# ============================================================
# The order of scenes that tells the story.
#
# Scene 1 (SpiralConstruction):
#   - Introduces the Ulam spiral construction method
#   - Shows integers arranged in an outward spiral
#   - Extends to 121 numbers for a good view
#
# Scene 2 (HighlightPrimes):
#   - Highlights prime numbers in yellow
#   - Reveals the unexpected diagonal patterns
#   - Makes the structure visually apparent
#
# Scene 3 (DiagonalPatterns):
#   - Draws diagonal lines through prime clusters
#   - Connects diagonals to quadratic polynomials
#   - Shows specific polynomial examples
#
# Scene 4 (PrimeDistribution):
#   - Discusses the significance for prime distribution
#   - Presents Ulam's discovery and its mystery
#   - Emphasizes the power of visualization

SCENE_ORDER = [
    SpiralConstruction,      # Part 1: Build the spiral
    HighlightPrimes,         # Part 2: Highlight primes
    DiagonalPatterns,        # Part 3: Reveal diagonal structure
    PrimeDistribution,       # Part 4: Discuss significance
]
