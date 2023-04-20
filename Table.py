import tkinter
from tkinter import *
from tkinter import ttk


class Table:
    def __init__(self, arr, window, cols, fin_table=False):
        self.arr = arr
        self.window = window
        self.cols = cols
        self.fin_table = fin_table

        # Define Scrolls
        tree_scroll_y = Scrollbar(self.window, orient=VERTICAL)
        tree_scroll_x = Scrollbar(self.window, orient=HORIZONTAL)

        tree_scroll_y.pack(side=RIGHT, fill=Y)
        tree_scroll_x.pack(side=BOTTOM, fill=X)

        # Define the columns text in the table
        headings = ('פרחים#', 'סוג זר', 'כמות זרים') + tuple(self.cols)
        if fin_table:
            headings = tuple(self.cols)

        self.tree = ttk.Treeview(self.window, columns=headings, show='headings',
                                 yscrollcommand=tree_scroll_y.set, xscrollcommand=tree_scroll_x.set,
                                 height=15)

        tree_scroll_y.config(command=self.tree.yview)
        tree_scroll_x.config(command=self.tree.xview)

        # Define line tags on the table for better visibility
        self.tree.tag_configure('oddRow', background="#FFFBEB")
        self.tree.tag_configure('evenRow', background="#F7EFE5")

        # Design the table
        self.style = ttk.Style()
        self.style.theme_use("default")
        self.style.configure("Treeview",
                        background="#EEEEEE",
                        foreground="black",
                        rowhight=25,
                        fieldbackground="#DDDDDD")

        # Naming and configure the columns
        for i in range(len(headings)):
            if i > 2:
                self.tree.column(i, stretch=True, anchor=CENTER, width=130)
                self.tree.heading(i, text=headings[i])
            else:
                self.tree.column(i, stretch=True, anchor=CENTER)
                self.tree.heading(i, text=headings[i])

        if not fin_table:
            self.tree.place(y=0)

        else:
            i = 1
            for x in self.arr:
                if x[1] > 0:
                    if i % 2 == 1:
                        self.tree.insert('', tkinter.END, values=(i, x[0], x[1]), tags=('oddRow',))
                    else:
                        self.tree.insert('', tkinter.END, values=(i, x[0], x[1]), tags=('evenRow',))
                    i += 1
            
            self.tree.pack(fill=BOTH)

    def item_selected(self):
        return self.tree.selection()[0]

    def get_windows_height(self):
        return self.window.winfo_height()
