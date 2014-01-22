#python

# Python modo API testing

import lx

## Localize the mesh ##
layerservice = lx.service.Layer() # Establish the layerservice
layerScanObject = layerservice.ScanAllocate(lx.symbol.f_LAYERSCAN_PRIMARY) # Select the active layer in the scene
localizedMesh = layerScanObject.MeshBase(0) # Get the mesh. Argument 0 to only return the first mesh if more are returned

## Accessing the map values ##
storageBuffer = lx.object.storage('f',2) # Storage for the U and V values. 'f' for float 2  because two values (u and v).
polyAccessor = localizedMesh.PolygonAccessor()
mapAccessor = localizedMesh.MeshMapAccessor()

## Get the map ID ##
mapAccessor.SelectByName(lx.symbol.i_VMAP_TEXTUREUV, "Texture")
mapID = mapAccessor.ID()

## Get the number of polys in the mesh and loop through them ##
## Select each poly and read its vertex UV values into a list of tuples ##
uvValues = [] # Storage list for the UV values
nPolys = localizedMesh.PolygonCount()
for eachPoly in xrange(nPolys):
    polyAccessor.SelectByIndex(eachPoly) # Select the polygon
    nVerts = polyAccessor.VertexCount() # get the number of verts of the polygon
    for eachVert in xrange(nVerts):
        vertID = polyAccessor.VertexByIndex(eachVert) # Get the vertex ID
        if polyAccessor.MapEvaluate(mapID, vertID, storageBuffer) == True: # only if there are uv values for a vertex these are stored in the storagebuffer object
            values = storageBuffer.get() # get() method to return the content of a storage object.
            uvValues.append(values)

# Let modo know that we are done editing!
layerScanObject.Apply()
lx.out(uvValues)