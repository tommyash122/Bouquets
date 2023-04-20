######################################################################################################################
# Bouquet Flowers Calculator
# Developer : Tommy Ashkenazi
# Version : 2.0 1/2/23
######################################################################################################################
import os
import random
import tkinter.messagebox
from tkinter import *
from PIL import ImageTk, Image
from Table import Table
from PDF import PDF
from fpdf.enums import XPos, YPos


def load_data(path):
    # Opening the file in read mode and encode it to utf-8 mode
    my_file = open(path, "r", encoding="UTF-8")

    # Reading the file into lines and insert them into a list
    data = my_file.read().splitlines()

    my_file.close()
    return data


def main():
    root = Tk()
    SUMS = []
    ACTIONS = []
    global cnt
    cnt = 0
    columns = load_data("Data/Flowers.txt")
    # Initiate SUMS
    for j in range(len(columns)):
        SUMS.append((columns[j], 0))

    my_tree = Table(SUMS, root, columns)

    # Create Labels
    lable_0 = Label(root, text="Bouquet's Name:", background="#F7EFE5")
    lable_1 = Label(root, text="Quantity:", background="#F7EFE5")

    # Receive input
    name_field = Entry()
    number_field = Entry()

    # Placements
    lable_0.place(relx=0.3, rely=0.7)
    name_field.place(relx=0.4, rely=0.7)

    lable_1.place(relx=0.3, rely=0.8)
    number_field.place(relx=0.4, rely=0.8)

    def add_to_table(name, number, reverse_action=False):
        try:
            global cnt
            _name = name.strip()
            _number = number

            if reverse_action:
                _number = int(_number) * -1
            else:
                _number = int(_number)
                # Add to actions array
                ACTIONS.append((_name, _number))

            bqt = load_data("Data/" + _name + ".txt")
        except:
            tkinter.messagebox.showerror("Error", "Invalid input")
            return

        counts = []
        flowers = []
        for x in bqt:
            counts.append(x.split(' ', 1)[0])
            flowers.append(x.split(' ', 1)[1])

        vals = ()
        for _ in columns:
            vals += tuple(' ')

        # Update SUMS record and insert vals item
        for i in range(len(flowers)):
            for j in range(len(columns)):
                if columns[j].encode(encoding="UTF-8") == (flowers[i].encode(encoding="UTF-8")):
                    y = list(vals)
                    y[j] = int(counts[i]) * _number  # Holds the current value that's needs to be edited

                    # That's The actual tuple inside SUMS
                    x = list(SUMS[j])
                    x[1] += y[j]
                    SUMS[j] = tuple(x)

                    # Update back the vals tuple after the change
                    vals = tuple(y)

        if not reverse_action:
            if cnt % 2 == 1:
                my_tree.tree.insert(parent='', index='end', iid=cnt, text="", values=(cnt + 1, _name, _number) + vals,
                                    tags=('oddRow',))
            else:
                my_tree.tree.insert(parent='', index='end', iid=cnt, text="", values=(cnt + 1, _name, _number) + vals,
                                    tags=('evenRow',))

            cnt += 1

        else:
            cnt -= 1

        # Delete text in boxes
        name_field.delete(0, END)
        number_field.delete(0, END)
        return

    def clear_table(SUMS):
        global cnt
        for x in my_tree.tree.get_children():
            my_tree.tree.delete(x)

        SUMS.clear()
        for j in range(len(columns)):
            SUMS.append((columns[j], 0))
        cnt = 0

        # Delete text in boxes
        name_field.delete(0, END)
        number_field.delete(0, END)
        return

    def remove_one():
        try:
            x = my_tree.item_selected()
            act = ACTIONS[int(x)]

            add_to_table(act[0], act[1], reverse_action=True)
            ACTIONS.remove(act)

            my_tree.tree.delete(x)
        except IndexError:
            tkinter.messagebox.showerror("Error", "No item has selected!")

    def print_vals(SUMS):
        table_window = Toplevel()
        Table(SUMS, table_window, ('שורה', 'שם הפרח', 'כמות'), fin_table=True)
        return

    def gen_pdf(SUMS):
        # Create a PDF object
        pdf = PDF('P', 'mm', 'A4')

        # get total page numbers
        pdf.alias_nb_pages()

        # Set auto page break
        pdf.set_auto_page_break(auto=True, margin=15)

        # Add Page
        pdf.add_page()

        pdf.add_font('DejaVu', '', 'dejavu-fonts-ttf-2.37/ttf/DejaVuSansCondensed.ttf')
        pdf.add_font('DejaVuB', '', 'dejavu-fonts-ttf-2.37/ttf/DejaVuSansCondensed-Bold.ttf')
        pdf.set_font('DejaVuB', '', 14, )

        # Table head
        head = ("שם הפרח", "כמות")
        pdf.cell(20, 0, '')
        pdf.cell(30, 10, head[1][::-1], align='R')
        pdf.cell(120, 10, head[0][::-1], align='R')
        pdf.ln(15)

        pdf.set_font('DejaVu', '', 14, )
        x, y = 10, 10
        for i in range(len(SUMS)):
            curr = SUMS[i]
            if curr[1] > 0:
                pdf.cell(20, 0, '')
                pdf.cell(30, 10, str(curr[1]), align='R')
                pdf.cell(120, 10, str(curr[0])[::-1], align='R')
                pdf.ln(15)

        pdf.output('Order_pdf.pdf')

    # Define Buttons
    add_button = Button(root, text="Add", command=
    lambda: add_to_table(name_field.get(), number_field.get()))
    add_button.place(relx=0.3, rely=0.9)

    clear_button = Button(root, text="Clear", command=
    lambda: clear_table(SUMS))
    clear_button.place(relx=0.35, rely=0.9)

    remove_one_button = Button(root, text="Remove Selected", command=remove_one)
    remove_one_button.place(relx=0.4, rely=0.9)

    print_button = Button(root, text="Print", font=15, command=
    lambda: print_vals(SUMS))
    print_button.configure(height=2, width=6)
    print_button.place(relx=0.75, rely=0.72)

    pdf_button = Button(root, text="PDF", font=15, command=
    lambda: gen_pdf(SUMS))
    pdf_button.configure(height=2, width=6)
    pdf_button.place(relx=0.85, rely=0.72)

    # Edit The Window Properties

    root.title("Gitale - Bouquet Flowers Counter")
    root.iconbitmap("logo/favicon.ico")
    root.geometry("1300x500")
    my_tree.tree.pack()

    root.configure(background="#F7EFE5")
    rand_img1 = (random.choice(os.listdir("Photos")))
    rand_img2 = (random.choice(os.listdir("Photos")))

    my_img1 = Image.open("Photos/" + rand_img1)
    my_img2 = Image.open("Photos/" + rand_img2)

    resized1 = my_img1.resize((120, 120))
    resized2 = my_img2.resize((120, 120))

    new_img1 = ImageTk.PhotoImage(resized1)
    new_img2 = ImageTk.PhotoImage(resized2)

    my_label_img1 = Label(root, image=new_img1, background="#F7EFE5")
    my_label_img2 = Label(root, image=new_img2, background="#F7EFE5")

    my_label_img1.place(relx=0.1, rely=0.7)
    my_label_img2.place(relx=0.6, rely=0.7)

    root.mainloop()


if __name__ == "__main__":
    main()
