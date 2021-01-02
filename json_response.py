{
    "burgess1":
    {
       "node_matrix":
        "optimal_R_by_time":    # time-resource-array eta
        "optimal_R2_by_time":   # time-resource-array eta
        "total_R":
        "total_R_square":
    },
    "burgess2":
    {
       "node_matrix":
        "optimal_R_by_time":    # time-resource-array eta
        "optimal_R2_by_time":   # time-resource-array eta
        "total_R":
        "total_R_square":
    },
    "estimated":
    {
       "node_matrix": [{'id': 11, 'name': 'K', 'predecessor': ['J'], 'duration': '3', 'resource': '5', 'descendant': [], 'slack': 0, 'critical': True, 'ES': 15, 'LS': 15, 'EF': 18, 'LF': 18, 'OS': 0, 'OF': 0, 'FP': True, 'BP': True}, 
            {'id': 8, 'name': 'H', 'predecessor': ['F', 'G'], 'duration': '5', 'resource': '2', 'descendant': [], 'slack': 4, 'critical': False, 'ES': 9, 'LS': 13, 'EF': 14, 'LF': 18, 'OS': 0, 'OF': 0, 'FP': True, 'BP': True}, 
            {'id': 1, 'name': 'A', 'predecessor': ['-'], 'duration': '3', 'resource': '3', 'descendant': ['C', 'D'], 'slack': 0, 'critical': True, 'ES': 0, 'LS': 0, 'EF': '3', 'LF': 3, 'OS': 0, 'OF': 0, 'FP': True, 'BP': True}, 
            {'id': 4, 'name': 'D', 'predecessor': ['A'], 'duration': '2', 'resource': '4', 'descendant': ['E', 'F'], 'slack': 5, 'critical': False, 'ES': '3', 'LS': 8, 'EF': 5, 'LF': 10, 'OS': 0, 'OF': 0, 'FP': True, 'BP': True}, 
            {'id': 2, 'name': 'B', 'predecessor': ['-'], 'duration': '5', 'resource': '2', 'descendant': ['G'], 'slack': 4, 'critical': False, 'ES': 0, 'LS': 4, 'EF': '5', 'LF': 9, 'OS': 0, 'OF': 0, 'FP': True, 'BP': True}, 
            {'id': 7, 'name': 'G', 'predecessor': ['B'], 'duration': '4', 'resource': '3', 'descendant': ['H'], 'slack': 4, 'critical': False, 'ES': '5', 'LS': 9, 'EF': 9, 'LF': 13, 'OS': 0, 'OF': 0, 'FP': True, 'BP': True}, 
            {'id': 6, 'name': 'F', 'predecessor': ['D'], 'duration': '3', 'resource': '1', 'descendant': ['H'], 'slack': 5, 'critical': False, 'ES': 5, 'LS': 10, 'EF': 8, 'LF': 13, 'OS': 0, 'OF': 0, 'FP': True, 'BP': True}, 
            {'id': 3, 'name': 'C', 'predecessor': ['A'], 'duration': '6', 'resource': '3', 'descendant': ['I'], 'slack': 0, 'critical': True, 'ES': '3', 'LS': 3, 'EF': 9, 'LF': 9, 'OS': 0, 'OF': 0, 'FP': True, 'BP': True}, 
            {'id': 9, 'name': 'I', 'predecessor': ['C'], 'duration': '4', 'resource': '3', 'descendant': ['J'], 'slack': 0, 'critical': True, 'ES': 9, 'LS': 9, 'EF': 13, 'LF': 13, 'OS': 0, 'OF': 0, 'FP': True, 'BP': True}, 
            {'id': 5, 'name': 'E', 'predecessor': ['D'], 'duration': '3', 'resource': '2', 'descendant': ['J'], 'slack': 5, 'critical': False, 'ES': 5, 'LS': 10, 'EF': 8, 'LF': 13, 'OS': 0, 'OF': 0, 'FP': True, 'BP': True}, 
            {'id': 10, 'name': 'J', 'predecessor': ['E', 'I'], 'duration': '2', 'resource': '4', 'descendant': ['K'], 'slack': 0, 'critical': True, 'ES': 13, 'LS': 13, 'EF': 15, 'LF': 15, 'OS': 0, 'OF': 0, 'FP': True, 'BP': True}]
        "optimal_R_by_time":  [0, 5, 5, 5, 5, 9, 7, 6, 6, 6, 6, 6, 6, 6, 6, 6, 7, 7, 7],     # actual data starts from index:1
        "optimal_R2_by_time": [ 0, 25, 25, 25, 25, 81, 49, 36, 36, 36, 36, 36, 36, 36, 36, 36, 49, 49, 49],      # actual data starts from index:1
        "total_R": 111,
        "total_R_square": 701,
    }
}