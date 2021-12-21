import pandas as pd
userdicdf = pd.read_csv(r'Z:\UserProfile\s20192004\Documents\Graaaasses.VSCode\csv\p_keka.csv', sep=',', encoding='utf-8', index_col=False, header=None)
print("トップ3")

for i in range(3):
    print(userdicdf[0][i])
    print(userdicdf[1][i])
    print("--"*50) 

print("ワースト3")

for i in range(3,6):
    print(userdicdf[0][i])
    print(userdicdf[1][i])
    print("--"*50) 