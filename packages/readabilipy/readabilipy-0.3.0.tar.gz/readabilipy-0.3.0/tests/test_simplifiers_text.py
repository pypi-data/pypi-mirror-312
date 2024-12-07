from pytest import mark
from checks import check_exact_html_output

from readabilipy.simplifiers import normalise_text, normalise_unicode, normalise_whitespace, strip_control_characters, strip_html_whitespace
from readabilipy.simplifiers import text


def test_unicode_normalisation():
    nfd_form = "Ame\u0301lie"
    nfc_form = "Amélie"
    assert normalise_unicode(nfd_form) == normalise_unicode(nfc_form)


def test_all_whitespace_is_normalised_to_empty_string():
    tab_space_new_line_tab_space = "\t \n\t \f \r\n"
    assert normalise_whitespace(tab_space_new_line_tab_space) == ""


def test_text_normalisation():
    unnormalised_string = "Ame\u0301lie   Poulain"
    assert normalise_text(unnormalised_string) == "Amélie Poulain"


def test_strip_html_whitespace():
    formatted_string = """
    <html>
        <body>
            <p>Some text here</p>
        </body>
    </html>
    """
    assert strip_html_whitespace(formatted_string) == "<html><body><p>Some text here</p></body></html>"


def test_strip_control_characters_non_printing_characters():
    unnormalised_string = "A string with non-printing characters in\u200Bc\u200Bluded\ufeff"
    assert strip_control_characters(unnormalised_string) == "A string with non-printing characters included"
    assert normalise_text(unnormalised_string) == "A string with non-printing characters included"


def test_strip_control_characters_cr():
    unnormalised_string = "A string with new lines\rin\u200Bc\u200Bluded\ufeff"
    assert strip_control_characters(unnormalised_string) == "A string with new lines\rincluded"
    assert normalise_text(unnormalised_string) == "A string with new lines included"


def test_strip_control_characters_lf():
    unnormalised_string = "A string with new lines\ninc\u200Bluded\ufeff"
    assert strip_control_characters(unnormalised_string) == "A string with new lines\nincluded"
    assert normalise_text(unnormalised_string) == "A string with new lines included"


def test_strip_control_characters_cr_lf():
    unnormalised_string = "A string with new lines\r\nin\u200Bc\u200Bluded\ufeff"
    assert strip_control_characters(unnormalised_string) == "A string with new lines\r\nincluded"
    assert normalise_text(unnormalised_string) == "A string with new lines included"


def test_strip_control_characters_ff():
    unnormalised_string = "A string with form feed\fin\u200Bc\u200Bluded\ufeff"
    assert strip_control_characters(unnormalised_string) == "A string with form feed\fincluded"
    assert normalise_text(unnormalised_string) == "A string with form feed included"


def test_strip_control_characters_tab():
    unnormalised_string = "A string with tabs\tin\u200Bc\u200Bluded\ufeff"
    assert strip_control_characters(unnormalised_string) == "A string with tabs\tincluded"
    assert normalise_text(unnormalised_string) == "A string with tabs included"


# Test whitespace around tags
@mark.parametrize('terminal_punctuation', text.terminal_punctuation_marks)
def test_ensure_correct_punctuation_joining(terminal_punctuation):
    """Do not join with ' ' if the following character is a punctuation mark."""
    input_html = f"""
        <div>
            <p>
                Some text <a href="example.com">like this</a>{terminal_punctuation} with punctuation.
            </p>
        </div>"""
    expected_output = f"""<div><p>Some text like this{terminal_punctuation} with punctuation.</p></div>"""
    check_exact_html_output(input_html, expected_output)


@mark.parametrize('matched_pair', text.matched_punctuation_marks)
def test_ensure_correct_bracket_quote_joining(matched_pair):
    """Do not join with ' ' if we are inside matched punctuation marks."""
    input_html = f"""
        <div>
            <p>
                Some text {matched_pair[0]}<a href="example.com">like this</a>{matched_pair[1]} with punctuation.
            </p>
        </div>"""
    expected_output = f"""<div><p>Some text {matched_pair[0]}like this{matched_pair[1]} with punctuation.</p></div>"""
    check_exact_html_output(input_html, expected_output)
