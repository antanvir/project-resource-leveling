import itertools
import numpy as np

from cpm import *


class EstimatedResourceSmoothing:

    def __init__(self, node_matrix=[]):
        self.node_matrix = node_matrix
        self.critical_activities = []
        self.critical_activities_length = 0
        self.nonCritical_activities = {}
        self.project_duration = 0
        self.nonCritical_activities_length = 0
        self.optimal_time_resource_matrix = None
        self.R_by_time = []
        self.R2_by_time = []
        self.optimal_total_R = int(1e9)
        self.optimal_total_R_square = int(1e9)
        # print('- Node_Matrix -\n', self.node_matrix)
    


    def print_estimate_schedule_details(self):
        print("\n--------------------------------\n")
        # print("Optimal Time-Resource Matrix")
        # print(self.optimal_time_resource_matrix)
        print("\nTotal R: ", self.optimal_total_R)
        print(self.R_by_time)
        print("Total R-square: ", self.optimal_total_R_square)
        print(self.R2_by_time)
        print("Name\tOS\tOF\tResource  Slack")
        for node in self.node_matrix:
            if node["critical"] == True:
                print(node["name"], "\t", node["ES"], "\t", node["EF"], "\t", node["resource"], "\t", node["slack"])
            else:
                print(node["name"], "\t", node["OS"], "\t", node["OF"], "\t", node["resource"], "\t", node["slack"])



    def separate_critical_activities(self):
        for ind, node in enumerate(self.node_matrix):
            if node["critical"] == True:
                self.project_duration += int(node["duration"])
                self.critical_activities.append(node)
                self.node_matrix[ind]["OS"] = node["ES"]
                self.node_matrix[ind]["OF"] = node["EF"] 



    def generate_time_resource_matrix(self):
        allotted_resources_for_cp = np.zeros(self.project_duration + 1, dtype=int)

        for ca in self.critical_activities:
            for ind, value in enumerate(allotted_resources_for_cp):
                if ind > int(ca["ES"]) and ind <= int(ca["EF"]):
                    allotted_resources_for_cp[ind] = value + int(ca["resource"])              
        allotted_resources_for_cp.shape = (1, self.project_duration + 1)
    
        flexible_resource_allocation_matrix = np.zeros((1, self.project_duration + 1), dtype=int)
        time_resource_matrix = np.concatenate((allotted_resources_for_cp, flexible_resource_allocation_matrix))
        # print(time_resource_matrix)
        return time_resource_matrix



    def update_optimal_start_and_finish_time(self, comb_choice, pos_in_combination_and_node_matrix_ind_mapping):
        for i, shift in enumerate(comb_choice):
            node_matrix_index = pos_in_combination_and_node_matrix_ind_mapping[i]
            es, duration = int(self.node_matrix[node_matrix_index]["ES"]), int(self.node_matrix[node_matrix_index]["duration"])
            self.node_matrix[node_matrix_index]["OS"] = es + int(shift) 
            self.node_matrix[node_matrix_index]["OF"] = es + int(shift) + duration




    def check_for_optimality(self, time_resource_matrix, comb_choice, pos_in_combination_and_node_matrix_ind_mapping):
        total_R_through_time = np.sum(time_resource_matrix, 0)
        total_R_square_through_time = [ r*r for r in total_R_through_time ]
        if np.sum(total_R_square_through_time) < self.optimal_total_R_square:
            self.optimal_total_R_square = np.sum(total_R_square_through_time)
            self.optimal_total_R = np.sum(total_R_through_time)
            self.optimal_time_resource_matrix = np.copy(time_resource_matrix)
            self.R_by_time = np.copy(total_R_through_time)
            self.R2_by_time = np.copy(total_R_square_through_time)
            self.update_optimal_start_and_finish_time(comb_choice, pos_in_combination_and_node_matrix_ind_mapping)




    def check_for_valid_combinations(self, combinations, node_name_and_pos_in_combination_map, pos_in_combination_and_node_matrix_ind_mapping):
        invalid_combo = np.array([])
        combinations = np.array(combinations)
        # print(combinations.shape)
        for ind, cur_node in enumerate(self.node_matrix):
            if cur_node["critical"] == False:
                invalid = []
                cur_node_pos = node_name_and_pos_in_combination_map[cur_node["name"]]
                predecessors_indices_in_comb = [ node_name_and_pos_in_combination_map[name] for name in cur_node["predecessor"] 
                                        if name in node_name_and_pos_in_combination_map.keys() ]
                # print(cur_node["name"], " ", cur_node["predecessor"], " ", predecessors_indices_in_comb)
                for pred_ind in predecessors_indices_in_comb:
                    pred_node = self.node_matrix[ pos_in_combination_and_node_matrix_ind_mapping[pred_ind] ]
                    es_cur_node, ef_pred_node =  int(cur_node["ES"]), int(pred_node["EF"])
                    invalid = np.where(es_cur_node + combinations[:, cur_node_pos] < ef_pred_node + combinations[:, pred_ind])
                    invalid_combo = np.append(invalid_combo, np.unique(invalid))
                    invalid_combo = np.unique(invalid_combo)
        combinations = np.delete(combinations, invalid_combo.astype(int), axis=0)
        return combinations.tolist()

                


    def estimated_resource_scheduler(self, time_resource_matrix):
        combinations = []
        pos_in_combination_and_node_matrix_ind_mapping = {}
        node_name_and_pos_in_combination_map = {}
        for index, node in enumerate(self.node_matrix):
            if node["critical"] == False:
                schedule_options_for_this_node = np.arange(int(node["slack"]) + 1, dtype=int)
                pos_in_combination_and_node_matrix_ind_mapping[len(combinations)] = index
                node_name_and_pos_in_combination_map[node["name"]] = len(combinations)
                combinations.append(schedule_options_for_this_node)
        # print("== Slack options for non-critical activities ==\n", combinations)
        combinations = list(itertools.product(*combinations))
        combinations = self.check_for_valid_combinations(combinations, 
                        node_name_and_pos_in_combination_map, pos_in_combination_and_node_matrix_ind_mapping)     
        # ======  2nd Choice of Implementation --> LET'S SEE ======== #
        for comb_choice in combinations:
            for i, shift in enumerate(comb_choice):
                node = self.node_matrix[ pos_in_combination_and_node_matrix_ind_mapping[i] ]
                es, duration, lf = int(node["ES"]), int(node["duration"]), int(node["LF"])
                for index in range(es+1, lf+1):
                    if index > es + int(shift) and index <= es + int(shift) + duration:
                        time_resource_matrix[1][index] += int(node["resource"])
            self.check_for_optimality(time_resource_matrix, comb_choice, pos_in_combination_and_node_matrix_ind_mapping)
            time_resource_matrix[1] = np.zeros(self.project_duration + 1, dtype=int)
        



    def estimate_optimal_schedule(self):
        self.separate_critical_activities()
        time_resource_matrix = self.generate_time_resource_matrix()
        self.estimated_resource_scheduler(time_resource_matrix)
        node_matrix = []
        for i, node in enumerate(self.node_matrix):
            single_node = {}
            single_node["ES"] = node["ES"]
            single_node["OS"] = node["OS"]
            single_node["OF"] = node["OF"]
            single_node["LF"] = node["LF"]
            single_node["name"] = node["name"]
            single_node["resource"] = node["resource"]
            node_matrix.append(single_node)


        R_by_time = self.R_by_time.tolist()
        R2_by_time = self.R2_by_time.tolist()
        optimal_total_R = int(self.optimal_total_R)
        optimal_total_R_square = int(self.optimal_total_R_square)
        # print(optimal_total_R_square)
        self.print_estimate_schedule_details()
        return {"node_matrix": node_matrix , "R_by_time": R_by_time, "R2_by_time": R2_by_time, 
                    "optimal_total_R": optimal_total_R, "optimal_total_R_square": optimal_total_R_square}
        

