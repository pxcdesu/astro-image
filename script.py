import os
import time
import subprocess
import webbrowser
import requests
from tkinter import *
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk, ImageEnhance

# 定数
DEFAULT_CONTRAST = 1.0
DEFAULT_BRIGHTNESS = 1.0
DEFAULT_GAMMA = 1.0
DEFAULT_QUALITY = 85
APP_VERSION = "1.0.0"  # バージョン番号
UPDATE_URL = "https://github.com/pxcdesu/astro-image/archive/refs/heads/main.zip"

class AstroImageApp:
    def __init__(self, root):
        self.root = root
        self.root.title(f"Astro Image v{APP_VERSION}")
        self.root.geometry("1200x1000")

        # 変数の初期化
        self.input_folder_path = StringVar()
        self.output_folder_path = StringVar()
        self.output_filename_var = StringVar()
        self.output_format_var = StringVar(value="png")
        self.progress_var = IntVar()
        self.contrast_var = DoubleVar(value=DEFAULT_CONTRAST)
        self.brightness_var = DoubleVar(value=DEFAULT_BRIGHTNESS)
        self.gamma_var = DoubleVar(value=DEFAULT_GAMMA)
        self.quality_var = IntVar(value=DEFAULT_QUALITY)

        self.preview_image = None
        self.current_image = None

        # UIの構築
        self.create_preview_frame()
        self.create_settings_frame()
        self.create_update_button()

    def create_preview_frame(self):
        preview_frame = ttk.LabelFrame(self.root, text="プレビューと画像調整")
        preview_frame.pack(pady=10, padx=10, fill="x")

        self.preview_canvas = Canvas(preview_frame, width=300, height=300, bg="gray")
        self.preview_canvas.pack(side="left", padx=10, pady=10)

        controls_frame = ttk.Frame(preview_frame)
        controls_frame.pack(side="left", padx=10, fill="y")

        sliders = [
            ("コントラスト", self.contrast_var, 0.0, 2.0),
            ("明るさ", self.brightness_var, 0.0, 2.0),
            ("ガンマ", self.gamma_var, 0.1, 2.0),
            ("出力品質", self.quality_var, 1, 100)
        ]

        for label, var, min_val, max_val in sliders:
            frame = ttk.Frame(controls_frame)
            frame.pack(fill="x", pady=5)
            
            ttk.Label(frame, text=f"{label}:").pack()
            ttk.Scale(frame, from_=min_val, to=max_val, variable=var,
                      command=self.update_preview, orient="horizontal", length=200).pack()

        ttk.Button(controls_frame, text="設定をリセット", command=self.reset_settings).pack(pady=10)

    def create_settings_frame(self):
        settings_frame = ttk.LabelFrame(self.root, text="入出力設定")
        settings_frame.pack(pady=10, padx=10, fill="x")

        ttk.Label(settings_frame, text="入力フォルダ:").pack(pady=5)
        ttk.Label(settings_frame, textvariable=self.input_folder_path, relief="sunken", width=50).pack(pady=5)
        ttk.Button(settings_frame, text="フォルダ指定", command=self.select_input_folder).pack(pady=5)

        ttk.Label(settings_frame, text="出力フォルダ:").pack(pady=5)
        ttk.Label(settings_frame, textvariable=self.output_folder_path, relief="sunken", width=50).pack(pady=5)
        ttk.Button(settings_frame, text="エクスポート先指定", command=self.select_output_folder).pack(pady=5)

        ttk.Label(settings_frame, text="出力ファイル名:").pack(pady=5)
        ttk.Entry(settings_frame, textvariable=self.output_filename_var, width=50).pack(pady=5)

        self.export_button = ttk.Button(settings_frame, text="エクスポート", command=self.export_images, state="disabled")
        self.export_button.pack(pady=20)

    def create_update_button(self):
        update_button = ttk.Button(self.root, text="アップデートをダウンロード", command=self.download_update)
        update_button.pack(pady=10)

    def download_update(self):
        try:
            save_path = filedialog.askdirectory(title="アップデートの保存先を選択")
            if not save_path:
                return

            zip_file_path = os.path.join(save_path, "astro-image-update.zip")
            response = requests.get(UPDATE_URL, stream=True)
            total_size = int(response.headers.get('content-length', 0))

            with open(zip_file_path, "wb") as f:
                downloaded_size = 0
                for chunk in response.iter_content(1024):
                    if chunk:
                        f.write(chunk)
                        downloaded_size += len(chunk)
                        progress = int(downloaded_size * 100 / total_size)
                        self.progress_var.set(progress)
                        self.root.update_idletasks()

            messagebox.showinfo("アップデート", f"アップデートがダウンロードされました！\n{zip_file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"アップデートのダウンロードに失敗しました: {e}")

    def reset_settings(self):
        self.contrast_var.set(DEFAULT_CONTRAST)
        self.brightness_var.set(DEFAULT_BRIGHTNESS)
        self.gamma_var.set(DEFAULT_GAMMA)
        self.quality_var.set(DEFAULT_QUALITY)
        self.update_preview()

    def select_input_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.input_folder_path.set(folder)

    def select_output_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.output_folder_path.set(folder)

    def update_preview(self, event=None):
        if self.current_image:
            img = self.apply_image_adjustments(self.current_image.copy())
            img.thumbnail((300, 300))
            self.preview_image = ImageTk.PhotoImage(img)
            self.preview_canvas.delete("all")
            self.preview_canvas.create_image(150, 150, image=self.preview_image)
            self.root.update_idletasks()

    def apply_image_adjustments(self, image):
        img = ImageEnhance.Contrast(image).enhance(self.contrast_var.get())
        img = ImageEnhance.Brightness(img).enhance(self.brightness_var.get())

        gamma = self.gamma_var.get()
        gamma_lookup = [int(((i / 255.0) ** (1.0 / gamma)) * 255) for i in range(256)]
        return img.point(lambda x: gamma_lookup[min(255, max(0, int(x)))])

    def export_images(self):
        messagebox.showinfo("エクスポート", "画像のエクスポート処理を実行します。（実装予定）")

if __name__ == "__main__":
    root = Tk()
    app = AstroImageApp(root)
    root.mainloop()
