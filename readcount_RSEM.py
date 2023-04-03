import os
import re
import pandas as pd
from functools import reduce

def main():
    path = os.getcwd()
    files = find_all(path)
    dfs = []
    for title, filename in files.items():
       df = get_readcount(title, filename)
       dfs.append(df)
    merge_df = reduce(lambda left, right:pd.merge(left, right, on='gene_id', how='outer'),dfs)
    merge_df = merge_df.set_index(merge_df.columns[0])
    merge_df.sort_index(axis=1, inplace=True)
    merge_df.drop_duplicates(inplace=True)
    merge_df.to_csv('RSEM_readcount.csv')
    
def find_all(path):
    result={}
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith('genes.results'):
                name = re.search('(\w+_[1,2,3]?)_.*', file).group(1)
                result[name] = file
    return result

def get_readcount(title, filename):
    with open(filename,'r') as file:
        result_all = []
        for line in file:
            result = {}
            line = line.strip()
            line_split = line.split('\t')
            if line.startswith('gene_id'):
                continue
            else:
                result['gene_id'] = line_split[0].split('.')[0]
                result[title]=line_split[4]
            result_all.append(result)
        return pd.DataFrame(result_all)
                
if __name__=="__main__" :
    main()