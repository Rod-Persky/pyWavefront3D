#!python3.3
# -*- coding: utf-8 -*-
"""
.. module:: formats.OBJ
   :platform: Agnostic
   :synopsis: Wavefront 3d legacy file format for use with snappyHexMesh

.. Created on Sun Aug  4 20:17:00 2013
.. codeauthor::  Rod Persky <rodney.persky@gmail.com>
.. Licensed under the Academic Free License ("AFL") v. 3.0
.. Source at https://bitbucket.org/Rod-Persky/3d-turbomachinery-design-tool
"""


class OBJStorage():
    def __init__(self):
        self.last_index = 1
        self.OBJList = []
        
    def commit(self, OBJAny):
        OBJAny.pointer = self.last_index
        self.OBJList.append(OBJAny)
        self.last_index = self.last_index + 1
        
    def save(self):
        out = ""
        for item in self.OBJList:
            out = "{}{}\n".format(out, item.export())
            
        return out
    

class obj_item():
    def __init__(self):
        self.data = []
        self.type = 0
        self.pointer = 0
        
    def export(self):
        self.get_pointers()
        text = str(self.type)
        for item in self.data:
            text = "{} {}".format(text, item)           
        return text
    
    def get_pointers(self):
        pass


class OBJVertex(obj_item):
    """Basic vertex / point
    Rational curves and surfaces require a weight
    """
    def __init__(self, x=0, y=0, z=0):
        obj_item.__init__(self)
        self.type = "v"
        self.data = [x, y, z]


class OBJFace(obj_item):
    def __init__(self, *OBJPoints):
        obj_item.__init__(self)
        self.type = "f"
        self.points = []
        
        for point in OBJPoints:
            self.points.append(point)
            
    def get_pointers(self):
        self.data = []
        for point in self.points:
            if type(point) == OBJPointCloud:
                for cloudpoint in point.points:
                    self.data.append(cloudpoint.pointer)
                    
            elif type(point) == OBJVertex:
                self.data.append(point.pointer)


class OBJPointCloud():
    def __init__(self, system):
        obj_item.__init__(self)
        self.system = system
        self.points = []
    
    def AddPoint(self, *OBJPoints):
        for OBJItem in OBJPoints:
            if type(OBJItem) == OBJVertex:
                self._AddPoint(OBJItem)
            elif type(OBJItem) == list:
                for item in OBJItem:
                    self._AddPoint(item)
                    
    def _AddPoint(self, OBJPoints):
        self.points.append(OBJPoints)
        if OBJPoints.pointer == 0:
            self.system.commit(self.points[len(self.points) - 1])
            
            #print(id(self.points[len(self.points) - 1]))
            #print(id(self.system.data[len(self.points) - 1]))

    def Move(self, transform_matrix):
        for idx, point in enumerate(self.points):
            for axis, value in enumerate(point.data):
                self.points[idx].data[axis] = value + transform_matrix[axis]
                
    def copy_from(self, cloud_origin, reverse_index=False):
        origin_len = len(cloud_origin.points)
        new_vertex = []
        for i in range(0, origin_len):
            
            if reverse_index:
                point = cloud_origin.points[(origin_len - 1) - i]
            else:
                point = cloud_origin.points[i]
                
            new_vertex.append(OBJVertex(point.data[0], point.data[1], point.data[2]))
            
        self.AddPoint(new_vertex)
        
    def extrude_surface(self, normal_vector):
        pass
        
    def get_pointers(self):
        for point in self.points:
            self.data.append(point.pointer)
    
    def export(self):
        return "#don't commit point clouds"


def draft(PointCloud1, PointCloud2):
    num_points = len(PointCloud1.points)
    num_faces  = num_points
    draft_faces = []
    
    for i in range(0, num_faces):
        try:
            draft_faces.append(OBJFace(PointCloud1.points[i], PointCloud1.points[i+1],
                                       PointCloud2.points[i+1], PointCloud2.points[i]))
        except IndexError:
            return draft_faces
    return draft_faces
            
  

def make_project_file(OBJ_filename):
    return """<!DOCTYPE MeshLabDocument>
    <MeshLabProject>
    <MeshGroup>
    <MLMesh label="{}" filename="test_obj_3d.obj">
    </MLMesh>
    </MeshGroup>
    <RasterGroup/>
    </MeshLabProject>""".format(OBJ_filename)


def update_egg():
    import os
    thisdir = os.path.dirname(__file__)
    os.chdir("../")
    os.system("py setup.py clean")
    os.system("py setup.py build")
    os.system("py setup.py install")
    os.chdir(thisdir)
    print("-------------------\n\n")

if __name__ == "__main__":
    import os
    import numpy
    update_egg()
    
    system = OBJStorage()
    PointCloud = OBJPointCloud(system)
    PointCloud2 = OBJPointCloud(system)
    
    keypoints = [[], []]
    
    for i in range(0, int(300 * numpy.pi * 2 + 1)):
        keypoints[0].append(numpy.sin(numpy.divide(i, 300)) * 30)
        keypoints[1].append(numpy.cos(numpy.divide(i, 300)) * 30)
    
    for index in range(0, len(keypoints[0])):
        PointCloud.AddPoint(OBJVertex(keypoints[0][index], keypoints[1][index]))
           
    PointCloud2.copy_from(PointCloud, False)
    PointCloud2.Move([0, 0, 10])
    
    bottom_face = OBJFace(PointCloud)
    top_face = OBJFace(PointCloud2)
    side_face = draft(PointCloud, PointCloud2)
    close_side = OBJFace(PointCloud.points[len(PointCloud.points) - 1],
                         PointCloud.points[0],
                         PointCloud2.points[0],
                         PointCloud2.points[len(PointCloud2.points) - 1])
    
    system.commit(top_face)
    system.commit(bottom_face)
    for item in side_face: system.commit(item) #@IgnorePep8
    system.commit(close_side)
      
    testfile = open("test_obj_3d.obj", "w")
    testfile.write(system.save())
    testfile.close()
    
    meshlab_project_file = open("meshlab_project_file.mlp", "w")
    meshlab_project_file.write(make_project_file("test_obj_3d.obj"))
    meshlab_project_file.close()
    
    os.startfile("meshlab_project_file.mlp")
