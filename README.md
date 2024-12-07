For preprocessing SVHN:

utils.py: To find information about the dataset(like largest image width/height)

padding.py: To scale and pad images to a square aspect ratio. Also to adjust bounding boxes to fit processed image. 

visualizebox.py : to test new bounding boxes It seems some of the bounding boxes might be longer than intended.


Bounding boxes are originally in Top Left Width Height format. The csv files are in this format. 

Yolo v8 needs square images of the same size for training.
