from rimworld_main_040220 import pawn_dict
import universal_functions as uf
import universal_functions_matplotlib as ufm
import xlwings_functions as xlfunc
import pandas as pd


print('')
print('------------------DATA PROCESSING------------------------')
print('')

tick_year = 3200000

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
            pass
            # print('SKILL ERROR',pawn,idx,skill)


    total = sum(total)

    pawn_total_skills.append(total)

pawn_total_skills,all_pawns= list(zip(*sorted(zip(pawn_total_skills,all_pawns))))
for name,total in zip(all_pawns,pawn_total_skills):
    # print(name,total)
    pawn_dict[name]["Total skills"] = total

def excel_sheet_to_mappable_dict(excel_file,workbook_sheet,main_cat_key,mappable_key):
    raw_data = xlfunc.grab_data_from_excel(excel_file, enter_workbook_sheet=workbook_sheet)
    # raw_data = xlfunc.pre_process_data(raw_data,0)
    # print('raw data',raw_data)

    temp_headers_list = []
    for idx,i in enumerate(raw_data):
        if main_cat_key in i:
            main_cat_list = raw_data[idx][1:]
        if mappable_key in i:
            map_cat_list = raw_data[idx][1:]
        temp_headers_list.append(raw_data[idx][0])


    dictionary = {k:v for k,v in zip(main_cat_list,map_cat_list)}
    # print(dictionary)

    psychology_processed = []
    for keys,values in pawn_dict.items():
        branch = []
        for k,v in values['Psychology'].items():
            # print(k,v)
            if k not in temp_headers_list:
                if dictionary[k] == 'good':
                    branch.append(v[0])
                elif dictionary[k] == 'bad':
                    branch.append(v[0]*-1)
        branch = sum(branch)
        psychology_processed.append(branch)
        values['Psychology'][mappable_key] = branch

    # print('processed',psychology_processed)


psychology_theme_list = ['good_bad_theme','intelligence_theme','bravery_theme']

for theme in psychology_theme_list:
    excel_sheet_to_mappable_dict('dictionaries.xlsx',"Psychology traits",main_cat_key='trait',
                                                  mappable_key=theme)

# excel_sheet_to_mappable_dict('dictionaries.xlsx',"Psychology traits",main_cat_key='trait',
#                                               mappable_key='intelligence_theme')
# excel_sheet_to_mappable_dict('dictionaries.xlsx',"Psychology traits",main_cat_key='trait',
#                                               mappable_key='bravery_theme')

#All single line data
pawn_join_date = []
pawn_biological_age = []
pawn_total_skills = []
pawn_health = []
pawn_psychology = [[] for theme in psychology_theme_list]
# pawn_psychology_good = []
# pawn_psychology_intelligence = []
# pawn_psychology_bravery = []

for idx,pawn in enumerate(all_pawns):
    pawn_join_date.append(pawn_dict[pawn]["Join date"])
    pawn_biological_age.append(int(pawn_dict[pawn]["Biological age"]))
    pawn_total_skills.append(pawn_dict[pawn]["Total skills"])
    pawn_health.append(pawn_dict[pawn]["Health"])
    for idx_theme,theme in enumerate(psychology_theme_list):
        pawn_psychology[idx_theme].append(pawn_dict[pawn]['Psychology'][theme])

import datetime
today_date = datetime.datetime.today()
today_date = str(today_date)
today_date = today_date.split("-")
today_date = today_date[0],today_date[1],today_date[2]
today_date = "".join(today_date)
today_date = today_date.split(" ")
today_date = today_date[0]

#Make Pyschology dicts




print('post psych')
for keys,values in pawn_dict.items():
    print(keys,values)

radar_names = ['Michael','Dade','Gizmo','Hayhouse']

pawn_psychology_selected = []

print('pawnpsych',pawn_psychology)
print('psychology_theme_list',psychology_theme_list)

for pawn_name in radar_names:
    branch = []
    for idx,psych_data in enumerate(pawn_psychology):

        #Normalize the list since any meaningful comparison needs to take into account different max values
        pawn_psychology[idx] = uf.normalize_list_max(psych_data, inverse=False)

        for name_idx,(name,data) in enumerate(zip(all_pawns,psych_data)):
            if name==pawn_name:
                branch.append([data])
    pawn_psychology_selected.append(branch)

print('pawn_psychology_selected',pawn_psychology_selected)

for idx,(name,psych_data) in enumerate(zip(radar_names,pawn_psychology_selected)):
        # pawn_psychology_selected.append(psych_data)
        ufm.radar_chart_simple(psych_data, psychology_theme_list, value_labels=name)


print('pawn_health')
for i in pawn_health:
    print(i)

show_all = True

superman_list = list(zip(*pawn_psychology))
superman_list = [sum(i) for i in superman_list]

#Normalized values
superman_list_normalized = uf.normalize_list_max(superman_list,inverse=False)
pawn_total_skills_normalized = uf.normalize_list_max(pawn_total_skills,inverse=False)
pawn_health_normalized = uf.normalize_list_max(pawn_health,alt_inverse=True)
normalized_all = superman_list_normalized,pawn_total_skills_normalized,pawn_health_normalized

normalization_weights = [1,1,0]

normalized_all = list(zip(*normalized_all))

normalized_all = [[j*weight for j,weight in zip(i,normalization_weights)] for i in normalized_all]

print('normalized_all')
for val,pawn in zip(normalized_all,all_pawns):
    print(val,pawn)

normalized_all = [sum(i) for i in normalized_all]

for val,pawn in zip(normalized_all,all_pawns):
    print(val,pawn)


ufm.bar_chart_simple(normalized_all, all_pawns, "Overall Best Pawn" + " " + str(today_date),
                         using_dates=False, average_line=True, axis_font_size=16, show=True)

ufm.bar_chart_simple(superman_list, all_pawns, "Pawn Psychology_Superman Combined" + " " + str(today_date),
                         using_dates=False, average_line=True, axis_font_size=16, show=True)

for theme,psych in zip(psychology_theme_list,pawn_psychology):
    ufm.bar_chart_simple(psych, all_pawns, "Pawn Psychology_ {}".format(theme) + " " + str(today_date),
                         using_dates=False, average_line=True, axis_font_size=16, show=True)

if show_all:

    #Total skills
    ufm.bar_chart_simple(pawn_total_skills,all_pawns,"Pawn Total Skills"+" "+str(today_date), using_dates=False,
                         average_line=True,show=True)

    #Health distribution
    ufm.bar_chart_simple(pawn_health,all_pawns,"Pawn Health (higher = worse)"+" "+str(today_date), using_dates=False, divide_y_by = False,
                         average_line=True,show=True)

    #Age distribution
    ufm.bar_chart_simple(pawn_biological_age,all_pawns,"Pawn Biological Age"+" "+str(today_date), using_dates=False, divide_y_by = tick_year,
                         average_line=True,show=True)

    #Join vs skills
    ufm.simple_scatterplot(pawn_join_date,pawn_total_skills,data_labels=all_pawns,
                           xy_labels=["Join Date", "Total Skills"],fitline=True, divide_x_by = tick_year, show=True)

    #Age vs health
    ufm.simple_scatterplot(pawn_biological_age,pawn_health,data_labels=all_pawns,
                           xy_labels=["Age", "Health"],fitline=True, divide_x_by = tick_year, show=True)


# ufm.heatmap()