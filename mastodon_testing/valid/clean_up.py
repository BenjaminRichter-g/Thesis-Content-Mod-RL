
kept = []

with open("hate_domains.txt", "r") as infile:
    for raw in infile:
        # Remove trailing whitespace so splits don’t carry “\n”
        line = raw.strip()
        parts = line.split(",")
        
        # DEBUG: show exactly what you’ve got
        print("RAW LINE:", repr(raw))
        print("STRIPPED:", repr(line))
        print("SPLIT PARTS:", parts)
        print("LAST PART REPR:", repr(parts[-1]))
        
        # Check for “racism” anywhere in the last field
        if "racism" in parts[-1]:
            domain = parts[0]
            kept.append(domain + "\n")
            print(f" → KEEP: {domain}")
        else:
            print(" → SKIP")

# After reading, show what we kept
print("\nFINAL kept list:", kept)

with open("racism_domains.txt", "w") as outfile:
    outfile.writelines(kept)
    print(f"Wrote {len(kept)} domains to racism_domains.txt")

