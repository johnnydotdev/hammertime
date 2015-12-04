import markdown
import gfm
import mc_extension

with open("Synchronization,-Part-1:-Mutex-Locks.md", "r") as f:
    string = f.read()
    html = markdown.markdown(string, extensions=['gfm', 'mc_extension'])
    with open("sync.html", "w") as f_target:
        with open("head.html", "r") as head:
            f_target.write(head.read())
        f_target.write(html)
        with open("tail.html", "r") as tail:
            f_target.write(tail.read())
