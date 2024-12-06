import os
import shutil
from manim import *
import numpy as np

class Arrow3D(Arrow):
    def __init__(self, start, end, **kwargs):
        super().__init__(start=start, end=end, **kwargs)

class EMWaveVisualizationEnhanced3D(ThreeDScene):
    def construct(self):
        #title
        title = Text("Electromagnetic Wave Propagation", font_size=36).to_edge(UP)
        title.set_shade_in_3d(True)
        self.play(Write(title))
        
        #axes
        axes = ThreeDAxes(
            x_range=[0, 10, 1],
            y_range=[-3, 3, 1],
            z_range=[-3, 3, 1],
            axis_config={"include_tip": True}
        )
        axes_labels = axes.get_axis_labels(x_label="z", y_label="E-field", z_label="B-field")
        for label in axes_labels:
            label.set_shade_in_3d(True)
        
        self.play(Create(axes), Write(axes_labels))
        
        #define wave params
        wavelength = 5
        amplitude_e = 1.5
        amplitude_b = 1.5
        wave_speed = 3.0
        frequency = wave_speed / wavelength
        angular_frequency = 2 * np.pi * frequency
        wave_number = 2 * np.pi / wavelength
        
        #e field oss in y dir
        e_field = ParametricFunction(
            lambda t: np.array([t, amplitude_e * np.sin(wave_number * t - angular_frequency * self.time), 0]),
            t_range=np.array([0, 10]),
            color=YELLOW,
            stroke_width=3
        ).add_updater(lambda m: m.become(
            ParametricFunction(
                lambda t: np.array([t, amplitude_e * np.sin(wave_number * t - angular_frequency * self.time), 0]),
                t_range=np.array([0, 10]),
                color=YELLOW,
                stroke_width=4
            )
        ))
        
        #b field oss in z dir
        b_field = ParametricFunction(
            lambda t: np.array([t, 0, amplitude_b * np.sin(wave_number * t - angular_frequency * self.time)]),
            t_range=np.array([0, 10]),
            color=BLUE,
            stroke_width=4
        ).add_updater(lambda m: m.become(
            ParametricFunction(
                lambda t: np.array([t, 0, amplitude_b * np.sin(wave_number * t - angular_frequency * self.time)]),
                t_range=np.array([0, 10]),
                color=BLUE,
                stroke_width=4
            )
        ))
        
        #add e and b fields
        self.play(Create(e_field), Create(b_field), run_time=2)
        
        #add arrows
        num_arrows = 80
        arrows = VGroup()
        for i in range(num_arrows):
            t = i * (10 / num_arrows)
            #e field arrow
            e_arrow = Arrow3D(
                start=np.array([t, 0, 0]),
                end=np.array([t, amplitude_e * np.sin(wave_number * t - angular_frequency * self.time), 0]),
                color=YELLOW,
                stroke_width=3,
                max_tip_length_to_length_ratio=0.2
            )
            #b field arrow
            b_arrow = Arrow3D(
                start=np.array([t, 0, 0]),
                end=np.array([t, 0, amplitude_b * np.sin(wave_number * t - angular_frequency * self.time)]),
                color=BLUE,
                stroke_width=3,
                max_tip_length_to_length_ratio=0.2
            )
            arrows.add(e_arrow, b_arrow)
        
        #add updater to arrows
        arrows.add_updater(lambda m: m.become(
            VGroup(*[
                Arrow3D(
                    start=np.array([t, 0, 0]),
                    end=np.array([t, amplitude_e * np.sin(wave_number * t - angular_frequency * self.time), 0]),
                    color=YELLOW,
                    stroke_width=3,
                    max_tip_length_to_length_ratio=0.2
                )
                for t in np.linspace(0, 10, num_arrows)
            ] + [
                Arrow3D(
                    start=np.array([t, 0, 0]),
                    end=np.array([t, 0, amplitude_b * np.sin(wave_number * t - angular_frequency * self.time)]),
                    color=BLUE,
                    stroke_width=3,
                    max_tip_length_to_length_ratio=0.2
                )
                for t in np.linspace(0, 10, num_arrows)
            ])
        ))
        
        self.play(LaggedStartMap(Create, arrows), run_time=2)
        
        #add labels
        e_label = MathTex(r"\vec{E}", color=YELLOW).next_to(e_field, UP, buff=0.1)
        e_label.set_shade_in_3d(True)
        b_label = MathTex(r"\vec{B}", color=BLUE).next_to(b_field, DOWN, buff=0.1)
        b_label.set_shade_in_3d(True)
        self.play(Write(e_label), Write(b_label), run_time=1.5)
        
        #add wave eq
        equation = MathTex(
            r"\vec{E}(z, t) = \vec{E}_0 \sin(kz - \omega t)",
            r"\quad",
            r"\vec{B}(z, t) = \vec{B}_0 \sin(kz - \omega t)"
        ).to_edge(DOWN)
        equation.set_shade_in_3d(True)
        self.play(Write(equation), run_time=2)
        
        #add explanation
        explanation = Text(
            "E and B fields oscillate perpendicular to each other and the direction of propagation.",
            font_size=24
        ).next_to(equation, DOWN, buff=0.5)
        explanation.set_shade_in_3d(True)
        self.play(Write(explanation), run_time=2)
        
        #rotate
        self.set_camera_orientation(phi=51 * DEGREES, theta=7 * DEGREES, R=10 * DEGREES)
        self.begin_ambient_camera_rotation(rate=0.1)
        self.wait(10)
        self.stop_ambient_camera_rotation()
        
        #final text
        final_text = Text("Maxwell's Equations Describe Electromagnetic Waves", font_size=28, color=GREEN).to_edge(UP)
        final_text.set_shade_in_3d(True)
        self.play(Transform(title, final_text), run_time=1.5)
        
        #fade out
        self.play(FadeOut(VGroup(title, axes, axes_labels, e_field, b_field, arrows, e_label, b_label, equation, explanation, final_text)))


def play():
    os.system("manim -qp main.py EMWaveVisualizationEnhanced3D --output_file=EM_Wave_Propagation_3D.mp4")

if __name__ == "__main__":
    play()
