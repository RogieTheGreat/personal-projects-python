import os
import sys
import subprocess


def ensure_packages():
    required = {
        "PIL": "pillow",
        "pypdf": "pypdf",
        "reportlab": "reportlab",
        "tkinterdnd2": "tkinterdnd2",
    }
    missing = []
    for module_name, package_name in required.items():
        try:
            __import__(module_name)
        except ImportError:
            missing.append(package_name)

    if missing:
        command = [sys.executable, "-m", "pip", "install", *missing]
        try:
            subprocess.check_call(command)
        except Exception as error:
            print("Could not install required packages:", ", ".join(missing))
            print(error)
            input("Press Enter to close...")
            raise SystemExit(1)

        os.execv(sys.executable, [sys.executable, *sys.argv])


ensure_packages()

import tkinter as tk
from io import BytesIO
from tkinter import filedialog, messagebox, ttk

from PIL import Image
from pypdf import PdfReader, PdfWriter
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from tkinterdnd2 import DND_FILES, TkinterDnD


def register_arial_font():
    paths = [
        r"C:\Windows\Fonts\arial.ttf",
        r"C:\Windows\Fonts\Arial.ttf",
    ]
    for path in paths:
        if os.path.exists(path):
            try:
                pdfmetrics.registerFont(TTFont("Arial", path))
                return "Arial"
            except Exception:
                pass
    return "Helvetica"


PDF_FONT = register_arial_font()


class PDFStamperApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF Stamper")
        self.centre_window(940, 900)
        self.root.minsize(800, 680)

        self.pdf_files = []
        self.pdf_descriptions = {}
        self.signature_file = ""
        self.output_folder = ""

        self.build_ui()

    def centre_window(self, width, height):
        self.root.update_idletasks()
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = max(0, (screen_width - width) // 2)
        y = max(0, (screen_height - height) // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def build_ui(self):
        bottom = ttk.Frame(self.root, padding=(18, 8))
        bottom.pack(side="bottom", fill="x")

        self.progress = ttk.Progressbar(bottom, maximum=100)
        self.progress.pack(fill="x", pady=(0, 5))

        self.status_label = ttk.Label(bottom, text="Ready", anchor="center")
        self.status_label.pack(fill="x", pady=(0, 5))

        self.stamp_button = ttk.Button(
            bottom,
            text="STAMP ALL PDF FILES",
            command=self.stamp_all_pdfs,
        )
        self.stamp_button.pack(fill="x", ipady=7)

        main = ttk.Frame(self.root, padding=16)
        main.pack(fill="both", expand=True)

        ttk.Label(
            main,
            text="PDF STAMPER",
            font=("Arial", 19, "bold"),
        ).pack(pady=(0, 2))

        ttk.Label(
            main,
            text="Add PDFs, then assign a different description to each file",
        ).pack(pady=(0, 10))

        pdf_frame = ttk.LabelFrame(
            main,
            text="1. PDF Files and Individual Descriptions",
            padding=9,
        )
        pdf_frame.pack(fill="both", expand=True, pady=4)

        self.drop_frame = tk.Frame(
            pdf_frame,
            bg="#f4f4f4",
            highlightbackground="#888888",
            highlightthickness=1,
        )
        self.drop_frame.pack(fill="both", expand=True)

        self.drop_label = tk.Label(
            self.drop_frame,
            text="Drag and drop PDFs here, or click Add PDF Files",
            bg="#f4f4f4",
            fg="#555555",
            font=("Arial", 10),
            pady=6,
        )
        self.drop_label.pack(fill="x")

        table_frame = ttk.Frame(self.drop_frame)
        table_frame.pack(fill="both", expand=True, padx=5, pady=(0, 5))
        table_frame.rowconfigure(0, weight=1)
        table_frame.columnconfigure(0, weight=1)

        self.pdf_tree = ttk.Treeview(
            table_frame,
            columns=("file", "description", "status"),
            show="headings",
            height=6,
            selectmode="browse",
        )
        self.pdf_tree.heading("file", text="PDF File")
        self.pdf_tree.heading("description", text="Description")
        self.pdf_tree.heading("status", text="Status")
        self.pdf_tree.column("file", width=210, minwidth=140)
        self.pdf_tree.column("description", width=480, minwidth=240)
        self.pdf_tree.column("status", width=80, minwidth=70, anchor="center")
        self.pdf_tree.grid(row=0, column=0, sticky="nsew")

        y_scroll = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.pdf_tree.yview,
        )
        y_scroll.grid(row=0, column=1, sticky="ns")
        self.pdf_tree.configure(yscrollcommand=y_scroll.set)

        self.pdf_tree.bind("<<TreeviewSelect>>", self.on_pdf_selected)
        self.pdf_tree.bind("<Double-1>", self.on_pdf_double_click)

        for widget in (self.drop_frame, self.drop_label, self.pdf_tree):
            widget.drop_target_register(DND_FILES)
            widget.dnd_bind("<<Drop>>", self.handle_pdf_drop)
            widget.dnd_bind("<<DropEnter>>", self.handle_drop_enter)
            widget.dnd_bind("<<DropLeave>>", self.handle_drop_leave)

        button_row = ttk.Frame(pdf_frame)
        button_row.pack(fill="x", pady=(7, 0))
        ttk.Button(
            button_row,
            text="Add PDF Files",
            command=self.add_pdf_files,
        ).pack(side="left", padx=(0, 6))
        ttk.Button(
            button_row,
            text="Remove Selected",
            command=self.remove_selected_pdf,
        ).pack(side="left", padx=6)
        ttk.Button(
            button_row,
            text="Clear List",
            command=self.clear_pdf_list,
        ).pack(side="left", padx=6)
        self.pdf_count_label = ttk.Label(button_row, text="0 PDF files")
        self.pdf_count_label.pack(side="right")

        description_frame = ttk.LabelFrame(
            main,
            text="2. Description for Selected PDF",
            padding=9,
        )
        description_frame.pack(fill="x", pady=5)
        description_frame.columnconfigure(1, weight=1)

        ttk.Label(description_frame, text="Selected PDF:").grid(
            row=0, column=0, sticky="w", padx=4, pady=3
        )
        self.selected_pdf_label = ttk.Label(
            description_frame,
            text="No PDF selected",
        )
        self.selected_pdf_label.grid(
            row=0, column=1, columnspan=2, sticky="w", padx=4, pady=3
        )

        ttk.Label(description_frame, text="Description:").grid(
            row=1, column=0, sticky="w", padx=4, pady=3
        )
        self.description_entry = ttk.Entry(description_frame)
        self.description_entry.grid(
            row=1, column=1, sticky="ew", padx=4, pady=3
        )
        self.description_entry.bind(
            "<Return>", lambda event: self.apply_description()
        )
        ttk.Button(
            description_frame,
            text="Apply and Next",
            command=self.apply_description,
        ).grid(row=1, column=2, padx=4, pady=3)

        common_frame = ttk.LabelFrame(
            main,
            text="3. Common Header Information",
            padding=9,
        )
        common_frame.pack(fill="x", pady=5)
        common_frame.columnconfigure(1, weight=1)

        fields = [
            ("Cost Centre ID:", "cost_centre_entry", "10926200"),
            ("Type:", "type_entry", ""),
            ("Cost Type:", "cost_type_entry", ""),
        ]
        for row, (label, attribute, default) in enumerate(fields):
            ttk.Label(common_frame, text=label).grid(
                row=row, column=0, sticky="w", padx=4, pady=3
            )
            entry = ttk.Entry(common_frame)
            entry.grid(row=row, column=1, sticky="ew", padx=4, pady=3)
            if default:
                entry.insert(0, default)
            setattr(self, attribute, entry)

        signature_frame = ttk.LabelFrame(main, text="4. Signature", padding=9)
        signature_frame.pack(fill="x", pady=5)
        signature_frame.columnconfigure(1, weight=1)

        ttk.Label(signature_frame, text="Name:").grid(
            row=0, column=0, sticky="w", padx=4, pady=3
        )
        self.name_entry = ttk.Entry(signature_frame)
        self.name_entry.insert(0, "FIRST LAST")
        self.name_entry.grid(
            row=0, column=1, columnspan=2, sticky="ew", padx=4, pady=3
        )

        ttk.Label(signature_frame, text="Signature image:").grid(
            row=1, column=0, sticky="w", padx=4, pady=3
        )
        self.signature_label = ttk.Label(
            signature_frame,
            text="No signature image selected",
        )
        self.signature_label.grid(
            row=1, column=1, sticky="w", padx=4, pady=3
        )
        ttk.Button(
            signature_frame,
            text="Browse Image",
            command=self.select_signature,
        ).grid(row=1, column=2, padx=4, pady=3)

        output_frame = ttk.LabelFrame(main, text="5. Output Folder", padding=9)
        output_frame.pack(fill="x", pady=5)
        self.output_folder_label = ttk.Label(
            output_frame,
            text="No output folder selected",
            wraplength=700,
        )
        self.output_folder_label.pack(
            side="left", fill="x", expand=True, padx=(0, 8)
        )
        ttk.Button(
            output_frame,
            text="Choose Folder",
            command=self.select_output_folder,
        ).pack(side="right")

    def add_pdf_files(self):
        files = filedialog.askopenfilenames(
            title="Select PDF Files",
            filetypes=[("PDF Files", "*.pdf")],
        )
        self.add_paths(files)

    def add_paths(self, paths):
        added = 0
        ignored = []

        for item in paths:
            path = os.path.normpath(str(item).strip("{}"))
            candidates = []

            if os.path.isdir(path):
                try:
                    candidates = [
                        os.path.join(path, name)
                        for name in os.listdir(path)
                        if name.lower().endswith(".pdf")
                    ]
                except OSError as error:
                    ignored.append(f"{os.path.basename(path)}: {error}")
                    continue
            elif os.path.isfile(path) and path.lower().endswith(".pdf"):
                candidates = [path]
            else:
                ignored.append(os.path.basename(path) or path)

            for candidate in candidates:
                candidate = os.path.normpath(candidate)
                if candidate not in self.pdf_files:
                    self.pdf_files.append(candidate)
                    self.pdf_descriptions[candidate] = ""
                    added += 1

        self.refresh_pdf_table()

        if added:
            self.status_label.config(text=f"Added {added} PDF file(s)")
            self.select_first_missing_description()

        if ignored:
            messagebox.showwarning(
                "Some Files Were Ignored",
                "Only PDF files can be added.\n\nIgnored:\n"
                + "\n".join(ignored),
            )

    def handle_pdf_drop(self, event):
        try:
            items = self.root.tk.splitlist(event.data)
        except tk.TclError:
            items = [event.data]
        self.set_drop_highlight(False)
        self.add_paths(items)
        return getattr(event, "action", None)

    def handle_drop_enter(self, event):
        self.set_drop_highlight(True)
        return getattr(event, "action", None)

    def handle_drop_leave(self, event):
        self.set_drop_highlight(False)
        return getattr(event, "action", None)

    def set_drop_highlight(self, active):
        if active:
            self.drop_frame.config(
                bg="#dceeff",
                highlightbackground="#1976d2",
                highlightthickness=2,
            )
            self.drop_label.config(
                bg="#dceeff",
                text="Release to add PDF files",
            )
        else:
            self.drop_frame.config(
                bg="#f4f4f4",
                highlightbackground="#888888",
                highlightthickness=1,
            )
            self.drop_label.config(
                bg="#f4f4f4",
                text="Drag and drop PDFs here, or click Add PDF Files",
            )

    def refresh_pdf_table(self):
        for item in self.pdf_tree.get_children():
            self.pdf_tree.delete(item)

        complete = 0
        for index, path in enumerate(self.pdf_files):
            description = self.pdf_descriptions.get(path, "").strip()
            status = "READY" if description else "MISSING"
            if description:
                complete += 1
            self.pdf_tree.insert(
                "",
                "end",
                iid=str(index),
                values=(os.path.basename(path), description, status),
            )

        missing = len(self.pdf_files) - complete
        self.pdf_count_label.config(
            text=f"{len(self.pdf_files)} PDF(s), {missing} missing"
        )

        if not self.pdf_files:
            self.status_label.config(text="Drag PDF files into the box")
        elif missing:
            self.status_label.config(
                text=f"{missing} PDF(s) still need descriptions"
            )
        else:
            self.status_label.config(text="All PDF descriptions are ready")

    def selected_index(self):
        selection = self.pdf_tree.selection()
        if not selection:
            return None
        try:
            index = int(selection[0])
        except ValueError:
            return None
        if 0 <= index < len(self.pdf_files):
            return index
        return None

    def selected_path(self):
        index = self.selected_index()
        if index is None:
            return None
        return self.pdf_files[index]

    def on_pdf_selected(self, event=None):
        path = self.selected_path()
        self.description_entry.delete(0, tk.END)

        if path is None:
            self.selected_pdf_label.config(text="No PDF selected")
            return

        self.selected_pdf_label.config(text=os.path.basename(path))
        self.description_entry.insert(
            0,
            self.pdf_descriptions.get(path, ""),
        )

    def on_pdf_double_click(self, event=None):
        self.on_pdf_selected()
        self.description_entry.focus_set()
        self.description_entry.select_range(0, tk.END)

    def apply_description(self):
        path = self.selected_path()
        if path is None:
            messagebox.showerror(
                "No PDF Selected",
                "Select a PDF from the table first.",
            )
            return

        description = self.description_entry.get().strip()
        if not description:
            messagebox.showerror(
                "Missing Description",
                "Type a description for the selected PDF.",
            )
            return

        current = self.selected_index()
        self.pdf_descriptions[path] = description
        self.refresh_pdf_table()

        next_index = self.find_missing_index((current or 0) + 1)
        if next_index is None:
            self.selected_pdf_label.config(
                text=f"{os.path.basename(path)} - description saved"
            )
            self.description_entry.delete(0, tk.END)
            return

        item = str(next_index)
        self.pdf_tree.selection_set(item)
        self.pdf_tree.focus(item)
        self.pdf_tree.see(item)
        self.on_pdf_selected()
        self.description_entry.focus_set()

    def find_missing_index(self, start=0):
        total = len(self.pdf_files)
        for index in list(range(start, total)) + list(range(0, min(start, total))):
            path = self.pdf_files[index]
            if not self.pdf_descriptions.get(path, "").strip():
                return index
        return None

    def select_first_missing_description(self):
        index = self.find_missing_index(0)
        if index is None:
            return
        item = str(index)
        self.pdf_tree.selection_set(item)
        self.pdf_tree.focus(item)
        self.pdf_tree.see(item)
        self.on_pdf_selected()
        self.description_entry.focus_set()

    def remove_selected_pdf(self):
        index = self.selected_index()
        if index is None:
            messagebox.showerror(
                "No PDF Selected",
                "Select a PDF to remove.",
            )
            return

        path = self.pdf_files.pop(index)
        self.pdf_descriptions.pop(path, None)
        self.selected_pdf_label.config(text="No PDF selected")
        self.description_entry.delete(0, tk.END)
        self.refresh_pdf_table()
        self.select_first_missing_description()

    def clear_pdf_list(self):
        self.pdf_files.clear()
        self.pdf_descriptions.clear()
        self.selected_pdf_label.config(text="No PDF selected")
        self.description_entry.delete(0, tk.END)
        self.refresh_pdf_table()

    def select_signature(self):
        path = filedialog.askopenfilename(
            title="Select Signature Image",
            filetypes=[
                ("Image Files", "*.png *.jpg *.jpeg *.bmp *.webp"),
                ("All Files", "*.*"),
            ],
        )
        if path:
            self.signature_file = os.path.normpath(path)
            self.signature_label.config(text=os.path.basename(path))

    def select_output_folder(self):
        path = filedialog.askdirectory(title="Select Output Folder")
        if path:
            self.output_folder = os.path.normpath(path)
            self.output_folder_label.config(text=self.output_folder)

    def wrap_text(self, text, font_name, font_size, maximum_width):
        words = text.split()
        lines = []
        current = ""

        for word in words:
            candidate = f"{current} {word}".strip()
            width = pdfmetrics.stringWidth(candidate, font_name, font_size)
            if width <= maximum_width:
                current = candidate
            else:
                if current:
                    lines.append(current)
                current = word

        if current:
            lines.append(current)
        return lines

    def create_stamp(
        self,
        page_width,
        page_height,
        cost_centre,
        expense_type,
        description,
        cost_type,
        employee_name,
    ):
        packet = BytesIO()
        stamp = canvas.Canvas(packet, pagesize=(page_width, page_height))

        font_size = 11
        line_spacing = 13
        header_x = page_width * 0.32
        header_top = page_height - 28
        maximum_width = page_width - header_x - 30

        lines = []
        for value in (cost_centre, expense_type, description, cost_type):
            if value.strip():
                lines.extend(
                    self.wrap_text(
                        value.upper(),
                        PDF_FONT,
                        font_size,
                        maximum_width,
                    )
                )

        if not lines:
            lines = [""]

        box_height = max(55, len(lines) * line_spacing + 14)

        stamp.saveState()
        try:
            stamp.setFillAlpha(0.50)
        except AttributeError:
            pass
        stamp.setFillColorRGB(1, 1, 1)
        stamp.rect(
            header_x - 7,
            header_top - box_height + 9,
            maximum_width + 14,
            box_height,
            fill=1,
            stroke=0,
        )
        stamp.restoreState()

        stamp.setFillColorRGB(0, 0, 0)
        stamp.setFont(PDF_FONT, font_size)
        y = header_top
        for line in lines:
            stamp.drawString(header_x, y, line)
            y -= line_spacing

        signature_width = min(220, page_width * 0.38)
        signature_height = 55
        signature_x = (page_width - signature_width) / 2
        signature_y = 35

        with Image.open(self.signature_file) as opened_image:
            signature_image = opened_image.copy()

        signature_image.thumbnail(
            (int(signature_width * 3), int(signature_height * 3))
        )
        if signature_image.mode not in ("RGBA", "RGB"):
            signature_image = signature_image.convert("RGBA")

        image_buffer = BytesIO()
        signature_image.save(image_buffer, format="PNG")
        image_buffer.seek(0)

        stamp.drawImage(
            ImageReader(image_buffer),
            signature_x,
            signature_y,
            width=signature_width,
            height=signature_height,
            preserveAspectRatio=True,
            anchor="c",
            mask="auto",
        )

        stamp.setFont(PDF_FONT, 8)
        stamp.drawCentredString(
            page_width / 2,
            signature_y - 2,
            employee_name.upper(),
        )

        stamp.save()
        packet.seek(0)
        return PdfReader(packet).pages[0]

    def create_output_path(self, input_pdf):
        base = os.path.splitext(os.path.basename(input_pdf))[0]
        output = os.path.join(self.output_folder, f"{base}_stamped.pdf")
        counter = 2
        while os.path.exists(output):
            output = os.path.join(
                self.output_folder,
                f"{base}_stamped_{counter}.pdf",
            )
            counter += 1
        return output

    def stamp_single_pdf(self, input_pdf, output_pdf):
        description = self.pdf_descriptions.get(input_pdf, "").strip()
        if not description:
            raise ValueError("No description assigned to this PDF.")

        reader = PdfReader(input_pdf)
        if reader.is_encrypted and reader.decrypt("") == 0:
            raise ValueError("The PDF is password protected.")

        writer = PdfWriter()

        common_values = {
            "cost_centre": self.cost_centre_entry.get().strip(),
            "expense_type": self.type_entry.get().strip(),
            "cost_type": self.cost_type_entry.get().strip(),
            "employee_name": self.name_entry.get().strip(),
        }

        for page in reader.pages:
            overlay = self.create_stamp(
                page_width=float(page.mediabox.width),
                page_height=float(page.mediabox.height),
                description=description,
                **common_values,
            )
            page.merge_page(overlay)
            writer.add_page(page)

        with open(output_pdf, "wb") as output_file:
            writer.write(output_file)

    def validate_inputs(self):
        if not self.pdf_files:
            messagebox.showerror("No PDF Files", "Add at least one PDF file.")
            return False

        missing = [
            os.path.basename(path)
            for path in self.pdf_files
            if not self.pdf_descriptions.get(path, "").strip()
        ]
        if missing:
            messagebox.showerror(
                "Missing Descriptions",
                "Each PDF needs a description.\n\nMissing:\n"
                + "\n".join(missing),
            )
            self.select_first_missing_description()
            return False

        if not self.signature_file:
            messagebox.showerror(
                "Missing Signature",
                "Select a signature image.",
            )
            return False

        if not self.name_entry.get().strip():
            messagebox.showerror("Missing Name", "Enter the signature name.")
            return False

        if not self.output_folder:
            messagebox.showerror(
                "Missing Output Folder",
                "Choose an output folder.",
            )
            return False

        return True

    def stamp_all_pdfs(self):
        if not self.validate_inputs():
            return

        os.makedirs(self.output_folder, exist_ok=True)
        successful = []
        failed = []
        total = len(self.pdf_files)

        self.stamp_button.config(state="disabled")
        self.progress["value"] = 0

        try:
            for number, input_pdf in enumerate(self.pdf_files, start=1):
                filename = os.path.basename(input_pdf)
                self.status_label.config(
                    text=f"Processing {number} of {total}: {filename}"
                )
                self.root.update_idletasks()

                try:
                    output_pdf = self.create_output_path(input_pdf)
                    self.stamp_single_pdf(input_pdf, output_pdf)
                    successful.append(output_pdf)
                except Exception as error:
                    failed.append((filename, str(error)))

                self.progress["value"] = (number / total) * 100
                self.root.update_idletasks()
        finally:
            self.stamp_button.config(state="normal")

        if not failed:
            self.status_label.config(
                text=f"Completed: {len(successful)} PDF file(s)"
            )
            messagebox.showinfo(
                "Batch Completed",
                f"{len(successful)} PDF file(s) stamped.\n\n"
                f"Saved in:\n{self.output_folder}",
            )
            self.open_output_folder()
        else:
            summary = "\n".join(
                f"{filename}: {error}" for filename, error in failed
            )
            self.status_label.config(
                text=f"Completed with {len(failed)} error(s)"
            )
            messagebox.showwarning(
                "Completed with Errors",
                f"Successful: {len(successful)}\n"
                f"Failed: {len(failed)}\n\n{summary}",
            )

    def open_output_folder(self):
        try:
            if sys.platform.startswith("win"):
                os.startfile(self.output_folder)
            elif sys.platform == "darwin":
                subprocess.Popen(["open", self.output_folder])
            else:
                subprocess.Popen(["xdg-open", self.output_folder])
        except OSError:
            pass


if __name__ == "__main__":
    try:
        root = TkinterDnD.Tk()
        style = ttk.Style(root)
        try:
            style.theme_use("vista")
        except tk.TclError:
            pass
        app = PDFStamperApp(root)
        root.mainloop()
    except Exception as error:
        try:
            messagebox.showerror("Error", str(error))
        except Exception:
            print(error)
            input("Press Enter to close...")
