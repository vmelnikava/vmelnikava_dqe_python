# import regexp module
import re

# create new input string
mystr = """homEwork:

  tHis iz your homeWork, copy these Text to variable.

 

  You NEED TO normalize it fROM letter CASEs point oF View. also, create one MORE senTENCE witH LAST WoRDS of each existING SENtence and add it to the END OF this Paragraph.

 

  it iZ misspeLLing here. fix“iZ” with correct “is”, but ONLY when it Iz a mistAKE.

 

  last iz TO calculate nuMber OF Whitespace characteRS in this Tex. caREFULL, not only Spaces, but ALL whitespaces. I got 87."""

# create new string variable
mystr2 = ''

# Step 1 to normalize string from letter cases point of view
mystr = mystr.capitalize()

# Step2 - Splitting input string into sentences using regex (take substr before :.!?)
for sentence in re.findall(r'[^.?!:]+[.?!:]+', mystr):
    # search for the first word in a sentence using regex, exclude None to avoid exceptions if empty sentence
    if (first_word := re.search(r'(\w+)', sentence)) is not None:
        # On success, take group() value from the match and replace it in text with capitalized one
        sentence = sentence.replace(first_word.group(0), first_word.group(0).capitalize())
    # add modified sentence to new string for normalized text
    mystr2 += sentence

# Print normalized text
print('\n---Normalized text:---')
print(mystr2)

# Create one more sentence with last words
# Using findall to find all LAST words from normalized text and create new string from them
mystr3 = (' '.join(re.findall(r'\s*(\w+)\s*[.:]', mystr2)).capitalize()) + '.'
# Print new sentence consisted of last words only
print('\n---New sentence with last words---')
print(mystr3)

# To add new sentence after a word Paragraph create variable indicating where to put new sentence
substr = 'paragraph.'
# Split normalized text by 'paragraph.' and join new sentence to it after substr
mystr4 = (substr + ' ' + mystr3).join(mystr2.split(substr))
# Print new text with added sentence of last words
print('\n---Added new sentence with last words---')
print(mystr4)

# Replace IZ with is
# find all matches (insensitive ?i, look for 'iz' with spaces before and after and replace wit is
mystr5 = re.sub(r'(?i)(?<=\s)iz(?=\s)', 'is', mystr4)

# print text with fixed 'iz'
print('\n---TEXT WITH FIXED IZ---')
print(mystr5)

# create new variable to count whitespaces in text
count = 0
# Run for cycle for each character in INITIAL text
for i in mystr:
    # if character is not equal to ' ', '\n', '\t'
    if not i.isspace():
        # do nothing
        continue
    # if character is equal to ' ', '\n', '\t' then increase number of found whitespaces
    count += 1
# print number of whitespaces
print("\n---Number of whitespaces in initial text--- ")
print(count)
