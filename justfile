uv := `which uv`

export PY_COLORS := "1"
export PYTHONBREAKPOINT := "pdb.set_trace"

uv_run := "uv run --frozen --extra dev"

[private]
default:
    @just help

# Regenerate uv.lock
lock:
    uv lock

# Create a development environment
env: lock
    uv sync --extra dev

# Upgrade uv.lock with the latest dependencies
upgrade:
    uv lock --upgrade

# Show available recipes
help:
    @just --list --unsorted

# Run action on monorepo. For a full list of actions, run `just repo`
repo *args: lock
    {{uv_run}} repository.py {{args}}

# Generate publishing token for Charmhub
generate-token *args:
    charmcraft login \
        --export=.charmhub.secret \
        --charm={{args}}\
        --permission=package-manage-metadata \
        --permission=package-manage-releases \
        --permission=package-manage-revisions \
        --permission=package-view-metadata \
        --permission=package-view-releases \
        --permission=package-view-revisions \
        --ttl=31536000  # 365 days
