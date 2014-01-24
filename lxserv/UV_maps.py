#python

import lx, lxifc

class uvVisitor(lxifc.Visitor):
    """
    Visitor object to call up MapEvaluate()
    """
    def __init__(self, polyAccessor, mapID):
        self.polyAccessor = polyAccessor
        self.mapID = mapID
        
        # create storage object in the visitor class
        # to only store the variables that are needed
        # Storage for the U and V values. 'f' for float 2
        # because two values (u and v).
        self.storage = lx.object.storage('f', 2)
        
        # We also create an empty list to store the UV values
        self.values = [] # Storage list for the UV values
        
    def vis_Evaluate(self):
        # When the vis_Evaluate() method is running, it's as though each polygon
        # gets selected (in the API sense). That means we can skip the step of 
        # selecting a polygon by it's index (polyAccessor.SelectByIndex(0) in our early script)
        nVerts = self.polyAccessor.VertexCount() # get the number of verts of the polygon
        for eachVert in xrange(nVerts):
            vertID = self.polyAccessor.VertexByIndex(eachVert) # Get the vertex ID
            if self.polyAccessor.MapEvaluate(self.mapID, vertID, self.storage): # only if there are uv values for a vertex these are stored in the storagebuffer object
                currentValue = self.storage.get() # get() method to return the content of a storage object.
                if currentValue not in self.values:
                    self.values.append(currentValue)
        
def execute():
    ## Localize the mesh ##
    layerService = lx.service.Layer() # Establish the layerService
    layerScanObject = layerService.ScanAllocate(lx.symbol.f_LAYERSCAN_PRIMARY) # Select the active layer in the scene
    localizedMesh = layerScanObject.MeshBase(0) # Get the mesh. Argument 0 to only return the first mesh if more are returned

    ## Accessing the map values ##
    polyAccessor = localizedMesh.PolygonAccessor()
    mapAccessor = localizedMesh.MeshMapAccessor()

    ## Get the map ID ##
    mapAccessor.SelectByName(lx.symbol.i_VMAP_TEXTUREUV, "Texture")
    mapID = mapAccessor.ID()
    
    ## Visitor instance ##
    visitorInstance = uvVisitor(polyAccessor, mapID)
    ## Call Enumerate()
    polyAccessor.Enumerate(lx.symbol.iMARK_ANY, visitorInstance, 0)
    # Let modo know that we are done editing!
    layerScanObject.Apply()
    for i in visitorInstance.values:
        lx.out(i)
