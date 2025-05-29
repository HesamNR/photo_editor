import cv2
import numpy as np
import matplotlib.pyplot as plt
import os

history_stack = []
history_log = []

def load_image(path):
    img = cv2.imread(path)
    if img is None:
        raise FileNotFoundError("Image not found.")
    history_stack.clear()
    history_log.clear()
    history_stack.append(img.copy())
    return img

def show_preview(original, modified, title="Preview"):
    fig, ax = plt.subplots(1, 2, figsize=(10, 5))
    ax[0].imshow(cv2.cvtColor(original, cv2.COLOR_BGR2RGB))
    ax[0].set_title("Original")
    ax[0].axis('off')
    ax[1].imshow(cv2.cvtColor(modified, cv2.COLOR_BGR2RGB))
    ax[1].set_title("Modified")
    ax[1].axis('off')
    plt.suptitle(title)
    plt.show()

def adjust_brightness(img, value):
    modified = cv2.convertScaleAbs(img, alpha=1, beta=value)
    history_stack.append(modified.copy())
    history_log.append(f"brightness {value:+}")
    return modified

def adjust_contrast(img, alpha):
    modified = cv2.convertScaleAbs(img, alpha=alpha, beta=0)
    history_stack.append(modified.copy())
    history_log.append(f"contrast x{alpha}")
    return modified

def convert_grayscale(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    modified = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
    history_stack.append(modified.copy())
    history_log.append("converted to grayscale")
    return modified

def add_padding(img, top, bottom, left, right, border_type):
    border_types = {
        'constant': cv2.BORDER_CONSTANT,
        'reflect': cv2.BORDER_REFLECT,
        'replicate': cv2.BORDER_REPLICATE
    }
    modified = cv2.copyMakeBorder(img, top, bottom, left, right, border_types.get(border_type, 0), value=(255,255,255))
    history_stack.append(modified.copy())
    history_log.append(f"padding {top}px T, {bottom}px B, {left}px L, {right}px R ({border_type})")
    return modified

def apply_threshold(img, method):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    t_type = cv2.THRESH_BINARY if method == 'binary' else cv2.THRESH_BINARY_INV
    _, thresh = cv2.threshold(gray, 127, 255, t_type)
    modified = cv2.cvtColor(thresh, cv2.COLOR_GRAY2BGR)
    history_stack.append(modified.copy())
    history_log.append(f"threshold {method}")
    return modified

def blend_with_another(img, path, alpha):
    img2 = cv2.imread(path)
    img2 = cv2.resize(img2, (img.shape[1], img.shape[0]))
    blended = ((1 - alpha) * img + alpha * img2).astype(np.uint8)
    history_stack.append(blended.copy())
    history_log.append(f"blend with {os.path.basename(path)}, alpha={alpha}")
    return blended

def undo():
    if len(history_stack) > 1:
        history_stack.pop()
        history_log.append("undo")
        return history_stack[-1]
    print("Nothing to undo.")
    return history_stack[-1]

def view_history():
    print("\n--- Operation History ---")
    for action in history_log:
        print("-", action)

def run_editor():
    
    while True:
        path = input("Enter path to image: ").strip()
        try:
            img = load_image(path)
            print("\nImage loaded successfully.\n")
            break
        except FileNotFoundError:
            print("Invalid path. Please try again.")
    print("\nImage loaded successfully.\n")

    while True:
        print("\n==== Mini Photo Editor ====")
        print("1. Adjust Brightness")
        print("2. Adjust Contrast")
        print("3. Convert to Grayscale")
        print("4. Add Padding")
        print("5. Apply Thresholding")
        print("6. Blend with Another Image")
        print("7. Undo Last Operation")
        print("8. View History")
        print("9. Save and Exit")

        choice = input("Select an option (1-9): ").strip()

        if choice == '1':
            val = int(input("Brightness value (-100 to 100): "))
            new_img = adjust_brightness(history_stack[-1], val)
        elif choice == '2':
            alpha = float(input("Contrast factor (e.g., 1.5): "))
            new_img = adjust_contrast(history_stack[-1], alpha)
        elif choice == '3':
            new_img = convert_grayscale(history_stack[-1])
        elif choice == '4':
            print("Padding types: constant, reflect, replicate")
            t = int(input("Top padding: "))
            b = int(input("Bottom padding: "))
            l = int(input("Left padding: "))
            r = int(input("Right padding: "))
            btype = input("Border type: ")
            new_img = add_padding(history_stack[-1], t, b, l, r, btype)
        elif choice == '5':
            m = input("Threshold method (binary/inverse): ").strip()
            new_img = apply_threshold(history_stack[-1], m)
        elif choice == '6':
            p2 = input("Path to second image: ")
            a = float(input("Alpha value (0 to 1): "))
            new_img = blend_with_another(history_stack[-1], p2, a)
        elif choice == '7':
            new_img = undo()
        elif choice == '8':
            view_history()
            while input("\nPress 0 to return to the main menu: ").strip() != '0':
                print("Invalid input. Press 0 to return.")
            continue
        elif choice == '9':
            filename = input("Enter filename to save (e.g., result.jpg): ")
            cv2.imwrite(filename, history_stack[-1])
            print(f"Image saved as {filename}")
            break
        else:
            print("Invalid option.")
            continue

        show_preview(img, new_img)
        img = new_img

run_editor()
