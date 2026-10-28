from datetime import datetime
import json
import os
import tkinter as tk
from tkinter import messagebox, ttk


class FinStudentApp:

    def __init__(self, root):
        self.root = root
        self.root.title("FinStudent - Catatan Keuangan Mahasiswa")
        self.root.geometry("980x680")
        self.root.configure(bg="#0f172a")  # Dark Slate Background

        self.file_path = "catatan_keuangan.json"
        self.transactions = self.load_data()

        self.setup_styles()
        self.create_widgets()
        self.update_ui()

    def setup_styles(self):
        self.style = ttk.Style()
        self.style.theme_use("clam")

        # Style untuk Tabel (Treeview)
        self.style.configure(
            "Treeview",
            background="#1e293b",
            foreground="#f8fafc",
            fieldbackground="#1e293b",
            rowheight=32,
            font=("Segoe UI", 9.5),
            borderwidth=0,
        )
        self.style.configure(
            "Treeview.Heading",
            background="#334155",
            foreground="#f8fafc",
            font=("Segoe UI", 10, "bold"),
            relief="flat",
        )
        self.style.map("Treeview", background=[("selected", "#475569")])

    def load_data(self):
        if os.path.exists(self.file_path):
            try:
                with open(self.file_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                return []
        return []

    def save_data(self):
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(self.transactions, f, indent=4)

    def create_widgets(self):
        # HEADER & FINANCIAL HEALTH CARD
        header_frame = tk.Frame(
            self.root, bg="#1e293b", bd=1, relief="solid", highlightthickness=0
        )
        header_frame.pack(fill="x", padx=20, pady=(20, 10))

        title_label = tk.Label(
            header_frame,
            text="FinStudent",
            font=("Segoe UI", 20, "bold"),
            bg="#1e293b",
            fg="#c084fc",
        )
        title_label.pack(side="left", padx=15, pady=10)

        subtitle_label = tk.Label(
            header_frame,
            text="| Pencatat Keuangan Mahasiswa",
            font=("Segoe UI", 10),
            bg="#1e293b",
            fg="#94a3b8",
        )
        subtitle_label.pack(side="left", pady=10)

        # Health Frame (Fitur Pembeda)
        self.health_frame = tk.Frame(
            header_frame, bg="#0f172a", padx=12, pady=6
        )
        self.health_frame.pack(side="right", padx=15, pady=10)

        self.health_status_lbl = tk.Label(
            self.health_frame,
            text="Status: -",
            font=("Segoe UI", 9, "bold"),
            bg="#0f172a",
            fg="#38bdf8",
        )
        self.health_status_lbl.pack(anchor="w")

        self.health_msg_lbl = tk.Label(
            self.health_frame,
            text="Memuat analisis...",
            font=("Segoe UI", 8),
            bg="#0f172a",
            fg="#94a3b8",
        )
        self.health_msg_lbl.pack(anchor="w")

        # DASHBOARD RINGKASAN (SALDO, IN, OUT)
        summary_frame = tk.Frame(self.root, bg="#0f172a")
        summary_frame.pack(fill="x", padx=20, pady=5)

        # Card Saldo
        card1 = tk.Frame(summary_frame, bg="#1e293b", padx=15, pady=12)
        card1.pack(side="left", expand=True, fill="both", padx=(0, 5))
        tk.Label(
            card1,
            text="TOTAL SALDO",
            font=("Segoe UI", 8, "bold"),
            bg="#1e293b",
            fg="#94a3b8",
        ).pack(anchor="w")
        self.lbl_balance = tk.Label(
            card1,
            text="Rp 0",
            font=("Segoe UI", 14, "bold"),
            bg="#1e293b",
            fg="#ffffff",
        )
        self.lbl_balance.pack(anchor="w")

        # Card Pemasukan
        card2 = tk.Frame(summary_frame, bg="#1e293b", padx=15, pady=12)
        card2.pack(side="left", expand=True, fill="both", padx=5)
        tk.Label(
            card2,
            text="TOTAL PEMASUKAN",
            font=("Segoe UI", 8, "bold"),
            bg="#1e293b",
            fg="#94a3b8",
        ).pack(anchor="w")
        self.lbl_income = tk.Label(
            card2,
            text="Rp 0",
            font=("Segoe UI", 14, "bold"),
            bg="#1e293b",
            fg="#34d399",
        )
        self.lbl_income.pack(anchor="w")

        # Card Pengeluaran
        card3 = tk.Frame(summary_frame, bg="#1e293b", padx=15, pady=12)
        card3.pack(side="left", expand=True, fill="both", padx=(5, 0))
        tk.Label(
            card3,
            text="TOTAL PENGELUARAN",
            font=("Segoe UI", 8, "bold"),
            bg="#1e293b",
            fg="#94a3b8",
        ).pack(anchor="w")
        self.lbl_expense = tk.Label(
            card3,
            text="Rp 0",
            font=("Segoe UI", 14, "bold"),
            bg="#1e293b",
            fg="#f87171",
        )
        self.lbl_expense.pack(anchor="w")

        # MAIN AREA (FORM INPUT & TABEL)
        main_frame = tk.Frame(self.root, bg="#0f172a")
        main_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # LEFT SIDE: FORM INPUT
        form_frame = tk.Frame(main_frame, bg="#1e293b", padx=15, pady=15)
        form_frame.pack(side="left", fill="y", padx=(0, 10))

        tk.Label(
            form_frame,
            text="Tambah Transaksi",
            font=("Segoe UI", 11, "bold"),
            bg="#1e293b",
            fg="#ffffff",
        ).pack(anchor="w", pady=(0, 10))

        # Inputs
        tk.Label(
            form_frame,
            text="Jenis Transaksi:",
            font=("Segoe UI", 8),
            bg="#1e293b",
            fg="#cbd5e1",
        ).pack(anchor="w")
        self.cmb_type = ttk.Combobox(
            form_frame,
            values=["Pemasukan (+)", "Pengeluaran (-)"],
            state="readonly",
        )
        self.cmb_type.current(0)
        self.cmb_type.pack(fill="x", pady=(2, 8))

        tk.Label(
            form_frame,
            text="Kategori Mahasiswa:",
            font=("Segoe UI", 8),
            bg="#1e293b",
            fg="#cbd5e1",
        ).pack(anchor="w")
        self.cmb_category = ttk.Combobox(
            form_frame,
            values=[
                "Uang Saku / Beasiswa",
                "Gaji / Freelance",
                "Kos & Listrik",
                "Makan & Minum",
                "Kuliah, Buku & Print",
                "UKT / SPP",
                "Hiburan & Nongkrong",
                "Lain-lain",
            ],
            state="readonly",
        )
        self.cmb_category.current(0)
        self.cmb_category.pack(fill="x", pady=(2, 8))

        tk.Label(
            form_frame,
            text="Nominal (Rp):",
            font=("Segoe UI", 8),
            bg="#1e293b",
            fg="#cbd5e1",
        ).pack(anchor="w")
        self.ent_amount = tk.Entry(
            form_frame, bg="#0f172a", fg="#ffffff", insertbackground="white"
        )
        self.ent_amount.pack(fill="x", pady=(2, 8))

        tk.Label(
            form_frame,
            text="Keterangan Catatan:",
            font=("Segoe UI", 8),
            bg="#1e293b",
            fg="#cbd5e1",
        ).pack(anchor="w")
        self.ent_desc = tk.Entry(
            form_frame, bg="#0f172a", fg="#ffffff", insertbackground="white"
        )
        self.ent_desc.pack(fill="x", pady=(2, 8))

        tk.Label(
            form_frame,
            text="Tanggal (YYYY-MM-DD):",
            font=("Segoe UI", 8),
            bg="#1e293b",
            fg="#cbd5e1",
        ).pack(anchor="w")
        self.ent_date = tk.Entry(
            form_frame, bg="#0f172a", fg="#ffffff", insertbackground="white"
        )
        self.ent_date.insert(0, datetime.now().strftime("%Y-%m-%d"))
        self.ent_date.pack(fill="x", pady=(2, 12))

        btn_add = tk.Button(
            form_frame,
            text="Simpan Transaksi",
            bg="#a855f7",
            fg="white",
            font=("Segoe UI", 9, "bold"),
            relief="flat",
            command=self.add_transaction,
            cursor="hand2",
        )
        btn_add.pack(fill="x", pady=5)

        btn_del = tk.Button(
            form_frame,
            text="Hapus Data Terpilih",
            bg="#ef4444",
            fg="white",
            font=("Segoe UI", 9),
            relief="flat",
            command=self.delete_transaction,
            cursor="hand2",
        )
        btn_del.pack(fill="x", pady=5)

        # RIGHT SIDE: TABEL RIWAYAT
        table_frame = tk.Frame(main_frame, bg="#1e293b", padx=10, pady=10)
        table_frame.pack(side="right", expand=True, fill="both")

        columns = ("id", "date", "type", "category", "desc", "amount")
        self.tree = ttk.Treeview(
            table_frame, columns=columns, show="headings", selectmode="browse"
        )

        self.tree.heading("date", text="Tanggal")
        self.tree.heading("type", text="Jenis")
        self.tree.heading("category", text="Kategori")
        self.tree.heading("desc", text="Keterangan")
        self.tree.heading("amount", text="Nominal (Rp)")

        self.tree.column("id", width=0, stretch=False)
        self.tree.column("date", width=90, anchor="center")
        self.tree.column("type", width=90, anchor="center")
        self.tree.column("category", width=140)
        self.tree.column("desc", width=180)
        self.tree.column("amount", width=120, anchor="e")

        scrollbar = ttk.Scrollbar(
            table_frame, orient="vertical", command=self.tree.yview
        )
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def add_transaction(self):
        t_type = (
            "income"
            if "Pemasukan" in self.cmb_type.get()
            else "expense"
        )
        category = self.cmb_category.get()
        desc = self.ent_desc.get().strip()
        date_str = self.ent_date.get().strip()

        try:
            amount = float(self.ent_amount.get())
            if amount <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror(
                "Error Input", "Masukkan nominal angka yang valid!"
            )
            return

        if not desc:
            messagebox.showerror("Error Input", "Keterangan tidak boleh kosong!")
            return

        new_data = {
            "id": int(datetime.now().timestamp() * 1000),
            "date": date_str,
            "type": t_type,
            "category": category,
            "description": desc,
            "amount": amount,
        }

        self.transactions.append(new_data)
        self.save_data()
        self.update_ui()

        # Reset Form
        self.ent_amount.delete(0, tk.END)
        self.ent_desc.delete(0, tk.END)

    def delete_transaction(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning(
                "Peringatan", "Pilih baris data yang mau dihapus!"
            )
            return

        item_values = self.tree.item(selected_item, "values")
        item_id = int(item_values[0])

        self.transactions = [
            t for t in self.transactions if t["id"] != item_id
        ]
        self.save_data()
        self.update_ui()

    def update_ui(self):
        # Clear Treeview
        for row in self.tree.get_children():
            self.tree.delete(row)

        total_income = 0
        total_expense = 0

        # Sort berdasarkan tanggal
        sorted_list = sorted(
            self.transactions, key=lambda x: x["date"], reverse=True
        )

        for t in sorted_list:
            amt = t["amount"]
            if t["type"] == "income":
                total_income += amt
                type_label = "Pemasukan"
                formatted_amt = f"+ Rp {amt:,.0f}"
            else:
                total_expense += amt
                type_label = "Pengeluaran"
                formatted_amt = f"- Rp {amt:,.0f}"

            self.tree.insert(
                "",
                "end",
                values=(
                    t["id"],
                    t["date"],
                    type_label,
                    t["category"],
                    t["description"],
                    formatted_amt,
                ),
            )

        balance = total_income - total_expense

        # Update Text Summary
        self.lbl_balance.config(text=f"Rp {balance:,.0f}")
        self.lbl_income.config(text=f"Rp {total_income:,.0f}")
        self.lbl_expense.config(text=f"Rp {total_expense:,.0f}")

        # Update Financial Health Indicator
        self.update_health_indicator(total_income, total_expense)

    def update_health_indicator(self, income, expense):
        if income == 0 and expense == 0:
            self.health_status_lbl.config(
                text="Status: Belum Ada Data", fg="#94a3b8"
            )
            self.health_msg_lbl.config(
                text="Tambahkan catatan transaksi pertama kamu."
            )
            return

        ratio = (expense / income * 100) if income > 0 else 100

        if ratio <= 60:
            self.health_status_lbl.config(
                text="Status: Sangat Sehat", fg="#34d399"
            )
            self.health_msg_lbl.config(
                text=f"Pengeluaran baru {ratio:.0f}% dari pemasukan. Aman!"
            )
        elif ratio <= 85:
            self.health_status_lbl.config(text="Status: Waspada", fg="#fbbf24")
            self.health_msg_lbl.config(
                text=f"Pengeluaran sudah {ratio:.0f}%. Hemat sisa budget!"
            )
        else:
            self.health_status_lbl.config(
                text="Status: Bahaya / Defisit", fg="#f87171"
            )
            self.health_msg_lbl.config(
                text=f"Pengeluaran melebihi batas safe ({ratio:.0f}%). Rem pengeluaran!"
            )


if __name__ == "__main__":
    root = tk.Tk()
    app = FinStudentApp(root)
    root.mainloop()