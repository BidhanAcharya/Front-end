from fastapi import FastAPI, Request, UploadFile, HTTPException, status
from fastapi.responses import HTMLResponse
import aiofiles
from pdftools import *
from classobjects import PDF , PresentationData
from bs4 import BeautifulSoup
from pptxtools import *
pdf=PDF()
import pdftitle, pdfplumber
from gemini import gemini_summarize
from presentify_model import summarize
presentation=PresentationData()

app = FastAPI()



app = FastAPI()

MAX_FILE_SIZE = 1024 * 1024 * 12 
@app.post('/extract-text')
async def extract_texts(file: UploadFile ):
    if file.size > MAX_FILE_SIZE:
        raise HTTPException(status_code=413, detail="File is too large")
    pdf_bytes = await file.read()

    # Optionally save the PDF temporarily
    with open('temp_pdf.pdf', 'wb') as f:
        f.write(pdf_bytes)

    pdf.textdata = clean_text(read_pdf('temp_pdf.pdf'))  # Replace with your program's function
    pdf_title = pdftitle.get_title_from_file('temp_pdf.pdf')
    author = pdfplumber.open('temp_pdf.pdf').metadata['Author']
    presentation.author = author
    presentation.title = pdf_title
    gemini_data = PresentationData()
    # gemini_data = gemini_summarize(pdf.textdata)
    try:
        gemini_data = gemini_summarize(pdf.textdata)
        presentation.introduction = gemini_data.introduction
        presentation.literature_review = gemini_data.literature_review
        presentation.methodology = gemini_data.methodology
        presentation.results = gemini_data.results
        presentation.conclusions = gemini_data.conclusions
    except:
        return {'error':'couldnt extract data'}
    data = PresentationData()
    data = summarize(gemini_data)
    data_dict = {'Introduction':data.introduction,
             'Literature Review':data.literature_review, 
             'Methodology':data.methodology, 
             'Results':data.results, 
             'Conclusion':data.conclusions}
    prs = Presentation()
    title_slide_layout = prs.slide_layouts[0]
    bullet_slide_layout = prs.slide_layouts[1]

    #addding page 1
    slide1 = add_slide(prs, title_slide_layout)
    slide1.placeholders[0].text = presentation.title
    slide1.placeholders[1].text= presentation.author

    #font style for title
    customizer_placeholder(slide1,0,'Arial',44,True)

    #font style for author
    customizer_placeholder(slide1,1,'Arial',22,True)

    #bullet slides
    title_list = ['Introduction','Literature Review','Methodology','Results','Conclusion']
    for title in title_list:
        slide2 = add_slide(prs, bullet_slide_layout)
        slide2.placeholders[0].text = title

        content = data_dict[title]
        sentences = split_sentences(content)
        print(sentences)

        slide2.shapes.placeholders[1].text_frame.text = sentences[0]
        customizer_placeholder(slide2,1,'Arial',28,False)

        for i in range(1,len(sentences)):
            p = slide2.shapes.placeholders[1].text_frame.add_paragraph()
            p.text = sentences[i]
            p.level = 0
            #font style for bullet
            customizer_placeholder_paragraphs(slide2,1,i,'Arial',28,False)
    #font style for title
    customizer_placeholder(slide2,0,'Arial',36,True)
    prs.save(f'slides/{presentation.title}.pptx')
    print('slide successfully created')
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
    # gemini_data = gemini_summarize(pdf.textdata)
    try:
        gemini_data = gemini_summarize(pdf.textdata)
        presentation.introduction = gemini_data.introduction
        presentation.literature_review = gemini_data.literature_review
        presentation.methodology = gemini_data.methodology
        presentation.results = gemini_data.results
        presentation.conclusions = gemini_data.conclusions
    except:
        return {'error':'couldnt extract data'}
    data = PresentationData()
    data = summarize(gemini_data)
    data_dict = {'Introduction':data.introduction,
             'Literature Review':data.literature_review, 
             'Methodology':data.methodology, 
             'Results':data.results, 
             'Conclusion':data.conclusions}
    prs = Presentation()
    title_slide_layout = prs.slide_layouts[0]
    bullet_slide_layout = prs.slide_layouts[1]

    #addding page 1
    slide1 = add_slide(prs, title_slide_layout)
    slide1.placeholders[0].text = presentation.title
    slide1.placeholders[1].text= presentation.author

    #font style for title
    customizer_placeholder(slide1,0,'Arial',44,True)

    #font style for author
    customizer_placeholder(slide1,1,'Arial',22,True)
    title_list = ['Introduction','Literature Review','Methodology','Results','Conclusion']
    #bullet slides
    for title in title_list:
        slide2 = add_slide(prs, bullet_slide_layout)
        slide2.placeholders[0].text = title

        content = data_dict[title]
        sentences = split_sentences(content)
        print(sentences)

        slide2.shapes.placeholders[1].text_frame.text = sentences[0]
        customizer_placeholder(slide2,1,'Arial',28,False)

        for i in range(1,len(sentences)):
            p = slide2.shapes.placeholders[1].text_frame.add_paragraph()
            p.text = sentences[i]
            p.level = 0
            #font style for bullet
            customizer_placeholder_paragraphs(slide2,1,i,'Arial',28,False)
    #font style for title
    customizer_placeholder(slide2,0,'Arial',36,True)
    prs.save(f'slides/{presentation.title}.pptx')
    print('slide successfully created')
    return {"message":"Slide created successfully!"}