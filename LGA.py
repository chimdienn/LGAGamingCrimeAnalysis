import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

df = pd.read_excel("Data/LGA Offences.xlsx", sheet_name="Table 02")

# Table 2 Offence Subgroup:
# Some subgroups in C, D and F Division:
# C: 'C31 Drug use', 'C32 Drug possession', 'C99 Other drug offences'
# D: 'D22 Drunk and disorderly in public'
# F: 'F11 Drink driving', 'F12 Drug driving', 'F33 Liquor and tobacco licensing offences'
# Total 3 Divisions, 7 Subgroups
# Drug-related: C31, C32, C99, F12
# Alcohoh-related: D22, F11, F33

drug_subgroup_list = ['C31 Drug use', 'C32 Drug possession', 'C99 Other drug offences', 'F12 Drug driving']
alcohol_subgroup_list = ['D22 Drunk and disorderly in public','F11 Drink driving', 'F33 Liquor and tobacco licensing offences']
offence_count_columns = ["Year", "Local Government Area", "Offence Subgroup", "Offence Count"]
offence_rate_columns = ["Year", "Local Government Area", "Offence Subgroup", "LGA Rate per 100,000 population"]
offence_df = df[offence_count_columns]
rate_df = df [offence_rate_columns]

lga_mapping = {
    "WHITTLESEA": ["Whittlesea", "Nillumbik"],
    "NORTHERN GRAMPIANS": ["Ararat", 'Northern Grampians'],
    "GREATER GEELONG": ["Queenscliffe", "Greater Geelong"],
    "COLAC-OTWAY": ["Corangamite", "Colac-Otway"],
    "MOORABOOL": ["Hepburn", "Moorabool"],
    "CENTRAL GOLDFIELDS": ["Central Goldfields", "Mount Alexander"],
    "MITCHELL": ["Mansfield", "Murrindindi", "Mitchell"],
    "ALPINE": ["Towong", "Alpine"],
    "BENALLA": ["Moira", "Strathbogie", "Benalla"],
    "CAMPASPE": ["Gannawarra", "Campaspe"],
    "GLENELG": ["Glenelg", "Southern Grampians"]
}

rows_to_remove = ["Buloke", "Golden Plains", "Hindmarsh", "Indigo", "Loddon", "Moyne", "Pyrenees", "West Wimmera", "Yarriambiack"]

def preprocess_df(offence_df, value, subgroup_list, lga_mapping, rows_to_remove):
    new_offence_df = offence_df[offence_df["Offence Subgroup"].isin(subgroup_list)].drop("Offence Subgroup",axis = 1)
    old_to_new = {old_lga: new_lga for new_lga, old_lgas in lga_mapping.items() for old_lga in old_lgas}

    # Map old LGAs to new LGAs
    new_offence_df['Local Government Area'] = new_offence_df['Local Government Area'].replace(old_to_new)

    # Group by 'Year' and 'LGA' and sum the fields
    new_offence_df_combined = new_offence_df.groupby(['Year', 'Local Government Area'], as_index=False).sum(numeric_only=True)
    new_offence_df_pivot = new_offence_df_combined.pivot(index='Local Government Area', columns='Year', values= value).fillna(0)
    new_offence_df_pivot.drop(columns = [2021,2022,2023], inplace = True)
    new_offence_df_pivot.drop(index=rows_to_remove, inplace = True)
    return new_offence_df_pivot

drug_offence_df = preprocess_df(offence_df, "Offence Count", drug_subgroup_list, lga_mapping, rows_to_remove)
alcohol_offence_df = preprocess_df(offence_df, "Offence Count", alcohol_subgroup_list, lga_mapping, rows_to_remove)
drug_rate_df = preprocess_df(rate_df, "LGA Rate per 100,000 population",  drug_subgroup_list, lga_mapping, rows_to_remove)
alcohol_rate_df = preprocess_df(rate_df,"LGA Rate per 100,000 population", alcohol_subgroup_list, lga_mapping, rows_to_remove)

def line_plot(df, n, y_label):
    plt.figure(figsize=(10, 8))
    x = ["20" + str(i) for i in range (14,21)]
    y = [df.iloc[i] for i in range (n)]
    for i in range (n):
        plt.plot(x, y[i], label=df.index[i])
    plt.xlabel('Year')
    plt.ylabel(y_label)
    plt.legend()
    plt.savefig("summary_"+ "_".join(y_label.lower().split())+ "_line.png")
    
line_plot(drug_offence_df, 5, "Drug Offence")
line_plot(alcohol_offence_df, 5, "Alcohoh Offence")

def heat_plot(df, y_label):
    plt.figure(figsize=(10, 8))

    # Draw the heatmap with the mask and correct aspect ratio
    sns.heatmap(df, cmap='viridis', linewidths=0.5, annot=False, fmt=".0f")

    # Add titles and labels as needed
    plt.title('Heatmap of '+ y_label + ' Count by LGA from 2014 to 2020')
    plt.xlabel('Year')
    plt.ylabel(y_label)
    plt.yticks(fontsize=7) 

    # Show the plot
    plt.tight_layout()
    plt.savefig("summary_"+ "_".join(y_label.lower().split())+ "_heat.png")

heat_plot(drug_offence_df, "Drug Offence")
heat_plot(alcohol_offence_df, "Alcohoh Offence")

drug_offence_df.to_csv("Data/drug_offence.csv", index= True)
alcohol_offence_df.to_csv("Data/alcohol_offence.csv", index = True)
drug_rate_df.to_csv("Data/drug_rate_offence.csv", index= True)
alcohol_rate_df.to_csv("Data/alcohol_rate_offence.csv", index = True)
