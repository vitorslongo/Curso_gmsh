import gmsh

occ = gmsh.model.occ
mesh = gmsh.model.mesh

gmsh.initialize()
gmsh.option.setNumber("General.Terminal", 0)
occ.addRectangle(0, 0, 0, 1, 2)
occ.synchronize()

gmsh.option.setNumber("Mesh.Algorithm", 7)
mesh.generate(2)

# qualities = []
for element in mesh.get_elements(2, 1)[1]:
    min = min(mesh.getElementQualities(element, "minSJ"))
    max = max(mesh.getElementQualities(element, "minSJ"))

print("min jac", min)
print("max jac", max)

# print(qualities)
gmsh.fltk.run()
gmsh.finalize()


















