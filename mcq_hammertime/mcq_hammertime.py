from __future__ import absolute_import
from markdown.blockprocessors import BlockProcessor
from markdown.extensions import Extension
from markdown.preprocessors import Preprocessor
from markdown.util import etree
import re, cgi

MCQ_START = "@MCQ\n"
ANS = "@ANS"
HINT = "@HINT"
EXP = "@EXP"
MCQ_END = "@END\n"

class HTMLPreprocessor(Preprocessor):
    def run(self, lines):
        return [cgi.escape(l) for l in lines]

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
                    stripped = stripped.rstrip(ANS).strip()
                    answer = stripped
                choices.append(stripped)

        # Construct the MCQuestion object.
        return MCQuestion(question=question, choices=choices,
                          answer=answer, hint=hint, explanation=explanation)

    def question_to_id(self, mc_question):
        mc_question_as_str = str(mc_question).lower()
        mc_question_as_str = mc_question_as_str.replace("\n", "")

        # Only alphanumeric characters allowed before processing.
        return re.sub(r"\W+", "", mc_question_as_str)

    def construct_mc_js(self, mc_question, question_id):
        ret = "var {question_id} = {{question: '{question_text}',choices: ['".format(question_id=question_id, question_text=mc_question.question)
        ret += "', '".join(mc_question.choices) + "'],"
        ret += "answer: '{question_answer}',".format(question_answer=mc_question.answer)
        ret += "hint: '{question_hint}',".format(question_hint=mc_question.hint)
        ret += "explanation: '{question_explanation}'}};".format(question_explanation=mc_question.explanation)

        return ret

    def run(self, parent, blocks):
        raw_block = blocks.pop(0)
        lines = [l.strip() for l in
                 raw_block.rstrip(MCQ_END).lstrip(MCQ_START).split("\n")]

        mc_question = self.construct_mcquestion(lines)
        mc_question_id = self.question_to_id(mc_question)

        # Construct question container TreeElement.
        question_container = etree.SubElement(parent, "div")
        question_container.set("class", "question-container")

        # Add TreeElement for question content container.
        question = etree.SubElement(question_container, 'div')
        question.set("class", "question")

        question_text = etree.SubElement(question, "h3")
        question_text.text = mc_question.question

        hint_button = etree.SubElement(question, "a")
        hint_button.set("href", "#")
        hint_button.set("class", "pure-button hint-button")
        hint_button.set("question_id", mc_question_id)
        hint_button.text = "Display Hint"

        exp_button = etree.SubElement(question, "a")
        exp_button.set("href", "#")
        exp_button.set("class", "pure-button exp-button")
        exp_button.set("question_id", mc_question_id)
        exp_button.text = "Display Explanation"

        choice_container = etree.SubElement(question, "ol")
        choice_container.set("type", "A")
        for choice in mc_question.choices:
            choice_elem = etree.SubElement(choice_container, "li")
            choice_content = etree.SubElement(choice_elem, "a")
            choice_content.set("href", "#")
            choice_content.set("class", "pure-button choice")
            choice_content.set("question_id", mc_question_id);
            choice_content.text = choice

        script = etree.SubElement(parent, "script")
        script.text = self.construct_mc_js(mc_question, mc_question_id)

        hint_elem = etree.SubElement(question, "p")
        hint_elem.set("id", "hint" + mc_question_id)

        exp_elem = etree.SubElement(question, "p")
        exp_elem.set("id", "exp" + mc_question_id)

class MCExtension(Extension):
    """
    Add Multiple Choice Questions to Markdown.
    """
    def extendMarkdown(self, md, md_globals):
        md.preprocessors.add('html_escape', HTMLPreprocessor(md), '_begin')
        md.parser.blockprocessors.add('mcq', MCProcessor(md.parser), '_begin')

def makeExtension(**kwargs):
    return MCExtension(**kwargs)
