with open("imagenet_classes_to_labels_map.txt") as f:
    labels = eval(f.read())
    
def get_topn_labels(row, n=10):
    outdf = row.astype(float).nlargest(n).reset_index()
    outdf.columns = ['label_id','percentage']
    outdf['label_name'] = outdf.label_id.map(labels)
    return outdf

class ToRGB(object):
    def __call__(self, img):
        return img.convert('RGB')