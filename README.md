# Get Contributor ID List Workflow
This workflow can be used as follows:
```yaml
on:
  workflow_dispatch:
    inputs:
      repo:
        description: "Repo address, like: https://github.com/karmada-io/karmada.git"
        required: true
        type: string
      start:
        description: 'The start tag/commit flag'
        required: true
        type: string
      end:
        description: 'The end tag/commit flag'
        required: true
        type: string
      exclude_contributor:
        description: 'The contributor to ignore, use space to split'
        required: false
        type: string

jobs:
  job_name:
    uses: jwcesign/get-contributors/.github/workflows/get-contributors.yaml@main
    with:
        repo: ${{ github.event.inputs.repo }}
        start: ${{ github.event.inputs.start }}
        end: ${{ github.event.inputs.end }}
        exclude_contributor: ${{ github.event.inputs.exclude_contributor }}
```

After running, the output looks like:
```sh
INFO:root:Start to clone repo:https://github.com/karmada-io/karmada.git
INFO:root:Start to get all commits
INFO:root:Ignore contributor:karmada-bot
INFO:root:Ignore contributor:karmada-bot
INFO:root:Find contributor match:lonelyCZ/@lonelyCZ
INFO:root:Find contributor match:changzhen/@XiShanYongYe-Chang
INFO:root:Find contributor match:RainbowMango/@RainbowMango
INFO:root:------------------------------
INFO:root:Total contributor:3
@lonelyCZ
@RainbowMango
@XiShanYongYe-Chang

INFO:root:------------------------------
```