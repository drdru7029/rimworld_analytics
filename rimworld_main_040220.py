import universal_functions as uf
import os
from itertools import groupby, chain


#MAIN DEFINITIONS

citiesout_path = r"D:\Google Drive\Games Archives\Rimworld\Save backups\Anhatia Accord (Permadeath)_new.txt"
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
# end_demarker = '<medCare>Best</medCare>'
end_demarker = '<abilityDataAbilityUser.GenericCompAbilityUser>'
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


print([len(i) for i in colony_pawns_final])
print(len(colony_pawns_final))


pawn_dict = {}
skill_begin = '<skills>'
skill_end = '</skills>'
skills_relevant = ['<def>', '<level>', '<passion>']





substrings_to_remove = ["</def>", "\n", "<def>", "<level>", "<passion>", "</level>", "</passion>",
                        '<painFactor>','</painFactor>','<rawRating>','</rawRating>']
skill_subdict_keys = ["Level", "Passion"]
pawn_names_substrings = ['<nick>','</nick>']

health_traits_keys = []
health_begin = '<healthTracker>'
health_end = '</healthTracker>'
health_relevant = ['<painFactor>']

#Psychology
psych_begin = '<psyche>'
psych_end = '</psyche>'
psych_relevant = ['<def>', '<rawRating>']

# '<isPermanent>', ,'<severity>'
for i in pawn_names_substrings:
    pawn_names = [x.replace(i,'') for x in pawn_names]
pawn_names = [i.strip() for i in pawn_names]

for idx, (i, name) in enumerate(zip(colony_pawns_final, pawn_names)):
    pawn_dict[name] = {}

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
pawns_to_remove = []
def extract_chain_values(value_begin,value_end,relevant_list,label,subdict_keys = [],subdict=False):
    for idx, (i, name) in enumerate(zip(colony_pawns_final, pawn_names)):
        # if len(i)<1000:

        # if name not in pawn_dict.keys():
        #     pawn_dict[name] = {}
        if subdict:
            pawn_dict[name][label] = {}

        # print(idx,name,len(i))
        for idx2, j in enumerate(i):
            # print('test',j)
            # try:
            if value_begin in j:
                value_begin_idx = idx2
            elif value_end in j:
                value_end_idx = idx2
            # except TypeError:
                # print('error',value_begin,value_end)

        values_list = i[value_begin_idx:value_end_idx]
        values_list = [i.replace('\t', '') for i in values_list]

        # Distill down to skill cat, skill and passion
        values_list = [i for i in values_list if any(w in i for w in relevant_list)]

        value_groups = []

        for idx, each in enumerate(values_list):
            # print('each',idx,each)
            if label=="Skills":
                # print('check', name, each)
                if '<def>' in each:
                    try:  # check for passion; if not, leave blank
                        if '<passion>' in values_list[idx + 2]:
                            branch = [each, values_list[idx + 1], values_list[idx + 2]]
                        else:
                            branch = [each, values_list[idx + 1]]
                    except IndexError:
                        try:
                            branch = [each, values_list[idx + 1]]
                        except IndexError:  # Correct for last IDX intellectuals with zero
                            # print('ERROR',idx,pawn,each)
                            branch = [each, '0']

                    if len(branch) == 2:
                        branch.append('na')

                    # value_groups.append(branch)

            elif label=="Health":
                # print('check',name,each)
                if health_relevant[0] in each:
                    branch = [each]
            elif label=='Psychology':
                # print('check',name,each)
                if '<def>' in each:
                    # print('check', name, each, values_list[idx+1])
                    try:
                        branch = [each,values_list[idx+1]]
                    except IndexError:
                        branch = [each,'0']
                        pawns_to_remove.append(name)
                    # print('TESTBRANCH', name,branch)


            value_groups.append(branch)


            for x in substrings_to_remove:
                value_groups = [[j.replace(x, '') for j in i] for i in value_groups]
            # print('valuegroups',value_groups)

        if label == 'Skills':
            # account for zero skill blanks
            for idx, each in enumerate(value_groups):
                for idx2, val in enumerate(each):
                    if idx2 == 1:
                        try:
                            value_groups[idx][idx2] = int(val)
                        except ValueError:
                            value_groups[idx][idx2] = 0
            # print('valgroups',value_groups)
            keys = [i.pop(0) for i in value_groups]

            # print('keys',keys)


        elif label=='Health':
            value_groups = list(uf.flatten(value_groups))
            value_groups = [float(i) for i in value_groups]
            value_groups = [sum(value_groups)]

            keys = [label]

            # print('value_groups',idx,name,value_groups)

        # print('keys',keys)

        else:
            # print('psychvalue_groups', idx, name, value_groups)
            for idx, each in enumerate(value_groups):
                for idx2, val in enumerate(each):
                    if idx2 == 1:
                        # print('TESTTEST',name,value_groups[idx][idx2])
                        try:
                            value_groups[idx][idx2] = float(val)
                        except ValueError:
                            value_groups[idx][idx2] = 0
            # print('valgroups',value_groups)
            keys = [i.pop(0) for i in value_groups]


            # print('valuegroups',value_groups)



        for group_idx, i in enumerate(value_groups):
            if len(subdict_keys)>0:
                pawn_dict[name][keys[group_idx]] = {}
                for k, v in zip(subdict_keys, i):
                    pawn_dict[name][keys[group_idx]][k] = v
            else:

                if subdict: #Places values in a subdictionary
                    pawn_dict[name][label][keys[group_idx]] = value_groups[group_idx]
                else:
                    pawn_dict[name][keys[group_idx]] = value_groups[group_idx]



extract_chain_values(skill_begin, skill_end, skills_relevant, "Skills", subdict_keys= skill_subdict_keys)
extract_chain_values(health_begin,health_end,health_relevant,"Health")
extract_chain_values(psych_begin,psych_end,psych_relevant,"Psychology",subdict=True)

pawns_to_remove = list(set(pawns_to_remove))

##ADD NEW DICT K:V HERE##

#Colony join date
join_strings = ['<joinTick>','</joinTick>']
join_dates = extract_single_values(join_strings,label="Join date")

#Biological age
age_strings = ['<ageBiologicalTicks>','</ageBiologicalTicks>']
pawn_ages = extract_single_values(age_strings,label="Biological age")

print('MAIN PAWN DICT')
for pawn in pawns_to_remove:
    print('Notice: removing {} from dictionary as some key:value pairs failed.'.format(pawn))
    del pawn_dict[pawn]

for keys,values in pawn_dict.items():
    if keys in pawns_to_remove:
        del pawn_dict[keys]
        # break
    print(keys,values)
    print('')

print('')
print('----------------END MAIN--------------------')
print('')