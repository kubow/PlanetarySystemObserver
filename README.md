# PlanetarySystemObserver

Layout for observing planetary system object positions using [JPL Horizon](https://en.wikipedia.org/wiki/JPL_Horizons_On-Line_Ephemeris_System) data.

## prerequisities

- python3
- python jupyter notebook package

The rest is covered in jupyter notebooks.

```
git clone https://github.com/kubow/PlanetarySystemObserver
cd PlanetarySystemObserver
# variants
# 1.
jupyter notebook
# 2.
streamlit

```

## source data

Visit [discussion on astronomy stack exchange](https://astronomy.stackexchange.com/questions/13488/where-can-i-find-the-positions-of-the-planets-stars-moons-artificial-satellit) to have broader overview of possible sources of space objects data positions.

This layout computes position of space objects using SPK files (SPICE Kernel) that matches closely to JPL HORIZON. Source files are generally available on [NASA Planetary Data System archive](https://naif.jpl.nasa.gov/pub/naif/generic_kernels/spk/).
