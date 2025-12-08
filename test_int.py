import pandas as pd
import random
import os

# ===== 1. Đọc dữ liệu gốc =====
data_path = "PDACL-main/data/gowalla/gowalla.train"  # chỉnh lại nếu khác đường dẫn
df = pd.read_csv(data_path, sep="\s+", names=["user", "item"])

# ===== 2. Lấy 5% dữ liệu ngẫu nhiên =====
df_small = df.sample(frac=0.05, random_state=42).reset_index(drop=True)
print(f"Original dataset size: {len(df)} → Sampled 5%: {len(df_small)} bộ")

# ===== 3. Hàm tạo augmentation =====
def drop_edges(df, drop_ratio):
    n_drop = int(len(df) * drop_ratio)
    drop_idx = random.sample(range(len(df)), n_drop)
    df_new = df.drop(drop_idx).reset_index(drop=True)
    return df_new

# ===== 4. Tạo WPA (drop nhẹ 10%) và SPA (drop mạnh 50%) =====
df_wpa = drop_edges(df_small, 0.1)
df_spa = drop_edges(df_small, 0.5)

print(f"WPA dataset size: {len(df_wpa)}")
print(f"SPA dataset size: {len(df_spa)}")

# ===== 5. Lưu ra file =====
os.makedirs("augmented_data", exist_ok=True)
df_small.to_csv("augmented_data/gowalla_5p_original.csv", index=False)
df_wpa.to_csv("augmented_data/gowalla_5p_wpa.csv", index=False)
df_spa.to_csv("augmented_data/gowalla_5p_spa.csv", index=False)

# ===== 6. Hiển thị ví dụ =====
# ===== Hiển thị 10 dòng cuối của cả 3 tập, in ngang hàng =====
compare_df = pd.concat(
    [df_small.tail(10).reset_index(drop=True),
     df_wpa.tail(10).reset_index(drop=True),
     df_spa.tail(10).reset_index(drop=True)],
    axis=1
)

# Đổi tên cột để phân biệt
compare_df.columns = [
    "user_ori", "item_ori",
    "user_wpa", "item_wpa",
    "user_spa", "item_spa"
]

print(compare_df)


# print("Overlap WPA vs Original:", len(pd.merge(orig, wpa, on=['user','item'])))
# print("Overlap SPA vs Original:", len(pd.merge(orig, spa, on=['user','item'])))
