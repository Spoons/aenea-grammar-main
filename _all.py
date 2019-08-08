# _all.py: main rule for DWK's grammar

try:
    from aenea import *
except:
    from dragonfly import *

import keyboard
import words
import programs

release = Key("shift:up, ctrl:up, alt:up")

alternatives = []
alternatives.append(RuleRef(rule=keyboard.KeystrokeRule()))
alternatives.append(RuleRef(rule=words.FormatRule()))
alternatives.append(RuleRef(rule=words.ReFormatRule()))
alternatives.append(RuleRef(rule=words.NopeFormatRule()))
alternatives.append(RuleRef(rule=words.PhraseFormatRule()))
alternatives.append(RuleRef(rule=programs.ProgramsRule()))
root_action = Alternative(alternatives)

sequence = Repetition(root_action, min=1, max=16, name="sequence")

class RepeatRule(CompoundRule):
    # Here we define this rule's spoken-form and special elements.
    spec = "<sequence> [[[and] repeat [that]] <n> times]"
    extras = [
        sequence,  # Sequence of actions defined above.
        IntegerRef("n", 1, 100),  # Times to repeat the sequence.
    ]
    defaults = {
        "n": 1,  # Default repeat count.
    }

    def _process_recognition(self, node, extras):  # @UnusedVariable
        sequence = extras["sequence"]  # A sequence of actions.
        print "repeat rule matched!"
        print sequence
        count = extras["n"]  # An integer repeat count.
        for i in range(count):  # @UnusedVariable
            for action in sequence:
                print action
                action.execute()
            release.execute()

grammar = Grammar("root rule")
grammar.add_rule(RepeatRule())  # Add the top-level rule.
grammar.load()  # Load the grammar.

def unload():
    """Unload function which will be called at unload time."""
    global grammar
    if grammar:
        grammar.unload()
    grammar = None


if __name__ == '__main__':

    class Observer(RecognitionObserver):
        def on_begin(self):
            print("Speech started.")

        def on_recognition(self, words):
            print(" ".join(words))

        def on_failure(self):
            print("Sorry, what was that?")

    engine = get_engine("kaldi",
        model_dir='kaldi_model_zamia',
        auto_add_to_user_lexicon=True)  # set to True to possibly use cloud for pronunciations

    engine.connect()

    observer = Observer()
    observer.register()

    try:
        # Loop forever
        print("Listening...")
        engine.do_recognition()
    except KeyboardInterrupt:
        pass
