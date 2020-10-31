from rimworld_main_0330 import pawn_dict
import universal_functions as uf
import universal_functions_matplotlib as ufm
import pandas as pd


print('')
print('------------------DATA PROCESSING------------------------')
print('')

all_pawns = list(pawn_dict.keys())
all_pawns.sort()

all_skills = []
for idx,(keys,values) in enumerate(pawn_dict.items()):
    if idx==0:
        all_skills.append(list(values.keys()))

all_skills = all_skills[0]

print('all_skills',all_skills)
print('all_pawns',all_pawns)

##Analysis types##

#total skills
pawn_total_skills = []
for idx,pawn in enumerate(all_pawns):
    total = []
    # each = pawn_dict[pawn]
    for skill in all_skills:
        try:
            total.append(int(pawn_dict[pawn][skill]['Level']))
        except:
            print('SKILL ERROR',pawn,idx,skill)


    total = sum(total)

    pawn_total_skills.append(total)

pawn_total_skills,all_pawns= list(zip(*sorted(zip(pawn_total_skills,all_pawns))))
for name,total in zip(all_pawns,pawn_total_skills):
    # print(name,total)
    pawn_dict[name]["Total skills"] = total



for keys,values in pawn_dict.items():
    print(keys,values["Total skills"])

ufm.bar_chart_simple(pawn_total_skills,all_pawns,"Pawn Total Skills", using_dates=False, average_line=True,show=True)

# ufm.heatmap()