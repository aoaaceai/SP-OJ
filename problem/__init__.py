from dataclasses import dataclass
# Problems should be stored in the following structure:
# - config.json
#   - name
#   - weight
#   - imageName
# - description.md

# Test cases, grading criteria, etc. are defined by the
# docker image, not the OJ.

# This Problem class only does the following jobs:
# - Provide data for the frontend to render



@dataclass
class Problem:
    id: int
    name: str
    weight: int
    imageName: str
    description: str