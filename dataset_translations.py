import os
import json
import logging

LOG = logging.getLogger(__name__)
curr = os.path.abspath(os.getcwd())

# path to dataset column name translations
path_to_ds_translations = curr + "/dataset_translations"
# path to superset translation files
path_to_superset_translations = curr + "/superset/translations"

def include_language():
    """
    Includes dataset language to superset language pack
    """
    # get the dataset column translation details
    languages = get_languages()
    for lang in languages:
        superset_trans_file = path_to_superset_translations + "/" + lang["lang"] + "/" + "LC_MESSAGES" + "/messages.json"
        local_trans_file = path_to_ds_translations + "/" + lang["lang"] + ".json"
        # if the translation files exist for the language
        if os.path.exists(superset_trans_file) and os.path.exists(local_trans_file):

            try:
                # get superset translation file for that language
                with open(superset_trans_file, 'r') as file:
                    data = json.load(file)

                # get the dataset column translation file for that language
                with open(local_trans_file, 'r') as file:
                    additional_content = json.load(file)

                # add dataset column translation to superset translation files
                if "superset" in data["locale_data"]:
                    data["locale_data"]["superset"] = data["locale_data"]["superset"] | additional_content


                with open(superset_trans_file, 'w') as file:
                    json.dump(data, file, indent=2)

            except Exception as e:

                LOG.error(e)





def get_languages():
    """
    Returns a dictionary containing a dataset language as key and the path to the language file as value

    :rtype:dict
    """

    languages = []
    if os.path.exists(path_to_ds_translations) and os.path.isdir(path_to_ds_translations):

        for root, dirs, files in os.walk(path_to_ds_translations):

            for file_name in files:

                ext = os.path.splitext(file_name)[1]
                # searching exclusively for JSON files
                if ext not in [".json"]:
                    continue
                file_path = os.path.join(root, file_name)
                lang = file_name.replace(".json", "")
                languages.append(
                    {
                        "lang": lang,
                        "path_to_local": file_path
                    }
                )
    return languages


if __name__ == "__main__":
    include_language()
