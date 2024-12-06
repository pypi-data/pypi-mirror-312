import urllib.parse

import httpx
import pytest

from stac_generator.base.generator import CollectionGenerator
from stac_generator.base.schema import StacCollectionConfig
from stac_generator.base.utils import read_source_config
from stac_generator.csv.generator import CsvGenerator
from stac_generator.csv.schema import CsvConfig
from tests import REMOTE_FIXTURE_URL

REMOTE_CONFIG_JSON = urllib.parse.urljoin(
    str(REMOTE_FIXTURE_URL), "Adelaide/point/point_data_config.json"
)

REMOTE_CONFIG_CSV = urllib.parse.urljoin(
    str(REMOTE_FIXTURE_URL), "Adelaide/point/point_data_config.csv"
)

REMOTE_GENERATED_DIR = urllib.parse.urljoin(
    str(REMOTE_FIXTURE_URL), "Adelaide/point/stac_generated/"
)


JSON_CONFIGS = read_source_config(REMOTE_CONFIG_JSON)
CSV_CONFIGS = read_source_config(REMOTE_CONFIG_CSV)


@pytest.fixture(scope="module")
def json_csv_generator() -> CsvGenerator:
    return CsvGenerator(JSON_CONFIGS)


@pytest.fixture(scope="module")
def csv_generator() -> CsvGenerator:
    return CsvGenerator(CSV_CONFIGS)


@pytest.fixture(scope="module")
def collection_generator(csv_generator: CsvGenerator) -> CollectionGenerator:
    return CollectionGenerator(
        StacCollectionConfig(id="point_data", datetime=None, gsd=None), generators=[csv_generator]
    )


@pytest.mark.parametrize("item_idx", range(len(JSON_CONFIGS)))
def test_generator_given_item_expects_matched_generated_item(
    item_idx: int, json_csv_generator: CsvGenerator
) -> None:
    config = JSON_CONFIGS[item_idx]
    expected_path = urllib.parse.urljoin(config["location"], f"stac_generated/{config['id']}.json")
    data = httpx.get(expected_path)
    expected = data.json()
    actual = json_csv_generator.create_item_from_config(CsvConfig(**config)).to_dict()
    assert expected["id"] == actual["id"]
    assert expected["bbox"] == actual["bbox"]
    assert expected["properties"] == actual["properties"]
    assert expected["assets"] == actual["assets"]
    assert expected["geometry"] == actual["geometry"]


@pytest.mark.parametrize("item_idx", range(len(CSV_CONFIGS)))
def test_generator_given_item_expects_matched_generated_item_csv_config_version(
    item_idx: int, csv_generator: CsvGenerator
) -> None:
    config = JSON_CONFIGS[item_idx]
    expected_path = urllib.parse.urljoin(config["location"], f"stac_generated/{config['id']}.json")
    data = httpx.get(expected_path)
    expected = data.json()
    actual = csv_generator.create_item_from_config(CsvConfig(**config)).to_dict()
    assert expected["id"] == actual["id"]
    assert expected["bbox"] == actual["bbox"]
    assert expected["properties"] == actual["properties"]
    assert expected["assets"] == actual["assets"]
    assert expected["geometry"] == actual["geometry"]


def test_collection_generator(collection_generator: CollectionGenerator) -> None:
    actual = collection_generator.create_collection().to_dict()
    expected_path = urllib.parse.urljoin(REMOTE_GENERATED_DIR, "collection.json")
    data = httpx.get(expected_path)
    expected = data.json()
    assert actual["extent"] == expected["extent"]
