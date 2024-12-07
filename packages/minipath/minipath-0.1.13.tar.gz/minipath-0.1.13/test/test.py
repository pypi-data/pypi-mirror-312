from minipath import MiniPath
import pandas as pd
from time import time
import logging
from PIL import Image
import numpy as np

logging.getLogger()

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,  # Set the logging level
    format='%(asctime)s - %(levelname)s - %(message)s',  # Customize the format
)


low_mag = 'https://healthcare.googleapis.com/v1/projects/ml-mps-adl-dpp-ndsa-p-4863/locations/us/datasets/ml-phi-pathology-data-us-p/dicomStores/ml-phi-pathology-data-us-p-dicom-ndsa/dicomWeb/studies/1.2.840.113713.1.1386.386146.86146931/series/1.2.826.0.1.3680043.10.559.1138182560881529769262800323820706134/instances/1.3.6.1.4.1.11129.5.7.1.1.426853759540.29276025.1695043168911079'
high_mag = 'https://healthcare.googleapis.com/v1/projects/ml-mps-adl-dpp-ndsa-p-4863/locations/us/datasets/ml-phi-pathology-data-us-p/dicomStores/ml-phi-pathology-data-us-p-dicom-ndsa/dicomWeb/studies/1.2.840.113713.1.1386.386146.86146931/series/1.2.826.0.1.3680043.10.559.1138182560881529769262800323820706134/instances/1.2.826.0.1.3680043.10.559.1111325636557798006944729960644988975'


# Creating a pandas dataframe with the specified columns and dummy values
data = {
    "gcs_url": [
        low_mag,
        high_mag

    ],
    "SeriesInstanceUID": [low_mag.split('/')[16],
                          high_mag.split('/')[16]],
    "row_num_asc": [1, 2],
    "row_num_desc": [2, 1]
}
df = pd.DataFrame(data)
df.to_csv('test.csv', index=False)
start = time()
minipath = MiniPath(csv='test.csv', subset=True, patch_size=8, min_k=5, patch_per_cluster=1, max_k=8)
minipath.get_representatives(full_url=low_mag)
rep_time = time()
high_res_frames = minipath.get_high_res()
high_res_time = time()

i = 0
for i,x in enumerate(high_res_frames):
    print(f"{i}: Mean: {x['img_array'].shape}")
   #img = Image.fromarray(x)
   #img.save(f'test/{i}.png')

loop_time = time()

print(f'{i} patches,'
      f'Rep time: {(rep_time - start) / 60 :.2f} min, '
      f'HighRes: {(high_res_time - rep_time) / 60 :.2f} min, '
      f'Loop Time: {(loop_time-high_res_time) / 60 :.2f} min, '
      f'Total: {(loop_time - start) / 60 :.2f} min')
