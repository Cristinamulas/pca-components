
import dataiku
# Import the helpers for custom recipes
from dataiku.customrecipe import get_input_names_for_role
from dataiku.customrecipe import get_output_names_for_role
from dataiku.customrecipe import get_output_names

from dataiku.customrecipe import get_recipe_config
import dataiku
import pandas as pd, numpy as np
from dataiku import pandasutils as pdu

from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler



# Inputs and outputs are defined by roles. In the recipe's I/O tab, the user can associate one
# or more dataset to each input and output role.
# Roles need to be defined in recipe.json, in the inputRoles and outputRoles fields.


input_dataset_name = get_input_names_for_role('input')[0] ##
input_dataset = dataiku.Dataset(input_dataset_name)
dataset_pca_df = input_dataset.get_dataframe()
number_components = get_recipe_config()['number of components']



# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
df_floats = dataset_pca_df.select_dtypes(np.float64)

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
df_normalized=(df_floats - df_floats.mean()) / df_floats.std()
pca = PCA(n_components=number_components)
x = pca.fit(df_normalized)

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
PCnames = ['PC'+str(i+1) for i in range(pca.n_components_)]
eigen_vectors = pd.DataFrame(pca.components_.T,columns=PCnames)
# eigen_vectors['Columns'] = df_floats.columns
# print(eigen_vectors)

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
eigen_variance = pd.DataFrame(pca.explained_variance_,columns=["Variance"],index=PCnames)

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
eigen_variance_ratio = pd.DataFrame(pca.explained_variance_ratio_,columns=["Variance_ratio"],index=PCnames)

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
frame_combined = pd.concat([eigen_variance, eigen_variance_ratio],axis=1)
frame_combined['PCA Components'] = PCnames
# print(frame_combined)

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE

# Write recipe outputs
output_eigen_vectors_final_name = get_output_names('output1')[0]
output_dataset_final_vectors = dataiku.Dataset(output_eigen_vectors_final_name)
output_dataset_final_vectors.write_with_schema(eigen_vectors)

# # Write recipe outputs
eigen_variance_ratio_final_name = get_output_names('output_eigen_variance')[1]
output_dataset_variance_final = dataiku.Dataset(eigen_variance_ratio_final_name)
output_dataset_variance_final.write_with_schema(frame_combined)