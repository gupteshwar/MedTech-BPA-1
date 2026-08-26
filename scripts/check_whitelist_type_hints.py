import ast
import sys


def check_file(filename):
	# filename comes from pre-commit's git-tracked file list or local CLI args, not external input
	with open(filename, encoding="utf-8") as f:  # nosemgrep: frappe-security-file-traversal
		content = f.read()

	try:
		tree = ast.parse(content, filename=filename)
	except SyntaxError:
		return []

	errors = []
	for node in ast.walk(tree):
		if isinstance(node, ast.FunctionDef):
			is_whitelisted = False
			for dec in node.decorator_list:
				if isinstance(dec, ast.Call):
					func = dec.func
				else:
					func = dec

				if isinstance(func, ast.Name) and func.id == "whitelist":
					is_whitelisted = True
				elif isinstance(func, ast.Attribute) and func.attr == "whitelist":
					is_whitelisted = True

			if is_whitelisted:
				for arg in node.args.args:
					if arg.arg in ("self", "cls"):
						continue
					if arg.annotation is None:
						errors.append(
							f"{filename}:{node.lineno}: Whitelisted function '{node.name}' parameter '{arg.arg}' is missing a type hint."
						)
	return errors


if __name__ == "__main__":
	all_errors = []
	for filepath in sys.argv[1:]:
		all_errors.extend(check_file(filepath))

	if all_errors:
		for err in all_errors:
			print(err, file=sys.stderr)
		sys.exit(1)
