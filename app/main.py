import typing
import pathlib
from PIL import Image, ImageDraw, ImageFont

NUMBER_OF_CHARS = 100000
CHARS_PER_LINE = 220


def build_hex_image(
    image: Image.Image,
    hex_matrix: typing.List[typing.List[str]],
    font: ImageFont.ImageFont,
) -> Image.Image:
    draw = ImageDraw.Draw(image)

    for row_index, row in enumerate(hex_matrix, start=0):
        for col_index, item in enumerate(row, start=0):
            draw.text(
                xy=(row_index * 10, col_index * 10),
                text=item,
                fill="#000000",
                font=font,
            )

    return image


def format_input_file_to_hex(
    file_path: pathlib.Path, size: typing.Tuple[int, int]
) -> typing.List[typing.List[str]]:
    hex_matrix: typing.List[typing.List[str]] = []

    with open(file_path, "rb") as file:
        data = file.read()[:NUMBER_OF_CHARS]

    data_pointer = 0
    rows, columns = size

    for _ in range(rows):
        row_hex_values: typing.List[str] = []
        for _ in range(columns):
            formatted = f"{data[data_pointer]:02x}".upper()
            row_hex_values.append(formatted)
            data_pointer += 1
        hex_matrix.append(row_hex_values)

    return hex_matrix


def create_image() -> None:
    font = ImageFont.truetype("fonts/GidoleFont/Gidole-Regular.ttf", size=10)
    hex_matrix = format_input_file_to_hex(
        file_path=pathlib.Path("test.bin"), size=(50, 200)
    )
    image: Image.Image = Image.new(mode="RGB", size=(1000, 1410), color="#606B73")
    image = build_hex_image(image=image, hex_matrix=hex_matrix, font=font)
    image.save("test.png")


if __name__ == "__main__":
    create_image()
