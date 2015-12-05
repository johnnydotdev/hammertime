import markdown, gfm, os
from .. import mcq_hammertime

cur_dir = os.path.dirname(__file__)
output_dir = os.path.join(cur_dir, "output")

with open(os.path.join(cur_dir, "Synchronization,-Part-1:-Mutex-Locks.md"), "r") as f:
    string = f.read()
    mcq = mcq_hammertime.MCExtension()
    html = markdown.markdown(string, extensions=['gfm', mcq])
    with open(os.path.join(output_dir, "synchronization-converted.html"), "w") as f_target:
        with open(os.path.join(cur_dir, "head.html"), "r") as head:
            f_target.write(head.read())
        f_target.write(html)
        with open(os.path.join(cur_dir,"tail.html"), "r") as tail:
            f_target.write(tail.read())
