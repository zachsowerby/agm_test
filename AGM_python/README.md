# AGM_python
A pared-down version of my AGM work.

## Alignment
The principle by which this corpus is constructed is the separation but alignment of editions of the same work which contain different aspects of that work. One edition has the text of a piece of music, another has the notation, and others have different aspects (metrical information, accent, or anything else you might want to add; potentially an edition with information about which words are functional words so that you can pursue the word boundary question). The alignment of different editions of the same begins with the file "citation.csv." (The file structure only serves as a way to make the relationship between the editions human-readable.) Within each edition, the XML structure is extremely simple, and only aligns to the citation level of the line. Within each line, words are separated by spaces; syllables within a word are separated by the "+" symbol (except in the text itself, as the Greek words can be syllabified systematically using Python); notes within a syllable are separated by the "~" symbol.

## Notation
The music notation represents the symbols as they appear on the page, without translating them into modern music terminology or interpreting the pitch. It's meant to be as reconstruction-agnostic as possible and avoid as much interpretation as possible. "gvn", "gin", and "gcn" represent the groups vocal notation, instrumental notation, and common notation (at the moment only the leimma); the subsequent number identifies a pitch, the number after that the sharpening (0, 1, or 2), the number after that the rhythmic modifier, and then after that numbers which identify the presence or absence of performance markers (arsis, hyphen), e.g.; "gvn:11.1.1.0.0" = Greek vocal notation, note 11, first sharp, rhythmic modifier of 1 (i.e. no modifier), and no arsis or hyphen. For more info see "musical_Unicode_Pitch.csv".

## Proof of Concept
As this is still a work in progress, I don't have the corpus well-optimized; however, the script "melody_accent_discrep.py" is a proof-of-concept for what the corpus should be able to do. My coding experience is only enough to understand that the code I've managed to get working is relatively inefficient, but the principles remain sound. This script aligns the editions of a work and extracts examples of where the melodic contour does not precisely follow the high points as given by the implied accentuation. At the moment, the code can't handle instances of lacunae (which are present in the Hymn to Helios and the Hymn to Nemesis; there are editions of the notation included which are cautiously reconstructed, and which thus do not have gaps). It tracks down the edition you want to examine by URN; the URN input at the moment is not fully optimized, but enough to examine a line in an edition or a sequence of lines within an edition.

## Use
Hope this helps! I'm not sure how useful it will be in its current state, but feel free to plunder or alter this as much as you need to for your own research.