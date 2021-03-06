import universal_functions as uf
import os
from itertools import groupby, chain


#MAIN DEFINITIONS

citiesout_path = r"D:\Google Drive\Games Archives\Rimworld\Save backups\Anhatia Accord (Permadeath).txt"
if os.path.exists(citiesout_path)==False:
    citiesout_path = r"C:\Users\Ace\Google Drive\Games Archives\Rimworld\Save backups\Anhatia Accord (Permadeath).txt"

raw_data = []

with open(citiesout_path,'r') as f:
    lines = f.readlines()
    for line in lines:
        raw_data.append(line)
        # print(line,)


def get_sections(fle,string):
    with open(fle) as f:
        grps = groupby(f, key=lambda x: x.lstrip().startswith(string))
        for k, v in grps:
            if k:
                yield chain([next(v)], (next(grps)[1]))  # all lines up to next #TYPE

colonist_demarker = '<abilityDataClassAbilityUser.AbilityData>AbilityUser.GenericCompAbilityUser</abilityDataClassAbilityUser.AbilityData>'
# colonist_demarker = '<kindDef>Colonist</kindDef>'

colony_pawns = get_sections(citiesout_path, colonist_demarker)
colony_pawns = [list(i) for i in colony_pawns]

# colony_pawns = [i for i in colony_pawns if 'Colonist' in ''.join(i)]

colony_pawns_final = []
pawn_names = []


colonist_demarker_2 = 'Faction_9'

end_demarker = '<abilityDataPawnAbilityUser.AbilityData>Thing_Human'
end_demarker = '<medCare>Best</medCare>'
for idx,each in enumerate(colony_pawns):
    # if idx==10:
    #     print(each)
    if any(colonist_demarker_2 in x for x in each):
        branch = []
        for pawn in each:
            if '<nick>' in pawn:
                pawn_names.append(pawn)
            if end_demarker not in pawn:
                branch.append(pawn)
            else:
                break
        colony_pawns_final.append(branch)

print('test')

print([len(i) for i in colony_pawns_final])
print(len(colony_pawns_final))


pawn_dict = {}
skill_begin = '<skills>'
skill_end = '</skills>'
skill_relevant = ['<def>','<level>','<passion>']





substrings_to_remove = ["</def>","\n","<def>","<level>","<passion>","</level>","</passion>"]
pawn_subdict_keys = ["Level", "Passion"]
pawn_names_substrings = ['<nick>','</nick>']

pawn_traits_substrings = ['<allTraits>','</allTraits>']

health_traits_keys = ['<healthTracker>','</healthTracker>']

for i in pawn_names_substrings:
    pawn_names = [x.replace(i,'') for x in pawn_names]
pawn_names = [i.strip() for i in pawn_names]


def extract_single_values(value_strings, label="",debug=False):

    final_values = []

    for idx, (i, name) in enumerate(zip(colony_pawns_final, pawn_names)):
        # if len(i)<1000:
        # if name=='Lindsey':
        #     print(i)
        join = False
        # print(label,idx, name, len(i))
        # try:
        for idx2, j in enumerate(i):
            if value_strings[0] in j:
                final_values.append(j)
                if debug:
                    print(value_strings[0],idx,name)
                join=True
                break


            # if value_begin in j:
            #     value_begin_idx = idx2
            #
            # elif value_end in j:
            #     value_end_idx = idx2
        if join==False:
            if debug:
                print('NOJOIN',idx,name)
            final_values.append('0')

        final_values = [i.replace('\t','') for i in final_values]
        for x in value_strings:
            final_values = [i.replace(x,'') for i in final_values]
        final_values = [i.strip() for i in final_values]

    if debug:
        print('finalvals',final_values)

    assert len(final_values)==len(pawn_names),print("Warning! {} len does not equal pawn len.".format(label))

    #automatically add to pawn_dict
    for group_idx,(name,val) in enumerate(zip(pawn_names,final_values)):
        pawn_dict[name][label] = val

    return final_values



    # return extract_list



for idx,(i,name) in enumerate(zip(colony_pawns_final,pawn_names)):
    # if len(i)<1000:

    pawn_dict[name] = {}

    # print(idx,name,len(i))
    for idx2,j in enumerate(i):
        if skill_begin in j:
            skill_begin_idx = idx2
        elif skill_end in j:
            skill_end_idx = idx2

    pawn_skills = i[skill_begin_idx:skill_end_idx]
    pawn_skills = [i.replace('\t','') for i in pawn_skills]

    #Distill down to skill cat, skill and passion
    pawn_skills = [i for i in pawn_skills if any(w in i for w in skill_relevant)]

    groups = []
    #Group each into nested list, taking into account passions
    # for each in pawn_skills:
    #     if '<def>' in each:
    #         groups.append([])

    for idx,each in enumerate(pawn_skills):
        # print(idx,each)
        if '<def>' in each:
            try: #check for passion; if not, leave blank
                if '<passion>' in pawn_skills[idx+2]:
                    branch = [each,pawn_skills[idx+1],pawn_skills[idx+2]]
                else:
                    branch = [each,pawn_skills[idx+1]]
            except IndexError:
                try:
                    branch = [each,pawn_skills[idx+1]]
                except IndexError: #Correct for last IDX intellectuals with zero
                    # print('ERROR',idx,pawn,each)
                    branch = [each, '0']

            if len(branch)==2:
                branch.append('na')

            groups.append(branch)

        for x in substrings_to_remove:
            groups = [[j.replace(x,'') for j in i] for i in groups]

    #account for zero skill blanks
    for idx,each in enumerate(groups):
        for idx2,val in enumerate(each):
            if idx2==1:
                try:
                    groups[idx][idx2] = int(val)
                except ValueError:
                    groups[idx][idx2] = 0



        # print('groups',idx,name,groups)
    keys = [i.pop(0) for i in groups]
    # print('keys',keys)

    for group_idx,i in enumerate(groups):
        pawn_dict[name][keys[group_idx]] = {}
        for k,v in zip(pawn_subdict_keys,i):
            pawn_dict[name][keys[group_idx]][k] = v

##ADD NEW DICT K:V HERE##

#Colony join date
join_strings = ['<joinTick>','</joinTick>']
join_dates = extract_single_values(join_strings,label="Join date")

#Biological age
age_strings = ['<ageBiologicalTicks>','</ageBiologicalTicks>']
pawn_ages = extract_single_values(age_strings,label="Biological age")

for keys,values in pawn_dict.items():
    print(keys,values)
    print('')