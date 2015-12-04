from __future__ import absolute_import
from markdown.blockprocessors import BlockProcessor
from markdown.extensions import Extension
from markdown.util import etree

MCQ_START = "@MCQ"
ANS = "@ANS"
HINT = "@HINT"
EXP = "@EXP"
MCQ_END = "@END"

class MCQuestion(object):
    """
    Class to hold properties of a Multiple Choice Question.
    """
    def __init__(self, question = "Enter question", choices = ["Enter choices"],
                 answer = "Enter answer", hint = "Enter hint",
                 explanation = "Enter explanation"):
        self.question    = question
        self.choices     = choices
        self.answer      = answer
        self.hint        = hint
        self.explanation = explanation

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

        # Extracting relevant data for construction of MCQuestion object.
        question    = lines[0]
        choices     = []
        answer      = ""
        hint        = ""
        explanation = ""

        for line in lines[1:]:
            if line.endswith(ANS):
                answer = line
                choices.append(line)
                continue
            elif line.endswith(HINT):
                hint = line
                continue
            elif line.endswith(EXP):
                explanation = line
                continue
            else:
                choices.append(line)

        # Construct the MCQuestion object.
        mc_question = MCQuestion(question=question, choices=choices,
                                 answer=answer, hint=hint, explanation=explanation)

        question_container = etree.SubElement(parent, 'div')
        question_container.set("class", "question-container")

        question = etree.SubElement(question_container, 'div')
        question.set("class", "question")

        question_text = etree.SubElement(question, "h3")
        question_text.text = mc_question.question

        choice_container = etree.SubElement(question, "ol")
        choice_container.set("type", "A")
        for choice in choices:
            choice = choice.lstrip("- ")
            choice_elem = etree.SubElement(choice_container, "li")
            choice_content = etree.SubElement(choice_elem, "a")
            choice_content.set("href", "#")
            choice_content.set("class", "pure-button")
            choice_content.text = choice

class MCExtension(Extension):
    """
    Add Multiple Choice Questions to Markdown.
    """
    def extendMarkdown(self, md, md_globals):
        md.parser.blockprocessors.add('mcq', MCProcessor(md.parser), '_begin')

def makeExtension(**kwargs):
    return MCExtension(**kwargs)
