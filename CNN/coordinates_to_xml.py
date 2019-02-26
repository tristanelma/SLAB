import xml.etree.ElementTree as ET

# Returns the root element of our XML tree.
# width, height, and depth are for entire image
# name, xmin, xmax, ymin, and ymax are for the bounding box
def makeXML(width, height, depth, name, xmin, xmax, ymin, ymax):
    annotation = ET.Element('annotation')

    folder = ET.SubElement(annotation, 'folder')
    folder.text = "SLAB"
    filename = ET.SubElement(annotation, 'filename')
    filename.text = "000001.jpg"

    source = ET.SubElement(annotation, 'source')
    database = ET.SubElement(source, 'database')
    database.text = "The SLAB Synthetic Image Database"
    source_annotation = ET.SubElement(source, 'annotation')
    source_annotation.text = "SLAB Synthetic Image"
    image = ET.SubElement(source, 'image')
    image.text = "NONE"
    source_flickrid = ET.SubElement(source, 'flickrid')
    source_flickrid.text = "NONE"

    owner = ET.SubElement(annotation, 'owner')
    owner_flickrid = ET.SubElement(owner, 'flickrid')
    owner_flickrid.text = "NONE"
    owner_name = ET.SubElement(owner, 'name')
    owner_name.text = "NONE"

    size = ET.SubElement(annotation, 'size')
    image_width = ET.SubElement(size, 'width')
    image_width.text = str(width)
    image_height = ET.SubElement(size, 'height')
    image_height.text = str(height)
    image_depth = ET.SubElement(size, 'depth')
    image_depth.text = str(depth)

    segmented = ET.SubElement(annotation, "segmented")
    segmented.text = "0"

    object = ET.SubElement(annotation, "object")
    object_name = ET.SubElement(object, "name")
    object_name.text = name
    object_pose = ET.SubElement(object, "pose")
    object_pose.text = "left"
    object_truncated = ET.SubElement(object, "truncated")
    object_truncated.text = "1"
    object_difficult = ET.SubElement(object, "difficult")
    object_difficult.text = "0"
    bndbox = ET.SubElement(object, "bndbox")
    bndbox_xmin = ET.SubElement(bndbox, "xmin")
    bndbox_xmin.text = str(xmin)
    bndbox_ymin = ET.SubElement(bndbox, "ymin")
    bndbox_ymin.text = str(ymin)
    bndbox_xmax = ET.SubElement(bndbox, "xmax")
    bndbox_xmax.text = str(xmax)
    bndbox_ymax = ET.SubElement(bndbox, "ymax")
    bndbox_ymax.text = str(ymax)

    return annotation

def write_xml(filename, word, x_min, x_max, y_min, y_max, width, height, depth=3):
    # Open output file in write mode
    output_file = open(filename, "w")
    # Build a new element tree, passing our root element into the constructor
    element_tree = ET.ElementTree(makeXML(width, height, depth, word, x_min, x_max, y_min, y_max))
    # Write the element tree to the output file
    element_tree.write(filename)
