GEN_CHANGELOG = """#!/bin/sh
        latisse generate
        git add CHANGELOG.md
        git commit -m "chore: Update CHANGELOG.md for new tag"
        """
