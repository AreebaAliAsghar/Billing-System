import tkinter as tk
from tkinter import messagebox, scrolledtext
from datetime import datetime
from fpdf import FPDF

def current_date():
    return datetime.now().strftime('%d-%b-%Y')

class Name:
    def __init__(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Address:
    def __init__(self, street, city, country, postal_code):
        self.street = street
        self.city = city
        self.country = country
        self.postal_code = postal_code
    
    def __str__(self):
        return f"{self.street}, {self.city}, {self.country}, {self.postal_code}"

class BillItem:
    def __init__(self, quantity, particular, rate):
        self.quantity = quantity
        self.particular = particular
        self.rate = rate
        self.amount = self.quantity * self.rate
    
    def __str__(self):
        return f"{self.particular:<30}{self.quantity:<10}{self.rate:<10}{self.amount:<10}"

class Bill:
    bill_counter = 1

    def __init__(self, date, customer_name, customer_address, items):
        self.date = date
        self.customer_name = customer_name
        self.customer_address = customer_address
        self.items = items
        self.bill_no = Bill.bill_counter
        Bill.bill_counter += 1
        self.total = sum(item.amount for item in self.items)

    def __str__(self):
        bill_details = (
            f"MOBILO\n"
            f"Mobile City\n"
            f"Deals in all kinds of Mobiles & Accessories\n"
            f"Cellno-0321-0000000\n"
            f"CASH MEMO\n"
            f"No: {self.bill_no}\n"
            f"Date: {self.date}\n"
            f"Customer Name: {self.customer_name}\n"
            f"Customer Address: {self.customer_address}\n"
            f"{'Particular':<30}{'Qty':<10}{'Rate':<10}{'Amount':<10}\n"
        )
        for item in self.items:
            bill_details += str(item) + '\n'
        bill_details += f"Total: {self.total}\n"
        bill_details += "Signature:________\n"
        bill_details += "Address: Basement # 2, Allahwala Plaza, Markaz K8, Islamabad"
        return bill_details

    def save_to_pdf(self, filename="bill.pdf"):
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.multi_cell(0, 10, str(self))
        pdf.output(filename)

class BillingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Billing System")
        self.items = []

        # Customer Details Frame
        customer_frame = tk.LabelFrame(root, text="Customer Details")
        customer_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        tk.Label(customer_frame, text="First Name:").grid(row=0, column=0, padx=5, pady=5)
        self.first_name_entry = tk.Entry(customer_frame)
        self.first_name_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(customer_frame, text="Last Name:").grid(row=0, column=2, padx=5, pady=5)
        self.last_name_entry = tk.Entry(customer_frame)
        self.last_name_entry.grid(row=0, column=3, padx=5, pady=5)

        tk.Label(customer_frame, text="Street:").grid(row=1, column=0, padx=5, pady=5)
        self.street_entry = tk.Entry(customer_frame)
        self.street_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(customer_frame, text="City:").grid(row=1, column=2, padx=5, pady=5)
        self.city_entry = tk.Entry(customer_frame)
        self.city_entry.grid(row=1, column=3, padx=5, pady=5)

        tk.Label(customer_frame, text="Country:").grid(row=2, column=0, padx=5, pady=5)
        self.country_entry = tk.Entry(customer_frame)
        self.country_entry.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(customer_frame, text="Postal Code:").grid(row=2, column=2, padx=5, pady=5)
        self.postal_code_entry = tk.Entry(customer_frame)
        self.postal_code_entry.grid(row=2, column=3, padx=5, pady=5)

        # Item Details Frame
        item_frame = tk.LabelFrame(root, text="Item Details")
        item_frame.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        tk.Label(item_frame, text="Particular:").grid(row=0, column=0, padx=5, pady=5)
        self.particular_entry = tk.Entry(item_frame)
        self.particular_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(item_frame, text="Quantity:").grid(row=0, column=2, padx=5, pady=5)
        self.quantity_entry = tk.Entry(item_frame)
        self.quantity_entry.grid(row=0, column=3, padx=5, pady=5)

        tk.Label(item_frame, text="Rate:").grid(row=0, column=4, padx=5, pady=5)
        self.rate_entry = tk.Entry(item_frame)
        self.rate_entry.grid(row=0, column=5, padx=5, pady=5)

        tk.Button(item_frame, text="Add Item", command=self.add_item).grid(row=0, column=6, padx=5, pady=5)

        self.bill_display = scrolledtext.ScrolledText(root, height=15, width=80)
        self.bill_display.grid(row=2, column=0, padx=10, pady=10)

        tk.Button(root, text="Generate Bill", command=self.generate_bill).grid(row=3, column=0, padx=10, pady=10)

    def add_item(self):
        try:
            quantity = int(self.quantity_entry.get())
            rate = float(self.rate_entry.get())
            particular = self.particular_entry.get()
            item = BillItem(quantity, particular, rate)
            self.items.append(item)
            messagebox.showinfo("Success", "Item added successfully!")
        except ValueError:
            messagebox.showerror("Error", "Invalid input! Please enter valid values.")

    def generate_bill(self):
        customer_name = Name(self.first_name_entry.get(), self.last_name_entry.get())
        customer_address = Address(self.street_entry.get(), self.city_entry.get(), self.country_entry.get(), self.postal_code_entry.get())
        bill = Bill(current_date(), customer_name, customer_address, self.items)
        self.bill_display.insert(tk.END, str(bill))
        bill.save_to_pdf()

if __name__ == "__main__":
    root = tk.Tk()
    app = BillingApp(root)
    root.mainloop()
