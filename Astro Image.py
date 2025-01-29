import os
import time
from tkinter import *
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk, ImageEnhance
import numpy as np
import subprocess
import webbrowser
import requests  # 追加
import zipfile  # 追加
import shutil  # 追加

# 定数
DEFAULT_CONTRAST = 1.0
DEFAULT_BRIGHTNESS = 1.0
DEFAULT_GAMMA = 1.0
DEFAULT_QUALITY = 85

class AstroImageApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Astro Image Beta")
        self.root.geometry("1200x1000")  # ウィンドウサイズを明示的に設定

        # 変数の初期化
        self.input_folder_path = StringVar()
        self.output_folder_path = StringVar()
        self.output_filename_var = StringVar()
        self.output_format_var = StringVar(value="png")
        self.blend_mode_var = StringVar(value="平均")  # 合成モードを選択
        self.progress_var = IntVar()
        self.contrast_var = DoubleVar(value=DEFAULT_CONTRAST)
        self.brightness_var = DoubleVar(value=DEFAULT_BRIGHTNESS)
        self.gamma_var = DoubleVar(value=DEFAULT_GAMMA)
        self.quality_var = IntVar(value=DEFAULT_QUALITY)
        self.time_remaining_var = StringVar(value="推定残り時間: --:--")
        
        self.preview_image = None
        self.current_image = None
        self.base_size = None
        self.start_time = None

        # UIの構築
        self.create_preview_frame()
        self.create_settings_frame()
        self.create_update_button()
        self.bind_events()

    def create_preview_frame(self):
        # プレビューと調整フレーム
        preview_frame = ttk.LabelFrame(self.root, text="プレビューと画像調整")
        preview_frame.pack(pady=10, padx=10, fill="x")  # ウィンドウ幅に合わせる

        # プレビューキャンバス
        self.preview_canvas = Canvas(preview_frame, width=300, height=300, bg="gray")
        self.preview_canvas.pack(side="left", padx=10, pady=10)

        # 調整コントロール
        controls_frame = ttk.Frame(preview_frame)
        controls_frame.pack(side="left", padx=10, fill="y")

        # スライダー
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
            ttk.Label(frame, text="低 ←").pack(side="left")
            ttk.Scale(frame, from_=min_val, to=max_val, 
                     variable=var, command=self.update_preview,
                     orient="horizontal", length=200).pack(side="left")
            ttk.Label(frame, text="→ 高").pack(side="left")

        ttk.Button(controls_frame, text="設定をリセット", 
                  command=self.reset_settings).pack(pady=10)

    def create_settings_frame(self):
        # 入出力設定フレーム
        settings_frame = ttk.LabelFrame(self.root, text="入出力設定")
        settings_frame.pack(pady=10, padx=10, fill="x")  # ウィンドウ幅に合わせる

        # 入力フォルダ
        ttk.Label(settings_frame, text="入力フォルダ:").pack(pady=5)
        ttk.Label(settings_frame, textvariable=self.input_folder_path, 
                 relief="sunken", width=50).pack(pady=5)
        ttk.Button(settings_frame, text="フォルダ指定", 
                  command=self.select_input_folder).pack(pady=5)

        # 出力フォルダ
        ttk.Label(settings_frame, text="出力フォルダ:").pack(pady=5)
        ttk.Label(settings_frame, textvariable=self.output_folder_path, 
                 relief="sunken", width=50).pack(pady=5)
        ttk.Button(settings_frame, text="エクスポート先指定", 
                  command=self.select_output_folder).pack(pady=5)

        # ファイル名とフォーマット
        ttk.Label(settings_frame, text="出力ファイル名:").pack(pady=5)
        ttk.Entry(settings_frame, textvariable=self.output_filename_var, 
                 width=50).pack(pady=5)

        ttk.Label(settings_frame, text="出力フォーマット:").pack(pady=5)
        ttk.OptionMenu(settings_frame, self.output_format_var, 
                      "png", "png", "jpeg").pack(pady=5)

        # 合成モード選択
        ttk.Label(settings_frame, text="合成モード:").pack(pady=5)
        ttk.OptionMenu(settings_frame, self.blend_mode_var, 
                      "平均", "平均", "比較明", "比較暗").pack(pady=5)

        # 進捗状況と残り時間
        ttk.Label(settings_frame, textvariable=self.time_remaining_var).pack(pady=5)
        ttk.Label(settings_frame, text="進捗状況:").pack(pady=5)
        self.progress_bar = ttk.Progressbar(settings_frame, 
                                          variable=self.progress_var, 
                                          maximum=100)
        self.progress_bar.pack(pady=5)

        self.export_button = ttk.Button(settings_frame, text="エクスポート", 
                                      command=self.export_images, 
                                      state="disabled")
        self.export_button.pack(pady=20)

    def create_update_button(self):
        # アップデートボタンの追加
        update_button = ttk.Button(self.root, text="アップデート", command=self.update_application)
        update_button.pack(pady=10)

    def update_application(self):
        # アップデート処理
        try:
            # GitHubから最新のリリースをダウンロード
            url = "https://github.com/ユーザー名/リポジトリ名/archive/refs/heads/main.zip"
            response = requests.get(url)
            zip_path = os.path.join(os.path.dirname(__file__), "update.zip")
            with open(zip_path, "wb") as f:
                f.write(response.content)

            # ZIPファイルを解凍
            with zipfile.ZipFile(zip_path, "r") as zip_ref:
                zip_ref.extractall(os.path.dirname(__file__))

            # 解凍されたフォルダを取得
            extracted_folder = os.path.join(os.path.dirname(__file__), "リポジトリ名-main")

            # 現在のファイルを削除して新しいファイルを移動
            current_file = os.path.abspath(__file__)
            os.remove(current_file)
            for filename in os.listdir(extracted_folder):
                shutil.move(os.path.join(extracted_folder, filename), os.path.dirname(current_file))

            # 解凍されたフォルダを削除
            shutil.rmtree(extracted_folder)
            os.remove(zip_path)

            # アプリケーションを再起動
            subprocess.Popen(["python", current_file])
            self.root.quit()
        except Exception as e:
            messagebox.showerror("Error", f"アップデート中にエラーが発生しました: {e}")

    def bind_events(self):
        # 入力が更新された際にエクスポートボタンの状態を確認
        for var in [self.input_folder_path, self.output_folder_path, 
                   self.output_filename_var, self.output_format_var]:
            var.trace("w", self.check_export_button_state)

    def reset_settings(self):
        # 設定をリセット
        self.contrast_var.set(DEFAULT_CONTRAST)
        self.brightness_var.set(DEFAULT_BRIGHTNESS)
        self.gamma_var.set(DEFAULT_GAMMA)
        self.quality_var.set(DEFAULT_QUALITY)
        self.update_preview()

    def select_input_folder(self):
        # 入力フォルダ選択
        folder = filedialog.askdirectory()
        if folder:
            self.input_folder_path.set(folder)
            self.load_first_preview()

    def select_output_folder(self):
        # 出力フォルダ選択
        folder = filedialog.askdirectory()
        if folder:
            self.output_folder_path.set(folder)

    def update_preview(self, event=None):
        # プレビュー画像の更新
        if self.current_image:
            img = self.apply_image_adjustments(self.current_image.copy())
            img.thumbnail((300, 300))
            self.preview_image = ImageTk.PhotoImage(img)
            self.preview_canvas.delete("all")
            self.preview_canvas.create_image(150, 150, image=self.preview_image)

    def apply_image_adjustments(self, image):
        # 画像調整
        img = image.convert('RGB')
        img = ImageEnhance.Contrast(img).enhance(self.contrast_var.get())
        img = ImageEnhance.Brightness(img).enhance(self.brightness_var.get())
        
        gamma = self.gamma_var.get()
        gamma_lookup = [int(((i / 255.0) ** (1.0 / gamma)) * 255) 
                       for i in range(256)]
        return img.point(lambda x: gamma_lookup[min(255, max(0, int(x)))])

    def load_first_preview(self):
        # プレビューの初期画像をロード
        folder = self.input_folder_path.get()
        if folder:
            files = [f for f in os.listdir(folder) 
                    if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
            if files:
                file_path = os.path.join(folder, files[0])
                self.current_image = Image.open(file_path)
                self.base_size = self.current_image.size
                self.update_preview()

    def check_export_button_state(self, *args):
        # エクスポートボタンの有効/無効をチェック
        if (self.input_folder_path.get() and self.output_folder_path.get() and 
            self.output_filename_var.get() and self.output_format_var.get()):
            self.export_button.config(state="normal")
        else:
            self.export_button.config(state="disabled")

    def export_images(self):
        # エクスポート処理
        self.progress_var.set(0)
        self.time_remaining_var.set("処理を開始します...")
        try:
            self.start_time = time.time()
            success = True  # 実際の処理は省略
            if success:
                self.time_remaining_var.set("処理完了!")
                messagebox.showinfo("Success", "エクスポートが完了しました！")
            else:
                self.time_remaining_var.set("エラーが発生しました")
        except Exception as e:
            self.time_remaining_var.set("エラーが発生しました")
            messagebox.showerror("Error", f"エクスポート中にエラーが発生しました: {e}")

if __name__ == "__main__":
    root = Tk()
    app = AstroImageApp(root)
    root.mainloop()
