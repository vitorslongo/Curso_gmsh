import gmsh
import sys

gmsh.initialize()

gmsh.model.add("quality_example")

# Geometria simples: quadrado 1x1
lc = 0.1
p1 = gmsh.model.geo.addPoint(0, 0, 0, lc)
p2 = gmsh.model.geo.addPoint(1, 0, 0, lc)
p3 = gmsh.model.geo.addPoint(1, 1, 0, lc)
p4 = gmsh.model.geo.addPoint(0, 1, 0, lc)

l1 = gmsh.model.geo.addLine(p1, p2)
l2 = gmsh.model.geo.addLine(p2, p3)
l3 = gmsh.model.geo.addLine(p3, p4)
l4 = gmsh.model.geo.addLine(p4, p1)

cl = gmsh.model.geo.addCurveLoop([l1, l2, l3, l4])
s = gmsh.model.geo.addPlaneSurface([cl])

gmsh.model.geo.synchronize()

# Malha
gmsh.model.mesh.generate(2)

# Define o tipo de qualidade que você quer avaliar
gmsh.model.mesh.getElementQualities()

# Pega os valores de qualidade para cada elemento
qualities = gmsh.model.mesh.getElementQualities()

print("Qualidade dos elementos (Aspect Ratio):")
for i, q in enumerate(qualities):
    print(f"Elemento {i}: {q:.3f}")

gmsh.fltk.run()  # Abre GUI para visualização, pode comentar se não quiser

gmsh.finalize()
