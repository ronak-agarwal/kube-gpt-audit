# kube-gpt-audit
Audit your Kubernetes cluster via OpenAI

### Pre-requists
1. Kubernetes cluster running and config file exist on your machine
2. You have OpenAI account setup, and you have API Token

`export OPENAI_AUTH_TOKEN=XXXXXX`

### Run CLI

`python3 -m kube_gpt_audit.cli --audit`

### Output

![output](https://github.com/ronak-agarwal/kube-gpt-audit/blob/main/images/output.png)
`

### Future Improvements

- Cover audit all Kuberenetes Resources (currently only support deployments)
- Expand the CLI to also support audit for Terraform (HCL templates) as a separate project