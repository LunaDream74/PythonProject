# UNIVERSITY OF SCIENCE - VNUHCM
# PYTHON PROJECT
# PROJECT:
# DATA ANALYSIS ON FOREIGN DIRECT INVESTMENT IN VIETNAM
GROUP 3 - 22CVD1

## 1. INFORMATION AND INTRODUCTION
Economic growth is positively correlated with the annual increase in FDI attraction in Vietnam. FDI capital accounts for a significant proportion of total investment capital of the whole society. The increase in disbursed FDI will expand the production scale of economic sectors, thereby creating conditions to promote economic growth. FDI also helps boost exports, contributing to Vietnam's trade balance surplus, thereby boosting GDP growth. Foreign direct investment data from 2015 to the end of 2022 provides readers with the number of new investments and the amount of capital invested by foreign investors.

Attributes: The data includes attributes such as investment partners, number of newly granted projects, registered capital (millions of dollars), number of adjusted projects, adjusted capital, number of capital contributions, capital contribution value (millions of dollars), the name of the industry to be invested and the year of investment.

Our data can be found at: https://data.opendevelopmentmekong.net/dataset/fdi-investment-in-vietnam-2015-2022

                          https://www.macrotrends.net/global-metrics/countries/VNM/vietnam/gnp-gross-national-product?fbclid=IwZXh0bgNhZW0CMTAAAR3wnWFKwLEHDuWMGpTR08Qb3b9ipDgKxRIpQUz8MgAuNYVtl53LGZI0Kis_aem_Ae6vdxhTj4hi_AUvnWxvorS9qUkDThthPtJ_nrmVgsIulSZ4-YORTEONfEz1rPuqD60yq7rnRePlXOCbpZ8lOCo5

- The purpose of this project is to understand the general trends in FDI, identify trends and changes in the flow of FDI, analyze which countries are the major investors in Viet Nam, finds out which of Viet Nam's industries attract the most FDI as well as the impact of FDI on Viet Nam's economy over the years.

# How to use:
## DISCLAIMER
        *Before using our code, you should install at least 3 of the 4 Python libraries we mentioned in sector 3 of this file.
        (Seaborn is optional)
        *To install, use:
                pip install numpy pandas matplotlib seaborn
                -m pip install <library name>

[Use VSCode]
- Open "fdiCountry.py" file to access our code and click the "Run code" button on the top right corner to run (or press Ctrl + Alt + N).
- After you run the code, a GUI will show up on your terminal. Just follows what it says and enjoy the graphs and charts. We recommend you should open full screen for better view of the graph. To access the next graph just close the tab figure.
## 2. SCOPE OF ANALYSIS
- Descriptive analysis: Based on the data given, look for a way to understand the basic trends in FDI in Viet Nam over the years
- Trend analysis: Identify trends and changes in the flow of FDI.
- Source analysis: Analyze which countries are the major investors in Vietnam. While doing so we also looked further into the biggest investor.
- Sector analysis: Determine which sectors, which industries attract the most FDI.
- Impact analysis: Assess the economic impact of FDI on Viet Nam's economy. i.e: GNP (Gross National Income)
## 3. PROJECT EXECUTION
Here, we use Python as a tool for data analysis and it's libraries to aid in our project.

- Pandas library: provides high-performance, easy-to-use data structures and data analysis tools for the Python programming language.
- Numpy library: used for working with arrays, matrices and brings the computational power of C to Python.
- Matplotlib library: we use pyplot submodule in matplotlib library for visualizing data with lines and charts. 
- Seaborn library: is a Python data visualization library based on matplotlib. It provides a high-level interface for drawing attractive and informative statistical graphics.

Our code can be divided into 3 parts: 
- Cleaning data
- Data transformation
- Visualization

# Cleaning data

- Firstly, we use pandas to read the 3 files to get data
- Then we clean out the blank spaces, minus signs and translate any name errors.
- Convert all number-liked strings to normal number for future use.

# Data transformation

- We select out appropriate collumns of data for analysis.
- Then we put them in a pandas's dataframe for easy plotting.
For example: take the graph "FDI capital in Viet Nam over the years".
   + For this graph we need 2 collumns of data, which is "Registered capital" and "Adjusted capital".
   + When we've identified which collumns are appropriate. We begin to take out the data, seperate by year and add them to a dataframe.

# Visualization

- Our goal is to turn the unreadable amount of data into a visual guide (like charts and graphs) to illustrate FDI trends and help you understand it.
- In this project we exclusively use "dataframe.plot" because it's the easiest to understand and quickest way to plot a graph or chart.