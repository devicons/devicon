from build_assets import arg_getters, api_handler

if __name__ == "__main__":
	args = arg_getters.get_in_develop_labeler_args()
	# find the issue closing line
	issues = args.issues
	if issues != "NONE":
		api_handler.label_issues(args.token, issues.split(" "), ["in-develop"])
