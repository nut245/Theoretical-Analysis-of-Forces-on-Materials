import math
import openpyxl
from tkinter import filedialog

RESOLUTION = 100 # create values of equal distance, up to the ultimate tensile strength of a substance

"""
Ultimate Tensile Strength: maximum stress that a material can withstand while being stretched or pulled before breaking.

Yield Strength: a measurement to determine the maximum stress that can be applied before permanent shape change is achieved in ductile materials. 

Max Elongation: when the relative velocity of the two masses is zero, but then both masses will have the velocity of the centre of mass.

Elongation/Young's Modulus: a property of the material that tells us how easily it can stretch and deform
"""

class Value_Table_Computer():
    def __init__(self, substanceProperties):
        # instantiation of necessary variables
        self.resolution = RESOLUTION

        try:
            self.oYS = substanceProperties["Yield_Strength"]
            self.oUTS = substanceProperties["Ultimate_Tensile_Strength"]
            self.E = substanceProperties["Youngs_Modulus"]
            self.eMAX = substanceProperties["Max_Elongation"]
        except ValueError:
            print("values in substance properties not found")

        self.value_table = {
        # strain : stress,
        }

        # performance of logic within respective methods
        self.n = self.Parameter_n()

        self.calculate_value_table()

    def calculate_value_table(self):
        interval = self.oUTS / self.resolution
        stress = 0
        while stress <= self.oUTS - interval:
            try:
                strain = self.H_N_Hill_Equation(o=stress)

                stress += interval

                self.value_table[round(strain,7)] = round(stress, 3)
            except:
                pass # some values may suffer from rounding errors, and are uncomputable

    def H_N_Hill_Equation(self, o):
        """
        Returns strain value (ε/e (float): represents total strain), given varying stress
        
        Parameters:
            o (float): signifies stress (σ)
            E (float): stands for Young's Modulus
            oYS (float): yield strength (σYS)
            n (float): material-dependent constants
        """
        try:
            return (o / self.E) + (0.002 * math.pow(o / self.oYS, self.n))
        except ValueError:
            print("(math domain error) Ultimate strength must be greater than yield strength!")
    
    def Parameter_n(self):
        """
        Returns parameter n, to be fed into H_N_Hill_Equation

        oUTS (float): Ultimate Tensile Strength (σUTS)
        eMAX (float): Maximum Elongation (εmax)
        oYS (float): yield strength (σYS)
        """
        try:
            return (math.log((self.eMAX - (self.oUTS/self.E)) / 0.002)) / (math.log(self.oUTS / self.oYS))
        except ValueError:
            print("(math domain error) Elastic modulus is too small compared to the strength!")

    def Strain_Value_at_Yield_Strength(self):
        """
        oYS (float): yield strength (σYS)
        E (float): stands for Young's Modulus
        """
        return (self.oYS / self.E) + 0.002
    
    def Strain_Value_at_Ultimate_Strength(self):
        """
        oUTS (float): Ultimate Tensile Strength (σUTS)
        E (float): stands for Young's Modulus
        eMAX (float): Maximum Elongation (εmax)
        """
        return (self.oUTS / self.E) + self.eMAX

class DataImporter():
    def __init__(self, valueTableComputer):
        # instantiation of necessary variables
        self.substanceProperties = {}

        # performance of logic within respective methods
        self.parse_properties()

        self.valueTableComputer = valueTableComputer(self.substanceProperties)

        self.completeValueTable = self.valueTableComputer.value_table

    def open_file(self):
        return filedialog.askopenfilename().replace('/', '//')
    
    def parse_properties(self):
        with open(self.open_file(), 'r') as file:
            for line in file:
                try:
                    key, value = line.split(" = ")
                    key, value = str(key.strip()), float(value.strip())
                    self.substanceProperties[key] = value
                except:
                    pass # there was an empty row or something in the text file, not to worry

class ExcelExporter():
    def __init__(self, dataImporter):
        # instantiation of necessary variables
        self.dataImporter = dataImporter

        self.data = [
            ["Strain", "Stress", None, "Strain Yield Strength", "Stress Yield Strength", None, "Strain Ultimate Strength", "Stress Ultimate Strength", None, "Young's Modulus"], # row 1
            
            [ # row 2
                None, None, None, # columns 1 - 3
            
                self.dataImporter.valueTableComputer.H_N_Hill_Equation(self.dataImporter.substanceProperties["Ultimate_Tensile_Strength"]), # columns 4 - 5
                self.dataImporter.substanceProperties["Ultimate_Tensile_Strength"], 
                
                None, 
                
                self.dataImporter.valueTableComputer.H_N_Hill_Equation(self.dataImporter.substanceProperties["Yield_Strength"]), # columns 6 - 7
                self.dataImporter.substanceProperties["Yield_Strength"],

                None,

                self.dataImporter.substanceProperties["Youngs_Modulus"]
            ]
        ]

        # performance of logic within respective methods
        self.fill_data()

        self.export_to_excel()
        
    def fill_data(self):
        for key, value in self.dataImporter.completeValueTable.items():
            self.data.append([key, value])

    def export_to_excel(self):
        workbook = openpyxl.Workbook()
        sheet = workbook.active
        for row in self.data:
            sheet.append(row)

        try:
            workbook.save(filename="Plotting\SubstanceStressStrainCurve.xlsx")
            print("Excel file created successfully!")
        except:
            print("unable to save to excel, file still open")


if __name__ == '__main__':
    ExcelExporter(DataImporter(Value_Table_Computer))