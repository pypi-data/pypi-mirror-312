run_id="khaki_jelly_s70lr4lk7b"
workspace_config_path="config.json"

# Default directory where logs are saved
logs_dir="user_logs"

uv tool install --python "<3.13" --prerelease=allow --with pip azure-cli
uvx az extension remove --name ml
uvx az extension add --name ml

config_query='{resource_group: .resource_group, workspace_name: .name, subscription_id: (.id | split("/")[2])}'
uvx az ml workspace show | uvx jq --raw-output $config_query > $workspace_config_path
cat $workspace_config_path

# We need to specify the Python version because uv's resolver ignores upper
# bounds for Python version in pyproject.toml
# https://docs.astral.sh/uv/reference/resolver-internals/#requires-python
# and azureml.core._metrics breaks for Python >= 3.13
uvx --python "<3.13" --from azure-tools \
    aml download \
        --config $workspace_config_path \
        --run-id $run_id \
        --source-aml-path $logs_dir \
        --convert-logs

uvx --from toolong tl $run_id/$logs_dir/*.log
