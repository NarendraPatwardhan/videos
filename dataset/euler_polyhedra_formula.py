"""
Natural Group Name: Euler's Polyhedra Formula

Educational Objectives:
- To introduce Euler's famous formula V - E + F = 2 for polyhedra
- To demonstrate the formula holds for various 3D shapes
- To build intuition for topological invariants
- To show a visual proof using planar graph representation

Story Arc & Intent:
The animation explores one of the most beautiful theorems in geometry - Euler's
polyhedron formula. By examining common 3D shapes and verifying the formula,
then showing a visual proof, students gain insight into this fundamental result.

Narrative Flow:
- Hook/Opening: Display beautiful 3D polyhedra
- Development: Count vertices, edges, and faces for each shape
- Build-up: Verify V - E + F = 2 for multiple examples
- Climax: Show why this formula works via planar graph proof
- Resolution: Emphasize the topological significance
- Extension: Mention generalizations and connections to topology

Technical Implementation Notes:
- Scene Classes: IntroducePolyhedra, CountComponents, VerifyFormula, ProofSketch
- Key Visual Elements: 3D polyhedra (cube, tetrahedron, octahedron), labels, equations
- Animation Techniques: 3D rotation, highlighting, graph planarization
- Mathematical Concepts: Graph theory, planar graphs, Euler characteristic

Dependency Chain:
Scenes use ThreeDScene for 3D visualization. Basic 3D shapes from manimlib.
Utility functions help with vertex/edge/face counting and highlighting.

Rendering Instructions:
To render these scenes, use the manim command-line tool:
- For a single scene: manimgl euler_polyhedra_formula.py IntroducePolyhedra
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
# 3D Configuration
POLYHEDRA_SCALE = 1.8
ROTATION_RATE = 0.3

# Color scheme for different polyhedra
CUBE_COLOR = BLUE
TETRAHEDRON_COLOR = GREEN
OCTAHEDRON_COLOR = YELLOW
ICOSAHEDRON_COLOR = PURPLE

# Component highlighting colors
VERTEX_COLOR = RED
EDGE_COLOR = BLUE
FACE_COLOR = GREEN

# ============================================================
# 3. UTILITY FUNCTIONS
# ============================================================

def get_polyhedron_data(shape_name):
    """
    Get vertices, edges, and face count for common polyhedra.

    Args:
        shape_name: Name of polyhedron ("cube", "tetrahedron", etc.)

    Returns:
        Dictionary with V, E, F counts
    """
    data = {
        "tetrahedron": {"V": 4, "E": 6, "F": 4},
        "cube": {"V": 8, "E": 12, "F": 6},
        "octahedron": {"V": 6, "E": 12, "F": 8},
        "dodecahedron": {"V": 20, "E": 30, "F": 12},
        "icosahedron": {"V": 12, "E": 30, "F": 20},
    }
    return data.get(shape_name, {"V": 0, "E": 0, "F": 0})

def create_count_label(V, E, F, font_size=32):
    """
    Create a formatted label showing V, E, F counts.

    Args:
        V: Number of vertices
        E: Number of edges
        F: Number of faces
        font_size: Font size

    Returns:
        VGroup with formatted counts
    """
    label = Tex(
        f"V = {V}, \\quad E = {E}, \\quad F = {F}",
        font_size=font_size
    )
    return label

def create_euler_check(V, E, F, font_size=32):
    """
    Create label showing V - E + F calculation.

    Args:
        V, E, F: Vertex, edge, face counts
        font_size: Font size

    Returns:
        Tex object with calculation
    """
    result = V - E + F
    check = "\\checkmark" if result == 2 else "\\times"
    color = GREEN if result == 2 else RED

    calc = Tex(
        f"V - E + F = {V} - {E} + {F} = {result} \\quad {check}",
        font_size=font_size,
        color=color
    )
    return calc

# ============================================================
# 4. BASE CLASSES AND HELPERS
# ============================================================
# No custom base classes needed

# ============================================================
# 5. SCENE IMPLEMENTATIONS
# ============================================================

class IntroducePolyhedra(ThreeDScene):
    """
    Part 1: Introduce various polyhedra in 3D.

    Narrative purpose:
        To showcase beautiful 3D shapes and introduce the concept of
        vertices, edges, and faces that we'll count.

    Mathematical content:
        Displays classic polyhedra (Platonic solids) and introduces
        the fundamental components: V (vertices), E (edges), F (faces).

    Visual approach:
        Show rotating 3D polyhedra with clear labeling. Highlight
        vertices, edges, and faces separately to build familiarity.
    """
    def construct(self):
        # ========================================
        # SETUP: Title (as 2D overlay)
        # ========================================
        title = Text("Euler's Polyhedron Formula", font_size=48)
        title.to_edge(UP)
        title.fix_in_frame()  # Keep fixed in frame for 3D scene

        self.add(title)
        self.wait()

        # ========================================
        # SHOW: A cube rotating
        # ========================================
        cube = Cube(side_length=2)
        cube.set_fill(CUBE_COLOR, opacity=0.7)
        cube.set_stroke(WHITE, width=2)

        # Set up 3D camera
        frame = self.camera.frame
        frame.set_euler_angles(theta=70 * DEGREES, phi=75 * DEGREES)

        self.play(ShowCreation(cube))
        self.wait()

        # Rotate the cube
        self.play(Rotate(cube, angle=2*PI, axis=UP, run_time=4, rate_func=linear))
        self.wait()

        # Label it
        cube_label = Text("Cube", font_size=36)
        cube_label.fix_in_frame()
        cube_label.to_edge(DOWN, buff=1)

        self.play(FadeIn(cube_label, shift=UP))
        self.wait(2)

        # ========================================
        # SHOW: Basic components
        # ========================================
        components = Text(
            "Vertices (V), Edges (E), Faces (F)",
            font_size=32,
            color=YELLOW
        )
        components.fix_in_frame()
        components.next_to(cube_label, UP, buff=0.5)

        self.play(Write(components))
        self.wait(2)

        # ========================================
        # CLEANUP and transition
        # ========================================
        self.play(
            FadeOut(cube),
            FadeOut(cube_label),
            FadeOut(components)
        )

        # ========================================
        # SHOW: Tetrahedron
        # ========================================
        tetrahedron = Tetrahedron()
        tetrahedron.set_height(2.5)
        tetrahedron.set_fill(TETRAHEDRON_COLOR, opacity=0.7)
        tetrahedron.set_stroke(WHITE, width=2)

        tet_label = Text("Tetrahedron", font_size=36)
        tet_label.fix_in_frame()
        tet_label.to_edge(DOWN, buff=1)

        self.play(
            ShowCreation(tetrahedron),
            FadeIn(tet_label, shift=UP)
        )
        self.wait()

        # Rotate
        self.play(Rotate(tetrahedron, angle=2*PI, axis=UP, run_time=4, rate_func=linear))
        self.wait(2)

        # ========================================
        # CLEANUP
        # ========================================
        self.play(
            FadeOut(tetrahedron),
            FadeOut(tet_label),
            FadeOut(title)
        )
        self.wait()


class CountComponents(ThreeDScene):
    """
    Part 2: Count V, E, F for different polyhedra.

    Narrative purpose:
        To systematically count the components of various polyhedra,
        preparing for the verification of Euler's formula.

    Mathematical content:
        Explicitly counts vertices, edges, and faces for cube,
        tetrahedron, and octahedron.

    Visual approach:
        Highlight each component type (vertices glow, edges glow, faces glow)
        while displaying counts on screen.
    """
    def construct(self):
        # ========================================
        # SETUP: Title
        # ========================================
        title = Text("Counting Components", font_size=48)
        title.to_edge(UP)
        title.fix_in_frame()

        self.add(title)
        self.wait()

        # Set up camera
        frame = self.camera.frame
        frame.set_euler_angles(theta=70 * DEGREES, phi=75 * DEGREES)

        # ========================================
        # COUNT: Tetrahedron
        # ========================================
        self.count_polyhedron_components(
            "tetrahedron",
            Tetrahedron(),
            TETRAHEDRON_COLOR,
            "Tetrahedron"
        )

        # ========================================
        # COUNT: Cube
        # ========================================
        self.count_polyhedron_components(
            "cube",
            Cube(),
            CUBE_COLOR,
            "Cube"
        )

        # ========================================
        # COUNT: Octahedron
        # ========================================
        self.count_polyhedron_components(
            "octahedron",
            Octahedron(),
            OCTAHEDRON_COLOR,
            "Octahedron"
        )

        # ========================================
        # CLEANUP
        # ========================================
        self.play(FadeOut(title))
        self.wait()

    def count_polyhedron_components(self, name, shape, color, display_name):
        """Helper to count and display components for a polyhedron."""
        # Setup shape
        shape.set_height(2.5)
        shape.set_fill(color, opacity=0.7)
        shape.set_stroke(WHITE, width=2)

        # Get data
        data = get_polyhedron_data(name)
        V, E, F = data["V"], data["E"], data["F"]

        # Label
        shape_label = Text(display_name, font_size=36)
        shape_label.fix_in_frame()
        shape_label.to_edge(LEFT, buff=0.5).shift(2 * UP)

        # Show shape
        self.play(
            ShowCreation(shape),
            FadeIn(shape_label)
        )
        self.wait()

        # Count vertices
        v_label = Tex(f"V = {V}", font_size=36, color=VERTEX_COLOR)
        v_label.fix_in_frame()
        v_label.next_to(shape_label, DOWN, buff=0.3, aligned_edge=LEFT)

        # Highlight vertices (approximate with dots at corners)
        self.play(
            shape.animate.set_stroke(VERTEX_COLOR, width=8),
            FadeIn(v_label)
        )
        self.wait()
        self.play(shape.animate.set_stroke(WHITE, width=2))

        # Count edges
        e_label = Tex(f"E = {E}", font_size=36, color=EDGE_COLOR)
        e_label.fix_in_frame()
        e_label.next_to(v_label, DOWN, buff=0.3, aligned_edge=LEFT)

        self.play(
            shape.animate.set_stroke(EDGE_COLOR, width=6),
            FadeIn(e_label)
        )
        self.wait()
        self.play(shape.animate.set_stroke(WHITE, width=2))

        # Count faces
        f_label = Tex(f"F = {F}", font_size=36, color=FACE_COLOR)
        f_label.fix_in_frame()
        f_label.next_to(e_label, DOWN, buff=0.3, aligned_edge=LEFT)

        self.play(
            shape.animate.set_fill(FACE_COLOR, opacity=0.9),
            FadeIn(f_label)
        )
        self.wait()
        self.play(shape.animate.set_fill(color, opacity=0.7))

        self.wait(2)

        # Cleanup
        self.play(
            FadeOut(shape),
            FadeOut(shape_label),
            FadeOut(v_label),
            FadeOut(e_label),
            FadeOut(f_label)
        )


class VerifyFormula(InteractiveScene):
    """
    Part 3: Verify V - E + F = 2 for all polyhedra.

    Narrative purpose:
        To demonstrate that despite different shapes having different
        V, E, F values, the formula V - E + F always equals 2.

    Mathematical content:
        Computes V - E + F for tetrahedron, cube, octahedron, dodecahedron,
        and icosahedron, showing all equal 2.

    Visual approach:
        Create a table showing all polyhedra with their counts and
        the verification that V - E + F = 2 in each case.
    """
    def construct(self):
        # ========================================
        # SETUP: Title
        # ========================================
        title = Text("Euler's Formula", font_size=48)
        title.to_edge(UP)

        self.play(FadeIn(title, shift=DOWN))
        self.wait()

        # ========================================
        # STATE: The formula
        # ========================================
        formula = Tex(
            R"V - E + F = 2",
            font_size=60,
            color=YELLOW
        )
        formula.next_to(title, DOWN, buff=0.7)

        box = SurroundingRectangle(formula, buff=0.3, color=YELLOW, stroke_width=3)

        self.play(
            Write(formula),
            ShowCreation(box)
        )
        self.wait(2)

        # ========================================
        # VERIFY: Create table
        # ========================================
        self.play(
            VGroup(formula, box).animate.scale(0.7).to_corner(UL, buff=0.5)
        )

        # Table header
        verification_title = Text("Verification for Platonic Solids", font_size=36)
        verification_title.shift(1.5 * UP)

        self.play(Write(verification_title))
        self.wait()

        # Create table data
        polyhedra = ["tetrahedron", "cube", "octahedron", "dodecahedron", "icosahedron"]
        names = ["Tetrahedron", "Cube", "Octahedron", "Dodecahedron", "Icosahedron"]

        table_rows = []
        for i, (poly, name) in enumerate(zip(polyhedra, names)):
            data = get_polyhedron_data(poly)
            V, E, F = data["V"], data["E"], data["F"]

            row = VGroup(
                Text(name, font_size=24),
                Tex(f"{V}", font_size=24),
                Tex(f"{E}", font_size=24),
                Tex(f"{F}", font_size=24),
                Tex(f"{V - E + F}", font_size=24, color=GREEN)
            )
            row.arrange(RIGHT, buff=0.8)
            table_rows.append(row)

        # Table header row
        header = VGroup(
            Text("Shape", font_size=24, weight=BOLD),
            Tex("V", font_size=24, color=VERTEX_COLOR),
            Tex("E", font_size=24, color=EDGE_COLOR),
            Tex("F", font_size=24, color=FACE_COLOR),
            Tex("V-E+F", font_size=24, color=YELLOW)
        )
        header.arrange(RIGHT, buff=0.8)

        # Arrange table
        table = VGroup(header, *table_rows)
        table.arrange(DOWN, buff=0.4, aligned_edge=LEFT)
        table.next_to(verification_title, DOWN, buff=0.7)
        table.shift(0.5 * LEFT)

        # Animate table
        self.play(FadeIn(header, shift=DOWN))
        self.wait()

        for row in table_rows:
            self.play(FadeIn(row, shift=DOWN))
            self.wait(0.5)

        self.wait(2)

        # ========================================
        # EMPHASIZE: All equal 2
        # ========================================
        emphasis = Text(
            "Always equals 2!",
            font_size=42,
            color=GREEN,
            weight=BOLD
        )
        emphasis.to_edge(DOWN, buff=1)

        self.play(FadeIn(emphasis, scale=1.5))
        self.wait(3)

        # ========================================
        # CLEANUP
        # ========================================
        self.play(FadeOut(*self.mobjects), run_time=1)
        self.wait()


class ProofSketch(InteractiveScene):
    """
    Part 4: Sketch the proof using planar graph representation.

    Narrative purpose:
        To provide intuition for why Euler's formula is true by showing
        how a polyhedron can be "flattened" into a planar graph.

    Mathematical content:
        Shows that removing one face and flattening creates a planar graph.
        Uses induction on faces: each face removal changes F by -1 and E by -1,
        keeping V - E + F constant.

    Visual approach:
        Visualize "cutting" a polyhedron and laying it flat, then show
        step-by-step face removal maintaining the Euler characteristic.
    """
    def construct(self):
        # ========================================
        # SETUP: Title
        # ========================================
        title = Text("Why Does This Work?", font_size=48)
        title.to_edge(UP)

        self.play(FadeIn(title, shift=DOWN))
        self.wait()

        # ========================================
        # CONCEPT: Planar graph representation
        # ========================================
        concept = Text(
            "Key Idea: Flatten the polyhedron into a planar graph",
            font_size=32
        )
        concept.next_to(title, DOWN, buff=0.7)

        self.play(Write(concept))
        self.wait(2)

        # ========================================
        # VISUALIZE: Cube to planar graph
        # ========================================
        # Show a simplified cube wireframe
        cube_desc = Text("Cube (3D)", font_size=28)
        cube_desc.shift(3 * LEFT + 1 * UP)

        # Simple cube representation (square with diagonals)
        cube_diagram = VGroup(
            Square(side_length=1.5),
            Square(side_length=1.5).shift(0.3 * UP + 0.3 * RIGHT),
        )
        for sq in cube_diagram:
            sq.set_stroke(BLUE, 2)

        # Connect corners
        lines = VGroup()
        for i in range(4):
            line = Line(
                cube_diagram[0].get_vertices()[i],
                cube_diagram[1].get_vertices()[i]
            )
            line.set_stroke(BLUE, 2)
            lines.add(line)

        cube_3d = VGroup(cube_diagram, lines)
        cube_3d.next_to(cube_desc, DOWN, buff=0.5)

        self.play(
            Write(cube_desc),
            ShowCreation(cube_3d)
        )
        self.wait(2)

        # ========================================
        # TRANSFORM: To planar graph
        # ========================================
        arrow = Arrow(LEFT, RIGHT, buff=0.5, color=YELLOW)
        arrow.next_to(cube_3d, RIGHT, buff=0.8)

        planar_desc = Text("Planar Graph (2D)", font_size=28)
        planar_desc.next_to(arrow, RIGHT, buff=0.8).shift(0.5 * UP)

        # Simplified planar graph (remove one face and flatten)
        # Draw as a square grid
        planar_graph = VGroup()
        size = 1.5
        positions = [
            [-size/2, size/2, 0], [size/2, size/2, 0],
            [size/2, -size/2, 0], [-size/2, -size/2, 0],
            [0, size/2, 0], [size/2, 0, 0],
            [0, -size/2, 0], [-size/2, 0, 0]
        ]

        # Draw vertices
        vertices = VGroup(*[Dot(pos, radius=0.08, color=YELLOW) for pos in positions])

        # Draw edges
        edges = VGroup(
            Line(positions[0], positions[1]),
            Line(positions[1], positions[2]),
            Line(positions[2], positions[3]),
            Line(positions[3], positions[0]),
            Line(positions[0], positions[4]),
            Line(positions[4], positions[1]),
            Line(positions[1], positions[5]),
            Line(positions[5], positions[2]),
            Line(positions[2], positions[6]),
            Line(positions[6], positions[3]),
            Line(positions[3], positions[7]),
            Line(positions[7], positions[0]),
        )
        for edge in edges:
            edge.set_stroke(GREEN, 2)

        planar_graph = VGroup(edges, vertices)
        planar_graph.next_to(planar_desc, DOWN, buff=0.5)

        self.play(ShowCreation(arrow))
        self.play(
            Write(planar_desc),
            TransformFromCopy(cube_3d, planar_graph)
        )
        self.wait(2)

        # ========================================
        # EXPLAIN: The proof idea
        # ========================================
        self.play(
            FadeOut(concept),
            FadeOut(cube_desc),
            FadeOut(cube_3d),
            FadeOut(arrow),
            FadeOut(planar_desc),
            VGroup(planar_graph).animate.shift(2 * UP).scale(0.8)
        )

        proof_steps = VGroup(
            Text("Proof Sketch:", font_size=32, weight=BOLD),
            Text("1. Remove one face and flatten → planar graph", font_size=26),
            Text("2. Remove faces one by one (removes 1 face, 1+ edges)", font_size=26),
            Text("3. Each step keeps V - E + F unchanged", font_size=26),
            Text("4. End with one face (a tree): V - E + F = V - (V-1) + 1 = 2", font_size=26),
            Text("5. Therefore, original polyhedron has V - E + F = 2", font_size=26),
        )
        proof_steps.arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        proof_steps.to_edge(DOWN, buff=0.5).shift(0.5 * LEFT)

        self.play(
            LaggedStart(
                *[FadeIn(step, shift=RIGHT) for step in proof_steps],
                lag_ratio=0.5
            ),
            run_time=6
        )
        self.wait(4)

        # ========================================
        # CONCLUSION
        # ========================================
        conclusion = Text(
            "This formula is a topological invariant!",
            font_size=36,
            color=YELLOW,
            weight=BOLD
        )
        conclusion.move_to(ORIGIN)

        self.play(
            FadeOut(proof_steps),
            FadeOut(planar_graph),
            FadeOut(title)
        )
        self.play(FadeIn(conclusion, scale=1.5))
        self.wait(3)

        # ========================================
        # CLEANUP
        # ========================================
        self.play(FadeOut(conclusion))
        self.wait()


# ============================================================
# 6. SCENE EXECUTION ORDER
# ============================================================
# The order of scenes that tells the story.
#
# Scene 1 (IntroducePolyhedra):
#   - Shows beautiful 3D polyhedra
#   - Introduces V, E, F concepts
#   - Builds visual familiarity
#
# Scene 2 (CountComponents):
#   - Systematically counts V, E, F for different shapes
#   - Highlights each component type
#   - Prepares for formula verification
#
# Scene 3 (VerifyFormula):
#   - States Euler's formula V - E + F = 2
#   - Verifies for all five Platonic solids
#   - Shows the remarkable consistency
#
# Scene 4 (ProofSketch):
#   - Explains why the formula works
#   - Uses planar graph representation
#   - Provides proof intuition via face removal

SCENE_ORDER = [
    IntroducePolyhedra,    # Part 1: Visual introduction
    CountComponents,       # Part 2: Counting exercise
    VerifyFormula,         # Part 3: Formula verification
    ProofSketch,           # Part 4: Proof sketch
]
