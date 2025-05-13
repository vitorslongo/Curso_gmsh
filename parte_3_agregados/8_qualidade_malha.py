import gmsh
gmsh.initialize()
gmsh.option.setNumber("General.Terminal", 0)

occ = gmsh.model.occ
mesh = gmsh.model.mesh
# gmsh.open("C:\\Users\\vvslo\\Desktop\\fluido_silenciador.STEP")

# Vamos gerar uma geometria que com certeza vai gerar elementos distorcidos para visualizarmos os parametros e seus valores
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
# parameter = "gamma" # razao do raio da esfera inscrita e circunscrita --> se for muito grande é ruim
# parameter = "volume" # volume do elemento
# parameter = "minSJ" 
# parameter = "minSIGE"
parameter = "minSICN"

""""
É possível cruzar alguns tipos de parametros, como por exemplo, se o raio da esfera circunscrita for muito grande e o volume muito pequeno é um elemento degenerado.

Se o volume do elemento for negativo, o Jacobiano é negativo --> erro grave

minSJ --> determinante do jacobiano
o mais utilizado na indústria, varia entre -1 (invertido, péssimo) e 1 (ótimo)
Valor aceitável: > 0.2 geralmente.

minSIGE: Minimum Scaled Inverse Gradient Error
Mede o erro na interpolação do gradiente dentro do elemento.
Quanto menor, pior a capacidade de resolver gradientes físicos (temperatura, velocidade, etc).
Valor entre 0() e 1. 
Bom pra problemas de transferência de calor e CFD onde o gradiente importa muito.

minSICN: minimum scaled inverse condition number (determinante do jacobiano divido pela norma de Frobenius do jacobiano)
Parâmetro de controle de qualidade de malha mais completo, carrega 3 informações: 
determinante do jacobiano --> volume do elemento, evita elementos colapsados
sinal do determinante do jacobiano --> orientação do sistema de coordendas locais do elemento, evita inversoes
norma de Frobenius (nornalizada) --> soma do tamanho dos vetores que compoem o sist. de corrd. locais, deteca esticamento do elemento
"""




for element in mesh.get_elements(3, 1)[1]:
    min = min(mesh.getElementQualities(element, parameter))
    max = max(mesh.getElementQualities(element, parameter))

print(parameter, "min:", min)
print(parameter,"max:", max)

# print(qualities)
gmsh.fltk.run()
gmsh.finalize()


















