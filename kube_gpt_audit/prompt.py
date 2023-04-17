def audit_prompt(resource_type: str, resource_yaml: str) -> str:
    return (
        f"You are a Kubernetes expert searching for vulnerabilities in a {resource_type} yaml. Scan the following"
        f" {resource_type} definition and list the vulnerabilities found. You should return the result as a json"
        " containing two columns (vulnerability, severity). The column vulnerability should contain a long text.The"
        " allowed severities are LOW, MEDIUM, HIGH, CRITICAL. don't write anything else besides the"
        f" json\n\n{resource_yaml}\n\nJSON:\n"
    )