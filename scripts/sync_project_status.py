#!/usr/bin/env python3
"""
Syncs GitHub Project Board column status based on issue labels.

Issues with label 'status:izvan-revizije' → column '⚪ Izvan revizije'
Issues with label 'status:ceka' → column '🟡 Za pregled'
(etc.)

Usage:
    python scripts/sync_project_status.py              # dry run
    python scripts/sync_project_status.py --apply
"""
import json
import subprocess
import sys
import time

if sys.stdout.encoding != "utf-8":
    try: sys.stdout.reconfigure(encoding="utf-8")
    except: pass

OWNER = "dageci"
PROJECT_NUMBER = 3
REPO = "dageci/eracun-fiskalizacija-datumi"

# Map label → project status option name
LABEL_TO_STATUS = {
    "status:ceka": "🟡 Za pregled",
    "status:u-reviziji": "🔵 U reviziji",
    "status:ceka-pu": "⏸️ Čeka PU",
    "status:potvrdeno": "🟢 Potvrđeno",
    "status:trazi-izmjenu": "⚠️ Traži izmjenu",
    "status:izvan-revizije": "⚪ Izvan revizije",
    "status:odbaceno": "❌ Odbačeno",
}


def gh_graphql(query, **variables):
    cmd = ["gh", "api", "graphql", "-f", f"query={query}"]
    for k, v in variables.items():
        # Use -F for integers, -f for strings
        if isinstance(v, int):
            cmd.extend(["-F", f"{k}={v}"])
        else:
            cmd.extend(["-f", f"{k}={v}"])
    result = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")
    if result.returncode != 0:
        print(f"GraphQL error: {result.stderr[:200]}")
        return None
    return json.loads(result.stdout)


def get_project_id_and_field():
    query = """
    query($owner: String!, $number: Int!) {
      user(login: $owner) {
        projectV2(number: $number) {
          id
          field(name: "Status") {
            ... on ProjectV2SingleSelectField {
              id
              options { id name }
            }
          }
        }
      }
    }
    """
    data = gh_graphql(query, owner=OWNER, number=PROJECT_NUMBER)
    if not data: return None, None, {}
    project = data["data"]["user"]["projectV2"]
    project_id = project["id"]
    field_id = project["field"]["id"]
    options = {opt["name"]: opt["id"] for opt in project["field"]["options"]}
    return project_id, field_id, options


def get_project_items(project_id):
    """Get all project items with their issue numbers and current status."""
    items = []
    cursor = None
    while True:
        after = f', after: "{cursor}"' if cursor else ""
        query = f"""
        query($projectId: ID!) {{
          node(id: $projectId) {{
            ... on ProjectV2 {{
              items(first: 100{after}) {{
                pageInfo {{ hasNextPage endCursor }}
                nodes {{
                  id
                  fieldValueByName(name: "Status") {{
                    ... on ProjectV2ItemFieldSingleSelectValue {{
                      name
                      optionId
                    }}
                  }}
                  content {{
                    ... on Issue {{
                      number
                      labels(first: 10) {{
                        nodes {{ name }}
                      }}
                    }}
                  }}
                }}
              }}
            }}
          }}
        }}
        """
        data = gh_graphql(query, projectId=project_id)
        if not data: break
        page = data["data"]["node"]["items"]
        for node in page["nodes"]:
            content = node.get("content")
            if not content or "number" not in content:
                continue
            labels = [l["name"] for l in content.get("labels", {}).get("nodes", [])]
            current_status = None
            fv = node.get("fieldValueByName")
            if fv and "name" in fv:
                current_status = fv["name"]
            items.append({
                "item_id": node["id"],
                "issue_number": content["number"],
                "labels": labels,
                "current_status": current_status,
            })
        if not page["pageInfo"]["hasNextPage"]:
            break
        cursor = page["pageInfo"]["endCursor"]
    return items


def set_item_status(project_id, item_id, field_id, option_id):
    query = """
    mutation($projectId: ID!, $itemId: ID!, $fieldId: ID!, $optionId: String!) {
      updateProjectV2ItemFieldValue(input: {
        projectId: $projectId
        itemId: $itemId
        fieldId: $fieldId
        value: { singleSelectOptionId: $optionId }
      }) {
        projectV2Item { id }
      }
    }
    """
    return gh_graphql(query, projectId=project_id, itemId=item_id, fieldId=field_id, optionId=option_id)


def main():
    apply = "--apply" in sys.argv

    print("Fetching project info...")
    project_id, field_id, options = get_project_id_and_field()
    if not project_id:
        print("Could not fetch project. Check gh auth scope.")
        return

    print(f"Project: {project_id}")
    print(f"Status field: {field_id}")
    print(f"Options: {list(options.keys())}")

    print("\nFetching project items...")
    items = get_project_items(project_id)
    print(f"Found {len(items)} items")

    # Determine what needs to change
    changes = []
    for item in items:
        # Find the status label
        target_status = None
        for label in item["labels"]:
            if label in LABEL_TO_STATUS:
                target_status = LABEL_TO_STATUS[label]
                break

        if not target_status:
            continue

        if item["current_status"] == target_status:
            continue  # already correct

        option_id = options.get(target_status)
        if not option_id:
            print(f"  WARNING: No option for '{target_status}'")
            continue

        changes.append({
            "item_id": item["item_id"],
            "issue": item["issue_number"],
            "from": item["current_status"],
            "to": target_status,
            "option_id": option_id,
        })

    print(f"\n{len(changes)} items need status change:")
    for c in changes[:10]:
        print(f"  #{c['issue']}: {c['from']} -> {c['to']}")
    if len(changes) > 10:
        print(f"  ... and {len(changes) - 10} more")

    if not apply:
        print("\nDRY RUN. Use --apply to execute.")
        return

    print(f"\nApplying {len(changes)} changes...")
    ok = 0
    err = 0
    for i, c in enumerate(changes, 1):
        result = set_item_status(project_id, c["item_id"], field_id, c["option_id"])
        if result and "errors" not in result:
            ok += 1
        else:
            err += 1
            print(f"  ERR #{c['issue']}")
        if i % 20 == 0:
            print(f"  ... {i}/{len(changes)}")
        time.sleep(0.3)

    print(f"\nDone: {ok} OK, {err} errors")


if __name__ == "__main__":
    main()
