def save_to_file(filename, jobs):
    file = open(f"{filename}.csv", "w")
    file.write("Link, Company, Location, Position\n")

    for job in jobs:
        file.write(
            f"{job['link']}, {job['company']}, {job['location']}, {job['position']}\n")

    file.close()
