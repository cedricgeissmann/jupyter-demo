#! /usr/bin/env bash

# Look for venv and activate if one is present

if [[ -e venv ]]; then
    source venv/bin/activate
    echo "venv is activated."
    cat << EOF
The requirements.txt might not be up to date. To be save, run 'pip install
-r requirements.txt'
EOF
elif [[ -e requirements.txt ]]; then
    python3 -m virtualenv venv &&
        source venv/bin/activate &&
        pip install -r requirements.txt
else
    echo "No venv or requirements.txt found."
fi

# Create a new tmux session
session_name=$(basename $(pwd))
tmux new-session -d -s ${session_name}
tmux split-window -d jupyter notebook
tmux attach -t ${session_name}
