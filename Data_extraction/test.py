import h5py
import pandas as pd

file_path = "/home/scohail/Desktop/Script ProCAST to Excel/V_30_714.erfh5"


with h5py.File(file_path, "r") as f:
    post_group = f["post"]
    
    # Check if they are groups or datasets
    for key in post_group.keys():
        if isinstance(post_group[key], h5py.Group):
            post_group_keys = post_group[key].keys()
            print(f"'{key}' is a group with contents: {list(post_group_keys)}")
            
        else:
            print(f"'{key}' is a dataset with shape: {post_group[key].shape} and dtype: {post_group[key].dtype}")
    
    first_state = f["post/constant/entityresults/NODE/COORDINATE/erfblock/res"]
    
    # List datasets/groups inside the first state

    if isinstance(first_state  ,h5py.Group):
    
        print("Contents of 'state000000000051':", list(first_state.keys()))
    else:
        first_state = pd.DataFrame(first_state)
        first_state.to_csv("/home/scohail/Desktop/Script ProCAST to Excel/teste/first_state.csv", index=False)

        print("Contents of 'state000000000101':", first_state.head())   



#=======================================Usual Paths ================================================#
'''



post/singlestate/state000000000681/entityresults/NODE/Temperature/ZONE1_set1/erfblock/res

post/singlestate/state000000000681/entityresults/NODE/Fraction Solid/ZONE1_set1/erfblock/res

post/multistate/multientityresults/MODEL/Fraction_Solid/ZONE1_set1/erfblock





'''