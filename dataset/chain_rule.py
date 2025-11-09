"""
Natural Group Name: Chain Rule for Derivatives

Educational Objectives:
- To introduce the chain rule for differentiation of composite functions
- To build intuition for why rates of change multiply
- To visualize function composition and derivative relationships
- To demonstrate the chain rule with concrete examples

Story Arc & Intent:
The animation makes the chain rule intuitive by showing how rates of change
compose: if x changes at one rate and y depends on x with another rate, the
overall rate is the product. This fundamental calculus rule becomes obvious
through careful visualization.

Narrative Flow:
- Hook/Opening: Introduce the idea of composed functions
- Development: Show how small changes propagate through composition
- Build-up: Derive the chain rule formula from first principles
- Climax: Apply to a concrete example like d/dx[sin(x²)]
- Resolution: Show multiple examples demonstrating the pattern
- Extension: Discuss practical applications and generalizations

Technical Implementation Notes:
- Scene Classes: CompositionIntro, RateOfChange, ChainRuleFormula, Examples
- Key Visual Elements: Function graphs, tangent lines, rate visualization, equations
- Animation Techniques: Graph transformations, zooming, rate arrows
- Mathematical Concepts: Derivatives, function composition, limits

Dependency Chain:
All scenes are independent. They use Axes, ParametricCurve, and Tex from
manimlib. Utility functions handle function plotting and derivative visualization.

Rendering Instructions:
To render these scenes, use the manim command-line tool:
- For a single scene: manimgl chain_rule.py CompositionIntro
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
# Axes configuration
X_RANGE = [-4, 4, 1]
Y_RANGE = [-3, 3, 1]
AXES_CONFIG = {
    "width": 10,
    "height": 6,
}

# Colors for different elements
FUNCTION_COLOR = BLUE
COMPOSITION_COLOR = GREEN
DERIVATIVE_COLOR = YELLOW
TANGENT_COLOR = RED

# ============================================================
# 3. UTILITY FUNCTIONS
# ============================================================

def get_quadratic_function():
    """Returns f(x) = x² function."""
    return lambda x: x**2

def get_sin_function():
    """Returns g(x) = sin(x) function."""
    return lambda x: np.sin(x)

def get_composed_function():
    """Returns composition g(f(x)) = sin(x²)."""
    return lambda x: np.sin(x**2)

def derivative_sin_x_squared(x):
    """
    Returns derivative of sin(x²) at x.
    d/dx[sin(x²)] = cos(x²) · 2x
    """
    return np.cos(x**2) * 2 * x

def create_function_label(func_str, color, font_size=36):
    """
    Create a labeled function.

    Args:
        func_str: LaTeX string for function
        color: Color for the label
        font_size: Font size

    Returns:
        Tex object
    """
    label = Tex(func_str, font_size=font_size, color=color)
    return label

# ============================================================
# 4. BASE CLASSES AND HELPERS
# ============================================================
# No custom base classes needed

# ============================================================
# 5. SCENE IMPLEMENTATIONS
# ============================================================

class CompositionIntro(InteractiveScene):
    """
    Part 1: Introduce function composition.

    Narrative purpose:
        To establish the concept of composing functions and why we need
        a rule for differentiating them.

    Mathematical content:
        Shows how two functions f and g can be composed to create g∘f,
        using visual flow diagrams and concrete examples.

    Visual approach:
        Display flow diagrams showing x → f(x) → g(f(x)) with specific
        numerical examples, then transition to general functions.
    """
    def construct(self):
        # ========================================
        # SETUP: Title
        # ========================================
        title = Text("The Chain Rule", font_size=48)
        title.to_edge(UP)

        self.play(FadeIn(title, shift=DOWN))
        self.wait()

        # ========================================
        # INTRODUCE: Function composition
        # ========================================
        subtitle = Text("Composing Functions", font_size=36)
        subtitle.next_to(title, DOWN, buff=0.5)

        self.play(Write(subtitle))
        self.wait()

        # ========================================
        # EXAMPLE: Specific composition
        # ========================================
        # Define f(x) = x² and g(x) = sin(x)
        f_def = Tex(R"f(x) = x^2", font_size=36, color=BLUE)
        g_def = Tex(R"g(x) = \sin(x)", font_size=36, color=GREEN)

        definitions = VGroup(f_def, g_def)
        definitions.arrange(RIGHT, buff=2)
        definitions.shift(1 * UP)

        self.play(
            Write(f_def),
            Write(g_def)
        )
        self.wait()

        # ========================================
        # COMPOSITION: g(f(x))
        # ========================================
        # Show the flow
        flow_diagram = VGroup(
            Tex("x", font_size=32),
            Arrow(RIGHT, buff=0.2),
            Tex("f(x) = x^2", font_size=32, color=BLUE),
            Arrow(RIGHT, buff=0.2),
            Tex(R"g(f(x)) = \sin(x^2)", font_size=32, color=GREEN)
        )
        flow_diagram.arrange(RIGHT, buff=0.3)
        flow_diagram.shift(0.5 * DOWN)

        self.play(
            LaggedStart(
                *[FadeIn(part, shift=RIGHT) for part in flow_diagram],
                lag_ratio=0.3
            )
        )
        self.wait(2)

        # ========================================
        # QUESTION: How to differentiate?
        # ========================================
        question = Text(
            "How do we find the derivative of g(f(x))?",
            font_size=36,
            color=YELLOW
        )
        question.shift(2 * DOWN)

        self.play(Write(question))
        self.wait(3)

        # ========================================
        # CLEANUP
        # ========================================
        self.play(FadeOut(*self.mobjects), run_time=1)
        self.wait()


class RateOfChange(InteractiveScene):
    """
    Part 2: Visualize rates of change multiplying.

    Narrative purpose:
        To build intuition for why derivatives multiply in the chain rule
        by showing how rates of change propagate through composition.

    Mathematical content:
        If y changes with respect to u at rate dy/du, and u changes with
        respect to x at rate du/dx, then y changes with respect to x at
        rate (dy/du)(du/dx).

    Visual approach:
        Use arrows of different lengths to represent rates, showing how
        a small change in x creates a change in u, which creates a change in y.
    """
    def construct(self):
        # ========================================
        # SETUP: Title
        # ========================================
        title = Text("Why Do Rates Multiply?", font_size=48)
        title.to_edge(UP)

        self.play(FadeIn(title, shift=DOWN))
        self.wait()

        # ========================================
        # SETUP: The composition chain
        # ========================================
        chain = VGroup(
            Tex("x", font_size=40),
            Arrow(RIGHT, buff=0.3, color=BLUE),
            Tex("u = f(x)", font_size=40),
            Arrow(RIGHT, buff=0.3, color=GREEN),
            Tex("y = g(u)", font_size=40)
        )
        chain.arrange(RIGHT, buff=0.4)
        chain.shift(1.5 * UP)

        self.play(
            LaggedStart(
                *[FadeIn(part, shift=DOWN) for part in chain],
                lag_ratio=0.2
            )
        )
        self.wait()

        # ========================================
        # SHOW: Small change in x
        # ========================================
        dx_label = Tex(R"\Delta x", font_size=36, color=BLUE)
        dx_label.next_to(chain[1], DOWN, buff=0.5)

        dx_arrow = Arrow(
            chain[0].get_right(),
            chain[0].get_right() + 1 * RIGHT,
            color=BLUE,
            buff=0.1
        )
        dx_arrow.next_to(chain[0], DOWN, buff=1)

        self.play(
            GrowArrow(dx_arrow),
            FadeIn(dx_label, scale=1.2)
        )
        self.wait()

        # ========================================
        # PROPAGATE: Change to u
        # ========================================
        du_text = Tex(
            R"\Delta u = f'(x) \cdot \Delta x",
            font_size=32,
            color=BLUE
        )
        du_text.next_to(chain[2], DOWN, buff=1.5)

        self.play(Write(du_text))
        self.wait()

        # ========================================
        # PROPAGATE: Change to y
        # ========================================
        dy_text = Tex(
            R"\Delta y = g'(u) \cdot \Delta u",
            font_size=32,
            color=GREEN
        )
        dy_text.next_to(du_text, DOWN, buff=0.5)

        self.play(Write(dy_text))
        self.wait(2)

        # ========================================
        # SUBSTITUTE: Combine the rates
        # ========================================
        substitution = Tex(
            R"\Delta y = g'(u) \cdot [f'(x) \cdot \Delta x]",
            font_size=36,
            color=YELLOW
        )
        substitution.next_to(dy_text, DOWN, buff=0.7)

        self.play(Write(substitution))
        self.wait(2)

        # ========================================
        # CONCLUDE: The chain rule emerges
        # ========================================
        conclusion = Tex(
            R"\frac{\Delta y}{\Delta x} = g'(u) \cdot f'(x)",
            font_size=42,
            color=YELLOW
        )
        conclusion.shift(2 * DOWN)

        box = SurroundingRectangle(conclusion, buff=0.3, color=YELLOW, stroke_width=3)

        self.play(
            FadeOut(du_text),
            FadeOut(dy_text),
            FadeOut(substitution),
            TransformFromCopy(substitution, conclusion),
            ShowCreation(box)
        )
        self.wait(3)

        # ========================================
        # CLEANUP
        # ========================================
        self.play(FadeOut(*self.mobjects), run_time=1)
        self.wait()


class ChainRuleFormula(InteractiveScene):
    """
    Part 3: State and derive the chain rule formula.

    Narrative purpose:
        To formally present the chain rule and show its derivation from
        the limit definition of the derivative.

    Mathematical content:
        States the chain rule: d/dx[g(f(x))] = g'(f(x)) · f'(x)
        Shows the formal limit derivation.

    Visual approach:
        Display the formula prominently, then show step-by-step algebraic
        derivation with clear highlighting of each step.
    """
    def construct(self):
        # ========================================
        # SETUP: Title
        # ========================================
        title = Text("The Chain Rule Formula", font_size=48)
        title.to_edge(UP)

        self.play(FadeIn(title, shift=DOWN))
        self.wait()

        # ========================================
        # STATE: The chain rule
        # ========================================
        chain_rule = Tex(
            R"\frac{d}{dx}[g(f(x))] = g'(f(x)) \cdot f'(x)",
            font_size=52,
            color=YELLOW
        )
        chain_rule.shift(1 * UP)

        box = SurroundingRectangle(chain_rule, buff=0.4, color=YELLOW, stroke_width=4)

        self.play(
            Write(chain_rule),
            ShowCreation(box)
        )
        self.wait(3)

        # ========================================
        # ALTERNATIVE: Leibniz notation
        # ========================================
        leibniz = Tex(
            R"\text{Or, in Leibniz notation: } \frac{dy}{dx} = \frac{dy}{du} \cdot \frac{du}{dx}",
            font_size=40
        )
        leibniz.next_to(box, DOWN, buff=1)

        self.play(Write(leibniz))
        self.wait(2)

        # ========================================
        # CLEANUP for derivation
        # ========================================
        self.play(
            VGroup(chain_rule, box).animate.scale(0.7).to_corner(UL, buff=0.5),
            FadeOut(leibniz)
        )

        # ========================================
        # DERIVATION: From limit definition
        # ========================================
        deriv_title = Text("Derivation", font_size=36, weight=BOLD)
        deriv_title.to_edge(LEFT, buff=1).shift(1.5 * UP)

        self.play(Write(deriv_title))
        self.wait()

        # Step 1: Start with limit definition
        step1 = Tex(
            R"\frac{d}{dx}[g(f(x))] = \lim_{\Delta x \to 0} \frac{g(f(x + \Delta x)) - g(f(x))}{\Delta x}",
            font_size=32
        )
        step1.next_to(deriv_title, DOWN, buff=0.5, aligned_edge=LEFT)

        self.play(Write(step1))
        self.wait(2)

        # Step 2: Let u = f(x), u + Δu = f(x + Δx)
        step2 = Tex(
            R"\text{Let } u = f(x), \quad \Delta u = f(x + \Delta x) - f(x)",
            font_size=28
        )
        step2.next_to(step1, DOWN, buff=0.5, aligned_edge=LEFT)

        self.play(Write(step2))
        self.wait(2)

        # Step 3: Rewrite
        step3 = Tex(
            R"= \lim_{\Delta x \to 0} \frac{g(u + \Delta u) - g(u)}{\Delta x}",
            font_size=32
        )
        step3.next_to(step2, DOWN, buff=0.5, aligned_edge=LEFT)

        self.play(Write(step3))
        self.wait(2)

        # Step 4: Multiply by Δu/Δu
        step4 = Tex(
            R"= \lim_{\Delta x \to 0} \frac{g(u + \Delta u) - g(u)}{\Delta u} \cdot \frac{\Delta u}{\Delta x}",
            font_size=30
        )
        step4.next_to(step3, DOWN, buff=0.5, aligned_edge=LEFT)

        self.play(Write(step4))
        self.wait(2)

        # Step 5: Take limits separately
        step5 = Tex(
            R"= g'(u) \cdot f'(x) = g'(f(x)) \cdot f'(x)",
            font_size=32,
            color=GREEN
        )
        step5.next_to(step4, DOWN, buff=0.5, aligned_edge=LEFT)

        self.play(Write(step5))
        self.wait(3)

        # ========================================
        # EMPHASIZE: QED
        # ========================================
        qed = Tex(R"\square", font_size=48, color=GREEN)
        qed.next_to(step5, RIGHT, buff=0.5)

        self.play(FadeIn(qed, scale=2))
        self.wait(3)

        # ========================================
        # CLEANUP
        # ========================================
        self.play(FadeOut(*self.mobjects), run_time=1)
        self.wait()


class Examples(InteractiveScene):
    """
    Part 4: Work through concrete examples.

    Narrative purpose:
        To solidify understanding by applying the chain rule to specific
        functions, showing the pattern in action.

    Mathematical content:
        Examples include:
        - d/dx[sin(x²)] = cos(x²) · 2x
        - d/dx[(x³ + 1)⁵] = 5(x³ + 1)⁴ · 3x²
        - d/dx[e^(cos x)] = e^(cos x) · (-sin x)

    Visual approach:
        For each example, identify inner/outer functions, apply chain rule
        step-by-step with color coding to track components.
    """
    def construct(self):
        # ========================================
        # SETUP: Title
        # ========================================
        title = Text("Chain Rule Examples", font_size=48)
        title.to_edge(UP)

        self.play(FadeIn(title, shift=DOWN))
        self.wait()

        # ========================================
        # EXAMPLE 1: d/dx[sin(x²)]
        # ========================================
        self.show_example(
            problem=R"\frac{d}{dx}[\sin(x^2)]",
            outer=R"g(u) = \sin(u)",
            inner=R"f(x) = x^2",
            outer_deriv=R"g'(u) = \cos(u)",
            inner_deriv=R"f'(x) = 2x",
            solution=R"\cos(x^2) \cdot 2x"
        )

        # ========================================
        # EXAMPLE 2: d/dx[(x³ + 1)⁵]
        # ========================================
        self.show_example(
            problem=R"\frac{d}{dx}[(x^3 + 1)^5]",
            outer=R"g(u) = u^5",
            inner=R"f(x) = x^3 + 1",
            outer_deriv=R"g'(u) = 5u^4",
            inner_deriv=R"f'(x) = 3x^2",
            solution=R"5(x^3 + 1)^4 \cdot 3x^2"
        )

        # ========================================
        # EXAMPLE 3: d/dx[e^(cos x)]
        # ========================================
        self.show_example(
            problem=R"\frac{d}{dx}[e^{\cos x}]",
            outer=R"g(u) = e^u",
            inner=R"f(x) = \cos x",
            outer_deriv=R"g'(u) = e^u",
            inner_deriv=R"f'(x) = -\sin x",
            solution=R"e^{\cos x} \cdot (-\sin x)"
        )

        # ========================================
        # FINAL MESSAGE
        # ========================================
        self.play(FadeOut(*self.mobjects))

        message = Text(
            "The chain rule is essential for\ndifferentiating composite functions!",
            font_size=40,
            color=YELLOW,
            weight=BOLD
        )
        message.move_to(ORIGIN)

        self.play(FadeIn(message, scale=1.2))
        self.wait(4)

        self.play(FadeOut(message))
        self.wait()

    def show_example(self, problem, outer, inner, outer_deriv, inner_deriv, solution):
        """Helper method to display a chain rule example."""
        # Problem statement
        prob = Tex(problem, font_size=44)
        prob.shift(2 * UP)

        self.play(Write(prob))
        self.wait()

        # Identify functions
        outer_label = Tex(R"\text{Outer: } " + outer, font_size=32, color=GREEN)
        inner_label = Tex(R"\text{Inner: } " + inner, font_size=32, color=BLUE)

        functions = VGroup(outer_label, inner_label)
        functions.arrange(DOWN, buff=0.4, aligned_edge=LEFT)
        functions.next_to(prob, DOWN, buff=0.8)

        self.play(
            FadeIn(outer_label, shift=RIGHT),
            FadeIn(inner_label, shift=RIGHT)
        )
        self.wait()

        # Apply chain rule
        derivs = Tex(
            outer_deriv + R" \cdot " + inner_deriv,
            font_size=36
        )
        derivs.next_to(functions, DOWN, buff=0.7)

        self.play(Write(derivs))
        self.wait()

        # Final answer
        answer = Tex(
            R"= " + solution,
            font_size=40,
            color=YELLOW
        )
        answer.next_to(derivs, DOWN, buff=0.7)

        box = SurroundingRectangle(answer, buff=0.2, color=YELLOW, stroke_width=2)

        self.play(
            Write(answer),
            ShowCreation(box)
        )
        self.wait(3)

        # Cleanup
        self.play(
            FadeOut(prob),
            FadeOut(functions),
            FadeOut(derivs),
            FadeOut(answer),
            FadeOut(box)
        )


# ============================================================
# 6. SCENE EXECUTION ORDER
# ============================================================
# The order of scenes that tells the story.
#
# Scene 1 (CompositionIntro):
#   - Introduces function composition
#   - Shows specific example: sin(x²)
#   - Poses the question of differentiation
#
# Scene 2 (RateOfChange):
#   - Explains why rates multiply
#   - Shows propagation of changes
#   - Builds intuition for the formula
#
# Scene 3 (ChainRuleFormula):
#   - States the chain rule formally
#   - Shows limit-based derivation
#   - Presents both notations
#
# Scene 4 (Examples):
#   - Works through 3 concrete examples
#   - Shows step-by-step application
#   - Reinforces the pattern

SCENE_ORDER = [
    CompositionIntro,      # Part 1: Setup
    RateOfChange,          # Part 2: Intuition
    ChainRuleFormula,      # Part 3: Formula
    Examples,              # Part 4: Practice
]
