from flask import Flask, request , render_template ,redirect

# import pdfminer
from pdfminer.high_level import extract_text , extract_pages
from pdfminer.layout import LTTextContainer , LTChar , LTTextBoxHorizontal

app = Flask(__name__)

@app.route('/')
def index():
    return redirect('/process_pdf')

@app.route('/process_pdf', methods=['POST','GET'])
def process_pdf():
    request.form['form']
    uploadfile = request.files.get('pdf_file')
    if request.method == 'POST':
        
        if uploadfile:
            certificates =  extract_certifications(extract_text_font(uploadfile))
    return render_template('home.html',certificates)



def extract_text_font(pdf_file):
    text_font = []
    for page_layout in extract_pages(pdf_file):
        # print(page_layout)
        for container in page_layout:
            if isinstance(container, LTTextBoxHorizontal):
                for line in container:
                        text = line.get_text()
                        # print(text)
                    # for line in element:
                        for character in line:
                            if isinstance(character, LTChar):
                                if hasattr(character, "fontname"):
                                    font_name = character.fontname
                                    fontsize = character.size

                        text_font.append([text,font_name,fontsize])            
    return text_font                            

# details_list = extract_text_font(pdf_content)    
# print(details_list)   


def extract_certifications(data):
    headings = []
    paragraphs = []
    current_heading = ''
    current_paragraph = []
    for i in range(1, len(data)-1):
        current_data = data[i]
        next_data = data[i + 1]
        previous_data = data[i - 1]
        # print(current_data)
        if current_data[2] > next_data[2] and current_data[2] > previous_data[2] :
            if current_heading != '':
                headings.append(current_heading)
                paragraphs.append(' '.join(current_paragraph))
            current_heading = current_data[0]
            
            # current_paragraph = []
        elif current_data[1] != next_data[1] and current_data[1] != previous_data[1] :
            if current_heading != '':
                headings.append(current_heading)
                paragraphs.append(' '.join(current_paragraph))
            current_heading = current_data[0]
            current_paragraph = []
        else:
            current_paragraph.append(current_data[0])
    if current_heading != '':
        headings.append(current_heading)
        paragraphs.append(' '.join(current_paragraph))
    # print(current_heading)    
    dictt =  {headings[i]: paragraphs[i] for i in range(len(headings))}
    # print(dictt)

    for key , value in dictt.items():
        text1 = ''.join(key.split()) #check in all headings
        if 'certification' in text1.lower():
            # print('Certifications:' , value)
            return value.strip().split('\n')















    #         pdf_reader = extract_text(uploadfile)

    #         paragraphs = pdf_reader.split('\n')

    #         i = 0
    #         while i < len(paragraphs):
    #             paragraph = paragraphs[i]
    #             if len(paragraph) == 0:
    #                 i += 1
    #                 continue
    #             elif 'font style="bold"' in paragraph and 'font size="bigger"' in paragraph:
    #                 # If the paragraph has bold text and font size bigger than the rest of the text, add a heading
    #                 html_template += '<h2>' + paragraph + '</h2>\n'
    #                 i += 1
    #                 paragraph_text = []
    #                 while i < len(paragraphs) and ('font style="bold"' not in paragraphs[i] or 'font size="bigger"' not in paragraphs[i]):
    #                     paragraph_text.append(paragraphs[i])
    #                     i += 1
    #                 html_template += '<p>' + '\n'.join(paragraph_text) + '</p>\n'
    #             else:
    #                 i += 1
    #         html_template += '</body>\n</html>'

        #     text = ''
        #     for page in range(len(pdf_reader.pages)):
        #         text += pdf_reader.pages[page].extract_text()

        # words = nltk.word_tokenize(text)
    
        # Check if "Certification" or similar headers are present in the text
        # certifications = []
        # for word in words:
        #     if word.lower() in ["certification", "certifications", "certified"]:
        #         # Extract the certification details that come after this word
        #         certification = []
        #         for w in words[words.index(word)+1:]:
        #             if w.lower() not in ["certification", "certifications", "certified"]:
        #                 certification.append(w)
        #             else:
        #                 break
        #         certifications.append(" ".join(certification))
    #         return html_template
    # return render_template('home.html',html_template)

if __name__ == '__main__':
    app.run(debug=True)




# Extract the text from the PDF file
# text_content = pdfminer.high_level.extract_text('document.pdf')

# # Split the text into paragraphs based on newline characters
# paragraphs = text_content.split('\n')

# # Initialize the HTML template
# html_template = '<html>\n<body>\n'

# # Loop through each paragraph and add a div with a heading for each
# i = 0
# while i < len(paragraphs):
#     paragraph = paragraphs[i]
#     if len(paragraph) == 0:
#         i += 1
#         continue
#     elif 'font style="bold"' in paragraph and 'font size="bigger"' in paragraph:
#         # If the paragraph has bold text and font size bigger than the rest of the text, add a heading
#         html_template += '<h2>' + paragraph + '</h2>\n'
#         i += 1
#         paragraph_text = []
#         while i < len(paragraphs) and ('font style="bold"' not in paragraphs[i] or 'font size="bigger"' not in paragraphs[i]):
#             paragraph_text.append(paragraphs[i])
#             i += 1
#         html_template += '<p>' + '\n'.join(paragraph_text) + '</p>\n'
#     else:
#         i += 1

# # Close the HTML template
# html_template += '</body>\n</html>'

