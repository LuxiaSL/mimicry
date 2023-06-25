import json
import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
from tkinter import font
from tkinter import ttk


def calculate_distribution(cargo_size, item_list):
    # Step 1: Calculate the total "time to use" of all items.
    total_time_to_use = sum([item['rate'] / item['cap'] for item in item_list])

    # Step 2: For each item, calculate its proportion of the total "time to use".
    distribution = []
    for item in item_list:
        proportion = (item['rate'] / item['cap']) / total_time_to_use

        # Step 3: Allocate cargo slots based on each item's proportion.
        slots = round(cargo_size * proportion)

        # Step 4: For each item, calculate the amount to be packed based on the number of slots allocated
        # to it and the item's stack size. Also, include the number of slots it should occupy.
        amount = slots * item['cap']
        distribution.append({
            'item': item['name'],
            'amount': amount,
            'stacks': slots,
            'slots': slots
        })
    return distribution




class SortableTable(ttk.Treeview):
    """A ttk.Treeview widget that allows the user to sort rows by clicking on the header."""

    def __init__(self, parent=None, columns=None, **kwargs):
        ttk.Treeview.__init__(self, parent, columns=columns, **kwargs)
        self.sort_direction = [1] * len(columns)

        # Set the column widths here. Adjust these values as needed.
        self.column("Name", width=175)
        self.column("Cap size", width=55)
        self.column("Rate", width=75)
        self.column("Amount", width=90)
        self.column("Stacks", width=75)

        for i, col in enumerate(columns, 1):
            self.heading(col, text=col, command=lambda _col=col, _i=i: self.sort_column(_col, _i))

    def sort_column(self, col, i):
        data = [(self.set(child, col), child) for child in self.get_children('')]
        # Try to convert to float for comparison. If it fails, it's a string, so compare as is.
        data.sort(key=lambda t: (self.try_parse_float(t[0]), t[1]), reverse=self.sort_direction[i - 1] == 1)
        for indx, item in enumerate(data):
            self.move(item[1], '', indx)
        self.sort_direction[i - 1] *= -1

    @staticmethod
    def try_parse_float(value):
        try:
            return float(value)
        except ValueError:
            return value


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master, bg='lightgray')
        self.master = master
        self.grid(padx=15, pady=15)

        # Load the stats database from the JSON file
        self.stats_data = self.load_stats_data()

        self.create_widgets()

    def create_widgets(self):
        self.item_list = []
        self.default_font = font.nametofont("TkDefaultFont")
        self.default_font.configure(size=12, weight='bold')

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
        self.items_table = SortableTable(self, columns=('Name', 'Cap size', 'Rate', 'Amount', 'Stacks'), show='headings', height=16)
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

        # Rate label and text box
        rate_frame = tk.Frame(self, bg='lightgray')
        rate_frame.grid(row=4, column=0, columnspan=1, padx=5)
        self.rate_label = tk.Label(rate_frame, text="Rate /s:", font=self.default_font, bg='lightgray')
        self.rate_label.pack(side='left')
        self.rate_entry = tk.Entry(rate_frame, font=self.default_font, width=5)
        self.rate_entry.insert(0, '0')  # Default rate
        self.rate_entry.pack(side='left')

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

        # Create a list of tuples containing the item name, stats count, and matching character percentage
        items_with_stats = [(item, self.stats_data.get(item, 0), self.calculate_matching_percentage(search_term, item))
                            for item in self.item_data]

        # Sort the items based on the stats count in descending order and the matching character percentage in descending order
        sorted_items = sorted(items_with_stats, key=lambda x: (x[1], x[2]), reverse=True)

        # Iterate through the sorted items and add them to the search results listbox
        for item, _, _ in sorted_items:
            if search_term in item.lower():
                self.search_results.insert(tk.END, item)

    def calculate_matching_percentage(self, search_term, item):
        common_length = 0
        min_length = min(len(search_term), len(item))
        for i in range(min_length):
            if search_term[i] == item[i]:
                common_length += 1
            else:
                break
        if min_length > 0:
            return common_length / min_length
        else:
            return 0.0

    def on_item_selected(self, event):
        try:
            selected_item = self.search_results.get(self.search_results.curselection())
            self.search_var.set(selected_item)
        except tk.TclError:
            pass  # Invalid listbox index, do nothing

    def add_item(self):
        name = self.search_var.get()
        if name in self.item_data:
            rate = float(self.rate_entry.get())
            self.item_list.append({'name': name, 'rate': rate, 'cap': self.item_data[name]})
            item = self.item_list[-1]
            self.items_table.insert('', 'end', values=(item['name'], item['cap'], item['rate'], '', ''))

            # Increment the stats count for the item
            self.increment_stats_count(name)

            self.calculate()  # Update the calculation
        else:
            should_add = messagebox.askyesno("Question", "Item not found in the database. Would you like to add it?")
            if should_add:
                cap_size = simpledialog.askinteger("Input", "Enter the item's cap size:", parent=self.master)
                self.item_data[name] = cap_size
                with open('items.json', 'w') as f:
                    json.dump(self.item_data, f)
                rate = float(self.rate_entry.get())
                self.item_list.append({'name': name, 'rate': rate, 'cap': cap_size})
                item = self.item_list[-1]
                self.items_table.insert('', 'end', values=(item['name'], item['cap'], item['rate'], '', ''))
                self.calculate()  # Update the calculation

    def remove_item(self):
        try:
            selected_item = self.items_table.selection()[0]
            item_name = self.items_table.item(selected_item)['values'][0]

            # Decrement the stats count for the item
            self.decrement_stats_count(item_name)

            self.items_table.delete(selected_item)
            del self.item_list[int(selected_item)]
        except IndexError:
            # No item selected, do nothing
            return

    def decrement_stats_count(self, item_name):
        if item_name in self.stats_data:
            self.stats_data[item_name] -= 1
            if self.stats_data[item_name] == 0:
                del self.stats_data[item_name]

        # Save the updated stats data to the JSON file
        self.save_stats_data()

    def increment_stats_count(self, item_name):
        if item_name in self.stats_data:
            self.stats_data[item_name] += 1
        else:
            self.stats_data[item_name] = 1

        # Save the updated stats data to the JSON file
        self.save_stats_data()

    def load_stats_data(self):
        try:
            with open('stats.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def save_stats_data(self):
        with open('stats.json', 'w') as f:
            json.dump(self.stats_data, f)

    def calculate(self):
        if not self.cargo_size_entry.get().isdigit():
            messagebox.showerror("Error", "Please enter a valid cargo size.")
            return

        cargo_size = int(self.cargo_size_entry.get())
        result = calculate_distribution(cargo_size, self.item_list)

        # Update the items table with the calculated amounts
        children = self.items_table.get_children()
        for i, item in enumerate(result):
            if i < len(children):
                item_id = children[i]
                self.items_table.set(item_id, 'Amount', item['amount'])
                self.items_table.set(item_id, 'Stacks', item['stacks'])


root = tk.Tk()
root.geometry('505x625')
app = Application(master=root)
app.mainloop()
