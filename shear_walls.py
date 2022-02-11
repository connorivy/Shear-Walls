from shear_wall_classes import *
from openpyxl import load_workbook

def main():
    project = Project()

    #load excel file
    workbook = load_workbook(filename="P:\\\\Structural\\2021\\2115 - Dallas\\2115.147 Toll Brothers Addison Road\\5 - Project Documents\B - Calculations\CI\Wood Calcs\Shear Walls\shear_wall_input.xlsx", data_only=True)

    ws = workbook.active

    prev_shear_wall_letter = 'ZZ'
    args = []
    blank_count = 0
    for row in ws.iter_rows(min_row=1, max_col=8, max_row=10, values_only=True):
        # quit the for loop once three consecutive blanks have been found
        if row[0] == None:
            blank_count += 1
            if blank_count > 3:
                return
            continue
        else:
            blank_count = 0
            
        if row[0] != prev_shear_wall_letter:
            args = []
            prev_shear_wall_letter = row[0]

        args.append([row[1:5]])

        print(args)
        print(row)
    #                                                   lvl, wind_trib, floor_trib, floor_load_type, wall_len, greater_wall_len, tie_distance=1
    # stacked_shear_wall_1 = StackedShearWall(project,    [1, 11, 5.1852, 'unit', 29],
    #                                                     [2, 11, 5.1852, 'unit', 29],    
    #                                                     [3, 11, 5.1852, 'unit', 29],    
    #                                                     [4, 11, 5.1852, 'unit', 29],
    #                                                     [5, 11, 2, 'roof', 29])

main()