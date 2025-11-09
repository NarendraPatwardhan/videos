"""
Markov Chains and Random Walks

This module demonstrates Markov chains, random walks, and their applications.
Covers state transitions, transition matrices, steady-state distributions,
and the famous PageRank algorithm.

Scenes:
    - IntroduceRandomWalk: Introduction to random walks and Markov property
    - TransitionMatrix: Understanding transition matrices and probabilities
    - SteadyState: Finding steady-state distributions
    - PageRankExample: Application to Google's PageRank algorithm
"""

from manimlib import *
import numpy as np


class IntroduceRandomWalk(Scene):
    """
    Introduce random walks and the Markov property.
    """

    def construct(self):
        # Title
        title = Text("Markov Chains and Random Walks", font_size=52)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait()

        # Markov property
        property_title = Text("The Markov Property", font_size=40, color=YELLOW)
        property_title.move_to(2.2 * UP)

        property_text = Text(
            '"The future depends only on the present, not the past"',
            font_size=32,
            color=GREY,
            slant=ITALIC
        )
        property_text.next_to(property_title, DOWN, buff=0.4)

        self.play(Write(property_title))
        self.wait(0.5)
        self.play(Write(property_text))
        self.wait(2)

        # Formal definition
        formal = Tex(
            R"P(X_{n+1} | X_n, X_{n-1}, \ldots, X_0) = P(X_{n+1} | X_n)",
            font_size=36
        )
        formal.next_to(property_text, DOWN, buff=0.6)
        self.play(Write(formal))
        self.wait(2)

        # Clear and show random walk example
        self.play(
            FadeOut(property_title),
            FadeOut(property_text),
            FadeOut(formal)
        )

        # Simple random walk on a number line
        walk_title = Text("Example: Random Walk on a Line", font_size=40, color=BLUE)
        walk_title.move_to(2.5 * UP)
        self.play(Write(walk_title))
        self.wait()

        # Create number line
        number_line = NumberLine(
            x_range=[-5, 5, 1],
            length=10,
            include_numbers=True,
            font_size=24
        )
        number_line.move_to(UP * 0.5)
        self.play(Create(number_line))
        self.wait()

        # Walker
        walker = Dot(number_line.n2p(0), color=RED, radius=0.12)
        self.play(FadeIn(walker))
        self.wait()

        # Rules
        rules = VGroup(
            Text("Each step:", font_size=32),
            Text("• Move left with probability 0.5", font_size=28),
            Text("• Move right with probability 0.5", font_size=28)
        )
        rules.arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        rules.move_to(DOWN * 2)
        self.play(Write(rules))
        self.wait()

        # Simulate random walk
        position = 0
        np.random.seed(42)

        for step in range(10):
            move = np.random.choice([-1, 1])
            position += move
            position = np.clip(position, -5, 5)  # Stay on screen

            self.play(
                walker.animate.move_to(number_line.n2p(position)),
                run_time=0.5
            )
            self.wait(0.3)

        self.wait(2)


class TransitionMatrix(Scene):
    """
    Explain transition matrices and state probabilities.
    """

    def construct(self):
        # Title
        title = Text("Transition Matrix", font_size=52)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait()

        # Simple example: Weather model
        example_title = Text("Example: Weather Model", font_size=40, color=YELLOW)
        example_title.next_to(title, DOWN, buff=0.5)
        self.play(Write(example_title))
        self.wait()

        # States
        states_label = Text("States:", font_size=32, color=GREY)
        states_label.move_to(1.5 * UP + 4.5 * LEFT)

        sunny = Text("Sunny", font_size=32, color=YELLOW)
        rainy = Text("Rainy", font_size=32, color=BLUE)

        states = VGroup(sunny, rainy)
        states.arrange(DOWN, buff=0.5, aligned_edge=LEFT)
        states.next_to(states_label, DOWN, buff=0.3)

        self.play(Write(states_label))
        self.wait(0.5)
        self.play(Write(sunny), Write(rainy))
        self.wait()

        # State diagram
        diagram_center = RIGHT * 2.5 + UP * 0.8

        # Nodes
        sunny_node = Circle(radius=0.8, color=YELLOW, fill_opacity=0.2)
        sunny_node.move_to(diagram_center + LEFT * 2)
        sunny_label = Text("S", font_size=36, color=YELLOW)
        sunny_label.move_to(sunny_node.get_center())

        rainy_node = Circle(radius=0.8, color=BLUE, fill_opacity=0.2)
        rainy_node.move_to(diagram_center + RIGHT * 2)
        rainy_label = Text("R", font_size=36, color=BLUE)
        rainy_label.move_to(rainy_node.get_center())

        self.play(
            Create(sunny_node),
            Create(rainy_node),
            Write(sunny_label),
            Write(rainy_label)
        )
        self.wait()

        # Transitions
        # S to S (self-loop)
        s_to_s = Arc(
            radius=1.2,
            start_angle=PI/4,
            angle=3*PI/2,
            color=YELLOW
        )
        s_to_s.move_arc_center_to(sunny_node.get_center() + UP * 0.8)
        s_to_s_label = Tex("0.7", font_size=28).next_to(s_to_s, UP, buff=0.1)

        # S to R
        s_to_r = Arrow(
            sunny_node.get_right(),
            rainy_node.get_left(),
            buff=0.8,
            color=GREEN
        )
        s_to_r_label = Tex("0.3", font_size=28).next_to(s_to_r, UP, buff=0.1)

        # R to R (self-loop)
        r_to_r = Arc(
            radius=1.2,
            start_angle=PI/4,
            angle=3*PI/2,
            color=BLUE
        )
        r_to_r.move_arc_center_to(rainy_node.get_center() + UP * 0.8)
        r_to_r_label = Tex("0.6", font_size=28).next_to(r_to_r, UP, buff=0.1)

        # R to S
        r_to_s = Arrow(
            rainy_node.get_left(),
            sunny_node.get_right(),
            buff=0.8,
            color=GREEN
        )
        r_to_s.shift(DOWN * 0.3)
        r_to_s_label = Tex("0.4", font_size=28).next_to(r_to_s, DOWN, buff=0.1)

        transitions = VGroup(s_to_s, s_to_r, r_to_r, r_to_s)
        labels = VGroup(s_to_s_label, s_to_r_label, r_to_r_label, r_to_s_label)

        self.play(
            LaggedStart(*[Create(t) for t in transitions], lag_ratio=0.3)
        )
        self.wait(0.5)
        self.play(
            LaggedStart(*[Write(l) for l in labels], lag_ratio=0.3)
        )
        self.wait(2)

        # Transition matrix
        matrix_label = Text("Transition Matrix P:", font_size=36)
        matrix_label.move_to(DOWN * 1.5 + LEFT * 3)

        # Matrix showing P[i][j] = probability of going from state i to state j
        transition_matrix = Matrix(
            [["0.7", "0.3"],
             ["0.4", "0.6"]],
            h_buff=1.2,
            bracket_h_buff=0.1,
            bracket_v_buff=0.1
        )
        transition_matrix.next_to(matrix_label, RIGHT, buff=0.5)

        # Row and column labels
        row_labels = VGroup(
            Text("S", font_size=24, color=YELLOW),
            Text("R", font_size=24, color=BLUE)
        )
        row_labels.arrange(DOWN, buff=0.68)
        row_labels.next_to(transition_matrix, LEFT, buff=0.3)

        col_labels = VGroup(
            Text("S", font_size=24, color=YELLOW),
            Text("R", font_size=24, color=BLUE)
        )
        col_labels.arrange(RIGHT, buff=0.9)
        col_labels.next_to(transition_matrix, UP, buff=0.3)

        self.play(Write(matrix_label))
        self.wait(0.5)
        self.play(Write(transition_matrix))
        self.wait(0.5)
        self.play(Write(row_labels), Write(col_labels))
        self.wait()

        # Highlight row sum = 1
        note = Text("Each row sums to 1", font_size=28, color=GREEN)
        note.next_to(transition_matrix, DOWN, buff=0.5)
        self.play(Write(note))
        self.wait(2)


class SteadyState(Scene):
    """
    Demonstrate finding steady-state distributions.
    """

    def construct(self):
        # Title
        title = Text("Steady-State Distribution", font_size=52)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait()

        # Question
        question = Text(
            "What happens after many transitions?",
            font_size=36,
            color=YELLOW
        )
        question.move_to(2 * UP)
        self.play(Write(question))
        self.wait()

        # Transition matrix (same as before)
        P_label = Tex("P = ", font_size=40)
        P_label.move_to(0.8 * UP + LEFT * 4)

        P = Matrix(
            [["0.7", "0.3"],
             ["0.4", "0.6"]],
            h_buff=1.0
        )
        P.next_to(P_label, RIGHT, buff=0.3)

        self.play(Write(P_label), Write(P))
        self.wait()

        # Initial distribution
        pi0_label = Tex(R"\pi_0 = ", font_size=40)
        pi0_label.next_to(P_label, DOWN, buff=0.7, aligned_edge=LEFT)

        pi0 = Matrix([["0.5"], ["0.5"]], h_buff=0.6)
        pi0.next_to(pi0_label, RIGHT, buff=0.3)

        pi0_text = Text("(Start: 50% sunny, 50% rainy)", font_size=24, color=GREY)
        pi0_text.next_to(pi0, RIGHT, buff=0.5)

        self.play(Write(pi0_label), Write(pi0))
        self.wait(0.5)
        self.play(Write(pi0_text))
        self.wait()

        # Evolution
        evolution_label = Text("Evolution:", font_size=32, color=BLUE)
        evolution_label.next_to(pi0_label, DOWN, buff=0.8, aligned_edge=LEFT)
        self.play(Write(evolution_label))
        self.wait()

        # Show iterations
        evolution_eq = Tex(R"\pi_{n+1} = P^T \pi_n", font_size=36)
        evolution_eq.next_to(evolution_label, DOWN, buff=0.4)
        self.play(Write(evolution_eq))
        self.wait(2)

        # After many steps
        self.play(FadeOut(question))

        steady_label = Text("Steady State:", font_size=36, color=GREEN)
        steady_label.move_to(2 * UP)

        steady_condition = Tex(R"\pi^* = P^T \pi^*", font_size=40)
        steady_condition.next_to(steady_label, DOWN, buff=0.4)

        self.play(Write(steady_label))
        self.wait(0.5)
        self.play(Write(steady_condition))
        self.wait()

        # Solution
        self.play(
            FadeOut(P_label),
            FadeOut(P),
            FadeOut(pi0_label),
            FadeOut(pi0),
            FadeOut(pi0_text),
            FadeOut(evolution_label),
            FadeOut(evolution_eq)
        )

        solution_title = Text("Solving for steady state:", font_size=32)
        solution_title.move_to(0.5 * UP + LEFT * 3)

        # System of equations
        eq1 = Tex(R"0.7\pi_S + 0.4\pi_R = \pi_S", font_size=32)
        eq2 = Tex(R"0.3\pi_S + 0.6\pi_R = \pi_R", font_size=32)
        eq3 = Tex(R"\pi_S + \pi_R = 1", font_size=32)

        equations = VGroup(eq1, eq2, eq3)
        equations.arrange(DOWN, aligned_edge=LEFT, buff=0.4)
        equations.next_to(solution_title, DOWN, buff=0.5)

        self.play(Write(solution_title))
        self.wait(0.5)
        self.play(LaggedStart(*[Write(eq) for eq in equations], lag_ratio=0.4))
        self.wait(2)

        # Result
        result_box = Rectangle(height=1.5, width=6, color=GREEN)
        result_box.move_to(DOWN * 2)

        result = Tex(
            R"\pi^* = \begin{bmatrix} 4/7 \\ 3/7 \end{bmatrix}",
            font_size=44,
            color=GREEN
        )
        result.move_to(result_box.get_center() + LEFT * 1.5)

        interpretation = Text("≈ 57% sunny, 43% rainy", font_size=28)
        interpretation.next_to(result, RIGHT, buff=0.5)

        self.play(Create(result_box))
        self.play(Write(result))
        self.wait(0.5)
        self.play(Write(interpretation))
        self.wait(3)


class PageRankExample(Scene):
    """
    Demonstrate PageRank algorithm as an application of Markov chains.
    """

    def construct(self):
        # Title
        title = Text("Application: Google PageRank", font_size=52)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait()

        # Subtitle
        subtitle = Text(
            "Ranking web pages using Markov chains",
            font_size=32,
            color=GREY
        )
        subtitle.next_to(title, DOWN, buff=0.3)
        self.play(Write(subtitle))
        self.wait(2)

        # Create a simple web graph
        web_title = Text("Web Graph:", font_size=36, color=YELLOW)
        web_title.move_to(2.3 * UP + LEFT * 4.5)
        self.play(Write(web_title))
        self.wait()

        # Nodes (web pages)
        positions = {
            "A": LEFT * 3 + UP * 0.5,
            "B": UP * 0.5,
            "C": RIGHT * 3 + UP * 0.5,
            "D": DOWN * 1.5
        }

        nodes = {}
        labels = {}

        for name, pos in positions.items():
            circle = Circle(radius=0.5, color=BLUE, fill_opacity=0.2)
            circle.move_to(pos)
            label = Text(name, font_size=32, color=WHITE)
            label.move_to(pos)

            nodes[name] = circle
            labels[name] = label

            self.play(Create(circle), Write(label), run_time=0.5)

        self.wait()

        # Links (directed edges)
        links = [
            ("A", "B"), ("A", "C"),
            ("B", "C"),
            ("C", "A"),
            ("D", "A"), ("D", "B"), ("D", "C")
        ]

        edges = []
        for start, end in links:
            arrow = Arrow(
                nodes[start].get_center(),
                nodes[end].get_center(),
                buff=0.5,
                color=GREEN,
                stroke_width=2
            )
            edges.append(arrow)
            self.play(Create(arrow), run_time=0.4)

        self.wait()

        # Random surfer model
        explanation_title = Text("Random Surfer Model:", font_size=32, color=YELLOW)
        explanation_title.move_to(UP * 2.3 + RIGHT * 3.5)

        explanation = VGroup(
            Text("• Start at random page", font_size=24),
            Text("• Click random outgoing link", font_size=24),
            Text("• Repeat many times", font_size=24),
            Text("• Count visits to each page", font_size=24)
        )
        explanation.arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        explanation.next_to(explanation_title, DOWN, buff=0.4, aligned_edge=LEFT)

        self.play(Write(explanation_title))
        self.wait(0.5)
        self.play(LaggedStart(*[Write(item) for item in explanation], lag_ratio=0.3))
        self.wait(2)

        # Show transition probabilities
        self.play(
            FadeOut(explanation_title),
            FadeOut(explanation)
        )

        prob_title = Text("Transition Probabilities:", font_size=32, color=BLUE)
        prob_title.move_to(UP * 2.3 + RIGHT * 3.5)
        self.play(Write(prob_title))
        self.wait()

        # Example: from A, can go to B or C with equal probability
        prob_text = VGroup(
            Text("From A: → B (1/2), → C (1/2)", font_size=24),
            Text("From B: → C (1)", font_size=24),
            Text("From C: → A (1)", font_size=24),
            Text("From D: → A (1/3), → B (1/3), → C (1/3)", font_size=24)
        )
        prob_text.arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        prob_text.next_to(prob_title, DOWN, buff=0.4, aligned_edge=LEFT)

        self.play(LaggedStart(*[Write(item) for item in prob_text], lag_ratio=0.3))
        self.wait(2)

        # PageRank scores
        self.play(
            FadeOut(prob_title),
            FadeOut(prob_text)
        )

        scores_title = Text("PageRank Scores:", font_size=36, color=GREEN)
        scores_title.move_to(UP * 2.3 + RIGHT * 3.5)

        # Hypothetical scores
        scores = VGroup(
            Text("A: 0.32", font_size=28, color=YELLOW),
            Text("B: 0.19", font_size=28),
            Text("C: 0.34", font_size=28, color=YELLOW),
            Text("D: 0.15", font_size=28)
        )
        scores.arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        scores.next_to(scores_title, DOWN, buff=0.4, aligned_edge=LEFT)

        self.play(Write(scores_title))
        self.wait(0.5)
        self.play(LaggedStart(*[Write(score) for score in scores], lag_ratio=0.2))
        self.wait()

        # Highlight top pages
        self.play(
            nodes["A"].animate.set_fill(YELLOW, opacity=0.4),
            nodes["C"].animate.set_fill(YELLOW, opacity=0.4)
        )
        self.wait(2)

        # Key insight
        insight = Text(
            "Pages with more incoming links (especially from important pages) rank higher",
            font_size=26,
            color=GREY
        )
        insight.to_edge(DOWN)
        self.play(Write(insight))
        self.wait(3)


# Utility functions for Markov chains

def create_transition_matrix(edges, states):
    """
    Create a transition matrix from a list of edges.

    Args:
        edges: List of (from_state, to_state, probability) tuples
        states: List of state names

    Returns:
        Transition matrix as numpy array
    """
    n = len(states)
    matrix = np.zeros((n, n))
    state_to_idx = {state: i for i, state in enumerate(states)}

    for from_state, to_state, prob in edges:
        i = state_to_idx[from_state]
        j = state_to_idx[to_state]
        matrix[i][j] = prob

    return matrix


def find_steady_state(transition_matrix, tolerance=1e-10, max_iterations=1000):
    """
    Find the steady-state distribution of a Markov chain.

    Args:
        transition_matrix: Transition matrix (rows sum to 1)
        tolerance: Convergence tolerance
        max_iterations: Maximum number of iterations

    Returns:
        Steady-state distribution vector
    """
    n = transition_matrix.shape[0]
    # Start with uniform distribution
    state = np.ones(n) / n

    for _ in range(max_iterations):
        new_state = transition_matrix.T @ state
        if np.allclose(new_state, state, atol=tolerance):
            return new_state
        state = new_state

    return state


def simulate_markov_chain(transition_matrix, initial_state, num_steps):
    """
    Simulate a Markov chain for a given number of steps.

    Args:
        transition_matrix: Transition matrix
        initial_state: Index of initial state
        num_steps: Number of steps to simulate

    Returns:
        List of states visited
    """
    n = transition_matrix.shape[0]
    states = [initial_state]
    current = initial_state

    for _ in range(num_steps):
        probabilities = transition_matrix[current]
        current = np.random.choice(n, p=probabilities)
        states.append(current)

    return states


def compute_pagerank(link_matrix, damping=0.85, tolerance=1e-6, max_iterations=100):
    """
    Compute PageRank scores for a web graph.

    Args:
        link_matrix: Adjacency matrix where link_matrix[i][j] = 1 if page i links to page j
        damping: Damping factor (typically 0.85)
        tolerance: Convergence tolerance
        max_iterations: Maximum iterations

    Returns:
        PageRank scores for each page
    """
    n = link_matrix.shape[0]

    # Compute out-degrees (number of outgoing links)
    out_degrees = link_matrix.sum(axis=1)

    # Handle dangling nodes (pages with no outgoing links)
    out_degrees[out_degrees == 0] = 1

    # Create transition matrix
    transition = link_matrix / out_degrees[:, np.newaxis]

    # Add damping
    # P = damping * transition + (1 - damping) / n
    teleport = (1 - damping) / n

    # Initialize PageRank scores
    pr = np.ones(n) / n

    for _ in range(max_iterations):
        new_pr = damping * (transition.T @ pr) + teleport
        if np.allclose(new_pr, pr, atol=tolerance):
            break
        pr = new_pr

    return pr


def random_walk_2d(steps, step_size=1):
    """
    Generate a 2D random walk.

    Args:
        steps: Number of steps
        step_size: Size of each step

    Returns:
        Array of (x, y) positions
    """
    angles = np.random.uniform(0, 2 * PI, steps)
    dx = step_size * np.cos(angles)
    dy = step_size * np.sin(angles)

    x = np.cumsum(np.concatenate([[0], dx]))
    y = np.cumsum(np.concatenate([[0], dy]))

    return np.column_stack([x, y])
