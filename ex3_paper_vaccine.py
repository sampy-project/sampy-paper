from sampy.agent.builtin_agent import BasicMammal
from sampy.graph.builtin_graph import SquareGridWithDiag
from sampy.disease.single_species.builtin_disease import ContactCustomProbTransitionPermanentImmunity
from sampy.intervention.built_in_interventions import BasicVaccination
from sampy.data_processing.csv_manager import CsvManager

from constant_paper import ARR_WEEKLY_MORTALITY, ARR_NB_WEEK_INF, ARR_PROB_WEEK_INF
from misc_paper import create_vaccine_map

import numpy as np
import time
import multiprocessing as mlp

# 0) Parameter(s)
nb_cores = 64
rng_seed = 1789


# 1) definition of the worker that will be launched in parallel
def worker(id_proc, nb_proc, seed):

    np.random.seed(seed + id_proc)
    nb_year_simu = 3

    path_output_csv = 'output/results_vaccine_ex_paper_' + str(id_proc) + '.csv'
    with open(path_output_csv, 'a') as csv_output:
        csv_output.write("radius;level;week;nb_vaccinated;time;" +
                         ';'.join(['nb_inf_week_' + str(i) for i in range(nb_year_simu * 52 + 1)]) + '\n')

    # 2) Manage csv param
    dict_types = {'center_x': int,
                  'center_y': int,
                  'radius': float,
                  'level': float,
                  'week_start': int,
                  'id_sim': int}
    csv_manager = CsvManager("input/csv_param_paper.csv", ';',
                             dict_types=dict_types,
                             nb_cores=nb_proc,
                             id_process=id_proc)

    # the graph being static in this sim, we start by creating it
    my_graph = SquareGridWithDiag(shape=(100, 100))
    my_graph.create_vertex_attribute('K', 10.)

    # get first batch of parameter and start studying
    param = csv_manager.get_parameters()
    while param is not None:

        str_output = str(param.radius) + ';' + str(param.level) + ';' + str(param.week_start)

        start_time = time.time()

        # create the population object
        agents = BasicMammal(graph=my_graph)
        disease = ContactCustomProbTransitionPermanentImmunity(host=agents, disease_name='disease')
        intervention = BasicVaccination(disease=disease, duration_vaccine=156)
        agents.load_population_from_csv('input/pop_for_vaccine_demo_week_' + str(param.week_start) + '.csv')

        dict_vaccine = create_vaccine_map((100, 100), (param.center_x, param.center_y), param.radius, param.level)
        can_be_vaccinated = ~agents.df_population['imm_disease'] & \
                            ~agents.df_population['inf_disease'] & \
                            ~agents.df_population['con_disease']
        intervention.apply_vaccine_from_dict(my_graph, dict_vaccine, condition=can_be_vaccinated)

        str_output = str_output + ';' + str(agents.df_population['vaccinated_disease'].sum())

        total_nb_inf = []
        for i in range(nb_year_simu * 52 + 1):
            if i < param.week_start:
                total_nb_inf.append('')
                continue

            total_nb_inf.append(str((agents.df_population['inf_disease'] | agents.df_population['con_disease']).sum()))

            agents.tick()
            my_graph.tick()
            disease.tick()
            intervention.update_vaccine_status()

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
                agents.create_offsprings_custom_prob(np.array([4, 5, 6, 7, 8, 9]),
                                                     np.array([0.1, 0.2, 0.2, 0.2, 0.2, 0.1]))
            if i % 52 == 40:
                can_move = agents.df_population['age'] > 11
                agents.dispersion_with_varying_nb_of_steps(np.array([1, 2, 3, 4]), np.array([.25, .25, .25, .25]),
                                                           condition=can_move)

        str_output = str_output + ';' + str(time.time() - start_time) + ';' + ';'.join(total_nb_inf) + '\n'
        with open(path_output_csv, 'a') as csv_output:
            csv_output.write(str_output)

        # get next batch of parameters, if it exists
        param = csv_manager.get_parameters()


if __name__ == '__main__':

    list_jobs = []
    for id_process in range(nb_cores):
        p = mlp.Process(target=worker, args=(id_process, nb_cores, rng_seed))
        list_jobs.append(p)
        list_jobs[-1].start()

    for p in list_jobs:
        p.join()
