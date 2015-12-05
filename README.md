#
A Github Flavored Markdown to HTML converter. With Multiple Choice Question capacity.

### Features
- Convert GFM to HTML
- Interactive Javascript for Multiple Choice Questions
- Extends Python Markdown
- Inline Markdown usable in `@MCQ` blocks

### How To Use
1. Begin your block with `@MCQ`
- Start your first line with the question
- Create a Markdown list, as normal--these will be your answer choices
- Denote the answer in the list by placing `@ANS` at the end of the line
- If you want hints, place these anywhere; just mark the hints as `@HINT`
- If you want explanation, place these anywhere; just mark the explanation as `@EXP`
- End your block with `@END`

### An Example
    @MCQ
    What is the class I am taking?
    - CS *241*
    - CS 374 @ANS
    - CS 210
    - STAT 428
    No Hint 4 u @HINT
    No Explanation 4 u @EXP
    @END

