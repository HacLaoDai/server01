
train_in  = "/home/lychien/Downloads/PDACL/PDACL-main/dataset/gowalla_main/gowalla.train"
test_in   = "/home/lychien/Downloads/PDACL/PDACL-main/dataset/gowalla_main/gowalla.test"
train_out = "/home/lychien/Downloads/PDACL/PDACL-main/dataset/gowalla/gowalla.train"
test_out  = "/home/lychien/Downloads/PDACL/PDACL-main/dataset/gowalla/gowalla.test"

max_user = 4000
max_item = 4000

# --- đọc train ---
train_users = set()
train_items = set()
train_lines = []

with open("/home/lychien/Downloads/PDACL/PDACL-main/dataset/gowalla_main/gowalla.train") as fin:
    for line in fin:
        u, i = map(int, line.strip().split())
        if u < max_user and i < max_item:
            train_lines.append((u, i))
            train_users.add(u)
            train_items.add(i)

# --- lọc test: chỉ giữ user có trong train ---
test_lines = []
with open("/home/lychien/Downloads/PDACL/PDACL-main/dataset/gowalla_main/gowalla.test") as fin:
    for line in fin:
        u, i = map(int, line.strip().split())
        if u in train_users and i in train_items:
            test_lines.append((u, i))

# --- ghi lại file ---
with open("/home/lychien/Downloads/PDACL/PDACL-main/dataset/gowalla/gowalla.train", "w") as fout:
    for u, i in train_lines:
        fout.write(f"{u} {i}\n")

with open("/home/lychien/Downloads/PDACL/PDACL-main/dataset/gowalla/gowalla.test", "w") as fout:
    for u, i in test_lines:
        fout.write(f"{u} {i}\n")

with open(train_out, "w") as fout:
    for u, i in train_lines:
        fout.write(f"{int(u)} {int(i)}\n")

with open(test_out, "w") as fout:
    for u, i in test_lines:
        fout.write(f"{int(u)} {int(i)}\n")

print(f"Final train users: {len(train_users)}, items: {len(train_items)}")
print(f"Final train lines: {len(train_lines)}, test lines: {len(test_lines)}")
