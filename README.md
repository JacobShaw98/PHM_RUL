# Predicting Failure in Manufacturing Tools
#### Data 606 Capstone Project - Group Work

### Overview 
This project aims to predict failure and the remaining useful life (RUL) of tools in an ion etching mill. This consists of predicting the failure itself and  It analyzes only one tools of the 20 tools in the phm 2018 Data challenge dataset. Being able to predict failure in manufacturing is critical as cost of failure of equipment is more costly than the cost of maintenance. 

### Dataset
The dataset can be found on the phm 2018 data challenge website (https://phmsociety.org/wp-content/uploads/2018/05/PHM-Data-Challenge-2018-vFinal-v2_0.pdf). According to the dataset discription the tools in the ion etch mill is used to manufacture wafers.The wafer is a semi-conductor in electronic devices and solar cells (https://en.Wikipedia.org/wiki/Wafer_(electronics)). An ion beam is used to insert grobves on the wafer. The helium gas is passed behind the wafer to cool it while the helium is indirectly cooled by the water system called flowcool. The dataset consists of 20 tools, each tool has 3 datasets provided for it. The train, time to fault and fault datasets. In this prooject only one tool is analyzed 01_M02. 

The Train dataset has 24 features and 5110542 rows. Its size is about 1.7GB.
The Time to Fault dataset has 4 features and 5110542 rows. Its size is 169.76 MB
The fault dataset has 4 features and 109 rows. Its size is 6KB.

The dataset provide data for 3 faults:
- Flowcool pressure dropped below limit
- Flowcool pressure too high check flowcool pump.
- Flowcool leak

### Some data issues
- Disparate data in the features data.
- Missing data on the TTF files
- The time variable has inconsistent gaps mostly like due to the machine being shut down for maintenance. Therefore, the time variable cannot be used as a index.
- Sensor data has no distinct pattern or seasonality.
- Extreme Imbalance data - The Fault and TTF datasets have over 5 million rows, compared to a total of 109 faults in the Fault dataset. 

### Pre-processing
- Data analysis divided to 3 parts. Each fault will be analyzed separately. 
- We begin with Flowcool Pressure Dropped Below Limit Fault.
- Fixture Shutter Position is set to 1 as most of the activity is on this setting.
- The Rotation Speed feature is dropped as it is constant. The time feature is also dropped.
- New classification features are created using cutoffs for failure.

### Streamlit
Go to https://jacobshaw98-phm-rul-streamlitdata-690-proj-2-github-4azyyj.streamlit.app/ to access the webhosted version of our interface
When asked to upload a CSV, upload the CSV that is located in the streamlit folder named 690_fault_1

### Tools used
- Numpy, Pandas, Matplotlib, Seaborn, Sklearn - Random Forest Regressor, Random Forest Classifier, Train-Test Split, TimeSeriesSplit, Streamlit, rfpimp.
