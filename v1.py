import qrcode
import json
import os

data = {
    "name": "Lý Văn Chiến",
    "birth_year": 2004
}

# Chuyển thành string JSON
data_str = json.dumps(data, ensure_ascii=False)

qr = qrcode.QRCode(
    version=2,  # version nhỏ vừa đủ cho text ngắn
    error_correction=qrcode.constants.ERROR_CORRECT_H,
    box_size=10,
    border=4
)
qr.add_data(data_str)
qr.make(fit=True)

# Tạo hình ảnh
img = qr.make_image(fill_color="black", back_color="white")

# Lưu file
if not os.path.exists("qr"):
    os.makedirs("qr")
filename = "qr/ly_van_chien.png"
img.save(filename)
print(f"✅ QR code đã lưu: {filename}")

# Hiển thị QR code (tùy chọn)
img.show()
