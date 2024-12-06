
import os 
import shutil 
import fnmatch 
import numpy as np
import pendulum as pd

import tkinter as tk  
from tkinter import simpledialog,messagebox 

from SolarEnergyPy.studio import mainWindow,get_user_input,popup

import SolarEnergyPy.solarPosFunc as sp
from VisualShape3D.geometry import *
from SolarEnergyPy.models import *
from VisualShape3D.VisualModels import VisualShape3D


class VisualProject(VisualShape3D):  
    TITLE_KEY = 'title'  
    PATH_KEY = 'path'  

    def __init__(self, name="untitled", site=(117, 31), tz='Asia/Shanghai', style=None, ax=None, *args, **kwargs):
        
        if style is None:  
            style = {'alpha': 0.5}  
        super().__init__(style) 

        self.name = name  

        self.longitude = site[0]  
        self.latitude = site[1]  
        self.tz = tz 

        self.project_file = f"{name}.prj"  
        self.material_properties = {}  


        # for entity management
        self.entities = {}  
        self.entitie_done = {}  
        self.entity_types = {"building", "collectors"} 


        circle = Shape(shape="regularPolygon", **{'R': 1, 'n': 48, 'P0': (0, 0, 0)})  
        self.ground = circle.move(by=(0, 90))  
        self.add_shape(self.ground, style=style) 

        if not self.exist_project(name):  
            self.create_new_project()  

        self.open_existing_project()

    def __str__(self):  
        return f"项目名称: {self.name}, 工作目录: {self.directory}, 经纬度: ({self.longitude}, {self.latitude}), 时区: {self.tz}"

### Project Management

    def exist_project(self, name):
        if not os.path.isfile(f"{name}.prj") or not os.path.isdir(name):
            return False
        return True

    def open_project_file(self):  
        project_name = ''
        project_directory = ''
        project_entities = {}
        try:  
            with open(self.project_file, 'r') as file:  
                for line in file:  
                    print(f"{line}")
                    key, value = line.strip().split(maxsplit=1)  
                    if key.lower() == 'title':  
                        project_name = value  
                    elif key.lower() == 'path':  
                        project_directory = remove_drive_from_path(value)
                    else:
                        project_entities[key] = value 

            return  project_name, project_directory, project_entities

        except Exception as e:  
            print(f"加载项目时发生错误: {e}") 
            return None

    def open_existing_project(self):  
        ret = self.open_project_file()
        if ret is not None: 
            self.name, self.directory, self.entities = ret
            project_directory = add_drive_to_path(self.directory)
        else :
            return None

        # 检查材料文件和建筑模板是否存在  
        materials_file = os.path.join(project_directory, 'materials', 'materials.csv')  
        building_axes_file = os.path.join(project_directory, 'building_axes.in')
        building_walls_file = os.path.join(project_directory, 'building_walls.in')
        building_geometry_file = os.path.join(project_directory, 'building_geometry.in')  

        if not os.path.isfile(materials_file):  
         self.create_materials(project_directory)  

        if not os.path.isfile(building_axes_file) or \
        not os.path.isfile(building_walls_file) or \
        not os.path.isfile(building_geometry_file) :  
         self.generate_formatted_input_files(project_directory)  

        self.load_material_properties(materials_file)  

    def create_new_project(self):  
        directory_path = os.path.join(os.getcwd(), self.name)  
        create_directory(directory_path)  
        self.directory = remove_drive_from_path(directory_path)  

        with open(self.project_file, 'w') as file:  
            file.write(f"title {self.name}\n")  
            file.write(f"path {self.directory}\n")  

        self.create_materials(directory_path)
        self.generate_formatted_input_files(directory_path)
        
    def create_materials(self, directory_path):  
        materials_directory_path = os.path.join(directory_path, 'materials')  
        materials_generator = BuildingMaterials(directory=materials_directory_path)
        materials_generator.write_materials_to_file() 

    def load_material_properties(self, file_path):  
        try:  
            with open(file_path, 'r') as file:  
                next(file)  # 跳过标题行  
                for line in file:  
                    data = line.strip().split(',')  
                    if len(data) != 4:  
                        continue  # 跳过无效行  
                    material_id, density, specific_heat, thermal_conductivity = data  
                    self.material_properties[material_id] = {  
                        'density': float(density),  
                        'specific_heat': float(specific_heat),  
                        'thermal_conductivity': float(thermal_conductivity)  
                    }  
        except FileNotFoundError:  
            print(f"材料文件 '{file_path}' 未找到。")  
        except Exception as e:  
            print(f"读取材料文件时发生错误: {e}")  

    def generate_formatted_input_files(self, directory_path):  
        generator = BuildingDataGenerator(directory=directory_path)  
    
        # Creating sample data about walls  
        generator.add_wall('first', [0.2, 0.15], ['1', '2'], 0.6, 0.6)  
        generator.write_walls_to_file()  
    
        # Creating sample data about axes  
        generator.add_axis(1, 0.0, 0.0)  
        generator.add_axis(2, 10.0, 0.0)  
        generator.add_axis('A', 0.0, 90.0)  
        generator.add_axis('B', 10.0, 90.0)  
        generator.add_axis('C', 20.0, 90.0)  
        generator.add_axis(3, 5.0, 45.0)  
        generator.write_axes_to_file()  
    
        # Creating example data about building geometry  
        generator.add_geometry('WALL', 1, 2, 'A', 'B', 3.0, 'BRICK', 0, 101)  # Valid wall type and axes  
        generator.add_geometry('WALL', 1, 2, 'B', 'C', 3.0, 'CONCRETE', 102, 103)  # Valid wall type and axes  
        generator.add_geometry('FLOOR', 'UNKNOWN_AXIS', 2, 'A', 'B', 0.2, 'BRICK', 101, -1)  # Invalid axis  
        generator.write_geometry_to_file()        

    def about_myself(self):
        with open(self.project_file, 'r') as file:  
            for line in file:  
                print(f"{line.rstrip()}")  

### Building Management
    # by function
    def create_building(self, name):
        if not self.exist_entity(name):
            self.register_entity(name = name, entity_type = 'building')
            self.entities[name] = Building(self, name)
            print(f"Success in creating a new building {name}")
            return self.entities[name]
        else :
            print(f"The building {name} has been registered.")
            return False
        
    def open_building(self, name):
        if self.exist_entity(name):
            entity = self.entities[name]
            if entity is not None and isinstance(entity,Building):
                return entity
            elif entity.lower() == 'building':
                self.entities[name] = Building(self, name)
                return self.entities[name]
        else :
            print(f"The buidling {name} does not exists!!")
            return False
    
    # by files
    def editor_for_building_geometry(self, parser):
        rootWindow = tk.Tk()
    
        H = 500
        W = 900
        size = '{}x{}'.format(W,H)
        studio = mainWindow(parser, rootWindow, title = 'Building Studio', size = size)

        studio.project_menu.insert(0,'command',label='New Building', command=self.create_a_building)
        studio.project_menu.insert(1,'command',label='Open Building', command=self.open_a_building)

        self.root = rootWindow

        rootWindow.mainloop() 

        self.root = None

    def create_a_building(self):
        print(get_user_input(f"new building"))

    def open_a_building(self):
        name, directory, entities = self.open_project_file()

        # 创建选项  
        options = []
        for k,v in entities.items():
            options.append(k)

        # 创建一个变量来存储选中的选项  
        default = options[0]  

        popup(self.root, options, default, callback = self.open_building)  


### Modeling collectors
    def add_collectors(self, name):
        if not self.exist_entity(name):
            self.register_entity(name = name, entity_type = "collectors")
            self.entities[name] = name

        return self.entities[name]

### Miscellaneous functions
    def set_site_timezone(self, longitude=117, latitude=31, tz='Asia/Shanghai' ):
        self.longitude = longitude
        self.latitude  = latitude
        self.tz = tz

    def set_simulation_period(self,start = sp.local_time(1,1,0,0), 
                      end = sp.local_time(12,31,23,59)):
        self.start = start
        self.end = end
        delta = self.end - self.start
        return delta.hours

    def exist_entity(self,name):
        if name in self.entities.keys():
            return True 
        else :
            return False

    def register_entity(self, name , entity_type):  
        """  
        增加一个实体，并向工程文件中追加一个条目。  
        条目包含两个字符串，第一个为名称，第二个为实体类型。  
        如果实体名称重名，则发出严重警告并退出。  
        最终返回成功与否。  
        """  
        project_data = {}
        try:  
            with open(self.project_file, 'r') as file:  
                for line in file:  
                    # print(f"{line}")
                    key, value = line.strip().split(maxsplit=1)  
                    project_data[key] = value  

        except Exception as e:  
            print(f"加载文件{elf.project_file}时发生错误: {e}") 

        # 创建实体子目录  
        entity_directory = ''.join([project_data['title'], "/", name])
        entity_directory_path = add_drive_to_path(entity_directory) 
        create_directory(entity_directory_path)

        # 添加新的实体  
        project_data[name] = entity_type 
    
        # 在项目文件中，增加此实体  
        with open(self.project_file, 'a') as file:  # 使用 'a' 模式追加条目  
            file.write(f"{name} {entity_type}\n")  
     
        return True  # 返回成功状态
 
    def create_entity_data_file(self, project_data, name):
        pass

    def write_entitiy_data_file(self, project_data, name):
        pass

### Plotting functions
    def render(self,elev= 20.0, azim = -70.0, axes = "off", origin = "on"):

        for k,v in self.entities.items():
            if k in self.entitie_done :
                pass
            else :
                self.entitie_done[k] = v
                if len(v.vertices) > 0 :  # a defined shape that has defined vertices
                    self.shapes.append(v)

        self.show(elev, azim, axes, origin)

    def getSolarPosition(self, time) :
        pass


### Demos
def plotPoints():
    P = Point(0.5,0.5,0.5)
    P.plot(style={'facecolor':'r','alpha':0.5})
    P1 = Point(0.5,0.7,0.5)
    P.add_plot(P1)
    P.show()

def plotLine():
    P1 = Point(0.2,0.1,0.1)
    P2 = Point(0.8,0.5,0.8)
    L  = Segment(P1,P2)
    L.plot()
    L.show()

def plotPolygon():
    x = [0.5,0.3,0.6,0.9,0.1]
    y = [0.1,0.9,0.3,0.4,0.8]
    z = [0.7,0.3,0.1,0.9,0.6]
    points = list(zip(x,y,z))
    poly = Polygon(points)
    poly.plot()
    poly.show()

def plotScene():
    se = Scene(title='new',site=(117,31))
    se.plot()
    print(se)
    se.render()    

def main():
    # plotPoints()
    # plotPolygon()
    # plotLine()
    plotScene()

if __name__ == '__main__':
    main()
