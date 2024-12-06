# SpeedyAnnotate <img src="https://gitlab.developers.cam.ac.uk/maths/cia/covid-19-projects/speedyannotate/-/raw/main/speedy_annotate/assets/qc_logos/1x/white_panel.png" alt="SpeedyAnnotate Logo" width="100" align="right">

*An image viewer and annotation tool for development of machine learning models and image quality assessment (IQA).*

---

SpeedyAnnotate is a straightforward and customisable annotation tool for images. It has three main modes:

1. **[Data Labelling Mode](#data-labelling-mode)**: Annotate images with checkboxes and radiobuttons, with the option of adding bounding boxes.

2. **[Conflict Resolution Mode](#conflict-resolution-mode)**: Resolve conflicts between two annotators by viewing only the images where 
there is a disagreement. Displays the annotations of both annotators and allows you to choose which to keep.

3. **[Image Quality Assessment (IQA)](#image-quality-assessment-iqa)**: Helps you compare and evaluate image quality compared to a reference by 
showing the image to be assessed next to a reference image (i.e. full reference IQA). The criteria for 
assessment are customisable.

The program may be run from the command line or as an executable, which can be downloaded or 
created from the source code (instructions below).

Primarily developed for use on Mac OS X, but also compatible with Linux and Windows.

> :warning: **Warning:** Please note that this application is still in development and there may be unresolved bugs and issues. 
> Use at your own risk!

## Table of Contents

* [Installation](#installation)
* [Usage](#usage)
* [Data Labelling Mode](#data-labelling-mode)
* [Conflict Resolution Mode](#conflict-resolution-mode)
* [Image Quality Assessment (IQA)](#image-quality-assessment-iqa)
* [Customisation](#customisation)
* [YAML Files](#yaml-files)
* [Backup Files](#backup-files)

Installation
------------

It is highly recommended to install `SpeedyAnnotate` in a virtual environment to avoid dependency conflicts with your 
system Python installation.

### Using `venv`

1. Create and activate a virtual environment:
   - **Mac/Linux**:
     ```bash
     python3 -m venv speedy_env
     source speedy_env/bin/activate
     ```
   - **Windows**:
     ```bash
     python -m venv speedy_env
     speedy_env\Scripts\activate
     ```

2. Install the package:
   ```bash
   pip install SpeedyAnnotate
   ```
   
### Using `conda`

1. Create and activate a virtual environment:
     ```bash
     conda create -n speedy_env python==3.10
     conda activate speedy_env
     ``` 
2.	Install the package:
       ```bash
       pip install SpeedyAnnotate
       ```

It is recommended to install the package using Python 3.10 as this was used in development. However, other 
versions of Python 3 should still work.

### Manual Installation

You can also clone the package from GitHub and install it manually. We recommend using `poetry` to manage the 
dependencies:

```bash
git clone https://gitlab.developers.cam.ac.uk/maths/cia/covid-19-projects/speedyannotate
cd speedy_annotate
pip install poetry
poetry install
```

Usage
-----

Run the following command in the command line (in your virtual environment if you created one):

```bash
speedy_annotate
```

Data Labelling Mode
-------------------

Originally developed for image quality control (QC) of machine learning datasets, the application may be
used to quickly check the quality of the images and/or to label them with ground truth. The viewer
supports DICOM, PNG, JPEG and other common image formats. Bounding boxes may be added to demarcate the findings.

<details><summary>Inputs</summary>

##### Checkboxes

Checkboxes are stored as integers:  

| Checkbox Value  |   Meaning   |
|:---------------:|:-----------:|
|        0        | False / No  |
|        1        |  Uncertain  |
|        2        | True / Yes  |

##### Bounding Boxes

- Added to the image by clicking and dragging the mouse.
- Multiple boxes may be added to each image and for each finding.
- The box is labelled with the name of the last checked checkbox.
- Moved by clicking and dragging the box. 
- Deleted by right-clicking on the box and selecting `Remove` from the menu.

##### Radiobuttons

Radiobuttons are stored as integers with the meaning of the integer corresponding to the order of the radiobuttons
inputted in the configuration wizard. For example, if the radiobuttons are `['Normal', 'Abnormal']`, then the values
will be `0` for `Normal` and `1` for `Abnormal`.

</details>

<details><summary>Outputs</summary>

Progress is typically saved as a JSON file, but can be exported to a CSV file within the app.

</details>

<details><summary>Progress</summary>

Your progress through the folder of images is shown in the progress bar at the bottom of the window.

</details>

<details><summary>Keyboard Shortcuts</summary>

|                                                                Key                                                                 |       Action        |
|:----------------------------------------------------------------------------------------------------------------------------------:|:-------------------:|
|                             <kbd>←</kbd>, <kbd>B</kbd>, <kbd>Back</kbd>, <kbd>⌫</kbd>, <kbd>DEL</kbd>                              |   Previous image    |
|                                     <kbd>→</kbd>, <kbd>↵</kbd>, <kbd>N</kbd>, <kbd>Space</kbd>                                     |     Next image      |
| <kbd>⌘</kbd> /<kbd>Ctrl</kbd><kbd>→</kbd>, <kbd>⌘</kbd> /<kbd>Ctrl</kbd><kbd>N</kbd>, <kbd>⌘</kbd>/<kbd>Ctrl</kbd><kbd>Space</kbd> | Next unviewed image |
|                                              <kbd>⌘</kbd>/<kbd>Ctrl</kbd><kbd>F</kbd>                                              |     Go to image     |
|                                                     <kbd>+</kbd>, <kbd>=</kbd>                                                     |       Zoom in       |
|                                                     <kbd>-</kbd>, <kbd>_</kbd>                                                     |      Zoom out       |
|                                                            <kbd>I</kbd>                                                            |  Invert greyscale   |
|                                               <kbd>⌘</kbd>/<kbd>Ctrl</kbd> + Scroll                                                |    Window width     |
|                                                       <kbd>⇧</kbd> + Scroll                                                        |    Window centre    |
|                                                            <kbd>W</kbd>                                                            |   Reset windowing   |
|                                              <kbd>⌘</kbd>/<kbd>Ctrl</kbd><kbd>W</kbd>                                              |   Auto-windowing    |
|                                                            <kbd>R</kbd>                                                            | Rotate images right |
|                                                            <kbd>L</kbd>                                                            | Rotate images left  |
|                                    <kbd>1</kbd>, <kbd>2</kbd>, <kbd>3</kbd>, <kbd>4</kbd>, etc                                     | Select radiobutton  |
|                                                            <kbd>S</kbd>                                                            |        Save         |
|                                              <kbd>⌘</kbd>/<kbd>Ctrl</kbd><kbd>S</kbd>                                              |       Save as       |
|                                              <kbd>⌘</kbd>/<kbd>Ctrl</kbd><kbd>E</kbd>                                              |    Export to CSV    |
|                                              <kbd>⌘</kbd>/<kbd>Ctrl</kbd><kbd>Q</kbd>                                              |        Quit         |
|                                              <kbd>⌘</kbd>/<kbd>Ctrl</kbd><kbd>T</kbd>                                              |     Reset Theme     |


Note: <kbd>⌘</kbd> + Scroll and <kbd>⇧</kbd> + Scroll are only currently available on Mac OS X.

</details>

![Labelling Mode Screenshot](https://gitlab.developers.cam.ac.uk/maths/cia/covid-19-projects/speedyannotate/-/raw/main/speedy_annotate/assets/qc_screenshot.png "Speedy Annotate in Data Labelling Mode")

Conflict Resolution Mode
------------------------

SpeedyAnnotate can be used to resolve conflicts between 2 annotators, who have used the Data Labelling Mode to 
annotate the same images.

> :warning: **Warning:** This mode is only available if the two annotators have used the same configuration settings.
> Any differences in the configuration settings will result in the program crashing.
> 
> To assist, there is the option to export the configuration settings to a `.yml` file, which can be shared with the 
> annotators and loaded when starting a new data labelling project.

> :information_source: **Important Info:**
> 
> - You will only showed the images that exhibit at least one disagreement between the two annotators.
> - You will not be able to modify the annotations of pathology that both annotators agree on.
> - You will see all bounding boxes and notes of both annotators.
> - You cannot draw new bounding boxes or make notes.
> - Radiobuttons are currently ignored completely in conflict resolution.
> - You are unable to export as a .csv, so results can only be saved as a json.

![Conflict Resolution Mode Screenshot](https://gitlab.developers.cam.ac.uk/maths/cia/covid-19-projects/speedyannotate/-/raw/main/speedy_annotate/assets/conflict_screenshot.png "Speedy Annotate in Conflict Resolution Mode")

Image Quality Assessment (IQA)
-------------------------------

Used for full-reference IQA, allowing for comparison images against a reference image.

<details><summary>Selecting the Image Folders and Filename Delimiter</summary>

On loading the app, the setup window will allow you to select the directory
containing the images to be labelled and the directory containing the reference image. 

You must specify the **delimiter** to go from the image name to the reference name. This is how the program matches the two 
images up for comparison. For example, if the image name is `image_1__preprocessed.png` and the reference name is 
`image_1.png`, then the delimiter would be `__` (double underscore). The delimiter is used to find the reference image 
for each image in the folder. If the reference image filenames are the same as the images to be labelled, then the 
delimiter should be left blank.

</details>

<details><summary>Inputs</summary>

The radiobuttons can be selected using the keyboard (i.e. 1, 2, 3, 4) or by clicking on the buttons with the mouse. 
When inputting from the keyboard, the selected radiobutton group is highlighted. When a button is clicked, it 
automatically moves to the next group.

</details>

<details><summary>Outputs</summary>

Progress is typically saved as a JSON file, with radiobutton outputs are stored as integers in the output json file.
However, the results can be exported to a CSV file within the app.

</details>

<details><summary>Progress</summary>

Your progress through the folder of images is shown in the progress bar at the bottom of the window.

</details>

<details><summary>Keyboard Shortcuts</summary>

|                                           Key                                            |       Action        |
|:----------------------------------------------------------------------------------------:|:-------------------:|
|                           <kbd>Enter</kbd> / <kbd>Return</kbd>                           | Next page / unrated |
| <kbd>←</kbd> / <kbd>B</kbd> / <kbd>Delete</kbd> / <kbd>Backspace</kbd> / <kbd>Back</kbd> |   Previous image    |
|                      <kbd>→</kbd> /<kbd>N</kbd> / <kbd>Space</kbd>                       |     Next image      |
|       <kbd>Cmd</kbd>/<kbd>Ctrl</kbd> + <kbd>→</kbd>/<kbd>N</kbd>/<kbd>Space</kbd>        | Next unrated image  |
|                  <kbd>1</kbd>, <kbd>2</kbd>, <kbd>3</kbd>, <kbd>4</kbd>                  | Select radiobutton  |
|                               <kbd>+</kbd> / <kbd>=</kbd>                                |       Zoom in       |
|                               <kbd>-</kbd> / <kbd>_</kbd>                                |      Zoom out       |
|                                       <kbd>R</kbd>                                       | Rotate images right |
|                                       <kbd>L</kbd>                                       | Rotate images left  |
|                                       <kbd>S</kbd>                                       |        Save         |
|                      <kbd>Cmd</kbd>/<kbd>Ctrl</kbd> + <kbd>Q</kbd>                       |        Quit         |

[//]: # (Note: <kbd>Cmd</kbd> + Scroll and <kbd>Shift</kbd> + Scroll are only currently available on Mac OS X.)

</details>

![IQA Mode Screenshot](https://gitlab.developers.cam.ac.uk/maths/cia/covid-19-projects/speedyannotate/-/raw/main/speedy_annotate/assets/iqa_screenshot.png "Speedy Annotate in Quality Assessment Mode")

Customisation
-------------

The program can be customised to suit the user's needs. The following options are available in the advanced 
settings during set-up:
- Change the maximum number of backups
- Backup frequency in minutes
- Change the backup directory
- Change the log directory

YAML Files
----------

These configuration settings are stored in the `config.yml` file in the `speedy_annotate` directory. This
can be edited directly if desired or a new version can be created and loaded when starting a new annotation project.

When starting a new labelling project, the user can choose to load a preset configuration file. This will load the
annotation settings/labelling fields from the file.

> :information_source: **Important Info:**
> 
> In Data Labelling and IQA modes, the config file can be exported from the app and shared with other annotators, 
> who can then load it when they set-up their labelling configuration. This will ensure that all annotators are 
> using the same configuration settings and simplifies the set-up process.
> 
> However, an image directory (Data Labelling mode) or assessment and reference image directories (IQA mode) must be 
> selected before the config is loaded. The paths to the files are NOT included in the config file, which only contains
> the settings for the labelling fields, backup settings, etc.

Backup Files
------------

By default, work is automatically backed up every 5 minutes and the backups are stored in the user's home directory 
(`~`) in the folder `~/speedy_annotate/backups` and up to the latest ten backups are stored. The number of backups, 
the backup interval and the backup directory can be customised in the advanced settings during set-up.
