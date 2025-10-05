import csv
import json
import pandas as pd

data = [
    ["student_id", "major", "GPA", "is_cs_major", "credits_taken"],
    [1, "Biology", 3.8, "No", "14.0"],
    [2, "Computer Science", 2.0, "Yes", "15.0"],
    [3, "Math", 3.5, "No", "13.0"],
    [4, "Computer Science", 3.2, "Yes", "14.0"],
    [5, "Public Health", 3.9, "No", "16.0"]
]

with open("raw_survey_data.csv", "w", newline='') as file:
    writer = csv.writer(file)
    writer.writerows(data)

course_dicts = [
  {
    "course_id": "DS2002",
    "section": "001",
    "title": "Data Science Systems",
    "level": 200,
    "instructors": [
      {"name": "Austin Rivera", "role": "Primary"}, 
      {"name": "Heywood Williams-Tracy", "role": "TA"} 
    ]
  },
  {
    "course_id": "BIOL3401",
    "title": "Anatomy and Physiology I",
    "level": 300,
    "instructors": [
      {"name": "Ann Massey", "role": "Primary"}
    ]
  },
  {
    "course_id": "DS3001",
    "title": "Foundations of Machine Learning",
    "level": 300,
    "instructors": [
      {"name": "Lei Li", "role": "Primary"},
       {"name": "Eva Winston", "role": "TA"} 
    ]
  },]

with open("raw_course_catalog.json", "w") as json_file:
    json.dump(course_dicts, json_file, indent=4)

df = pd.read_csv("raw_survey_data.csv")
df["is_cs_major"] = df["is_cs_major"].replace({
    "Yes": True, 
    "No": False
    })

#kept getting future warning so this is to avoid that
df = df.infer_objects(copy=False)

df = df.astype({
  "credits_taken": "float64",
  "GPA": "float64"
})

df.to_csv("clean_survey_data.csv", index=False)

with open("raw_course_catalog.json", "r") as json_file:
    course_catalog = json.load(json_file)

course_norm = pd.json_normalize(
    data=course_catalog, record_path=['instructors'], 
    meta=['course_id', 'title', 'level'])

course_norm.to_csv("clean_course_catalog.csv", index=False)


clean_df = pd.read_csv("clean_survey_data.csv")
#print(clean_df.head()) #used this in my other DS class 
