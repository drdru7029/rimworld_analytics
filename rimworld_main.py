import universal_functions as uf
import os


#MAIN DEFINITIONS

citiesout_path = r"D:\Google Drive\Games Archives\Rimworld\Save backups\Anhatia Accord (Permadeath).txt"
if os.path.exists(citiesout_path)==False:
    citiesout_path = r"C:\Users\Ace\Google Drive\Games Archives\Rimworld\Save backups\Anhatia Accord (Permadeath).txt"


#Establish log interval (in days)
date_interval = 1

raw_data = []

with open(citiesout_path,'r') as f:
    lines = f.readlines()
    for line in lines:
        raw_data.append(line)
        # print(line,)

from itertools import groupby, chain

for idx,i in enumerate(raw_data):
    if '<name.nick>Michael</name.nick>' in i:
        print(idx,i,raw_data[idx:idx+500])

def get_sections(fle,string):
    with open(fle) as f:
        grps = groupby(f, key=lambda x: x.lstrip().startswith(string))
        for k, v in grps:
            if k:
                yield chain([next(v)], (next(grps)[1]))  # all lines up to next #TYPE

colonist_demarker = '<abilityDataClassAbilityUser.AbilityData>AbilityUser.GenericCompAbilityUser</abilityDataClassAbilityUser.AbilityData>'
# colonist_demarker = '<kindDef>Colonist</kindDef>'

test = get_sections(citiesout_path,colonist_demarker)
test = [list(i) for i in test]

# for i in colony_pawns:
#     for j in i:
#         print(j)

test = [i for i in test if 'Colonist' in ''.join(i)]
print([len(i) for i in test])
print(len(test))
# count = 0
# for idx,i in enumerate(colony_pawns):
#     if len(i)<1000:
#         print(idx,i)
#         print('')
#         print('')
    # if 'Michael' in i:
    #     count+=1
    #     print(idx,i)
    #     print('')

# print('count',count)

# pawn_count = 0
# colonist_count = 0
# pawn_idx = []
#
# for idx,i in enumerate(raw_data):
#     if '<thing Class="Pawn">' in i:
#         pawn_count+=1
#         pawn_idx.append(idx)


# pawn_idx_range = pawn_idx[0],pawn_idx[-1]
# print('pawn_idx_range',pawn_idx_range)
# pawn_data = raw_data[pawn_idx_range[0]:pawn_idx_range[-1]]
# pawn_data_chunks = []
# for idx,val in enumerate(pawn_idx):
#     try:
#         pawn_data_chunks.append(pawn_idx[idx+1]-val)
#     except IndexError:
#         pass
#
# pawn_data = uf.partition_flattened_list_multiple(pawn_data, pawn_data_chunks)
#
#
# for idx,i in enumerate(pawn_data):
#     print(idx,i)
#     print('')
# print([len(i) for i in pawn_data])

# print('raw_data',len(raw_data), 'char count',pawn_count,colonist_count)




# raw_data = [i[0].split(',') for i in raw_data]

# for i in raw_data:
#     print(i)

#<thing Class="Pawn">