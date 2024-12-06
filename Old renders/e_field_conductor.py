import os
from manim import *
import numpy as np
 
class Arrow3D(Arrow):
    def __init__(self, start, end, **kwargs):
        super().__init__(start=start, end=end, **kwargs)
 
 
 
class ElectricFieldWithConductor(ThreeDScene):
    NUM_FIELD_LINES = 500
 
    def electric_field(self, x, y, z):
        #check for negative z
        if z < 0:
            return np.array([0, 0, 0])  #no field if z < 0
        y_value = np.sqrt(z) if z > 0 else 0  #set y_value if z > 0
        #calculate field strength
        r = np.sqrt(x**2 + y_value**(3/2) + np.sqrt(z))
        if r == 0:
            return np.array([0, 0, 0])  #avoid division by zero
        field_strength = 1 / r**2  #inverse square law
        return field_strength * np.array([x, y_value, z])  #radial field
 
 
    def construct(self):
        #title
        title = Text("Electric Field Around a Conductor", font_size=36).to_edge(UP)
        self.play(Write(title))
        self.wait(1)
 
        #create conductor
        conductor = Sphere(radius=1.0, color=GRAY, fill_opacity=0.8)
        self.play(Create(conductor))
        self.wait(1)
 
        num_field_lines = self.NUM_FIELD_LINES
        field_radius = 3.0
 
        field_lines = VGroup()
 
        for i in range(num_field_lines):
            #generate field points
            phi = np.arccos(1 - 2 * (i + 0.5) / num_field_lines)
            theta = np.pi * (1 + 5**0.5) * (i + 0.5)
 
            x = field_radius * np.sin(phi) * np.cos(theta)
            y = field_radius * np.sin(phi) * np.sin(theta)
            z = field_radius * np.cos(phi)
 
            #calculate electric field vector
            field_vector = self.electric_field(x, y, z)
 
            start_point = np.array([x, y, z])
            end_point = start_point + 0.5 * field_vector  #scale field vector
 
            arrow = Arrow3D(
                start=start_point,
                end=end_point,
                color=BLUE,
                stroke_width=2,
                max_tip_length_to_length_ratio=0.2
            )
            field_lines.add(arrow)
 
        #animate field lines
        self.play(LaggedStartMap(Create, field_lines, lag_ratio=0.02))
        self.wait(1)
 
        #inside text
        inside_text = Text("E = 0 Inside the Conductor", font_size=24, color=YELLOW)
        inside_text.next_to(conductor, DOWN, buff=0.5)
        self.play(Write(inside_text))
        self.wait(1)
 
        #field equation
        equation = MathTex(
            r"\vec{E} = \frac{1}{4\pi\epsilon_0} \frac{q}{r^2} \hat{r}",
            color=WHITE
        )
        equation.to_edge(DOWN)
        self.play(Write(equation))
        self.wait(3)
 
        #fade out text
        self.play(FadeOut(inside_text, equation, title))
 
        #camera rotation
        self.begin_ambient_camera_rotation(rate=0.2)
        self.wait(5)
        self.stop_ambient_camera_rotation()
 
        #final text
        final_text = Text("Maxwell Dictates the Behavior of Electric Fields", font_size=28, color=GREEN)
        final_text.to_edge(UP)
        self.play(Transform(title, final_text))
        self.wait(2)
 
        #fade out all
        self.play(FadeOut(VGroup(title, conductor, field_lines, equation, final_text)))
        self.wait(1)
 
def play():
    os.system("manim -qp main.py ElectricFieldWithConductor --output_file=ElectricField_Conductor.mp4")
 
if __name__ == "__main__":
    play()
