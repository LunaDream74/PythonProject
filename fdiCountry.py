import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

df_FDI = pd.read_csv('fdi_country_partners_en.csv')
df_indust = pd.read_csv('fdi_industry_en.csv')
df_GNP = pd.read_csv('vietnam-gnp-gross-national-product.csv')

        #cleaning data
head = ['Order','Country','Number of new projects',
        'Newly registered capital (million USD)','Adjusted project number',
        'Adjusted capital (million USD)',
        'Number of times of capital contribution to buy shares',
        'Value of capital contribution, share purchase\n(million USD)','Year']

dfCleaned = df_FDI.fillna(0).replace(to_replace='Liên bang Nga',value='Federal Republic of Russia').replace(' -   ', '0', regex= True)
dfCleaned = dfCleaned.replace(r'\s*(.*?)\s*', r'\1', regex=True)        #trim blank spaces on both sides
dfCleaned = dfCleaned.astype('str')                                     #convert all to str

df_Ind_Cl = df_indust.fillna(0).replace(' -   ', '0', regex= True)
df_Ind_Cl = df_Ind_Cl.replace(to_replace='Manufacturing and processing industry', value='Manufacturing')
df_Ind_Cl = df_Ind_Cl.replace(to_replace='Producing and distributing electricity, gas, water, air conditioning', value='electricity, gas, water, air conditioning')
df_Ind_Cl = df_Ind_Cl.replace(to_replace='Real estate business', value='Real estate')
df_Ind_Cl = df_Ind_Cl.replace(r'\s*(.*?)\s*', r'\1', regex=True)        #trim blank spaces on both sides
df_Ind_Cl = df_Ind_Cl.astype('str') 

for index in range(2,9):
        #usually in accounting(or in excel/csv) they use parentheses rather than negative sign
        #so we have to replace that in our datas
        dfCleaned[head[index]] = (dfCleaned[head[index]].replace('[\,) ]', '', regex= True)).replace('[(]', '-', regex=True)
        df_Ind_Cl[head[index]] = (df_Ind_Cl[head[index]].replace('[\,) ]', '', regex= True)).replace('[(]', '-', regex=True)
        #now we convert collumn 2 -> 8 back to float or int
        dfCleaned[head[index]] = pd.to_numeric(dfCleaned[head[index]])
        df_Ind_Cl[head[index]] = pd.to_numeric(df_Ind_Cl[head[index]])

        #seperate by year
#GNP file
df_GNP['date'] = pd.to_datetime(df_GNP['date'])
df_GNP['year'] = df_GNP['date'].dt.year
df_GNP_f = df_GNP[df_GNP['year'] >= 2015]

#FDI file
df2015 = dfCleaned[dfCleaned[head[8]] == 2015]
df2016 = dfCleaned[dfCleaned[head[8]] == 2016]
df2017 = dfCleaned[dfCleaned[head[8]] == 2017]
df2018 = dfCleaned[dfCleaned[head[8]] == 2018]
df2019 = dfCleaned[dfCleaned[head[8]] == 2019]
df2020 = dfCleaned[dfCleaned[head[8]] == 2020]
df2021 = dfCleaned[dfCleaned[head[8]] == 2021]
df2022 = dfCleaned[dfCleaned[head[8]] == 2022]
#industry file
inds15 = df_Ind_Cl[df_Ind_Cl[head[8]] == 2015]
inds22 = df_Ind_Cl[df_Ind_Cl[head[8]] == 2022]

#make a list of years and dataframe by year for easy access
years = [2015,2016,2017,2018,2019,2020,2021,2022]
dfyears = [df2015,df2016,df2017,df2018,df2019,df2020,df2021,df2022]

#--------------------------------------------------------------------------------
'''VN's FDI over the years graph'''
def graph1():
        fdi = []

        for year in dfyears:
                fdi.append(round(sum(year[head[3]])+sum(year[head[5]])+sum(year[head[7]]),3))

        plotdf = pd.DataFrame({'FDI': fdi}, index= years)
        ax = plotdf.plot(kind='bar', xlabel='Year', ylabel='Million USD', title="VietNam's FDI over the years", rot=0)

        for c in ax.containers:
                ax.bar_label(c, fmt=lambda x: f'{x:.0f}' if x > 0 else '', label_type='edge')

        plt.show()

#--------------------------------------------------------------------------------
'''FDI capital in VN during 2015-2022 graph'''
def graph2():
        totalRegisCap = []
        totalAdjCap = []

        for year in dfyears:
                totalRegisCap.append(round(sum(year[head[3]]),3))
                totalAdjCap.append(round(sum(year[head[5]]), 2))

        plotdf = pd.DataFrame({'Registered capital': totalRegisCap, 'Adjusted capital': totalAdjCap},
                        index = years)

        ax = plotdf.plot(kind='bar', stacked=True, xlabel='Year', ylabel='Million USD', rot=0,
                title='FDI capital in VietNam during 2015-2022')

        for c in ax.containers:
                ax.bar_label(c, fmt=lambda x: f'{x:.0f}' if x > 0 else '', label_type='center')

        plt.show()
#----------------------------------------------------------------------------------
'''VN's FDI investors in 2019 graph'''
def graph3():
        numProj = []
        fdi = []
        country = []

        temp1df = df2019.groupby(head[1])[head[3]].sum()        #registered capital of each country
        temp2df = df2019.groupby(head[1])[head[5]].sum()        #adjusted capital of each country
        temp3df = df2019.groupby(head[1])[head[7]].sum()        #capital contribution, share purchase of each country

        FDIdf = temp1df + temp2df + temp3df                     #total fdi



        #find top 10 investors and others in 2019
        #find fdi
        #sort largest to smallest
        x = sorted(FDIdf, reverse=True)
        for pos, value in enumerate(FDIdf):
                if value in x[0:10]:
                        country.append(FDIdf.index[pos])
                        fdi.append(value)

        #find number of project
        #find number of project from the top 10 biggest investor above
        for name in country:
                for index in df2019.index:
                        if df2019[head[1]][index] == name:
                                numProj.append(df2019[head[2]][index] + df2019[head[4]][index])
        #find the rest of number of project
        remProj = []
        for index in df2019.index:
                if df2019[head[1]][index] not in country:
                        remProj.append(df2019[head[2]][index] + df2019[head[4]][index])

        country.append("Other countries")
        fdi.append(round(sum(x[11:]),3))
        numProj.append(round(sum(remProj)))

        plotdf = pd.DataFrame({'FDI': fdi, 'Number of project': numProj},
                        index= country)

        #AX: bar chart
        ax=plotdf['FDI'].plot(kind="bar", color="orange", title="VietNam's top 10 FDI investors and other in 2019", yticks=range(0, 10000, 500))
        ax.set_ylabel("Total FDI (million USD)")
        ax.set_xlabel("Investors")

        for tick in ax.get_xticklabels():       #rotate the xlabel in correct position
                tick.set_rotation(0)

        #AX2: Create secondary y-axis with same x-axis as above
        ax2=ax.twinx()
        ax2.plot(ax.get_xticks(),plotdf["Number of project"], color="red", linewidth=1.5, marker = ".")
        ax2.grid(False)
        ax2.set_ylabel("Number of projects")
        ax2.tick_params(axis='y')

        #add value to bars and line
        def add_value_labels(ax, typ, spacing=5):
                space = spacing
                va = 'bottom'

                if typ == 'bar':
                        for i in ax.patches:
                                y_value = i.get_height()
                                x_value = i.get_x() + i.get_width() / 2
                                label = "{:.0f}".format(y_value)
                                ax.annotate(label,(x_value, y_value), xytext=(0, space), 
                                        textcoords="offset points", ha='center', va=va)
                        
                if typ == 'line':
                        line = ax.lines[0]
                        for x_value, y_value in zip(line.get_xdata(), line.get_ydata()):
                                label = "{:.2f}".format(y_value)
                                ax.annotate(label,(x_value, y_value), xytext=(0, space), 
                                        textcoords="offset points", ha='center', va=va)

        add_value_labels(ax, typ='bar')
        add_value_labels(ax2, typ='line')

        plt.show()
#----------------------------------------------------------------------------------
'''top investor graph'''
def graph4():
        country = []
        fdi = []

        temp1df = dfCleaned.groupby(head[1])[head[3]].sum()     #find sum of registered capital of each country
        temp2df = dfCleaned.groupby(head[1])[head[5]].sum()     #find sum of adjusted capital of each country
        temp3df = dfCleaned.groupby(head[1])[head[7]].sum()     #find sum of capital contribution, share purchase of each country

        tempdf = temp1df + temp2df + temp3df            #total FDI

        #sort largest to smallest
        x = sorted(tempdf, reverse=True)
        #calculate and find top 10 highest investor
        for pos, value in enumerate(tempdf):
                if value in x[0:11]:
                        country.append(tempdf.index[pos])
                        fdi.append(value)
        #add "other countries" to country list
        country.append('Other countries')
        #add total fdi of all other countries to fdi list
        fdi.append(round(sum(x[11:]),3))

        plotdf = pd.DataFrame({'FDI': fdi}, index=country)

        ax = plotdf.plot(kind='bar', xlabel='Investor', ylabel='Million USD',
                        title="VietNam's top FDI investors compare to others over the years", rot=0)

        for c in ax.containers:
                ax.bar_label(c, fmt=lambda x: f'{x:.0f}' if x > 0 else '', label_type='edge')

        plt.show()
#---------------------------------------------------------------------------------
'''Biggest FDI investor(Korea) over the year'''
def graph5():
        regisCap = dfCleaned.loc[dfCleaned[head[1]] == 'Korea'][head[3]]        #get registered capital of korea for each year
        adjCap = dfCleaned.loc[dfCleaned[head[1]] == 'Korea'][head[5]]          #get adjusted capital of korea for each year
        share = dfCleaned.loc[dfCleaned[head[1]] == 'Korea'][head[7]]           #get capital contribution, share purchase of korea for each year

        #convert series to list
        regisCap = regisCap.tolist()
        adjCap = adjCap.tolist()
        share = share.tolist()

        plotdf = pd.DataFrame({'Registered capital': regisCap, 'Adjusted capital': adjCap, 'Capital contribution, share purchase': share},
                        index= years)

        ax = plotdf.plot(kind='bar', stacked=True, xlabel='Year', ylabel='Million USD', rot=0,
                title="Korea's FDI in VietNam during 2015-2022")

        for c in ax.containers:
                ax.bar_label(c, fmt=lambda x: f'{x:.0f}' if x > 0 else '', label_type='center')
                
        plt.show()
#-----------------------------------------------------------------------------------
'''Comparison of FDI invested industry between the year 2015 and 2022'''
def graph6():
        industry15 = []
        fdi15 = []
        industry22 = []
        fdi22 = []
        #in 2015
        temp1df = inds15.groupby('Industry')[head[3]].sum()        #find sum of registered capital of each industry
        temp2df = inds15.groupby('Industry')[head[5]].sum()        #find sum of adjusted capital of each industry
        temp3df = inds15.groupby('Industry')[head[7]].sum()        #find sum of capital contribution, share purchase of each industry

        inds_15 = temp1df + temp2df + temp3df                  #total fdi of each industry
        #sort largest to smallest
        x = sorted(inds_15, reverse=True)
        for posi, val in enumerate(inds_15):
                if val in x[0:3]:
                        industry15.append(inds_15.index[posi])
                        fdi15.append(val)
        #add "other countries" to country list
        industry15.append('Other')
        #add total fdi of all other countries to fdi list
        fdi15.append(round(sum(x[3:]),3))

        #in 2022
        temp4df = inds22.groupby('Industry')[head[3]].sum()        #find sum of registered capital of each industry
        temp5df = inds22.groupby('Industry')[head[5]].sum()        #find sum of adjusted capital of each industry
        temp6df = inds22.groupby('Industry')[head[7]].sum()        #find sum of capital contribution, share purchase of each industry

        inds_22 = temp4df + temp5df + temp6df                  #total fdi of each industry
        #sort largest to smallest
        y = sorted(inds_22, reverse=True)
        for pos, value in enumerate(inds_22):
                if value in y[0:3]:
                        industry22.append(inds_22.index[pos])
                        fdi22.append(value)
        #add "other countries" to country list
        industry22.append('Other')
        #add total fdi of all other countries to fdi list
        fdi22.append(round(sum(x[3:]),3))

        df_inds_15 = pd.DataFrame({'industry': industry15, 'FDI total': fdi15})
        df_inds_22 = pd.DataFrame({'industry': industry22, 'FDI total': fdi22})
        
        #plotting
        fig,axes = plt.subplots(nrows= 1, ncols= 2)
        df_inds_15.plot(kind= 'pie', y= 'FDI total', labels= df_inds_15['industry'], autopct='%.2f%%', ax = axes[0])
        df_inds_22.plot(kind= 'pie', y= 'FDI total', labels= df_inds_22['industry'], autopct='%.2f%%', ax = axes[1])
        plt.suptitle("Comparison of FDI invested industry between the year 2015 and 2022")
        axes[0].set_title('2015')
        axes[1].set_title('2022')
        plt.show()
#-----------------------------------------------------------------------------------
'''Viet Nam's FDI influence on GNP over the years'''
def graph7():
        fdi = []
        #since the data is in billion USD and the graph is in million, we have to *1000
        gnp = df_GNP_f[' GNP'] * 1000

        #convert series to list to add to plot later
        gnp = gnp.tolist()

        #calculate the total FDI of each year
        for year in dfyears:
                fdi.append(round(sum(year[head[3]])+sum(year[head[5]])+sum(year[head[7]]),3))

        plt.plot(years, fdi, '-*', label= 'FDI')
        plt.plot(years, gnp, '-o', label= 'GNP')
        plt.xlabel("Year")
        plt.ylabel("Million USD")
        plt.legend()
        plt.title("Viet Nam's FDI influence on GNP over the years")
        plt.show()
#-----------------------------------------------------------------------------------
def menu():
        print("1. Viet Nam's FDI over the years.")
        print("2. FDI capital in Viet Nam over the years.")
        print("3. Viet Nam's top 10 FDI investor and others in 2019.")
        print("4. Viet Nam's top investors compare to others over the years.")
        print("5. Korea's FDI in Viet Nam over the years.")
        print("6. Comparison of FDI invested industry between the year 2015 and 2022.")
        print("7. Viet Nam's FDI influence on GNP over the years")
        print("0. Exit.")

def main():
        print("Welcome!!!")
        print("Which graph would you like to see?")
        while True:
                menu()
                option = int(input("Enter your option: "))
                #check for invalid option
                if option not in range(0,8):
                        print("Invalid option. Try again")
                else:
                        if option == 1:
                                os.system('cls')
                                graph1()
                        if option == 2:
                                os.system('cls')
                                graph2()
                        if option == 3:
                                os.system('cls')
                                graph3()
                        if option == 4:
                                os.system('cls')
                                graph4()
                        if option == 5:
                                os.system('cls')
                                graph5()
                        if option == 6:
                                os.system('cls')
                                graph6()
                        if option == 7:
                                os.system('cls')
                                graph7()
                        if option == 0:
                                os.system('cls')
                                print("Exiting.....")
                                print("Goodbye. Thank you for using our code!!")
                                break
main()