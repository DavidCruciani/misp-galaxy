from api import TidalAPI
import json

VERSION = 1
GALAXY_PATH = "../../galaxies/"
CLUSTER_PATH = "../../clusters/"
GALAXY_UUID = "41c3e5c0-de5c-4edb-b48b-48cd8e7519e6"

def create_galaxy():
    galaxy = {}
    galaxy["description"] = "Tidal Threat Group Galaxy"
    galaxy["name"] = "Tidal Threat Group"
    galaxy["namespace"] = "tidal"
    galaxy["type"] = "threat-group"
    galaxy["uuid"] = GALAXY_UUID
    galaxy["version"] = VERSION
    return galaxy


def create_cluster(galaxy, data):
    cluster = {}
    values = []

    for group in data["data"]:
        value = {}
        relations = []
        # TODO check for id and associated_group_id and add to relations
        for entry in group["associated_groups"]:
            relation = {}
            relation["dest-uuid"] = entry["id"]
            relation["type"] = "related-to"
            relations.append(relation)

        value["description"] = group["description"]

        value["meta"] = {}
        value["meta"]["source"] = group["source"]
        value["meta"]["group-attack-id"] = group["group_attack_id"]
        value["meta"]["country"] = [country["country_code"] for country in group["country"]]
        value["meta"]["observed_country"] = [country["country_code"] for country in group["observed_country"]]
        value["meta"]["motive"] = [motive["name"] for motive in group["observed_motivation"]]
        value["meta"]["target-category"] = [sector["name"] for sector in group["observed_sector"]]
        value["meta"]["tags"] = group["tags"]
        value["meta"]["owner"] = group["owner_name"]

        value["related"] = relations
        value["uuid"] = group["id"]
        value["value"] = group["name"]
        values.append(value)

    cluster["authors"] = ["Tidal"]
    cluster["category"] = "Threat Group"
    cluster["description"] = "Tidal Threat Groups"
    cluster["name"] = "Tidal Threat Group"
    cluster["source"] = "https://app-api.tidalcyber.com/api/v1/groups"
    cluster["type"] = "threat-group"
    cluster["uuid"] = galaxy["uuid"]
    cluster["values"] = values
    return cluster


if __name__ == "__main__":

    api = TidalAPI()
    data = api.get_data("groups")
    galaxy = create_galaxy()
    cluster = create_cluster(galaxy, data)

    with open(GALAXY_PATH + "tidal-threat-group.json", "w") as galaxy_file:
        json.dump(galaxy, galaxy_file, indent=4)

    with open(CLUSTER_PATH + "tidal-threat-group.json", "w") as cluster_file:
        json.dump(cluster, cluster_file, indent=4)