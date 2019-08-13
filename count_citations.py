import json, argparse, re
import numpy as np
from refextract import extract_references_from_file
from Levenshtein import ratio
from os import listdir
from os.path import isfile, join, splitext


def countCitations(directory, min_distance_ratio):
    file_paths = [join(directory, f) for f in listdir(directory) if isfile(join(directory, f))]
    file_paths = filter(lambda x: x.endswith(".pdf"), file_paths)
    references = []
    for filepath in file_paths:
        print("Extracting references from %s" % filepath)
        json_file_path = splitext(filepath)[0] + ".json"

        if isfile(json_file_path):
            # load json if available
            with open(json_file_path, 'r') as f:
                extracted_refs = json.load(f)["references"]
        else:
            extracted_refs = extract_references_from_file(filepath)
            dict_object = dict(references=extracted_refs)
            try:
                file_object = open(json_file_path, 'w')
                # Save references data into the JSON file
                json.dump(dict_object, file_object)
            except Exception:
                print("Failed to save json file")

        # remove entries without year and author
        extracted_refs = filter(lambda x: 'author' in x and 'year' in x, extracted_refs)
        # remove leading citation number (e.g. [1])
        extracted_refs = map(lambda x: (re.sub("\[\d+\]", "", x['raw_ref'][0]).strip(), x['year'][0]), extracted_refs)
        references += extracted_refs

    print("Calculating distances...")
    distances = createDistanceMatrix(references)

    mask = np.where((distances > min_distance_ratio), distances, 0)
    counts = (mask > 0).sum(axis=1)

    i_indices = np.where(counts > 0)[0]

    result = []
    for i in i_indices:
        count = counts[i] + 1
        title = references[i][0]
        result.append((count, title))

    result.sort(key=lambda x: x[0], reverse=True)

    print("\n==========================")
    print("Number of papers: %i" % len(file_paths))
    print("Total references found: %i\n" % len(references))
    for count, title in result:
        print("Cited by %i papers: %s" % (count, title))


def createDistanceMatrix(references):
    distances = np.zeros((len(references), len(references)))

    for i, (ref_a, year_a) in enumerate(references):
        for j, (ref_b, year_b) in enumerate(references):
            if i == j or distances[j][i] != 0:
                continue
            if year_a != year_b:
                # has to be the same year
                distances[i][j] = 0
            else:
                distances[i][j] = ratio(ref_a, ref_b)
    return distances


def main():
    ap = argparse.ArgumentParser()

    ap.add_argument("-d", "--directory", required=True,
                    help="Directory containing publications in PDF format")
    ap.add_argument("-r", "--ratio", required=False,
                    help="Minimum distance ratio to identify if two references are equal, "
                         "where 1.0 is a full-match and 0.0 is not a match. Default ratio is 0.6",
                    default=0.6)

    args = vars(ap.parse_args())

    directory = args['directory']
    min_distance_ratio = float(args['ratio'])

    countCitations(directory=directory, min_distance_ratio=min_distance_ratio)


if __name__ == '__main__':
    main()
