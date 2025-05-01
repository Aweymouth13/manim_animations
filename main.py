import os
import numpy as np
from manim import *

class WignerToLiouville3D(ThreeDScene):
    def construct(self):
        title = Text('wigner to liouville transition', font_size=36).to_edge(UP)
        self.play(Write(title))

        axes = ThreeDAxes(
            x_range=[-5, 5, 1],
            y_range=[-5, 5, 1],
            z_range=[-1, 1, 0.5],
            axis_config={'include_tip': True}
        )
        labels = axes.get_axis_labels(x_label='x', y_label='p', z_label='W(x,p)')
        for lbl in labels:
            lbl.set_shade_in_3d(True)
        self.play(Create(axes), Write(labels))

        hbar = ValueTracker(1.0)

        def wigner(u, v):
            h = hbar.get_value()
            return (1 / (PI * h)) * np.exp(-u**2 - v**2) * np.cos(2 * u * v / h)

        surface = always_redraw(lambda: Surface(
            lambda u, v: axes.c2p(u, v, wigner(u, v)),
            u_range=[-5, 5],
            v_range=[-5, 5],
            resolution=(30, 30),
            fill_opacity=0.7,
            checkerboard_colors=[BLUE_D, BLUE_E]
        ))

        self.play(FadeIn(surface), run_time=2)

        eq1 = MathTex(
            r'W(x,p)=\frac{1}{\pi\hbar}e^{-x^2-p^2}\cos\Bigl(\frac{2xp}{\hbar}\Bigr)'
        ).to_edge(DOWN)
        self.play(Write(eq1), run_time=2)

        arrow = MathTex(r'\hbar\to0').next_to(eq1, UP)
        self.play(Write(arrow))

        self.play(hbar.animate.set_value(0.1), run_time=5)

        eq2 = MathTex(r'\frac{\partial f}{\partial t} + \{f,H\} = 0').to_edge(DOWN)
        self.play(Transform(eq1, eq2), Transform(arrow, Text('classical liouville', font_size=24)))

        note = Text('action principle bridges both', font_size=24).next_to(eq2, DOWN)
        self.play(Write(note))

        self.set_camera_orientation(phi=60 * DEGREES, theta=30 * DEGREES)
        self.begin_ambient_camera_rotation(rate=0.1)
        self.wait(6)
        self.stop_ambient_camera_rotation()

        self.play(FadeOut(VGroup(title, axes, labels, surface, eq1, arrow, note)))

def play():
    os.system('manim -ql main.py WignerToLiouville3D --output_file=wigner_liouville.mp4')

if __name__ == '__main__':
    play()
