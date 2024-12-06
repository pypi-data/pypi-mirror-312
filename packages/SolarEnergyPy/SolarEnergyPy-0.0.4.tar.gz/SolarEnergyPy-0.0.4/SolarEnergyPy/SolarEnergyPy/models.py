import os 
import shutil 
import fnmatch 
import csv 
from dataclasses import dataclass, field, fields  
from typing import List  

import numpy as np
from VisualShape3D.plotable import *
from VisualShape3D.geometry import Point,Shape
from SolarEnergyPy.geomfactors import *


def remove_drive_from_path(absolute_path):  
    # 使用 os.path.splitdrive() 分离驱动器和路径  
    drive, path = os.path.splitdrive(absolute_path)  
    return path  # 返回去掉驱动器的路径部分  

def add_drive_to_path(path):  
    # 获取当前工作目录的驱动器  
    current_drive = os.path.splitdrive(os.getcwd())[0]  
    return os.path.join(current_drive, path)  # 将驱动器与路径合并

def create_directory(path):  
    """  
    创建指定路径的目录。如果目录已存在，则不执行任何操作。  
    """  
    try:  
        os.makedirs(path, exist_ok=True)  # 使用 exist_ok=True 以避免目录已存在的错误  
    except Exception as e:  
        print(f"创建目录 '{path}' 时出错: {e}")    


# a surface without any indexing
class Facet(Plotable):
    '''
         A node in the thermal network
    '''
    def __init__(self, vertices=[], indices=[], emissivity_visible = 0.0, **kwargs):
        
        super().__init__(**kwargs)

        # self.copy_vertices(vertice_index)
        self.vertices = list(vertices)
        self.indices = list(indices)      # the global indexing of vertices
        self.emissivity_visible = emissivity_visible 
        self.emissivity_infrared = None

    def set_emissivity(self, emissivity = {'infrared':0.8}):
        if 'infrared' in emissivity :
            self.emissivity_infrared = emissivity['infrared']  
        else:
            self.emissivity_visible = emissivity['visible']

    def set_normal(self, x,y,z):
        self.normal = np.array([x,y,z])

    def copy_vertices(self, vertices):
        self.vertices = []
        for v in vertices :
            self.vertices.append(v)

    def reverse_vertices(self):
        a = self.vertices[::-1]  # copy value
        b = self.indices[::-1] 
        a_reverse = a[:-1]
        a_reverse.insert(0, a[-1])
        b_reverse = b[:-1]
        b_reverse.insert(0, b[-1])
        for i,v in enumerate(a_reverse):  # copy pointer
            self.vertices[i] = v

        for i,v in enumerate(b_reverse):  # copy pointer
            self.indices[i] = v

        return self.vertices,self.indices

    def get_vertices(self):
        return self.vertices

    # def deep_copy(self):
    #     return self.__class__(**self.get_seed())
### visualization
    def iplot(self, style =None, ax=None,**kwargs):
        if self.hidden :
            return

        if style == None:
            style = ('default','default','default')

        if ax == None :
            ax = self.get_ax()

        plotable3d = self.get_plotable_data()
        ( face_color, edge_color, alpha) = style

        if face_color == 'default': face_color = 't'
        if edge_color == 'default': edge_color = self.edgecolor
        if     alpha  == 'default': alpha = self.alpha

        for polygon in plotable3d:
            polygon.set_facecolor(face_color)
            polygon.set_edgecolor(edge_color)
            polygon.set_alpha(alpha)
            ax.add_collection3d(polygon)
    
    def get_plotable_data(self):
        """
        :returns: matplotlib Poly3DCollection
        :rtype: mpl_toolkits.mplot3d
        """
        import mpl_toolkits.mplot3d as mplot3d
        return [mplot3d.art3d.Poly3DCollection([self.vertices])]

    def get_instance(self): return self

    def get_domain(self):
        """
        :return  ndarray([min], [max])
            opposite vertices of the bounding prism for this object
        """
        # Min/max along the column
        vertices = np.array(self.vertices)
        return np.array([vertices.min(axis=0),  # min (x,y,z)
                         vertices.max(axis=0)]) # max (x,y,z)

### Functions for geometry calculation
    def get_seed(self):
        """
        get the dict form of its arguments for a temporary copy :
           Pathch(dict)
        """
        dict_args = {'vertices':self.vertices.copy(),
                     'indces':self.indices.copy(), 
                     'emissivity_infrared':self.emissivity_infrared,
                     'emissivity_visible':self.emissivity_visible}
        return dict_args

# A surface with global indexing
class Surface(Facet):
    def __init__(self, label, wall, bFront=True, emissivity_visible = 0.6, **kwargs):
 
        self.label = label
        self.id = wall.id *2 - 1
        self.iv = wall.front
        self.wall = wall
        self.bFront = bFront
        self.hidden = False

        if self.isNegative(): 
            self.id = self.wall.id *2
            self.iv = wall.back

        super().__init__(wall.vertices, wall.indices, emissivity_visible , **kwargs)

        if self.isNegative():
            self.reverse_vertices()
 
    def __str__(self):
        info=f"    face({self.id}) = {self.indices} ({self.label})"
        return info

    def print(self): print(self)

    def isNegative(self):
        return self.bFront == False

    def turn_off(self):
        self.hidden = True

    def turn_on(self):
        self.hidden = False

### Functions for geometry calculation
    def get_seed(self):
        """
        get the dict form of its arguments for creating a copy :
           Facet(dict)
        """
        wall = Wall(self.wall.get_seed())
        dict_args = {'label':self.label, 'wall':wall, 'bFront':self.bFront}
        return dict_args

    # def deep_copy(self):
    #     return self.__class__(**self.get_seed())

@dataclass  
class Wall:  
    '''  
    Represents a wall with thermal and optical properties.  

    Attributes:  
        label (str): The label of the wall.  
        wall_id (int): Unique identifier for the wall.  
        front (float): Front space of the wall.  
        back (float): Back space of the wall.  
        vertices (List[float]): List of vertices defining the wall's geometry.  
        indices (List[int]): List of indices for the vertices.  
        front_emissivity_visible (float): Emissivity of the front surface in the visible spectrum.  
        back_emissivity_visible (float): Emissivity of the back surface in the visible spectrum.  
    '''  
    
    label: str  
    id: int  
    front: float = 0  
    back: float = 0  
    vertices: List[float] = field(default_factory=list)  
    indices: List[int] = field(default_factory=list)  
    front_emissivity_visible: float = 0.0  
    back_emissivity_visible: float = 0.0  

    def __post_init__(self):  
        # Validation  
        if self.front < 0 or self.back < 0:  
            raise ValueError("Front and back spaces must be non-negative.")  
        if not (0 <= self.front_emissivity_visible <= 1) or not (0 <= self.back_emissivity_visible <= 1):  
            raise ValueError("Emissivity values must be between 0 and 1.")  

    def get_seed(self) -> dict:  
        return {  
            'label': self.label,   
            'id': self.id,   
            'front': self.front,   
            'back': self.back,   
            'vertices': self.vertices.copy(),  
            'indices': self.indices.copy(),  
            'front_emissivity_visible': self.front_emissivity_visible,  
            'back_emissivity_visible': self.back_emissivity_visible  
        }

class Space(Plotable):
    '''
         A node in the thermal network
    '''
    def __init__(self, iv = 0, surfaces=[], **kwargs):

        super().__init__(**kwargs)

        self.iv = iv
        self.surfaces = list(surfaces)
        self.surface_number = len(self.surfaces)
        self.hidden = False


    def __str__(self):
        info =f'Space({self.iv}) is enclosed by {self.surface_number} surfaces\n'
        for f in self.surfaces :
                info += f.__str__()+'\n' 
        return info

    def print(self): print(self)

    def add_front_surface(self, wall):
        label = f"{wall.label}+"
        surface = Surface(label, wall )
        self.surfaces.append(surface)
        self.surface_number += 1
        return surface

    def add_back_surface(self, wall):
        label = f"{wall.label}-"
        surface = Surface(label, wall, bFront=False)
        self.surfaces.append(surface)
        self.surface_number += 1
        return surface

    def get_surface_number(self):
        return self.surface_number

    def turn_off(self):
        self.hidden = True

    def turn_on(self):
        self.hidden = False
### visualization
    def iplot(self, style = None, ax = None, **kwargs):
        
        if self.hidden :
            return

        if style == None:
            style = ('default','default','default')

        if ax == None :
            ax = self.get_ax()

        bDefault_Face_Color = False
        bDefault_Edge_Color = False
        bDefault_Alpha = False


        face_color = style['facecolor'] if 'facecolor' in style else 't'
        edge_color = style['edgecolor'] if 'edgecolor' in style else 'default'
        alpha      = style['alpha']     if 'alpha'     in style else 'default'

        if face_color == 'default': face_color = 't'
        if face_color == 't':       bDefault_Face_Color = True
        if edge_color == 'default': bDefault_Edge_Color = True
        if     alpha  == 'default': bDefault_Alpha = True

        plotable3d = self.get_plotable_data()
        for i,polygon in enumerate(plotable3d):
            if bDefault_Face_Color : 
                face_color = self.surfaces[i].face_color
            if bDefault_Edge_Color : 
                edge_color = self.surfaces[i].edge_color
            if bDefault_Face_Color : 
                     alpha = self.surfaces[i].alpha

            polygon.set_facecolor(face_color)
            polygon.set_edgecolor(edge_color)
            polygon.set_alpha(alpha)
            ax.add_collection3d(polygon)
    
    def get_plotable_data(self):
        """
        :returns: matplotlib Poly3DCollection
        :rtype: mpl_toolkits.mplot3d
        """
        data_list=[]
        for surface in self.surfaces :
            data_list = data_list + surface.get_plotable_data()

        return data_list
    
    def get_instance(self): return self

### Functions for geometry calculation
    def get_seed(self):
        """
        get the dict form of its arguments for creating a copy :
           Patch(dict)
        """
        dict_args = {'iv':self.iv, 'surfaces': self.surfaces}
        return dict_args

    def get_domain(self):
        if self.surfaces != []:
            space_domain = np.vstack([face.get_domain() 
                                    for face in self.surfaces])
        else:
            space_domain = np.ones((0, 3))

        points = space_domain
        return np.array([points.min(axis=0), points.max(axis=0)])


@dataclass
class ThermalMaterial:
    name: str  = field(default='standard brick', repr=False)
    rho: float = field(default=1970.2, metadata={'unit': 'kg/m^3'}  , repr=False)
    c:   float = field(default=0.2334, metadata={'unit': 'J/(kg K)'}, repr=False)
    k:   float = field(default=0.6924, metadata={'unit': 'W/(m K)'} , repr=False)

    def __str__(self):
        return f"{self.name, self.rho, self. c, self.k}"

class BuildingMaterials:  
    def __init__(self, directory='materials', filename='materials.csv'):  
        self.directory = directory  
        self.filename = os.path.join(directory, filename)  
        
        # Create the directory if it does not exist  
        os.makedirs(self.directory, exist_ok=True)  
        
        # Define the materials data  
        self.materials_data = [  
            ("STANDARD-BRICK", 1970.214, 0.2334000, 0.6924000),  
            ("GYPSUM-BOARD", 1249.404, 0.3034200, 0.4327500),  
            ("SOFT-WOOD", 432.4860, 0.7818900, 0.1090530),  
            ("GLASS-WOOL", 52.05850, 0.1867200, 3.8082000E-02),  
            ("CONCRETE", 2306.592, 0.2450700, 0.9347400),  
            ("STUCCO(INTOREXT)", 2114.376, 0.2334000, 0.7443300),  
            ("AIR-SPACE-AT-70F", 1.201350, 0.2800800, 8.9419633E-02),  
            ("PACKED-EARTH", 1521.710, 0.2334000, 6.4047001E-02),  
            ("CELOTEX-INSUL-BOARD", 288.3240, 0.3617700, 5.4872699E-02),  
            ("CORKBOARD", 160.1800, 0.5659950, 4.8468001E-02),  
            ("GYPSUM-PLASTER", 740.0316, 0.2334000, 0.8078000),  
            ("CEMENT-PLASTER", 1182.128, 0.2334000, 0.7212500),  
            ("WOOL-ASBESTAS", 400.4500, 0.2334000, 8.9435004E-02),  
            ("ALUMINUM", 2691.024, 0.2450700, 204.2580),  
            ("STAINLESS-STEEL", 8249.270, 0.1400400, 28.85000),  
            ("STEEL", 7800.766, 0.1400400, 44.71750),  
            ("DRY-CLAY", 1794.016, 0.2450700, 0.5409375),  
            ("CELLULAR-GLASS-INSUL", 100.1125, 0.2450700, 5.7700001E-02),  
            ("MINERAL-FIBERBOARD", 288.3240, 0.1983900, 5.0487500E-02),  
            ("POLYSTYRENE-INSUL", 28.83240, 0.3384300, 3.6062501E-02),  
            ("POLYURETHANE-INSUL", 24.02700, 0.4434600, 2.3079999E-02),  
            ("PRESSED-WOOD-CHIPS", 352.3960, 0.4434600, 8.6550005E-02),  
            ("CELLULOSE", 44.04950, 0.3851100, 3.8947500E-02),  
            ("SAWDUST", 192.2160, 0.3851100, 6.4912498E-02),  
            ("PLYWOOD-SHEET", 544.6120, 0.3384300, 0.1154000),  
            ("HARDWOOD", 720.8100, 0.3501000, 0.1586750),  
            ("CEMENT-ASBESTOS-TILE", 1970.214, 0.2334000, 0.3894750),  
            ("LIMESTONE", 2114.376, 0.2567400, 1.557900),  
            ("ASPHALT", 2114.376, 0.2567400, 0.9382020),  
            ("META-LATH&PLASTER", 1601.800, 0.2800800, 0.4760250),  
            ("CONCRETESLAB", 2306.592, 0.2567400, 0.9347400),  
            ("SOLID-GYPSUM", 1020.347, 0.3034200, 0.1021290),  
            ("MARBLE", 2450.754, 0.2450700, 2.509950),  
            ("DRY-SAND", 1601.800, 0.2217300, 0.3288900),  
            ("SLATE", 3219.618, 0.2334000, 1.550976),  
            ("PLAIN-WATER", 997.9214, 1.167000, 0.5729610),  
            ("REINFORCED-CONCRETE", 2242.520, 0.1820520, 0.9347400),  
            ("ADOBE-BRICKS", 1441.620, 0.2800800, 0.5296860),  
            ("MORTAR-CEMENT", 1858.088, 0.1867200, 0.7212500),  
            ("BUILT-UPROOF", 1121.260, 0.4084500, 0.1622812),  
            ("CONCRETEBLOCK", 608.6840, 0.2334000, 0.5712300),  
            ("ACOUSTICAL-TILE", 480.5400, 0.2334000, 6.0585000E-02),  
            ("ROCKWOOL-INSULATION", 32.03600, 0.1983900, 3.7504997E-02),  
            ("1/2CARPET1/4-PAD", 173.4749, 0.3851100, 0.1168425),  
            ("PARTICLE-B-1/4-PAD", 640.7200, 0.3384300, 0.2769600),  
            ("RARO", 0.1601800, 1.1670000E-02, 1.7310000E-03),  
            ("RARO2", 2402.700, 0.2334000, 1.731000),  
        ]  

    def write_materials_to_file(self):  
        """  
        Write the materials data to a CSV file.  
        """  
        header = ['name', 'density', 'capacity', 'conductivity']  

        with open(self.filename, mode='w', newline='') as file:  
            writer = csv.writer(file)  
            writer.writerow(header)  
            writer.writerows(self.materials_data)  

        print(f"Materials data written to {self.filename}") 

class BuildingDataGenerator:  
    def __init__(self, directory='.', walls_filename='building_walls.in', axes_filename='building_axes.in', geometry_filename='building_geometry.in'):  
        self.directory = directory  
        self.walls_filename = os.path.join(directory, walls_filename)  
        self.axes_filename = os.path.join(directory, axes_filename)  
        self.geometry_filename = os.path.join(directory, geometry_filename)  
        
        # Create the directory if it does not exist  
        os.makedirs(self.directory, exist_ok=True)  

        self.wall_data = []  
        self.axes_data = []  
        self.geometry_data = []  

    def add_wall(self, wall_name, layer_thicknesses, layer_materials, front_emissivity, back_emissivity):  
        """  
        Add a wall's data to the list.  

        :param wall_name: Name of the wall  
        :param layer_thicknesses: List of thicknesses for each layer  
        :param layer_materials: List of materials for each layer  
        :param front_emissivity: Front emissivity value  
        :param back_emissivity: Back emissivity value  
        """  
        if len(layer_thicknesses) != len(layer_materials):  
            raise ValueError("Layer thicknesses and materials must have the same length.")  
  
        wall_entry = [wall_name] + [item for pair in zip(layer_thicknesses, layer_materials) for item in pair] + \
                     [front_emissivity, back_emissivity]
        self.wall_data.append(wall_entry)  

    def write_walls_to_file(self):  
        """  
        Write the wall data to a file.  
        """  
        header = ['WALL_NAME'] + \
                 [f'THICKNESS{i+1} MATERIAL{i+1}' for i in range(len(self.wall_data[0]) - 2)] + \
                 ['FRONT_EMISSIVITY', 'BACK_EMISSIVITY']  

        with open(self.walls_filename, mode='w', newline='') as file:  
            writer = csv.writer(file)  
            writer.writerow(header)  
            writer.writerows(self.wall_data)  

        print(f"Wall data written to {self.walls_filename}")  

    def add_axis(self, axis_id, axis_position, axis_angle):  
        """  
        Add an axis's data to the list.  

        :param axis_id: Identifier for the axis  
        :param axis_position: Position of the axis  
        :param axis_angle: Angle of the axis  
        """  
        axis_entry = [axis_id, axis_position, axis_angle]  
        self.axes_data.append(axis_entry)  

    def write_axes_to_file(self):  
        """  
        Write the axes data to a file.  
        """  
        header = ['AXIS_ID', 'AXIS_POSITION', 'AXIS_ANGLE']  

        with open(self.axes_filename, mode='w', newline='') as file:  
            writer = csv.writer(file)  
            writer.writerow(header)  
            writer.writerows(self.axes_data)  

        print(f"Axis data written to {self.axes_filename}")  

    def add_geometry(self, geometry_type, left_axis, right_axis, bottom_axis, top_axis, height, wall_type, front_room, back_room):  
        """  
        Add geometry data to the list.  

        :param geometry_type: Type of the geometry (e.g., WALL, FLOOR)  
        :param left_axis: Left axis ID  
        :param right_axis: Right axis ID  
        :param bottom_axis: Bottom axis ID  
        :param top_axis: Top axis ID  
        :param height: Height of the geometry  
        :param wall_type: Type of wall  
        :param front_room: Front room ID  
        :param back_room: Back room ID  
        """  
        # Check if the wall_type exists in wall_data  
        wall_types = [entry[0] for entry in self.wall_data]  # Extract wall names from wall_data  
        if wall_type not in wall_types:  
            print(f"Warning: Wall type '{wall_type}' not found in wall data. It will be added anyway.")  

        # Check if the axes exist in axes_data  
        axes_ids = [entry[0] for entry in self.axes_data]  # Extract axis IDs from axes_data  
        for axis in [left_axis, right_axis, bottom_axis, top_axis]:  
            if axis not in axes_ids:  
                print(f"Warning: Axis '{axis}' not found in axes data. It will be added anyway.")  

        geometry_entry = [geometry_type, left_axis, right_axis, bottom_axis, top_axis, height, wall_type, front_room, back_room]  
        self.geometry_data.append(geometry_entry)  

    def write_geometry_to_file(self):  
        """  
        Write the geometry data to a file.  
        """  
        header = ['TYPE', 'LEFT_AXIS', 'RIGHT_AXIS', 'BOTTOM_AXIS', 'TOP_AXIS', 'HEIGHT', 'WALL_TYPE', 'FRONT_ROOM', 'BACK_ROOM']  

        with open(self.geometry_filename, mode='w', newline='') as file:  
            writer = csv.writer(file)  
            writer.writerow(header)  
            writer.writerows(self.geometry_data)  

        print(f"Geometry data written to {self.geometry_filename}")  

class BuildingInput:
    def __init__(self, project_directory):

        self.project_directory = project_directory

        self.axes = {}           # 存储轴网定义 {axis_id: (position, angle)}
        self.structures = []     # 存储建筑构件信息
        self.geometry_data = []  # 存储生成的几何信息
        self.type_counters = {}  # 记录每种类型的计数器

        # 定义热活性和热不活性的类型集合
        self.thermal_active_types = {'WALL', 'FLOOR', 'ROOF', 'WINDOW', 'DOOR'}
        self.thermal_inactive_types = {'EAVE', 'PARTITION'}
        
        
    def read_grid_definition(self, file_path):
        """
        读取轴网定义文件。
        文件格式示例：
        AXIS_ID, AXIS_POSITION, AXIS_ANGLE
        1, 0.0, 0.0
        A, 10.0, 90.0
        """
        with open(file_path, 'r') as file:
            next(file)  # 跳过头部
            for line in file:
                if line.strip() and not line.startswith("#"):  # 跳过空行和注释
                    data = line.strip().split(',')
                    axis_id = data[0].strip()
                    position = float(data[1].strip())
                    angle = float(data[2].strip())
                    self.axes[axis_id] = (position, angle)

    def read_building_structure(self, file_path):
        """
        读取建筑结构定义文件。
        文件格式示例：
        TYPE, LEFT_AXIS, RIGHT_AXIS, BOTTOM_AXIS, TOP_AXIS, HEIGHT, WALL_TYPE, FRONT_ROOM, BACK_ROOM
        WALL, 1, 2, A, B, 3.0, BRICK, 101, 0
        FLOOR, 1, 2, A, B, 0.2, CONCRETE, 101, -1
        """
        with open(file_path, 'r') as file:
            next(file)  # 跳过头部
            for idx, line in enumerate(file):
                if line.strip() and not line.startswith("#"):  # 跳过空行和注释
                    data = line.strip().split(',')
                    struct_type = data[0].strip()
                    left_axis   = data[1].strip()
                    right_axis  = data[2].strip()
                    bottom_axis = data[3].strip()
                    top_axis    = data[4].strip()
                    height      = float(data[5].strip())
                    wall_type   = data[6].strip()
                    front_room  = int(data[7].strip())
                    back_room   = int(data[8].strip())

                    # 确定墙体的热活性状态
                    if struct_type in self.thermal_active_types:
                        thermal_type = 'thermal active'

                    elif struct_type in self.thermal_inactive_types:
                        thermal_type = 'thermal inactive'
                        
                    else:
                        raise ValueError(f"Unknown structure type: {struct_type}")

                    # 生成唯一的name
                    unique_name = f"{struct_type}_{idx + 1}_{front_room}_{back_room}"

                    self.structures.append({
                        'name': unique_name,
                        'type': thermal_type,
                        'left_axis': left_axis,
                        'right_axis': right_axis,
                        'bottom_axis': bottom_axis,
                        'top_axis': top_axis,
                        'height': height,
                        'wall_type': wall_type,
                        'front_room': front_room,
                        'back_room': back_room
                    })

    def check_consistency(self):
        """
        检查输入文件的一致性。
        确保所有在建筑结构文件中使用的轴都在轴网定义文件中定义。
        """
        for structure in self.structures:
            if structure['left_axis'] not in self.axes or \
               structure['right_axis'] not in self.axes or \
               structure['bottom_axis'] not in self.axes or \
               structure['top_axis'] not in self.axes:
                raise ValueError(f"Axis not defined in grid file for structure: {structure}")

    def generate_geometry_info(self):
        """
        根据轴网和建筑结构生成几何信息，调整前后表面方向。
        """
        for structure in self.structures:
            left_pos, left_angle = self.axes[structure['left_axis']]
            right_pos, right_angle = self.axes[structure['right_axis']]
            bottom_pos, bottom_angle = self.axes[structure['bottom_axis']]
            top_pos, top_angle = self.axes[structure['top_axis']]
            height = structure['height']
            wall_type = structure['wall_type']
            front_room = structure['front_room']
            back_room = structure['back_room']

            # 生成墙体或地板四个顶点的绝对坐标，按逆时针顺序
            p1 = (left_pos, bottom_pos, 0)
            p2 = (right_pos, bottom_pos, 0)
            p3 = (right_pos, top_pos, height)
            p4 = (left_pos, top_pos, height)

            # 更新几何数据
            geometry_info = {
                'name': structure['name'],
                'type': structure['type'],
                'wall_type': wall_type,
                'front_room': front_room,
                'back_room': back_room,
                'points': [p1, p2, p3, p4]
            }

            if structure['type'] == 'thermal active':
                # 判断并调整外墙的前表面朝向
                if (front_room == 0 or front_room == -1) and (back_room != 0 and back_room != -1):
                    # 前表面正确朝向室外或土壤，不需要调整
                    self.geometry_data.append(geometry_info)
                elif (back_room == 0 or back_room == -1) and (front_room != 0 and front_room != -1):
                    # 后表面朝向室外或土壤，交换前后表面，并反转顶点顺序
                    geometry_info['front_room'], geometry_info['back_room'] = back_room, front_room
                    geometry_info['points'] = [p4, p3, p2, p1]  # 反转顶点顺序
                    self.geometry_data.append(geometry_info)
                else:
                    # 对于内墙，不需要调整
                    self.geometry_data.append(geometry_info)
            else:
                # 热不活性的构件直接添加
                self.geometry_data.append(geometry_info)

    def output_geometry_info(self, output_file):
        """
        输出生成的几何信息到文件
        """
        with open(output_file, 'w') as file:
            file.write("NAME, TYPE, FRONT_ROOM, BACK_ROOM, POINT_1_X, POINT_1_Y, POINT_1_Z, ..., POINT_4_X, POINT_4_Y, POINT_4_Z\n")
            for geometry in self.geometry_data:
                line = [geometry['id'], geometry['type'], str(geometry['front_room']), str(geometry['back_room'])]
                for point in geometry['points']:
                    line.extend(map(str, point))
                file.write(", ".join(line) + "\n")

    def run(self):
        """
        主方法：读取轴网和建筑结构，检查一致性，生成几何信息，并输出
        """
      
        project_directory = self.project_directory
        grid_file = os.path.join(project_directory, 'building_axes.in')
        structure_file = os.path.join(project_directory, 'building_geometry.in')
        output_file = os.path.join(project_directory, 'building_geometry.dat')

        self.read_grid_definition(grid_file)
        self.read_building_structure(structure_file)
        self.check_consistency()  # 检查输入文件的一致性
        self.generate_geometry_info()
        self.output_geometry_info(output_file)

class Building(Plotable):
    def __init__(self, project_instance, title="default", exist_ok = False, **kwargs):

        super().__init__()
        
        self.title = title

        self.vertices = []
        self.vertice_number = 0

        self.walls = []
        self.spaces = []
        self.surfaces = dict()
        
        self.space_number   = 0
        self.wall_number    = 0
        self.surface_number = 0

        self.face_color_front = 'xkcd:beige'
        self.face_color_back  = 'xkcd:aqua'
        self.edge_color       = 'xkcd:olive'

        self.hidden = False

        self.project = project_instance
        self.materials = self.project.material_properties

        self.wall_structures = {}      # 墙体结构类型
        self.get_wall_structures()

        self.building_geometry = []    # 建筑几何模型
        self.status = 'empty'
        if not exist_ok :
            self.generate_formatted_input_files_of_building_geometry()
            
        else:
            self.read()


### Modeling by Editing Formatted Files
    def read(self):
        project_directory = self.project.directory
        building_directory = os.path.join(project_directory, self.title)
        building_directory_path = add_drive_to_path(building_directory)
        geometry_file = os.path.join(building_directory_path, 'building_geometry.dat')

        if os.path.isfile(geometry_file):
            self.read_building_geometry(geometry_file)
        else :
            self.status ='empty'
            print(f" The registered building is empty, that is , without \n {geometry_file}")

    def save(self):
        project_directory = self.project.directory
        building_directory = os.path.join(project_directory, self.title)
        building_directory_path = add_drive_to_path(building_directory)
        geometry_file = os.path.join(building_directory_path, 'building_geometry.dat')
        
        self.save_building_geometry(geometry_file)

    def generate_formatted_input_files_of_building_geometry(self):
        project_directory = self.project.directory
        building_directory = os.path.join(project_directory, self.title)
        project_directory_path  = add_drive_to_path(project_directory)
        building_directory_path = add_drive_to_path(building_directory)

        # 将所有符合条件的 .in 文件复制到此子目录   
        # 确保目标目录存在  
        os.makedirs(building_directory_path, exist_ok=True)  
        
        # 根据 title 确定要复制的文件类型  
        self.copy_formatted_input_files(project_directory_path, building_directory_path)

    #
    # To edit building_geometry formatted input-files, 
    # then,
    # it generate building_geometry.dat from files *.in 
    #
    def generate_building_geometry_from_in_to_dat(self):
        project_directory = self.project.project_directory
        building_directory = os.path.join(project_directory, self.title)
        building_directory_path = add_drive_to_path(building_directory)

        bi = BuildingInput(building_directory_path)
        bi.run()        
 
    def get_wall_structures(self):
        project_directory = self.project.directory
        building_directory = os.path.join(project_directory, self.title)
        building_directory_path = add_drive_to_path(building_directory)

        wall_file = os.path.join(building_directory_path, 'building_walls.in')
        self.read_wall_structures(wall_file)

        for k,v in self.wall_structures.items():
            print(f"{k} - {v}")

    # read self.building_geometry from building_geometry.dat
    def read_building_geometry(self, file_path):
        """
        读取建筑几何模型文件。
        文件格式示例：
        Name, TYPE, FRONT_ROOM, BACK_ROOM, POINT_1_X, POINT_1_Y, POINT_1_Z, ..., POINT_N_X, POINT_N_Y, POINT_N_Z
        WALL1, BRICK_WALL, 101, 0, 0, 0, 0, 10, 0, 0, 10, 10, 0, 0, 10, 0
        """

        with open(file_path, 'r') as file:
            next(file)  # 跳过头部
            for line in file:
                i = i + 1
                data = line.strip().split(',')
                structure_name = data[0].strip()  # 修改为字符串
                structure_type = data[1].strip()  # -1, 0, 1, 2, ...
                front_room = int(data[2].strip())
                back_room = int(data[3].strip())

                points = []
                for i in range(4, len(data), 3):
                    x = float(data[i])
                    y = float(data[i + 1])
                    z = float(data[i + 2])
                    points.append((x, y, z))
                
                # 确保多边形顶点按逆时针顺序排列
                points = self.ensure_counterclockwise(points)

                self.building_geometry.append({
                    'name': structure_name,
                    'type': structure_type,
                    'front_room': front_room,
                    'back_room': back_room,
                    'points': points
                })
           
    # dump self.building_geometry to building_geometry.dat
    def save_building_geometry(self, geometry_file):

        with open(geometry_file, 'w') as file:
            file.write("NAME, TYPE, FRONT_ROOM, BACK_ROOM, POINT_1_X, POINT_1_Y, POINT_1_Z, ..., POINT_4_X, POINT_4_Y, POINT_4_Z\n")
            for wall in self.building_geometry:
                line = [wall['name'], wall['type'], str(wall['front_room']), str(wall['back_room'])]
                for point in wall['points']:
                    line.extend(map(str, point))
                file.write(", ".join(line) + "\n")

    # create rooms according to self.building_geometry
    def create_rooms(self):
        for wall in self.building_geometry:
            self.addWall(label=wall['name'], shape=wall['points'], front=wall['front_room'], back=wall['back_room'])
 
    def read_wall_structures(self, file_path):
        """
        读取墙体结构类型文件。
        文件格式示例：
        WALL_ID, LAYER_1_THICKNESS, LAYER_1_MATERIAL, ..., FRONT_EMISSIVITY_VISIBLE, BACK_EMISSIVITY_VISIBLE,
        1, 0.2, 1, 0.15, 2, 0.9, 0.1, 0.8, 0.2
        """
        with open(file_path, 'r') as file:
            next(file)  # 跳过头部
            for line in file:
                data = line.strip().split(',')
                wall_id = data[0].strip()
                layers = []
                for i in range(1, len(data) - 2, 2):
                    thickness = float(data[i])
                    material_type = int(data[i + 1])
                    layers.append({'thickness': thickness, 'material_type': material_type})
                
                front_emissivity = float(data[-4])
                front_reflectivity = float(data[-3])
                back_emissivity = float(data[-2])
                back_reflectivity = float(data[-1])

                self.wall_structures[wall_id] = {
                    'layers': layers,
                    'front_emissivity': front_emissivity,
                    'back_emissivity':  back_emissivity,
                }

    def ensure_counterclockwise(self, points):
        """
        确保多边形顶点按逆时针顺序排列
        """
        # 计算多边形的法向量
        normal = np.cross(np.array(points[1]) - np.array(points[0]), np.array(points[2]) - np.array(points[0]))
        if normal[2] < 0:
            points.reverse()
        return points

    def copy_formatted_input_files(self, source_directory, target_directory):
        # 将所有符合条件的 .in 文件复制到此子目录   
        
        # 根据 title 确定要复制的文件类型  
        file_group = 'building_*.in' 
        
        # 遍历 project_directory 中的文件  
        for infile in os.listdir(source_directory):  
            if fnmatch.fnmatch(infile, file_group):  # 使用 fnmatch 进行文件名模式匹配  
                # 构建源文件的完整路径  
                source_file = os.path.join(source_directory, infile)  
                # 复制文件到 building_directory  
                shutil.copy(source_file, target_directory)
 

### For manipulating the model
    def __str__(self):
        info = ""
        info += f"There are {self.space_number} spaces in the building.\n"
        for space in self.spaces:
            info +=space.__str__()+'\n'
        info += f"A complete list of all vertices ( {self.vertice_number} ) : \n"
        for i,v in enumerate(self.vertices):
            info +=f"      {i} {v}\n"
        return info

    def print(self): print(self)

    def turn_off(self):
        self.hidden = True

    def turn_on(self):
        self.hidden = False

    def hide_surface(self,surface_label):
        if surface_label in self.surfaces.keys() :
            self.surfaces[surface_label].turn_off()

    def show_surface(self,surface_label):
        if surface_label in self.surfaces.keys() :
            self.surfaces[surface_label].turn_on()

    def hide_space(self,space_indice):
        for s in self.spaces:
            if s.iv == space_indice :
                s.turn_off()

    def show_surface(self,surface_label):
        if surface_label in self.surfaces.keys() :
            self.surfaces[surface_label].turn_on()

### For visualization
    def get_instance(self) : return self

    # def get_domain(self):
    #     if self.vertices != [] :
    #         return np.array([self.vertices.min(axis=0),  # min (x,y,z)
    #                          self.vertices.max(axis=0)]) # max (x,y,z)
    #     points = np.ones((0, 3))
    #     return np.array([points.min(axis=0), points.max(axis=0)])
    def get_domain(self):
        """
        :return   ndarray([min], [max])
        """
        if self.vertices != [] : 
            buidling_domain = np.vstack([ v for v in self.vertices])
        else:
            buidling_domain = np.ones((0, 3))

        points = np.vstack(( buidling_domain,))
        return np.array([points.min(axis=0), points.max(axis=0)])

    def iplot(self, style, ax, **kwargs):
        if self.hidden :
            return

        if self.spaces == [] :
            return

        for each in self.spaces:
            # print(each.iv)
            each.iplot(style, ax)

### Modeling by Functions
    def addWall(self, label='', shape=None, front=0, back=0,
                      front_emissivity_visible = 0.0, back_emissivity_visible = 0.0, **kwargs):

        self.wall_number += 1
        self.parse({'label':label, 'shape': shape, 'front':front, 'back':back, 
            'front_emissivity_visible': front_emissivity_visible,'back_emissivity_visible': back_emissivity_visible}, **kwargs)


    def parse(self, input, **kwargs):

        vertices, indices = self.add_vertice(input['shape'])

        iv = input['front']
        jv = input['back'] 

        wall = Wall(input['label'], self.wall_number, iv, jv, vertices, indices,
                    input['front_emissivity_visible'], input['back_emissivity_visible'])

        self.walls.append(wall)

        space_front = self.add_space( iv )
        space_back  = self.add_space( jv )

        # ip = self.wall_number
        # i = 2*ip-1
        # j = 2*ip

        s1 = space_front.add_front_surface( wall )
        s2 = space_back.add_back_surface( wall)

        # self.surfaces.append(s1)
        # self.surfaces.append(s2)
        self.surfaces[s1.label] = s1
        self.surfaces[s2.label] = s2
        self.surface_number += 2

    def add_vertice(self,shape):
        vertices = list()
        indices = list()
        for P in shape:
            k = self.contain_vertice(P)  
            if k < 0 :

                V = list(P)  # V, P 为两块内存的个独立指针
                i = self.vertice_number
                self.vertice_number += 1
                self.vertices.append(V)

            else :
                V = self.vertices[k]  # 获得指针
                i = k
            
            vertices.append(V)
            indices.append(i)

        return vertices, indices

    def add_space(self, iv):
        if not self.contain_space(iv) :
            space = Space( iv )
            self.spaces.append(space)
            self.space_number += 1
            return space

        else:
            for each in self.spaces:
                if each.iv == iv :
                    return each
        
    def get_space(self,iv):
        if not self.contain_space(iv) :
            return None

        for each in self.spaces :
            if each.iv == iv :
                return each
        
### Helper functions
    def contain_space(self, iv):
        iv_list = [each.iv for each in self.spaces ]
        return iv in iv_list

    def contain_vertice(self, P) :
        a = Point(*list(P))

        for k,v in enumerate(self.vertices) :
            b = Point(*list(v))
            if a == b :
                return k
        return -1

    def add_to_space(self, iv, surface):
        space = self.get_space(iv)
        if not space : 
            self.spaces += Space(iv,surfaces=[surface])
            self.index_space +=1
        else:
            space.surfaces += surface
        return self.index_space

    def box3D(self,W,H):
        # W,H,A,B,C,D = 1.0, 1.0, 0.3, 0.20, 0.50, 0.40
        rect_wall = Shape('rectangle',W,H)
        self.addWall(label='South', shape=rect_wall.transform( to = (W,0,0), angles=(  0,  0)), front=0, back=1)
        self.addWall(label='East',  shape=rect_wall.transform( to = (W,W,0), angles=( 90,  0)), front=0, back=1)
        self.addWall(label='North' ,shape=rect_wall.transform( to = (0,W,0), angles=(180,  0)), front=0, back=1)
        self.addWall(label='West',  shape=rect_wall.transform( to = (0,0,0), angles=(270,  0)), front=0, back=1)
        self.addWall(label='top',   shape=rect_wall.transform( to = (W,0,H), angles=(  0, 90)), front=0, back=1)  
        self.addWall(label='bottom',shape=rect_wall.transform( to = (0,0,0), angles=(  0,-90)), front=0, back=1)

        return self

    def shift(self,dx,dy,dz):
        dv = [dx,dy,dz]
        for V in self.vertices :
            V[0] = V[0] + dv[0]
            V[1] = V[1] + dv[1]
            V[2] = V[2] + dv[2]


    def initialize(self):
        self.explode_inputs()
        self.view_factors()

    def explode_inputs(self):

        ip,iv_max = 0,0
        for each in self.walls:
            front = each['front']
            back  = each['back'] 

            # i = 2*ip-1
            # j = 2*ip

            i  = self.add_to_surfaces(front,ip)
            j  = self.add_to_surfaces(back,-ip)
            iv = self.add_to_space(front,i)
            jv = self.add_to_space(back,j)

            if front > iv_max : iv_max = front
            if  back > iv_max : iv_max = back
            
            ip += 1

        iv_max +=2

        if jv != iv_max :
            raise ValueError("Inputs are wrong")

    def view_factors(self):
        pass

def test():
    b = Building()
    print(b)

    W,H,A,B,C,D = 1.0, 0.5, 0.3, 0.20, 0.50, 0.40
    shape1 = Shape('rectangle',W,H,A,B,C,D)
    b.addWall(label='first',shape=shape1, front=0, back=1)
    print(b)

    shape2 = shape1.transform( to = (0,0,0), angles=(45,0))
    b.addWall(label='second',shape=shape2, front=1, back=2)
    b.print()

    b.plot(hideAxes=True)
    b.show()

def demoSpace():
    space = Space(7)
    print(space)

if __name__ == '__main__':
    test()