"""
Fourier Transform

This module demonstrates the continuous Fourier Transform, which extends the concept
of Fourier series from periodic functions to arbitrary signals. Shows the transition
from discrete frequency analysis to continuous frequency domain representation.

Scenes:
    - FromSeriesToTransform: Transition from Fourier series to transform
    - FrequencyDomain: Understanding the frequency domain representation
    - WavePackets: Analyzing wave packets and localized signals
    - Applications: Real-world applications of Fourier transforms
"""

from manimlib import *
import numpy as np


class FromSeriesToTransform(Scene):
    """
    Show the transition from Fourier series (discrete) to Fourier transform (continuous).
    """

    def construct(self):
        # Title
        title = Text("From Fourier Series to Fourier Transform", font_size=48)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait()

        # Fourier Series recap
        series_title = Text("Fourier Series (Periodic)", font_size=36, color=BLUE)
        series_title.move_to(2.5 * UP + 3.5 * LEFT)

        series_eq = Tex(
            R"f(t) = \sum_{n=-\infty}^{\infty} c_n e^{i n \omega_0 t}",
            font_size=32
        )
        series_eq.next_to(series_title, DOWN, buff=0.4)

        series_note = Text("Discrete frequencies", font_size=24, color=GREY)
        series_note.next_to(series_eq, DOWN, buff=0.3)

        # Show periodic signal
        axes_series = Axes(
            x_range=[0, 4, 1],
            y_range=[-1.5, 1.5, 0.5],
            height=2.5,
            width=5,
            axis_config={"include_tip": False}
        )
        axes_series.next_to(series_note, DOWN, buff=0.3)
        axes_series.shift(LEFT * 0.5)

        # Periodic square wave
        def periodic_wave(x):
            period = 2
            x_mod = x % period
            return 1 if x_mod < period / 2 else -1

        periodic_graph = axes_series.get_graph(
            lambda x: np.sign(np.sin(2 * PI * x)),
            x_range=[0, 4],
            color=BLUE,
            discontinuities=np.arange(0, 4, 1)
        )

        self.play(Write(series_title))
        self.wait(0.5)
        self.play(Write(series_eq))
        self.wait(0.5)
        self.play(Write(series_note))
        self.wait(0.5)
        self.play(Create(axes_series), Create(periodic_graph))
        self.wait(2)

        # Fourier Transform
        transform_title = Text("Fourier Transform (Aperiodic)", font_size=36, color=GREEN)
        transform_title.move_to(2.5 * UP + 3.5 * RIGHT)

        transform_eq = Tex(
            R"\hat{f}(\omega) = \int_{-\infty}^{\infty} f(t) e^{-i\omega t} dt",
            font_size=30
        )
        transform_eq.next_to(transform_title, DOWN, buff=0.4)

        transform_note = Text("Continuous frequencies", font_size=24, color=GREY)
        transform_note.next_to(transform_eq, DOWN, buff=0.3)

        # Show aperiodic signal
        axes_transform = Axes(
            x_range=[-2, 2, 1],
            y_range=[-1.5, 1.5, 0.5],
            height=2.5,
            width=5,
            axis_config={"include_tip": False}
        )
        axes_transform.next_to(transform_note, DOWN, buff=0.3)
        axes_transform.shift(RIGHT * 0.5)

        # Gaussian pulse
        gaussian_graph = axes_transform.get_graph(
            lambda x: np.exp(-x**2),
            x_range=[-2, 2],
            color=GREEN
        )

        self.play(Write(transform_title))
        self.wait(0.5)
        self.play(Write(transform_eq))
        self.wait(0.5)
        self.play(Write(transform_note))
        self.wait(0.5)
        self.play(Create(axes_transform), Create(gaussian_graph))
        self.wait(2)

        # Highlight the key difference
        arrow = Arrow(
            series_note.get_right(),
            transform_note.get_left(),
            color=YELLOW
        )
        arrow.shift(UP * 0.2)

        transition_text = Text("Increase period → ∞", font_size=28, color=YELLOW)
        transition_text.next_to(arrow, UP, buff=0.1)

        self.play(Create(arrow), Write(transition_text))
        self.wait(3)


class FrequencyDomain(Scene):
    """
    Visualize signals in the frequency domain.
    """

    def construct(self):
        # Title
        title = Text("The Frequency Domain", font_size=52)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait()

        # Time domain
        time_label = Text("Time Domain", font_size=36, color=BLUE)
        time_label.move_to(2.5 * UP + 4 * LEFT)

        time_axes = Axes(
            x_range=[0, 4, 1],
            y_range=[-2, 2, 1],
            height=3,
            width=5,
            axis_config={
                "include_tip": False,
                "numbers_to_exclude": []
            }
        )
        time_axes.next_to(time_label, DOWN, buff=0.5)
        time_axes.add_coordinates()

        # X and Y labels
        t_label = Tex("t", font_size=32).next_to(time_axes.x_axis, RIGHT)
        f_label = Tex("f(t)", font_size=32).next_to(time_axes.y_axis, UP)

        # Create a signal: sum of two sine waves
        def signal(t):
            return 0.8 * np.sin(2 * PI * 2 * t) + 0.5 * np.sin(2 * PI * 5 * t)

        signal_graph = time_axes.get_graph(signal, x_range=[0, 4], color=BLUE)

        self.play(Write(time_label))
        self.play(Create(time_axes), Write(t_label), Write(f_label))
        self.wait(0.5)
        self.play(Create(signal_graph), run_time=2)
        self.wait()

        # Frequency domain
        freq_label = Text("Frequency Domain", font_size=36, color=GREEN)
        freq_label.move_to(2.5 * UP + 4 * RIGHT)

        freq_axes = Axes(
            x_range=[0, 8, 1],
            y_range=[0, 1, 0.5],
            height=3,
            width=5,
            axis_config={
                "include_tip": False,
                "numbers_to_exclude": []
            }
        )
        freq_axes.next_to(freq_label, DOWN, buff=0.5)
        freq_axes.add_coordinates()

        omega_label = Tex(R"\omega", font_size=32).next_to(freq_axes.x_axis, RIGHT)
        F_label = Tex(R"|\hat{f}(\omega)|", font_size=32).next_to(freq_axes.y_axis, UP)

        self.play(Write(freq_label))
        self.play(Create(freq_axes), Write(omega_label), Write(F_label))
        self.wait()

        # Show the frequency components
        # Two spikes at frequencies 2 and 5
        spike1_line = Line(
            freq_axes.c2p(2, 0),
            freq_axes.c2p(2, 0.8),
            color=GREEN,
            stroke_width=6
        )
        spike2_line = Line(
            freq_axes.c2p(5, 0),
            freq_axes.c2p(5, 0.5),
            color=GREEN,
            stroke_width=6
        )

        spike1_label = Tex("2 \\text{ Hz}", font_size=24).next_to(spike1_line, UP, buff=0.1)
        spike2_label = Tex("5 \\text{ Hz}", font_size=24).next_to(spike2_line, UP, buff=0.1)

        self.play(Create(spike1_line), Write(spike1_label))
        self.wait(0.5)
        self.play(Create(spike2_line), Write(spike2_label))
        self.wait(2)

        # Show the transform relationship
        transform_arrow = Arrow(
            time_axes.get_right() + RIGHT * 0.3,
            freq_axes.get_left() + LEFT * 0.3,
            color=YELLOW
        )
        transform_arrow.shift(UP * 0.5)

        ft_symbol = Tex(R"\mathcal{F}", font_size=48, color=YELLOW)
        ft_symbol.next_to(transform_arrow, UP, buff=0.1)

        self.play(Create(transform_arrow), Write(ft_symbol))
        self.wait(2)

        # Explanation
        explanation = Text(
            "Each frequency component is isolated",
            font_size=32,
            color=YELLOW
        )
        explanation.to_edge(DOWN)
        self.play(Write(explanation))
        self.wait(3)


class WavePackets(Scene):
    """
    Demonstrate wave packets and the uncertainty principle.
    """

    def construct(self):
        # Title
        title = Text("Wave Packets and Localization", font_size=50)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait()

        # Create axes for time domain
        time_axes = Axes(
            x_range=[-4, 4, 1],
            y_range=[-1.5, 1.5, 0.5],
            height=3.5,
            width=10,
            axis_config={"include_tip": False}
        )
        time_axes.move_to(UP * 1.5)

        t_label = Tex("t", font_size=32).next_to(time_axes.x_axis, RIGHT)

        # Wave packet (modulated sine wave)
        def wave_packet(t, center=0, width=1, freq=4):
            envelope = np.exp(-((t - center) ** 2) / (2 * width**2))
            carrier = np.cos(2 * PI * freq * t)
            return envelope * carrier

        packet_graph = time_axes.get_graph(
            lambda t: wave_packet(t),
            x_range=[-4, 4],
            color=BLUE
        )

        # Envelope
        envelope_upper = time_axes.get_graph(
            lambda t: np.exp(-(t**2) / 2),
            x_range=[-4, 4],
            color=YELLOW,
            stroke_width=2
        )
        envelope_lower = time_axes.get_graph(
            lambda t: -np.exp(-(t**2) / 2),
            x_range=[-4, 4],
            color=YELLOW,
            stroke_width=2
        )

        self.play(Create(time_axes), Write(t_label))
        self.wait(0.5)
        self.play(Create(packet_graph), run_time=2)
        self.wait()
        self.play(Create(envelope_upper), Create(envelope_lower))
        self.wait()

        # Label
        localized_label = Text("Localized in time", font_size=28, color=BLUE)
        localized_label.next_to(time_axes, RIGHT, buff=0.5)
        self.play(Write(localized_label))
        self.wait(2)

        # Frequency domain
        freq_axes = Axes(
            x_range=[-8, 8, 2],
            y_range=[0, 1.2, 0.5],
            height=3.5,
            width=10,
            axis_config={"include_tip": False}
        )
        freq_axes.move_to(DOWN * 1.5)

        omega_label = Tex(R"\omega", font_size=32).next_to(freq_axes.x_axis, RIGHT)

        # Fourier transform of wave packet (Gaussian centered at freq)
        def ft_wave_packet(omega, center_freq=4, bandwidth=1):
            return np.exp(-((omega - center_freq) ** 2) / (2 * bandwidth**2))

        ft_graph = freq_axes.get_graph(
            lambda w: ft_wave_packet(w),
            x_range=[-8, 8],
            color=GREEN
        )

        self.play(Create(freq_axes), Write(omega_label))
        self.wait(0.5)
        self.play(Create(ft_graph), run_time=2)
        self.wait()

        spread_label = Text("Spread in frequency", font_size=28, color=GREEN)
        spread_label.next_to(freq_axes, RIGHT, buff=0.5)
        self.play(Write(spread_label))
        self.wait(2)

        # Uncertainty principle
        self.play(
            FadeOut(localized_label),
            FadeOut(spread_label)
        )

        uncertainty = Tex(
            R"\Delta t \cdot \Delta \omega \geq \frac{1}{2}",
            font_size=48,
            color=YELLOW
        )
        uncertainty.move_to(RIGHT * 4.5)

        uncertainty_box = SurroundingRectangle(uncertainty, color=YELLOW, buff=0.2)

        uncertainty_label = Text(
            "Uncertainty Principle",
            font_size=32,
            color=YELLOW
        )
        uncertainty_label.next_to(uncertainty_box, UP, buff=0.3)

        self.play(Write(uncertainty_label))
        self.wait(0.5)
        self.play(Write(uncertainty), Create(uncertainty_box))
        self.wait()

        explanation = Text(
            "Cannot be localized in both time and frequency simultaneously",
            font_size=28,
            color=GREY
        )
        explanation.next_to(uncertainty_box, DOWN, buff=0.3)
        self.play(Write(explanation))
        self.wait(3)


class Applications(Scene):
    """
    Show real-world applications of Fourier transforms.
    """

    def construct(self):
        # Title
        title = Text("Applications of Fourier Transform", font_size=52)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait()

        # Create application cards
        applications = [
            {
                "title": "Signal Processing",
                "color": BLUE,
                "items": ["Audio compression (MP3)", "Noise filtering", "Equalization"]
            },
            {
                "title": "Image Processing",
                "color": GREEN,
                "items": ["JPEG compression", "Edge detection", "Image filtering"]
            },
            {
                "title": "Communications",
                "color": PURPLE,
                "items": ["Radio/TV broadcasting", "WiFi/cellular", "Modulation"]
            },
            {
                "title": "Quantum Mechanics",
                "color": RED,
                "items": ["Wave functions", "Momentum space", "Uncertainty"]
            }
        ]

        # Position cards in a 2x2 grid
        positions = [
            UP * 1.5 + LEFT * 3.5,
            UP * 1.5 + RIGHT * 3.5,
            DOWN * 1.5 + LEFT * 3.5,
            DOWN * 1.5 + RIGHT * 3.5
        ]

        cards = VGroup()

        for app, pos in zip(applications, positions):
            # Card background
            card = Rectangle(
                height=2.5,
                width=5.5,
                fill_opacity=0.1,
                fill_color=app["color"],
                stroke_color=app["color"],
                stroke_width=3
            )
            card.move_to(pos)

            # Title
            card_title = Text(app["title"], font_size=32, color=app["color"])
            card_title.move_to(card.get_top() + DOWN * 0.4)

            # Items
            items_group = VGroup()
            for i, item in enumerate(app["items"]):
                item_text = Text(f"• {item}", font_size=22)
                item_text.move_to(card.get_center() + DOWN * (0.3 * i + 0.2))
                items_group.add(item_text)

            card_group = VGroup(card, card_title, items_group)
            cards.add(card_group)

        # Animate cards appearing
        self.play(LaggedStart(*[FadeIn(card) for card in cards], lag_ratio=0.3))
        self.wait(3)

        # Highlight signal processing
        self.play(cards[0].animate.scale(1.1).set_stroke(width=5))
        self.wait()
        self.play(cards[0].animate.scale(1/1.1).set_stroke(width=3))

        # Show a specific example: audio filtering
        self.play(FadeOut(cards))

        example_title = Text("Example: Audio Noise Removal", font_size=40, color=YELLOW)
        example_title.move_to(2.5 * UP)
        self.play(Write(example_title))
        self.wait()

        # Steps
        steps = VGroup(
            Text("1. Transform audio to frequency domain", font_size=28),
            Text("2. Identify and remove noise frequencies", font_size=28),
            Text("3. Inverse transform back to time domain", font_size=28),
            Text("4. Result: Clean audio signal", font_size=28, color=GREEN)
        )
        steps.arrange(DOWN, aligned_edge=LEFT, buff=0.5)
        steps.move_to(UP * 0.3)

        for step in steps:
            self.play(Write(step))
            self.wait(0.8)

        self.wait()

        # Formulas
        forward = Tex(
            R"\hat{f}(\omega) = \int_{-\infty}^{\infty} f(t) e^{-i\omega t} dt",
            font_size=32
        )
        forward.move_to(DOWN * 1.8 + LEFT * 2.5)

        inverse = Tex(
            R"f(t) = \frac{1}{2\pi}\int_{-\infty}^{\infty} \hat{f}(\omega) e^{i\omega t} d\omega",
            font_size=32
        )
        inverse.move_to(DOWN * 1.8 + RIGHT * 2.5)

        forward_label = Text("Forward", font_size=24, color=BLUE).next_to(forward, UP, buff=0.2)
        inverse_label = Text("Inverse", font_size=24, color=GREEN).next_to(inverse, UP, buff=0.2)

        self.play(
            Write(forward_label),
            Write(inverse_label)
        )
        self.wait(0.5)
        self.play(Write(forward), Write(inverse))
        self.wait(3)


# Utility functions for Fourier transforms

def fourier_transform_numerical(signal, time, frequencies):
    """
    Compute numerical Fourier transform of a signal.

    Args:
        signal: Array of signal values
        time: Array of time values
        frequencies: Array of frequencies to evaluate

    Returns:
        Complex Fourier transform values at given frequencies
    """
    dt = time[1] - time[0]
    transform = np.zeros(len(frequencies), dtype=complex)

    for i, freq in enumerate(frequencies):
        # Integrate signal * exp(-i * 2π * freq * t)
        integrand = signal * np.exp(-1j * 2 * PI * freq * time)
        transform[i] = np.trapz(integrand, dx=dt)

    return transform


def inverse_fourier_transform_numerical(spectrum, frequencies, time):
    """
    Compute numerical inverse Fourier transform.

    Args:
        spectrum: Array of complex spectrum values
        frequencies: Array of frequency values
        time: Array of time values to evaluate

    Returns:
        Reconstructed signal at given time points
    """
    df = frequencies[1] - frequencies[0]
    signal = np.zeros(len(time), dtype=complex)

    for i, t in enumerate(time):
        # Integrate spectrum * exp(i * 2π * freq * t)
        integrand = spectrum * np.exp(1j * 2 * PI * frequencies * t)
        signal[i] = np.trapz(integrand, dx=df) / (2 * PI)

    return signal


def gaussian_pulse(t, center=0, width=1):
    """
    Generate a Gaussian pulse.

    Args:
        t: Time array or value
        center: Center of the pulse
        width: Width parameter (standard deviation)

    Returns:
        Gaussian pulse values
    """
    return np.exp(-((t - center) ** 2) / (2 * width ** 2))


def gaussian_spectrum(omega, center=0, bandwidth=1):
    """
    Fourier transform of a Gaussian pulse.

    Args:
        omega: Frequency array or value
        center: Center frequency
        bandwidth: Bandwidth parameter

    Returns:
        Spectrum values
    """
    return np.sqrt(2 * PI) * bandwidth * np.exp(-((omega - center) ** 2) * bandwidth ** 2 / 2)


def window_function(t, window_type="hann", width=1):
    """
    Generate various window functions for signal processing.

    Args:
        t: Time array or value
        window_type: Type of window ("hann", "hamming", "blackman", "rectangular")
        width: Width of the window

    Returns:
        Window function values
    """
    normalized_t = t / width

    if window_type == "hann":
        return np.where(
            np.abs(normalized_t) <= 1,
            0.5 * (1 + np.cos(PI * normalized_t)),
            0
        )
    elif window_type == "hamming":
        return np.where(
            np.abs(normalized_t) <= 1,
            0.54 + 0.46 * np.cos(PI * normalized_t),
            0
        )
    elif window_type == "blackman":
        return np.where(
            np.abs(normalized_t) <= 1,
            0.42 + 0.5 * np.cos(PI * normalized_t) + 0.08 * np.cos(2 * PI * normalized_t),
            0
        )
    else:  # rectangular
        return np.where(np.abs(normalized_t) <= 1, 1, 0)


def create_wave_packet(t, carrier_freq=5, envelope_width=1, center=0):
    """
    Create a wave packet (modulated carrier wave).

    Args:
        t: Time array or value
        carrier_freq: Frequency of carrier wave
        envelope_width: Width of Gaussian envelope
        center: Center of the packet

    Returns:
        Wave packet values
    """
    envelope = gaussian_pulse(t, center=center, width=envelope_width)
    carrier = np.cos(2 * PI * carrier_freq * t)
    return envelope * carrier
