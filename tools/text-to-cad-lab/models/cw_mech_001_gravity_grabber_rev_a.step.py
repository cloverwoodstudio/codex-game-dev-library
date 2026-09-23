"""CW-MECH-001 Gravity Grabber REV A. Approved datasheet geometry. Units mm."""
from build123d import Align, Box, Compound, Cylinder, Location, Sphere, Torus, fillet
def C(r,h,x=0,y=0,z=0,rot=(0,0,0)): return Location((x,y,z),rot)*Cylinder(r,h,align=(Align.CENTER,Align.CENTER,Align.CENTER))
def B(a,b,c,x=0,y=0,z=0,rot=(0,0,0)): return Location((x,y,z),rot)*Box(a,b,c,align=(Align.CENTER,Align.CENTER,Align.CENTER))
def gen_step():
 p=[]
 base=Box(112,112,8,align=(Align.CENTER,Align.CENTER,Align.MIN)); p.append(fillet(base.edges().filter_by_position(0,8),2) if False else base)
 # layered circular chassis + four radial couplers
 p += [C(50,7,z=11.5),C(47,20,z=25),C(51,5,z=37.5)]
 p += [C(10,24,55,0,25,(0,90,0)),C(10,24,-55,0,25,(0,90,0)),C(10,24,0,55,25,(90,0,0)),C(10,24,0,-55,25,(90,0,0))]
 # glass energy chamber, inner emitter, collars
 p += [C(17,44,-27,8,63),C(5,27,-27,8,63),Location((-27,8,63))*Sphere(7),C(21,5,-27,8,40),C(21,5,-27,8,86)]
 # exposed coil: six real windings around rear tower
 p += [C(7,42,7,22,62)]
 for i in range(6): p.append(Location((7,22,45+i*7))*Torus(12,1.8))
 # rotating shoulder tower + arm links
 p += [C(15,10,18,-8,48),C(12,8,18,-8,59),C(7,16,18,-8,61,(90,0,0)), B(49,5,12,39,-13,72,(0,-12,0)),B(49,5,12,39,-3,72,(0,-12,0)), B(37,4,7,39,-8,73,(0,-12,0)), C(10,16,62,-8,82,(90,0,0)),C(6,20,62,-8,82,(90,0,0)), B(39,5,11,77,-13,68,(0,28,0)),B(39,5,11,77,-3,68,(0,28,0))]
 # wrist + gripper head + two fingers
 p += [C(11,16,92,-8,57,(90,0,0)),C(6,19,92,-8,57,(90,0,0)),B(20,18,14,92,-8,46), B(7,6,24,98,-18,31,(0,-18,0)),B(7,6,24,98,2,31,(0,-18,0)), B(9,7,9,101,-18,18,(0,18,0)),B(9,7,9,101,2,18,(0,18,0))]
 # hard pipes, valve body, gauge and fastener caps
 p += [C(4,35,-5,-22,55,(62,0,0)),C(4,30,29,25,49,(0,58,0)),B(15,13,15,32,27,38,(0,0,10)),C(11,5,-38,-22,50,(90,0,0))]
 p += [C(4,8,-35,-35,39),C(4,8,35,-35,39),C(4,8,-35,35,39),C(4,8,35,35,39)]
 p += [B(22,4,12,-12,-49,26),B(16,4,9,15,-49,26), C(3,8,-45,-25,39),C(3,8,45,25,39), B(5,5,43,-44,8,63),B(5,5,43,-10,8,63)]
 # conformance detail: stepped chassis, coupler collars, chamber braces/caps
 p += [C(53,2,z=7),C(48,2,z=41), C(13,4,48,0,25,(0,90,0)),C(13,4,-48,0,25,(0,90,0)),C(13,4,0,48,25,(90,0,0)),C(13,4,0,-48,25,(90,0,0))]
 p += [B(5,7,45,-44,8,63),B(5,7,45,-10,8,63),B(38,6,5,-27,8,89),B(38,6,5,-27,8,37)]
 # coil mounting yoke and terminals
 p += [B(31,5,5,7,22,42),B(31,5,5,7,22,86),C(4,8,-7,22,42),C(4,8,21,22,86)]
 # pipe collars / valve hardware
 p += [C(6,6,-5,-22,42,(62,0,0)),C(6,6,-5,-22,69,(62,0,0)),C(6,6,20,25,42,(0,58,0)),C(6,6,39,25,57,(0,58,0)),C(6,8,32,27,48)]
 # conformance R3: layered pivots, arm armor, jaw mechanics, service fasteners
 p += [C(14,3,18,-17,61,(90,0,0)),C(14,3,18,1,61,(90,0,0)),C(5,22,18,-8,61,(90,0,0))]
 p += [B(42,3,5,39,-16,76,(0,-12,0)),B(42,3,5,39,0,76,(0,-12,0))]
 p += [C(12,3,62,-17,82,(90,0,0)),C(12,3,62,1,82,(90,0,0)),C(5,22,62,-8,82,(90,0,0))]
 p += [B(31,3,5,77,-16,72,(0,28,0)),B(31,3,5,77,0,72,(0,28,0))]
 p += [C(13,3,92,-18,57,(90,0,0)),C(13,3,92,2,57,(90,0,0))]
 # gripper knuckles and inner gripping pads
 p += [C(5,9,96,-18,44,(90,0,0)),C(5,9,96,2,44,(90,0,0)),B(5,8,12,99,-18,20,(0,12,0)),B(5,8,12,99,2,20,(0,12,0))]
 # asymmetric chassis panel bolts
 for x,y in [(-24,-49),(0,-49),(24,-49),(-48,-24),(-48,24),(48,-24),(48,24)]:
  p.append(C(2.2,3,x,y,40))
 model=Compound(children=p); model.label='CW-MECH-001_GRAVITY_GRABBER_REV_A'; return model
