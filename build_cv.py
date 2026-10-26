from pathlib import Path
from html import escape
import json
import os
import re
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle, KeepTogether
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.enums import TA_RIGHT
from reportlab.lib.pagesizes import letter

ROOT = Path(__file__).resolve().parent
content = json.loads((ROOT / 'content.json').read_text(encoding='utf-8'))
out = ROOT / 'public' / 'assets' / 'or-goldreich-cv.pdf'
out.parent.mkdir(parents=True, exist_ok=True)
# Set CV_FONT_DIR to use local DejaVu fonts; standard PDF fonts are a portable fallback.
font_dir = Path(os.environ.get('CV_FONT_DIR', '/usr/share/fonts/truetype/dejavu'))
if all((font_dir / f).is_file() for f in ['DejaVuSans.ttf', 'DejaVuSans-Bold.ttf', 'DejaVuSerif.ttf']):
    for name, file in [('Body','DejaVuSans.ttf'), ('BodyBold','DejaVuSans-Bold.ttf'), ('Heading','DejaVuSerif.ttf')]:
        pdfmetrics.registerFont(TTFont(name, str(font_dir / file)))
    pdfmetrics.registerFontFamily('Body', normal='Body', bold='BodyBold', italic='Body', boldItalic='BodyBold')
    body_font, heading_font = 'Body', 'Heading'
else:
    body_font, heading_font = 'Helvetica', 'Times-Roman'
ink=colors.HexColor('#262B28'); muted=colors.HexColor('#636B65'); accent=colors.HexColor('#3E6451'); rule=colors.HexColor('#D6DCD5')
styles={
 'name':ParagraphStyle('name',fontName=heading_font,fontSize=29,leading=35,textColor=ink,spaceAfter=4),
 'sub':ParagraphStyle('sub',fontName=body_font,fontSize=10.2,leading=14,textColor=muted,spaceAfter=6),
 'body':ParagraphStyle('body',fontName=body_font,fontSize=10.2,leading=14,textColor=ink,spaceAfter=4),
 'section':ParagraphStyle('section',fontName=heading_font,fontSize=15,leading=20,textColor=accent,spaceBefore=11,spaceAfter=6,keepWithNext=True),
 'role':ParagraphStyle('role',fontName=body_font,fontSize=10.2,leading=14,textColor=ink,spaceAfter=3,keepWithNext=True),
 'date':ParagraphStyle('date',fontName=body_font,fontSize=9.1,leading=14,textColor=muted,alignment=TA_RIGHT),
 'pub':ParagraphStyle('pub',fontName=body_font,fontSize=10.2,leading=14,textColor=ink,spaceAfter=11),
 'small':ParagraphStyle('small',fontName=body_font,fontSize=9.4,leading=13.4,textColor=muted,spaceAfter=4),
}
story=[]
def p(s,style='body'): return Paragraph(s,styles[style])
def add(s,style='body'): story.append(p(s,style))
def section(s): add(s,'section')
def comma_separated_authors(value):
    return re.sub(r',?\s+and\s+', ', ', value, flags=re.IGNORECASE)
def entry(name,role,dates,desc=None):
    left=p('<b>'+name+'</b><br/>'+role,'role')
    right=p(dates,'date')
    table=Table([[left,right]],colWidths=[343,161],hAlign='LEFT')
    table.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),0),('RIGHTPADDING',(0,0),(-1,-1),0),('TOPPADDING',(0,0),(-1,-1),0),('BOTTOMPADDING',(0,0),(-1,-1),2)]))
    items=[table]
    if desc: items.append(p(desc))
    items.append(Spacer(1,3))
    story.append(KeepTogether(items))

add(escape(content['name']), 'name')
add('Statistics · Stochastic optimization · Probabilistic modeling','sub')
add('Chicago, Illinois · <link href="mailto:' + escape(content['email']) + '" color="#3E6451">' + escape(content['email']) + '</link>', 'sub')
section('Research interests')
add('Convergence, stability and statistical properties of stochastic gradient descent; learning-rate schedules, gradient noise, concentration inequalities and high-dimensional statistical theory.')
section('Education')
entry('The University of Chicago','PhD in Statistics','September 2022 - present')
entry('Tel Aviv University','Graduate coursework in Statistics and Data Science','October 2021 - June 2022','Transferred to the University of Chicago PhD program before completing the degree.')
entry('Technion - Israel Institute of Technology','BSc in Mathematics, cum laude','October 2015 - September 2018','GPA: 91.1. Dean’s List on four occasions.')
section('Papers')
for publication in content['publications']:
    authors = escape(comma_separated_authors(publication['authors']))
    title = escape(publication['title']).replace('Lᵖ', 'L<super>p</super>')
    venue = publication.get('venue', '').strip()
    # Submission destinations are private workflow details and are omitted from the CV.
    if venue.lower().startswith('submitted'):
        venue = ''
    suffix = ' <font color="#636B65">' + escape(venue.rstrip('.') + '.') + '</font>' if venue else ''
    add(authors.rstrip('.') + '. <b>' + title.rstrip('.') + '.</b>' + suffix, 'pub')

story.append(PageBreak())
section('Engineering and research experience')
entry('Nvidia Networking','Formal Verification Software Engineer · Tel Aviv-Yafo','February 2020 - November 2021','Developed verification methodology and Python/C tooling for network protocols and low-level dataplane code. Built reusable macros and automation scripts; consulted on numerical logic, correctness and edge cases.')
entry('Tel Aviv University','Research Assistant · Tel Aviv-Yafo','February 2022 - August 2022','Provided mathematical and quantitative support for empirical legal research in antitrust and regulatory policy. Helped formulate quantitative arguments, structure empirical analyses and interpret model outcomes.')
entry('Israeli Air Force','Computing Systems Instructor · Tzrifin','January 2012 - January 2015','Managed a logistics information system and delivered technical support and user training. Designed and implemented a C#/.NET/SQL application for time tracking and scheduling.')
section('Teaching')
entry('The University of Chicago','Teaching Assistant','January 2023 - present','Office hours and grading for STAT 23400 Statistical Models and Methods, STAT 22600 Analysis of Categorical Data, STAT 26100 Time Dependent Data and STAT 22400 Applied Regression Analysis.')
entry('Technion - Israel Institute of Technology','Teaching Assistant','October 2017 - January 2020','Taught linear and abstract algebra, set theory and mathematical foundations. Prepared original recitation notes; received recognition for excellence in teaching in three consecutive semesters.')
section('Skills, languages and service')
add('<b>Technical:</b> Python, R, SQL, MATLAB, C, C++, C#, Java; .NET application development.')
add('<b>Languages:</b> Hebrew (native); English (fluent).')
add('<b>Service:</b> Technion department student committee member for two years.')

class CVCanvas(canvas.Canvas):
    def __init__(self,*a,**kw):
        super().__init__(*a,**kw)
        self.states=[]
    def showPage(self):
        self.states.append(dict(self.__dict__))
        self._startPage()
    def save(self):
        count=len(self.states)
        for state in self.states:
            self.__dict__.update(state)
            self.setStrokeColor(rule)
            self.setLineWidth(.6)
            self.line(54,43,558,43)
            self.setFont(body_font,8)
            self.setFillColor(muted)
            self.drawString(54,29,content['name'] + ' | Curriculum vitae')
            self.drawRightString(558,29,f'{self._pageNumber} / {count}')
            if self._pageNumber>1:
                self.setFont(body_font,8.5)
                self.drawString(54,759,content['name'].upper())
                self.drawRightString(558,759,'STATISTICS · RESEARCH · PROJECTS')
            super().showPage()
        super().save()

doc=SimpleDocTemplate(str(out),pagesize=letter,leftMargin=54,rightMargin=54,topMargin=45,bottomMargin=59,title=content['name'] + ' - Curriculum Vitae',author=content['name'])
doc.build(story,canvasmaker=CVCanvas)
print(out)
