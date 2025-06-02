import data_load as dl
import kmeans
import hierarchical
import spectral
import coolplots

points, classes = dl.Get2DPointData(2)

pointsTransformed = spectral.SpectralTransformation(points, 2, True)

kmeans.KmeansClassifyPoints(points, pointsTransformed, k=6, isVisualized=True, isPlusPlus=True, dataID=1)
hierarchical.HierarchicalClassifyPoints(points, pointsTransformed, isVisualized=True, dataID=1)

kmeans.KmeansClassifyPoints(points, points, k=6, isVisualized=True, isPlusPlus=True, dataID=2)
hierarchical.HierarchicalClassifyPoints(points, points, isVisualized=True, dataID=2)