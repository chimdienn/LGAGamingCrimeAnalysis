import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

columns_to_drop = ["Region", "2011", "2012", "2013"]
def filter_lga_name(full_name):
    words = full_name.split()
    try:
        i = words.index("of")
    except ValueError:
        i = words.index("OF")
    return " ".join(words[i+1:])

df= pd.read_csv("Data/EGM.csv").head(57).drop(columns= columns_to_drop)
df["LGA Name"] = df["LGA Name"].apply(filter_lga_name)
df['LGA Name'] = df['LGA Name'].apply(lambda x: 'Merri-bek' if x == 'Moreland' else x)
df.sort_values(by= "LGA Name", inplace= True)
# Set the index to LGA Name 
df.set_index('LGA Name', inplace=True)


# Plot the EGM losses of the first n LGAs
def line_plot(df, n):
    x = ["20" + str(i) for i in range (14,21)]
    y = [df.iloc[i] for i in range (n)]
    for i in range (n):
        plt.plot(x, y[i], label=df.index[i])
    plt.xlabel('Year')
    plt.ylabel("Gaming losses")
    plt.title('Line chart of Gaming Losses by LGA from 2014 to 2020')
    plt.legend()
    plt.savefig("summary_egm_line.png")
    
line_plot(df, 5)

def heat_plot(data):

    # Convert columns to float if not already
    data = data.astype(float)

    plt.figure(figsize=(10, 8))

    # Draw the heatmap with the mask and correct aspect ratio
    sns.heatmap(data, cmap='viridis', linewidths=.5, annot=False, fmt=".0f")

    # Add titles and labels as needed
    plt.title('Heatmap of Gaming Losses by LGA from 2014 to 2020')
    plt.xlabel('Year')
    plt.ylabel('LGA Name')

    # Show the plot
    plt.savefig("summary_egm_heat.png")

heat_plot(df)
df.index.name = 'Local Government Area'
df.to_csv("Data/cleaned_EGM.csv", index = True)
