from __future__ import absolute_import
from markdown.blockprocessors import BlockProcessor
from markdown.extensions import Extension
from markdown.util import etree

MCQ_START = "@MCQ\n"
MCQ_END = "@END\n"

class MCProcessor(BlockProcessor):
    """
    Add Processor for BlockParsers
    """
    def test(self, parent, block):
        ret = block.startswith(MCQ_START)
        return ret

    def run(self, parent, blocks):
        raw_block = blocks.pop(0)
        lines = [l.strip() for l in
                 raw_block.rstrip(MCQ_END).lstrip(MCQ_START).split("\n")]

        question_container = etree.SubElement(parent, 'div')
        question_container.set("class", "question-container")

        question = etree.SubElement(question_container, 'div')
        question.set("class", "question")

        question_text = etree.SubElement(question, "h3")
        question_text.text = lines[0]

        choices = etree.SubElement(question, "ol")
        choices.set("type", "A")
        for choice in lines[1:]:
            choice = choice.lstrip("- ")
            choice_elem = etree.SubElement(choices, "li")
            choice_content = etree.SubElement(choice_elem, "a")
            choice_content.set("href", "#")
            choice_content.set("class", "pure-button pure-button-primary")
            choice_content.text = choice
        print lines

class MCExtension(Extension):
    """
    Add Multiple Choice Questions to Markdown.
    """
    def extendMarkdown(self, md, md_globals):
        md.parser.blockprocessors.add('mcq', MCProcessor(md.parser), '_begin')

def makeExtension(**kwargs):
    return MCExtension(**kwargs)
