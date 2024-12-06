Single DLD             |  Parallelized DLD
:-------------------------:|:-------------------------:
<img src="./assets/img/demo_002_layout_overlay.png" alt="Image" style="width:100%;"/>  |  <img src="./assets/img/demo_001_layout_overlay.png" alt="Image" style="width:100%;"/>

# mnFlow
Micro-nanoflow (`mnFlow`) library is aimed at providing the community with tools for design and modeling of micro-nanofluidic chips.
The current focus of the project is on [Deterministic Lateral Displacement (DLD)](https://www.science.org/doi/10.1126/science.1094567) structures.
In particular, the DLD design automation (DDA) tool aims at automating the entire process of design and production of computer-aided design (CAD) files for DLD-based micro-nanofluidic chips.
The produced CAD files can be used for computational modeling, optimization, and manufacturing of DLD devices.

## Usage
### Installation

To use `mnFlow`, first install it using ``pip`` (preferably in a virtual environment using [venv](https://docs.python.org/3/library/venv.html#creating-virtual-environments)):

```console
python -m pip install mnflow
```

### Getting Started
Let us design a DLD structure with critical diameter of ``d_c=10.0`` (microns) and periodicity of ``Np=10``.
The channel is vertical by default.
In this example, we pass ``rot_last=90`` to apply a 90-degree rotation to form a horizontal channel (for better arrangement in this document).
Finally, we pass ``opt_save_image=True`` to save an image of the layout.
Here, is the final script: 

```Python
from mnflow.mfda.cad.dld.theme.block import DLD
dld = DLD(
    d_c=10.0,
    Np=10,
    rot_last=90,
    opt_save_image=True,
)
```

__Output:__
```
----------------------------------------
core.DLD___Np:10_Nw:8_gap_w:21.571_pitch_w:43.142_gap_a:21.571_pitch_a:43.142_height:86.284_boundary_treatment:pow_3
block.DLD___num_unit:9_opt_mirror:False_array_counts:[1, 1]_opt_mirror_before_array:[False, False]
----------------------------------------
{'Np': 10,
 'Nw': 8,
 'area': 1781004.4974180001,
 'bb': [(-3861.227, -113.554), (21.571, 345.137)],
 'count of 1D arrays of core.DLD': 1,
 'd_c': 9.999999999999998,
 'lx': 3882.798,
 'ly': 458.69100000000003,
 'performance': {'Flow rate @ 1 bar/area (micro-liter/min/mm-sq)': 715.9902222759154,
                 'die area (mm-sq)': 1.7810044974180002,
                 'gap over crit. dia.': 2.1571083717157262,
                 'volumetric flow rate at 1 bar (micro-liter/min)': 1275.1818059807188},
 'resistance (Pa.sec/m^3)': 4705211423076.657,
 'volumetric flow rate at 1 bar (m^3/sec)': 2.1253030099678647e-08,
 'volumetric flow rate at 1 bar (milli-liter/hr)': 76.51090835884312}
```

__Output layout:__
<img src="./assets/img/quick_start_layout_overlay.png" alt="Image" style="width:100%;"/>

At this point, you should have a few files created in your working directory automatically: layout files in `gds` and `png` formats. 

If that is the case, and if the layout is similar to the output layout presented above, and if the log you see after executing the script matches that shown above, the package should have been installed properly.

## How to contribute code

Follow these steps to submit your code contribution.

### Step 1. Open an issue

Before making any changes, we recommend opening an issue (if one doesn't already exist) and discussing your proposed changes. This way, we can give you feedback and validate the proposed changes.

### Step 2. Make code changes

To make code changes, you need to fork the repository.

### Step 3. Create a pull request
Once the change is ready, open a pull request from your branch in your fork to the `dev` branch of this repository.

### Step 4. Review
Work with reviewers to apply any changes that may be necessary.

### Step 5. Merge
Once the change is approved, we will merge the changes into the repository.

## Acknowledgments

This project utilizes the packages mentioned in the following.
We gratefully acknowledge their contributions to this project.

- [``klayout``](https://github.com/KLayout/klayout): For creating CAD layouts.
- [``numpy``](https://github.com/numpy/numpy): For numerical computations.
- [``pillow``](https://github.com/python-pillow/Pillow): For creating image of layouts.
- [``scipy``](https://github.com/scipy/scipy): For solving equations.
- [``matplotlib``](https://github.com/matplotlib/matplotlib): For data visualization
- [``black``](https://github.com/psf/black), [``flake8``](https://github.com/PyCQA/flake8), and [``isort``](https://github.com/PyCQA/isort): For linting and formatting codes.
- [``git``](https://github.com/git/git) and [``pre-commit``](https://github.com/pre-commit/pre-commit): For revision control and pre-commit hooks, respectively.
- [``sphinx``](https://github.com/sphinx-doc/sphinx), and [``sphinx-rtd-theme``](https://github.com/readthedocs/sphinx_rtd_theme): For creating docs.
- [``pytest``](https://github.com/pytest-dev/pytest), and [``pytest-cov``](https://github.com/pytest-dev/pytest-cov): For creating test cases.

