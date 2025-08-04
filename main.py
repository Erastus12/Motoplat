# ---------------------------------------------------------------------------------------------
# Author    : Erastus Keytaro Bangun
# Project   : Sistem Deteksi, Rekognisi Pelat Nomor dan Identifikasi Sepeda Motor yang Bergerak
# Created   : Juli 2025
# GitHub    : https://github.com/IAlreadyTried
# Note      : Bagian dari studi S1 - Teknologi Informasi Universitas Sumatera Utara (USU)
# ---------------------------------------------------------------------------------------------

import tkinter as tk # Library untuk GUI
from PIL import Image, ImageTk # Library untuk convert gambar supaya bisa di display di GUI
import cv2 # Library untuk looping frame pada video
import time # Library untuk tentukan FPS dan sinkronisasi 
from ultralytics import YOLO
import easyocr
import re # Library untuk Regular Expression
import mysql.connector # Library penghubung python dan database MySQL

# HUBUNGAN KE DATABASE
def get_koneksi_db():
    try:
        conn= mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="data_plat_motor"
    )
        print ("Koneksi Berhasil")
        return conn
    except mysql.connector.Error as err:
        print("Koneksi DB gagal:", err)
        return None


# Load model YOLOv10 dan model EasyOCR
plat_model = YOLO("models/model_yolov10_ku.pt")
reader = easyocr.Reader(['en'])

# flag-flag Global
detection_active = False
cap = cv2.VideoCapture("videos/contoh_3.mp4") #Kalau mau pakai kamera webcam, tinggal ganti nilai menjadi integer 0
prev_time = 0
last_log_time = 0
logged_texts = set()
detected_motor_images = {}  # Mapping: plat -> path gambar motor

# Buat root Tkinter utama (main)
root = tk.Tk()
root.state('zoomed') #Mengaktifkan Fullscreen(Zoomed)
root.title("Sistem Deteksi Plat Nomor")
root.geometry("1200x600")

# Hidupkan koneksi database
conn = get_koneksi_db()
cursor = conn.cursor(dictionary=True)

# ------------------------ SPLASH SCREEN ------------------------
splash_frame = tk.Frame(root)
splash_frame.pack(fill="both", expand=True, pady=100)

# logo_label = tk.Label(splash_frame, text="LOGO", bg="lightgray", font=("Arial", 32, "bold"), width=25, height=8, relief="ridge")
# logo_label.pack(pady=40)

gambar_logo = Image.open("assets/logo_aplikasi.jpg")
gambar_logo_tk = ImageTk.PhotoImage(gambar_logo)
logo_label = tk.Label(splash_frame, image=gambar_logo_tk)
logo_label.image = gambar_logo_tk
logo_label.pack(pady=0)

btn_frame = tk.Frame(splash_frame)
btn_frame.pack()

def show_penjelasan():
    splash_frame.pack_forget()
    penjelasan_frame.pack(fill="both", expand=True)

def show_monitoring():
    splash_frame.pack_forget()
    monitoring_frame.pack(fill="both", expand=True)

def kembali_ke_splash():
    penjelasan_frame.pack_forget()
    splash_frame.pack(fill="both", expand=True)

def masuk_ke_monitoring():
    penjelasan_frame.pack_forget()
    monitoring_frame.pack(fill="both", expand=True)

def toggle_detection():
    global detection_active
    detection_active = not detection_active
    toggle_button.config(text="Berhenti Monitoring" if detection_active else "Mulai Monitoring 🎥")

penjelasan_btn = tk.Button(btn_frame, text="Penjelasan", font=("Arial", 12), width=15, bg="lightgray", command=show_penjelasan)
penjelasan_btn.pack(side="left", padx=20, pady=10)

monitoring_btn = tk.Button(btn_frame, text="Monitoring", font=("Arial", 12), width=15, bg="lightgray", command=show_monitoring)
monitoring_btn.pack(side="right", padx=20, pady=10)

# ------------------------ PENJELASAN SCREEN ------------------------
penjelasan_frame = tk.Frame(root)
penjelasan_frame.grid_columnconfigure(0, weight=1)
penjelasan_frame.grid_columnconfigure(1, weight=0)  # Kolom tengah
penjelasan_frame.grid_columnconfigure(2, weight=1)

keterangan_frame = tk.Frame(penjelasan_frame, bg="lightgray", relief="ridge", borderwidth=2, width=400, height=350)
keterangan_frame.grid(row=0, column=1, padx=0, pady=40)
# keterangan_frame.grid_propagate(False)
keterangan_frame.grid_columnconfigure(0, weight=1)
keterangan_frame.grid_columnconfigure(1, weight=0)  # Kolom tengah
keterangan_frame.grid_columnconfigure(2, weight=1)

penjelasan_content = tk.Label(keterangan_frame, text="Penjelasan", bg="lightgray", font=("Arial", 20, "bold"))
penjelasan_content.grid(row=0, column=1, pady=10)

paragraf = tk.Label(keterangan_frame, justify="left", bg="#d3d3d3", wraplength=1000,
    text=(
        '"Aplikasi ini dirancang untuk membantu proses pemantauan kendaraan bermotor, khususnya sepeda motor, dengan mendeteksi dan mengenali plat nomor secara otomatis menggunakan teknologi Computer Vision dan Optical Character Recognition (OCR). Sistem ini memanfaatkan model deteksi objek YOLOv10 untuk mendeteksi lokasi plat nomor dan EasyOCR untuk membaca isi teks pada plat."\n\n'
        '"Aplikasi ini cocok digunakan dalam konteks monitoring lalu lintas terbatas, sistem gerbang otomatis, atau pengawasan area parkir, dengan keunggulan utama berupa deteksi real-time dan pencatatan otomatis."\n\n'
        'Cara menggunakan aplikasi:\n'
        '1. Masuk ke Halaman Monitoring\n'
        '    Klik tombol "Monitoring" pada halaman awal untuk memulai deteksi plat nomor.\n'
        '2. Aktifkan Kamera atau Input Video\n'
        '    Tekan tombol "Hidupkan Kamera 🎥" untuk memulai proses pendeteksian. Aplikasi akan menangkap gambar dari webcam atau video input dan menampilkan hasilnya secara real-time.\n'
        '3. Deteksi Plat Nomor\n'
        '    Sistem akan secara otomatis mendeteksi objek plat nomor di dalam frame dan menampilkan hasil OCR di sisi kanan sebagai daftar plat yang terdeteksi.\n'
        '4. Preview Crop dan Hasil OCR\n'
        '    Gambar potongan plat motor (hasil crop) akan ditampilkan sebagai pratinjau, beserta teks hasil pembacaan.\n'
        '5. Lihat Daftar Sepeda Motor Terdeteksi\n'
        '    Semua plat yang berhasil dikenali akan dicatat dalam daftar, lengkap dengan timestamp dan status validasi.\n'
        '\n'
        '    Developed by Erastus Bangun, 2025\n'
    ),
    font=("Arial", 14)
)
paragraf.grid(row=1, column=1, pady=5, padx=20)

penjelasan_nav = tk.Frame(penjelasan_frame)
penjelasan_nav.grid(row=1, column=1)

back_btn = tk.Button(penjelasan_nav, text="< Kembali", font=("Arial", 12), width=15, bg="lightgray", command=kembali_ke_splash)
back_btn.pack(side="left", padx=20)

penjelasan_next = tk.Button(penjelasan_nav, text="Monitoring >", font=("Arial", 12), width=15, bg="lightgray", command=masuk_ke_monitoring)
penjelasan_next.pack(side="right", padx=20)

# ------------------------ MONITORING SCREEN ------------------------
monitoring_frame = tk.Frame(root)

# Header Navigasi Monitoring
monitoring_nav = tk.Frame(monitoring_frame)
monitoring_nav.pack(anchor="w", fill="x")
back_monitoring_btn = tk.Button(monitoring_nav, text="< Kembali", font=("Arial", 12), command=lambda: [monitoring_frame.pack_forget(), splash_frame.pack(fill="both", expand=True)])
back_monitoring_btn.pack(side="left", padx=10, pady=5)

# Kontainer Utama
main_monitoring_area = tk.Frame(monitoring_frame)
main_monitoring_area.pack(fill="both", expand=True)


# Tampilan Kamera
camera_frame = tk.Frame(main_monitoring_area, bg="lightgray", relief="ridge", borderwidth=2)
camera_frame.grid(row=0, column=0, rowspan=2, padx=0, pady=0, sticky="nsew")
video_label = tk.Label(camera_frame)
video_label.pack(fill="both", expand=True)

# Data Kendaraan
live_data_frame = tk.Frame(main_monitoring_area, relief="ridge", borderwidth=2)
live_data_frame.grid(row=0, column=1, padx=0, pady=0, sticky="nsew")
title_label = tk.Label(live_data_frame, text="Sepeda Motor Terdeteksi", font=("Arial", 12, "bold"), bg="lightgray", width=30)
title_label.pack(fill="x")

# Preview Crop
preview_frame = tk.Frame(main_monitoring_area, relief="ridge", borderwidth=2)
preview_frame.grid(row=0, column=2, padx=0, pady=0, sticky="nsew")
preview_label = tk.Label(preview_frame, text="Preview OCR", font=("Arial", 12, "bold"), bg="lightgray", width=49)
preview_label.pack()
preview_image_label = tk.Label(preview_frame)
preview_image_label.pack()

#Preview Data Sepeda Motor
data_sepeda_motor_frame = tk.Frame(main_monitoring_area, relief="ridge", borderwidth=2)
data_sepeda_motor_frame.grid(row=1, column=1, columnspan=2, padx=0, pady=0, sticky="nsew")

#Gambar Motornya
gambar_sepeda_motor_frame = tk.Frame(data_sepeda_motor_frame, bg="lightgray", relief="ridge", borderwidth=2, width=347)
gambar_sepeda_motor_frame.grid(row=0, column=0, padx=0, pady=0, sticky="nsw")

# Load gambar
motornya = Image.open("assets/place_holder_gambar.jpg") #(Rasionya 1 : 1.34 )
motornya_tk = ImageTk.PhotoImage(motornya)

# Tempelkan ke label
label_gambar = tk.Label(gambar_sepeda_motor_frame, image=motornya_tk)
label_gambar.image = motornya_tk # simpan referensi agar tidak hilang dari memori
label_gambar.pack()

# Frame untuk informasi kendaraan (di sebelah gambar)
info_kendaraan_frame = tk.Frame(data_sepeda_motor_frame, padx=10, pady=5)
info_kendaraan_frame.grid(row=0, column=1, sticky="nsw")

data_fields = {
    "Nomor Polisi": "-",
    "Merk Motor": "-",
    "Model": "-",
    "Warna": "-",
    "Tahun": "-",
    "Akhir Pajak": "-",
    "Akhir STNK": "-",
    "Status": "-",
    "Pelanggaran": "-",
}

info_labels = {}

for i, (label, value) in enumerate(data_fields.items()):
    lbl = tk.Label(info_kendaraan_frame, text=label, anchor="w", font=("Arial", 14, "bold"))
    lbl.grid(row=i, column=0, sticky="w", pady=2)

    val = tk.Label(info_kendaraan_frame, text=value, anchor="w", font=("Arial", 14))
    val.grid(row=i, column=1, sticky="w", pady=2, padx=10)

    info_labels[label] = val

main_monitoring_area.grid_rowconfigure(1, weight=1)
main_monitoring_area.grid_columnconfigure(1, weight=1)
data_sepeda_motor_frame.grid_rowconfigure(0, weight=1)
data_sepeda_motor_frame.grid_columnconfigure(1, weight=1)

result_rows = []
last_logged_labels = []

def tampilkan_gambar_motor(label):
    if label in detected_motor_images:
        path = detected_motor_images[label]
        try:
            # Tampilkan gambar
            motornya = Image.open(path)
            motornya = motornya.resize((338, 453))
            motornya_tk = ImageTk.PhotoImage(motornya)
            label_gambar.config(image=motornya_tk)
            label_gambar.image = motornya_tk

            # Hilangkan confidence dari label pakai RegEx
            plat_bersih = re.sub(r"\s*\(.*?\)", "", label).strip()
            # print("Plat yang dicari:", plat_bersih)  # debug

            cursor.execute("SELECT * FROM data_plat WHERE nomor_polisi = %s", (plat_bersih,))
            row = cursor.fetchone()

            # Update data kendaraan (contoh dummy)
            contoh_data = {
                "Nomor Polisi": f": {label}",
                "Merk Motor": f": {row['merk']}",
                "Model": f": {row['model']}",
                "Warna": f": {row['warna']}",
                "Tahun": f": {row['tahun']}",
                "Akhir Pajak": f": {row['akhir_pajak']}",
                "Akhir STNK": f": {row['akhir_stnk']}",
                "Status": f": {row['status']}",
                "Pelanggaran": f": {row['pelanggaran']}",
            }

            for key in info_labels:
                info_labels[key].config(text=contoh_data.get(key, "-"))

        except Exception as e:
            print("Gagal membuka gambar:", e)

def update_detection_list(labels):
    global last_logged_labels, last_log_time

    now = time.time()
    if now - last_log_time >= .5:
        last_log_time = now
        if labels != last_logged_labels:
            last_logged_labels = labels.copy()
            for row in result_rows:
                row.destroy()
            result_rows.clear()
            for label_text in labels:
                row = tk.Frame(live_data_frame)
                row.pack(fill="x", pady=2)
                icon = tk.Label(row, text="🏍️", font=("Arial", 14))
                icon.pack(side="left", padx=5)
                plate = tk.Label(row, text=label_text, font=("Arial", 14))
                plate.pack(side="left", padx=10)
                stat = tk.Label(row, text="✅", font=("Arial", 14))
                stat.pack(side="right", padx=5)
                result_rows.append(row)

# Tambahkan canvas dan scrollbar untuk daftar deteksi
scroll_canvas = tk.Canvas(live_data_frame, borderwidth=0, width=300, height=200)
scroll_frame = tk.Frame(scroll_canvas)
scrollbar = tk.Scrollbar(live_data_frame, orient="vertical", command=scroll_canvas.yview)
scroll_canvas.configure(yscrollcommand=scrollbar.set)

scrollbar.pack(side="right", fill="y")
scroll_canvas.pack(side="left", fill="both", expand=True)
scroll_canvas.create_window((0, 0), window=scroll_frame, anchor="nw")

# Update scrollregion saat isi bertambah
scroll_frame.bind("<Configure>", lambda e: scroll_canvas.configure(scrollregion=scroll_canvas.bbox("all")))

# Fungsi untuk update list sepeda motor terdeteksi tanpa menghapus entry-entry sebelumnya
def append_detection_list(labels):
    for label_text in labels:
        if label_text not in logged_texts:
            row = tk.Frame(scroll_frame)
            row.pack(fill="x", pady=2)

            icon = tk.Label(row, text="🏍️", font=("Arial", 14))
            icon.pack(side="left", padx=5)

            btn = tk.Button(row, text=label_text, font=("Arial", 12), relief="raised",
                            command=lambda lbl=label_text: tampilkan_gambar_motor(lbl))
            btn.pack(side="left", padx=10)

            try:
                # Hilangkan confidence dari label pakai RegEx juga
                plat_bersih = re.sub(r"\s*\(.*?\)", "", label_text).strip()
                print("Plat yang dicari:", plat_bersih)  # debug

                cursor.execute("SELECT * FROM data_plat WHERE nomor_polisi = %s", (plat_bersih,))
                row_db = cursor.fetchone()

                # Update data kendaraan (contoh dummy)
                if row_db['status'] == "Melanggar":
                    logonya = "❌"
                    warna = "red"
                else:
                    logonya = "✅"
                    warna = "green"

                stat = tk.Label(row, text=logonya, font=("Arial", 14), fg=warna)
                stat.pack(side="right", padx=5)
            except Exception as e:
                print("Gagal membuat logo:", e)

            logged_texts.add(label_text)

# Tombol Kamera & Data
footer_monitoring = tk.Frame(monitoring_frame)
footer_monitoring.pack(pady=10)

toggle_button = tk.Button(footer_monitoring, text="Mulai Monitoring 🎥", font=("Arial", 12), width=20, bg="lime", command=toggle_detection)
toggle_button.pack(side="left", padx=20)

data_btn = tk.Button(footer_monitoring, text="Tampilkan Data Sepeda Motor", font=("Arial", 12), width=30, bg="lightgray")
data_btn.pack(side="right", padx=20)

#Fungsi untuk memfilter plat yang terbaca
def filter_plat_nomor(text):
    # Hapus semua karakter selain huruf dan angka, lalu kapitalisasi
    clean_text = re.sub(r'[^A-Za-z0-9]', '', text).upper()

    # Format plat yang valid: 1-2 huruf + 4 angka + 3 huruf
    match = re.match(r'^([A-Z]{1,2})(\d{4})([A-Z]{3})$', clean_text)
    if match:
        wilayah, angka, huruf = match.groups()
        return f"{wilayah} {angka} {huruf}"
    return None

# Fungsi untuk memproses setiap frame
def update_frame():
    global prev_time, last_log_time, detected_motor_images

    ret, frame = cap.read()
    if not ret:
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)  # ulang dari awal jika video selesai
        root.after(10, update_frame)
        return

    current_time = time.time()
    detected_labels = []

    if detection_active:
        results = plat_model(frame, conf = 0.5)[0]
        for box in results.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            conf = float(box.conf[0])
            cls_id = int(box.cls[0])

            cropped = frame[y1:y2, x1:x2]

            center_plat_x = (x1 + x2)/2 #Centroid x (Titik Tengah Plat)
            center_plat_y = (y1 + y2)/2 #Centroid y (Titik Tengah Plat)

            h, w = frame.shape[:2]  # ukuran frame
            center_video_x = w // 2
            center_video_y = h // 2

            h_motor = (y2-y1)*14.3
            w_motor = 0.75 * h_motor
            plat_ke_motor = h_motor * 0.162

            # Hitungan supaya untuk setiap gambar motor yang dicapture, lokasi plat selalu berada ditengah gambar preview
            x1_motor = max(0, int(center_plat_x - (w_motor/2)))
            y1_motor = max(0, int(center_plat_y - plat_ke_motor - (h_motor/2)))
            x2_motor = min(w, int(center_plat_x + (w_motor/2)))
            y2_motor = min(h, int(center_plat_y - plat_ke_motor + (h_motor/2)))

            motor_cropped = frame[y1_motor:y2_motor, x1_motor:x2_motor]
            cropped_rgb = cv2.cvtColor(cropped, cv2.COLOR_BGR2RGB)
            motor_cropped_rgb = cv2.cvtColor(motor_cropped, cv2.COLOR_BGR2RGB)

            # Jalankan OCR setiap 0.5 detik
            text = "..."
            if current_time - last_log_time >= .5:
                ocr_result = reader.readtext(cropped_rgb)

                # Jalankan kalau hasil OCR ada dan Confidence nya >= 40%
                if ocr_result and ocr_result[0][2] >= 0.40:
                    text_mentah = ocr_result[0][1]  # hasil teks pertama
                    ocr_conf = ocr_result[0][2]  # confidence score EasyOCR
                    text_filtered = filter_plat_nomor(text_mentah) #Filter hasil plat nomor yang dibaca

                    if text_filtered:
                        text = text_filtered
                        label = f"{text} ({ocr_conf:.2f})"

                        if cropped.size > 0:
                            cropped_pil = Image.fromarray(cropped_rgb)
                            cropped_pil = cropped_pil.resize((490, 196)) # Rasionya 5:2
                            cropped_imgtk = ImageTk.PhotoImage(image=cropped_pil)
                            preview_image_label.imgtk = cropped_imgtk
                            preview_image_label.configure(image=cropped_imgtk)
                        file_gambar = f"hasil_crop/crop_{current_time}.jpg"
                        cropped_pil.save(file_gambar)

                        if motor_cropped.size > 0:
                            motor_cropped_pil = Image.fromarray(motor_cropped_rgb)
                            motor_cropped_pil = motor_cropped_pil.resize((347, 465)) # Rasionya 5:2
                            file_gambar_motor = f"hasil_crop_motor/crop_{current_time}.jpg"
                            motor_cropped_pil.save(file_gambar_motor)
                            detected_motor_images[label] = file_gambar_motor

                        detected_labels.append(label)
                    else:
                        text = "Tidak Valid"
                        label = f"{text} ({ocr_conf:.2f})"

                else:
                    text = "Tidak Terbaca"
                    ocr_conf = 0.0
                    label = f"{text} ({ocr_conf:.2f})"

            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2) # Gambar bounding box YOLO nya
            cv2.putText(frame, text, (x1, y1 - 10), #tampilkan hasil bacaan EasyOCR diatas bounding box YOLO
            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)

    # Tambahkan ke daftar jika waktunya logging
    if current_time - last_log_time >= .5:
        last_log_time = current_time
        append_detection_list(detected_labels)

    fps = 1 / (current_time - prev_time) if prev_time else 0
    prev_time = current_time
    cv2.putText(frame, f"FPS: {fps:.2f}", (10, 80),
                cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 255, 0), 5)

 # Resize frame supaya muat ke kotak 640x640 dan pertahankan aspect ratio
    h, w = frame.shape[:2]
    scale = min(680 / w, 680 / h)
    resized = cv2.resize(frame, (int(w * scale), int(h * scale)))
    frame_rgb = cv2.cvtColor(resized, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(frame_rgb)
    imgtk = ImageTk.PhotoImage(image=img)

    video_label.imgtk = imgtk
    video_label.configure(image=imgtk)
    root.after(10, update_frame)

update_frame() #Jalankan loop utama untuk pemrosesan setiap frame video capture cv2
root.mainloop() #Jalankan loop utama GUI TKinter
cap.release()
cv2.destroyAllWindows()
