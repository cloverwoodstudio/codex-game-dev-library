"""Parametric production-pilot sci-fi reactor module. Units: millimetres."""
from build123d import Align, Axis, Box, Cylinder, Location, fillet

BASE=88.0
BASE_H=8.0
BODY_R=29.0
BODY_H=34.0
CORE_R=16.0
CORE_H=48.0
PORT_R=6.0
PORT_LEN=18.0

def gen_step():
    base=Box(BASE,BASE,BASE_H,align=(Align.CENTER,Align.CENTER,Align.MIN))
    base=fillet(base.edges().filter_by(Axis.Z),radius=6.0)
    body=Location((0,0,BASE_H))*Cylinder(BODY_R,BODY_H,align=(Align.CENTER,Align.CENTER,Align.MIN))
    core=Location((0,0,BASE_H))*Cylinder(CORE_R,CORE_H,align=(Align.CENTER,Align.CENTER,Align.MIN))
    ring1=Location((0,0,BASE_H+8))*Cylinder(BODY_R+4,5,align=(Align.CENTER,Align.CENTER,Align.MIN))
    ring2=Location((0,0,BASE_H+BODY_H-5))*Cylinder(BODY_R+4,5,align=(Align.CENTER,Align.CENTER,Align.MIN))
    model=base+body+core+ring1+ring2
    # Four radial hard-surface power couplers.
    for x,y,rot in [(BODY_R+PORT_LEN/2,0,90),(-(BODY_R+PORT_LEN/2),0,90),(0,BODY_R+PORT_LEN/2,0),(0,-(BODY_R+PORT_LEN/2),0)]:
        port=Location((x,y,BASE_H+BODY_H/2),(0,rot,0))*Cylinder(PORT_R,PORT_LEN,align=(Align.CENTER,Align.CENTER,Align.CENTER))
        model=model+port
    model.label="production_reactor_pilot"
    return model
