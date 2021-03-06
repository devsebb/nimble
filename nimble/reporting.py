from io import StringIO
import pandas as pd
import numpy as np

def load_data(input_path):
  with open(input_path, "r") as f:
    metadata = [next(f)]

    str_rep = ""
    max_line_len = 0

    for line in f:
      csv_line = line.split("\t")[1].strip() + "," + line.split("\t")[0] + "\n"
      str_rep += csv_line + "\n"
      curr_line_len = len(csv_line.split(","))

      if(curr_line_len > max_line_len):
        max_line_len = curr_line_len

      metadata.append(line.split("\t")[1:])

  names = [i for i in range(0, max_line_len)]
  return (pd.read_csv(StringIO(str_rep), header=None, names=names), metadata)


def write_data(output_path, out_data, metadata):
  out_data = out_data.drop(0, axis=1)

  with open(output_path, "w") as f:
    metadata = iter(metadata)
    f.write(next(metadata))

    for row in out_data.apply(lambda row: row.values[~pd.isna(row.values)], axis=1):
      line_metadata = "\t".join([elem for elem in next(metadata)])
      
      if len(row) > 0:
        f.write(",".join([reference for reference in row]) + "\t" + line_metadata)


def get_unique_references(data):
  return pd.unique(data[data.columns[1:]].values.ravel('K'))


def min_pct(data, pct):
  if pct == None:
    pct = 0.01

  num_reads_total = data[0].sum()
  references = get_unique_references(data)
  references_to_drop = []

  for reference in references:
    num_reads = data[data.apply(lambda row: reference in row.values, axis=1)][0].sum()

    if (num_reads / num_reads_total < pct):
      references_to_drop.append(reference)

  for reference in references_to_drop:
    data = data.replace(reference, np.nan)

  return data


def min_count(data, count):
  if count == None:
    count = 5

  references = get_unique_references(data)
  references_to_drop = []

  for reference in references:
    num_reads = data[data.apply(lambda row: reference in row.values, axis=1)][0].sum()

    if (num_reads < count):
      references_to_drop.append(reference)

  for reference in references_to_drop:
    data = data.replace(reference, np.nan)

  return data


def min_pct_lineage(data, value):
  if pct == None:
    pct = 0.01

  return ""


def report(method, value, results_path, output_path):
  (data, metadata) = load_data(results_path)

  out_data = None

  if method == "minPct":
    out_data = min_pct(data, value)
  elif method == "minCount":
    out_data = min_count(data, value)
  elif method == "minPctLineage":
    out_data = min_pct_lineage(data, value)
  else:
    print("Incorrect format. Please see 'nimble help'.")

  write_data(output_path, out_data, metadata)