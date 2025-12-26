import base64
import math
from io import BytesIO
from PIL import Image
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
from database.task_db import get_face_events
IMAGES_PER_PAGE = 25
ROWS = 5
COLS = 5


import base64
from io import BytesIO
from PIL import Image

def base64_to_image(b64: str):
    if not b64:
        return None

    # bỏ header nếu có
    if "," in b64:
        b64 = b64.split(",")[1]

    # fix padding
    missing_padding = len(b64) % 4
    if missing_padding:
        b64 += "=" * (4 - missing_padding)

    try:
        return Image.open(BytesIO(base64.b64decode(b64)))
    except Exception as e:
        print("❌ Lỗi decode base64:", e)
        return None

def show_face_gallery(face_events):
    """
    face_events = [
        {
            "name": "chien",
            "time_in": datetime,
            "Image3": "base64..."
        },
        ...
    ]
    """

    total_pages = math.ceil(len(face_events) / IMAGES_PER_PAGE)
    current_page = [0]  # dùng list để mutable trong callback

    fig, axes = plt.subplots(ROWS, COLS, figsize=(12, 12))
    plt.subplots_adjust(bottom=0.12)

    def render_page():
        for ax in axes.flat:
            ax.clear()
            ax.axis("off")

        start = current_page[0] * IMAGES_PER_PAGE
        end = start + IMAGES_PER_PAGE
        page_items = face_events[start:end]

        for i, item in enumerate(page_items):
            r, c = divmod(i, COLS)
            img = base64_to_image(item["image2"])

            name = item.get("name", "Người lạ")
            time_in = item["time_in"].strftime("%Y-%m-%d %H:%M:%S")

            axes[r, c].imshow(img)
            axes[r, c].set_title(
                f"{name} | {time_in}",
                fontsize=9,
                color="white",
                backgroundcolor="black"
            )
            axes[r, c].axis("off")

        fig.suptitle(
            f"Trang {current_page[0] + 1}/{total_pages}",
            fontsize=14
        )
        fig.canvas.draw_idle()

    # ===== BUTTONS =====
    ax_prev = plt.axes([0.3, 0.02, 0.15, 0.05])
    ax_next = plt.axes([0.55, 0.02, 0.15, 0.05])

    btn_prev = Button(ax_prev, "◀ Trang trước")
    btn_next = Button(ax_next, "Trang sau ▶")

    def prev_page(event):
        if current_page[0] > 0:
            current_page[0] -= 1
            render_page()

    def next_page(event):
        if current_page[0] < total_pages - 1:
            current_page[0] += 1
            render_page()

    btn_prev.on_clicked(prev_page)
    btn_next.on_clicked(next_page)

    render_page()
    plt.show()
 
events = get_face_events(limit=200)
print(len(events))
show_face_gallery(events)
