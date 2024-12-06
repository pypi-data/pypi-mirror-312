import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
import pandas as pd
import time
import os


class PlateBendingKirchhoffClass:
    def __init__(
        self,
        E,
        t,
        a,
        b,
        p0,
        x0,
        u,
        y0,
        v,
        nu=0.0,
        kappa_s=5 / 6,
        K=0,
        n_inte=50,
        loading="Regular",
        support="hhhh",
        reihen=8,
    ):
        """
        Initialisierung der Klasse PlateBendingKirchhoff.

        Args:
            E (float): Elastizitätsmodul.
            t (float): Dicke der Platte.
            a (float): Länge der Platte in x-Richtung.
            b (float): Länge der Platte in y-Richtung.
            p0 (float): Maximale Last.
            x0 (float): Startpunkt der Last in x-Richtung.
            u (float): Breite der Last in x-Richtung.
            y0 (float): Startpunkt der Last in y-Richtung.
            v (float): Breite der Last in y-Richtung.
            nu (float, optional): Querdehnzahl. Standardmäßig 0.0.
            kappa_s (float, optional): Schubkorrekturfaktor. Standardmäßig 5/6.
            K (int, optional): Torsionssteifigkeit. Standardmäßig 0.
            n_inte (int, optional): Anzahl der Integrationspunkte. Standardmäßig 50.
            loading (str, optional): Art der Belastung. Standardmäßig "Regular".
            support (str, optional): Lagerungsbedingungen. Standardmäßig "hhhh".
            reihen (int, optional): Anzahl der Reihen für die Reihenentwicklung. Standardmäßig 8.
        """
        # Materialien
        self.E = E
        self.nu = nu
        self.kappa_s = kappa_s
        self.K = K
        # Plattenabmessungen in [m]
        self.t = t
        self.a = a
        self.b = b

        self.n_inte = n_inte

        self.list_a = np.linspace(0, self.a, self.n_inte)
        self.list_b = np.linspace(0, self.b, self.n_inte)

        # Belastung
        self.p0 = p0
        self.x0 = x0
        self.u = u
        self.y0 = y0
        self.v = v

        self.loading = loading

        # Steifigkeitsmatrix-Komponenten
        self.D_11 = E * t**3 / (12 * (1 - nu**2))
        self.D_22 = self.D_11
        self.D_12 = self.D_11 * nu
        self.D_66 = (1 - nu) / 2 * self.D_11

        self.support = support

        self.reihen = reihen

        self.mat = np.zeros((self.reihen**2, self.reihen**2))

        self.load = np.zeros((self.reihen**2))

    def CalculateAll(self):
        """
        Führt alle Berechnungsschritte aus.
        """
        self.AssembleStiffnessMatrix()
        self.Construct_Loadvector()
        self.ReduceMatrix()
        self.SolveSystem()
        self.TransformSolutionMatrix()

    def AssembleStiffnessMatrix(self):
        """
        Berechnung der Steifigkeitsmatrix für die Plattenstruktur mit dem C++-Modul via pybind11.
        """
        # Sicherstellen, dass das C++-Modul importiert werden kann
        try:
            import plate_bending_cpp
        except ImportError as e:
            print("Fehler beim Import des C++-Moduls:", e)
            raise

        # Aufruf der assemble_stiffness_matrix-Funktion aus dem C++-Modul
        self.mat = plate_bending_cpp.assemble_stiffness_matrix(
            self.D_11, self.D_22, self.D_12, self.D_66,
            self.reihen, self.n_inte, self.a, self.b, self.support
        )
        self.mat = np.array(self.mat)  # Konvertierung in ein NumPy-Array

    def Construct_Loadvector(self):
        """
        Konstruktion des Lastvektors basierend auf der aufgebrachten Belastung.
        """
        # Hier nehmen wir an, dass die Belastungsdaten direkt in der Klasse verfügbar sind
        # Wenn Sie die Belastungsdaten aus einer Datei lesen möchten, passen Sie diesen Teil entsprechend an

        # Beispielhafte Definition der Rechtecklasten
        # In der Praxis sollten diese Daten aus Ihrer Anwendung oder Datenquelle stammen
        rectangular_loads = [
            # [x0, x1, y0, y1, p0]
            [self.x0, self.x0 + self.u, self.y0, self.y0 + self.v, self.p0]
        ]

        for load in rectangular_loads:
            x0, x1, y0, y1, p0 = load

            # Sicherstellen, dass die Last innerhalb der Plattenabmessungen liegt
            x0 = max(0, min(self.a, x0))
            x1 = max(0, min(self.a, x1))
            y0 = max(0, min(self.b, y0))
            y1 = max(0, min(self.b, y1))

            list_load_inte_x = np.linspace(x0, x1, 100)
            list_load_inte_y = np.linspace(y0, y1, 100)
            for m in range(1, self.reihen + 1):
                for n in range(1, self.reihen + 1):
                    # Integration über die Lastfläche
                    omega_1m = np.trapz(self.function_1(list_load_inte_x, m), list_load_inte_x)
                    omega_1n = np.trapz(self.function_2(list_load_inte_y, n), list_load_inte_y)

                    self.load[n - 1 + self.reihen * (m - 1)] += p0 * omega_1m * omega_1n

    def function_1(self, x, m):
        if self.support == "hhhh":
            return np.sin(x * np.pi / self.a * m)
        else:
            # Andere Unterstützungsbedingungen können hier implementiert werden
            return np.zeros_like(x)

    def function_2(self, y, n):
        if self.support == "hhhh":
            return np.sin(y * np.pi / self.b * n)
        else:
            # Andere Unterstützungsbedingungen können hier implementiert werden
            return np.zeros_like(y)

    def ReduceMatrix(self):
        """
        Reduziert die Matrix und den Lastvektor, um Nullzeilen und -spalten zu entfernen.
        """
        # Prüfen, welche Zeilen und Spalten nur Nullen enthalten
        non_zero_rows = ~np.all(self.mat == 0, axis=1)
        non_zero_cols = ~np.all(self.mat == 0, axis=0)

        # Reduziere die Matrix und den Vektor, um nur Nicht-Null Zeilen und Spalten zu behalten
        self.reduced_mat = self.mat[non_zero_rows, :][:, non_zero_cols]
        self.reduced_load = self.load[non_zero_rows]

    def SolveSystem(self):
        """
        Löst das reduzierte Gleichungssystem.
        """
        if self.reduced_mat.size > 0:
            self.x_reduced = np.linalg.solve(self.reduced_mat, self.reduced_load)
        else:
            print("Keine Lösung möglich, da das Gleichungssystem nur Nullen enthält.")

    def TransformSolutionMatrix(self):
        """
        Transformiert die Lösungsvektoren in eine Matrixform.
        """
        # Berechnen der Dimension der quadratischen Matrix
        n = int(np.sqrt(len(self.x_reduced)))

        if n**2 != len(self.x_reduced):
            raise ValueError("Die Länge von x_reduced ist nicht das Quadrat einer ganzen Zahl")

        # Umstrukturieren des Vektors x_reduced in eine quadratische n x n Matrix
        self.matrix = self.x_reduced.reshape(n, n)

    def SolutionPointDisp(self, a_sol, b_sol):
        """
        Berechnet die Durchbiegung an einem bestimmten Punkt (a_sol, b_sol).
        """
        x_disp = 0.0
        if self.support == "hhhh":
            for m in range(1, self.reihen + 1):
                for n in range(1, self.reihen + 1):
                    x_disp += (
                        self.matrix[m - 1][n - 1]
                        * self.function_1(a_sol, m)
                        * self.function_2(b_sol, n)
                    )
        else:
            # Andere Unterstützungsbedingungen können hier implementiert werden
            pass

        return x_disp

    def SolutionPointMomentx(self, a_sol, b_sol):
        """
        Berechnet den Biegemoment mxx an einem bestimmten Punkt (a_sol, b_sol).
        """
        mxx = 0.0
        if self.support == "hhhh":
            for m in range(1, self.reihen + 1):
                for n in range(1, self.reihen + 1):
                    mxx += self.matrix[m - 1][n - 1] * (
                        -self.D_11 * self.function_1xx(a_sol, m) * self.function_2(b_sol, n)
                        - self.D_12 * self.function_2yy(b_sol, n) * self.function_1(a_sol, m)
                    )
        else:
            # Andere Unterstützungsbedingungen können hier implementiert werden
            pass

        return mxx

    def SolutionPointMomenty(self, a_sol, b_sol):
        """
        Berechnet den Biegemoment myy an einem bestimmten Punkt (a_sol, b_sol).
        """
        myy = 0.0
        if self.support == "hhhh":
            for m in range(1, self.reihen + 1):
                for n in range(1, self.reihen + 1):
                    myy += self.matrix[m - 1][n - 1] * (
                        -self.D_12 * self.function_1xx(a_sol, m) * self.function_2(b_sol, n)
                        - self.D_22 * self.function_2yy(b_sol, n) * self.function_1(a_sol, m)
                    )
        else:
            # Andere Unterstützungsbedingungen können hier implementiert werden
            pass

        return myy

    def function_1xx(self, x, m):
        if self.support == "hhhh":
            return -np.sin(x * np.pi / self.a * m) * (np.pi / self.a * m) ** 2
        else:
            return np.zeros_like(x)

    def function_2yy(self, y, n):
        if self.support == "hhhh":
            return -np.sin(y * np.pi / self.b * n) * (np.pi / self.b * n) ** 2
        else:
            return np.zeros_like(y)

    def PlotLoad(self):
        """
        Plottet die aufgebrachte Belastung auf der Platte.
        """
        x_values = [0, self.a, self.a, 0, 0]
        y_values = [0, 0, self.b, self.b, 0]

        # Beispielhafte Lasten (dies sollte an Ihre Anwendung angepasst werden)
        rectangular_loads = [
            # [x0, x1, y0, y1]
            [self.x0, self.x0 + self.u, self.y0, self.y0 + self.v]
        ]

        for load in rectangular_loads:
            x0, x1, y0, y1 = load
            x = [x0, x1, x1, x0, x0]
            y = [y0, y0, y1, y1, y0]
            plt.plot(x, y)

        plt.plot(x_values, y_values)
        plt.gca().set_aspect('equal', adjustable='box')
        plt.show(block=False)
        plt.pause(2)
        plt.close()

    def PlotMomentGrid(self, grid_size=20):
        """
        Berechnet und plottet ein Raster der Momentenverläufe.

        Args:
            grid_size (int): Anzahl der Unterteilungen in x- und y-Richtung. Standardmäßig 20.
        """
        x_values = np.linspace(0, self.a, grid_size)
        y_values = np.linspace(0, self.b, grid_size)
        self.mx_values = np.zeros((grid_size, grid_size))
        self.my_values = np.zeros((grid_size, grid_size))

        for i, x in enumerate(x_values):
            for j, y in enumerate(y_values):
                self.mx_values[i][j] = self.SolutionPointMomentx(x, y)
                self.my_values[i][j] = self.SolutionPointMomenty(x, y)

        print("Max-Moment x in [kNm]", self.mx_values.max() * 1000)
        print("Min-Moment x in [kNm]", self.mx_values.min() * 1000)
        print("Max-Moment y in [kNm]", self.my_values.max() * 1000)
        print("Min-Moment y in [kNm]", self.my_values.min() * 1000)

        X, Y = np.meshgrid(x_values, y_values)
        fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
        surf = ax.plot_surface(
            X, Y, self.mx_values, cmap=cm.coolwarm, linewidth=0, antialiased=False
        )
        ax.set_title('Moment Mx')
        plt.show(block=False)
        plt.pause(6)
        plt.close()

        fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
        surf = ax.plot_surface(
            X, Y, self.my_values, cmap=cm.coolwarm, linewidth=0, antialiased=False
        )
        ax.set_title('Moment My')
        plt.show(block=False)
        plt.pause(6)
        plt.close()




