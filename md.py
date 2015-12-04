import markdown
import gfm
import mc_extension

with open("Synchronization,-Part-1:-Mutex-Locks.md", "r") as f:
    string = f.read()
    html = markdown.markdown(string, extensions=['gfm', 'mc_extension'])
    with open("sync.html", "w") as f_target:
        f_target.write(html)

