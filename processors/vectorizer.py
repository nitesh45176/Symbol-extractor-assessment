import cv2
import os
import svgwrite


def png_to_svg(image_path, output_path):
    """
    Convert a PNG symbol into an SVG vector.
    """

    # Read image
    image = cv2.imread(image_path)

    # Convert to grayscale
    gray = cv2.cvtColor(
        image,
        cv2.COLOR_BGR2GRAY
    )


    # Convert to binary
    _, threshold = cv2.threshold(
        gray,
        200,
        255,
        cv2.THRESH_BINARY_INV
    )


    # Find contours
    contours, _ = cv2.findContours(
        threshold,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )


    height, width = gray.shape


    # Create SVG canvas
    drawing = svgwrite.Drawing(
        output_path,
        size=(width, height)
    )


    # Convert every contour into SVG path
    for contour in contours:

        if cv2.contourArea(contour) < 5:
            continue


        points = contour.squeeze()


        if len(points.shape) < 2:
            continue


        path_data = []

        # Move to first point
        first = points[0]
        path_data.append(
            f"M {first[0]} {first[1]}"
        )


        # Draw lines to remaining points
        for point in points[1:]:
            x, y = point

            path_data.append(
                f"L {x} {y}"
            )


        # Close shape
        path_data.append("Z")


        drawing.add(
            drawing.path(
                d=" ".join(path_data),
                fill="none",
                stroke="black",
                stroke_width=1
            )
        )


    # Save SVG file
    drawing.save()


def convert_all_to_svg(symbol_paths):
    """
    Convert all extracted PNG symbols to SVG.
    """

    svg_files = []


    for path in symbol_paths:

        filename = os.path.basename(path)
        name = os.path.splitext(filename)[0]


        output = f"vectors/{name}.svg"


        png_to_svg(
            path,
            output
        )


        svg_files.append(output)


    return svg_files