import gmsh
gmsh.initialize()

occ = gmsh.model.occ
mesh = gmsh.model.mesh
option = gmsh.option.setNumber

option("General.Terminal", 0)

fields_list = []

origin = [0, 0, 0]
main_cylinder = occ.add_cylinder(*origin, 0, 0, 1, 1)
small_cylinder = occ.add_cylinder(.5, 0, 1, 0, 0, 1, .2)
small_box = occ.addBox(-.5, 0, 1, .2, .2, 1 )
occ.synchronize()


option("Mesh.MeshSizeFactor", 0.1)
# global_size = .07
# refinement_size = .01

# refinement_field = mesh.field.add("Constant")
# mesh.field.setNumbers(refinement_field, "SurfacesList", [5, 12])
# mesh.field.setNumber(refinement_field, "VIn", refinement_size)
# fields_list.append(refinement_field)

# global_field = mesh.field.add("Constant")
# mesh.field.setNumbers(global_field, "VolumesList", [])
# mesh.field.setNumber(global_field, "VOut", global_size)
# fields_list.append(global_field)

# minimum_field = mesh.field.add("Min")
# mesh.field.setNumbers(minimum_field, "FieldsList", fields_list)
# mesh.field.setAsBackgroundMesh(minimum_field)

# 2D Mesh Algorithms
MESH_ADAPT_2D = 1
AUTOMATIC_2D = 2
INITIAL_MESH_ONLY_2D = 3
DELAUNAY_2D = 5
FRONTAL_DELAUNAY_2D = 6
BAMG_2D = 7
FRONTAL_DELAUNAY_FOR_QUADS_2D = 8
PACKING_OF_PARALLELOGRAMS_2D = 9
QUASI_STRUCTURED_QUADS_2D = 11

# 3D Mesh Algorithms
DELAUNAY_3D = 1
INITIAL_MESH_ONLY_3D = 3
FRONTAL_3D = 4
MMG_3D = 7
RTREE_3D = 9
HXT_3D = 10

# Recombination Algorithms
SIMPLE_RECOMBINATION = 0
BLOSSOM_RECOMBINATION = 1
SIMPLE_FULL_QUAD_RECOMBINATION = 2
BLOSSOM_FULL_QUAD_RECOMBINATION = 3

# Subdivision Algorithms
NO_SUBDIVISION = 0
ALL_QUADRANGLES_SUBDIVISION = 1
ALL_HEXAHEDRA_SUBDIVISION = 2
BARYCENTRIC_SUBDIVISION = 3







gmsh.option.setNumber("Mesh.Algorithm3D", 10)
from time import time
t1 = time()
mesh.generate(3)
t2 = time()
print("Elapsed time to generate mesh:",t2 - t1, "s")


gmsh.fltk.run()
gmsh.finalize()