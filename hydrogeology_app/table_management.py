import tkinter as tk
from tkinter import ttk
import os
import pandas as pd
from hydrogeology_app.calculadora import HydrogeologyCalculator
from hydrogeology_app.funciones_figuras import (
    mifflin_graphic,
    gibbs_graphic,
    piper_graphic,
    stiff_graphic,
)


class TableManagement:
    """
    A class to manage the display, filtering, and exportation of table data within a hydrogeology application.

    Attributes:
    -----------
    app_hydrogeology : HydrogeologyApp
        An instance of the HydrogeologyApp class, which manages the main application and provides necessary
        functionality and data access.
    df_data : pd.DataFrame
        The DataFrame containing the data to be managed and displayed in the table.
    frame_table : Frame
        The frame that contains the table widget.
    data_tree : pd.DataFrame
        A copy of the data used for manipulation and filtering within the table.
    treeview : Treeview
        The Treeview widget used to display the table data.
    combobox_group : Combobox
        A Combobox widget used for selecting the column to group the data by.
    combobox_color : Combobox
        A Combobox widget used for selecting the column to color the data by.
    """

    def __init__(self, app_hydrogeology, df_data) -> None:
        """
        Initialize the TableManagement class with the hydrogeology application context and data.

        Parameters:
        -----------
        app_hydrogeology : HydrogeologyApp
            An instance of the HydrogeologyApp class that manages the main application.
        df_data : pd.DataFrame
            The DataFrame containing the data to be managed and displayed in the table.
        """
        self.app_hydrogeology = app_hydrogeology
        self.df_data = df_data
        self.frame_table = None
        self.data_tree = None
        self.treeview = None
        self.combobox_group = None
        self.combobox_color = None

    def generate_table(self):
        """
        Generate and display the table of data, including controls for filtering, deleting, and exporting data.

        This method creates the table within the application window, setting up the necessary buttons, scrollbars,
        and Treeview widget. It also configures the columns based on the provided data and adds functionality for
        grouping, coloring, and exporting the displayed data.
        """
        frame_buttons = tk.Frame(self.app_hydrogeology.canvas_frame)
        filter_button = tk.Button(
            frame_buttons,
            text="Filtrar Datos",
            command=self.create_calculator,
        )
        filter_button.grid(row=0, column=0, sticky="w")
        button_delete_selected = tk.Button(
            frame_buttons,
            text="Eliminar Seleccionados",
            command=self.remove_selected,
        )
        button_delete_selected.grid(row=0, column=2, sticky="w")
        self.app_hydrogeology.canvas_frame.create_window(
            (10, 390), window=frame_buttons, anchor="nw"
        )
        self.app_hydrogeology.ajustar_xpadx(frame_buttons, 5)
        self.frame_table = tk.Frame(self.app_hydrogeology.canvas_frame)
        self.frame_table.grid(row=0, column=0, sticky="nsew")
        self.frame_table.config(width=1200)
        canvas = tk.Canvas(self.frame_table)

        canvas.grid(row=0, column=0, sticky="nsew")
        canvas.config(width=1200)
        horizontal_scroll = tk.Scrollbar(
            self.frame_table, orient="horizontal", command=canvas.xview
        )
        horizontal_scroll.grid(row=1, column=0, sticky="nsew")
        frame_treeview = tk.Frame(canvas)
        frame_treeview.pack()
        canvas.create_window((0, 0), window=frame_treeview, anchor="nw")
        self.treeview = ttk.Treeview(
            frame_treeview
        )
        self.treeview.pack()
        data_copy = self.df_data.copy()
        self.data_tree = self.df_data.copy()
        self.treeview["columns"] = tuple(["ID"] + data_copy.columns.to_list())
        self.treeview.column("#0", width=0, stretch=tk.NO)
        self.treeview.heading("#0", text="")
        if len(data_copy) > 0:
            self.treeview.column("ID", width=50, anchor=tk.CENTER)
            self.treeview.heading("ID", text="ID")
        else:
            self.treeview.column("ID", width=1200, anchor=tk.CENTER)
        for column in data_copy.columns.to_list():
            length = max(
                [
                    data_copy[column].astype(str).str.len().max() * 10 + 10,
                    len(column) * 10 + 10,
                ]
            )
            self.treeview.column(column, width=length, anchor=tk.CENTER)
            self.treeview.heading(column, text=column)
        self.insert_data()
        frame_treeview.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))

        # Asegurar que el Treeview se ajuste al redimensionar la ventana
        frame_treeview.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        export_frame = tk.Frame(self.app_hydrogeology.canvas_frame)
        self.combobox_group = self.app_hydrogeology.generate_combobox(
            export_frame, "Seleccionar Columna Agrupación: ", 0, 2
        )
        self.combobox_color = self.app_hydrogeology.generate_combobox(
            export_frame, "Seleccionar Columna Color: ", 0, 4
        )
        frame_buttons = tk.Frame(self.app_hydrogeology.canvas_frame)
        button_figures = tk.Button(
            frame_buttons,
            text="Generar figures",
            command=self.export_figures,
        )
        button_figures.grid(row=0, column=0, sticky="w")
        button_export_excel = tk.Button(
            frame_buttons,
            text="Exportar Excel",
            command=self.export_excel,
        )
        button_export_excel.grid(row=0, column=3, sticky="w")
        self.app_hydrogeology.ajustar_xpadx(frame_buttons, 5)
        self.app_hydrogeology.ajustar_xpadx(export_frame, 5)
        self.app_hydrogeology.canvas_frame.create_window(
            (1000, 390), window=frame_buttons, anchor="nw"
        )
        group_columns = self.df_data.columns.to_list()
        data_column = [
            "Error %",
            "Total Aniones (meq/L)",
            "Total Cationes (meq/L)",
            "Nitratos (meq/L)",
            "Bicarbonato (meq/L)",
            "Carbonato (meq/L)",
            "Sulfatos (meq/L)",
            "Cloruros (meq/L)",
            "Potasio (meq/L)",
            "Sodio (meq/L)",
            "Magnesio (meq/L)",
            "Calcio (meq/L)",
            "Sulfatos (mg/L)",
            "Sodio (mg/L)",
            "Potasio (mg/L)",
            "Nitratos (mg/L)",
            "Magnesio (mg/L)",
            "Cloruros (mg/L)",
            "Carbonato (mg/L)",
            "Calcio (mg/L)",
            "Bicarbonato (mg/L)",
        ]
        grouped_columns = list(set(group_columns).difference(set(data_column)))
        self.app_hydrogeology.populate_combo_frame(export_frame, grouped_columns)
        self.app_hydrogeology.canvas_frame.create_window(
            (570, 375), window=export_frame, anchor="nw"
        )
        self.app_hydrogeology.canvas_frame.create_window((10,425), window=self.frame_table, anchor="nw")

    def insert_data(self):
        """
        Insert data into the Treeview widget from the provided DataFrame.

        Parameters:
        -----------
        data_copy : pd.DataFrame
            The DataFrame containing the data to be inserted into the Treeview for display.
        """
        print(self.df_data)
        if len(self.df_data) > 0:
            self.df_data.index = [str(indice) for indice in self.df_data.index.tolist()]
            self.df_data[self.app_hydrogeology.combobox_date.get()] = pd.to_datetime(
                self.df_data[self.app_hydrogeology.combobox_date.get()]
            ).dt.strftime("%Y-%m-%d")
            for dato in self.df_data.to_records().tolist():
                self.treeview.insert("", tk.END, values=dato)

    def remove_selected(self):
        """
        Remove the selected rows from the Treeview widget and the underlying data.

        This method deletes the currently selected rows in the Treeview and updates the internal DataFrame to
        reflect the deletions.
        """
        selected = self.treeview.selection()
        for item in selected:
            row_id = self.treeview.item(item)["values"][0]
            self.data_tree.drop(index=row_id, inplace=True)
            self.treeview.delete(item)

    def export_excel(self):
        """
        Export the current data in the table to an Excel file.

        This method prompts the user to select a save location and filename, and then exports the data
        displayed in the Treeview to an Excel file at the specified location.
        """
        file_location = tk.filedialog.asksaveasfilename(
            defaultextension=".xlsx", filetypes=[("Archivos de Excel", "*.xlsx")]
        )
        if file_location:
            self.data_tree.to_excel(file_location, index=False)

    def export_figures(self):
        """
        Generate and export hydrogeological figures (Mifflin, Gibbs, Piper, Stiff) based on the current data.

        This method prompts the user to select a directory for saving the generated figures, then creates and
        saves the Mifflin, Gibbs, Piper, and Stiff diagrams using the data in the table. The figures are saved
        as image files in the selected directory.
        """
        folder_path = tk.filedialog.askdirectory()
        if folder_path:
            try:
                colgrup = self.combobox_group.get()
                colgrup = colgrup if colgrup != "" else None
                colcolor = self.combobox_color.get()
                colcolor = colcolor if colcolor != "" else None
                col_date = self.app_hydrogeology.combobox_date.get()
                figure_data = self.data_tree.copy()
                figure_data[col_date] = pd.to_datetime(figure_data[col_date])
                figure_mifflin = mifflin_graphic(
                    self.data_tree, col_style=colgrup, col_color=colcolor
                )
                figure_gibbs = gibbs_graphic(
                    self.data_tree, col_style=colgrup, col_color=colcolor
                )
                figure_pipper = piper_graphic(
                    self.data_tree, col_style=colgrup, col_color=colcolor
                )
                figure_mifflin.savefig(
                    os.path.join(folder_path, "fig_mifflin.jpg"), dpi=400
                )
                figure_gibbs.savefig(
                    os.path.join(folder_path, "fig_gibbs.jpg"), dpi=400
                )
                figure_pipper.savefig(
                    os.path.join(folder_path, "fig_pipper.jpg"), dpi=400
                )
                figures_stiff = stiff_graphic(
                    figure_data, self.app_hydrogeology.combobox_point.get(), col_date
                )
                for punto, fig in figures_stiff.items():
                    fig.savefig(os.path.join(folder_path, f"fig_stiff{punto}.jpg"))
                tk.messagebox.showinfo(
                    "Finalización", "La generación de figures termino con exito"
                )
            except Exception as e:
                # Muestra una ventana de mensaje de error con el mensaje de la excepción
                tk.messagebox.showerror("Error", f"Ocurrió un error: {str(e)}")

    def create_calculator(self):
        """
        Create and display the calculator interface for filtering data.

        This method initializes and opens a calculator window that allows the user to apply complex filters
        and expressions to the data displayed in the table.
        """
        calculator = HydrogeologyCalculator(self)
        calculator.create_calculator()

