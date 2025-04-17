import gmsh
gmsh.initialize()
gmsh.option.setNumber("General.Terminal", 0)

occ = gmsh.model.occ
mesh = gmsh.model.mesh
# gmsh.open("C:\\Users\\vvslo\\Desktop\\fluido_silenciador.STEP")
main = occ.addRectangle(0, 0, 0, 1, 2)

rec1 = occ.addRectangle(0, .75, 0, .54, .5)
rec2 = occ.addRectangle(.55, .75, 0, .45, .5)

result = occ.cut([(2, main)], [(2, rec1), (2, rec2)])
occ.extrude([(2, 1)], 0, 0, 1)
occ.synchronize()

gmsh.option.setNumber("Mesh.Algorithm", 7)
gmsh.option.setNumber("Mesh.CharacteristicLengthFactor", 0.5)
mesh.generate(3)

print(mesh.get_elements(3, 1))
# qualities = []
parameter = "gamma"
for element in mesh.get_elements(3, 1)[1]:
    min = min(mesh.getElementQualities(element, parameter))
    max = max(mesh.getElementQualities(element, parameter))

print(parameter, "min", min)
print(parameter,"max", max)

# print(qualities)
gmsh.fltk.run()
gmsh.finalize()


















