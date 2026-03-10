elif col == "coordinate":
    escaped = val.replace("\\", "\\\\")
    vals.append(f"E'{escaped}'::bytea")
