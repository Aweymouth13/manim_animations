import os
from manim import *
import numpy as np
 
class Arrow3D(Arrow):
    def __init__(self, start, end, **kwargs):
        super().__init__(start=start, end=end, **kwargs)
 
class MeissnerEffectVisualization(ThreeDScene):
    NUM_FIELD_LINES = 1000
 
    def magnetic_field(self, x, y, z):
        #define magnetic field
        r = np.sqrt(x**4 + y**2 + z**(2))
        if r < 0.1:  #inside superconductor, B=0
            return np.array([0, 0, 0])
        return np.array([x, y, z]) / r**2  #B decreases with distance
 
    def construct(self):
        #title
        title = Text("Meissner Effect in a Superconductor", font_size=36).to_edge(UP)
        self.play(Write(title))
        self.wait(1)
 
        #create superconductor
        superconductor = Sphere(
            radius=2.5,
            color=RED,
            fill_opacity=0.1,          
            checkerboard_colors=None,  
            resolution=(64, 64)        
        )
        self.play(Create(superconductor))
        self.wait(1)
 
        num_field_lines = self.NUM_FIELD_LINES
        field_radius = 4
        field_lines = VGroup()
 
        for i in range(num_field_lines):
            #generate starting points
            phi = np.arccos(1 - 2 * (i + 0.5) / num_field_lines)
            theta = np.pi * (1 + 5**0.5) * (i + 0.5)
 
            x = field_radius * np.sin(phi) * np.cos(theta)
            y = field_radius * np.sin(phi) * np.sin(theta)
            z = field_radius * np.cos(phi)
 
            #calculate magnetic field vector
            field_vector = self.magnetic_field(x, y, z)
 
            start_point = np.array([x, y, z])
            end_point = start_point + 2 * field_vector  #longer arrows
 
            arrow = Arrow3D(
                start=start_point,
                end=end_point,
                color=RED,
                stroke_width=5,  #wider arrows
                max_tip_length_to_length_ratio=0.3
            )
            field_lines.add(arrow)
 
        #animate field lines
        self.play(LaggedStartMap(Create, field_lines, lag_ratio=0.002))
        self.wait(1)
 
        #add explanatory text
        inside_text = Text("B = 0 Inside", font_size=24, color=YELLOW)
        inside_text.next_to(superconductor, LEFT, buff=0.5)
        self.play(Write(inside_text))
        self.wait(1)
 
        equation = MathTex(
            r"\nabla \cdot \vec{B} = 0, \quad \nabla \times \vec{B} = \mu_0 \vec{J}",
            color=WHITE
        )
        equation.to_edge(DOWN)
        self.play(Write(equation))
        self.wait(3)
 
        #fade out text
        self.play(FadeOut(VGroup(title, inside_text, equation)))
 
        #start camera rotation
        self.begin_ambient_camera_rotation(rate=0.2)
        self.wait(3)
        self.stop_ambient_camera_rotation()
 
        #final text
        final_text = Text("Superconductors Expel Magnetic Fields", font_size=28, color=YELLOW_C).move_to(ORIGIN)
 
        #fixed final text
        self.add_fixed_in_frame_mobjects(final_text)
 
        #fade in final text
        self.play(FadeIn(final_text))
        self.wait(2)
 
        #fade out all
        #self.play(FadeOut(VGroup(title, superconductor, field_lines, equation, inside_text, final_text)))
        self.wait(1)
 
def play():
    os.system("manim -qp main.py MeissnerEffectVisualization --output_file=Meissner_Effect.mp4")
 
if __name__ == "__main__":
    play()
