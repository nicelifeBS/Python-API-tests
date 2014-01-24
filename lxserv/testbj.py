#python
import lx, lxifc

class uvVisitor(lxifc.Visitor):
    def __init__(self, polyAccessor, mapID):
        self.polyAccessor = polyAccessor
        self.mapID = mapID
        self.storage = lx.object.storage('f', 2)
        self.values = []
        
    def vis_Evaluate(self):
        nVerts = self.polyAccessor.VertexCount()
        for eachVert in xrange(nVerts):
            vertID = self.polyAccessor.VertexByIndex(eachVert)
            if self.polyAccessor.MapEvaluate(self.mapID, vertID, self.storage):
                currentValue = self.storage.get()
                if currentValue not in self.values:
                    self.values.append(currentValue)
        
def execute():
    ## Localize the mesh ##
    layerService = lx.service.Layer()
    layerScanObject = layerService.ScanAllocate(lx.symbol.f_LAYERSCAN_PRIMARY)
    localizedMesh = layerScanObject.MeshBase(0)

    ## Accessing the map values ##
    polyAccessor = localizedMesh.PolygonAccessor()
    mapAccessor = localizedMesh.MeshMapAccessor()

    ## Get the map ID ##
    mapAccessor.SelectByName(lx.symbol.i_VMAP_TEXTUREUV, "Texture")
    mapID = mapAccessor.ID()
    
    ## Visitor instance ##
    visitorInstance = uvVisitor(polyAccessor, mapID)
    polyAccessor.Enumerate(lx.symbol.iMARK_ANY, visitorInstance, 0)
    layerScanObject.Apply()
    for i in visitorInstance.values:
        lx.out(i)
