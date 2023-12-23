import typing
import pathlib
from PIL import Image, ImageDraw, ImageFont
import git

DATA_READ_LIMIT_BYTES = 100_000


def draw_hex_matrix_to_image(
    image: Image.Image,
    hex_matrix: typing.List[typing.List[str]],
    font: ImageFont.FreeTypeFont,
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


def draw_title_to_image(
    image: Image.Image, font: ImageFont.FreeTypeFont, title: str
) -> Image.Image:
    draw = ImageDraw.Draw(image)
    draw.text(xy=(500, 1410 - font.size), text=title, font=font)
    return image


def draw_commit_list_to_image(
    image: Image.Image,
    anchor: typing.Tuple[int, int],
    font: ImageFont.FreeTypeFont,
    commits: typing.List[str],
) -> Image.Image:
    draw = ImageDraw.Draw(image)
    x_anchor, y_anchor = anchor
    for index, commit in enumerate(reversed(commits)):
        y_position = y_anchor + font.size * index
        draw.text(
            xy=(500, y_position),
            font=font,
            text=commit,
        )
    return image


def get_commit_list(repo: git.Repo, author: str | None = None) -> typing.List[str]:
    result: typing.List[str] = []
    commits: typing.List[git.Commit] = list(repo.iter_commits())
    for commit in commits:
        if author is not None and commit.author != author:
            continue
        result.append(f"{commit.message.strip()}")
    return result


def get_hex_matrix(
    file_path: pathlib.Path, size: typing.Tuple[int, int]
) -> typing.List[typing.List[str]]:
    hex_matrix: typing.List[typing.List[str]] = []

    with open(file_path, "rb") as file:
        data = file.read()[:DATA_READ_LIMIT_BYTES]

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
    font_path = "fonts/GidoleFont/Gidole-Regular.ttf"
    hex_font = ImageFont.truetype(font_path, size=10)
    title_font = ImageFont.truetype(font_path, size=75)
    hex_matrix = get_hex_matrix(file_path=pathlib.Path("test.bin"), size=(50, 200))
    image: Image.Image = Image.new(mode="RGB", size=(1000, 1410), color="#606B73")
    image = draw_hex_matrix_to_image(image=image, hex_matrix=hex_matrix, font=hex_font)
    image = draw_title_to_image(image=image, font=title_font, title="OPUS BUILD 14")

    repo = git.Repo(".")
    commits = get_commit_list(repo=repo)
    image = draw_commit_list_to_image(
        image=image, anchor=(500, 0), font=hex_font, commits=commits
    )

    image.save("test.png")


if __name__ == "__main__":
    # get a list of commits

    create_image()
