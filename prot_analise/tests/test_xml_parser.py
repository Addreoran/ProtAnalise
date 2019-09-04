from prot_analise.scripts.parse_XML import ParseXML


def test_xml_parser():
    parser = ParseXML("./text.xml", typ=True)
    parser.parse_onefile_XMLs(["Q6GZX4"])
    assert parser.kingdoms == {'Viruses': ['Q6GZX4']}
    assert parser.specieses == {'Frog virus 3 (isolate Goorha)': ['Q6GZX4']}
    assert parser.lengths == {'Q6GZX4': 256}


if __name__ == "__main__":
    test_xml_parser()
    print("Everything passed")
