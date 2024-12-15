# SpaceXMag: An Automatic Space Optimization Tool for Low-Vision Users

SpaceXMag is an automatic, scalable, and rapid optimization framework for smartphone app interfaces. Designed for low-vision users, it reduces unnecessary whitespace, preserves spatial relationships of UI elements, and enhances accessibility features like discernible borders. By compacting whitespace, SpaceXMag enables users to view more information within a magnified viewport, minimizing panning and increasing usability.

---

## Features

### Accessibility Optimizations:
- **Whitespace Reduction:** Automatically compacts whitespace to display more content in magnified views.
- **Preserved Layouts:** Maintains the relative alignment and spatial hierarchy of UI elements.
- **Visual Cues:** Applies borders (e.g., red outlines) to make UI elements easier to locate and interact with.

### Magnification Modes:
- **Fullscreen Mode:** Uniform magnification of the entire screen.
- **Window Mode:** Magnifies only a specific area while preserving contextual surroundings.
- **Fisheye Mode:** Provides non-uniform magnification with customizable lens shapes (e.g., circular, rectangular).

### Scalability and Speed:
- Processes each UI in **~1.44 seconds** on average.
- Tested on a dataset of **25,677 Android app screenshots**, achieving a **47.17% whitespace reduction**.

---

## Results

SpaceXMag significantly improves usability for low-vision users, as demonstrated in a user study with **11 participants**:
- **28.13% time reduction** for overview tasks.
- **42.89% time reduction** for target acquisition tasks.
- Participants rated the optimized UIs as more usable and contextually clear.

---

## Installation

### Requirements
Ensure you have Python installed along with necessary dependencies.

### Steps:
- git clone https://github.com/your-repo/SpaceXMag.git
- cd SpaceXMag
# to Launch fullscreen magnification:
- python fullscreen_mag_user_controlled.py
# to launch window magnification:
- python window_mag_user_controlled.py
# to launch fisheye magnification:
- python fisheye_user_controlled.py
