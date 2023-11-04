# PlanetarySystemObserver

Layout for observing planetary system object positions using various [[sources]] data.

The second part is about representation these positions as [[zodiac|zodiacal position]].

## How to use

- ensure you have [python3](https://www.python.org/downloads/) installed
- clone the workspace

```shell
git clone https://github.com/kubow/PlanetarySystemObserver
cd PlanetarySystemObserver
```

- preferably use a virtual environment

```shell
python -m venv venv  # init directory
source venv/bin/activate  # activate environment
```

- install requirements and run variants

```shell
pip install -r requirements.txt  # install dependencies
# basic run (command line experience)
python main.py
# alternatives
jupyter notebook  # duplicated code with description
streamlit run your_script.py  # web application
python -m streamlit run your_script.py
```
