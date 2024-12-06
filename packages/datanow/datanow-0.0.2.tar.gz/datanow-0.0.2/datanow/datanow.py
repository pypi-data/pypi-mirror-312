
#***********************************************************************************************************
#*************************** WELCOME MESSAGE ****************************************************************
#***********************************************************************************************************

def datanow():
#  pip install mlxtend pandas openpyxl
#  pip install pandas scikit-learn openpyxl matplotlib
  print("**********************************************************")
  print("Welcome to use datanow *: an open source stat tool")
  print()
  print("please type test to start")
  # print()
  # print()
  print("**********************************************************")




#SUBPACKAGE: test---------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------
# functions: conduct varoious statistic tests
#***********************************************************************************************************
def test():
  import pandas as pd
  import numpy as np
  from scipy import stats
  import seaborn as sns
  import matplotlib.pyplot as plt
  from google.colab import files
  import io

  # Step 1: Upload the Excel file
  uploaded = files.upload()

  # Step 2: Load the Excel file into a DataFrame
  df = pd.read_excel(io.BytesIO(uploaded[list(uploaded.keys())[0]]))

  # Step 3: Display the uploaded data
  print("Here is the uploaded data:")
  print(df.head())

  # Step 4: Explain the statistical tests
  print("\nPlease choose a statistical test to perform:")
  print("1. Chi-Square Test: Used to examine the association between two categorical variables.")
  print("2. T-test: Used to compare the means of two groups.")
  print("3. ANOVA: Used to compare the means of three or more groups.")
  # print("4. Z-test: Used to compare the means of two groups, typically when the sample size is large or the population variance is known.")

  # Step 5: User chooses the statistical test
  choice = input("\nEnter the number corresponding to your choice (1, 2, or 3):\n")

  # Step 6: User enters the significance level
  alpha = float(input("\nEnter the significance level (e.g., 0.05 for 5% significance):\n"))

  # Step 7: Perform the chosen test and display the results
  if choice == '1':
      # Chi-Square Test
      crosstab = pd.crosstab(df['Group'], df['Measure'])
      chi2, p, dof, expected = stats.chi2_contingency(crosstab)

      print(f"\nChi-Square Test Results:")
      print(f"Chi-Square Statistic: {chi2:.4f}")
      print(f"Degrees of Freedom: {dof}")
      print(f"p-value: {p:.4f}")
      
      if p < alpha:
          print(f"Interpretation: The p-value is less than {alpha}, indicating a statistically significant association between the Group and Measure variables. This means that the distribution of the Measure variable is different across the different Groups, and the likelihood of this difference being due to chance is low.")
      else:
          print(f"Interpretation: The p-value is greater than {alpha}, indicating no statistically significant association between the Group and Measure variables. This suggests that any observed differences in the distribution of the Measure variable across the Groups could likely be due to chance.")

      # print("Note: Chi-Square Test is most appropriate when you have two categorical variables and you want to see if the categories are independent of each other.")
      
      # Plot the results
      sns.countplot(x='Group', hue='Measure', data=df)
      plt.title('Chi-Square Test: Group vs Measure')
      plt.show()

  elif choice == '2':
      # T-test (independent samples)
      groups = df['Group'].unique()
      
      if len(groups) != 2:
          print("Error: T-test requires exactly two groups.")
      else:
          group1 = df[df['Group'] == groups[0]]['Measure']
          group2 = df[df['Group'] == groups[1]]['Measure']
          
          t_stat, p = stats.ttest_ind(group1, group2)
          
          print(f"\nT-test Results:")
          print(f"T-statistic: {t_stat:.4f}")
          print(f"p-value: {p:.4f}")
          
          if p < alpha:
              print(f"Interpretation: The p-value is less than {alpha}, indicating a statistically significant difference in the means of {groups[0]} and {groups[1]}. This suggests that the observed difference in means is unlikely to have occurred by chance.")
          else:
              print(f"Interpretation: The p-value is greater than {alpha}, indicating no statistically significant difference in the means of {groups[0]} and {groups[1]}. This implies that any observed difference in means could likely be due to chance.")

          # print("Note: The T-test assumes that the data in each group is normally distributed and that the variances in the two groups are equal.")
          
          # Plot the results
          sns.boxplot(x='Group', y='Measure', data=df)
          plt.title('T-test: Group vs Measure')
          plt.show()

  elif choice == '3':
      # ANOVA
      f_stat, p = stats.f_oneway(*(df[df['Group'] == group]['Measure'] for group in df['Group'].unique()))

      print(f"\nANOVA Results:")
      print(f"F-statistic: {f_stat:.4f}")
      print(f"p-value: {p:.4f}")
      
      if p < alpha:
          print(f"Interpretation: The p-value is less than {alpha}, indicating a statistically significant difference in means across the groups. This suggests that at least one group mean is significantly different from the others.")
      else:
          print(f"Interpretation: The p-value is greater than {alpha}, indicating no statistically significant difference in means across the groups. This suggests that any observed differences in means are likely due to chance.")

      # print("Note: ANOVA assumes that the data in each group is normally distributed and that the variances across the groups are equal. If you find a significant result, post-hoc tests can be conducted to determine which specific groups differ from each other.")
      
      # Plot the results
      sns.boxplot(x='Group', y='Measure', data=df)
      plt.title('ANOVA: Group vs Measure')
      plt.show()

  elif choice == '4':
      # Z-test
      groups = df['Group'].unique()
      
      if len(groups) != 2:
          print("Error: Z-test requires exactly two groups.")
      else:
          group1 = df[df['Group'] == groups[0]]['Measure']
          group2 = df[df['Group'] == groups[1]]['Measure']
          
          mean1 = np.mean(group1)
          mean2 = np.mean(group2)
          std1 = np.std(group1, ddof=1)
          std2 = np.std(group2, ddof=1)
          n1 = len(group1)
          n2 = len(group2)
          
          # Calculate the Z-statistic
          z_stat = (mean1 - mean2) / np.sqrt((std1**2/n1) + (std2**2/n2))
          p = stats.norm.sf(abs(z_stat)) * 2  # two-tailed p-value
          
          print(f"\nZ-test Results:")
          print(f"Z-statistic: {z_stat:.4f}")
          print(f"p-value: {p:.4f}")
          
          if p < alpha:
              print(f"Interpretation: The p-value is less than {alpha}, indicating a statistically significant difference in the means of {groups[0]} and {groups[1]}. This suggests that the observed difference in means is unlikely to have occurred by chance.")
          else:
              print(f"Interpretation: The p-value is greater than {alpha}, indicating no statistically significant difference in the means of {groups[0]} and {groups[1]}. This implies that any observed difference in means could likely be due to chance.")

          print("Note: The Z-test is generally used when the sample size is large or when the population variance is known. It assumes that the data in each group is normally distributed.")
          
          # Plot the results
          sns.boxplot(x='Group', y='Measure', data=df)
          plt.title('Z-test: Group vs Measure')
          plt.show()

  else:
      print("Invalid choice. Please restart and select a valid option.")

