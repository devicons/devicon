import re
from build_assets import arg_getters, api_handler

def main():
	args = arg_getters.get_in_develop_labeler_args()
	try:
		# find the issue closing line
		issue_line = [line for line in args.body.split("\n") if line.startswith("**This PR closes")][0]

		issue_pattern = re.compile(r"\d+")
		issues_numbers = issue_pattern.findall(issue_line)
		api_handler.label_issues(args.token, issues_numbers, ["in-develop"])
	except IndexError:  # if can't find the issue line
		raise Exception("The PR body doesn't contain `**This PR closes` keywords")

if __name__ == "__main__":
	main()
