#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pathlib

import pandas as pd

# In[2]:


file_path = pathlib.Path(
    "../../data/5.converted_data/custom_aggregated_data.parquet"
).resolve(strict=True)
df = pd.read_parquet(file_path)
df.head()


# We want to remove CellProfiler features that do not accurately contribute to the shape variance.
#
#
# Spatial moment features are removed as they are not invariant to rotation and translation.
#
# Central moment features are removed as measurements of size is not of interest.
#
# Normalized moment features are removed as they do not contribute to the shape variance.
#
# EulerNumber is removed as we are not concerned with the number of holes in the shape.
#
# Extent is removed as we do not care about the ratio of pixels in the bounding box to the pixels in the shape.
#
# Orientation is removed as we are not concerned with the angle of the major axis of the shape.
#
# Zernike features are removed as they are not invariant to rotation and translation.
#
# Texture features are removed as we are not interested in the texture of the shape.

# In[3]:


list_to_drop = [
    "SpatialMoment",
    "CentralMoment",
    "NormalizedMoment",
    "EulerNumber",
    "Extent",
    "Orientation",
    "Zernike",
    "Texture",
]


# In[4]:


# drop columns that contain Metadata
df1 = df.copy()
df1 = df1.drop(columns=[col for col in df1.columns if "Metadata" in col])
columns = df1.columns.to_list()
print(df1.shape)
# if column contains any of the strings in list_to_drop, drop it
for col in list_to_drop:
    columns = [c for c in columns if col not in c]
df1 = df1[columns]
print(df1.shape)
df1["Metadata_genotype"] = df["Metadata_genotype"]
df1["Metadata_replicate"] = df["Metadata_replicate"]


# In[5]:


df1.head()


# In[6]:


# save the dataframe
df_path = pathlib.Path(
    "../../data/5.converted_data/custom_aggregated_manual_feature_selected_data.parquet"
)
df1.to_parquet(df_path)
