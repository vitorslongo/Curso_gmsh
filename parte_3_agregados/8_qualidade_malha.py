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
parameter = "gamma" # raio da esfera circunscrita --> se for muito grande é ruim
parameter = "volume" # volume do elemento
parameter = "minSJ" # jacobiano mínimo escalado
parameter = "minSICN"
parameter = "minSIGE"

# É possível cruzar alguns tipos de parametros, como por exemplo, se o raio da esfera circunscrita for muito grande e o volume muito pequeno é um elemento degenerado.

# Se o volume do elemento for negativo, o Jacobiano é negativo --> erro grave

# minSJ --> Jacobiano da transformação do elemento de referência para o real, escalado pela norma dos vetores das arestas.
#  o mais utilizado na indústria, varia entre -1 (invertido, péssimo) e 1 (ótimo)
# Valor aceitável: > 0.2 geralmente.

# minSIGE: Minimum Scaled Inverse Gradient Error
# Mede o erro na interpolação do gradiente dentro do elemento.
# Quanto menor, pior a capacidade de resolver gradientes físicos (temperatura, velocidade, etc).
# Valor entre 0 e 1.
# Bom pra problemas de transferência de calor e CFD onde o gradiente importa muito.

# minSICNE





for element in mesh.get_elements(3, 1)[1]:
    min = min(mesh.getElementQualities(element, parameter))
    max = max(mesh.getElementQualities(element, parameter))

print(parameter, "min:", min)
print(parameter,"max:", max)

# print(qualities)
gmsh.fltk.run()
gmsh.finalize()


















