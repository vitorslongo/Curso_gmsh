import gmsh
gmsh.initialize()
occ = gmsh.model.occ
mesh = gmsh.model.mesh
option = gmsh.option.setNumber

option("General.Verbosity", 0)

main = occ.addRectangle(0, 0, 0, 1, 2)

rec1 = occ.addRectangle(0, .75, 0, .54, .5)
rec2 = occ.addRectangle(.55, .75, 0, .45, .5)

result = occ.cut([(2, main)], [(2, rec1), (2, rec2)])
occ.extrude([(2, 1)], 0, 0, 1)
occ.synchronize()


# option("Mesh.Algorithm", 7)
gmsh.option.setNumber("Mesh.CharacteristicLengthFactor", 0.5)
mesh.generate(3)

# parameter = "gamma" # razao do raio da esfera inscrita e circunscrita --> se for muito grande é ruim
# parameter = "volume" # volume do elemento
# parameter = "minSJ"
# parameter = "minSIGE"
parameter = "minSICN"

for element in mesh.getElements(3, 1)[1]:
    min = min(mesh.getElementQualities(element, parameter))
    max = max(mesh.getElementQualities(element, parameter))

print(parameter, "min:", min)
print(parameter, "max:", max)


gmsh.fltk.run()
gmsh.finalize()