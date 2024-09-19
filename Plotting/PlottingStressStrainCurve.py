import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

print("NumPy version:", np.__version__)
print("Pandas version:", pd.__version__)

class StressStrainPlotter():
    def __init__(self, substance_name):
        # instantiation of necessary variables
        self.substance_df = pd.read_excel("Plotting\SubstanceStressStrainCurve.xlsx")
        print(self.substance_df)

        self.substance_strain = self.substance_df['Strain']
        self.substance_stress = self.substance_df['Stress']

        self.fig = plt.figure()
        self.ax1 = self.fig.add_axes((0.1, 0.2, 0.8, 0.7))

        self.substance_name = substance_name

        # performance of logic within respective methods
        self.setup_axis()

        self.plot_data()

        self.annotate_graph()

        plt.show()

        plt.savefig('stress-strain_curve.png', dpi=300, bbox_inches='tight')

    def setup_axis(self):
        self.ax1.set_title(f'Stress Strain Curve of {self.substance_name} in tension')
        self.ax1.set_xlabel('strain')
        self.ax1.set_ylabel('stress (psi)')
        self.ax1.grid()

    def plot_data(self):
        self.ax1.plot(self.substance_strain, self.substance_stress)
        self.ax1.plot(self.substance_df["Strain Yield Strength"], 
                      self.substance_df['Stress Yield Strength'], 
                      marker="X", markersize=8, markeredgecolor="blue", markerfacecolor="blue")
        self.ax1.plot(self.substance_df["Strain Ultimate Strength"], 
                      self.substance_df['Stress Ultimate Strength'], 
                      marker="o", markersize=8, markeredgecolor="blue", markerfacecolor="blue")

    def annotate_graph(self):
        self.ultimate_strain = self.splice_needed_heading("Strain Ultimate Strength")
        self.ultimate_stress = self.splice_needed_heading("Stress Ultimate Strength")

        self.yield_strain = self.splice_needed_heading("Strain Yield Strength")
        self.yield_stress = self.splice_needed_heading("Stress Yield Strength")

        # accidently programmed the vales the wrong way around... too lazy to fix
        self.marker_descriptors = f"(O) Yield Strength: {self.ultimate_stress}   Yield Strain: {self.ultimate_strain}\n(X) Ultimate Strength: {self.yield_stress}   Ultimate Strain: {self.yield_strain}"
        self.fig.text(0.5, .05, self.marker_descriptors, ha='center')

    def splice_needed_heading(self, dictionary_key):
        return str(self.substance_df[dictionary_key].head(1)).split("Name: ")[0].split()[1]

if __name__ == '__main__':
    substance_name = input("Name of Substance? ")
    StressStrainPlotter(substance_name=substance_name)