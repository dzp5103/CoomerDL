import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox
import threading
import os
from app.utils.converter import MediaConverter

class ConverterPage(ctk.CTkFrame):
    def __init__(self, parent, app, **kwargs):
        super().__init__(parent, **kwargs)
        self.app = app
        self.tr = app.tr
        self.converter = MediaConverter()
        self.converting = False

        self.create_widgets()

    def create_widgets(self):
        # Header
        header = ctk.CTkFrame(self)
        header.pack(fill="x", padx=20, pady=20)
        ctk.CTkLabel(header, text=self.tr("Media Converter (FFmpeg)"), font=ctk.CTkFont(size=24, weight="bold")).pack(side="left")

        # Main Container
        main = ctk.CTkFrame(self)
        main.pack(fill="both", expand=True, padx=20, pady=10)

        # Input File
        ctk.CTkLabel(main, text="Input File:", font=("Arial", 12, "bold")).pack(anchor="w", padx=20, pady=(20, 5))
        input_frame = ctk.CTkFrame(main, fg_color="transparent")
        input_frame.pack(fill="x", padx=20, pady=5)

        self.input_entry = ctk.CTkEntry(input_frame)
        self.input_entry.pack(side="left", fill="x", expand=True)
        ctk.CTkButton(input_frame, text="Browse", width=100, command=self.browse_input).pack(side="left", padx=(10,0))

        # Output Format
        ctk.CTkLabel(main, text="Output Settings:", font=("Arial", 12, "bold")).pack(anchor="w", padx=20, pady=(20, 5))
        opts_frame = ctk.CTkFrame(main)
        opts_frame.pack(fill="x", padx=20, pady=5)

        ctk.CTkLabel(opts_frame, text="Format:").grid(row=0, column=0, padx=10, pady=10)
        self.format_combo = ctk.CTkComboBox(opts_frame, values=["mp4", "mkv", "webm", "avi", "mp3", "wav", "m4a", "gif"])
        self.format_combo.grid(row=0, column=1, padx=10, pady=10)
        self.format_combo.set("mp4")

        # Advanced Args (Conditional)
        self.adv_label = ctk.CTkLabel(opts_frame, text="Custom FFmpeg Args:")
        self.adv_entry = ctk.CTkEntry(opts_frame, width=300, placeholder_text="-vcodec libx264 -crf 23")

        # Check advanced mode
        self.refresh_advanced_visibility()

        # Progress
        self.progress_bar = ctk.CTkProgressBar(main)
        self.progress_bar.pack(fill="x", padx=20, pady=(40, 5))
        self.progress_bar.set(0)

        self.status_label = ctk.CTkLabel(main, text="Ready", text_color="gray")
        self.status_label.pack(anchor="w", padx=20, pady=5)

        # Buttons
        btn_frame = ctk.CTkFrame(main, fg_color="transparent")
        btn_frame.pack(pady=20)

        self.convert_btn = ctk.CTkButton(btn_frame, text="Start Conversion", command=self.start_conversion, font=("Arial", 14, "bold"))
        self.convert_btn.pack(side="left", padx=10)

        self.cancel_btn = ctk.CTkButton(btn_frame, text="Cancel", fg_color="red", hover_color="darkred", command=self.cancel_conversion, state="disabled")
        self.cancel_btn.pack(side="left", padx=10)

    def refresh_advanced_visibility(self):
        if self.app.advanced_mode:
            self.adv_label.grid(row=1, column=0, padx=10, pady=10)
            self.adv_entry.grid(row=1, column=1, columnspan=3, padx=10, pady=10, sticky="ew")
        else:
            self.adv_label.grid_forget()
            self.adv_entry.grid_forget()

    def browse_input(self):
        f = filedialog.askopenfilename()
        if f:
            self.input_entry.delete(0, "end")
            self.input_entry.insert(0, f)

    def start_conversion(self):
        inp = self.input_entry.get().strip()
        if not inp or not os.path.exists(inp):
            messagebox.showerror("Error", "Invalid input file.")
            return

        fmt = self.format_combo.get()
        # Auto-generate output path
        base, _ = os.path.splitext(inp)
        out = f"{base}_converted.{fmt}"

        args = self.adv_entry.get().strip() if self.app.advanced_mode else ""
        options = {"args": args}

        self.converting = True
        self.convert_btn.configure(state="disabled")
        self.cancel_btn.configure(state="normal")
        self.progress_bar.set(0)
        self.status_label.configure(text="Starting...")

        # Run in thread
        threading.Thread(target=self.run_conversion, args=(inp, out, options)).start()

    def run_conversion(self, inp, out, options):
        def update(p, msg):
            self.app.after(0, lambda: self.update_ui(p, msg))

        try:
            success = self.converter.convert(inp, out, options, update)
            self.app.after(0, lambda: self.finish_conversion(success))
        except Exception as e:
            self.app.after(0, lambda: self.update_ui(0, f"Error: {e}"))
            self.app.after(0, lambda: self.finish_conversion(False))

    def update_ui(self, p, msg):
        self.progress_bar.set(p)
        self.status_label.configure(text=msg)

    def finish_conversion(self, success):
        self.converting = False
        self.convert_btn.configure(state="normal")
        self.cancel_btn.configure(state="disabled")
        if success:
            messagebox.showinfo("Success", "Conversion finished successfully!")
            self.status_label.configure(text="Finished.")

    def cancel_conversion(self):
        if self.converting:
            self.converter.cancel()
