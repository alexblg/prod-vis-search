import torch
import torch.nn as nn
import torch.nn.functional as F
import torchvision.transforms as transforms
import torchvision

import os 
from os import listdir
import pandas as pd
from PIL import Image

IMG_PATH = r"/home/alex/data/wir/raffineurs"
IMG_INVENTORY_PATH = 'app/static/img_inventory.csv'
IMG_STATIC_LIST = ['1015-8599-large_default-votre-portrait-dans-un-studio-du-xixeme-siecle.jpg',
 '1033-8975-large_default-mug-egoist-feminisit-anarchist-pessimist-optimist.jpg',
 '1058-14147-large_default-t-shirt-smoking-pipe.jpg',
 '1087-9246-large_default-cube-en-bois-magnetique.jpg',
 '1128-13515-large_default-rendez-vous-pour-creer-votre-creme-sur-mesure.jpg',
 '1160-9831-large_default-un-terrarium-a-composer-soi-meme.jpg',
 '1191-10092-large_default-maillot-de-bain-iguazu.jpg',
 '1215-10321-large_default-affiche-50-choses-a-faire-dans-une-vie.jpg',
 '1244-10653-large_default-carnet-de-projets.jpg',
 '1261-10675-large_default-affiches-ville-mondrian.jpg']
IMG_STATIC_LIST = os.listdir(IMG_PATH)

with open("imagenet_classes_to_labels_map.txt") as f:
    labels = eval(f.read())
    
if torch.cuda.is_available():  
    dev = "cuda:1" 
else:  
    dev = "cpu"  
device = torch.device(dev)
device = torch.device('cpu')

import torchvision.models as models

net = models.resnet101(pretrained=True)
net.to(device)
net.eval()

from torchvision import transforms
transform = transforms.Compose([            #[1]
 transforms.Resize(256),                    #[2]
 transforms.CenterCrop(224),                #[3]
 transforms.ToTensor(),                     #[4]
 transforms.Normalize(                      #[5]
 mean=[0.485, 0.456, 0.406],                #[6]
 std=[0.229, 0.224, 0.225]                  #[7]
 )])

df = pd.DataFrame(columns=['prod_id','img_id','image_name']+list(labels.keys()))
df['prod_id'] = [img.split('-')[0] for img in IMG_STATIC_LIST]
df['img_id'] = [img.split('-')[1] for img in IMG_STATIC_LIST]
df['image_name'] = IMG_STATIC_LIST

for i, image_name in enumerate(df.image_name):
    print(i, image_name)
    
    # load image
    img_path = os.path.join(IMG_PATH, image_name)
    img = Image.open(img_path)
    
    # infer classes
    output = net(transform(img).unsqueeze(0))
    _, indices = torch.sort(output[[0][:]], descending=True)
    percentage = torch.nn.functional.softmax(output, dim=1)[0]
    
    # store in dataframe
    df.loc[i, df.columns[3:]] = percentage.detach().numpy()

df.to_csv('img_infer_output.csv', index=False)
    
from utils import get_topn_labels

labelled_df = df.loc[:, df.columns[:3]].copy()
labelled_df['content'] = ''

for i, image_name in enumerate(df.image_name):
    topnlabels = get_topn_labels(df.loc[i, df.columns[3:]])
    labelled_df.loc[i, 'content'] = ' '.join(topnlabels.label_name.tolist())
    
labelled_df.to_csv('img_top10_labels.csv', index=False)