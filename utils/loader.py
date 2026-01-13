import pandas as pd
import os

def load_dataset(filepath):
    try:
        extension= os.path.splitext(filepath.name)[1].lower()
        if extension=='.csv':
            df= pd.read_csv(filepath)
        elif extension in ['.xls','.xlsx']:
            df= pd.read_excel(filepath)
        else:
            return None, "Unsuppoted file format. Must be either excel or csv"
        return df, None

    except Exception as e:
        return None, str(e)

