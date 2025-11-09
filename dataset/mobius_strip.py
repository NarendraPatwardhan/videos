"""
Natural Group Name: Möbius Strip Non-Orientable Surface

Educational Objectives:
- To visualize the construction of a Möbius strip from a rectangle
- To demonstrate that it has only one edge and one surface
- To show the non-orientable property through an ant walking on it
- To build intuition for topological properties beyond 3D geometry

Story Arc & Intent:
The animation reveals the Möbius strip's paradoxical properties: a surface with
only one side and one edge, created by a simple half-twist. This transforms
abstract topology into a concrete, mind-bending visual experience.

Narrative Flow:
- Hook/Opening: A simple rectangular strip of paper
- Development: Adding a half-twist before joining the ends
- Build-up: Tracing the edge - discovering it's a single continuous loop
- Climax: An ant walking returns upside-down - the non-orientable property
- Resolution: One-sidedness and connection to topology

Technical Implementation Notes:
- Scene Classes: ConstructStrip, OneEdgeSurface, AntWalking, NonOrientable
- Key Visual Elements: 3D surfaces, parametric surfaces, paths, rotations
- Animation Techniques: 3D transformations, surface creation, path animation
- Mathematical Concepts: Topology, non-orientability, one-sidedness, genus

Dependency Chain:
Uses ThreeDScene for 3D visualization. Parametric surfaces created using
Surface objects. All other components are basic manimlib elements.

Rendering Instructions:
To render these scenes, use the manim command-line tool:
- For a single scene: manimgl mobius_strip.py ConstructStrip
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
# - BLUE: The Möbius strip surface (top)
# - GREEN: The Möbius strip surface (bottom, but same as top!)
# - RED: Edge highlighting
# - YELLOW: Ant or path markers
# - WHITE: Labels and arrows
# - GREY_A: De-emphasized elements
#
# Key Manim Constants Used:
# - UP, DOWN, LEFT, RIGHT, IN, OUT: Direction vectors
# - ORIGIN: Center point
# - PI: π for angle calculations
# - MED_SMALL_BUFF: Spacing

# Möbius strip parameters
MOBIUS_RADIUS = 2.0
MOBIUS_WIDTH = 0.8

# ============================================================
# 3. UTILITY FUNCTIONS
# ============================================================

def mobius_strip_parametric(u, v):
    """
    Parametric equation for a Möbius strip.

    Args:
        u: Parameter along the strip (0 to 2π)
        v: Parameter across the width (-1 to 1)

    Returns:
        3D point [x, y, z]
    """
    # u goes from 0 to 2π (around the loop)
    # v goes from -1 to 1 (across the width)

    R = MOBIUS_RADIUS
    w = MOBIUS_WIDTH

    x = (R + v * w * np.cos(u / 2)) * np.cos(u)
    y = (R + v * w * np.cos(u / 2)) * np.sin(u)
    z = v * w * np.sin(u / 2)

    return np.array([x, y, z])

def create_mobius_surface(resolution=(40, 20), color=BLUE, **kwargs):
    """
    Create a Möbius strip surface.

    Args:
        resolution: Tuple (u_res, v_res) for surface resolution
        color: Color of the surface
        **kwargs: Additional arguments for Surface

    Returns:
        Surface mobject
    """
    return Surface(
        lambda u, v: mobius_strip_parametric(u, v),
        u_range=[0, TAU],
        v_range=[-1, 1],
        resolution=resolution,
        **kwargs
    )

def edge_parametric(t):
    """
    Parametric equation for the edge of the Möbius strip.

    Args:
        t: Parameter (0 to 4π to trace the full edge)

    Returns:
        3D point on the edge
    """
    # The edge goes around twice (4π) because it's a single edge
    u = t / 2
    v = 1.0  # Edge at v = 1

    return mobius_strip_parametric(u, v)

# ============================================================
# 4. SCENE CLASSES
# ============================================================

class ConstructStrip(ThreeDScene):
    """
    Scene 1: Construct a Möbius strip from a rectangular strip.

    This scene shows a flat rectangle, adds a half-twist, and joins
    the ends to create the Möbius strip.
    """

    def construct(self):
        # ========================================
        # TITLE (2D overlay)
        # ========================================
        title = Text("Constructing a Möbius Strip", font_size=48)
        title.to_edge(UP)
        title.fix_in_frame()
        self.add(title)

        # ========================================
        # START: Flat rectangular strip
        # ========================================
        # Create a simple flat strip
        strip = Surface(
            lambda u, v: np.array([u, v, 0]),
            u_range=[-3, 3],
            v_range=[-0.5, 0.5],
            resolution=(30, 5),
            color=BLUE,
        )
        strip.set_fill(BLUE, opacity=0.8)
        strip.set_stroke(WHITE, width=1, opacity=0.8)

        instruction = Text("Start with a rectangular strip", font_size=28)
        instruction.next_to(title, DOWN, buff=0.3)
        instruction.fix_in_frame()

        self.play(Write(instruction))
        self.wait()
        self.play(ShowCreation(strip))
        self.wait()

        # ========================================
        # SETUP: Camera angle
        # ========================================
        self.play(FadeOut(instruction))

        self.move_camera(
            phi=60 * DEGREES,
            theta=-45 * DEGREES,
            run_time=2
        )
        self.wait()

        # ========================================
        # TWIST: Add half-twist
        # ========================================
        twist_instruction = Text("Add a half-twist (180°)", font_size=28)
        twist_instruction.next_to(title, DOWN, buff=0.3)
        twist_instruction.fix_in_frame()

        self.add_fixed_in_frame_mobjects(twist_instruction)
        self.wait()

        # Show the twisting motion (visual representation)
        # For simplicity, we'll fade to the final Möbius strip
        mobius = create_mobius_surface(color=BLUE)
        mobius.set_fill(BLUE, opacity=0.8)
        mobius.set_stroke(WHITE, width=1, opacity=0.5)

        self.play(
            ReplacementTransform(strip, mobius),
            run_time=3
        )
        self.wait()

        # ========================================
        # JOIN: Connect the ends
        # ========================================
        self.play(FadeOut(twist_instruction))

        join_instruction = Text("Join the ends together", font_size=28, color=GREEN)
        join_instruction.next_to(title, DOWN, buff=0.3)
        join_instruction.fix_in_frame()

        self.add_fixed_in_frame_mobjects(join_instruction)
        self.wait(2)

        # ========================================
        # RESULT
        # ========================================
        self.play(FadeOut(join_instruction))

        result = Text("Result: Möbius Strip!", font_size=32, color=YELLOW)
        result.to_edge(DOWN).shift(UP * 0.5)
        result.fix_in_frame()

        self.add_fixed_in_frame_mobjects(result)
        self.wait()

        # Rotate to show the strip
        self.begin_ambient_camera_rotation(rate=0.2)
        self.wait(4)
        self.stop_ambient_camera_rotation()

        self.wait()


class OneEdgeSurface(ThreeDScene):
    """
    Scene 2: Demonstrate that the Möbius strip has only one edge.

    This scene traces along the edge of the strip, showing that if you
    follow it continuously, you return to the starting point without
    ever leaving the edge.
    """

    def construct(self):
        # ========================================
        # SETUP
        # ========================================
        title = Text("One Edge, One Surface", font_size=42)
        title.to_edge(UP)
        title.fix_in_frame()

        mobius = create_mobius_surface(color=BLUE)
        mobius.set_fill(BLUE, opacity=0.7)
        mobius.set_stroke(WHITE, width=0.5, opacity=0.3)

        self.add(title, mobius)

        self.set_camera_orientation(phi=60 * DEGREES, theta=-45 * DEGREES)
        self.wait()

        # ========================================
        # CLAIM: One edge
        # ========================================
        claim = Text("Claim: This surface has only ONE edge", font_size=28)
        claim.next_to(title, DOWN, buff=0.3)
        claim.fix_in_frame()

        self.add_fixed_in_frame_mobjects(claim)
        self.wait()

        # ========================================
        # TRACE THE EDGE
        # ========================================
        self.play(FadeOut(claim))

        trace_instruction = Text("Let's trace along the edge...", font_size=28, color=YELLOW)
        trace_instruction.next_to(title, DOWN, buff=0.3)
        trace_instruction.fix_in_frame()

        self.add_fixed_in_frame_mobjects(trace_instruction)
        self.wait()

        # Create edge path
        edge_path = ParametricCurve(
            edge_parametric,
            t_range=[0, 4 * PI],
            color=RED,
            stroke_width=6
        )

        # Trace the edge slowly
        self.play(
            ShowCreation(edge_path),
            run_time=6,
            rate_func=linear
        )
        self.wait()

        # ========================================
        # OBSERVATION
        # ========================================
        self.play(FadeOut(trace_instruction))

        observation = VGroup(
            Text("We went around twice and", font_size=24),
            Text("returned to the start!", font_size=24, color=GREEN),
            Text("It's a single continuous edge", font_size=24, color=GREEN),
        )
        observation.arrange(DOWN, buff=0.2)
        observation.to_edge(DOWN).shift(UP * 0.5)
        observation.fix_in_frame()

        for line in observation:
            self.add_fixed_in_frame_mobjects(line)
            self.wait(0.5)

        self.wait()

        # Slow rotation to show the strip
        self.begin_ambient_camera_rotation(rate=0.15)
        self.wait(4)
        self.stop_ambient_camera_rotation()

        self.wait()


class AntWalking(ThreeDScene):
    """
    Scene 3: Show an ant walking on the surface, returning upside-down.

    This scene demonstrates the non-orientable property: an ant walking
    along the strip returns to its starting position but flipped over.
    """

    def construct(self):
        # ========================================
        # SETUP
        # ========================================
        title = Text("The Ant Experiment", font_size=42)
        title.to_edge(UP)
        title.fix_in_frame()

        mobius = create_mobius_surface(color=BLUE)
        mobius.set_fill(BLUE, opacity=0.6)
        mobius.set_stroke(WHITE, width=0.5, opacity=0.3)

        self.add(title, mobius)

        self.set_camera_orientation(phi=60 * DEGREES, theta=-45 * DEGREES)
        self.wait()

        # ========================================
        # INTRODUCE ANT
        # ========================================
        intro = Text("Imagine an ant walking on the surface", font_size=28)
        intro.next_to(title, DOWN, buff=0.3)
        intro.fix_in_frame()

        self.add_fixed_in_frame_mobjects(intro)
        self.wait()

        # Create ant (simple dot with arrow)
        ant_start = mobius_strip_parametric(0, 0)
        ant = Dot3D(point=ant_start, color=YELLOW, radius=0.1)

        # Arrow to show orientation
        ant_arrow = Arrow3D(
            start=ant_start,
            end=ant_start + UP * 0.3,
            color=YELLOW,
            thickness=0.02,
            height=0.3,
            base_radius=0.05
        )

        self.play(FadeIn(ant))
        self.play(GrowArrow(ant_arrow))
        self.wait()

        # ========================================
        # ANT WALKS AROUND
        # ========================================
        self.play(FadeOut(intro))

        walking = Text("The ant walks around the strip...", font_size=28, color=YELLOW)
        walking.next_to(title, DOWN, buff=0.3)
        walking.fix_in_frame()

        self.add_fixed_in_frame_mobjects(walking)
        self.wait()

        # Create path for ant to follow (along the center of the strip)
        def ant_path(t):
            u = t
            v = 0  # Center of strip
            return mobius_strip_parametric(u, v)

        # Animate ant moving
        t_values = np.linspace(0, 2 * PI, 100)
        path_points = [ant_path(t) for t in t_values]

        def update_ant(mob, alpha):
            idx = int(alpha * (len(path_points) - 1))
            mob.move_to(path_points[idx])

        def update_arrow(mob, alpha):
            idx = int(alpha * (len(path_points) - 1))
            t = t_values[idx]
            base = path_points[idx]

            # Arrow flips as we go around
            # Normal vector rotates with the twist
            angle = t / 2  # Half twist
            up_dir = np.array([
                -np.sin(angle) * np.sin(t),
                np.sin(angle) * np.cos(t),
                np.cos(angle)
            ])
            up_dir = up_dir / np.linalg.norm(up_dir) * 0.3

            mob.put_start_and_end_on(base, base + up_dir)

        self.play(
            UpdateFromAlphaFunc(ant, update_ant),
            UpdateFromAlphaFunc(ant_arrow, update_arrow),
            run_time=8,
            rate_func=linear
        )
        self.wait()

        # ========================================
        # OBSERVATION: UPSIDE DOWN
        # ========================================
        self.play(FadeOut(walking))

        result = VGroup(
            Text("The ant returned to the start", font_size=26),
            Text("but it's UPSIDE-DOWN!", font_size=26, color=RED),
        )
        result.arrange(DOWN, buff=0.2)
        result.to_edge(DOWN).shift(UP * 0.5)
        result.fix_in_frame()

        for line in result:
            self.add_fixed_in_frame_mobjects(line)
            self.wait(0.5)

        # Flash the arrow to emphasize
        self.play(ant_arrow.animate.set_color(RED), run_time=0.5)
        self.play(ant_arrow.animate.set_color(YELLOW), run_time=0.5)
        self.play(ant_arrow.animate.set_color(RED), run_time=0.5)

        self.wait(2)


class NonOrientable(Scene):
    """
    Scene 4: Explain the non-orientable property and topology.

    This scene summarizes the key properties of the Möbius strip and
    connects it to the broader field of topology.
    """

    def construct(self):
        # ========================================
        # TITLE
        # ========================================
        title = Text("Non-Orientable Surface", font_size=42)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait()

        # ========================================
        # DEFINITION
        # ========================================
        definition = Text(
            "A surface is non-orientable if there's no consistent",
            font_size=28
        )
        definition2 = Text(
            'notion of "up" and "down" everywhere on it',
            font_size=28
        )

        def_group = VGroup(definition, definition2)
        def_group.arrange(DOWN, buff=0.2)
        def_group.next_to(title, DOWN, buff=0.6)

        self.play(Write(definition))
        self.play(Write(definition2))
        self.wait()

        # ========================================
        # KEY PROPERTIES
        # ========================================
        properties = VGroup(
            Text("Möbius Strip Properties:", font_size=32, color=YELLOW),
            Text("• One surface (one-sided)", font_size=26),
            Text("• One edge", font_size=26),
            Text("• Non-orientable", font_size=26),
            Text("• If you cut it down the middle... try it!", font_size=26, color=GREY_A),
        )
        properties.arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        properties.next_to(def_group, DOWN, buff=0.8)

        for item in properties:
            self.play(FadeIn(item, shift=UP))
            self.wait(0.4)

        self.wait()

        # ========================================
        # COMPARISON
        # ========================================
        self.play(FadeOut(def_group))

        comparison_title = Text("Compare to a Cylinder:", font_size=28, color=BLUE)
        comparison_title.next_to(title, DOWN, buff=0.6)

        comparison = VGroup(
            Text("• Two surfaces (inside and outside)", font_size=24),
            Text("• Two edges (top and bottom)", font_size=24),
            Text("• Orientable (has clear inside/outside)", font_size=24),
        )
        comparison.arrange(DOWN, buff=0.25, aligned_edge=LEFT)
        comparison.next_to(comparison_title, DOWN, buff=0.4)

        self.play(Write(comparison_title))
        for item in comparison:
            self.play(FadeIn(item, shift=UP))
            self.wait(0.3)

        self.wait()

        # ========================================
        # TOPOLOGY
        # ========================================
        self.play(
            FadeOut(properties),
            FadeOut(comparison_title),
            FadeOut(comparison)
        )

        topology_title = Text("Welcome to Topology!", font_size=36, color=GREEN)
        topology_title.move_to(ORIGIN + UP * 0.5)

        self.play(Write(topology_title))
        self.wait()

        topology_desc = VGroup(
            Text("The study of properties that remain", font_size=26),
            Text("unchanged under continuous deformation", font_size=26),
            Text("(stretching, bending, but not tearing)", font_size=26, color=GREY_A),
        )
        topology_desc.arrange(DOWN, buff=0.2)
        topology_desc.next_to(topology_title, DOWN, buff=0.5)

        for line in topology_desc:
            self.play(FadeIn(line, shift=UP))
            self.wait(0.4)

        self.wait()

        # ========================================
        # FINAL THOUGHT
        # ========================================
        final = Text(
            "The Möbius strip: Simple to make, profound to understand",
            font_size=24,
            color=YELLOW
        )
        final.to_edge(DOWN).shift(UP * 0.5)

        self.play(FadeIn(final, shift=UP))
        self.wait(2)


# ============================================================
# 5. SCENE SUMMARY AND EXECUTION ORDER
# ============================================================
#
# Scene 1 (ConstructStrip):
#   - Starts with a flat rectangular strip
#   - Adds a half-twist (180°)
#   - Joins the ends to create the Möbius strip
#
# Scene 2 (OneEdgeSurface):
#   - Traces the edge of the Möbius strip
#   - Shows it's a single continuous edge
#   - Demonstrates the one-edge property
#
# Scene 3 (AntWalking):
#   - An ant walks around the strip
#   - Returns to start position but upside-down
#   - Demonstrates non-orientability
#
# Scene 4 (NonOrientable):
#   - Explains non-orientable surfaces
#   - Compares to orientable surfaces (cylinder)
#   - Introduces topology as a field

SCENE_ORDER = [
    ConstructStrip,        # Part 1: Construction from rectangle
    OneEdgeSurface,        # Part 2: Single edge property
    AntWalking,            # Part 3: Non-orientable demonstration
    NonOrientable,         # Part 4: Topology and properties
]
