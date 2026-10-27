"""Generate labelled PNG placeholder art for the first UI layout review.

This is a development-only helper. The game itself needs only tkinter and the
already-created PNG files; it does not import Pillow at runtime.
"""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
FONT_PATH = Path(r"C:\Windows\Fonts\msyh.ttc")
BACKGROUND_SIZE = (800, 300)
PORTRAIT_SIZE = (180, 250)

BACKGROUNDS = [
    ("lobby.png", "庄园门厅", "占位场景 · 门禁记录与访客簿", "#1b304d", "#477b8f"),
    ("tower.png", "钟楼", "占位场景 · 停摆的古董钟", "#30213d", "#7a536b"),
    ("archive.png", "西侧档案室", "占位场景 · 被翻找的信件", "#3c2a1d", "#93703e"),
    ("garden.png", "玻璃花房", "占位场景 · 温室与足迹", "#163a38", "#4e8871"),
    ("corridor.png", "员工走廊", "占位场景 · 洗衣记录与服务门", "#1f2c3f", "#526a7f"),
    ("boathouse.png", "旧船屋", "占位场景 · 财务账册与寄送箱", "#243545", "#496f80"),
]

PORTRAITS = [
    ("andrew.png", "安德鲁·魏", "钟表匠", "#6a4352"),
    ("elena.png", "艾琳娜·朴", "园丁", "#335f5a"),
    ("marco.png", "马可·陈", "档案研究员", "#4a5373"),
    ("naomi.png", "娜奥米·贝尔", "管家", "#745142"),
    ("victor.png", "维克多·黑尔", "庄园财务主管", "#615078"),
]


def font(size: int) -> ImageFont.FreeTypeFont:
    if not FONT_PATH.exists():
        raise FileNotFoundError(f"Required font not found: {FONT_PATH}")
    return ImageFont.truetype(FONT_PATH, size)


def center_text(draw: ImageDraw.ImageDraw, text: str, y: int, text_font: ImageFont.FreeTypeFont, color: str, width: int) -> None:
    box = draw.textbbox((0, 0), text, font=text_font)
    draw.text(((width - (box[2] - box[0])) / 2, y), text, font=text_font, fill=color)


def create_background(filename: str, title: str, subtitle: str, left: str, right: str) -> None:
    image = Image.new("RGB", BACKGROUND_SIZE, left)
    draw = ImageDraw.Draw(image)
    for x in range(BACKGROUND_SIZE[0]):
        ratio = x / (BACKGROUND_SIZE[0] - 1)
        start = tuple(int(left[index : index + 2], 16) for index in (1, 3, 5))
        end = tuple(int(right[index : index + 2], 16) for index in (1, 3, 5))
        color = tuple(round(start[i] + (end[i] - start[i]) * ratio) for i in range(3))
        draw.line((x, 0, x, BACKGROUND_SIZE[1]), fill=color)
    draw.rectangle((18, 18, BACKGROUND_SIZE[0] - 18, BACKGROUND_SIZE[1] - 18), outline="#e8b85a", width=3)
    draw.rectangle((43, 43, BACKGROUND_SIZE[0] - 43, BACKGROUND_SIZE[1] - 43), outline="#77d7d1", width=1)
    draw.line((85, 150, BACKGROUND_SIZE[0] - 85, 150), fill="#f4f0e7", width=1)
    center_text(draw, title, 78, font(48), "#f4f0e7", BACKGROUND_SIZE[0])
    center_text(draw, subtitle, 172, font(21), "#dbe4ed", BACKGROUND_SIZE[0])
    center_text(draw, "文字占位背景 · 可替换为正式美术", 232, font(13), "#77d7d1", BACKGROUND_SIZE[0])
    target = ROOT / "assets" / "cases" / "night-clock" / "locations" / filename
    target.parent.mkdir(parents=True, exist_ok=True)
    image.save(target)


def create_portrait(filename: str, name: str, role: str, color: str) -> None:
    image = Image.new("RGB", PORTRAIT_SIZE, color)
    draw = ImageDraw.Draw(image)
    draw.rectangle((9, 9, PORTRAIT_SIZE[0] - 10, PORTRAIT_SIZE[1] - 10), outline="#e8b85a", width=2)
    draw.ellipse((57, 41, 123, 107), outline="#f4f0e7", width=3)
    draw.polygon([(32, 192), (60, 120), (120, 120), (148, 192)], outline="#f4f0e7", fill="#24314c")
    center_text(draw, name, 198, font(22), "#f4f0e7", PORTRAIT_SIZE[0])
    center_text(draw, role, 227, font(13), "#77d7d1", PORTRAIT_SIZE[0])
    target = ROOT / "assets" / "cases" / "night-clock" / "portraits" / filename
    target.parent.mkdir(parents=True, exist_ok=True)
    image.save(target)


def create_ui_cover(relative_path: str, title: str, subtitle: str, left: str, right: str) -> None:
    """Create a labelled cover for the game's start screen."""
    image = Image.new("RGB", BACKGROUND_SIZE, left)
    draw = ImageDraw.Draw(image)
    for x in range(BACKGROUND_SIZE[0]):
        ratio = x / (BACKGROUND_SIZE[0] - 1)
        start = tuple(int(left[index : index + 2], 16) for index in (1, 3, 5))
        end = tuple(int(right[index : index + 2], 16) for index in (1, 3, 5))
        color = tuple(round(start[i] + (end[i] - start[i]) * ratio) for i in range(3))
        draw.line((x, 0, x, BACKGROUND_SIZE[1]), fill=color)
    draw.rectangle((18, 18, BACKGROUND_SIZE[0] - 18, BACKGROUND_SIZE[1] - 18), outline="#77d7d1", width=3)
    draw.rectangle((43, 43, BACKGROUND_SIZE[0] - 43, BACKGROUND_SIZE[1] - 43), outline="#e8b85a", width=1)
    center_text(draw, title, 83, font(46), "#f4f0e7", BACKGROUND_SIZE[0])
    center_text(draw, subtitle, 173, font(20), "#dbe4ed", BACKGROUND_SIZE[0])
    center_text(draw, "文字占位贴图 · 可替换为正式美术", 232, font(13), "#77d7d1", BACKGROUND_SIZE[0])
    target = ROOT / relative_path
    target.parent.mkdir(parents=True, exist_ok=True)
    image.save(target)


def main() -> None:
    for item in BACKGROUNDS:
        create_background(*item)
    for item in PORTRAITS:
        create_portrait(*item)
    create_ui_cover("assets/ui/start-screen.png", "文字推理游戏", "案件档案 · 开始页面", "#17233b", "#31546b")
    print("已生成 7 张场景/开始页贴图和 5 张人物肖像占位 PNG。")


if __name__ == "__main__":
    main()
