import tkinter as tk
import re



class HydrogeologyCalculator:
    """
    A class to manage and evaluate expressions within a hydrogeology application, using a GUI-based interface
    for selecting fields, applying filters, and calculating results.

    Attributes:
    -----------
    app_table_management : TableManagement
        An instance of the TableManagement class, which manages the table data and provides access to necessary
        data structures such as treeview and data_tree.
    listbox_fields : tk.Listbox
        A Listbox widget used for displaying and selecting fields.
    listbox_uniques : tk.Listbox
        A Listbox widget used for displaying unique values of the selected field.
    entry_formula : tk.Entry
        An Entry widget used for inputting and displaying the expression to be evaluated.
    comparators : list
        A list of comparison operators used in expressions.
    grouping : str
        A string representing grouping symbols, such as parentheses.
    operators : list
        A list of logical operators used in expressions.
    calculator_window : tk.Toplevel
        The top-level window for the calculator interface.
    """

    def __init__(self, app_table_mananegement):
        """
        Initialize the HydrogeologyCalculator with the necessary application context.

        Parameters:
        -----------
        app_table_management : TableManagement
            An instance of the TableManagement class, providing access to data and treeview management.
        """
        self.app_table_mananegement = app_table_mananegement
        self.listbox_fields = None
        self.listbox_uniques = None
        self.entry_formula = None
        self.comparators = ["=", "<>", ">", ">=", "<", "<=", "In", "Like", "Not"]
        self.grouping = "()"
        self.operators = ["Or", "And"]
        self.calculator_window = None

    def get_unique_values(self):
        """
        Populate the listbox with unique values of the selected field.

        This method retrieves the selected field from the fields listbox, finds its unique values in the
        dataset managed by TableManagement, and displays those unique values in the unique values listbox.
        """
        selected_index = self.listbox_fields.curselection()
        selected_values = [self.listbox_fields.get(i) for i in selected_index]
        if len(selected_values) > 0:
            self.listbox_uniques.delete(0, tk.END)
            field = selected_values[0]
            field = field.replace('"', "")
            values = self.app_table_mananegement.data_tree[field].unique().tolist()
            self.listbox_uniques.config(state="normal")
            for value in values:
                self.listbox_uniques.insert(tk.END, f'"{value}"')

    def clear_uniques(self, _):
        """
        Clear the unique values listbox.

        This method clears the unique values listbox and disables it when no field is selected.
        Triggered by an event.
        """
        self.listbox_uniques.delete(0, tk.END)
        self.listbox_uniques.config(state="disabled")

    def add_unique_text(self, _):
        """
        Insert the selected unique value into the expression.

        This method inserts the currently selected unique value from the unique values listbox
        into the expression entry at the current cursor position.
        Triggered by a double-click event.
        """
        text = self.listbox_uniques.get(self.listbox_uniques.curselection())
        cursor_position = self.entry_formula.index(tk.INSERT)
        self.entry_formula.insert(cursor_position, text)

    def add_field_text(self, _):
        """
        Insert the selected field into the expression.

        This method inserts the currently selected field from the fields listbox
        into the expression entry at the current cursor position.
        Triggered by a double-click event.
        """
        text = self.listbox_fields.get(self.listbox_fields.curselection())
        cursor_position = self.entry_formula.index(tk.INSERT)
        self.entry_formula.insert(cursor_position, f"[${text}]")

    def click_button(self, text):
        """
        Insert a specified text into the expression.

        This method inserts the provided text (e.g., an operator or grouping symbol)
        into the expression entry at the current cursor position.

        Parameters:
        -----------
        text : str
            The text to be inserted into the expression.
        """
        cursor_position = self.entry_formula.index(tk.INSERT)
        self.entry_formula.insert(cursor_position, text)

    def evaluate_expression(self, expression):
        """
        Evaluate the given expression against the dataset and select matching rows.

        This method parses and evaluates the expression by replacing field placeholders with actual values
        from the dataset. It then identifies the rows that satisfy the expression and selects them in the treeview.

        Parameters:
        -----------
        expression : str
            The expression to be evaluated against the dataset.
        """
        index = 0
        indices = []
        for row in self.app_table_mananegement.treeview.selection():
            self.app_table_mananegement.treeview.selection_remove(row)

        for _, row in self.app_table_mananegement.data_tree.iterrows():
            try:
                columns = re.findall(r'\[\$"(.*?)"\]', expression)
                row_expression = expression
                for column in columns:
                    if column not in row:
                        raise KeyError(f"Column '{column}' not found in the dataset.")
                    
                    value = row[column]
                    if isinstance(value, (int, float)):
                        row_expression = row_expression.replace(f'[$"{column}"]', str(value))
                    else:
                        row_expression = row_expression.replace(f'[$"{column}"]', f'"{str(value)}"')
                if eval(row_expression):
                    indices.append(int(index))

            except KeyError as e:
                print(f"KeyError: {e}")
            except SyntaxError as e:
                print(f"SyntaxError in the expression: {row_expression}. Error: {e}")
            except (TypeError, ValueError) as e:
                print(f"TypeError or ValueError: {e}")
        
            
            index += 1
        if not indices:
            print("No matching rows found.")


        return indices

    def select_rows(self):
        """
        Evaluate the expression entered by the user and select matching rows.

        This method retrieves the expression from the entry widget, evaluates it,
        and then selects the rows in the treeview that match the expression criteria.
        """
        expression = self.entry_formula.get()
        self.evaluate_expression(expression)

    def create_calculator(self):
        """
        Create and display the calculator window.

        This method sets up the calculator window, including the fields listbox,
        unique values listbox, operator buttons, and the entry widget for the expression.
        It initializes and places all necessary GUI components for the user to interact with.
        """
        self.calculator_window = tk.Toplevel(
            self.app_table_mananegement.app_hydrogeology.root
        )
        self.calculator_window.title("Calculator")
        self.calculator_window.geometry("500x600")
        available_fields = self.app_table_mananegement.data_tree.columns.tolist()

        self.listbox_fields = tk.Listbox(
            self.calculator_window, selectmode=tk.SINGLE, exportselection=0, height=5
        )
        for field in available_fields:
            self.listbox_fields.insert(tk.END, f'"{field}"')
        self.listbox_fields.place(relheight=0.25, relwidth=0.9, relx=0.05, rely=0.05)
        self.listbox_fields.bind("<<ListboxSelect>>", self.clear_uniques)
        self.listbox_fields.bind("<Double-Button-1>", self.add_field_text)

        button_frame = tk.Frame(self.calculator_window)
        button_frame.place(rely=0.32, relx=0.05, relwidth=0.4)

        button_equals = tk.Button(
            button_frame, text="==", width=5, command=lambda: self.click_button("==")
        )
        button_equals.grid(column=0, row=0, padx=2, pady=0.1)
        button_not_equals = tk.Button(
            button_frame, text="!=", width=5, command=lambda: self.click_button("!=")
        )
        button_not_equals.grid(column=1, row=0, padx=2, pady=0.1)
        button_like = tk.Button(
            button_frame,
            text="Like",
            width=5,
            command=lambda: self.click_button("Like"),
        )
        button_like.grid(column=2, row=0, padx=2, pady=0.1)

        button_greater = tk.Button(
            button_frame, text="<", width=5, command=lambda: self.click_button("<")
        )
        button_greater.grid(column=0, row=1, padx=2, pady=0.1)
        button_greater_equals = tk.Button(
            button_frame, text="<=", width=5, command=lambda: self.click_button("<=")
        )
        button_greater_equals.grid(column=1, row=1, padx=2, pady=0.1)
        button_and = tk.Button(
            button_frame, text="And", width=5, command=lambda: self.click_button("&")
        )
        button_and.grid(column=2, row=1, padx=2, pady=0.1)

        button_less = tk.Button(
            button_frame, text=">", width=5, command=lambda: self.click_button(">")
        )
        button_less.grid(column=0, row=2, padx=2, pady=0.1)
        button_less_equals = tk.Button(
            button_frame, text=">=", width=5, command=lambda: self.click_button(">=")
        )
        button_less_equals.grid(column=1, row=2, padx=2, pady=0.1)
        button_or = tk.Button(
            button_frame, text="Or", width=5, command=lambda: self.click_button("|")
        )
        button_or.grid(column=2, row=2, padx=2, pady=0.1)

        button_parentheses = tk.Button(
            button_frame, text="( )", width=5, command=lambda: self.click_button("( )")
        )
        button_parentheses.grid(column=0, row=3, padx=2, pady=0.1)
        button_in = tk.Button(
            button_frame, text="in", width=5, command=lambda: self.click_button("in []")
        )
        button_in.grid(column=2, row=3, padx=2, pady=0.1)
        button_not = tk.Button(
            button_frame, text="not", width=5, command=lambda: self.click_button("not")
        )
        button_not.grid(column=2, row=4, padx=2, pady=0.1)

        self.listbox_uniques = tk.Listbox(
            self.calculator_window, selectmode=tk.SINGLE, exportselection=0, height=20
        )
        self.listbox_uniques.place(rely=0.32, relx=0.4, relwidth=0.55, relheight=0.25)
        self.listbox_uniques.config(state="disabled")
        self.listbox_uniques.bind("<Double-Button-1>", self.add_unique_text)

        button_unique = tk.Button(
            self.calculator_window,
            text="Get Unique Values",
            command=self.get_unique_values,
        )
        button_unique.place(relwidth=0.3, relx=0.4, rely=0.58)

        self.entry_formula = tk.Entry(self.calculator_window, justify="left")
        self.entry_formula.place(rely=0.65, relheight=0.25, relx=0.05, relwidth=0.9)

        button_apply = tk.Button(
            self.calculator_window, text="Apply", command=self.select_rows
        )
        button_apply.place(rely=0.92, relx=0.75, relwidth=0.2)
