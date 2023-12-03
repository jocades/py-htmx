#!/bin/bash

# Split the terminal vertically and run browser-sync
tmux split-window -v 'browser-sync "http://localhost:8000" "web/pages" --watch --files .'
n.py
#!/bin/bash

# Split the terminal vertically and run browser-sync
tmux split-window -v 'browser-sync "http://localhost:8000" "web/pages" --watch --files .'

# Split the right pane horizontally and run py main.py
tmux split-window -h 'py main.py'

# Select the layout you prefer (even-horizontal, even-vertical, main-horizontal, main-vertical)
tmux select-layout even-horizontal
# Send the command 'py main.py' to the second pane and run it
tmux send-keys -t 1 'py main.py' C-m

# Select the layout you prefer (even-horizontal, even-vertical, main-horizontal, main-vertical)
tmux select-layout even-horizontal
