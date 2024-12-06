
# SOLSTAR : SOLar Simulation of Thermal and Active Radio emissions

**SOLSTAR** (**SOL**ar **S**imulation of **T**hermal and **A**ctive **R**adio emissions) is a simulation tool for simulating solar radio emissions at GHz frequencies. It is designed to simulate spectral image cube at user given frequency range and frequency resolution at any observation date based on extreme ultraviolet observations of the Sun. It is also capable of simulate visibilities for a given radio interferometric array configuration.

---

## 🌟 Features

- **GHz Frequency Simulation**: Simulate solar radio emissions in the GHz range.
- **Visibility simulation**: Simulate visibility of a given radio interferometric array (Not ready yet).
- **Customizable Parameters**: Configure frequency ranges, frequency and temporal resolutions, and spatial resolution. 
- **Data Export**: Export simulation images in FITS and visibilities in CASA measurement format.
- **Modular Architecture**: Integrates seamlessly with other solar physics tools and workflows.

---

## 🚀 Installation

To install and set up **SOLSTAR**, follow these steps:

### Prerequisites
- Python 3.10 or higher
- Git
- Required Python libraries (listed in `requirements.txt`)

### Steps to install from PyPI
   ```bash
   pip install solstar
   ```

### Steps to install from repository

1. Clone the repository:
   ```bash
   git clone https://github.com/devojyoti96/solstar.git
   cd solstar
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
---

## 🛠️ Usage

### Making Spectral Image Cube

1.  To launch the application:
   ```bash
   run_solstar 
   ```
   
2. Preview parameters of the application:
   ```bash
   run_solstar -h
   ```
  
3. It will display the parameters:  

  --obs_date=String     Observation date (yyyy-mm-dd)  
  --obs_time=String     Observation time (hh:mm:ss)  
  --workdir=String      Working directory path  
  --start_freq=Float    Start frequency in MHz  
  --end_freq=Float      End frequency in MHz  
  --freqres=Float       Frequency resolution in MHz  
  --spatial_res=Float   Spatial resolution in arcseconds  
  --observatory=String  Observatory name (MeerKAT, uGMRT, eOVSA, ASKAP, FASR, SKAO-MID)  
  --obs_lat=Float       Observatory latitude in degree  
  --obs_lon=Float       Observatory longitude in degree  
  --obs_alt=Float       Observatory altitude in meter  
  --output_product=String Output product, TB: for brightness temperature map, flux: for flux density map  
  --make_cube=Boolean   Make spectral cube or keep spectral slices seperate
  
4. Run the simulation for a specific observatory (MeerKAT) for producing brightness temperature spectral cube at 0.6 arcsecond resolution:
   ```bash
   run_solstar --obs_date 2023-12-04 --obs_time 06:30:00 --workdir $HOME/simulation_try --start_freq 850 --end_freq 1700 --freqres 10.0 --spatial_res 0.6 --observatory MeerKAT --output_product TB --make_cube True
   ```
5. Access the results in the `$HOME/simulation_try` folder.

### Other examples
1. Run the simulation for a geodetic location (latitude = 30deg, longitude = 20deg, altitude = 100 meter) for producing brightness temperature spectral slices at 5.0 arcsecond resolution:
   ```bash
   run_solstar --obs_date 2023-12-04 --obs_time 06:30:00 --workdir $HOME/simulation_try --start_freq 850 --end_freq 1700 --freqres 10.0 --obs_lat 30.0  --obs_lon 20.0 --obs_alt 100.0 output_product TB --make_cube False
   ```
   
2. Run the simulation for a specific observatory (MeerKAT) for producing flux density spectral cube at 4.0 arcsecond spatial resolution:
   ```bash
   run_solstar --obs_date 2023-12-04 --obs_time 06:30:00 --workdir $HOME/simulation_try --start_freq 850 --end_freq 1700 --freqres 10.0 --spatial_res 4.0 --observatory MeerKAT --output_product flux --make_cube True
   ```
3. Run the simulation for a specific observatory (uGMRT) for producing flux density spectral slices at 5.0 arcsecond spatial resolution:
   ```bash
   run_solstar --obs_date 2023-12-04 --obs_time 06:30:00 --workdir $HOME/simulation_try --start_freq 850 --end_freq 1700 --freqres 10.0 --observatory uGMRT --output_product flux --make_cube False
   ```
---

## Current ongoing and future developments

1. Simulation of visibilties for different array configurations

2. Inclusion of magnetic field model for gyroresonance simulation

3. Simulation of flare times including gyrosynchrotron simulation

---

## 📜 License

This project is licensed under the [MIT License](LICENSE).

---

## 🙌 Acknowledgments

- Developed by the **Devojyoti Kansabanik** and **Surajit Mondal**.
- Inspired by cutting-edge advancements in GHz solar radio spectroscopic imaging and analysis.

---

## 📬 Contact

For questions, feature requests, or support:
- **Email**: dkansabanik@ucar.edu
- **GitHub Issues**: [https://github.com/devojyoti96/solstar/issues](https://github.com/your-repo/STARSIM/issues)

---

**SOLSTAR** is your gateway to understanding solar radio emissions at GHz frequencies. Start exploring today! 🌞

