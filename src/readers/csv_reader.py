import csv

class CSVReader:
    def to_pt_array(self, path):
        pts = []
        with open(path) as csvfile:
            for row in csv.reader(csvfile):
                pts.append([float(c) for c in row])
        return pts
