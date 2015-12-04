from __future__ import absolute_import
from markdown.blockprocessors import BlockProcessor
from markdown.extensions import Extension
from markdown.util import etree
import re

MCQ_START = "@MCQ\n"
ANS = "@ANS"
HINT = "@HINT"
EXP = "@EXP"
MCQ_END = "@END\n"

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

    def __repr__(self):
        return "Question: {0},\n\
                Choices: {1},\n\
                Answer: {2},\n\
                Hint: {3},\n\
                Explanation: {4}".format(self.question, str(self.choices),
                                         self.answer, self.hint,
                                         self.explanation)

class MCProcessor(BlockProcessor):
    """
    Add Processor for BlockParsers
    """
    def test(self, parent, block):
        ret = block.startswith(MCQ_START)
        return ret

    def construct_mcquestion(self, lines):
        """
        Return a constructed MCQuestion object given the relevant lines.
        """
        # Extracting relevant data for construction of MCQuestion object.
        question    = lines[0]
        choices     = []
        answer      = ""
        hint        = ""
        explanation = ""

        print lines
        for line in lines[1:]:
            if line.endswith(HINT):
                hint = line.rstrip(HINT)
                continue
            elif line.endswith(EXP):
                explanation = line.rstrip(EXP)
                continue
            else:
                # Add to choices whether a designated answer or not.
                stripped = line.lstrip("- ")
                if line.endswith(ANS):
                    stripped = stripped.rstrip(ANS)
                    answer = stripped
                choices.append(stripped)

        # Construct the MCQuestion object.
        return MCQuestion(question=question, choices=choices,
                                 answer=answer, hint=hint, explanation=explanation)

    def question_to_id(self, mc_question):
        mc_question_as_str = str(mc_question)

        # Only alphanumeric characters allowed before processing.
        re.sub(r"\W+", "", mc_question_as_str)
        return mc_question_as_str.replace(" ", "-")

    def construct_mc_js(self, mc_question):
        mc_question_id = self.question_to_id(mc_question)



    def run(self, parent, blocks):
        raw_block = blocks.pop(0)
        lines = [l.strip() for l in
                 raw_block.rstrip(MCQ_END).lstrip(MCQ_START).split("\n")]

        mc_question = self.construct_mcquestion(lines)

        # Construct question container TreeElement.
        question_container = etree.SubElement(parent, "div")
        question_container.set("class", "question-container")

        # Add TreeElement for question content container.
        question = etree.SubElement(question_container, 'div')
        question.set("class", "question")

        question_text = etree.SubElement(question, "h3")
        question_text.text = mc_question.question

        choice_container = etree.SubElement(question, "ol")
        choice_container.set("type", "A")
        for choice in mc_question.choices:
            choice_elem = etree.SubElement(choice_container, "li")
            choice_content = etree.SubElement(choice_elem, "a")
            choice_content.set("href", "#")
            choice_content.set("class", "pure-button")
            choice_content.text = choice

        script = etree.SubElement(parent, "script")

class MCExtension(Extension):
    """
    Add Multiple Choice Questions to Markdown.
    """
    def extendMarkdown(self, md, md_globals):
        md.parser.blockprocessors.add('mcq', MCProcessor(md.parser), '_begin')

def makeExtension(**kwargs):
    return MCExtension(**kwargs)
