# PlanetarySystemObserver

Layout for observing planetary system object positions using various [[sources]] data.

The second part is about representation these positions as [[zodiac|zodiacal position]].

## How to use

- ensure you have [python3](https://www.python.org/downloads/) installed
- clone the workspace
- work in a virtual environment

```shell
python -m venv planetary  # init directory
source planetary/bin/activate  # activate environment
pip install -r requirements.txt  # install dependencies
```

- run the code

```shell
# basic run (command line experience)
python observer
# alternatives
jupyter notebook  # duplicated code with description
streamlit run observer/ui_streamlit.py  # web application
python -m streamlit run observer/ui_streamlit.py
```
