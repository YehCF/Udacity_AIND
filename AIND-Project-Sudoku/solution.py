assignments = []



def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """

    # Don't waste memory appending actions that don't actually change any values
    if values[box] == value:
        return values

    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """

    # Find all instances of naked twins
    for unit in unit_list:
        twins = {}
        for box in unit:
            if values[box] in twins.keys():
                twins[values[box]].append(box)
            else:
                twins[values[box]] = [box]

        twins = {value: twins_boxes for value, twins_boxes in twins.items() if len(twins_boxes) == len(value) and len(value) > 1}
        
        if len(twins.keys()) > 0:
        # If there's twins 
            # Eliminate the naked twins as possibilities for their peers
            for value, twins_boxes in twins.items():
                twins_peers = set(unit) - set(twins_boxes)
                #print(twins_boxes, "", twins_peers)
                for box in twins_peers:
                    new_value = values[box]
                    for i in value:
                        new_value = new_value.replace(i,"")
                    values = assign_value(values, box, new_value)
    return values


def cross(A, B):
    '''
    "Cross product of elements in A and elements in B."
    for exmaple:
        A: 'DEF', B:'123'
        cross(A, B) yields ['D1','D2','D3','E1','E2','E3','F1','F2','F3'] 
    '''
    return [a+b for a in A for b in B]

def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    # Transform into dictionary form  {box: value}
    values = {box: value if value is not '.' else columns for box, value in zip(boxes, grid)}
    assert len(values) == 81, "There should be 81 pairs in values dictionary"    
    return values

def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    if values:
        grid_values_2D = []

        for i, row_unit in enumerate(row_units):
            row_value = []
            for j, box in enumerate(row_unit):
                row_value.append(values[box])
                if j % 3 == 2 and j != len(row_unit) - 1:
                    row_value.append("|")
            grid_values_2D.append(" ".join(row_value))
            if i % 3 == 2 and i != len(rows) - 1:
                grid_values_2D.append("".join(['-']*len(grid_values_2D[-1])))
        print("\n".join(grid_values_2D))
    else:
        print("The puzzle is not solved")

def eliminate(values):
    '''
    Eliminate the possible values in certain box's peers 
    (Iterate through the boxes whose value is specified)
    Args:
        values(dict): The sudoku in dictionary form
    '''
    solved_values = {box:value for box, value in values.items() if len(value) == 1}
    for box, value in solved_values.items():
        for peer in peers[box]:
            new_value = values[peer].replace(value, "") # use replace, it will return a new value
            values = assign_value(values, peer, new_value)
    return values

def only_choice(values):
    '''
    Find the box that only has a choice, and then fill the value in box
    (that is, the values which only appear once in certain unit)
    '''
    # Iterate through each unit
    for unit in unit_list:
        for num in '123456789':
            boxes_with_num = [box for box in unit if num in values[box]]
            if len(boxes_with_num) == 1:
                values = assign_value(values, boxes_with_num[0], num)
    return values

def reduce_puzzle(values):
    '''
    reduce the possibilities of the puzzle
    '''
    solved_boxes = [box for box, value in values.items() if len(value) == 1]
    stalled = False
    while not stalled:
        solved_boxes_before = len([box for box, value in values.items() if len(value) == 1])    
        values = eliminate(values)
        values = only_choice(values)
        values = naked_twins(values)
        solved_boxes_after = len([box for box, value in values.items() if len(value) == 1])
        stalled = solved_boxes_before == solved_boxes_after
    # check if there's an box with no possiblities
        if len([box for box, value in values.items() if len(value) == 0]):
            return False
    return values

def search(values):
    '''
    Reduce the puzzle and search for possible solutions
    '''
    values = reduce_puzzle(values)
    # check whether it is solved or stuck
    if values is False:
        return False
    if all([len(value) == 1 for box, value in values.items()]):
        return values # Solved
    # choose one who has fewer possiblities
    n, b = min((len(value),box) for box, value in values.items() if len(value) > 1)
    # pick one value and fill in the box, then try to solve the puzzle
    for value in values[b]:
        new_values = values.copy()
        new_values = assign_value(new_values, b, value)
        attempt = search(new_values)
        if attempt:
            return attempt
    

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    values = grid_values(grid)

    return search(values)





# Sudoku building blocks
# create boxes
rows = "ABCDEFGHI"
columns = '123456789'
boxes = cross(rows, columns)

# create unit list
row_units = [cross(row, columns) for row in rows]
column_units = [cross(rows, column) for column in columns]
square_units = [cross(rows[i:i+3],columns[j:j+3]) for i in range(0, 8, 3) for j in range(0,8,3)]
diagonal_units = [[r+c for r, c in zip(rows, columns)], [r+c for r, c in zip(rows, reversed(columns))]]
unit_list = row_units + column_units + square_units + diagonal_units
units = {box: [unit for unit in unit_list if box in unit] for box in boxes}
peers = {box: list(set(sum(units[box],[]))-set([box])) for box in boxes}

if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
