import itertools
import numpy as np

from cpm import *


class BurgessProcedure:

	def __init__(self, node_matrix=[]):
		self.node_matrix = node_matrix
		self.critical_activities = [] #List Or Array#
		self.critical_activities_length = 0
		self.nonCritical_activities = {}
		self.delay_activity_resluts = {}
		self.delay_activity_r = {}
		self.delay_activity_r2 = {} #Dictionary Or Map#
		self.project_duration = 0
		self.nonCritical_activities_length = 0
		self.optimal_time_resource_matrix = None
		self.optimal_total_R = int(1e9)
		self.optimal_total_R_square = int(1e9)
		# print('- Node_Matrix -\n', self.node_matrix)
	

	def print_burgess_schedule_details(self):
		print("---------------------------------")
		print("---------------------------------")
		print("---------------------------------")
		print("Optimal Result", self.optimal_total_R_square)
		print("---------------------------------")
		print("Name\tOS\tOF\tShift \tR^2 \tSUM(R)\tSUM(R^2)")
		for node in self.node_matrix:
			if node["critical"] == True:
				print(node["name"], "\t", node["OS"], "\t", node["OF"], "\t", int(node["OS"])-int(node["ES"]))
			else:
				print(node["name"], "\t", node["OS"], "\t", node["OF"], "\t", int(node["OS"])-int(node["ES"]),"\t",
				self.delay_activity_resluts[node["name"]], "\t", self.delay_activity_r[node["name"]], "\t", self.delay_activity_r2[node["name"]])


	def initialize_OS_OF(self):
		for node in self.node_matrix:
			node["OS"] = node["ES"] 
			node["OF"] = node["EF"]


	def separate_critical_activities(self):
		for node in self.node_matrix:
			if node["critical"] == True:
				self.project_duration += int(node["duration"])
				self.critical_activities.append(node)


	def generate_time_resource_matrix(self):
		allotted_resources_for_cp = np.zeros(self.project_duration + 1, dtype=int)

		for ca in self.critical_activities:
			for ind, value in enumerate(allotted_resources_for_cp):
				if ind > int(ca["ES"]) and ind <= int(ca["EF"]):
					allotted_resources_for_cp[ind] = value + int(ca["resource"])              
		# allotted_resources_for_cp.shape = (1, self.project_duration + 1)
	
		# flexible_resource_allocation_matrix = np.zeros((1, self.project_duration + 1), dtype=int)
		
		# time_resource_matrix = np.concatenate((allotted_resources_for_cp, flexible_resource_allocation_matrix))
		# print(time_resource_matrix)
		return allotted_resources_for_cp

	def calculate_total_resources(self, node, allotted_resources_for_cp):
		allotted_resources = np.copy(allotted_resources_for_cp)
		for a in self.node_matrix:
			if a["critical"] == False and a["name"] != node["name"]:
				for ind, value in enumerate(allotted_resources):
					if ind > int(a["OS"]) and ind <= int(a["OF"]):
						allotted_resources[ind] = value + int(a["resource"]) 
		return allotted_resources

	def is_all_node_moved(self):
		moved = True
		for node in self.node_matrix:
			if node["critical"] == False:
				if int(node["ES"]) == int(node["OS"]):
					moved = False
		return moved

	def burgess_scheduler1(self, allotted_resources_for_cp):
		sorted_node_matrix = sorted(self.node_matrix, key = lambda i: int(i['ES']), reverse=True)
		while True:
			min_sum = int(1e9)
			for node in sorted_node_matrix:
				if node["critical"] == False:
					# print("node", node, "\n")
					des_os = int(1e9)
					des_nodes = node["descendant"]
					for desN in des_nodes:
						des_node = list(filter(lambda key: key['name'] == desN, self.node_matrix))
						# print(des_node, "\n")
						if des_node[0]['OS'] < des_os:
							des_os = des_node[0]['OS']
							# print(des_os, "\n")

					allotted_resources = self.calculate_total_resources(node, allotted_resources_for_cp)
					# print(allotted_resources)
					self.delay_activity_resluts[node["name"]] = int(1e9)
					for i in range(1, node["slack"]+1):
						if(int(node["EF"])+i > des_os):
							break
						temp_alloted_resource = np.copy(allotted_resources)
						sum = 0
						for ind, value in enumerate(temp_alloted_resource):
							if ind > int(node["ES"])+i and ind <= int(node["EF"])+i:
								temp_alloted_resource[ind] = value + int(node["resource"])

						square_resources = [r*r for r in temp_alloted_resource]
						sum = np.sum(square_resources)
						# print("Hi", node['name'], i, "\n")
						# print(self.delay_activity_resluts[node["name"]], sum, "\n")
						if sum < self.delay_activity_resluts[node["name"]]:
							self.delay_activity_resluts[node["name"]] = sum
							self.delay_activity_r[node["name"]] = temp_alloted_resource
							self.delay_activity_r2[node["name"]] = square_resources
							node["OS"] = int(node["ES"]) + i        
							node["OF"] = int(node["EF"]) + i
					if self.delay_activity_resluts[node["name"]] < min_sum and self.is_all_node_moved():
						min_sum = self.delay_activity_resluts[node["name"]]
			if min_sum < self.optimal_total_R_square:
				self.optimal_total_R_square = min_sum
			else:
				break  

	def burgess_scheduler2(self, allotted_resources_for_cp):
		sorted_node_matrix = sorted(self.node_matrix, key = lambda i: int(i['ES']), reverse=True)
		while True:
			min_sum = int(1e9)
			for node in sorted_node_matrix:
				if node["critical"] == False:
					# print("node", node, "\n")
					des_os = int(1e9)
					des_nodes = node["descendant"]
					for desN in des_nodes:
						des_node = list(filter(lambda key: key['name'] == desN, self.node_matrix))
						# print(des_node, "\n")
						if des_node[0]['OS'] < des_os:
							des_os = des_node[0]['OS']
							# print(des_os, "\n")

					allotted_resources = self.calculate_total_resources(node, allotted_resources_for_cp)
					# print(allotted_resources)
					self.delay_activity_resluts[node["name"]] = int(1e9)
					for i in range(0, node["slack"]+1):
						if(int(node["EF"])+i > des_os):
							break
						temp_alloted_resource = np.copy(allotted_resources)
						sum = 0
						for ind, value in enumerate(temp_alloted_resource):
							if ind > int(node["ES"])+i and ind <= int(node["EF"])+i:
								temp_alloted_resource[ind] = value + int(node["resource"])

						square_resources = [r*r for r in temp_alloted_resource]
						sum = np.sum(square_resources)
						# print("Hi", node['name'], i, "\n")
						# print(self.delay_activity_resluts[node["name"]], sum, "\n")
						if sum < self.delay_activity_resluts[node["name"]]:
							self.delay_activity_resluts[node["name"]] = sum
							self.delay_activity_r[node["name"]] = temp_alloted_resource
							self.delay_activity_r2[node["name"]] = square_resources
							node["OS"] = int(node["ES"]) + i        
							node["OF"] = int(node["EF"]) + i
					if self.delay_activity_resluts[node["name"]] < min_sum:
						min_sum = self.delay_activity_resluts[node["name"]]
			# print("Min Sum", min_sum)            
			# self.print_burgess_schedule_details()
			if min_sum < self.optimal_total_R_square:
				self.optimal_total_R_square = min_sum
			else:
				break   


	def prepare_burgess_response(self):
		R_by_time = None
		R2_by_time = None
		total_R = 0
		total_R2 = int(self.optimal_total_R_square)
		node_matrix = self.node_matrix

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

		for node in self.node_matrix:
			if node["critical"] == False:               
				R_by_time = np.array(self.delay_activity_r[node["name"]], dtype=int)
				R2_by_time = np.array(self.delay_activity_r2[node["name"]], dtype=int)
				total_R = np.sum(R_by_time)
				break
		# R_by_time = R_by_time.astype('int')
		return {"node_matrix": node_matrix, "R_by_time": R_by_time.tolist(), "R2_by_time": R2_by_time.tolist(), 
			"optimal_total_R": int(total_R), "optimal_total_R_square": int(total_R2)}


	def estimate_optimal_schedule_burgess1(self):
		self.initialize_OS_OF()
		self.separate_critical_activities()
		allotted_resources_for_cp = self.generate_time_resource_matrix()
		self.burgess_scheduler1(allotted_resources_for_cp)
		self.print_burgess_schedule_details()
		# print(self.prepare_burgess_response())
		return self.prepare_burgess_response()

	def estimate_optimal_schedule_burgess2(self):
		self.initialize_OS_OF()
		self.separate_critical_activities()
		allotted_resources_for_cp = self.generate_time_resource_matrix()
		self.burgess_scheduler2(allotted_resources_for_cp)
		self.print_burgess_schedule_details()
		
		return self.prepare_burgess_response()
		
		