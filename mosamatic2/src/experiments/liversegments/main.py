import slicer

# Define segment names and their corresponding file paths
segment_names = ["S1", "S2", "S3", "S4", "S5", "S6", "S7", "S8"]
file_paths = [
    "D:\\Mosamatic\\TotalSegmentatorOutput\\liver_segment_1.nii.gz",
    "D:\\Mosamatic\\TotalSegmentatorOutput\\liver_segment_2.nii.gz",
    "D:\\Mosamatic\\TotalSegmentatorOutput\\liver_segment_3.nii.gz",
    "D:\\Mosamatic\\TotalSegmentatorOutput\\liver_segment_4.nii.gz",
    "D:\\Mosamatic\\TotalSegmentatorOutput\\liver_segment_5.nii.gz",
    "D:\\Mosamatic\\TotalSegmentatorOutput\\liver_segment_6.nii.gz",
    "D:\\Mosamatic\\TotalSegmentatorOutput\\liver_segment_7.nii.gz",
    "D:\\Mosamatic\\TotalSegmentatorOutput\\liver_segment_8.nii.gz"
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
}

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
