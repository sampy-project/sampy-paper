from sampy.agent.builtin_agent import BasicMammal
from sampy.graph.builtin_graph import SquareGridWithDiag
from sampy.disease.single_species.builtin_disease import ContactCustomProbTransitionPermanentImmunity
from constant_paper import ARR_WEEKLY_MORTALITY, ARR_NB_WEEK_INF, ARR_PROB_WEEK_INF
import numpy as np
import matplotlib.pyplot as plt


folder_pictures = "C:/post_doc/data/data_paper_sampy/pictures/disease_noise"
path_to_pop_csv = "C:/post_doc/data/data_paper_sampy/noise_pop.csv"
path_to_map = "C:/post_doc/data/data_paper_sampy/k_maps_arrays/map_noise.npy"

# create the landscape
my_graph = SquareGridWithDiag(shape=(100, 100))
map_2d = np.load(path_to_map)
my_graph.create_attribute_from_2d_array('K', map_2d)

# create the population object
agents = BasicMammal(graph=my_graph)
agents.load_population_from_csv(path_to_pop_csv)

# disease
disease = ContactCustomProbTransitionPermanentImmunity(disease_name='disease', host=agents)
arr_new_contamination = disease.contaminate_vertices([(50, 50), (50, 51)], .5)
disease.initialize_counters_of_newly_infected(arr_new_contamination, ARR_NB_WEEK_INF, ARR_PROB_WEEK_INF)

list_disease_pic = []
nb_year_simu = 10
for i in range(nb_year_simu * 52 + 1):

    list_disease_pic.append(agents.count_pop_per_vertex(position_attribute='territory',
                                                        condition=agents.df_population['inf_disease'] |
                                                                  agents.df_population['con_disease']))

    if i % 52 == 0:
        print('year', str(i // 52), ':', agents.df_population.nb_rows)

    agents.tick()
    my_graph.tick()
    disease.tick()

    agents.kill_too_old(52 * 6 - 1)
    agents.natural_death_orm_methodology(ARR_WEEKLY_MORTALITY, ARR_WEEKLY_MORTALITY)
    agents.kill_children_whose_mother_is_dead(11)

    agents.mov_around_territory(0.5, condition=agents.df_population['age'] >= 11)
    arr_new_infected = disease.contact_contagion(0.1, return_arr_new_infected=True)
    disease.initialize_counters_of_newly_infected(arr_new_infected, ARR_NB_WEEK_INF, ARR_PROB_WEEK_INF)
    disease.transition_between_states('con', 'death', proba_death=0.8)
    disease.transition_between_states('con', 'imm')
    disease.transition_between_states('inf', 'con',
                                      arr_nb_timestep=np.array([1, 2]),
                                      arr_prob_nb_timestep=np.array([.5, .5]))

    if i % 52 == 15:
        agents.find_random_mate_on_position(1., position_attribute='territory')
    if i % 52 == 22:
        agents.create_offsprings_custom_prob(np.array([4, 5, 6, 7, 8, 9]), np.array([0.1, 0.2, 0.2, 0.2, 0.2, 0.1]))
    if i % 52 == 40:
        can_move = agents.df_population['age'] > 11
        agents.dispersion_with_varying_nb_of_steps(np.array([1, 2, 3, 4]), np.array([.25, .25, .25, .25]),
                                                   condition=can_move)

for i, val in enumerate(list_disease_pic):
    plt.imshow(my_graph.convert_1d_array_to_2d_array(val), vmin=0, vmax=5)
    plt.savefig(folder_pictures + '/' + str(i) + '.png', dpi=300)
    plt.clf()
