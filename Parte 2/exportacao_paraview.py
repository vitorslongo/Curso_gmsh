import gmsh

gmsh.initialize()
gmsh.model.add("Placa_Estruturada")

Lx = 1
Ly = 1
Lz = 0.1

box = gmsh.model.occ.addBox(0, 0, 0, Lx, Ly, Lz)
gmsh.model.occ.synchronize()

face_tags = [s[1] for s in gmsh.model.getEntities(2)]

for face in face_tags:
    gmsh.model.mesh.setTransfiniteSurface(face)
gmsh.model.mesh.setTransfiniteVolume(1)

gmsh.option.setNumber("Mesh.CharacteristicLengthFactor", 0.1)
gmsh.option.setNumber("Mesh.RecombineAll", 1)
gmsh.model.mesh.generate(3)
# gmsh.fltk.run()



gmsh.write("placa_estruturada.vtk")