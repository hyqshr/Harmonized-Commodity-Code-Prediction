# Harmonized Commodity Code Prediction

Description
-----------
Harmonized Tariff Schedule (HTS) codes provide a systematic structure for the classification and taxation of products, enabling International trade worldwide. Customs experts assign HS codes to tens of thousands of products every day. This manual process of assigning codes is a time-consuming, tiresome, and error-prone task. So, we want to automate this process leveraging machine learning to reduce errors in the classification process and reduce manual effort. 
To build this machine learning model, we are using 2021 updated US Imports data from the US Imports website [7], from where we crawled numerous product descriptions for each HS code. We are using YAKE, RAKE, and KeyBERT models to extract keywords from the data, which will be matched with the new product descriptions using Fuzzy String Matching to assign HS codes to new products. We will find the best-performing model using metrics such as accuracy, precision, recall, and F1 score. 

Authors
-----------
Priyanka Padinam, Santosh Saranyan , Hwijong Im, Yiqiu Huang
