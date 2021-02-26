from mathgl import *

d = mglData()
d.Create(6, 9)

gr = mglGraph(0, 600, 500)
gr.Rotate(60, 250)
gr.Light(True)
gr.SetTicks('x', 1, 0);
gr.Alpha(False)
gr.SetRanges(0, 6, 0, 4, -800, 800)
gr.Axis()

gr.WriteFrame("test.png")