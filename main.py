#lncr net sales payout curve, refactored w/centralized params
import os
from manim import *

CFG={
    'background_color':'#0b0f14',
    'floor_x':151_898,
    'target_x':189_873,
    'ceil_x':227_848,
    'xmin':120_000,
    'xmax':260_000,
    'ymin':0,
    'ymax':180,
    'y_floor':40.0,
    'y_target':100.0,
    'y_ceil':160.0,
    'x_step':20_000,
    'y_step':20,
    'x_length':8.0,
    'y_length':4.0,
    'axes_to_edge':'down',
    'axes_buff':1.5,
    'axis_color':'#94a3b8',
    'axis_opacity':0.6,
    'show_numbers':True,
    'font_title':12,
    'font_ticks':10,
    'font_readout':12,
    'font_caption':18,
    'title_text':'LNCR Net Sales — Payout Curve',
    'title_slant':ITALIC,
    'tag_pad':0.12,
    'tag_bg':'#0b0f14',
    'tag_bg_opacity':0.9,
    'txt_color':WHITE,
    'hline_color':'#475569',
    'hline_width':1.5,
    'hline_opacity':0.85,
    'seg_width':4,
    'seg_color_floor':'#f59e0b',
    'seg_color_target':'#10b981',
    'seg_color_ceil':'#6366f1',
    'dash_length':0.12,
    'dash_opacity':0.95,
    'legend_enabled':True,
    'legend_side':'left',
    'legend_buff':0.4,
    'legend_font':16,
    'legend_pad':0.18,
    'legend_row_gap':0.14,
    'readout_side':'right',
    'readout_buff':0.85,
    'readout_gap':0.5,
    'caption_side':'right',
    'caption_buff':1.0,
    'dot_radius':0.05,
    'dot_color':WHITE,
    'start_sales':130_000,
    'rt_phase1':1.5,
    'rt_phase2':4.5,
    'rt_phase3':4.5,
    'rt_phase4':1.5,
    'rt_fadeshort':0.2,
    'rt_fademed':0.3,
    'rt_lines':0.5,
    'rate':linear,
    'quality':'480',
    'preview':False,
    'output_file':'lncr_bonus_graph.mp4',
    'x_axis_label':'Net Sales ($)',
    'y_axis_label':'Payout (%)',
    'axis_label_font':9,
}

QUALITY_FLAGS={
    '4k':'-qk',
    '1080':'-qh',
    '720':'-qm',
    '480':'-ql'
}

config.background_color=CFG['background_color']

def tag(txt, size, color, pad, bg, bg_op):
    t=Text(txt, font_size=size, color=color)
    bgrect=BackgroundRectangle(t, color=bg, fill_opacity=bg_op, buff=pad)
    return VGroup(bgrect, t)

def build_legend(axes):
    if not CFG['legend_enabled']:
        return VGroup()
    items=[
        (CFG['seg_color_floor'], f'floor 80% • ${CFG["floor_x"]:,}'),
        (CFG['seg_color_target'], f'target 100% • ${CFG["target_x"]:,}'),
        (CFG['seg_color_ceil'], f'ceiling 120% • ${CFG["ceil_x"]:,}')
    ]
    rows=[]
    for color,label in items:
        sw=Line(ORIGIN,RIGHT*0.6).set_stroke(color, CFG['seg_width'])
        tt=Text(label, font_size=CFG['legend_font'], color=CFG['txt_color'])
        row=VGroup(sw, tt).arrange(RIGHT, buff=0.22)
        rows.append(row)
    col=VGroup(*rows).arrange(DOWN, buff=CFG['legend_row_gap'])
    box=BackgroundRectangle(col, color=CFG['tag_bg'], fill_opacity=0.92, buff=CFG['legend_pad'])
    g=VGroup(box,col)
    g.next_to(axes, UP, buff=0)
    if CFG['legend_side']=='left':
        g.to_edge(LEFT, buff=CFG['legend_buff'])
    else:
        g.to_edge(RIGHT, buff=CFG['legend_buff'])
    return g

class LNCRBonusGraph(Scene):
    def construct(self):
        floor_x=CFG['floor_x']; target_x=CFG['target_x']; ceil_x=CFG['ceil_x']
        xmin=CFG['xmin']; xmax=CFG['xmax']; ymin=CFG['ymin']; ymax=CFG['ymax']
        y_floor=CFG['y_floor']; y_target=CFG['y_target']; y_ceil=CFG['y_ceil']

        title=Text(CFG['title_text'], font_size=CFG['font_title'], color=CFG['txt_color'], slant=CFG['title_slant'])
        tbg=BackgroundRectangle(title, color=CFG['tag_bg'], fill_opacity=1.0, buff=0.2)
        self.play(FadeIn(VGroup(tbg,title).to_edge(UP, buff=0.4)), run_time=CFG['rt_fadeshort'])

        axes=Axes(
            x_range=[xmin, xmax, CFG['x_step']],
            y_range=[ymin, ymax, CFG['y_step']],
            x_length=CFG['x_length'], y_length=CFG['y_length'],
            axis_config={
                'include_numbers':CFG['show_numbers'],
                'stroke_color':CFG['axis_color'],
                'stroke_opacity':CFG['axis_opacity']
            }
        ).add_coordinates()

        if CFG['axes_to_edge']=='down':
            axes.to_edge(DOWN, buff=CFG['axes_buff'])
        elif CFG['axes_to_edge']=='up':
            axes.to_edge(UP, buff=CFG['axes_buff'])
        elif CFG['axes_to_edge']=='left':
            axes.to_edge(LEFT, buff=CFG['axes_buff'])
        else:
            axes.to_edge(RIGHT, buff=CFG['axes_buff'])

        self.play(Create(axes), run_time=CFG['rt_fadeshort'])

        xlab=axes.get_x_axis_label(Text(CFG['x_axis_label'], font_size=CFG['axis_label_font']))
        ylab=axes.get_y_axis_label(Text(CFG['y_axis_label'], font_size=CFG['axis_label_font']))
        self.add(xlab, ylab)

        h40=Line(axes.c2p(xmin, y_floor), axes.c2p(xmax, y_floor)).set_stroke(CFG['hline_color'], CFG['hline_width'], opacity=CFG['hline_opacity'])
        h100=Line(axes.c2p(xmin, y_target), axes.c2p(xmax, y_target)).set_stroke(CFG['hline_color'], CFG['hline_width'], opacity=CFG['hline_opacity'])
        h160=Line(axes.c2p(xmin, y_ceil), axes.c2p(xmax, y_ceil)).set_stroke(CFG['hline_color'], CFG['hline_width'], opacity=CFG['hline_opacity'])
        self.play(Create(h40), Create(h100), Create(h160), run_time=CFG['rt_fademed'])

        ylbl_40=tag('minimum 40%', CFG['font_ticks'], CFG['txt_color'], CFG['tag_pad'], CFG['tag_bg'], CFG['tag_bg_opacity'])
        ylbl_100=tag('on target 100%', CFG['font_ticks'], CFG['txt_color'], CFG['tag_pad'], CFG['tag_bg'], CFG['tag_bg_opacity'])
        ylbl_160=tag('maximum 160%', CFG['font_ticks'], CFG['txt_color'], CFG['tag_pad'], CFG['tag_bg'], CFG['tag_bg_opacity'])
        ylbl_40.next_to(h40, LEFT, buff=0.2)
        ylbl_100.next_to(h100, LEFT, buff=0.2)
        ylbl_160.next_to(h160, LEFT, buff=0.2)
        self.play(FadeIn(ylbl_40), FadeIn(ylbl_100), FadeIn(ylbl_160), run_time=CFG['rt_fadeshort'])

        v_floor=DashedLine(axes.c2p(floor_x, ymin), axes.c2p(floor_x, ymax), dash_length=CFG['dash_length'], color=CFG['seg_color_floor']).set_stroke(opacity=CFG['dash_opacity'])
        v_target=DashedLine(axes.c2p(target_x, ymin), axes.c2p(target_x, ymax), dash_length=CFG['dash_length'], color=CFG['seg_color_target']).set_stroke(opacity=CFG['dash_opacity'])
        v_ceil=DashedLine(axes.c2p(ceil_x, ymin), axes.c2p(ceil_x, ymax), dash_length=CFG['dash_length'], color=CFG['seg_color_ceil']).set_stroke(opacity=CFG['dash_opacity'])
        self.play(Create(v_floor), Create(v_target), Create(v_ceil), run_time=CFG['rt_fademed'])

        leg=build_legend(axes)
        if CFG['legend_enabled']:
            self.play(FadeIn(leg), run_time=CFG['rt_fadeshort'])

        seg1=Line(axes.c2p(xmin, y_floor), axes.c2p(floor_x, y_floor)).set_stroke('#374151', CFG['seg_width'])
        seg2=Line(axes.c2p(floor_x, y_floor), axes.c2p(target_x, y_target)).set_stroke(CFG['seg_color_floor'], CFG['seg_width'])
        seg3=Line(axes.c2p(target_x, y_target), axes.c2p(ceil_x, y_ceil)).set_stroke(CFG['seg_color_target'], CFG['seg_width'])
        seg4=Line(axes.c2p(ceil_x, y_ceil), axes.c2p(xmax, y_ceil)).set_stroke(CFG['seg_color_ceil'], CFG['seg_width'])
        self.play(Create(seg1), Create(seg2), Create(seg3), Create(seg4), run_time=CFG['rt_lines'])

        def payout(x):
            if x<=floor_x: return y_floor
            if x<=target_x: return y_floor+(x-floor_x)/(target_x-floor_x)*(y_target-y_floor)
            if x<=ceil_x: return y_target+(x-target_x)/(ceil_x-target_x)*(y_ceil-y_target)
            return y_ceil

        sales=ValueTracker(CFG['start_sales'])
        dot=always_redraw(lambda: Dot(axes.c2p(sales.get_value(), payout(sales.get_value())), radius=CFG['dot_radius'], color=CFG['dot_color']))
        self.add(dot)

        readout_group=VGroup()
        def readout_updater(group):
            current_sales=sales.get_value()
            current_payout=payout(current_sales)
            new_sales_lbl=tag(f'net sales ${int(current_sales):,}', CFG['font_readout'], CFG['txt_color'], CFG['tag_pad'], CFG['tag_bg'], CFG['tag_bg_opacity'])
            new_payout_lbl=tag(f'payout {current_payout:.1f}%', CFG['font_readout'], CFG['txt_color'], CFG['tag_pad'], CFG['tag_bg'], CFG['tag_bg_opacity'])
            arranged=VGroup(new_sales_lbl, new_payout_lbl) if CFG['readout_side']=='left' else VGroup(new_payout_lbl, new_sales_lbl)
            arranged.arrange(RIGHT, buff=CFG['readout_gap'])
            if CFG['readout_side']=='left':
                arranged.next_to(axes, UP, buff=CFG['readout_buff']).to_edge(LEFT, buff=1.2)
            else:
                arranged.next_to(axes, UP, buff=CFG['readout_buff']).to_edge(RIGHT, buff=1.2)
            group.become(arranged)

        readout_group.add_updater(readout_updater)
        self.add(readout_group)

        cap_text='below floor → payout locked at 40%'
        cap=tag(cap_text, CFG['font_caption'], CFG['txt_color'], CFG['tag_pad'], CFG['tag_bg'], CFG['tag_bg_opacity'])
        cap.next_to(axes, UP, buff=0.25)
        if CFG['caption_side']=='left':
            cap.to_edge(LEFT, buff=CFG['caption_buff'])
        else:
            cap.to_edge(RIGHT, buff=CFG['caption_buff'])
        self.play(FadeIn(cap), run_time=CFG['rt_fadeshort'])

        self.play(sales.animate.set_value(floor_x-1), run_time=CFG['rt_phase1'], rate_func=CFG['rate'])
        self.play(
            Transform(cap, tag('80%→100% → straight-line to 100%', CFG['font_caption'], CFG['txt_color'], CFG['tag_pad'], CFG['tag_bg'], CFG['tag_bg_opacity']).move_to(cap)),
            sales.animate.set_value(target_x),
            run_time=CFG['rt_phase2'], rate_func=CFG['rate']
        )
        self.play(
            Transform(cap, tag('100%→120% → straight-line to 160%', CFG['font_caption'], CFG['txt_color'], CFG['tag_pad'], CFG['tag_bg'], CFG['tag_bg_opacity']).move_to(cap)),
            sales.animate.set_value(ceil_x),
            run_time=CFG['rt_phase3'], rate_func=CFG['rate']
        )
        self.play(
            Transform(cap, tag('above ceiling → payout capped at 160%', CFG['font_caption'], CFG['txt_color'], CFG['tag_pad'], CFG['tag_bg'], CFG['tag_bg_opacity']).move_to(cap)),
            sales.animate.set_value(250_000),
            run_time=CFG['rt_phase4'], rate_func=CFG['rate']
        )
        self.wait(1.2)

def _quality_flag(q):
    return QUALITY_FLAGS.get(q.lower(), QUALITY_FLAGS['1080'])

def play():
    scene='LNCRBonusGraph'
    qflag=_quality_flag(CFG['quality'])
    pflag='-p' if CFG['preview'] else ''
    this=os.path.basename(__file__)
    out=CFG['output_file']
    cmd=f'manim {pflag} {qflag} {this} {scene} --output_file={out}'
    os.system(cmd)

if __name__=='__main__':
    play()
