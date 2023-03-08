import csv
import subprocess
from os import listdir
from os.path import join
import json

def extract_id(json):
    try:
        return int(json["topic"])
    except KeyError:
        return 0


# folder with all the runs
runsFolder = input("Copy here the full path to the runs folder: ")

# file .qrels
qrelsFile = input("Copy here the full path to the runs qrels file: ")

# trec_eval executable
trecExec = input("Copy here the full path to the TREC eval EXECUTABLE: ")
if(len(trecExec) == 0):
    trecExec = "trec_eval/trec_eval"

trec_res = []

# Save max nDCG and its run
max_ID = None
max_ndcg = 0

# Get runIDs
runIDs = [f[0:-4] for f in listdir(runsFolder) if (
    join(runsFolder, f).endswith(".txt"))]

# Setup JSON object to store rows
csv_json_data = {"runNames": [], "topics": [], "ndcg": {}}

for runID, i in zip(runIDs, range(len(runIDs))):
    runID_name = runID.replace("-", " ").title()
    csv_json_data["runNames"].append(runID_name)

# Calculates runs score
for runID, runName in zip(runIDs, csv_json_data["runNames"]):
    print("RUN #{runID}".format(runID=runID))

    # Get trec_eval evaluation
    runFile = join(runsFolder, runID + ".txt")
    trec_eval = subprocess.run(
        [trecExec, '-q', '-m', 'ndcg_cut.5', qrelsFile, runFile], stdout=subprocess.PIPE).stdout.decode('UTF-8')

    # All ndcg of all topics
    topicsRes = []
    topics = []
    for i in range(len(trec_eval.split("\n")) - 2):
        trec_topic_res = trec_eval.split("\n")[i]
        topicID = int(trec_topic_res.split("\t")[-2])
        topic_ndcg = float(trec_topic_res.split("\t")[-1])

        if topicID in csv_json_data["ndcg"]:
            csv_json_data["ndcg"][topicID].append(topic_ndcg)
        else:
            csv_json_data["ndcg"][topicID] = [topic_ndcg]

        topics.append(topicID)
        topicsRes.append({'topic': topicID, 'ndcg': topic_ndcg})

    # Get average measure of ndcg
    ndcg_tot = float(trec_eval.split("\n")[-2].split("\t")[-1])

    if "All" in csv_json_data["ndcg"]:
        csv_json_data["ndcg"]["All"].append(ndcg_tot)
    else:
        csv_json_data["ndcg"]["All"] = [ndcg_tot]

    # Print average ndcg
    print("\tnDCG: {ndcg}\n".format(ndcg=ndcg_tot))

    if len(csv_json_data["topics"]) <= 0:
        topics.sort()
        topics.append("All")
        csv_json_data["topics"] = topics

    topicsRes.sort(key=extract_id)

    # Update max
    if ndcg_tot >= max_ndcg:
        max_ndcg = ndcg_tot
        max_ID = runFile

    # Save results
    trec_res.append({
        "runID": runID,
        "runName": runName,
        "runFile": runFile,
        "ndcg_avg": ndcg_tot,
        "ndcg_topics": topicsRes
    })

# Get max
print("\nMaximum nDCG@5 is {max_ndcg} of #{runID}".format(
    max_ndcg=max_ndcg,
    runID=max_ID
))

print("\nSaving results...")

# Save results in csv table
with open('trec_eval_results_runs.csv', mode='w', encoding='UTF-8') as trec_eval_res:
    csv_writer = csv.writer(
        trec_eval_res, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

    csv_writer.writerow(["Topic"] + csv_json_data["runNames"])

    for topic in csv_json_data["topics"]:
        csv_writer.writerow([topic] + csv_json_data["ndcg"][topic])

# Save results in JSON file
with open("trec_res.json", mode='w', encoding='UTF-8') as fp:
    json.dump(trec_res, fp, indent=2)

print("\n[FINISHED]")
