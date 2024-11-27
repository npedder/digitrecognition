import h5py
import numpy as np
import os
import digitStruct
## Note digitStruct.py source found at:
## https://github.com/prijip/Py-Gsvhn-DigitStruct-Reader/blob/master/digitStruct.py

# Main
if __name__ == "__main__":

    dsFileName = 'SVHN/train_digitStruct.mat'
    print ('Working on',os.path.split(dsFileName))

    print ('Create .h5 called',os.path.splitext(dsFileName)[0]+'.h5')
    h5f = h5py.File(os.path.splitext(dsFileName)[0]+'.h5', 'w')
    print ('Created',os.path.split(h5f.filename))

# Count number of images in digitStruct.mat file [/name] dataset
    mat_f = h5py.File(dsFileName)
    num_img = mat_f['/digitStruct/name'].size
    mat_f.close()

    ds_dtype = np.dtype ( [('name','S16'), ('label','S10'), ('left','f8'),
                            ('top','f8'), ('width','f8'), ('height','f8')] )
    ds_recarray = np.recarray ( (10,) , dtype=ds_dtype )
    ds_table = h5f.create_dataset('digitStruct', (2*num_img,), dtype=ds_dtype, maxshape=(None,) )

    idx_dtype = np.dtype ( [('name','S16'), ('first','i4'), ('length','i4')] )
##    idx_recarray = np.recarray ( (1,) , dtype=idx_dtype )
    idx_table = h5f.create_dataset('idx_digitStruct', (num_img,), dtype=idx_dtype, maxshape=(None,) )

    imgCounter = 0
    lblCounter = 0

    for dsObj in digitStruct.yieldNextDigitStruct(dsFileName):
        if (imgCounter % 1000 == 0) :
               print(dsObj.name)

        if (idx_table.shape[0] < imgCounter ) : # resize idx_table as needed
            idx_table.resize(idx_table.shape[0]+1000, axis=0)

        idx_table[imgCounter,'name'] = dsObj.name
        idx_table[imgCounter,'first'] = lblCounter
        idx_table[imgCounter,'length'] = len(dsObj.bboxList)

        raCounter = 0

        for bbox in dsObj.bboxList:

            ds_recarray[raCounter]['name'] = dsObj.name
            ds_recarray[raCounter]['label'] = bbox.label
            ds_recarray[raCounter]['left'] = bbox.left
            ds_recarray[raCounter]['top'] = bbox.top
            ds_recarray[raCounter]['width'] = bbox.width
            ds_recarray[raCounter]['height'] = bbox.height
            raCounter += 1
            lblCounter += 1

        if (ds_table.shape[0] < lblCounter ) :   # resize ds_table as needed
            ds_table.resize(ds_table.shape[0]+1000, axis=0)
        ds_table[lblCounter-raCounter:lblCounter] = ds_recarray[0:raCounter]

        imgCounter += 1

##        if imgCounter >= 2000:
##            break

    print ('Total images processed:', imgCounter )
    print ('Total labels processed:', lblCounter )

    ds_table.resize(lblCounter, axis=0)
    idx_table.resize(imgCounter, axis=0)

    h5f.close()