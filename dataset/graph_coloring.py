"""
Graph Coloring Problem

This module demonstrates the graph coloring problem, where we assign colors to
vertices of a graph such that no two adjacent vertices have the same color.
Covers the Four Color Theorem, chromatic number, and greedy algorithms.

Scenes:
    - IntroduceColoringProblem: Introduction to graph coloring with map example
    - FourColorTheorem: The famous Four Color Theorem
    - ChromaticNumber: Understanding chromatic numbers of different graphs
    - GreedyAlgorithm: Greedy coloring algorithm demonstration
"""

from manimlib import *
import numpy as np


class IntroduceColoringProblem(Scene):
    """
    Introduce the graph coloring problem using map coloring.
    """

    def construct(self):
        # Title
        title = OldTexText("The Graph Coloring Problem", font_size=52)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait()

        # The problem statement
        problem = OldTexText(
            "Color regions so that adjacent regions have different colors",
            font_size=32,
            color=YELLOW
        )
        problem.move_to(UP * 2.5)
        self.play(Write(problem))
        self.wait(2)

        # Create a simple map (abstract regions)
        # Region A (center)
        region_a = Polygon(
            LEFT * 0.5 + UP * 0.3,
            RIGHT * 0.5 + UP * 0.3,
            RIGHT * 0.5 + DOWN * 0.3,
            LEFT * 0.5 + DOWN * 0.3,
            fill_opacity=0.6,
            fill_color=GREY,
            stroke_color=WHITE,
            stroke_width=3
        )

        # Region B (top)
        region_b = Polygon(
            LEFT * 0.5 + UP * 0.3,
            RIGHT * 0.5 + UP * 0.3,
            RIGHT * 1 + UP * 1.5,
            LEFT * 1 + UP * 1.5,
            fill_opacity=0.6,
            fill_color=GREY,
            stroke_color=WHITE,
            stroke_width=3
        )

        # Region C (right)
        region_c = Polygon(
            RIGHT * 0.5 + UP * 0.3,
            RIGHT * 0.5 + DOWN * 0.3,
            RIGHT * 2 + DOWN * 0.8,
            RIGHT * 2 + UP * 0.8,
            fill_opacity=0.6,
            fill_color=GREY,
            stroke_color=WHITE,
            stroke_width=3
        )

        # Region D (bottom)
        region_d = Polygon(
            LEFT * 0.5 + DOWN * 0.3,
            RIGHT * 0.5 + DOWN * 0.3,
            RIGHT * 1 + DOWN * 1.5,
            LEFT * 1 + DOWN * 1.5,
            fill_opacity=0.6,
            fill_color=GREY,
            stroke_color=WHITE,
            stroke_width=3
        )

        # Region E (left)
        region_e = Polygon(
            LEFT * 0.5 + UP * 0.3,
            LEFT * 0.5 + DOWN * 0.3,
            LEFT * 2 + DOWN * 0.8,
            LEFT * 2 + UP * 0.8,
            fill_opacity=0.6,
            fill_color=GREY,
            stroke_color=WHITE,
            stroke_width=3
        )

        regions = VGroup(region_a, region_b, region_c, region_d, region_e)
        regions.move_to(DOWN * 0.5)

        # Labels
        label_a = OldTexText("A", font_size=32).move_to(region_a.get_center())
        label_b = OldTexText("B", font_size=32).move_to(region_b.get_center())
        label_c = OldTexText("C", font_size=32).move_to(region_c.get_center())
        label_d = OldTexText("D", font_size=32).move_to(region_d.get_center())
        label_e = OldTexText("E", font_size=32).move_to(region_e.get_center())

        labels = VGroup(label_a, label_b, label_c, label_d, label_e)

        self.play(LaggedStart([ShowCreation(region) for region in regions], lag_ratio=0.2))
        self.wait(0.5)
        self.play(Write(labels))
        self.wait()

        # Color the regions
        self.play(region_a.animate.set_fill(RED, opacity=0.6))
        self.wait(0.5)
        self.play(region_b.animate.set_fill(BLUE, opacity=0.6))
        self.wait(0.5)
        self.play(region_c.animate.set_fill(GREEN, opacity=0.6))
        self.wait(0.5)
        self.play(region_d.animate.set_fill(BLUE, opacity=0.6))
        self.wait(0.5)
        self.play(region_e.animate.set_fill(GREEN, opacity=0.6))
        self.wait()

        # Highlight that adjacent regions have different colors
        note = OldTexText("Adjacent regions have different colors!", font_size=32, color=GREEN)
        note.to_edge(DOWN)
        self.play(Write(note))
        self.wait(2)

        # Convert to graph representation
        self.play(
            FadeOut(regions),
            FadeOut(labels),
            FadeOut(note),
            FadeOut(problem)
        )

        graph_title = OldTexText("As a Graph:", font_size=40, color=YELLOW)
        graph_title.move_to(UP * 2.5)
        self.play(Write(graph_title))
        self.wait()

        # Create graph nodes
        node_a = Circle(radius=0.3, fill_opacity=0.7, fill_color=RED, stroke_color=WHITE)
        node_a.move_to(ORIGIN)
        node_b = Circle(radius=0.3, fill_opacity=0.7, fill_color=BLUE, stroke_color=WHITE)
        node_b.move_to(UP * 2)
        node_c = Circle(radius=0.3, fill_opacity=0.7, fill_color=GREEN, stroke_color=WHITE)
        node_c.move_to(RIGHT * 2.5 + UP * 0.5)
        node_d = Circle(radius=0.3, fill_opacity=0.7, fill_color=BLUE, stroke_color=WHITE)
        node_d.move_to(DOWN * 2)
        node_e = Circle(radius=0.3, fill_opacity=0.7, fill_color=GREEN, stroke_color=WHITE)
        node_e.move_to(LEFT * 2.5 + UP * 0.5)

        nodes = VGroup(node_a, node_b, node_c, node_d, node_e)

        # Labels
        label_a2 = OldTexText("A", font_size=24).move_to(node_a.get_center())
        label_b2 = OldTexText("B", font_size=24).move_to(node_b.get_center())
        label_c2 = OldTexText("C", font_size=24).move_to(node_c.get_center())
        label_d2 = OldTexText("D", font_size=24).move_to(node_d.get_center())
        label_e2 = OldTexText("E", font_size=24).move_to(node_e.get_center())

        # Edges (adjacent regions)
        edge_ab = Line(node_a.get_top(), node_b.get_bottom(), stroke_width=2)
        edge_ac = Line(node_a.get_right(), node_c.get_left(), stroke_width=2)
        edge_ad = Line(node_a.get_bottom(), node_d.get_top(), stroke_width=2)
        edge_ae = Line(node_a.get_left(), node_e.get_right(), stroke_width=2)

        edges = VGroup(edge_ab, edge_ac, edge_ad, edge_ae)

        self.play(LaggedStart([ShowCreation(edge) for edge in edges], lag_ratio=0.2))
        self.wait(0.5)
        self.play(LaggedStart([ShowCreation(node) for node in nodes], lag_ratio=0.1))
        self.wait(0.5)
        self.play(Write(VGroup(label_a2, label_b2, label_c2, label_d2, label_e2)))
        self.wait(2)

        # Count colors
        colors_used = OldTexText("3 colors used: Red, Blue, Green", font_size=32, color=YELLOW)
        colors_used.to_edge(DOWN)
        self.play(Write(colors_used))
        self.wait(3)


class FourColorTheorem(Scene):
    """
    Present the famous Four Color Theorem.
    """

    def construct(self):
        # Title
        title = OldTexText("The Four Color Theorem", font_size=52)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait()

        # Statement of the theorem
        theorem_box = Rectangle(height=2.5, width=11, color=YELLOW)
        theorem_box.move_to(UP * 1.5)

        theorem_text = OldTexText(
            "Any map can be colored using at most 4 colors",
            font_size=36,
            color=YELLOW
        )
        theorem_text.move_to(theorem_box.get_center() + UP * 0.4)

        condition = OldTexText(
            "such that no adjacent regions share the same color",
            font_size=30,
            color=GREY
        )
        condition.move_to(theorem_box.get_center() + DOWN * 0.3)

        self.play(ShowCreation(theorem_box))
        self.wait(0.5)
        self.play(Write(theorem_text))
        self.wait(0.5)
        self.play(Write(condition))
        self.wait(2)

        # Historical context
        history_title = OldTexText("Historical Context:", font_size=36, color=BLUE)
        history_title.move_to(DOWN * 0.5)
        self.play(Write(history_title))
        self.wait()

        history = VGroup(
            OldTexText("• Conjectured in 1852 by Francis Guthrie", font_size=28),
            OldTexText("• Attempted by many mathematicians for over a century", font_size=28),
            OldTexText("• First proved in 1976 by Appel and Haken", font_size=28),
            OldTexText("• Used computer verification (controversial!)", font_size=28, color=RED),
        )
        history.arrange(DOWN, aligned_edge=LEFT, buff=0.35)
        history.next_to(history_title, DOWN, buff=0.5)

        self.play(LaggedStart([Write(h) for h in history], lag_ratio=0.4))
        self.wait(3)

        # Example: Why not 3?
        self.play(
            FadeOut(theorem_box),
            FadeOut(theorem_text),
            FadeOut(condition),
            FadeOut(history_title),
            FadeOut(history)
        )

        example_title = OldTexText("Why not 3 colors?", font_size=40, color=YELLOW)
        example_title.move_to(UP * 2.8)
        self.play(Write(example_title))
        self.wait()

        # Create K4 (complete graph on 4 vertices) which needs 4 colors
        explanation = OldTexText("Counterexample: 4 mutually adjacent regions", font_size=32)
        explanation.next_to(example_title, DOWN, buff=0.4)
        self.play(Write(explanation))
        self.wait()

        # K4 vertices
        radius = 1.5
        angles = [PI/2 + i * PI/2 for i in range(4)]
        positions = [np.array([radius * np.cos(a), radius * np.sin(a), 0]) for a in angles]

        nodes = VGroup(*[
            Circle(radius=0.35, fill_opacity=0.7, stroke_color=WHITE, stroke_width=3)
            .move_to(pos)
            for pos in positions
        ])

        # All edges (complete graph)
        edges = VGroup()
        for i in range(4):
            for j in range(i + 1, 4):
                edge = Line(positions[i], positions[j], stroke_width=2, color=GREY)
                edges.add(edge)

        self.play(LaggedStart([ShowCreation(edge) for edge in edges], lag_ratio=0.05))
        self.wait(0.5)

        # Color nodes with 4 different colors
        colors = [RED, BLUE, GREEN, YELLOW]
        for i, (node, color) in enumerate(zip(nodes, colors)):
            node.set_fill(color)
            self.play(ShowCreation(node), run_time=0.5)
            self.wait(0.3)

        self.wait()

        conclusion = OldTexText("Each region touches all others → need 4 colors", font_size=30, color=GREEN)
        conclusion.to_edge(DOWN)
        self.play(Write(conclusion))
        self.wait(3)


class ChromaticNumber(Scene):
    """
    Explore chromatic numbers of different graphs.
    """

    def construct(self):
        # Title
        title = OldTexText("Chromatic Number", font_size=52)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait()

        # Definition
        definition = OldTexText(
            "χ(G) = minimum number of colors needed to color graph G",
            font_size=32,
            color=YELLOW
        )
        definition.next_to(title, DOWN, buff=0.5)
        self.play(Write(definition))
        self.wait(2)

        # Example 1: Path graph (χ = 2)
        example1_title = OldTexText("Path Graph", font_size=36, color=BLUE)
        example1_title.move_to(UP * 1.5 + LEFT * 4.5)
        self.play(Write(example1_title))
        self.wait()

        # Create path: v1 - v2 - v3 - v4
        path_nodes = VGroup(*[
            Circle(radius=0.25, fill_opacity=0.7, stroke_color=WHITE)
            .move_to(LEFT * 4.5 + UP * (0.5 - i * 0.5))
            for i in range(4)
        ])

        path_edges = VGroup(*[
            Line(path_nodes[i].get_center(), path_nodes[i+1].get_center(), stroke_width=2)
            for i in range(3)
        ])

        self.play(LaggedStart([ShowCreation(edge) for edge in path_edges], lag_ratio=0.2))
        self.wait(0.5)

        # Color with 2 colors alternating
        colors_2 = [RED, BLUE, RED, BLUE]
        for node, color in zip(path_nodes, colors_2):
            node.set_fill(color)
            self.play(ShowCreation(node), run_time=0.3)

        chi_1 = Tex(R"\chi = 2", font_size=32, color=GREEN)
        chi_1.next_to(path_nodes, DOWN, buff=0.5)
        self.play(Write(chi_1))
        self.wait(2)

        # Example 2: Cycle graph (χ = 2 or 3)
        example2_title = OldTexText("Cycle Graph (odd)", font_size=36, color=GREEN)
        example2_title.move_to(UP * 1.5 + RIGHT * 0)
        self.play(Write(example2_title))
        self.wait()

        # Create cycle: C5 (5-cycle)
        cycle_radius = 0.8
        cycle_center = UP * 0 + RIGHT * 0
        cycle_angles = [PI/2 + i * 2*PI/5 for i in range(5)]
        cycle_positions = [cycle_center + cycle_radius * np.array([np.cos(a), np.sin(a), 0])
                          for a in cycle_angles]

        cycle_nodes = VGroup(*[
            Circle(radius=0.2, fill_opacity=0.7, stroke_color=WHITE)
            .move_to(pos)
            for pos in cycle_positions
        ])

        cycle_edges = VGroup(*[
            Line(cycle_positions[i], cycle_positions[(i+1) % 5], stroke_width=2)
            for i in range(5)
        ])

        self.play(LaggedStart([ShowCreation(edge) for edge in cycle_edges], lag_ratio=0.1))
        self.wait(0.5)

        # Color with 3 colors (odd cycle needs 3)
        colors_3 = [RED, BLUE, RED, BLUE, GREEN]
        for node, color in zip(cycle_nodes, colors_3):
            node.set_fill(color)
            self.play(ShowCreation(node), run_time=0.3)

        chi_2 = Tex(R"\chi = 3", font_size=32, color=GREEN)
        chi_2.next_to(cycle_nodes, DOWN, buff=0.8)
        self.play(Write(chi_2))
        self.wait(2)

        # Example 3: Complete graph K4 (χ = 4)
        example3_title = OldTexText("Complete Graph K₄", font_size=36, color=PURPLE)
        example3_title.move_to(UP * 1.5 + RIGHT * 4.5)
        self.play(Write(example3_title))
        self.wait()

        # Create K4
        k4_radius = 0.7
        k4_center = UP * 0 + RIGHT * 4.5
        k4_angles = [PI/2 + i * PI/2 for i in range(4)]
        k4_positions = [k4_center + k4_radius * np.array([np.cos(a), np.sin(a), 0])
                       for a in k4_angles]

        k4_nodes = VGroup(*[
            Circle(radius=0.2, fill_opacity=0.7, stroke_color=WHITE)
            .move_to(pos)
            for pos in k4_positions
        ])

        k4_edges = VGroup()
        for i in range(4):
            for j in range(i + 1, 4):
                edge = Line(k4_positions[i], k4_positions[j], stroke_width=1.5, color=GREY)
                k4_edges.add(edge)

        self.play(LaggedStart([ShowCreation(edge) for edge in k4_edges], lag_ratio=0.03))
        self.wait(0.5)

        # Color with 4 colors
        colors_4 = [RED, BLUE, GREEN, YELLOW]
        for node, color in zip(k4_nodes, colors_4):
            node.set_fill(color)
            self.play(ShowCreation(node), run_time=0.3)

        chi_3 = Tex(R"\chi = 4", font_size=32, color=GREEN)
        chi_3.next_to(k4_nodes, DOWN, buff=0.8)
        self.play(Write(chi_3))
        self.wait(2)

        # General formula for complete graph
        formula = Tex(R"\chi(K_n) = n", font_size=36, color=YELLOW)
        formula.to_edge(DOWN)
        self.play(Write(formula))
        self.wait(3)


class GreedyAlgorithm(Scene):
    """
    Demonstrate the greedy coloring algorithm.
    """

    def construct(self):
        # Title
        title = OldTexText("Greedy Coloring Algorithm", font_size=52)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait()

        # Algorithm description
        algo_title = OldTexText("Algorithm:", font_size=36, color=YELLOW)
        algo_title.move_to(UP * 2.5 + LEFT * 4.5)
        self.play(Write(algo_title))
        self.wait()

        steps = VGroup(
            OldTexText("1. Order the vertices", font_size=26),
            OldTexText("2. For each vertex:", font_size=26),
            OldTexText("   • Check colors of neighbors", font_size=24, color=GREY),
            OldTexText("   • Assign smallest available color", font_size=24, color=GREY),
        )
        steps.arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        steps.next_to(algo_title, DOWN, buff=0.4, aligned_edge=LEFT)
        self.play(LaggedStart([Write(step) for step in steps], lag_ratio=0.3))
        self.wait(2)

        # Create a sample graph
        graph_title = OldTexText("Example:", font_size=32, color=BLUE)
        graph_title.move_to(UP * 2.5 + RIGHT * 3)
        self.play(Write(graph_title))
        self.wait()

        # Graph structure
        positions = {
            0: RIGHT * 2 + UP * 1.5,
            1: RIGHT * 4 + UP * 1.5,
            2: RIGHT * 2 + DOWN * 0,
            3: RIGHT * 4 + DOWN * 0,
            4: RIGHT * 3 + DOWN * 1.5
        }

        nodes = VGroup(*[
            Circle(radius=0.3, fill_opacity=0.3, fill_color=GREY, stroke_color=WHITE, stroke_width=2)
            .move_to(pos)
            for pos in positions.values()
        ])

        labels = VGroup(*[
            OldTexText(str(i), font_size=24).move_to(pos)
            for i, pos in positions.items()
        ])

        # Edges
        edge_list = [(0, 1), (0, 2), (1, 3), (2, 3), (2, 4), (3, 4)]
        edges = VGroup(*[
            Line(positions[i], positions[j], stroke_width=2, color=GREY)
            for i, j in edge_list
        ])

        self.play(LaggedStart([ShowCreation(edge) for edge in edges], lag_ratio=0.1))
        self.wait(0.5)
        self.play(LaggedStart([ShowCreation(node) for node in nodes], lag_ratio=0.1))
        self.wait(0.5)
        self.play(Write(labels))
        self.wait()

        # Color assignment
        colors = [RED, BLUE, GREEN, YELLOW, PURPLE, ORANGE]
        vertex_colors = []

        status = OldTexText("Coloring...", font_size=28, color=YELLOW)
        status.to_edge(DOWN)
        self.play(Write(status))

        # Greedy coloring in order 0, 1, 2, 3, 4
        for vertex_id in range(5):
            # Highlight current vertex
            self.play(nodes[vertex_id].animate.set_stroke(color=YELLOW, width=4))
            self.wait(0.5)

            # Find neighbors
            neighbors = [j if i == vertex_id else i
                        for i, j in edge_list
                        if i == vertex_id or j == vertex_id]

            # Find neighbor colors
            neighbor_colors = [vertex_colors[n] for n in neighbors if n < vertex_id]

            # Assign smallest available color
            color_idx = 0
            while color_idx < len(colors) and colors[color_idx] in neighbor_colors:
                color_idx += 1

            assigned_color = colors[color_idx]
            vertex_colors.append(assigned_color)

            # Color the vertex
            self.play(
                nodes[vertex_id].animate.set_fill(assigned_color, opacity=0.7),
                nodes[vertex_id].animate.set_stroke(color=WHITE, width=2)
            )
            self.wait(0.7)

        # Result
        self.play(FadeOut(status))
        result = OldTexText(f"Colors used: {len(set(vertex_colors))}", font_size=32, color=GREEN)
        result.to_edge(DOWN)
        self.play(Write(result))
        self.wait()

        # Note about optimality
        note = OldTexText(
            "Note: Greedy may not always give optimal coloring!",
            font_size=26,
            color=GREY,
            slant=ITALIC
        )
        note.next_to(result, UP, buff=0.3)
        self.play(Write(note))
        self.wait(3)


# Utility functions for graph coloring

def greedy_coloring(adjacency_list, vertex_order=None):
    """
    Apply greedy coloring algorithm to a graph.

    Args:
        adjacency_list: Dictionary {vertex: [neighbors]}
        vertex_order: Optional list specifying vertex ordering

    Returns:
        Dictionary {vertex: color} where color is an integer
    """
    if vertex_order is None:
        vertex_order = list(adjacency_list.keys())

    coloring = {}

    for vertex in vertex_order:
        # Find colors of neighbors
        neighbor_colors = {coloring[neighbor]
                          for neighbor in adjacency_list[vertex]
                          if neighbor in coloring}

        # Find smallest available color
        color = 0
        while color in neighbor_colors:
            color += 1

        coloring[vertex] = color

    return coloring


def chromatic_number_upper_bound(adjacency_list):
    """
    Compute upper bound on chromatic number using greedy algorithm.

    Args:
        adjacency_list: Dictionary {vertex: [neighbors]}

    Returns:
        Upper bound on chromatic number
    """
    coloring = greedy_coloring(adjacency_list)
    return max(coloring.values()) + 1


def is_valid_coloring(adjacency_list, coloring):
    """
    Check if a coloring is valid (no adjacent vertices have same color).

    Args:
        adjacency_list: Dictionary {vertex: [neighbors]}
        coloring: Dictionary {vertex: color}

    Returns:
        True if coloring is valid
    """
    for vertex, neighbors in adjacency_list.items():
        vertex_color = coloring[vertex]
        for neighbor in neighbors:
            if coloring[neighbor] == vertex_color:
                return False
    return True


def chromatic_number_complete_graph(n):
    """
    Return chromatic number of complete graph K_n.

    Args:
        n: Number of vertices

    Returns:
        Chromatic number (which equals n)
    """
    return n


def chromatic_number_cycle(n):
    """
    Return chromatic number of cycle graph C_n.

    Args:
        n: Number of vertices in cycle

    Returns:
        Chromatic number (2 if n is even, 3 if n is odd)
    """
    return 2 if n % 2 == 0 else 3


def chromatic_number_bipartite():
    """
    Return chromatic number of any bipartite graph.

    Returns:
        2 (all bipartite graphs are 2-colorable)
    """
    return 2


def welsh_powell_coloring(adjacency_list):
    """
    Apply Welsh-Powell algorithm (greedy with degree-based ordering).

    Args:
        adjacency_list: Dictionary {vertex: [neighbors]}

    Returns:
        Dictionary {vertex: color}
    """
    # Order vertices by degree (descending)
    vertex_order = sorted(adjacency_list.keys(),
                         key=lambda v: len(adjacency_list[v]),
                         reverse=True)

    return greedy_coloring(adjacency_list, vertex_order)
