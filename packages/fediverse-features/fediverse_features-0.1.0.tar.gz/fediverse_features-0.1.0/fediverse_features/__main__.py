import click

from . import fediverse_features_archive, load_config


@click.command
@click.option("--list", is_flag=True, default=False)
@click.option("--tag")
def features(list, tag):
    if not tag:
        config = load_config()
        tag = config.tag

    with fediverse_features_archive(tag) as archive:
        if list:
            print("Available feature files")
            for filename in archive.namelist():
                if filename.endswith(".feature"):
                    print(filename)
        else:
            for name in config.features:
                archive.extract(name, "features")


if __name__ == "__main__":
    features()
