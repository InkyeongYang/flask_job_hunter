import csv


def save_to_file(words, jobs):
    file = open(f"{words}.csv", "w")
    writer = csv.writer(file)
    writer.writerow(["link", "title", "company", "location"])
    for job in jobs:
        writer.writerow(list(job.values()))
    return