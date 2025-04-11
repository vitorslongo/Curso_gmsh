import gmsh
gmsh.initialize()
occ = gmsh.model.occ
mesh = gmsh.model.mesh



gmsh.option.setNumber("General.Verbosity", 0)

occ.addBox(0, 0, 0, 1, 1, 1)
occ.synchronize()
gmsh.option.setNumber("Mesh.MeshSizeFactor", 10)
mesh.generate(3)

node_tags, coords, _ = mesh.getNodes(2, -1, True)

element_types, element_tags, element_nodes = mesh.getElements(2, -1, )



# print("node_tags:", node_tags)

print("element_types", element_types)
# print("coords", coords)





# gmsh.fltk.run()
gmsh.finalize()