
DatToGmsh is a Python program that reads a two column *.csv file containing the coordinates of discrete points of a closed boundary in the X-Y plane and writes a 3D geometry file in the Gmsh format (*.geo) by extruding the aformentioned boundary in the Z direction.

This program automatically creates three physical boundary conditions i.e. top, bottom and sides, respectively for CFD applications.

Please note that you need to open the '*.geo' file, created by this program, in Gmsh and assign approperiate volume and also physical volume before writing the mesh file.

A test case, Boundary.dat, is available here. 


Copyright (c) 2018 Dr Arash Hamzehloo, Imperial College London.
a.hamzehloo@imperial.ac.uk

