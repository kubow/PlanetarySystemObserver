import argparse
# from display import display_radial, display_3d
from pathlib import Path
from sys import argv, exit

"""This is main file to run the application and create basic directory structure
context.py      : contains main positioning logic
settings.py     : translation methods (plain text for now - future db)
test.py         : testing an application
ui_streamlit.py : application web interface 
visual.py       : graphs and charts
"""


def create_dir(location):
    try:
        Path(location).mkdir(parents=True, exist_ok=False)
    except FileExistsError:
        print(f"Folder {location} is already present")
    else:
        print(f"Folder {location} was created")


def download_file(location, file_name=""):
    # https://stackoverflow.com/questions/11768214/python-download-a-file-from-an-ftp-server
    import shutil
    import urllib.request as request
    from contextlib import closing

    bsp_location = f"https://naif.jpl.nasa.gov/pub/naif/generic_kernels/spk/planets/{file_name}"

    with closing(request.urlopen(bsp_location)) as r:
        with open(f"./{location}/{file_name}", "wb") as f:
            shutil.copyfileobj(r, f)
    print(f"SPK file ./{location}/{file_name} downloaded ....")


def get_source_file(location: str = "source", file_name="de430.bsp"):
    if Path(f"./{location}/{file_name}").is_file():
        print(f"SPK file ./{location}/{file_name} exists...")
    else:
        print(
            f"SPK file ./{location}/{file_name} downloading, wait some time please..."
        )
        download_file(location, file_name)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="basic methods available")
    parser.add_argument("-t", help="interactive text mode", type=bool, default=True)
    args = parser.parse_args()
    if args.t:
        # from streamlit import cli as stcli
        try:
            from streamlit.web import cli as stcli

            argv = ["streamlit", "run", "./observer/ui_streamlit.py"]
            exit(stcli.main())
        except ImportError:
            import ui_streamlit as st

            print("What?")
            st.main()
