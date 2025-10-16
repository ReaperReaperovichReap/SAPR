import tkinter as tk
import tkinter.messagebox as messagebox
import tkinter.filedialog as filedialog
import numpy as np
import matplotlib
import json
from tkinter import ttk

matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

class ComputerMechanicsGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Плоская стержневая система")

        self.support_left_vars = []
        self.support_right_vars = []

        self.point_load_side_vars = []
        self.point_load_side_right_buttons = []
        self.point_load_side_left_buttons = []

        self.create_widgets()

        self.axis.clear()
        self.axis.set_title("Плоская стержневая конструкция")
        self.axis.set_xlabel("Длина, м")
        self.axis.set_ylabel("Высота, м")
        self.axis.axis('equal')
        self.axis.grid()

        first_length = self.parse_number(self.length_entries[0].get())
        x = np.cumsum([0, first_length])
        self.axis.plot(x, [0] * (len(x)), 'k-')
        self.canvas.draw()
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def on_closing(self):
        plt.close('all')
        self.quit()
        self.destroy()

    def create_widgets(self):
        self.length_entries = []
        self.area_entries = []
        self.e_modulus_entries = []
        self.allowable_stress_entries = []
        self.point_load_entries = []
        self.distributed_load_entries = []
        self.delete_buttons = []

        self.length_labels = []
        self.area_labels = []
        self.e_modulus_labels = []
        self.allowable_stress_labels = []
        self.point_load_labels = []
        self.distributed_load_labels = []

        self.add_member_button = tk.Button(self, text="+", command=self.add_member)
        self.add_member_button.grid(row=0, column=7)

        self.add_member_row(1)

        self.update_button = tk.Button(self, text="Обновить", command=self.update_visualization)
        self.update_button.grid(row=19, column=0, columnspan=14)

        self.save_button = tk.Button(self, text="Сохранить", command=self.save_to_json)
        self.save_button.grid(row=19, column=8, columnspan=2)

        self.load_button = tk.Button(self, text="Загрузить", command=self.load_from_json)
        self.load_button.grid(row=19, column=10, columnspan=2)

        self.calculate_button = tk.Button(self, text="Рассчитать", command=self.calculate)
        self.calculate_button.grid(row=19, column=12, columnspan=2)

        self.section_label = tk.Label(self, text="Координата сечения:")
        self.section_label.grid(row=20, column=0)
        self.section_entry = tk.Entry(self, width=10)
        self.section_entry.grid(row=20, column=1)
        self.section_button = tk.Button(self, text="Рассчитать сечение", command=self.calculate_section)
        self.section_button.grid(row=20, column=2)

        self.figure, self.axis = plt.subplots(figsize=(8, 6))
        self.canvas = FigureCanvasTkAgg(self.figure, self)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=21, column=0, columnspan=14)

    def add_member_row(self, row):
        length_entry = tk.Entry(self, width=10)
        length_entry.grid(row=row, column=0)
        length_label = tk.Label(self, text="Длина, м")
        length_label.grid(row=row, column=1)
        self.length_entries.append(length_entry)
        self.length_labels.append(length_label)

        area_entry = tk.Entry(self, width=10)
        area_entry.grid(row=row, column=2)
        area_label = tk.Label(self, text="Площадь, м²")
        area_label.grid(row=row, column=3)
        self.area_entries.append(area_entry)
        self.area_labels.append(area_label)

        e_modulus_entry = tk.Entry(self, width=10)
        e_modulus_entry.grid(row=row, column=4)
        e_modulus_label = tk.Label(self, text="Модуль упругости, Па")
        e_modulus_label.grid(row=row, column=5)
        self.e_modulus_entries.append(e_modulus_entry)
        self.e_modulus_labels.append(e_modulus_label)

        allowable_stress_entry = tk.Entry(self, width=10)
        allowable_stress_entry.grid(row=row, column=6)
        allowable_stress_label = tk.Label(self, text="Допускаемое напряжение, Па")
        allowable_stress_label.grid(row=row, column=7)
        self.allowable_stress_entries.append(allowable_stress_entry)
        self.allowable_stress_labels.append(allowable_stress_label)

        support_left_var = tk.BooleanVar()
        support_right_var = tk.BooleanVar()
        support_left_checkbox = tk.Checkbutton(self, text="⊣", variable=support_left_var)
        support_right_checkbox = tk.Checkbutton(self, text="⊢", variable=support_right_var)

        support_left_checkbox.grid(row=row, column=8)
        support_right_checkbox.grid(row=row, column=9)

        self.support_left_vars.append(support_left_var)
        self.support_right_vars.append(support_right_var)

        point_load_entry = tk.Entry(self, width=10)
        point_load_entry.grid(row=row, column=10)
        point_load_label = tk.Label(self, text="Сосредоточенная нагрузка, Н")
        point_load_label.grid(row=row, column=11)
        self.point_load_entries.append(point_load_entry)
        self.point_load_labels.append(point_load_label)

        point_load_side_var = tk.StringVar(value="right")
        point_load_side_right = tk.Radiobutton(self, text="→", variable=point_load_side_var, value="right")
        point_load_side_left = tk.Radiobutton(self, text="←", variable=point_load_side_var, value="left")

        point_load_side_right.grid(row=row, column=12)
        point_load_side_left.grid(row=row, column=13)

        self.point_load_side_vars.append(point_load_side_var)
        self.point_load_side_right_buttons.append(point_load_side_right)
        self.point_load_side_left_buttons.append(point_load_side_left)

        distributed_load_entry = tk.Entry(self, width=10)
        distributed_load_entry.grid(row=row, column=14)
        distributed_load_label = tk.Label(self, text="Распределенная нагрузка, Н/м")
        distributed_load_label.grid(row=row, column=15)
        self.distributed_load_entries.append(distributed_load_entry)
        self.distributed_load_labels.append(distributed_load_label)

        delete_button = tk.Button(self, text="-", command=lambda r=row: self.delete_member(r))
        delete_button.grid(row=row, column=16)
        self.delete_buttons.append(delete_button)

    def delete_member(self, row):
        if len(self.length_entries) > 1:
            index = row - 1

            # Удаление всех виджетов, связанных с элементом
            widgets_to_destroy = [
                self.length_entries[index], self.length_labels[index],
                self.area_entries[index], self.area_labels[index],
                self.e_modulus_entries[index], self.e_modulus_labels[index],
                self.allowable_stress_entries[index], self.allowable_stress_labels[index],
                self.support_left_vars[index], self.support_right_vars[index],
                self.point_load_entries[index], self.point_load_labels[index],
                self.point_load_side_right_buttons[index],
                self.point_load_side_left_buttons[index],
                self.distributed_load_entries[index],
                self.distributed_load_labels[index],
                self.delete_buttons[index]
            ]

            for widget in widgets_to_destroy:
                if hasattr(widget, 'destroy'):
                    widget.destroy()

            # Удаление элементов из списков
            del self.length_entries[index]
            del self.length_labels[index]
            del self.area_entries[index]
            del self.area_labels[index]
            del self.e_modulus_entries[index]
            del self.e_modulus_labels[index]
            del self.allowable_stress_entries[index]
            del self.allowable_stress_labels[index]
            del self.support_left_vars[index]
            del self.support_right_vars[index]
            del self.point_load_entries[index]
            del self.point_load_labels[index]
            del self.point_load_side_vars[index]
            del self.point_load_side_right_buttons[index]
            del self.point_load_side_left_buttons[index]
            del self.distributed_load_entries[index]
            del self.distributed_load_labels[index]
            del self.delete_buttons[index]

            # Перемещение виджетов
            for i in range(index, len(self.length_entries)):
                self.length_entries[i].grid(row=i + 1, column=0)
                self.length_labels[i].grid(row=i + 1, column=1)
                self.area_entries[i].grid(row=i + 1, column=2)
                self.area_labels[i].grid(row=i + 1, column=3)
                self.e_modulus_entries[i].grid(row=i + 1, column=4)
                self.e_modulus_labels[i].grid(row=i + 1, column=5)
                self.allowable_stress_entries[i].grid(row=i + 1, column=6)
                self.allowable_stress_labels[i].grid(row=i + 1, column=7)
                self.point_load_entries[i].grid(row=i + 1, column=10)
                self.point_load_labels[i].grid(row=i + 1, column=11)
                self.point_load_side_right_buttons[i].grid(row=i + 1, column=12)
                self.point_load_side_left_buttons[i].grid(row=i + 1, column=13)
                self.distributed_load_entries[i].grid(row=i + 1, column=14)
                self.distributed_load_labels[i].grid(row=i + 1, column=15)

                self.delete_buttons[i].configure(command=lambda r=i + 1: self.delete_member(r))
                self.delete_buttons[i].grid(row=i + 1, column=16)

            self.update_visualization()

    def add_member(self):
        self.add_member_row(len(self.length_entries) + 1)
        self.update_visualization()

    def parse_number(self, value):
        if not value.strip():
            return 0
        try:
            return float(value.strip().lower().replace('e', 'e+').replace('е', 'e+'))
        except ValueError:
            return 0

    def update_visualization(self):
        if not any(left_var.get() or right_var.get() for left_var, right_var in
                   zip(self.support_left_vars, self.support_right_vars)):
            tk.messagebox.showwarning("Внимание", "Необходимо установить хотя бы одну опору в конструкции!")
            return

        self.lengths = [self.parse_number(entry.get()) for entry in self.length_entries]
        self.areas = [self.parse_number(entry.get()) for entry in self.area_entries]
        self.e_modulus = [self.parse_number(entry.get()) for entry in self.e_modulus_entries]
        self.allowable_stress = [self.parse_number(entry.get()) for entry in self.allowable_stress_entries]
        self.point_loads = [self.parse_number(entry.get()) for entry in self.point_load_entries]
        self.distributed_loads = [self.parse_number(entry.get()) for entry in self.distributed_load_entries]

        self.axis.clear()
        self.axis.set_title("Плоская стержневая конструкция")
        self.axis.set_xlabel("Длина, м")
        self.axis.set_ylabel("Высота, м")
        self.axis.axis('equal')
        self.axis.grid()

        x = np.cumsum([0] + self.lengths)
        self.axis.plot(x, [0] * (len(x)), 'k-')

        for i, (left_support, right_support) in enumerate(zip(self.support_left_vars, self.support_right_vars)):
            if left_support.get():
                self.axis.plot([x[i], x[i]], [0, 0.5], 'r-', linewidth=3)
            if right_support.get():
                self.axis.plot([x[i + 1], x[i + 1]], [0, 0.5], 'r-', linewidth=3)

        for i, (load, side) in enumerate(zip(self.point_loads, self.point_load_side_vars)):
            if load != 0:
                if side.get() == "right":
                    self.axis.plot([x[i + 1]], [0], 'r>' if load > 0 else 'b<')
                    self.axis.text(x[i + 1], 0.5, f"{load:.1f} кН", va='bottom', ha='center')
                else:
                    self.axis.plot([x[i]], [0], 'r>' if load < 0 else 'b<')
                    self.axis.text(x[i], 0.5, f"{load:.1f} кН", va='bottom', ha='center')

        for i, load in enumerate(self.distributed_loads):
            if load != 0:
                self.axis.plot([x[i], x[i + 1]], [0, 0], 'g-')
                self.axis.text((x[i] + x[i + 1]) / 2, 0.5, f"{load:.1f} кН/м", va='bottom', ha='center')

        self.canvas.draw()

    def save_to_json(self):
        data = {
            "lengths": [self.parse_number(entry.get()) for entry in self.length_entries],
            "areas": [self.parse_number(entry.get()) for entry in self.area_entries],
            "e_modulus": [self.parse_number(entry.get()) for entry in self.e_modulus_entries],
            "allowable_stress": [self.parse_number(entry.get()) for entry in self.allowable_stress_entries],
            "left_support": [var.get() for var in self.support_left_vars],
            "right_support": [var.get() for var in self.support_right_vars],
            "point_loads": [self.parse_number(entry.get()) for entry in self.point_load_entries],
            "distributed_loads": [self.parse_number(entry.get()) for entry in self.distributed_load_entries],
            "point_load_directions": [var.get() for var in self.point_load_side_vars]
        }

        filename = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            title="Сохранить конструкцию"
        )

        if filename:
            try:
                with open(filename, "w", encoding="utf-8") as f:
                    json.dump(data, f, ensure_ascii=False, indent=4)

                messagebox.showinfo("Успех", f"Данные сохранены в файл {filename}")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось сохранить файл: {e}")

    def load_from_json(self):
        filename = filedialog.askopenfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            title="Загрузить конструкцию"
        )

        if filename:
            try:
                with open(filename, "r", encoding="utf-8") as f:
                    data = json.load(f)

                while len(self.length_entries) > 1:
                    self.delete_member(len(self.length_entries))

                self.length_entries[0].delete(0, tk.END)
                self.length_entries[0].insert(0, str(data['lengths'][0]))
                self.area_entries[0].delete(0, tk.END)
                self.area_entries[0].insert(0, str(data['areas'][0]))
                self.e_modulus_entries[0].delete(0, tk.END)
                self.e_modulus_entries[0].insert(0, str(data['e_modulus'][0]))
                self.allowable_stress_entries[0].delete(0, tk.END)
                self.allowable_stress_entries[0].insert(0, str(data['allowable_stress'][0]))
                self.support_left_vars[0].set(data['left_support'][0])
                self.support_right_vars[0].set(data['right_support'][0])
                self.point_load_entries[0].delete(0, tk.END)
                self.point_load_entries[0].insert(0, str(data['point_loads'][0]))
                self.distributed_load_entries[0].delete(0, tk.END)
                self.distributed_load_entries[0].insert(0, str(data['distributed_loads'][0]))
                self.point_load_side_vars[0].set(data['point_load_directions'][0])

                for i in range(1, len(data['lengths'])):
                    self.add_member()
                    self.length_entries[i].delete(0, tk.END)
                    self.length_entries[i].insert(0, str(data['lengths'][i]))
                    self.area_entries[i].delete(0, tk.END)
                    self.area_entries[i].insert(0, str(data['areas'][i]))
                    self.e_modulus_entries[i].delete(0, tk.END)
                    self.e_modulus_entries[i].insert(0, str(data['e_modulus'][i]))
                    self.allowable_stress_entries[i].delete(0, tk.END)
                    self.allowable_stress_entries[i].insert(0, str(data['allowable_stress'][i]))
                    self.support_left_vars[i].set(data['left_support'][i])
                    self.support_right_vars[i].set(data['right_support'][i])
                    self.point_load_entries[i].delete(0, tk.END)
                    self.point_load_entries[i].insert(0, str(data['point_loads'][i]))
                    self.distributed_load_entries[i].delete(0, tk.END)
                    self.distributed_load_entries[i].insert(0, str(data['distributed_loads'][i]))
                    self.point_load_side_vars[i].set(data['point_load_directions'][i])

                self.update_visualization()

                messagebox.showinfo("Успех", f"Конструкция загружена из файла {filename}")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось загрузить файл: {e}")

    def calculate(self):
        input_data = {
            "lengths": [self.parse_number(entry.get()) for entry in self.length_entries],
            "areas": [self.parse_number(entry.get()) for entry in self.area_entries],
            "e_modulus": [self.parse_number(entry.get()) for entry in self.e_modulus_entries],
            "allowable_stress": [self.parse_number(entry.get()) for entry in self.allowable_stress_entries],
            "left_support": [var.get() for var in self.support_left_vars],
            "right_support": [var.get() for var in self.support_right_vars],
            "point_loads": [self.parse_number(entry.get()) for entry in self.point_load_entries],
            "distributed_loads": [self.parse_number(entry.get()) for entry in self.distributed_load_entries],
            "point_load_directions": [var.get() for var in self.point_load_side_vars]
        }

        rod_system = RodSystem(input_data)
        results = rod_system.calculate_results()

        post_processor = PostProcessor(results, self.figure, self.canvas)

        post_processor.generate_results_file()
        post_processor.display_results_in_table()
        post_processor.plot_result_graphs(results['rod_results'])

        print("Calculation Results:")
        for rod in results['rod_results']:
            print(f"\nRod {rod['rod_index']}:")
            print(f"  Start Ux: {rod['start_displacement']:.6f}")
            print(f"  End Displacement: {rod['end_displacement']:.6f}")
            print(f"  Nx at End: {rod['axial_force_start']:.6f}")
            print(f"  Nx at Start: {rod['axial_force_end']:.6f}")
            print(f"  Normal Stress at End: {rod['normal_stress_start']:.6f}")
            print(f"  Normal Stress at Start: {rod['normal_stress_end']:.6f}")

    def calculate_section(self):
        section_coordinate = self.parse_number(self.section_entry.get())
        input_data = {
            "lengths": [self.parse_number(entry.get()) for entry in self.length_entries],
            "areas": [self.parse_number(entry.get()) for entry in self.area_entries],
            "e_modulus": [self.parse_number(entry.get()) for entry in self.e_modulus_entries],
            "allowable_stress": [self.parse_number(entry.get()) for entry in self.allowable_stress_entries],
            "left_support": [var.get() for var in self.support_left_vars],
            "right_support": [var.get() for var in self.support_right_vars],
            "point_loads": [self.parse_number(entry.get()) for entry in self.point_load_entries],
            "distributed_loads": [self.parse_number(entry.get()) for entry in self.distributed_load_entries],
            "point_load_directions": [var.get() for var in self.point_load_side_vars]
        }

        rod_system = RodSystem(input_data)
        section_results = rod_system.calculate_section_results(section_coordinate)

        if section_results:
            messagebox.showinfo("Результаты расчёта сечения",
                                f"Координата сечения: {section_coordinate}\n"
                                f"Перемещение: {section_results['displacement']:.6f}\n"
                                f"Осевая сила(Nx): {section_results['axial_force']:.6f}\n"
                                f"Нормальное напряжение: {section_results['normal_stress']:.6f}")
        else:
            messagebox.showerror("Ошибка", "Не удалось рассчитать сечение.")

class RodSystem:
    def __init__(self, input_data):
        self.lengths = np.array(input_data.get('lengths', []))
        self.areas = np.array(input_data.get('areas', []))
        self.e_modulus = np.array(input_data.get('e_modulus', []))
        self.allowable_stress = np.array(input_data.get('allowable_stress', []))
        self.left_support = np.array(input_data.get('left_support', []))
        self.right_support = np.array(input_data.get('right_support', []))
        self.point_loads = np.array(input_data.get('point_loads', []))
        self.distributed_loads = np.array(input_data.get('distributed_loads', []))
        self.point_load_directions = input_data.get('point_load_directions', [])

        self.num_rods = len(self.lengths)

        self.validate_input_data()

    def validate_input_data(self):
        arrays = [
            ('areas', self.areas),
            ('e_modulus', self.e_modulus),
            ('allowable_stress', self.allowable_stress),
            ('left_support', self.left_support),
            ('right_support', self.right_support),
            ('point_loads', self.point_loads),
            ('distributed_loads', self.distributed_loads),
            ('point_load_directions', self.point_load_directions)
        ]

        for name, arr in arrays:
            if len(arr) != self.num_rods:
                raise ValueError(f"Array '{name}' must have the same length as 'lengths' ({self.num_rods}).")

    def calculate_stiffness_matrix(self):
        k_global = np.zeros((self.num_rods + 1, self.num_rods + 1))

        for i in range(self.num_rods):
            k_rod = (self.e_modulus[i] * self.areas[i]) / self.lengths[i]

            k_global[i, i] += k_rod
            k_global[i + 1, i + 1] += k_rod
            k_global[i, i + 1] -= k_rod
            k_global[i + 1, i] -= k_rod

        return k_global

    def calculate_load_vector(self):
        load_vector = np.zeros(self.num_rods + 1)

        for i in range(self.num_rods):
            if self.point_loads[i] != 0:
                if self.point_load_directions[i] == 'left':
                    load_vector[i] += self.point_loads[i]
                else:
                    load_vector[i + 1] += self.point_loads[i]

            if self.distributed_loads[i] != 0:
                eq_force = self.distributed_loads[i] * self.lengths[i]
                load_vector[i] += eq_force / 2
                load_vector[i + 1] += eq_force / 2

        return load_vector

    def solve_displacement(self):
        k_global = self.calculate_stiffness_matrix()
        load_vector = self.calculate_load_vector()

        k_modified = k_global.copy()
        load_modified = load_vector.copy()

        for i in range(self.num_rods):
            if self.left_support[i]:
                node_index = i
                k_modified[node_index, :] = 0
                k_modified[:, node_index] = 0
                k_modified[node_index, node_index] = 1.0
                load_modified[node_index] = 0.0

            if self.right_support[i]:
                node_index = i + 1
                k_modified[node_index, :] = 0
                k_modified[:, node_index] = 0
                k_modified[node_index, node_index] = 1.0
                load_modified[node_index] = 0.0

        displacements = np.linalg.solve(k_modified, load_modified)

        return displacements

    def calculate_rod_forces(self, displacements):
        rod_forces = []

        for i in range(self.num_rods):
            k_rod = (self.e_modulus[i] * self.areas[i]) / self.lengths[i]
            delta = displacements[i + 1] - displacements[i]
            N = k_rod * delta
            q = self.distributed_loads[i]

            if q != 0:
                N_start = N + (q * self.lengths[i] / 2)
                N_end = N - (q * self.lengths[i] / 2)
            else:
                N_start = N
                N_end = N

            rod_forces.append({
                'start': N_start,
                'end': N_end
            })
        return rod_forces

    def calculate_stress(self, rod_forces):
        rod_stresses = []

        for i in range(self.num_rods):
            stress_start = rod_forces[i]['start'] / self.areas[i]
            stress_end = rod_forces[i]['end'] / self.areas[i]

            rod_stresses.append({
                'start': stress_start,
                'end': stress_end
            })
        return rod_stresses

    def calculate_rod_results(self):
        displacements = self.solve_displacement()
        rod_forces = self.calculate_rod_forces(displacements)
        rod_stresses = self.calculate_stress(rod_forces)

        rod_results = []
        for i in range(self.num_rods):
            rod_results.append({
                'rod_index': i + 1,
                'length': self.lengths[i],
                'start_displacement': displacements[i],
                'end_displacement': displacements[i + 1],
                'axial_force_start': rod_forces[i]['start'],
                'axial_force_end': rod_forces[i]['end'],
                'normal_stress_start': rod_stresses[i]['start'],
                'normal_stress_end': rod_stresses[i]['end'],
                'allowable_stress': self.allowable_stress[i]  # Добавлено допускаемое напряжение
            })

        return rod_results

    def calculate_results(self):
        rod_results = self.calculate_rod_results()
        return {
            'rod_results': rod_results
        }

    def calculate_section_results(self, section_coordinate):
        displacements = self.solve_displacement()
        rod_forces = self.calculate_rod_forces(displacements)
        rod_stresses = self.calculate_stress(rod_forces)

        cumulative_lengths = np.cumsum([0] + list(self.lengths))
        rod_index = np.searchsorted(cumulative_lengths, section_coordinate, side='right') - 1

        if rod_index < 0 or rod_index >= self.num_rods:
            return None

        local_coordinate = section_coordinate - cumulative_lengths[rod_index]

        displacement = np.interp(local_coordinate, [0, self.lengths[rod_index]],
                                  [displacements[rod_index], displacements[rod_index + 1]])
        axial_force = np.interp(local_coordinate, [0, self.lengths[rod_index]],
                                 [rod_forces[rod_index]['start'], rod_forces[rod_index]['end']])
        normal_stress = np.interp(local_coordinate, [0, self.lengths[rod_index]],
                                   [rod_stresses[rod_index]['start'], rod_stresses[rod_index]['end']])

        return {
            'displacement': displacement,
            'axial_force': axial_force,
            'normal_stress': normal_stress
        }

class PostProcessor:
    def __init__(self, results, figure, canvas):
        self.results = results
        self.figure = figure
        self.canvas = canvas
        self.ax_force = self.figure.add_subplot(311)
        self.ax_stress = self.figure.add_subplot(312)
        self.ax_displacement = self.figure.add_subplot(313)

    def generate_results_file(self, filename='results.json'):
        with open(filename, 'w') as f:
            json.dump(self.results, f, indent=4)
        print(f"Results exported to '{filename}'")

    def display_results_in_table(self):
        table_window = tk.Toplevel()
        table_window.title("Результаты расчёта")

        tree = ttk.Treeview(table_window)

        tree["columns"] = ("Rod Index", "Start Displacement", "End Displacement", "Axial Force Start", "Axial Force End", "Normal Stress Start", "Normal Stress End", "Allowable Stress")

        tree.column("#0", width=0, stretch=tk.NO)
        tree.column("Rod Index", anchor=tk.CENTER, width=80)
        tree.column("Start Displacement", anchor=tk.CENTER, width=120)
        tree.column("End Displacement", anchor=tk.CENTER, width=120)
        tree.column("Axial Force Start", anchor=tk.CENTER, width=120)
        tree.column("Axial Force End", anchor=tk.CENTER, width=120)
        tree.column("Normal Stress Start", anchor=tk.CENTER, width=120)
        tree.column("Normal Stress End", anchor=tk.CENTER, width=120)
        tree.column("Allowable Stress", anchor=tk.CENTER, width=120)

        tree.heading("#0", text="", anchor=tk.CENTER)
        tree.heading("Rod Index", text="Индекс стержня")
        tree.heading("Start Displacement", text="Начальное перемещение")
        tree.heading("End Displacement", text="Конечное перемещение")
        tree.heading("Axial Force Start", text="Осевая сила (начало)")
        tree.heading("Axial Force End", text="Осевая сила (конец)")
        tree.heading("Normal Stress Start", text="Нормальное напряжение (начало)")
        tree.heading("Normal Stress End", text="Нормальное напряжение (конец)")
        tree.heading("Allowable Stress", text="Допускаемое напряжение")

        tree.tag_configure("red_text", foreground="red")

        for rod in self.results['rod_results']:
            normal_stress_start = rod['normal_stress_start']
            normal_stress_end = rod['normal_stress_end']
            allowable_stress = rod['allowable_stress']

            tags = []
            if allowable_stress < normal_stress_start or allowable_stress < normal_stress_end:
                tags.append("red_text")

            tree.insert("", "end", values=(
                rod['rod_index'],
                f"{rod['start_displacement']:.6f}",
                f"{rod['end_displacement']:.6f}",
                f"{rod['axial_force_start']:.6f}",
                f"{rod['axial_force_end']:.6f}",
                f"{rod['normal_stress_start']:.6f}",
                f"{rod['normal_stress_end']:.6f}",
                f"{rod['allowable_stress']:.6f}"
            ), tags=tags)

        tree.pack(expand=True, fill=tk.BOTH)

    def plot_result_graphs(self, results):
        x = np.cumsum([0] + [res['length'] for res in results])

        graph_window = tk.Toplevel()
        graph_window.title("Графики результатов")

        fig, axs = plt.subplots(1, 3, figsize=(18, 6))
        canvas = FigureCanvasTkAgg(fig, master=graph_window)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        forces = [res['axial_force_start'] for res in results] + [results[-1]['axial_force_end']]
        axs[0].step(x, forces, where='post', linewidth=2, color='blue')
        axs[0].fill_between(x, forces, step="post", alpha=0.3, color='blue')
        axs[0].set_title('Эпюра продольной силы Nx', pad=20, fontsize=12)
        axs[0].set_ylabel('Сила, Н', fontsize=10)
        axs[0].grid(True)

        stresses = [res['normal_stress_start'] for res in results] + [results[-1]['normal_stress_end']]
        axs[1].step(x, stresses, where='post', linewidth=2, color='green')
        axs[1].fill_between(x, stresses, step="post", alpha=0.3, color='green')
        axs[1].set_title('Эпюра напряжений σx', pad=20, fontsize=12)
        axs[1].set_ylabel('Напряжение, Па', fontsize=10)
        axs[1].grid(True)

        displacements = [res['start_displacement'] for res in results] + [results[-1]['end_displacement']]
        axs[2].plot(x, displacements, linewidth=2, color='red')
        axs[2].fill_between(x, displacements, alpha=0.3, color='red')
        axs[2].set_title('Эпюра перемещений ux', pad=20, fontsize=12)
        axs[2].set_xlabel('Длина конструкции, м', fontsize=10)
        axs[2].set_ylabel('Перемещение, м', fontsize=10)
        axs[2].grid(True)

        canvas.draw()

        tree.pack(expand=True, fill=tk.BOTH)

    def plot_result_graphs(self, results):
        x = np.cumsum([0] + [res['length'] for res in results])

        graph_window = tk.Toplevel()
        graph_window.title("Графики результатов")

        fig, axs = plt.subplots(1, 3, figsize=(18, 6))
        canvas = FigureCanvasTkAgg(fig, master=graph_window)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        forces = [res['axial_force_start'] for res in results] + [results[-1]['axial_force_end']]
        axs[0].step(x, forces, where='post', linewidth=2, color='blue')
        axs[0].fill_between(x, forces, step="post", alpha=0.3, color='blue')
        axs[0].set_title('Эпюра продольной силы Nx', pad=20, fontsize=12)
        axs[0].set_ylabel('Сила, Н', fontsize=10)
        axs[0].grid(True)

        stresses = [res['normal_stress_start'] for res in results] + [results[-1]['normal_stress_end']]
        axs[1].step(x, stresses, where='post', linewidth=2, color='green')
        axs[1].fill_between(x, stresses, step="post", alpha=0.3, color='green')
        axs[1].set_title('Эпюра напряжений σx', pad=20, fontsize=12)
        axs[1].set_ylabel('Напряжение, Па', fontsize=10)
        axs[1].grid(True)

        displacements = [res['start_displacement'] for res in results] + [results[-1]['end_displacement']]
        axs[2].plot(x, displacements, linewidth=2, color='red')
        axs[2].fill_between(x, displacements, alpha=0.3, color='red')
        axs[2].set_title('Эпюра перемещений ux', pad=20, fontsize=12)
        axs[2].set_xlabel('Длина конструкции, м', fontsize=10)
        axs[2].set_ylabel('Перемещение, м', fontsize=10)
        axs[2].grid(True)

        canvas.draw()


    def plot_result_graphs(self, results):
        x = np.cumsum([0] + [res['length'] for res in results])

        graph_window = tk.Toplevel()
        graph_window.title("Графики результатов")

        fig, axs = plt.subplots(1, 3, figsize=(18, 6))
        canvas = FigureCanvasTkAgg(fig, master=graph_window)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        forces = [res['axial_force_start'] for res in results] + [results[-1]['axial_force_end']]
        axs[0].step(x, forces, where='post', linewidth=2, color='blue')
        axs[0].fill_between(x, forces, step="post", alpha=0.3, color='blue')
        axs[0].set_title('Эпюра продольной силы Nx', pad=20, fontsize=12)
        axs[0].set_ylabel('Сила, Н', fontsize=10)
        axs[0].grid(True)

        stresses = [res['normal_stress_start'] for res in results] + [results[-1]['normal_stress_end']]
        axs[1].step(x, stresses, where='post', linewidth=2, color='green')
        axs[1].fill_between(x, stresses, step="post", alpha=0.3, color='green')
        axs[1].set_title('Эпюра напряжений σx', pad=20, fontsize=12)
        axs[1].set_ylabel('Напряжение, Па', fontsize=10)
        axs[1].grid(True)

        displacements = [res['start_displacement'] for res in results] + [results[-1]['end_displacement']]
        axs[2].plot(x, displacements, linewidth=2, color='red')
        axs[2].fill_between(x, displacements, alpha=0.3, color='red')
        axs[2].set_title('Эпюра перемещений ux', pad=20, fontsize=12)
        axs[2].set_xlabel('Длина конструкции, м', fontsize=10)
        axs[2].set_ylabel('Перемещение, м', fontsize=10)
        axs[2].grid(True)

        canvas.draw()

if __name__ == "__main__":
    app = ComputerMechanicsGUI()
    app.mainloop()
