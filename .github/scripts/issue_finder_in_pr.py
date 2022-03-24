import re
from build_assets import arg_getters, filehandler

if __name__ == "__main__":
	args = arg_getters.get_issue_finder_in_pr()
	try:
		# find the issue closing line
		issue_line = [line for line in args.body.split("\n") if line.startswith("**This PR closes")][0]

		print("Issue Line is " + issue_line)
		issue_pattern = re.compile(r"\d+")
		issues_numbers = issue_pattern.findall(issue_line)
		print("Labelling issues: " + str(issues_numbers))

		filehandler.write_to_file("issue_nums.txt", " ".join(issues_numbers) if len(issues_numbers) > 0 else "NONE")
	except IndexError:  # if can't find the issue line
		print("The PR body doesn't contain `**This PR closes` keywords. Ending workflow.") 
		filehandler.write_to_file("issue_nums.txt", "NONE")  
