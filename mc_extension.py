from __future__ import absolute_import
from markdown.blockprocessors import BlockProcessor
from markdown.extensions import Extension

MCQ_START = "@MCQ"
MCQ_END = "@END"

class MCProcessor(BlockProcessor):
    """
    Add Processor for BlockParsers
    """
    def test(self, parent, block):
        ret = block.startswith(MCQ_START)
        return ret

    def run(self, parent, blocks):
        raw_block = blocks.pop(0)
        lines = [l.strip().rstrip(MCQ_END).lstrip(MCQ_START) for l in
                 raw_block.split("\n")]
        print lines

class MCExtension(Extension):
    """
    Add Multiple Choice Questions to Markdown.
    """
    def extendMarkdown(self, md, md_globals):
        md.parser.blockprocessors.add('mcq', MCProcessor(md.parser), '_begin')

def makeExtension(**kwargs):
    return MCExtension(**kwargs)
