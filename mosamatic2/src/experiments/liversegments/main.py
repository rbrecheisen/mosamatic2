import slicer

#################################################################################################################
# Load this script in 3D Slicer as follows:
# - Open Python console: View > Python Console
# - Copy paste following line and run it: 
#
#   exec(open("D:\\SoftwareDevelopment\\GitHub\\mosamatic2\\mosamatic2\\src\\experiments\\liversegments\\main.py").read())
#
#################################################################################################################

# Define segment names and their corresponding file paths
segment_names = ["S1", "S2", "S3", "S4", "S5", "S6", "S7", "S8", "VESSELS"]
file_paths = [
    "D:\\Mosamatic\\TestData\\totalsegmentatortask\\liver_segment_1.nii.gz",
    "D:\\Mosamatic\\TestData\\totalsegmentatortask\\liver_segment_2.nii.gz",
    "D:\\Mosamatic\\TestData\\totalsegmentatortask\\liver_segment_3.nii.gz",
    "D:\\Mosamatic\\TestData\\totalsegmentatortask\\liver_segment_4.nii.gz",
    "D:\\Mosamatic\\TestData\\totalsegmentatortask\\liver_segment_5.nii.gz",
    "D:\\Mosamatic\\TestData\\totalsegmentatortask\\liver_segment_6.nii.gz",
    "D:\\Mosamatic\\TestData\\totalsegmentatortask\\liver_segment_7.nii.gz",
    "D:\\Mosamatic\\TestData\\totalsegmentatortask\\liver_segment_8.nii.gz",
    "D:\\Mosamatic\\TestData\\totalsegmentatortask\\liver_vessels.nii.gz",
]

# Define colors as RGB triples (values between 0 and 1)
colors = {
    "S1": (1.0, 0.0, 0.0),     # Red
    "S2": (0.0, 1.0, 0.0),     # Green
    "S3": (0.0, 0.0, 1.0),     # Blue
    "S4": (1.0, 1.0, 0.0),     # Yellow
    "S5": (1.0, 0.0, 1.0),     # Magenta
    "S6": (0.0, 1.0, 1.0),     # Cyan
    "S7": (0.6, 0.4, 0.2),     # Brown
    "S8": (0.5, 0.5, 0.5),     # Gray
    "VESSELS": (0.0, 0.0, 0.0) # Vessels
}

slicer.mrmlScene.Clear()

ctVolume = slicer.util.loadVolume("G:\\My Drive\\data\\Mosamatic\\testdata\\output\\boadockerpipeline\\dicom2niftitask\\patient1.nii.gz")
# vrLogic = slicer.modules.volumerendering.logic()
# vrNode = vrLogic.CreateDefaultVolumeRenderingNodes(ctVolume)

# # Adjust rendering preset (e.g. CT-AAA, CT-Bone, etc.)
# displayNode = vrNode.GetDisplayNode()
# displayNode.SetVisibility(True)  # Show volume rendering
# vrLogic.CopyDisplayToVolumeRenderingDisplayNode(vrLogic.GetPresetByName("CT-AAA"), displayNode)

layoutManager = slicer.app.layoutManager()
layoutManager.setLayout(slicer.vtkMRMLLayoutNode.SlicerLayoutFourUpView)  # show 2D + 3D

for comp in ["Red", "Yellow", "Green"]:
    sliceWidget = layoutManager.sliceWidget(comp)
    sliceWidget.sliceController().setSliceVisible(True)

# Create a new segmentation node
segmentationNode = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLSegmentationNode", "LiverSegments")

# Import each segment mask and assign it a name and color
for name, path in zip(segment_names, file_paths):
    labelmapNode = slicer.util.loadLabelVolume(path)
    slicer.modules.segmentations.logic().ImportLabelmapToSegmentationNode(labelmapNode, segmentationNode)
    segment = segmentationNode.GetSegmentation().GetNthSegment(segmentationNode.GetSegmentation().GetNumberOfSegments() - 1)
    segment.SetName(name)
    if name in colors:
        segment.SetColor(*colors[name])
    slicer.mrmlScene.RemoveNode(labelmapNode)  # optional cleanup

# Create 3D surface for all segments
segmentationNode.CreateDefaultDisplayNodes()
segmentationNode.GetSegmentation().CreateRepresentation('Closed surface')
segmentationNode.GetDisplayNode().SetVisibility3D(True)
segmentationNode.GetDisplayNode().SetOpacity3D(0.2)
