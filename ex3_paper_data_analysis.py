import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt


path_data_paper = "C:/post_doc/data/data_paper_sampy"
sns.set_theme(style="darkgrid")

#
# dict_parm_to_curv = dict()
# total_time = 0.
# with open(path_data_paper + '/sims_output.csv', 'r') as f:
#     for i, line in enumerate(f):
#         if i == 0:
#             continue
#         data = line.replace('\n', '').split(';')
#         if i == 1:
#             base_case = np.array(list(map(int, data[5:])))
#             continue
#
#         total_time += float(data[4])
#
#         week_radius_level = (int(data[2]), float(data[0]), float(data[1]))
#         list_infected = []
#         for j, val in enumerate(data[5:]):
#             if val == '':
#                 list_infected.append(base_case[j])
#             else:
#                 list_infected.append(int(val))
#         time_series = np.array(list_infected)
#         if week_radius_level in dict_parm_to_curv:
#             dict_parm_to_curv[week_radius_level][0] += 1
#             dict_parm_to_curv[week_radius_level].append(time_series)
#         else:
#             dict_parm_to_curv[week_radius_level] = [1, time_series]
#
#
# list_df = []
# for key, val in dict_parm_to_curv.items():
#     df = pd.DataFrame()
#     timesteps = []
#     for time_series in val[1:]:
#         timesteps = timesteps + list(range(time_series.shape[0]))
#     all_val = np.hstack(val[1:])
#     df['timesteps'] = timesteps
#     df['nb_infected'] = all_val
#     df['radius'] = key[1]
#     df['level_percent'] = round(key[2] * 100)
#     df['week_vaccine'] = key[0]
#     list_df.append(df)
#
# final_df = pd.concat(list_df)
#
# final_df.to_csv(path_data_paper + '/dataframe_for_seaborn_visua.csv', sep=';')
final_df = pd.read_csv(path_data_paper + '/dataframe_for_seaborn_visua.csv', sep=';')

df_test = final_df[(final_df['week_vaccine'] == 32) & (final_df['radius'] == 15.) & (final_df['level_percent'] == 60)]

# print(df.head(20))
sns.relplot(x="timesteps", y="nb_infected", kind="line", data=df_test)#, hue='level_percent')
plt.show()



