"""Production Gauntlet: asymmetric multi-part electro-hydraulic regulator. Units mm."""
from build123d import Align, Axis, Box, Compound, Cylinder, Location, Sphere, Torus, fillet
from math import cos,sin,pi

def C(r,h,x=0,y=0,z=0,rot=(0,0,0)):
 return Location((x,y,z),rot)*Cylinder(r,h,align=(Align.CENTER,Align.CENTER,Align.CENTER))
def B(a,b,c,x=0,y=0,z=0,rot=(0,0,0)):
 return Location((x,y,z),rot)*Box(a,b,c,align=(Align.CENTER,Align.CENTER,Align.CENTER))
def gen_step():
 parts=[]
 # 1-5: chassis and reactor stack
 base=Box(112,92,8,align=(Align.CENTER,Align.CENTER,Align.MIN)); base=fillet(base.edges().filter_by(Axis.Z),5); parts.append(base)
 parts += [C(38,8,z=12), C(33,26,z=27), C(36,5,z=41), C(24,8,z=47)]
 # 6-9: four radial coupler bodies (intentionally asymmetric lengths)
 parts += [C(8,22,44,0,28,(0,90,0)), C(8,28,-43,0,26,(0,90,0)), C(8,20,0,40,31,(90,0,0)), C(8,14,0,-37,24,(90,0,0))]
 # 10-12: raised rear service tower
 parts += [B(22,16,36,-23,17,61), C(8,10,-23,17,84), C(5,14,-23,17,94)]
 # 13-15: glass pressure vessel + collars
 parts += [C(11,34,19,13,67), C(14,4,19,13,50), C(14,4,19,13,84)]
 # 16-18: mechanical arm, elbow pivot, tool head
 parts += [B(48,8,8,-3,-2,78,(0,-12,8)), C(7,12,-28,-6,75,(90,0,0)), B(18,14,10,22,3,83,(0,0,8))]
 # 19-20: fork fingers
 parts += [B(5,6,24,28,-3,70,(0,10,0)), B(5,6,24,28,9,70,(0,10,0))]
 # 21-24: exposed coil as discrete toroidal windings
 for i in range(4): parts.append(Location((-17,-19,53+i*5),(90,0,0))*Torus(8,1.4))
 # 25-27: diagonal pipe segments / valve block
 parts += [C(3.5,38,-3,22,57,(62,0,0)), C(3.5,28,33,-13,51,(0,58,0)), B(14,12,14,34,-14,38,(0,0,12))]
 # 28-30: gauge, spindle, emergency sphere
 parts += [C(10,4,-37,-20,52,(90,0,0)), C(3,20,-37,-20,62), Location((-37,-20,73))*Sphere(6)]
 model=Compound(children=parts)
 model.label='production_mechanism_gauntlet_30_part'
 return model
