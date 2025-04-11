
import gmsh
import numpy as np

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

class SectionMesh:

    def __init__(self):

        self.element_size = 10
        self.tolerance = 1e-6


    def _process_mesh(self):
        self._initialize_gmsh()
        self._create_geometry()
        self._set_gmsh_options()
        self._process_section_mesh()
        self._finalize_gmsh()


    def _create_geometry():
        gmsh.initialize()
        h = 120
        w = 60
        t = 6

        # points coordiantes
        points_coords = np.array([  [0, -h/2, 0],
                                    [w, -h/2, 0],
                                    [w, -h/2 + t, 0],
                                    [t, -h/2 + t, 0],
                                    [t, h/2 - t, 0],
                                    [w, h/2 - t, 0],
                                    [w, h/2, 0],
                                    [0, h/2, 0],
                                    [0, -h/2, 0]  ])

        # create points
        points = list()
        for i, coords in enumerate(points_coords):
            points.append(gmsh.model.occ.addPoint(*coords, meshSize=0))

        # create lines
        lines = list()
        for i, point in enumerate(points):
            if i <= len(points) - 2:
                lines.append(gmsh.model.occ.addLine(point, points[i+1]))

        loop = gmsh.model.occ.addCurveLoop(lines)
        gmsh.model.occ.addSurfaceFilling(loop)

        gmsh.model.occ.synchronize()
        gmsh.option.setNumber('General.FltkColorScheme', 1)
        gmsh.fltk.run()

    _create_geometry()

    def _initialize_gmsh(self):

        if gmsh.is_initialized():
            gmsh.finalize()

        gmsh.initialize("", False)
        gmsh.option.setNumber("General.Terminal", 0)
        gmsh.option.setNumber("General.Verbosity", 0)
        gmsh.option.setNumber('Geometry.Tolerance', self.tolerance)


    def _set_gmsh_options(self):
        """
        This method sets the mesher algorithm configuration.

        Parameters
        ----------

        """

        try:
            gmsh.option.setNumber("General.NumThreads", 4)
        except:
            pass

        gmsh.option.setNumber('Mesh.CharacteristicLengthMin', 0.5*self.element_size)
        gmsh.option.setNumber('Mesh.CharacteristicLengthMax', self.element_size)
        gmsh.option.setNumber("Mesh.MeshSizeFactor", 2)
        gmsh.option.setNumber('Mesh.CharacteristicLengthExtendFromBoundary', 1)
        gmsh.option.setNumber('Mesh.MeshSizeFromPoints', 1)
        gmsh.option.setNumber('Mesh.Optimize', 1)
        gmsh.option.setNumber('Mesh.OptimizeNetgen', 0)
        gmsh.option.setNumber('Mesh.HighOrderOptimize', 0)
        gmsh.option.setNumber('Mesh.ElementOrder', 2)
        gmsh.option.setNumber('Mesh.Algorithm', DELAUNAY_2D)
        gmsh.option.setNumber('Mesh.Algorithm3D', FRONTAL_3D)
        gmsh.option.setNumber('Mesh.RecombineAll', 1)
        gmsh.option.setNumber("Mesh.RecombinationAlgorithm", BLOSSOM_FULL_QUAD_RECOMBINATION)
        gmsh.option.setNumber("Mesh.SubdivisionAlgorithm", NO_SUBDIVISION)


    def _process_section_mesh(self):
        """
        This method generate the section mesh and processes the nodal 
        coordinates and the connectivity.
        """

        try:

            gmsh.model.mesh.generate(3)
            gmsh.model.mesh.removeDuplicateNodes()

            # process the nodal coordinates
            node_indexes, coords, _ = gmsh.model.mesh.getNodes(2, -1, True)
            self.process_section_nodal_coordinates(node_indexes, coords)

            # process the connectivity
            element_types, element_indexes, element_nodes = gmsh.model.mesh.getElements(2, -1)

            if len(element_indexes) > 1:
                print("multiple element type detected")

            for i in range(len(element_nodes)):
                element_name, _, _, nodes_per_element, _, _ = gmsh.model.mesh.getElementProperties(element_types[i])
                self.process_section_connectivity(element_indexes[i], element_nodes[i], element_name, nodes_per_element)

            gmsh.option.setNumber('General.FltkColorScheme', 1)
            gmsh.fltk.run()

        except Exception as log_error:
            from traceback import print_exception
            print_exception(log_error)


    def process_section_nodal_coordinates(self, node_indexes: np.ndarray, coords: np.ndarray):
        """ 
            This method processes the nodal coordinates from section mesh.
        """
        n_nodes = len(node_indexes)
        n_indexes = np.arange(n_nodes, dtype=int)
        self.section_nodal_coordinates = np.zeros((n_nodes, 4))
        self.section_nodal_coordinates[n_indexes, 1:] = coords.reshape(-1, 3) / 1e3
        self.section_nodal_coordinates[n_indexes, :1] = node_indexes.reshape(-1, 1) - 1


    def process_section_connectivity(self, element_indexes: np.ndarray, element_nodes: np.ndarray, element_name: str, nodes_per_element: int):
        """ 
            This method processes the connectivity from section mesh.
        """
        n_elements = len(element_indexes)
        e_indexes = np.arange(n_elements, dtype=int)
        cols = nodes_per_element

        section_connectivity = np.zeros((n_elements, cols+1))
        section_connectivity[:, 0] = e_indexes
        section_connectivity[:, 1:] = element_nodes.reshape(-1, cols) - 1

        self.section_connectivities = dict()
        self.section_connectivities[element_name] = section_connectivity


    def _finalize_gmsh(self):
        """
        This method finalize the mesher gmsh algorithm.
        """
        gmsh.finalize()


if __name__ == "__main__":
    
    mesh = SectionMesh()
    mesh._process_mesh()