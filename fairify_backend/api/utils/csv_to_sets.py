import pandas as pd

def load_word_sets_from_csv(file_path):

    df = pd.read_csv(file_path)
    
    headings = list(df.columns)
    

    target_1 = df[headings[0]].dropna().tolist()  
    target_2 = df[headings[1]].dropna().tolist() 
    attr_1 = df[headings[2]].dropna().tolist()   
    attr_2 = df[headings[3]].dropna().tolist()   
    
    return target_1, target_2, attr_1, attr_2, headings
