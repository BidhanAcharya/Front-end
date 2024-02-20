from fastapi import FastAPI, UploadFile, HTTPException
from classobjects import PDF , PresentationData
from bs4 import BeautifulSoup
import pdftitle, pdfplumber
from pdftools import *
from pptxtools import *
from gemini import gemini_summarize
from presentify_model import summarize

pdf=PDF()
presentation=PresentationData()

app = FastAPI()


def presentation(data_dict,presentation_title,presentation_author):
    
    title_list = ['Introduction','Literature Review','Methodology','Results','Conclusion']
    
    title_color = "black"
    author_color = "black"
    bullet_color = "black"
    bullet_title_color = "black"
    background_color = "white"
    
    prs = pptx.Presentation()

    prs.slide_width = Inches(16)
    prs.slide_height = Inches(9)

    title_slide_layout = prs.slide_layouts[0]
    bullet_slide_layout = prs.slide_layouts[1]

    # addding page 1
    slide1 = add_slide(prs, title_slide_layout)

    slide1.placeholders[0].text = presentation_title
    slide1.placeholders[1].text = presentation_author

    slide1.placeholders[0].width = Inches(10)
    slide1.placeholders[0].height = Inches(2)
    slide1.placeholders[0].left = Inches(3)
    slide1.placeholders[0].top = Inches(3)

    slide1.placeholders[1].width = Inches(10)
    slide1.placeholders[1].height = Inches(2)
    slide1.placeholders[1].left = Inches(3)
    slide1.placeholders[1].top = Inches(4.75)

    # font style for title
    customizer_topics(slide1, 0, 'Arial', 44, True, title_color)

    # font style for author
    customizer_topics(slide1, 1, 'Arial', 22, True, author_color)

    # bullet slides
    for title in title_list:
        slide2 = add_slide(prs, bullet_slide_layout)

        slide2.placeholders[0].text = title

        slide2.placeholders[0].width = Inches(10)
        slide2.placeholders[0].height = Inches(2)
        slide2.placeholders[0].left = Inches(3)
        slide2.placeholders[0].top = Inches(0.25)

        content = data_dict[title]
        sentences = split_sentences(content)

        slide2.shapes.placeholders[1].text_frame.text = sentences[0]

        slide2.placeholders[1].width = Inches(14.5)
        slide2.placeholders[1].height = Inches(6)
        slide2.placeholders[1].left = Inches(0.75)
        slide2.placeholders[1].top = Inches(2)

        customizer_bullet_point(slide2, 1, 0, 'Arial', 28, False, bullet_color)

        for i in range(1, len(sentences)):
            p = slide2.shapes.placeholders[1].text_frame.add_paragraph()
            p.text = sentences[i]
            p.level = 0
            # font style for bullet
            customizer_bullet_point(slide2, 1, i, 'Arial', 28, False, bullet_color)

        # font style for title
        customizer_topics(slide2, 0, 'Arial', 36, True, bullet_title_color)

    customizer_background_color(prs,background_color)
    prs.save(f'slides/{presentation_title}.pptx')
    print('slide successfully created')
    
MAX_FILE_SIZE = 1024 * 1024 * 12 

@app.post('/extract-text')
async def extract_texts(file: UploadFile ):
    if file.size > MAX_FILE_SIZE:
        raise HTTPException(status_code=413, detail="File is too large")
    pdf_bytes = await file.read()

    # Optionally save the PDF temporarily
    with open('temp_pdf.pdf', 'wb') as f:
        f.write(pdf_bytes)

    pdf.textdata = clean_text(read_pdf('temp_pdf.pdf'))
    pdf_title = pdftitle.get_title_from_file('temp_pdf.pdf')
    try:
        author = pdfplumber.open('temp_pdf.pdf').metadata['Author']
    except:
        author = ''
    presentation.author = author
    presentation.title = pdf_title
    gemini_data = PresentationData()
    
    try:
        gemini_data = gemini_summarize(pdf.textdata)
        presentation.introduction = clean_text(gemini_data.introduction)
        presentation.literature_review = clean_text(gemini_data.literature_review)
        presentation.methodology = clean_text(gemini_data.methodology)
        presentation.results = clean_text(gemini_data.results)
        presentation.conclusions = clean_text(gemini_data.conclusions)
    except:
        return {'error':'couldnt extract data'}
    data = PresentationData()
    data = summarize(gemini_data)
    data_dict = {'Introduction':data.introduction,
             'Literature Review':data.literature_review, 
             'Methodology':data.methodology, 
             'Results':data.results, 
             'Conclusion':data.conclusions}
    #number 1 call function:
    presentation(data_dict,presentation.title,presentation.author)
    return {"message":"Slide created successfully!"}

@app.post("/get_data_from_url")
async def get_data_fromI_url(arxiv_url: str):
    response = requests.get(arxiv_url)
    response = response.content
    soup = BeautifulSoup(response, 'html.parser')

    presentation.title =  soup.find('h1', class_='title mathjax').text
    presentation.author = soup.find('div', class_='authors').text
    pdf_link = arxiv_url.replace('abs', 'pdf')
    pdf.textdata = clean_text(read_pdf_from_url(pdf_link))
    presentation.title = presentation.title.replace('Title:','')
    presentation.author = presentation.author.replace('Authors:','')
    gemini_data = PresentationData()
   
    try:
        gemini_data = gemini_summarize(pdf.textdata)
        presentation.introduction = clean_text(gemini_data.introduction)
        presentation.literature_review = clean_text(gemini_data.literature_review)
        presentation.methodology = clean_text(gemini_data.methodology)
        presentation.results = clean_text(gemini_data.results)
        presentation.conclusions = clean_text(gemini_data.conclusions)
    except:
        return {'error':'couldnt extract data'}
    data = PresentationData()
    data = summarize(gemini_data)
    data_dict = {'Introduction':data.introduction,
             'Literature Review':data.literature_review, 
             'Methodology':data.methodology,
             'Results':data.results, 
             'Conclusion':data.conclusions}
    #number 2
    presentation(data_dict,presentation.title,presentation.author)
    return {"message":"Slide created successfully!"}