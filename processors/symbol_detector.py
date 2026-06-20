import cv2
import os


def extract_symbols(page_paths):
    """
    Extract individual symbols from PDF page images.
    """

    extracted_files = []

    count = 1

    for page_path in page_paths:

        # Read image
        image = cv2.imread(page_path)

        # Convert to grayscale
        gray = cv2.cvtColor(
            image,
            cv2.COLOR_BGR2GRAY
        )


        # Convert black lines into white objects
        _, threshold = cv2.threshold(
            gray,
            0,
            255,
            cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU
)


        # Connect nearby lines
        kernel = cv2.getStructuringElement(
            cv2.MORPH_RECT,
            (50, 50)
        )

        threshold = cv2.morphologyEx(
            threshold,
            cv2.MORPH_CLOSE,
            kernel
        )
        cv2.imwrite("debug_threshold.png", threshold)

        # Find all contours
        contours, hierarchy = cv2.findContours(
            threshold,
            cv2.RETR_CCOMP,
            cv2.CHAIN_APPROX_SIMPLE
        )
        
        print("Total contours:", len(contours))

        # Store valid symbol areas
        boxes = []


        for i,contour in enumerate(contours):

            parent = hierarchy[0][i][3]

            # Remove deep nested contours
            if parent > 0:
                continue

            print(
            i,
            "Parent:",
            hierarchy[0][i][3],
            "Child:",
            hierarchy[0][i][2]
        )

            x, y, w, h = cv2.boundingRect(contour)

            area = w * h


            # Remove tiny dots/noise
            height, width = image.shape[:2]

# Ignore very large contour (page border)
            ratio = w / h
            if (
                area > 8000 and
                area < width * height * 0.15 and
                0.3 < ratio < 4
            ):
                boxes.append((x, y, w, h))


        # Sort top to bottom, left to right
        boxes = sorted(
            boxes,
            key=lambda box: (box[1], box[0])
        )
        print("Valid symbols:", len(boxes))


        # Crop each detected symbol
        for x, y, w, h in boxes:

            # Add padding around symbol
            padding = 20

            x1 = max(0, x - padding)
            y1 = max(0, y - padding)

            x2 = x + w + padding
            y2 = y + h + padding


            symbol = image[y1:y2, x1:x2]


            filename = (
                f"symbols/symbol_{count}.png"
            )


            cv2.imwrite(
                filename,
                symbol
            )


            extracted_files.append(
                filename
            )

            count += 1


    return extracted_files