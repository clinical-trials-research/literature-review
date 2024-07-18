from litreview import ClinicalTrials

trials = ClinicalTrials(num_studies=100)
# trials.update_database()
print(trials.query("NCTId", "BriefTitle"))
