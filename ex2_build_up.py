from sampy.agent.builtin_agent import BasicMammal
from sampy.graph.builtin_graph import SquareGridWithDiag
from constant_paper import ARR_WEEKLY_MORTALITY
import numpy as np
import matplotlib.pyplot as plt


folder_pictures = "C:/post_doc/data/data_paper_sampy/pictures/build_up_halves"
path_to_pop_csv = "C:/post_doc/data/data_paper_sampy/k10_pop.csv"
path_to_map = "C:/post_doc/data/data_paper_sampy/k_maps_arrays/map_k10.npy"

# create the landscape
my_graph = SquareGridWithDiag(shape=(100, 100))
map_2d = np.load(path_to_map)
my_graph.create_attribute_from_2d_array('K', map_2d)

# create the population object
agents = BasicMammal(graph=my_graph)
# create some agents
dict_new_agents = dict()
dict_new_agents['age'] = [52, 52, 52, 52, 52, 52, 52, 52, 52, 52]
dict_new_agents['gender'] = [0, 1, 0, 1, 0, 1, 0, 1, 0, 1]
dict_new_agents['territory'] = [4950 for _ in range(10)]
dict_new_agents['position'] = [4950 for _ in range(10)]
agents.add_agents(dict_new_agents)

list_pop_pic = []
nb_year_simu = 100
for i in range(nb_year_simu * 52 + 1):

    if i % 52 == 0:
        list_pop_pic.append(agents.count_pop_per_vertex(position_attribute='territory'))
        print('year', str(i // 52), ':', list_pop_pic[-1].sum())

    agents.tick()
    my_graph.tick()

    agents.kill_too_old(52 * 6 - 1)
    agents.natural_death_orm_methodology(ARR_WEEKLY_MORTALITY, ARR_WEEKLY_MORTALITY)
    agents.kill_children_whose_mother_is_dead(11)

    agents.mov_around_territory(0.5, condition=agents.df_population['age'] >= 11)

    if i % 52 == 15:
        agents.find_random_mate_on_position(1., position_attribute='territory')
    if i % 52 == 22:
        agents.create_offsprings_custom_prob(np.array([4, 5, 6, 7, 8, 9]), np.array([0.1, 0.2, 0.2, 0.2, 0.2, 0.1]))
    if i % 52 == 40:
        can_move = agents.df_population['age'] > 11
        agents.dispersion_with_varying_nb_of_steps(np.array([1, 2, 3, 4]), np.array([.25, .25, .25, .25]),
                                                   condition=can_move)

agents.save_population_to_csv(path_to_pop_csv)

# for i, val in enumerate(list_pop_pic):
#     plt.imshow(my_graph.convert_1d_array_to_2d_array(val), vmin=0, vmax=70)
#     plt.savefig(folder_pictures + '/' + str(i) + '.png', dpi=300)
#     plt.clf()
