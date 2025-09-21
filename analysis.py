import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from sklearn.feature_selection import mutual_info_regression
from scipy.stats import pearsonr

columns_to_sum = [str(i) for i in range (2014,2021)]

egm_df = pd.read_csv("Data/cleaned_EGM.csv")
egm_df['Sum'] = egm_df[columns_to_sum].sum(axis=1)

drug_df = pd.read_csv("Data/drug_offence.csv")
drug_df['Sum'] = drug_df[columns_to_sum].sum(axis=1)

alcohol_df = pd.read_csv("Data/alcohol_offence.csv")
alcohol_df['Sum'] = alcohol_df[columns_to_sum].sum(axis=1)

def sum_scatter():
    plt.figure(figsize=(10, 8))
    
    plt.scatter(list(egm_df["Sum"]), list(drug_df["Sum"]), label = "Drug")
    slope, intercept = np.polyfit(egm_df["Sum"], drug_df["Sum"], 1)

    # Generate y values for the line of best fit
    line_of_best_fit = slope * egm_df["Sum"] + intercept

    # Step 3: Plot the line of best fit
    plt.plot(egm_df["Sum"], line_of_best_fit, color='blue', alpha = 0.5)
    
    plt.scatter(list(egm_df["Sum"]), list(alcohol_df["Sum"]), label = "Alcohol")
    slope, intercept = np.polyfit(egm_df["Sum"], alcohol_df["Sum"], 1)

    # Generate y values for the line of best fit
    line_of_best_fit = slope * egm_df["Sum"] + intercept

    # Step 3: Plot the line of best fit
    plt.plot(egm_df["Sum"], line_of_best_fit, color='orange', alpha = 0.5)
    
    
    plt.xlabel('Total Gaming Losses', fontsize=12)
    plt.ylabel('Total Offences', fontsize=12)
    plt.title("Total Drug and Alcohol Offences of every LGA from 2014 to 2020")
    plt.legend()
    plt.savefig("total_losses_offence_scatter")
sum_scatter()

# Pearson Correlation
print(f'Total EMG - Drug Pearson Correlation: {egm_df["Sum"].corr(drug_df["Sum"]):.3f}') # = 0.725 strong positive linear relationship
print(f'Total EGM - Alcohol Pearson Correlation: {egm_df["Sum"].corr(alcohol_df["Sum"]):.3f}\n') # = 0.293 weak positive linear relationship

# Mutual Information
print(f'Total EGM - Drug Mutual Information: {mutual_info_regression(egm_df["Sum"].values.reshape(-1, 1),drug_df["Sum"], discrete_features=False)[0]:.3f}') # = 0.749 meaningful amount of shared information
print(f'Total EGM - Alcohol Mutual Information: {mutual_info_regression(egm_df["Sum"].values.reshape(-1, 1),alcohol_df["Sum"], discrete_features=False)[0]:.3f}\n') # = 0.319  not as much meaningful

def egm_offence_scatter(start, end, offence_df, y_label):
    plt.figure(figsize=(10, 8))
    for i in range (start, end):
        plt.scatter(list(egm_df.iloc[i])[1:-1], list(offence_df.iloc[i])[1:-1], label = offence_df["Local Government Area"][i])
    plt.xlabel('Gaming Losses', fontsize=12)
    plt.ylabel(y_label, fontsize=12)
    plt.title("Gaming Losses vs " + y_label + " by every year from 2014 to 2020")
    plt.legend()
    plt.savefig("_".join(y_label.lower().split()) + "_from_LGA_" + str(start) + "_to_" + str(end) + "_by_every_year")
    
egm_offence_scatter(5, 10, drug_df, "Drug Offences")
egm_offence_scatter(5, 10, alcohol_df, "Alcohol Offences")
egm_offence_scatter(20, 27, drug_df, "Drug Offences")
egm_offence_scatter(20, 27, alcohol_df, "Alcohol Offences")

def calculate_mean_pear_corr(offence_df):
    total_corr = 0
    for i in range (57):
        corr_coeff, p_value = pearsonr(list(egm_df.iloc[i]["2014": "2020"]), list(offence_df.iloc[i]["2014": "2020"]))
        total_corr += corr_coeff
    return total_corr/57
print(f"Mean EGM - Drug pearson corr from 2014 - 2020 of all 57 LGAs: {calculate_mean_pear_corr(drug_df):.3f}")
print(f"Mean EGM - Alcohol pearson corr from 2014 - 2020 of all 57 LGAs: {calculate_mean_pear_corr(alcohol_df):.3f}\n")

def calculate_mean_MI(offence_df):
    total_MI = 0
    for i in range(57):
        total_MI += mutual_info_regression(egm_df.iloc[i]["2014": "2020"].values.reshape(-1,1), offence_df.iloc[i]["2014": "2020"], discrete_features=False)[0]
    return total_MI/57
print(f"Mean EGM - Drug mutual information from 2014 - 2020 of all 57 LGAs: {calculate_mean_MI(drug_df):.3f}")
print(f"Mean EGM - Alcohol mutual information from 2014 - 2020 of all 57 LGAs: {calculate_mean_MI(alcohol_df):.3f}\n")
