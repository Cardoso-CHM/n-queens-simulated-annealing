from math import exp
import time
import random
from copy import deepcopy

def create_board(n):
    board = {}
    random_values = list(range(n))
    random.shuffle(random_values)
    
    for i,j in enumerate(list(range(n))):
        board[j] = random_values[i]
    
    return board

def display(board):
    size = len(board)
    print('Displaying board of size:', size)
    if(size <= 30):
        for i in range(len(board)):
            for j in range(len(board)):
                if board[j] == i:
                    print('♕ ', end="")
                else:
                    print('+ ', end="")
            print()
        print('\n')
    else:
        for column, row in board.items():
            print("{} => {}".format(column, row))
        print('\n')
            
def calc_number_of_conflics_in_diag(number_of_quens_in_diag):
    if number_of_quens_in_diag < 2:
        return 0
    if number_of_quens_in_diag == 2:
        return 1
    
    return (number_of_quens_in_diag - 1) * number_of_quens_in_diag / 2
            
def evaluate_solution(board):
    number_of_conflicts = 0
    
    principal_diags_used = {}
    secondary_diags_used = {}
    
    for column in board:
        current_principal_diag_index = column - board[column]
        current_secondary_diag_index = column + board[column]
        
        if current_principal_diag_index not in principal_diags_used:
            principal_diags_used[current_principal_diag_index] = 1
        else:
            principal_diags_used[current_principal_diag_index] += 1
        
        if current_secondary_diag_index not in secondary_diags_used:
            secondary_diags_used[current_secondary_diag_index] = 1
        else:
            secondary_diags_used[current_secondary_diag_index] += 1
            
    for i in principal_diags_used:
        number_of_conflicts += calc_number_of_conflics_in_diag(principal_diags_used[i])
        
    for i in secondary_diags_used:
        number_of_conflicts += calc_number_of_conflics_in_diag(secondary_diags_used[i])
        
    return number_of_conflicts


def simulated_annealing(queens, current_solution, temp, cool_down_tax):
    reached_global_max = False
    
    current_solution_cost = evaluate_solution(current_solution)
    
    while temp > 0 and not reached_global_max:
        temp *= cool_down_tax
        
        # Gerando índices aleatórios para realizar a troca de um par de rainhas, na nova solução candidata
        new_queen_index = [random.randrange(0, queens), random.randrange(0, queens)]
        while new_queen_index[0] == new_queen_index[1]:
            new_queen_index = [random.randrange(0, queens), random.randrange(0, queens)]
            
        new_candidate_solution = deepcopy(current_solution)
            
        # Realizando troca de um par de rainhas, atribuíndo a linha de uma para outra
        aux = new_candidate_solution[new_queen_index[0]];
        new_candidate_solution[new_queen_index[0]] = new_candidate_solution[new_queen_index[1]]
        new_candidate_solution[new_queen_index[1]] = aux
        
        variation = evaluate_solution(new_candidate_solution) - current_solution_cost
        
        if(variation < 0 or random.uniform(0, 1) < exp(-variation/temp)):
            current_solution = deepcopy(new_candidate_solution)
            current_solution_cost = evaluate_solution(current_solution)
            
        if(current_solution_cost == 0):
            reached_global_max = True
    
    return current_solution 
        

if __name__ == "__main__":
    start = time.time()

    # random.seed(12)
    number_of_queens = 100
    temperature = 100
    cool_down_tax = 0.999
   
    initial_solution = create_board(number_of_queens)
    print("Initial solution with", evaluate_solution(initial_solution), "conflicts")
    display(initial_solution)
    
    solution = simulated_annealing(number_of_queens, initial_solution, temperature, cool_down_tax)
    
    print("Best solution found with", evaluate_solution(solution), "conflicts")
    display(solution)
    
    
    print("Done in :", time.time() - start, " seconds.")
