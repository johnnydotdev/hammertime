from __future__ import absolute_import
from markdown.blockprocessors import BlockProcessor
from markdown.extensions import Extension

class MCProcessor(BlockProcessor):

    MCQ_START = "@MCQ"
    MCQ_END = "@ENDMCQ"

    def test(self, parent, block):
        print "Testing " + block
        return block.startswith(MCQ_START)

    def run(self, parent, blocks)
        raw_block = blocks.pop(0)
        pass

class MCExtension(Extension):
    """
    Add Multiple Choice Questions to Markdown.
    """

    def extendMarkdown(self, md, md_globals):
        md.parser.blockprocessors.add('mcq', MCProcessor(md.parser))

def makeExtension(**kwargs):
    return MCExtension(**kwargs)
