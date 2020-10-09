import csv
import xml.etree.ElementTree as ET
from pyCTS import CTS_URN
import os
from greek_accentuation.syllabify import syllabify

class citableNode:
    def __init__(self, urn, text):
        self.urn = urn
        self.text = text

class alignmentModule:
    def __init__(self, urn, normalized, lyric, notation, accent, meter):
        self.urn = urn
        self.normalized = normalized
        self.lyric = lyric
        self.notation = notation
        self.accent = accent
        self.meter = meter

def align(φ):
    cts_urn = CTS_URN(φ)
    work_component = cts_urn.work_component
    passage_component = cts_urn.passage_component
    nodesList = []
    with open(r'../citation.csv', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=",", quotechar='|')
        rows = []
        for row in reader:
            rows.append(row)
        for x in range(len(rows)):
            a = rows[x][0]
            b = a.split(":")[3].split(".")[:-1]
            c = ".".join(b)
            if c == work_component:
                root = ET.parse("../" + rows[x][2]).getroot()
                new_cts_urn = CTS_URN(a + passage_component)
                r = passage_component.split("-")
                w = root[1][0]
                text = []
                if len(r) == 1:
                    text.append(w[int(passage_component) - 1].text)
                if len(r) > 1:
                    for i in range(int(r[0]), int(r[1])+1):
                        text.append(w[i - 1].text)
                node = citableNode(new_cts_urn, text)
                nodesList.append(node)
    for node in nodesList:
        if node.urn.version == 'normalized':
            normalized = node
        if node.urn.version == 'text':
            lyric = node
        if node.urn.version == 'notation':
            notation = node
        if node.urn.version == 'accent':
            accent = node
        if node.urn.version == 'meter':
            meter = node
    module = alignmentModule(cts_urn, normalized, lyric, notation, accent, meter)
    return(module)

def alignedSyllabify(φ):
    norText = []
    lyrText = []
    notText = []
    accText = []
    metText = []
    for i in range(len(φ.normalized.text)):
        for word in φ.normalized.text[i].split(" "):
            norText.append(syllabify(word))
    for i in range(len(φ.lyric.text)):
        for word in φ.lyric.text[i].split(" "):
            lyrText.append(syllabify(word))
    for i in range(len(φ.notation.text)):
        for word in φ.notation.text[i].split(" "):
            notText.append(word.split("+"))
    for i in range (len(φ.accent.text)):
        for word in φ.accent.text[i].split(" "):
            accText.append(word.split("+"))
    for i in range (len(φ.meter.text)):
        for word in φ.meter.text[i].split(" "):
            metText.append(word.split("+"))
    combo = zip(norText, lyrText, notText, accText, metText)
    return(combo)

def notationParser(stringOfNotation):
    unicodeWords = []
    wordNoteClusters = stringOfNotation.split(" ")
    syllableNoteClusters = []
    notes = []
    for wordNoteCluster in wordNoteClusters:
        syllableNoteClusters.append(wordNoteCluster.split("+"))
    for syllableNoteCluster in syllableNoteClusters:
        e = []
        for note in syllableNoteCluster:
            e.append(note.split("~"))
        notes.append(e)
    for word in notes:
        unicodeSyllables = []
        for syllable in word:
            unicodeNotes = []
            for note in syllable:
                α = note.split(".")[0:2]
                β = ".".join(α)
                with open(r'../resources/musical_Unicode_Pitch.csv', newline='', encoding='utf-8') as csvfile:
                    reader = csv.reader(csvfile, delimiter=",", quotechar='|')
                    rows = []
                    for row in reader:
                        rows.append(row)
                    for x in range(len(rows)):
                        a = rows[x][0].split(":")[3:5]
                        b = ":".join(a)
                        if β == b:
                            unicodeNotes.append(chr(int(rows[x][2], 16)))
            if len(unicodeNotes) > 0:
                unicodeSyllables.append(unicodeNotes)
        if len(unicodeSyllables) > 0:
            unicodeWords.append(unicodeSyllables)
    return(unicodeWords)

def writeNotationToFile(φ):
    f = open(r'../results/result.md', 'w+', encoding='utf-8')
    if type(φ) == alignmentModule:
        allNotes = []
        allNotesTogether = []
        finalNoteLines = []
        for u in φ.notation.text:
            allNotes.append(notationParser(u))
        f.write("||"+ "\n" + "|:---:|")
        for lines in allNotes:
            q = []
            for words in lines:
                for syllables in words:
                    for notes in syllables:
                        q.append(notes)
            allNotesTogether.append(q)
        for j in allNotesTogether:
            g = " ".join(j)
            finalNoteLines.append(g)
        for t in range(len(allNotesTogether)):
            f.write("\n" + "|" + finalNoteLines[t] + "|" + "\n" + "|" + φ.normalized.text[t] + "|" + "\n" + "|" + "" + "|")
    f.close()

x = align("urn:cts:greekMusic:seikilos.1:1-4")
##writeNotationToFile(x)
y = alignedSyllabify(x)

print("\n", x.urn, "\n\n", x.normalized.urn, '\t------->\t', x.normalized.text, '\n', x.lyric.urn, '\t------->\t', x.lyric.text, '\n', x.notation.urn, '\t------->\t', x.notation.text, '\n', x.accent.urn, '\t------->\t', x.accent.text, '\n', x.meter.urn, '\t------->\t', x.meter.text)
print("\n\n\n\n\n")

##for fad in y:
##    print(notationParser(" ".join(fad[2])), "\n", fad[0], "\n\n\n")

##os.system('pandoc --pdf-engine=xelatex --template=default.latex -V fontsize=24 -V mainfont="ALPHABETUM Unicode" ../results/result.md -o ../results/result.pdf')
##print("pdf written")

int3not = []
for line in x.notation.text:
    words = line.split(" ")
    for word in words:
        int2 = []
        syllables = word.split("+")
        for syllable in syllables:
            int1 = []
            notes = syllable.split("~")
            for note in notes:
                int1.append(note)
            int2.append(int1)
        int3not.append(int2)

int3acc = []
for line in x.accent.text:
    words = line.split(" ")
    for word in words:
        int2 = []
        syllables = word.split("+")
        for syllable in syllables:
            int1 = []
            notes = syllable.split("~")
            for note in notes:
                int1.append(note)
            int2.append(int1)
        int3acc.append(int2)

int3lyr = []
for line in x.lyric.text:
    words = line.split(" ")
    for word in words:
        int3lyr.append(word)

for i in range(len(int3not)):
    print(str(int3lyr[i]) + ":\n", int3acc[i], "\n", int3not[i], "\n\n\n")

print("In " + str(x.urn) + ":\n")
for word in y:
    listlistlist = []
    motionList = []
    for syllable in word[2]:
        ph = syllable.split("~")
        listlist = []
        list = []
        for note in ph:
            e = note.split(":")[-1]
            h = e.split(".")[0:2]
            k = (3*int(h[0])) - (3-int(h[1]))
            listlist.append(k)
        motion = listlist[0] - listlist[-1]
        motionList.append(motion)
        listlist.sort()
        u = listlist[-1]
        list.append(u)
        listlistlist.append(list)
    flat_list = []
    for sublist in listlistlist:
        for item in sublist:
            flat_list.append(item)
    flat_list2 = flat_list[:]
    flat_list.sort()
    s = flat_list[-1]
    if word[3].count('/') + word[3].count('=') <= 1:
        for i in range(len(flat_list)):
            if word[3][i] == "/":
                if flat_list2[i] < s:
                    print("\t" + "".join(word[0]) + ": failure (not highest note in word)")
                if motionList[i] > 0:
                    print("\t" + "".join(word[0]) + ": failure (falling motion on acute)")
            if word[3][i] == "=":
                if flat_list2[i] < s:
                    print("\t" + "".join(word[0]) + ": failure (not highest note in word)")
                if motionList[i] < 0:
                    print("\t" + "".join(word[0]) + ": failure (non-falling motion on circumflex)")
