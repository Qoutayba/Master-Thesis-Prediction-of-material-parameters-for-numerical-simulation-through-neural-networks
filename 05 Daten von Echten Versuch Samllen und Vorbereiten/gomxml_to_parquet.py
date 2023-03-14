#!/usr/bin/env python3

"""converter for GOM results (animator xml format) to pandas as parquet"""
from pathlib import Path
from typing import List
import json

from lxml import etree
import click
import pandas as pd

@click.command()
@click.option(
    "--input-files",
    type=click.Path(exists=True, dir_okay=False, file_okay=True),
    default=list(
        set(binout for binout in Path("data/raw/experiments").glob("**/*.xml"))
    ),
    help="Location of the XML files of the experiment results. "
    "Default: All XML files in subfolders of data/raw/experiments",
    multiple=True,
)
@click.option(
    "--output-folder",
    type=click.Path(dir_okay=True, file_okay=False),
    default="data/share/experiments",
    help="Folder Location to store the generated parquet files.",
)
def gomxmls_to_parquet(input_files: List[str], output_folder: str):
    """
    convert multiple experiment results to parquet
    :param input_folders: Location of the XML file of the experiment results.
    :param output_folder: the location to store the genreated parquet and metadata.json files.
    :return:
    """
    for input_folder in input_files:
        gomxml_to_parquet(input_folder, output_folder)


def gomxml_to_parquet(input_file_path: str, output_folder: str):
    """convert a single experiment to parquet"""
    name = Path(input_file_path).stem
    input_metadata_path = Path(input_file_path).parent / "metadata.json"
    metadata_exists = True
    # validate input files exit
    if not Path(input_file_path).exists():
        print(f"No xml found at {input_file_path} - skipping")
        return
    if not Path(input_metadata_path).exists():
        print(f"No metadata found at {input_metadata_path} - skipping")
        metadata_exists = False

    # set output paths
    Path(output_folder).mkdir(exist_ok=True)
    parquet_path = Path(output_folder) / (name + ".parquet")
    parquet_connectivity_path = Path(output_folder) / (name + "_connectivity.parquet")

    metadata_path = Path(output_folder) / (name + ".json")

    # load XML
    with open(input_file_path) as input_file:
        tree = etree.parse(input_file)

    #assume Force-Displacement XML when no triangles are present:
    if (tree.getroot().findall("*//triangle") == []):
        result_blocks = tree.getroot().findall(".//result")
        result_names = [
            result[0][0].tag if len(result[0]) > 0 else None for result in result_blocks
        ]
        results_data = []
        for result_block, result_name in zip(result_blocks, result_names):
            if result_name is not None:
                results_data.append(
                    [
                        {
                            "time": elem.getparent().attrib["rel_time"],
                            result_block[0][0].attrib["unit_name"]: elem[1].attrib["value"], #deviation
                        }
                        for elem in result_block.findall(f".//{result_name}")
                    ]
                )

        for result_data in results_data:
            try:
                df = df.merge(pd.DataFrame(result_data), on=["time"])
            except:
                df = pd.DataFrame(result_data)
        df.set_index("time").to_parquet(parquet_path)

    #assume Fields XML:
    else:
        # gather results into dicts
        result_blocks = tree.getroot().findall(".//result")
        result_names = [
            result[0][0].tag if len(result[0]) > 0 else None for result in result_blocks
        ]
        results_data = []
        for result_block, result_name in zip(result_blocks, result_names):
            if result_name is not None:
                results_data.append(
                    [
                        {
                            "time": elem.getparent().attrib["rel_time"],
                            "ids": elem.attrib["id"],
                            result_name: elem[0].attrib["value"],
                        }
                        for elem in result_block.findall(f".//{result_name}")
                    ]
                )

        # get point positions (for all time steps)
        points = tree.getroot().findall(".//point")
        pints_data = [
            {
                "time": point.getparent().getparent().getparent().attrib["rel_time"],
                "ids": point.attrib["id"],
                "x": point.attrib["x"],
                "y": point.attrib["y"],
                "z": point.attrib["z"],
            }
            for point in points
        ]

        # build dataframe
        df = pd.DataFrame(pints_data)
        for result_data in results_data:
            df = df.merge(pd.DataFrame(result_data), on=["time", "ids"])

        # store connectivity in different file
        triangles = tree.getroot().findall("*//triangle")
        triangles_df = pd.DataFrame(
            [
                {"p1": tri.attrib["p1"], "p2": tri.attrib["p2"], "p3": tri.attrib["p3"]}
                for tri in triangles
            ]
        )

        # store parquets
        df = df.set_index(["ids", "time"])
        df.to_parquet(parquet_path)
        triangles_df.to_parquet(parquet_connectivity_path)

        if (metadata_exists == True):
            # add metadata file (including metadata of inout folder)
            with open(input_metadata_path, encoding="utf-8") as input_metadata_file:
                metadata = (
                    json.load(input_metadata_file) if input_metadata_path.exists() else {}
                )
            ## add metadata of conversion process here?
            # metadata["gomxml_to_parquet"] = ""
            with open(metadata_path, "w", encoding="utf-8") as metadata_file:
                json.dump(metadata, metadata_file)


if __name__ == "__main__":
    gomxmls_to_parquet()  # pylint: disable=no-value-for-parameter
