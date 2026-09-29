import os
import sys
import subprocess
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


# ---------------------------------------------------------
# FONT SETUP
# ---------------------------------------------------------

def register_arial_font():
    """
    Register Arial when available.
    Fall back to Helvetica when Arial cannot be found.
    """

    possible_paths = [
        r"C:\Windows\Fonts\arial.ttf",
        r"C:\Windows\Fonts\Arial.ttf",
        "/usr/share/fonts/truetype/msttcorefonts/Arial.ttf",
    ]

    for font_path in possible_paths:
        if os.path.exists(font_path):
            try:
                pdfmetrics.registerFont(
                    TTFont("Arial", font_path)
                )
                return "Arial"

            except Exception:
                pass

    return "Helvetica"


PDF_FONT = register_arial_font()


# ---------------------------------------------------------
# APPLICATION
# ---------------------------------------------------------

class PDFStamperApp:

    def __init__(self, root):
        self.root = root

        self.root.title(
            "TINKR Batch PDF Stamper"
        )

        # Centre the app on the screen.
        window_width = 900
        window_height = 850

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        centre_x = max(
            0,
            int(
                (screen_width - window_width) / 2
            )
        )

        centre_y = max(
            0,
            int(
                (screen_height - window_height) / 2
            )
        )

        self.root.geometry(
            f"{window_width}x{window_height}"
            f"+{centre_x}+{centre_y}"
        )

        self.root.minsize(
            780,
            650
        )

        # List of complete PDF file paths.
        self.pdf_files = []

        # Dictionary containing one description per PDF.
        #
        # Example:
        # {
        #     "C:\\Receipts\\1.pdf": "Home to Airport",
        #     "C:\\Receipts\\2.pdf": "Airport to Hotel"
        # }
        self.pdf_descriptions = {}

        self.signature_file = ""
        self.output_folder = ""

        self.create_interface()

    # -----------------------------------------------------
    # CREATE INTERFACE
    # -----------------------------------------------------

    def create_interface(self):

        # -------------------------------------------------
        # FIXED BOTTOM ACTION AREA
        # -------------------------------------------------

        action_frame = ttk.Frame(
            self.root,
            padding=(20, 10)
        )

        action_frame.pack(
            side="bottom",
            fill="x"
        )

        self.progress = ttk.Progressbar(
            action_frame,
            mode="determinate",
            maximum=100
        )

        self.progress.pack(
            fill="x",
            pady=(0, 5)
        )

        self.status_label = ttk.Label(
            action_frame,
            text="Ready",
            anchor="centre"
        )

        self.status_label.pack(
            fill="x",
            pady=(0, 7)
        )

        self.stamp_button = ttk.Button(
            action_frame,
            text="STAMP ALL PDF FILES",
            command=self.stamp_all_pdfs
        )

        self.stamp_button.pack(
            fill="x",
            ipady=8
        )

        # -------------------------------------------------
        # MAIN CONTENT
        # -------------------------------------------------

        main_frame = ttk.Frame(
            self.root,
            padding=(20, 15)
        )

        main_frame.pack(
            side="top",
            fill="both",
            expand=True
        )

        ttk.Label(
            main_frame,
            text="TINKR PDF STAMPER",
            font=("Arial", 20, "bold")
        ).pack(
            pady=(0, 5)
        )

        ttk.Label(
            main_frame,
            text=(
                "Add multiple PDFs and assign a different "
                "description to each file"
            ),
            font=("Arial", 10)
        ).pack(
            pady=(0, 12)
        )

        # -------------------------------------------------
        # PDF FILE SECTION
        # -------------------------------------------------

        pdf_frame = ttk.LabelFrame(
            main_frame,
            text="1. PDF Files and Individual Descriptions",
            padding=10
        )

        pdf_frame.pack(
            fill="both",
            expand=True,
            pady=5
        )

        self.drop_frame = tk.Frame(
            pdf_frame,
            background="#f4f4f4",
            highlightbackground="#8a8a8a",
            highlightthickness=1
        )

        self.drop_frame.pack(
            fill="both",
            expand=True
        )

        self.drop_instruction_label = tk.Label(
            self.drop_frame,
            text=(
                "Drag and drop PDF files here\n"
                "or click Add PDF Files"
            ),
            font=("Arial", 10),
            foreground="#555555",
            background="#f4f4f4",
            pady=6
        )

        self.drop_instruction_label.pack(
            fill="x"
        )

        # -------------------------------------------------
        # PDF TABLE
        # -------------------------------------------------

        table_frame = ttk.Frame(
            self.drop_frame
        )

        table_frame.pack(
            fill="both",
            expand=True,
            padx=5,
            pady=(0, 5)
        )

        self.pdf_tree = ttk.Treeview(
            table_frame,
            columns=(
                "filename",
                "description",
                "status"
            ),
            show="headings",
            height=7,
            selectmode="browse"
        )

        self.pdf_tree.heading(
            "filename",
            text="PDF File"
        )

        self.pdf_tree.heading(
            "description",
            text="Description"
        )

        self.pdf_tree.heading(
            "status",
            text="Status"
        )

        self.pdf_tree.column(
            "filename",
            width=230,
            minwidth=150,
            anchor="w"
        )

        self.pdf_tree.column(
            "description",
            width=430,
            minwidth=250,
            anchor="w"
        )

        self.pdf_tree.column(
            "status",
            width=90,
            minwidth=80,
            anchor="centre"
        )

        vertical_scrollbar = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.pdf_tree.yview
        )

        horizontal_scrollbar = ttk.Scrollbar(
            table_frame,
            orient="horizontal",
            command=self.pdf_tree.xview
        )

        self.pdf_tree.configure(
            yscrollcommand=vertical_scrollbar.set,
            xscrollcommand=horizontal_scrollbar.set
        )

        self.pdf_tree.grid(
            row=0,
            column=0,
            sticky="nsew"
        )

        vertical_scrollbar.grid(
            row=0,
            column=1,
            sticky="ns"
        )

        horizontal_scrollbar.grid(
            row=1,
            column=0,
            sticky="ew"
        )

        table_frame.rowconfigure(
            0,
            weight=1
        )

        table_frame.columnconfigure(
            0,
            weight=1
        )

        # Select a PDF and load its description.
        self.pdf_tree.bind(
            "<<TreeviewSelect>>",
            self.on_pdf_selected
        )

        # Double-click also focuses the description input.
        self.pdf_tree.bind(
            "<Double-1>",
            self.on_pdf_double_click
        )

        # Enable drag and drop.
        for widget in (
            self.drop_frame,
            self.drop_instruction_label,
            self.pdf_tree
        ):
            widget.drop_target_register(
                DND_FILES
            )

            widget.dnd_bind(
                "<<Drop>>",
                self.handle_pdf_drop
            )

            widget.dnd_bind(
                "<<DropEnter>>",
                self.handle_drop_enter
            )

            widget.dnd_bind(
                "<<DropLeave>>",
                self.handle_drop_leave
            )

        # -------------------------------------------------
        # PDF LIST BUTTONS
        # -------------------------------------------------

        pdf_button_frame = ttk.Frame(
            pdf_frame
        )

        pdf_button_frame.pack(
            fill="x",
            pady=(8, 0)
        )

        ttk.Button(
            pdf_button_frame,
            text="Add PDF Files",
            command=self.add_pdf_files
        ).pack(
            side="left",
            padx=(0, 6)
        )

        ttk.Button(
            pdf_button_frame,
            text="Remove Selected",
            command=self.remove_selected_pdf
        ).pack(
            side="left",
            padx=6
        )

        ttk.Button(
            pdf_button_frame,
            text="Clear List",
            command=self.clear_pdf_list
        ).pack(
            side="left",
            padx=6
        )

        self.pdf_count_label = ttk.Label(
            pdf_button_frame,
            text="0 PDF files selected"
        )

        self.pdf_count_label.pack(
            side="right"
        )

        # -------------------------------------------------
        # INDIVIDUAL DESCRIPTION EDITOR
        # -------------------------------------------------

        description_frame = ttk.LabelFrame(
            main_frame,
            text="2. Description for Selected PDF",
            padding=10
        )

        description_frame.pack(
            fill="x",
            pady=7
        )

        description_frame.columnconfigure(
            1,
            weight=1
        )

        ttk.Label(
            description_frame,
            text="Selected PDF:"
        ).grid(
            row=0,
            column=0,
            sticky="w",
            padx=5,
            pady=4
        )

        self.selected_pdf_label = ttk.Label(
            description_frame,
            text="No PDF selected",
            foreground="#555555"
        )

        self.selected_pdf_label.grid(
            row=0,
            column=1,
            columnspan=2,
            sticky="w",
            padx=5,
            pady=4
        )

        ttk.Label(
            description_frame,
            text="Description:"
        ).grid(
            row=1,
            column=0,
            sticky="w",
            padx=5,
            pady=4
        )

        self.description_entry = ttk.Entry(
            description_frame
        )

        self.description_entry.grid(
            row=1,
            column=1,
            sticky="ew",
            padx=5,
            pady=4
        )

        self.description_entry.bind(
            "<Return>",
            lambda event: self.apply_description()
        )

        ttk.Button(
            description_frame,
            text="Apply Description",
            command=self.apply_description
        ).grid(
            row=1,
            column=2,
            padx=5,
            pady=4
        )

        ttk.Label(
            description_frame,
            text=(
                "Select a PDF, type its description, then click "
                "Apply Description. Pressing Enter also applies it."
            ),
            foreground="#666666"
        ).grid(
            row=2,
            column=0,
            columnspan=3,
            sticky="w",
            padx=5,
            pady=(2, 0)
        )

        # -------------------------------------------------
        # COMMON HEADER INFORMATION
        # -------------------------------------------------

        details_frame = ttk.LabelFrame(
            main_frame,
            text="3. Common Header Information",
            padding=10
        )

        details_frame.pack(
            fill="x",
            pady=7
        )

        details_frame.columnconfigure(
            1,
            weight=1
        )

        common_fields = [
            (
                "Cost Centre ID:",
                "cost_centre_entry"
            ),
            (
                "Type:",
                "type_entry"
            ),
            (
                "Cost Type:",
                "cost_type_entry"
            ),
        ]

        for row, (
            label_text,
            attribute_name
        ) in enumerate(common_fields):

            ttk.Label(
                details_frame,
                text=label_text
            ).grid(
                row=row,
                column=0,
                sticky="w",
                padx=5,
                pady=4
            )

            entry = ttk.Entry(
                details_frame
            )

            entry.grid(
                row=row,
                column=1,
                sticky="ew",
                padx=5,
                pady=4
            )

            setattr(
                self,
                attribute_name,
                entry
            )

        # Optional helpful defaults.
        self.cost_centre_entry.insert(
            0,
            "10926200"
        )

        # -------------------------------------------------
        # SIGNATURE
        # -------------------------------------------------

        signature_frame = ttk.LabelFrame(
            main_frame,
            text="4. Signature",
            padding=10
        )

        signature_frame.pack(
            fill="x",
            pady=7
        )

        signature_frame.columnconfigure(
            1,
            weight=1
        )

        ttk.Label(
            signature_frame,
            text="Name:"
        ).grid(
            row=0,
            column=0,
            sticky="w",
            padx=5,
            pady=4
        )

        self.name_entry = ttk.Entry(
            signature_frame
        )

        self.name_entry.insert(
            0,
            "ROGIE BERNABE"
        )

        self.name_entry.grid(
            row=0,
            column=1,
            columnspan=2,
            sticky="ew",
            padx=5,
            pady=4
        )

        ttk.Label(
            signature_frame,
            text="Signature image:"
        ).grid(
            row=1,
            column=0,
            sticky="w",
            padx=5,
            pady=4
        )

        self.signature_label = ttk.Label(
            signature_frame,
            text="No signature image selected",
            wraplength=450
        )

        self.signature_label.grid(
            row=1,
            column=1,
            sticky="w",
            padx=5,
            pady=4
        )

        ttk.Button(
            signature_frame,
            text="Browse Image",
            command=self.select_signature
        ).grid(
            row=1,
            column=2,
            padx=5,
            pady=4
        )

        # -------------------------------------------------
        # OUTPUT FOLDER
        # -------------------------------------------------

        output_frame = ttk.LabelFrame(
            main_frame,
            text="5. Output Folder",
            padding=10
        )

        output_frame.pack(
            fill="x",
            pady=7
        )

        self.output_folder_label = ttk.Label(
            output_frame,
            text="No output folder selected",
            wraplength=650
        )

        self.output_folder_label.pack(
            side="left",
            fill="x",
            expand=True,
            padx=(0, 10)
        )

        ttk.Button(
            output_frame,
            text="Choose Folder",
            command=self.select_output_folder
        ).pack(
            side="right"
        )

    # -----------------------------------------------------
    # ADD PDF FILES
    # -----------------------------------------------------

    def add_pdf_files(self):

        selected_files = filedialog.askopenfilenames(
            title="Select One or Multiple PDF Files",
            filetypes=[
                (
                    "PDF Files",
                    "*.pdf"
                )
            ]
        )

        self.add_paths(
            selected_files
        )

    def add_paths(self, paths):

        added_count = 0
        ignored_items = []

        for item in paths:

            path = os.path.normpath(
                str(item).strip("{}")
            )

            paths_to_add = []

            if os.path.isdir(path):

                try:
                    paths_to_add = [
                        os.path.join(
                            path,
                            filename
                        )
                        for filename in os.listdir(path)
                        if filename.lower().endswith(
                            ".pdf"
                        )
                    ]

                except OSError as error:
                    ignored_items.append(
                        f"{os.path.basename(path)}: "
                        f"{error}"
                    )
                    continue

            elif (
                os.path.isfile(path)
                and path.lower().endswith(".pdf")
            ):

                paths_to_add = [
                    path
                ]

            else:

                ignored_items.append(
                    os.path.basename(path) or path
                )

            for pdf_path in paths_to_add:

                normalised_path = os.path.normpath(
                    pdf_path
                )

                if normalised_path not in self.pdf_files:

                    self.pdf_files.append(
                        normalised_path
                    )

                    # Each new PDF starts with no description.
                    self.pdf_descriptions[
                        normalised_path
                    ] = ""

                    added_count += 1

        self.refresh_pdf_table()

        if added_count:

            self.status_label.config(
                text=(
                    f"Added {added_count} "
                    "PDF file(s)"
                )
            )

            # Automatically select the first PDF that
            # does not yet have a description.
            self.select_first_missing_description()

        if ignored_items:

            messagebox.showwarning(
                "Some Files Were Ignored",
                (
                    "Only PDF files can be added."
                    "\n\n"
                    "Ignored:\n"
                    + "\n".join(ignored_items)
                )
            )

    # -----------------------------------------------------
    # DRAG AND DROP
    # -----------------------------------------------------

    def handle_pdf_drop(self, event):

        try:
            dropped_items = (
                self.root.tk.splitlist(
                    event.data
                )
            )

        except tk.TclError:
            dropped_items = [
                event.data
            ]

        self.set_drop_highlight(
            False
        )

        self.add_paths(
            dropped_items
        )

        return getattr(
            event,
            "action",
            None
        )

    def handle_drop_enter(self, event):

        self.set_drop_highlight(
            True
        )

        return getattr(
            event,
            "action",
            None
        )

    def handle_drop_leave(self, event):

        self.set_drop_highlight(
            False
        )

        return getattr(
            event,
            "action",
            None
        )

    def set_drop_highlight(self, active):

        if active:

            self.drop_frame.config(
                background="#dceeff",
                highlightbackground="#1976d2",
                highlightthickness=2
            )

            self.drop_instruction_label.config(
                background="#dceeff",
                text="Release to add PDF files"
            )

        else:

            self.drop_frame.config(
                background="#f4f4f4",
                highlightbackground="#8a8a8a",
                highlightthickness=1
            )

            self.drop_instruction_label.config(
                background="#f4f4f4",
                text=(
                    "Drag and drop PDF files here\n"
                    "or click Add PDF Files"
                )
            )

    # -----------------------------------------------------
    # PDF TABLE MANAGEMENT
    # -----------------------------------------------------

    def refresh_pdf_table(self):

        for item_id in self.pdf_tree.get_children():
            self.pdf_tree.delete(
                item_id
            )

        completed_count = 0

        for index, pdf_file in enumerate(
            self.pdf_files
        ):

            description = (
                self.pdf_descriptions
                .get(pdf_file, "")
                .strip()
            )

            if description:
                status = "READY"
                completed_count += 1

            else:
                status = "MISSING"

            self.pdf_tree.insert(
                "",
                tk.END,
                iid=str(index),
                values=(
                    os.path.basename(
                        pdf_file
                    ),
                    description,
                    status
                )
            )

        file_count = len(
            self.pdf_files
        )

        missing_count = (
            file_count - completed_count
        )

        self.pdf_count_label.config(
            text=(
                f"{file_count} PDF file(s), "
                f"{missing_count} description(s) missing"
            )
        )

        if file_count == 0:

            self.status_label.config(
                text="Drag PDF files into the box"
            )

        elif missing_count == 0:

            self.status_label.config(
                text=(
                    f"All {file_count} PDF files "
                    "have descriptions"
                )
            )

        else:

            self.status_label.config(
                text=(
                    f"{missing_count} PDF file(s) "
                    "still need descriptions"
                )
            )

    def get_selected_pdf_index(self):

        selection = self.pdf_tree.selection()

        if not selection:
            return None

        try:
            return int(
                selection[0]
            )

        except ValueError:
            return None

    def get_selected_pdf_path(self):

        selected_index = (
            self.get_selected_pdf_index()
        )

        if selected_index is None:
            return None

        if not (
            0 <= selected_index
            < len(self.pdf_files)
        ):
            return None

        return self.pdf_files[
            selected_index
        ]

    def on_pdf_selected(self, event=None):

        pdf_path = (
            self.get_selected_pdf_path()
        )

        if not pdf_path:

            self.selected_pdf_label.config(
                text="No PDF selected"
            )

            self.description_entry.delete(
                0,
                tk.END
            )

            return

        self.selected_pdf_label.config(
            text=os.path.basename(
                pdf_path
            )
        )

        saved_description = (
            self.pdf_descriptions
            .get(pdf_path, "")
        )

        self.description_entry.delete(
            0,
            tk.END
        )

        self.description_entry.insert(
            0,
            saved_description
        )

    def on_pdf_double_click(self, event=None):

        self.on_pdf_selected()

        self.description_entry.focus_set()

        self.description_entry.select_range(
            0,
            tk.END
        )

    def apply_description(self):

        pdf_path = (
            self.get_selected_pdf_path()
        )

        if not pdf_path:

            messagebox.showerror(
                "No PDF Selected",
                (
                    "Please select a PDF from "
                    "the list first."
                )
            )

            return

        description = (
            self.description_entry
            .get()
            .strip()
        )

        if not description:

            messagebox.showerror(
                "Missing Description",
                (
                    "Please type a description "
                    "for the selected PDF."
                )
            )

            return

        self.pdf_descriptions[
            pdf_path
        ] = description

        current_index = (
            self.get_selected_pdf_index()
        )

        self.refresh_pdf_table()

        # Select the next PDF with a missing description.
        next_index = self.find_next_missing_index(
            start_index=(
                current_index + 1
                if current_index is not None
                else 0
            )
        )

        if next_index is not None:

            self.pdf_tree.selection_set(
                str(next_index)
            )

            self.pdf_tree.focus(
                str(next_index)
            )

            self.pdf_tree.see(
                str(next_index)
            )

            self.on_pdf_selected()

            self.description_entry.focus_set()

        else:

            self.selected_pdf_label.config(
                text=(
                    os.path.basename(pdf_path)
                    + " - description saved"
                )
            )

            self.description_entry.delete(
                0,
                tk.END
            )

            self.status_label.config(
                text="All PDF descriptions are complete"
            )

    def find_next_missing_index(
        self,
        start_index=0
    ):

        file_count = len(
            self.pdf_files
        )

        if file_count == 0:
            return None

        # Check from the requested position to the end.
        for index in range(
            start_index,
            file_count
        ):

            pdf_path = self.pdf_files[
                index
            ]

            description = (
                self.pdf_descriptions
                .get(pdf_path, "")
                .strip()
            )

            if not description:
                return index

        # Wrap around and check the beginning.
        for index in range(
            0,
            min(start_index, file_count)
        ):

            pdf_path = self.pdf_files[
                index
            ]

            description = (
                self.pdf_descriptions
                .get(pdf_path, "")
                .strip()
            )

            if not description:
                return index

        return None

    def select_first_missing_description(self):

        missing_index = (
            self.find_next_missing_index(0)
        )

        if missing_index is None:
            return

        item_id = str(
            missing_index
        )

        self.pdf_tree.selection_set(
            item_id
        )

        self.pdf_tree.focus(
            item_id
        )

        self.pdf_tree.see(
            item_id
        )

        self.on_pdf_selected()

        self.description_entry.focus_set()

    def remove_selected_pdf(self):

        selected_index = (
            self.get_selected_pdf_index()
        )

        if selected_index is None:

            messagebox.showerror(
                "No PDF Selected",
                (
                    "Please select a PDF "
                    "to remove."
                )
            )

            return

        pdf_path = self.pdf_files[
            selected_index
        ]

        del self.pdf_files[
            selected_index
        ]

        self.pdf_descriptions.pop(
            pdf_path,
            None
        )

        self.selected_pdf_label.config(
            text="No PDF selected"
        )

        self.description_entry.delete(
            0,
            tk.END
        )

        self.refresh_pdf_table()

        self.select_first_missing_description()

    def clear_pdf_list(self):

        self.pdf_files.clear()
        self.pdf_descriptions.clear()

        self.selected_pdf_label.config(
            text="No PDF selected"
        )

        self.description_entry.delete(
            0,
            tk.END
        )

        self.refresh_pdf_table()

    # -----------------------------------------------------
    # SELECT SIGNATURE
    # -----------------------------------------------------

    def select_signature(self):

        selected_file = filedialog.askopenfilename(
            title="Select Signature Image",
            filetypes=[
                (
                    "Image Files",
                    "*.png *.jpg *.jpeg "
                    "*.bmp *.webp"
                ),
                (
                    "All Files",
                    "*.*"
                ),
            ]
        )

        if selected_file:

            self.signature_file = (
                os.path.normpath(
                    selected_file
                )
            )

            self.signature_label.config(
                text=os.path.basename(
                    self.signature_file
                )
            )

    # -----------------------------------------------------
    # SELECT OUTPUT FOLDER
    # -----------------------------------------------------

    def select_output_folder(self):

        selected_folder = (
            filedialog.askdirectory(
                title="Select Output Folder"
            )
        )

        if selected_folder:

            self.output_folder = (
                os.path.normpath(
                    selected_folder
                )
            )

            self.output_folder_label.config(
                text=self.output_folder
            )

    # -----------------------------------------------------
    # TEXT WRAPPING
    # -----------------------------------------------------

    def wrap_text(
        self,
        text,
        font_name,
        font_size,
        maximum_width
    ):

        if not text:
            return []

        words = text.split()
        lines = []
        current_line = ""

        for word in words:

            proposed_line = (
                f"{current_line} {word}".strip()
            )

            proposed_width = (
                pdfmetrics.stringWidth(
                    proposed_line,
                    font_name,
                    font_size
                )
            )

            if proposed_width <= maximum_width:

                current_line = proposed_line

            else:

                if current_line:

                    lines.append(
                        current_line
                    )

                current_line = word

        if current_line:

            lines.append(
                current_line
            )

        return lines

    # -----------------------------------------------------
    # CREATE PDF STAMP
    # -----------------------------------------------------

    def create_stamp(
        self,
        page_width,
        page_height,
        cost_centre,
        expense_type,
        description,
        cost_type,
        employee_name
    ):

        packet = BytesIO()

        stamp_canvas = canvas.Canvas(
            packet,
            pagesize=(
                page_width,
                page_height
            )
        )

        font_name = PDF_FONT
        font_size = 11
        line_spacing = 13

        header_x = (
            page_width * 0.32
        )

        header_top = (
            page_height - 28
        )

        maximum_text_width = (
            page_width
            - header_x
            - 30
        )

        # Only the entered values appear on the PDF.
        # Labels such as COST CENTRE ID and DESCRIPTION
        # are deliberately omitted.
        header_values = [
            cost_centre,
            expense_type,
            description,
            cost_type
        ]

        header_lines = []

        for value in header_values:

            if value.strip():

                header_lines.extend(
                    self.wrap_text(
                        text=value.upper(),
                        font_name=font_name,
                        font_size=font_size,
                        maximum_width=(
                            maximum_text_width
                        )
                    )
                )

        if not header_lines:

            header_lines = [""]

        header_box_height = max(
            55,
            (
                len(header_lines)
                * line_spacing
                + 14
            )
        )

        # 50% transparent white background.
        stamp_canvas.saveState()

        try:
            stamp_canvas.setFillAlpha(
                0.50
            )

        except AttributeError:
            pass

        stamp_canvas.setFillColorRGB(
            1,
            1,
            1
        )

        stamp_canvas.rect(
            header_x - 7,
            (
                header_top
                - header_box_height
                + 9
            ),
            maximum_text_width + 14,
            header_box_height,
            fill=1,
            stroke=0
        )

        stamp_canvas.restoreState()

        # Header text.
        stamp_canvas.saveState()

        stamp_canvas.setFillColorRGB(
            0,
            0,
            0
        )

        stamp_canvas.setFont(
            font_name,
            font_size
        )

        current_y = header_top

        for line in header_lines:

            stamp_canvas.drawString(
                header_x,
                current_y,
                line
            )

            current_y -= line_spacing

        stamp_canvas.restoreState()

        # -------------------------------------------------
        # SIGNATURE IMAGE
        # -------------------------------------------------

        signature_width = min(
            220,
            page_width * 0.38
        )

        signature_height = 55

        signature_x = (
            page_width
            - signature_width
        ) / 2

        signature_y = 35

        if self.signature_file:

            try:

                with Image.open(
                    self.signature_file
                ) as original_image:

                    signature_image = (
                        original_image.copy()
                    )

                signature_image.thumbnail(
                    (
                        int(
                            signature_width * 3
                        ),
                        int(
                            signature_height * 3
                        )
                    )
                )

                if signature_image.mode not in (
                    "RGBA",
                    "RGB"
                ):

                    signature_image = (
                        signature_image.convert(
                            "RGBA"
                        )
                    )

                image_buffer = BytesIO()

                signature_image.save(
                    image_buffer,
                    format="PNG"
                )

                image_buffer.seek(0)

                stamp_canvas.drawImage(
                    ImageReader(
                        image_buffer
                    ),
                    signature_x,
                    signature_y,
                    width=signature_width,
                    height=signature_height,
                    preserveAspectRatio=True,
                    anchor="c",
                    mask="auto"
                )

            except Exception as error:

                raise ValueError(
                    "Could not load signature image: "
                    f"{error}"
                ) from error

        # Name below the signature.
        stamp_canvas.setFont(
            font_name,
            8
        )

        stamp_canvas.setFillColorRGB(
            0,
            0,
            0
        )

        stamp_canvas.drawCentredString(
            page_width / 2,
            signature_y - 2,
            employee_name.upper()
        )

        stamp_canvas.save()

        packet.seek(0)

        return PdfReader(
            packet
        ).pages[0]

    # -----------------------------------------------------
    # CREATE OUTPUT PATH
    # -----------------------------------------------------

    def create_output_path(
        self,
        input_pdf
    ):

        input_filename = os.path.basename(
            input_pdf
        )

        base_name = os.path.splitext(
            input_filename
        )[0]

        output_path = os.path.join(
            self.output_folder,
            f"{base_name}_stamped.pdf"
        )

        counter = 2

        while os.path.exists(
            output_path
        ):

            output_path = os.path.join(
                self.output_folder,
                (
                    f"{base_name}_stamped_"
                    f"{counter}.pdf"
                )
            )

            counter += 1

        return output_path

    # -----------------------------------------------------
    # STAMP ONE PDF
    # -----------------------------------------------------

    def stamp_single_pdf(
        self,
        input_pdf,
        output_pdf
    ):

        description = (
            self.pdf_descriptions
            .get(input_pdf, "")
            .strip()
        )

        if not description:

            raise ValueError(
                "No description has been assigned "
                "to this PDF."
            )

        reader = PdfReader(
            input_pdf
        )

        if reader.is_encrypted:

            decrypt_result = reader.decrypt(
                ""
            )

            if decrypt_result == 0:

                raise ValueError(
                    "The PDF is password protected."
                )

        writer = PdfWriter()

        cost_centre = (
            self.cost_centre_entry
            .get()
            .strip()
        )

        expense_type = (
            self.type_entry
            .get()
            .strip()
        )

        cost_type = (
            self.cost_type_entry
            .get()
            .strip()
        )

        employee_name = (
            self.name_entry
            .get()
            .strip()
        )

        for page in reader.pages:

            page_width = float(
                page.mediabox.width
            )

            page_height = float(
                page.mediabox.height
            )

            stamp_page = self.create_stamp(
                page_width=page_width,
                page_height=page_height,
                cost_centre=cost_centre,
                expense_type=expense_type,
                description=description,
                cost_type=cost_type,
                employee_name=employee_name
            )

            page.merge_page(
                stamp_page
            )

            writer.add_page(
                page
            )

        with open(
            output_pdf,
            "wb"
        ) as output_file:

            writer.write(
                output_file
            )

    # -----------------------------------------------------
    # STAMP ALL PDF FILES
    # -----------------------------------------------------

    def stamp_all_pdfs(self):

        if not self.pdf_files:

            messagebox.showerror(
                "No PDF Files",
                (
                    "Please add at least "
                    "one PDF file."
                )
            )

            return

        # Ensure every PDF has a description.
        missing_descriptions = [
            os.path.basename(pdf_file)
            for pdf_file in self.pdf_files
            if not (
                self.pdf_descriptions
                .get(pdf_file, "")
                .strip()
            )
        ]

        if missing_descriptions:

            messagebox.showerror(
                "Missing Descriptions",
                (
                    "Each PDF needs its own description."
                    "\n\n"
                    "Missing descriptions:\n"
                    + "\n".join(
                        missing_descriptions
                    )
                )
            )

            self.select_first_missing_description()

            return

        if not self.signature_file:

            messagebox.showerror(
                "Missing Signature",
                (
                    "Please select a "
                    "signature image."
                )
            )

            return

        if not self.name_entry.get().strip():

            messagebox.showerror(
                "Missing Name",
                (
                    "Please enter the name "
                    "below the signature."
                )
            )

            return

        if not self.output_folder:

            messagebox.showerror(
                "Missing Output Folder",
                (
                    "Please choose an "
                    "output folder."
                )
            )

            return

        os.makedirs(
            self.output_folder,
            exist_ok=True
        )

        total_files = len(
            self.pdf_files
        )

        successful_files = []
        failed_files = []

        self.stamp_button.config(
            state="disabled"
        )

        self.progress["value"] = 0

        try:

            for file_number, input_pdf in enumerate(
                self.pdf_files,
                start=1
            ):

                filename = os.path.basename(
                    input_pdf
                )

                self.status_label.config(
                    text=(
                        f"Processing {file_number} "
                        f"of {total_files}: "
                        f"{filename}"
                    )
                )

                self.root.update_idletasks()

                try:

                    output_pdf = (
                        self.create_output_path(
                            input_pdf
                        )
                    )

                    self.stamp_single_pdf(
                        input_pdf,
                        output_pdf
                    )

                    successful_files.append(
                        output_pdf
                    )

                except Exception as error:

                    failed_files.append(
                        (
                            filename,
                            str(error)
                        )
                    )

                self.progress["value"] = (
                    file_number
                    / total_files
                ) * 100

                self.root.update_idletasks()

        finally:

            self.stamp_button.config(
                state="normal"
            )

        successful_count = len(
            successful_files
        )

        failed_count = len(
            failed_files
        )

        if failed_count == 0:

            self.status_label.config(
                text=(
                    f"Completed: "
                    f"{successful_count} "
                    "PDF file(s)"
                )
            )

            messagebox.showinfo(
                "Batch Completed",
                (
                    f"{successful_count} "
                    "PDF file(s) were stamped "
                    "successfully.\n\n"
                    "Saved in:\n"
                    f"{self.output_folder}"
                )
            )

            self.open_output_folder()

        else:

            self.status_label.config(
                text=(
                    f"Completed with "
                    f"{failed_count} error(s)"
                )
            )

            failed_summary = "\n".join(
                (
                    f"{filename}: {error}"
                    for filename, error
                    in failed_files
                )
            )

            messagebox.showwarning(
                "Batch Completed with Errors",
                (
                    f"Successful: "
                    f"{successful_count}\n"
                    f"Failed: "
                    f"{failed_count}\n\n"
                    f"{failed_summary}\n\n"
                    "Output folder:\n"
                    f"{self.output_folder}"
                )
            )

    # -----------------------------------------------------
    # OPEN OUTPUT FOLDER
    # -----------------------------------------------------

    def open_output_folder(self):

        if (
            not self.output_folder
            or not os.path.isdir(
                self.output_folder
            )
        ):
            return

        try:

            if sys.platform.startswith(
                "win"
            ):

                os.startfile(
                    self.output_folder
                )

            elif sys.platform == "darwin":

                subprocess.Popen(
                    [
                        "open",
                        self.output_folder
                    ]
                )

            else:

                subprocess.Popen(
                    [
                        "xdg-open",
                        self.output_folder
                    ]
                )

        except OSError:
            pass


# ---------------------------------------------------------
# START APPLICATION
# ---------------------------------------------------------

if __name__ == "__main__":

    root = TkinterDnD.Tk()

    style = ttk.Style(
        root
    )

    try:
        style.theme_use(
            "vista"
        )

    except tk.TclError:
        pass

    app = PDFStamperApp(
        root
    )

    root.mainloop()