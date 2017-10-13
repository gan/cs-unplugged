"""Module for generating Pixel Painter resource."""

from PIL import Image, ImageDraw, ImageFont
from utils.retrieve_query_parameter import retrieve_query_parameter
from math import ceil
from yattag import Doc
import string

def resource(request, resource):
    """Create a image for Pixel Painter resource.

    Args:
        request: HTTP request object (HttpRequest).
        resource: Object of resource data (Resource).

    Returns:
        A dictionaries for each resource page.
    """
    STATIC_PATH = "static/img/resources/pixel-painter/{}.png"
    FONT_PATH = "static/fonts/PatrickHand-Regular.ttf"
    FONT = ImageFont.truetype(FONT_PATH, 80)
    FONT_SMALL = ImageFont.truetype(FONT_PATH, 50)
    TEXT_COLOUR = "#888"

    parameter_options = valid_options()
    method = retrieve_query_parameter(request, "method", parameter_options["method"])
    image_name = retrieve_query_parameter(request, "image", parameter_options["image"])

    image = Image.open(STATIC_PATH.format(image_name))
    (image_width, image_height) = image.size

    COLUMNS_PER_PAGE = 15
    ROWS_PER_PAGE = 20
    BOX_SIZE = 200
    IMAGE_SIZE_X = BOX_SIZE * COLUMNS_PER_PAGE
    IMAGE_SIZE_Y = BOX_SIZE * ROWS_PER_PAGE
    LINE_COLOUR = "#666"
    LINE_WIDTH = 1

    pages = []
    number_column_pages = ceil(image_width / COLUMNS_PER_PAGE)
    number_row_pages = ceil(image_height / ROWS_PER_PAGE)
    page_grid_coords = create_page_grid_coords(number_column_pages, number_row_pages)

    grid_page = grid_reference_page(page_grid_coords, image_name)
    pages.append({"type": "html", "data": grid_page})

    # For each page row
    for number_row_page in range(0, number_row_pages):
        page_start_row = (number_row_page) * ROWS_PER_PAGE
        # For each page column
        for number_column_page in range(0, number_column_pages):
            page_start_column = (number_column_page) * COLUMNS_PER_PAGE
            # Create page
            page = Image.new("RGB", (IMAGE_SIZE_X, IMAGE_SIZE_Y), "#fff")
            draw = ImageDraw.Draw(page)
            page_columns = min(COLUMNS_PER_PAGE, image_width - page_start_column)
            page_rows = min(ROWS_PER_PAGE, image_height - page_start_row)
            page_reference_added = False

            # Draw grid
            grid_width = page_columns * BOX_SIZE
            grid_height = page_rows * BOX_SIZE

            for x_coord in range(0, page_columns * BOX_SIZE, BOX_SIZE):
                draw.line(
                    [(x_coord, 0), (x_coord, grid_height)],
                    fill=LINE_COLOUR,
                    width=LINE_WIDTH
                )
            draw.line(
                [(page_columns * BOX_SIZE - 1, 0), (page_columns * BOX_SIZE - 1, grid_height)],
                fill=LINE_COLOUR,
                width=LINE_WIDTH
            )

            for y_coord in range(0, grid_height, BOX_SIZE):
                draw.line(
                    [(0, y_coord), (grid_width, y_coord)],
                    fill=LINE_COLOUR,
                    width=LINE_WIDTH
                )
            draw.line(
                [(0, grid_height - 1), (grid_width, grid_height - 1)],
                fill=LINE_COLOUR,
                width=LINE_WIDTH
            )

            # Draw text
            for column in range(0, page_columns):
                for row in range(0, page_rows):
                    pixel_value = image.getpixel((page_start_column + column, page_start_row + row))
                    text = str(1 - int(pixel_value / 255))
                    text_width, text_height = draw.textsize(text, font=FONT)
                    text_coord_x = (column * BOX_SIZE) + (BOX_SIZE / 2) - (text_width / 2)
                    text_coord_y = (row * BOX_SIZE) + (BOX_SIZE / 2) - (text_height / 2)
                    draw.text(
                        (text_coord_x, text_coord_y),
                        text,
                        font=FONT,
                        fill=TEXT_COLOUR
                    )

                    # Add page grid reference
                    if not page_reference_added and text == "0":
                        draw.text(
                            ((column * BOX_SIZE) + LINE_WIDTH * 4, (row * BOX_SIZE) + -4),
                            page_grid_coords[number_row_page][number_column_page],
                            font=FONT_SMALL,
                            fill=TEXT_COLOUR
                        )
                        page_reference_added = True

            pages.append({"type": "image", "data": page})
    return pages


def create_page_grid_coords(columns, rows):
    """Create a grid of page coordinates in a 2D array.

    Example:
        When asked for a grid for a 3x2 page grid, the result is:
        grid = [
         ["A1", "A2", "A3"],
         ["B1", "B2", "B3"]
        ]
        grid[0][0] = "A1"
        grid[0][1] = "A2"
        grid[2][1] = "C2"

    Args:
        columns: Number of page columns (int).
        rows: Number of page rows (int).

    Returns:
        A 2D list containing page grid references as strings (list).
    """
    LETTERS = string.ascii_uppercase
    page_grid_coords = [[""] * columns for i in range(rows)]
    for row in range(0, rows):
        for column in range(0, columns):
            page_grid_coords[row][column] = "{}{}".format(LETTERS[row], column + 1)
    return page_grid_coords


def grid_reference_page(page_grid_coords, image_name):
    """Create page grid reference HTML.

    Args:
        page_grid_coords: A 2D list containing the page grid as strings (list).
        image_name: The name of the image used in this resource (str).

    Returns:
        HTML string for the grid reference page.
    """
    doc, tag, text, line = Doc().ttl()
    line("style", "#grid-table td {border:1px solid black;padding:1rem 0.5rem;}")
    with tag("h1"):
        text("Pixel Painter")
    with tag("h2"):
        text("Page grid reference for {} image".format(image_name))
    with tag("p"):
        text(
            "Once pixels on each page are filled in correctly, ",
            "cut each grid out and arrange in the following layout ",
            "(page names are in the top right corner)."
        )
    with tag("table", id="grid-table"):
        with tag("tbody"):
            for row_num in range(0, len(page_grid_coords)):
                with tag("tr"):
                    for column_num in range(0, len(page_grid_coords[row_num])):
                        line("td", page_grid_coords[row_num][column_num])
    return doc.getvalue()


def subtitle(request, resource):
    """Return the subtitle string of the resource.

    Used after the resource name in the filename, and
    also on the resource image.

    Args:
        request: HTTP request object (HttpRequest).
        resource: Object of resource data (Resource).

    Returns:
        text for subtitle (str).
    """
    return ""


def valid_options():
    """Provide dictionary of all valid parameters.

    This excludes the header text parameter.

    Returns:
        All valid options (dict).
    """
    return {
        "method": ["junior-binary"],
        "image": ["boat", "fish", "hot-air-balloon"],
        "paper_size": ["a4", "letter"],
    }
