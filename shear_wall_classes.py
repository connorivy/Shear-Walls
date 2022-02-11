from utils import ft_inches_to_decimal as ft2dec
import math

class Project:
    def __init__(self):
        self.elev_lvl1_ft = 100
        self.elev_lvl1plus4_ft = 104
        self.elev_lvl2_ft = ft2dec(114, 8+7/8)
        self.elev_lvl3_ft = ft2dec(125, 4+3/4)
        self.elev_lvl4_ft = ft2dec(136, 5/8)
        self.elev_lvl5_ft = ft2dec(146, 8+1/2)
        self.elev_roof_ft = ft2dec(157, 8+5/8)

        self.wind_reduction_factor = .6
        self.DL_reduction_factor = .9

        self.shear_per_lvl_plf = [131, 236, 215, 227, 156, 611]

        self.typ_floor_assemb_ft = ft2dec(1, 9+3/4)

    def get_lvl_elev(self, lvl):
        if lvl==1: 
            return self.elev_lvl1_ft
        elif lvl==1.5: 
            return self.elev_lvl1plus4_ft
        elif lvl==2: 
            return self.elev_lvl2_ft
        elif lvl==3: 
            return self.elev_lvl3_ft
        elif lvl==4: 
            return self.elev_lvl4_ft
        elif lvl==5: 
            return self.elev_lvl5_ft
        elif lvl==6: 
            return self.elev_roof_ft
        else:
            print(f'{lvl} is not a valid level')


    def get_stud_length(self, lvl):
        if lvl == 5:
            return ft2dec(9, 8+5/8)
        elif lvl == 1:
            return ft2dec(12, 8+5/8)
        else:
            return ft2dec(8, 8+5/8)

    def get_DL_psf(self, type):
        if type == 'unit':
            return 27
        elif type == 'roof':
            return 20
        else:
            print(f'{type} is not a valid dead load type')

    
class ShearWall():
    def __init__(self, project_info, lvl, wind_trib, floor_trib, floor_load_type, wall_len, greater_wall_len=-1, tie_distance=1):
        # initialize certain variables as 0 so we know if the values have been set or not
        self.shear_point_load = 0

        self.project_info = project_info
        self.lvl = lvl
        self.wind_trib = wind_trib
        self.floor_trib = floor_trib
        self.floor_load_type= floor_load_type
        self.wall_len = wall_len
        if greater_wall_len == -1:
            self.greater_wall_len = wall_len
        else:
            self.greater_wall_len = greater_wall_len
        self.tie_distance = tie_distance

        self.get_base_elev()
        self.get_stud_height()
        self.get_self_weight_plf()
        self.get_shear_point_load()
        self.get_shear_force()
        self.get_overturning_moment()
        print('Overturning Moment', self.overturning_moment)
        self.get_resisting_moment()
        self.get_total_moment()
        self.get_chord_forces()

    def get_base_elev(self):
        self.base_elev = self.project_info.get_lvl_elev(self.lvl)
        print('Base Elevation', self.base_elev)

    def get_stud_height(self):
        self.stud_height = self.project_info.get_stud_length(self.lvl)

    def get_self_weight_plf(self):
        self.weight = 7 * self.stud_height

    def get_shear_point_load(self):
        # wind shear at level * wind trib * wall_len / greater_wall_len
        # don't subtract one to level because the level 1 wall is acted on by level 2 wind 
        self.shear_point_load = self.project_info.wind_reduction_factor * self.project_info.shear_per_lvl_plf[math.floor(self.lvl)] * self.wind_trib * self.wall_len / self.greater_wall_len
        print('Shear Point Load', self.shear_point_load)

    def get_shear_force(self):
        self.shear_force = self.shear_point_load / self.wall_len
        print('Shear Force', self.shear_force)

    def get_overturning_moment(self, elev_for_moment=-1):
        if elev_for_moment == -1:
            elev_for_moment = self.base_elev

        # print(self.project_info.get_lvl_elev(math.floor(self.lvl)+1), elev_for_moment)

        # the following formula is not transferable with a different 'project' structure
        self.overturning_moment = self.shear_point_load * (self.project_info.get_lvl_elev(math.floor(self.lvl)+1) - elev_for_moment)
        return self.overturning_moment

    def get_resisting_moment(self):
        dist_dead_load = self.project_info.get_DL_psf(self.floor_load_type) * self.floor_trib + self.weight
        self.resisting_moment = self.project_info.DL_reduction_factor * dist_dead_load * self.wall_len ** 2 / 2
        print('Resisting Moment', self.resisting_moment)

    def get_total_moment(self):
        self.total_moment = self.resisting_moment - self.overturning_moment
        print('Total Moment', self.total_moment)

    def get_chord_forces(self):
        self.chord_forces = self.total_moment / (self.wall_len - self.tie_distance)
        print('Chord Forces', self.chord_forces)


class StackedShearWall():
    # stacked shear walls is expecting input that looks like this (project_info, [these are the args for a wall except project info], [these are a differnt wall args])
    def __init__(self, project_info, *args):
        min_lvl = 1000
        self.shear_walls = []
        
        for wall_args in args:
            self.shear_walls.append(ShearWall(project_info, *wall_args))
            min_lvl = min(min_lvl, self.shear_walls[-1].lvl)
        self.min_lvl = math.floor(min_lvl)
        self.num_lvls = len(self.shear_walls)
        self.max_lvl = math.floor(min_lvl) + self.num_lvls - 1 

        self.shear_force = []
        self.overturning_moment = []
        self.resisting_moment = []
        self.total_moment = [0] * (self.num_lvls)
        self.chord_forces = [0] * (self.num_lvls)
        self.project_info = project_info

        for index in range(self.num_lvls):
            print(f'\n\nLEVEL {self.min_lvl + index}:')
            print('---------------------------------------------')
            self.get_shear_force_at_lvl(self.min_lvl + index)
            self.get_overturning_moment_at_lvl(self.min_lvl + index)
            self.get_resisting_moment_at_lvl(self.min_lvl + index)
            self.get_total_moment_at_lvl(self.min_lvl + index)
            self.get_chord_forces_at_lvl(self.min_lvl + index)

    def get_shear_force_at_lvl(self, lvl):
        shear_force = 0
        for index in range(lvl, self.max_lvl+1):
            shear_force += self.shear_walls[index-self.min_lvl].shear_force
        self.shear_force.append(shear_force)
        print('Shear Force', self.shear_force[-1])

    def get_overturning_moment_at_lvl(self, lvl, elev_for_moment=-1):
        overturning_moment = 0
        elev = self.project_info.get_lvl_elev(lvl)

        for index in range(lvl, self.max_lvl+1):
            overturning_moment += self.shear_walls[index-self.min_lvl].get_overturning_moment(elev)

        self.overturning_moment.append(overturning_moment)
        print('Overturning Moment', self.overturning_moment[-1])

    def get_resisting_moment_at_lvl(self, lvl):
        resisting_moment = 0
        for index in range(lvl, self.max_lvl+1):
            resisting_moment += self.shear_walls[index-self.min_lvl].resisting_moment
        self.resisting_moment.append(resisting_moment)
        print('Resisting Moment', self.resisting_moment[-1])

    def get_total_moment_at_lvl(self, lvl):
        self.total_moment[lvl - self.min_lvl] = self.resisting_moment[lvl - self.min_lvl] - self.overturning_moment[lvl - self.min_lvl]
        print('Total Moment', self.total_moment[lvl - self.min_lvl])

    def get_chord_forces_at_lvl(self, lvl):
        self.chord_forces[lvl - self.min_lvl] = self.total_moment[lvl - self.min_lvl] / (self.shear_walls[lvl - self.min_lvl].wall_len - self.shear_walls[lvl - self.min_lvl].tie_distance)
        print('Chord Forces', self.chord_forces[lvl - self.min_lvl])

        
