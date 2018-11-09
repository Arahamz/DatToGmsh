#####################################################################
#This Python program reads a two column *.csv file containing the 
#coordinates of discrete points of a closed boundary in the X-Y 
#plane and writes a 3D geometry file in the Gmsh format (*.geo) by 
#extruding the aformentioned boundary in the Z direction.
#
#This program automatically creates three physical boundary conditions
#i.e. top, bottom and sides, respectively for CFD applications.
#
#Please note that you need to open the '*.geo' file, created by this
#program, in Gmsh and assign approperiate volume and also physical 
#volume before writing the mesh file. 
#
#
#Copyright (c) 2018 Dr Arash Hamzehloo, Imperial College London.
#a.hamzehloo@imperial.ac.uk
#
#   


#This function calulates the number of lines in the geometry points file
def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1

#Beginning of the program

datfile = input ('Please enter name of the geometry points file (without the .dat and within single quotation marks):\n')

Height = input ('Please enter the height of your geometry [m]:\n')
H = str(Height)

Depth = input ('Please enter the depth of your geometry [m]:\n')
D = str(Depth)

#This is the characteristic lenght of mesh at the geometrical points,
#It can be adjusted later within the Gmsh environment.  
#For furhter information read: http://gmsh.info//doc/texinfo/gmsh.html
CharLength = input ('Please enter characteristic length of mesh at the geometrical points [m]:\n')
CL = str(CharLength)
        
print ('Creating new mesh....')
                
mesh = open(datfile + '.geo', 'w+')
geometry = open(datfile + '.dat', 'r')

N = file_len(datfile + '.dat')

LineCount = 0
spline2 = []
spline3 = []
surf = []
for line in geometry:
        LineCount +=1
        new = line.split(",")
        #Here we create the points of the top boundary
        mesh.write('Point('+(str(LineCount))+') = {'+(str(new[0]))+', '+(str(new[1]))+', '+H+', '+CL+'}')  
        mesh.write('; \n') 
        #Here we create the points of the bottom boundary by duplicating the top boundary points  
        mesh.write('Point('+(str(LineCount+N))+') = {'+(str(new[0]))+', '+(str(new[1]))+', '+D+', '+CL+'}')  
        mesh.write('; \n')      
        #Here we connect the top and bottom points with splines
        mesh.write('Spline(%s) = {%s, %s}; \n' % (str(LineCount),str(LineCount),str(LineCount+N).replace('\n','')))
        if LineCount > 1:
                #Here we connect the adjancet points of the top and bottom boundaries with splines
                mesh.write('Spline(%s) = {%s, %s}; \n' % (str(LineCount+N),str(LineCount),str(LineCount-1).replace('\n','')))
                spline2.append(LineCount+N)

                mesh.write('Spline(%s) = {%s, %s}; \n' % (str(LineCount+(2*N)),str(LineCount+N),str(LineCount+N-1).replace('\n','')))
                spline3.append(LineCount+(2*N))
                #Here we create closed spline loops and then surfaces of the side boundaries
                mesh.write('Line Loop(%s) = {%s, %s, %s, %s}; \n' % (str(LineCount+(3*N)), str(LineCount-1),str(-1*(LineCount+(2*N))) \
                ,str(-1*LineCount), str(LineCount+N).replace('\n','')))

                mesh.write('Plane Surface(%s) = {%s}; \n' % (str(LineCount+(4*N)),str(LineCount+(3*N)).replace('\n','')))
                surf.append(LineCount+(4*N))
#Here we close the top and bottom boundaries by connecting the first and the last points 
mesh.write('Spline(%s) = {%s, %s}; \n' % (str(LineCount+1),str(1),str(N).replace('\n','')));
spline2.append(N+1);

mesh.write('Spline(%s) = {%s, %s}; \n' % (str(LineCount+N+1),str(1+N),str(2*N).replace('\n','')));
spline3.append(((2*N)+1))
#Here we close the overall side surface by creating the last side surface for the spline mentioned in the previous step
mesh.write('Line Loop(%s) = {%s, %s, %s, %s}; \n' % (str(LineCount+(3*N)+1), str(N),str(-1*(LineCount+N+1)) \
,str(-1*1), str(N+1).replace('\n','')))

mesh.write('Plane Surface(%s) = {%s}; \n' % (str(LineCount+(4*N)+1),str(LineCount+(3*N)+1).replace('\n','')))
surf.append(LineCount+(4*N)+1)
                
#Here we create the top surface
spline2[:int((LineCount+N))] = reversed(spline2[:int(LineCount+N)])
splines ='Line Loop('+(str(5*N+1))+') ={'+(str(spline2))+'}'
splines = splines.replace('[','')
splines = splines.replace(']','')
mesh.write(splines)
mesh.write('; \n')

mesh.write('Plane Surface(%s) = {%s}; \n' % (str(LineCount+(4*N)+2),str(5*N+1).replace('\n','')))

#Here we create the bottom surface
spline3[:int((LineCount+(2*N)))] = reversed(spline3[:int(LineCount+(2*N))])
splines ='Line Loop('+(str(5*N+2))+') ={'+(str(spline3))+'}'
splines = splines.replace('[','')
splines = splines.replace(']','')
mesh.write(splines)
mesh.write('; \n')

mesh.write('Plane Surface(%s) = {%s}; \n' % (str(LineCount+(4*N)+3),str(5*N+2).replace('\n','')))
#Here we create the physical boundaries for CFD (top, bottom and side, respectively)       
mesh.write('Physical Surface(%s) = {%s}; \n' % (str(LineCount+(4*N)+4),str(LineCount+(4*N)+2).replace('\n','')))
mesh.write('Physical Surface(%s) = {%s}; \n' % (str(LineCount+(4*N)+5),str(LineCount+(4*N)+3).replace('\n','')))

surf[:int((LineCount+(4*N)))] = reversed(surf[:int(LineCount+(4*N))])
surfs ='Physical Surface('+(str(LineCount+(4*N)+6))+') ={'+(str(surf))+'}'
surfs = surfs.replace('[','')
surfs = surfs.replace(']','')
mesh.write(surfs)
mesh.write('; \n')
                            
geometry.close()  
mesh.close()
#End of the program
