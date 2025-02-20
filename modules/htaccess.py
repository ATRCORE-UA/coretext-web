import os
from flask import redirect

def read_htaccess(directory):
    htaccess_path = os.path.join(directory, '.htaccess')
    if os.path.isfile(htaccess_path):
        with open(htaccess_path, 'r') as f:
            return f.readlines()
    return None

def apply_htaccess_rules(rules, requested_path):
    for rule in rules:
        rule = rule.strip()

        if rule.startswith("Deny from all"):
            return "403 Forbidden", 403

        elif rule.startswith("Redirect"):
            parts = rule.split()
            if len(parts) >= 3:
                old_path = parts[1]
                new_path = parts[2]
                if requested_path.endswith(old_path):
                    return new_path, 301

        elif rule.startswith("Redirecttourl"):
            parts = rule.split()
            if len(parts) >= 2:
                target_url = parts[1]
                return target_url, 301

        elif rule.startswith("ErrorDocument"):
            parts = rule.split()
            if len(parts) >= 3:
                error_code = int(parts[1])
                custom_page = parts[2]
                return custom_page, error_code

        elif rule.startswith("Options -Indexes"):
            return "403 Forbidden - Directory listing is disabled", 403

        elif rule.startswith("ReturnStatus"):
            parts = rule.split()
            if len(parts) >= 2:
                status_code = int(parts[1])
                return "", status_code
    return None

def check_htaccess_in_all_directories(requested_path):
    current_path = requested_path
    while current_path != "/":
        htaccess_rules = read_htaccess(current_path)
        if htaccess_rules:
            rule_result = apply_htaccess_rules(htaccess_rules, requested_path)
            if rule_result:
                return rule_result

        parent_path = os.path.dirname(current_path)
        if parent_path == current_path:
            break
        current_path = parent_path
    return None
