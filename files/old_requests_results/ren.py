import os

source = "general-crime"
target = "general_crime"

files = os.listdir("../requests_results")
for file in files:
    os.rename(file, file.replace(source, target))
