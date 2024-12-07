"""
Inadequately test CMap parsing and such.
"""

from playa.cmapdb import parse_tounicode
from playa.font import Type1FontHeaderParser

STREAMDATA = b"""
/CIDInit/ProcSet findresource begin
12 dict begin
begincmap
/CIDSystemInfo<<
/Registry (Adobe)
/Ordering (UCS)
/Supplement 0
>> def
/CMapName/Adobe-Identity-UCS def
/CMapType 2 def
1 begincodespacerange
<00> <FF>
endcodespacerange
1 beginbfrange
<006F> <0072> [<00E7> <00E9> <00E8> <00EA>]
endbfrange
3 beginbfchar
<01> <0078>
<02> <030C>
<03> <0075>
endbfchar
endcmap
CMapName currentdict /CMap defineresource pop
end
end
"""


def test_cmap_parser():
    cmap = parse_tounicode(STREAMDATA)
    assert cmap.cid2unichr == {
        1: "x",
        2: "̌",
        3: "u",
        111: "ç",
        112: "é",
        113: "è",
        114: "ê",
    }


# Basically the sort of stuff we try to find in a Type 1 font
TYPE1DATA = b"""
%!PS-AdobeFont-1.0: MyBogusFont 0.1
/FontName /MyBogusFont def
/Encoding 256 array
0 1 255 {1 index exch /.notdef put} for
dup 48 /zero put
dup 49 /one put
readonly def
"""


def test_t1header_parser():
    parser = Type1FontHeaderParser(TYPE1DATA)
    assert parser.get_encoding() == {
        48: "0",
        49: "1",
    }
