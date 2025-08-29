# mosamatic2
Advanced desktop and API tool for body composition analysis


## 1. Introduction
mosamatic2 is a Python-based tool for advanced body composition analysis. It can work with
two types of imaging data: (1) CT and (2) Dixon MRI. CT images are used to do standard body
composition analysis at L3 level. The tool runs a 2D muscle and fat segmentation on the L3
images and calculates the following body composition metrics:

- Muscle area
- Muscle (mean) radiation attenuation
- Subcutaneous fat area
- Subcutaneous fat (mean) radiation attenuation
- Visceral fat area
- Visceral fat (mean) radiation attenuation

mosamatic2 is also able to use Dixon MRI images to calculate Proton Density Fat Fraction
(PDFF) maps from both L3 images and full (3D) scans. These maps are used to calculate fat
infiltration in either muscle or liver tissue and provides important information about the 
health status of the patient, as well as predictions regarding survival, the risk of post-
surgical complications or the risk of chemotherapy toxicity.
To calculate PDFF maps for muscle tissue (at L3) mosamatic2 requires both a CT scan as well
as a Dixon MRI scan of the patient. Muscle and fat tissue at L3 is extracted using a specific
muscle and fat segmentation AI model. The CT scan is registered to the Dixon MRI scan after
which the L3 muscle and fat tissue can be extracted from the Dixon MRI image at L3. Muscle
fat infiltration can then be determined from the Dixon MRI. 
In the case of liver analysis, mosamatic2 uses Total Segmentator or MOOSE to extract a 3D
mask of the liver from the Dixon MRI water images. The PDFF map in that case can then be
extracted inside the liver parenchyma only and used for clinical assessment.


## 2. Desktop vs. API
mosamatic2 can be started in two ways: (1) as a desktop application (written in PySide6)
or (2) as an API server that can be called through its REST interface from the command-line.
This allows mosamatic2 to be used inside larger data processing and analysis pipelines.


## 3. Installation
mosamatic2 is available on PyPI.org and can be installed using the following command (after
installing Python 3.11):

    python -m pip install mosamatic2

After installation mosamatic2 can be started as desktop application with the command:

    mosamatic2

or as an API server with the command:

    mosamatic2-api

In the latter case, the API server can be accessed through its REST interface at the 
following URL:

    http://localhost:8000

For a full explanation of the mosamatic2 REST interface, see the section "API specification"
below. It explains how to provide the datasets to the API server (either by uploading them or 
specify the local directory where the scans are stored) and how to process the datasets.

You can also find all documentation related to mosamatic2 (both desktop and API) on our 
website https://www.mosamatic.com. 


## 4. Desktop features and user manual


## 5. API specification
