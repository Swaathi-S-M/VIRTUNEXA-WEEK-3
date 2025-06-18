import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
from db import connect_db, add_transaction, fetch_all_transactions
from utils import get_today_date, log_action
from calculator import calculate
from datetime import datetime

class FinanceApp:
    def __init__(self, root):
        self.conn = connect_db()
        self.root = root
        self.root.title("Personal Finance Tracker")
        self.root.geometry("600x500")

        self.build_tabs()

    def build_tabs(self):
        tab_control = ttk.Notebook(self.root)

        self.tab1 = ttk.Frame(tab_control)
        self.tab2 = ttk.Frame(tab_control)
        self.tab3 = ttk.Frame(tab_control)
        self.tab4 = ttk.Frame(tab_control)

        tab_control.add(self.tab1, text="Add Income/Expense")
        tab_control.add(self.tab2, text="Summary")
        tab_control.add(self.tab3, text="Calculator")
        tab_control.add(self.tab4, text="Quit")

        tab_control.pack(expand=1, fill="both")

        self.build_add_tab()
        self.build_summary_tab()
        self.build_calculator_tab()
        self.build_quit_tab()

    def build_add_tab(self):
        frame = ttk.LabelFrame(self.tab1, text="Add Transaction")
        frame.pack(padx=20, pady=20, fill="x")

        ttk.Label(frame, text="Type:").grid(row=0, column=0, padx=5, pady=5)
        self.type_var = tk.StringVar(value="income")
        ttk.Combobox(frame, textvariable=self.type_var, values=["income", "expense"], width=20).grid(row=0, column=1)

        ttk.Label(frame, text="Category:").grid(row=1, column=0, padx=5, pady=5)
        self.cat_entry = ttk.Entry(frame)
        self.cat_entry.grid(row=1, column=1)

        ttk.Label(frame, text="Amount:").grid(row=2, column=0, padx=5, pady=5)
        self.amt_entry = ttk.Entry(frame)
        self.amt_entry.grid(row=2, column=1)

        ttk.Label(frame, text="Date (YYYY-MM-DD):").grid(row=3, column=0, padx=5, pady=5)
        self.date_entry = ttk.Entry(frame)
        self.date_entry.insert(0, get_today_date())
        self.date_entry.grid(row=3, column=1)

        ttk.Button(frame, text="Add Transaction", command=self.save_transaction).grid(row=4, columnspan=2, pady=10)

    def build_summary_tab(self):
        self.summary_frame = ttk.Frame(self.tab2)
        self.summary_frame.pack(pady=10, padx=10, fill="both")

        ttk.Button(self.summary_frame, text="Refresh Summary", command=self.show_summary).pack()

        self.text = tk.Text(self.summary_frame, height=15, width=70)
        self.text.pack(pady=10)

    def build_calculator_tab(self):
        frame = ttk.Frame(self.tab3)
        frame.pack(pady=20)

        ttk.Label(frame, text="Number 1:").grid(row=0, column=0)
        self.num1_entry = ttk.Entry(frame)
        self.num1_entry.grid(row=0, column=1)

        ttk.Label(frame, text="Operator:").grid(row=1, column=0)
        self.op_entry = ttk.Entry(frame)
        self.op_entry.grid(row=1, column=1)

        ttk.Label(frame, text="Number 2:").grid(row=2, column=0)
        self.num2_entry = ttk.Entry(frame)
        self.num2_entry.grid(row=2, column=1)

        ttk.Button(frame, text="Calculate", command=self.calc_result).grid(row=3, columnspan=2, pady=5)
        self.calc_result_var = tk.StringVar()
        ttk.Label(frame, textvariable=self.calc_result_var).grid(row=4, columnspan=2)

    def build_quit_tab(self):
        ttk.Button(self.tab4, text="Exit App", command=self.root.destroy).pack(pady=100)

    def save_transaction(self):
        try:
            trans_type = self.type_var.get()
            category = self.cat_entry.get()
            amount = float(self.amt_entry.get())
            date = self.date_entry.get()
            datetime.strptime(date, "%Y-%m-%d")

            add_transaction(self.conn, trans_type, category, amount, date)
            log_action(f"Transaction added: {trans_type} - {category} - {amount} - {date}")
            messagebox.showinfo("Success", "Transaction added successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add transaction: {str(e)}")

    def show_summary(self):
        rows = fetch_all_transactions(self.conn)
        if not rows:
            self.text.delete('1.0', tk.END)
            self.text.insert(tk.END, "No transactions found.")
            return

        df = pd.DataFrame(rows, columns=["id", "type", "category", "amount", "date"])
        df['date'] = pd.to_datetime(df['date'])
        df['month'] = df['date'].dt.to_period("M")

        summary = df.pivot_table(
            index='month',
            columns='type',
            values='amount',
            aggfunc='sum',
            fill_value=0
        )
        summary['net_balance'] = summary.get('income', 0) - summary.get('expense', 0)

        self.text.delete('1.0', tk.END)
        self.text.insert(tk.END, str(summary))
        summary.to_csv("monthly_summary.csv")

    def calc_result(self):
        result = calculate(self.num1_entry.get(), self.op_entry.get(), self.num2_entry.get())
        self.calc_result_var.set(f"Result: {result}")
