import pytesseract
from pytesseract import Output
import cv2

# Tesseract configuration
myconfig = r"--psm 11 --oem 3"

def classify_region(width, height):
    """
    Classifies the region type based on its width and height.
    Adjust thresholds as needed for specific history card layouts.
    """
    if height > 50:  # Likely a heading
        return "heading"
    elif width > 300:  # Likely a table
        return "table"
    else:  # Likely a paragraph
        return "paragraph"

def segment_text_regions(img):
    """
    Segments text regions and classifies them into headings, tables, or paragraphs.
    """
    data = pytesseract.image_to_data(img, config=myconfig, output_type=Output.DICT)
    height, width, _ = img.shape
    text_regions = []

    amount_boxes = len(data['text'])
    for i in range(amount_boxes):
        # Filter by confidence score
        if float(data['conf'][i]) > 75:
            x, y, w, h = data['left'][i], data['top'][i], data['width'][i], data['height'][i]
            cropped_image = img[y:y+h, x:x+w]
            region_type = classify_region(w, h)
            
            # Append region details to the list
            text_regions.append({
                "region_type": region_type,
                "coordinates": (x, y, x+w, y+h),
                "cropped_image": cropped_image,
                "text": data['text'][i]
            })

            # Draw bounding box on the image
            color = (0, 255, 0) if region_type == "heading" else (255, 0, 0) if region_type == "table" else (0, 0, 255)
            cv2.rectangle(img, (x, y), (x+w, y+h), color, 2)
            cv2.putText(img, region_type, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1, cv2.LINE_AA)

    return img, text_regions

def main():
    # Load the image
    img = cv2.imread("example.jpg")

    # Segment and classify text regions
    annotated_img, text_regions = segment_text_regions(img)

    # Save and display results
    for i, region in enumerate(text_regions):
        region_img_path = f"region_{i}.png"
        cv2.imwrite(region_img_path, region["cropped_image"])
        print(f"Region {i}:")
        print(f"  Type: {region['region_type']}")
        print(f"  Coordinates: {region['coordinates']}")
        print(f"  Text: {region['text']}")
        print(f"  Cropped image saved to: {region_img_path}\n")

    # Display annotated image with regions
    cv2.imshow("Annotated Image", annotated_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
