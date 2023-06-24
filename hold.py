import json
import threading
import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
from tkinter import font
from tkinter import ttk


def calculate_distribution(cargo_size, item_list):
    total_usage = sum([item['rate'] for item in item_list])
    distribution = []

    for item in item_list:
        proportion = item['rate'] / total_usage
        slots = cargo_size * proportion
        amount = slots * item['cap']
        stacks = slots
        distribution.append({
            'item': item['name'],
            'amount': amount,
            'stacks': stacks
        })

    return distribution


class SortableTable(ttk.Treeview):
    """A ttk.Treeview widget that allows the user to sort rows by clicking on the header."""

    def __init__(self, parent=None, columns=None, **kwargs):
        ttk.Treeview.__init__(self, parent, columns=columns, **kwargs)
        self.sort_direction = [1] * len(columns)
        for i, col in enumerate(columns, 1):
            self.heading(col, text=col, command=lambda _col=col, _i=i: self.sort_column(_col, _i))

    def sort_column(self, col, i):
        data = [(self.set(child, col), child) for child in self.get_children('')]
        data.sort(reverse=self.sort_direction[i - 1] == 1)

        for indx, item in enumerate(data):
            self.move(item[1], '', indx)

        self.sort_direction[i - 1] *= -1


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master, bg='lightgray')
        self.master = master
        self.grid(padx=15, pady=15)
        self.create_widgets()

    def create_widgets(self):
        self.item_list = []
        self.default_font = font.nametofont("TkDefaultFont")
        self.default_font.configure(size=14, weight='bold')

        # Load item names from JSON file
        with open('items.json', 'r') as f:
            self.item_data = json.load(f)

        # Remove item button
        self.remove_item_button = tk.Button(self, text="-", font=self.default_font, command=self.remove_item,
                                            bg='salmon', width=3, height=1)
        self.remove_item_button.grid(row=0, column=0, padx=5, pady=10, sticky='w')

        # Cargo size label and text box
        cargo_size_frame = tk.Frame(self, bg='lightgray')
        cargo_size_frame.grid(row=0, column=1, columnspan=1, padx=5)
        self.cargo_size_label = tk.Label(cargo_size_frame, text="Cargo Size:", font=self.default_font, bg='lightgray')
        self.cargo_size_label.pack(side='left')
        self.cargo_size_entry = tk.Entry(cargo_size_frame, font=self.default_font, width=4)
        self.cargo_size_entry.insert(0, '450')  # Default cargo size
        self.cargo_size_entry.pack(side='left')

        # Calculate button
        self.calculate_button = tk.Button(self, text="\u2699", font=self.default_font, command=self.calculate,
                                          bg='lightblue', width=3, height=1)
        self.calculate_button.grid(row=0, column=4, padx=5, pady=10)

        # Items table
        self.items_table = SortableTable(self, columns=('Name', 'Cap size', 'Rate', 'Amount'), show='headings')
        self.items_table.grid(row=1, column=0, columnspan=5, sticky='nsew')

        # Search box
        self.search_var = tk.StringVar()
        self.search_var.trace("w", lambda name, index, mode, sv=self.search_var: self.update_listbox(sv))
        self.search_box = tk.Entry(self, textvariable=self.search_var, font=self.default_font)
        self.search_box.grid(row=2, column=0, columnspan=2, sticky='w', padx=5, pady=5)

        # Listbox for search results
        self.search_results = tk.Listbox(self, height=5, font=self.default_font)
        self.search_results.grid(row=3, column=0, columnspan=5, sticky='nsew', padx=5)
        self.search_results.bind('<<ListboxSelect>>', self.on_item_selected)

        # Rate input
        self.rate_var = tk.StringVar(value='0')
        self.rate_input = tk.Entry(self, textvariable=self.rate_var, font=self.default_font, width=4)
        self.rate_input.grid(row=4, column=0, padx=5)

        # Add item button
        self.add_item_button = tk.Button(self, text="Add", font=self.default_font, command=self.add_item,
                                         bg='lightgreen', width=3, height=1)
        self.add_item_button.grid(row=4, column=1, pady=5)

        # Make the search row and table resizable
        self.rowconfigure(3, weight=1)
        self.columnconfigure(0, weight=1)

    def update_listbox(self, search_var):
        search_term = search_var.get().lower()
        self.search_results.delete(0, tk.END)
        matches = []
        for item in self.item_data:
            if search_term in item.lower():
                matches.append(item)
        for item in matches[:5]:  # Show only the top 5 matches
            self.search_results.insert(tk.END, item)

    def on_item_selected(self, event):
        selected_item = self.search_results.get(self.search_results.curselection())
        self.search_var.set(selected_item)

    def add_item(self):
        name = self.search_var.get()
        if name in self.item_data:
            rate = int(self.rate_var.get())
            self.item_list.append({'name': name, 'rate': rate, 'cap': self.item_data[name]})
            item = self.item_list[-1]
            self.items_table.insert('', 'end', values=(item['name'], item['cap'], item['rate'], ''))
            self.calculate()  # Update the calculation
        else:
            should_add = messagebox.askyesno("Question", "Item not found in the database. Would you like to add it?")
            if should_add:
                cap_size = simpledialog.askinteger("Input", "Enter the item's cap size:", parent=self.master)
                self.item_data[name] = cap_size
                with open('items.json', 'w') as f:
                    json.dump(self.item_data, f)
                rate = int(self.rate_var.get())
                self.item_list.append({'name': name, 'rate': rate, 'cap': cap_size})
                item = self.item_list[-1]
                self.items_table.insert('', 'end', values=(item['name'], item['cap'], item['rate'], ''))
                self.calculate()  # Update the calculation

    def remove_item(self):
        selected_item = self.items_table.selection()[0]
        self.items_table.delete(selected_item)
        del self.item_list[int(selected_item)]

    def calculate(self):
        if not self.cargo_size_entry.get().isdigit():
            messagebox.showerror("Error", "Please enter a valid cargo size.")
            return

        cargo_size = int(self.cargo_size_entry.get())
        result = calculate_distribution(cargo_size, self.item_list)

        # Clear the items table
        self.items_table.delete(*self.items_table.get_children())

        # Update the items table with the calculated amounts
        for item in result:
            self.items_table.insert('', 'end', values=(item['item'], item['cap'], item['stacks'], item['amount']))

        self.calculate_button["state"] = "normal"

    def calculate_thread(self, cargo_size):
        result = calculate_distribution(cargo_size, self.item_list)

        # Update the items table with the calculated amounts
        for i, item in enumerate(result):
            try:
                self.items_table.set(i, 'Amount', item['amount'])
            except tk.TclError:
                # Item was removed, skip it
                continue

        self.calculate_button["state"] = "normal"

root = tk.Tk()
root.geometry('830x550')
app = Application(master=root)
app.mainloop()
