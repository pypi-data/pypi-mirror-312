import numpy as np
from VisualShape3D.geometry import *
from VisualShape3D.VisualShape3D import VisualShape3D

import json

class Material:
    def __init__(self, name, density, capacity, conductivity):
        self.name = name
        self.density = density
        self.capacity = capacity
        self.conductivity = conductivity

    def to_dict(self):
        return vars(self)

class Layer:
    def __init__(self, material, thickness):
        self.material = material
        self.thickness = thickness

    def to_dict(self):
        return {'material': self.material.to_dict(), 'thickness': self.thickness}

class Surface :
    def __init__(self, visible, infrared):
        self.visible = visible
        self.infrared = infrared

    def to_dict(self):
        return vars(self)

class Struct:
    def __init__(self, layers, front_surface, back_surface):
        self.layers = layers
        self.front_surface = front_surface
        self.back_surface = back_surface

    def to_dict(self):
        return {
            'layers': [layer.to_dict() for layer in self.layers],
            'front_surface': self.front_surface.to_dict(),
            'back_surface': self.back_surface.to_dict()
        }

    @staticmethod
    def from_dict(struct_dict):
        layers = [Layer(Material(**layer['material']), layer['thickness']) for layer in struct_dict['layers']]
        front_surface = Surface(**struct_dict['front_surface'])
        back_surface = Surface(**struct_dict['back_surface'])
        return Struct(layers, front_surface, back_surface)

class StructureManager:
    def __init__(self, filename):
        self.filename = filename

    def append_structure(self, struct):
        with open(self.filename, 'a') as file:
            file.write(json.dumps(struct.to_dict()) + "\n")

    def load_structures(self):
        structures = []
        with open(self.filename, 'r') as file:
            for line in file:
                struct_dict = json.loads(line)
                structures.append(Struct.from_dict(struct_dict))
        return structures

class Building(VisualShape3D):
    def __init__(self, style = None):
        super().__init__


def demo():
    # 创建材料、层和结构
    concrete = Material("Concrete", 2.4, 840, 1.4)
    insulation = Material("Insulation", 0.04, 1000, 0.03)
    layer1 = Layer(concrete, 0.2)
    layer2 = Layer(insulation, 0.05)
    
    # 创建前后表面
    front_surface = Surface(0.5, 0.7)
    back_surface = Surface(0.6, 0.8)

    # 创建结构并包含表面信息
    wall = Struct([layer1, layer2], front_surface, back_surface)

    # 保存结构到文件
    manager = StructureManager('structures.jsonl')
    manager.append_structure(wall)

    # 从文件加载结构
    loaded_structures = manager.load_structures()
    for struct in loaded_structures:
        print("Loaded Struct:")
        for layer in struct.layers:
            print(f"  Material: {layer.material.name}, Thickness: {layer.thickness}")
        print(f"  Front Surface: Visible={struct.front_surface.visible}, Infrared={struct.front_surface.infrared}")
        print(f"  Back Surface: Visible={struct.back_surface.visible}, Infrared={struct.back_surface.infrared}")

if __name__ == '__main__':
    demo()
