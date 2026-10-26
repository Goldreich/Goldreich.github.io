"""Build the dependency-free personal website from editable content and snapshot data."""
import json
import re
from html import escape as e
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DIST = ROOT / 'public'
PROFILE = json.loads((ROOT / 'content.json').read_text())
SNAPSHOT = json.loads((DIST / 'assets/knesset-forecast.json').read_text())
REPO = 'https://github.com/Goldreich/26th-knesset-prediction'
COMMIT = '00a0988471e51f7d89cc7aeb0e42cfa57b2d3713'
SNAPSHOT_REPO = REPO + '/blob/' + COMMIT
DASHBOARD = 'https://goldreich.github.io/26th-knesset-prediction/'
ROWS = sorted([r for r in SNAPSHOT['forecast']['lists'] if r['mean_seats'] > .01], key=lambda r: -r['mean_seats'])

def link(url, text, cls=''):
    return f'<a href="{e(url, quote=True)}"' + (f' class="{cls}"' if cls else '') + f'>{text}</a>'

def shell(title, page, body, description, prefix=''):
    nav = ''.join(f'<a href="{prefix}{path}"'+(' aria-current="page"' if key == page else '')+f'>{label}</a>' for key, path, label in [('home','index.html','Home'),('research','research.html','Research'),('projects','projects.html','Projects'),('cv','cv.html','CV')])
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(title)} · Or Goldreich</title><meta name="description" content="{e(description, quote=True)}">
<meta name="theme-color" content="#faf9f6"><meta property="og:title" content="{e(title)} · Or Goldreich"><meta property="og:description" content="{e(description, quote=True)}"><meta property="og:type" content="website">
<link rel="icon" href="{prefix}assets/favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="{prefix}styles.css"><script src="{prefix}site.js" defer></script></head>
<body><a class="skip" href="#main">Skip to content</a><header class="site-header"><div class="wrap header-inner"><a class="brand" href="{prefix}index.html" aria-label="Or Goldreich home"><span class="monogram" aria-hidden="true">OG</span><span class="brand-name">Or Goldreich</span></a><nav class="nav" aria-label="Main navigation">{nav}</nav></div></header>
<main class="wrap" id="main">{body}</main><footer class="footer"><div class="wrap footer-inner"><span>Or Goldreich · Statistics · University of Chicago</span><span><a href="mailto:{PROFILE['email']}">Email</a> &nbsp; / &nbsp; <a href="{PROFILE['github']}">GitHub</a></span></div></footer></body></html>'''

def authors(text):
    text = re.sub(r',\s*and\s+|\s+and\s+|\s*&\s*', ', ', text, flags=re.I)
    return e(text).replace('Or Goldreich','<strong>Or Goldreich</strong>')

def paper(p):
    title = e(p['title'])
    venue = f'<p class="venue">{e(p["venue"])}</p>' if p.get('venue') else ''
    links = []
    if p.get('url'):
        links.append(link(p['url'],'Paper'))
    if p.get('pdf'):
        links.append(link(p['pdf'],'PDF'))
    downloads = '<div class="pub-links">'+''.join(links)+'</div>' if links else ''
    return f'<article class="paper"><h3>{title}</h3><p class="authors">{authors(p["authors"])}</p>{venue}{downloads}</article>'

def mini_chart(prefix=''):
    names={'Yashar! with Eisenkot':'Yashar!','The Democrats':'Democrats'}
    rows=''
    for r in ROWS[:5]:
        lo,hi=r['interval_80'];mean=r['mean_seats']
        rows+=f'<div class="mini-row"><span>{e(names.get(r["name_en"],r["name_en"]))}</span><span class="track" aria-hidden="true"><span class="interval" style="left:{lo/40*100}%;width:{(hi-lo)/40*100}%"></span><span class="dot" style="left:{mean/40*100}%"></span></span><span class="num">{mean:.1f}</span></div>'
    return f'<div class="figure-panel" aria-label="Expected seats and 80 percent uncertainty intervals for the five lists with the highest expected seats"><p class="eyebrow">Five leading lists · Expected seats</p>{rows}<p class="figure-caption">Dot: expected seats &nbsp; Line: 80% model interval.<br>Frozen forecast · 24 October 2026.</p></div>'

def feature():
    return f'''<div class="project-feature"><div><span class="badge">Bayesian forecasting · 2026</span><h3>26th Knesset Prediction</h3><p>A probabilistic forecast of Israel’s parliamentary election, from national polling measurements to a joint distribution over all 120 seats.</p><p>Daily voting intention, pollster effects, and election-wide uncertainty meet exact seat-allocation rules.</p><div class="button-row">{link('projects/knesset/index.html','Explore the project <span aria-hidden="true">→</span>','button')}</div><div class="link-row">{link(DASHBOARD,'Prediction dashboard ↗')}{link(REPO,'Source code ↗')}</div></div>{mini_chart()}</div>'''

home=f'''<section class="intro home-intro"><div class="home-copy"><h1>Or Goldreich</h1><p class="role">PhD Candidate in Statistics<br>University of Chicago</p><p class="lead">{e(PROFILE['bio'])}</p><p class="bio-more">{e(PROFILE['bio_more'])}</p><div class="link-row">{link('mailto:'+PROFILE['email'],PROFILE['email'])}{link(PROFILE['scholar'],'Google Scholar')}{link(PROFILE['github'],'GitHub')}{link(PROFILE['linkedin'],'LinkedIn')}{link('assets/or-goldreich-cv.pdf','CV (PDF)')}</div></div><div class="profile-photo"><img src="assets/or-goldreich.jpg" alt="Portrait of Or Goldreich" width="1216" height="1536" fetchpriority="high"></div></section>'''
(DIST/'index.html').write_text(shell('Research & projects','home',home,'Or Goldreich, PhD candidate in Statistics at the University of Chicago. Research in stochastic optimization and statistical theory, with applied forecasting projects.'))

research=f'''<section class="page-intro research-intro"><h1>Research</h1><p>{link(PROFILE['scholar'],'Google Scholar')}</p></section><div class="publication-list research-list">'''+''.join(paper(p) for p in PROFILE['publications'])+'''</div>'''
(DIST/'research.html').write_text(shell('Research','research',research,'Papers by Or Goldreich on stochastic gradient descent, convergence, stability, and statistical theory.'))

projects=f'''<section class="page-intro"><h1>Projects</h1><p class="lead">Applied projects in probabilistic forecasting, simulation, and reproducible computation.</p></section><section class="section project-list" aria-label="Featured project">{feature()}</section><section class="small-project"><div><span class="badge">Monte Carlo simulation · 2026</span><h3>Tennis forecasting</h3></div><div><p>A Python pipeline for ATP/WTA match forecasts, combining serve/return estimation, surface-specific Elo, and point-by-point Monte Carlo simulation. Match and proposition probabilities share simulated paths, with versioned inputs and assumptions.</p><p style="margin-top:12px">{link('https://github.com/Goldreich/tennis-model','Source code ↗')}</p></div></section>'''
(DIST/'projects.html').write_text(shell('Projects','projects',projects,'Independent statistical projects by Or Goldreich, featuring a Bayesian forecast for the 26th Knesset and probabilistic tennis modeling.'))

def timeline(date,title,role,description=''):
    return f'<div class="timeline-row"><div class="timeline-date">{date}</div><div><h3>{title}</h3><p class="degree">{role}</p>'+(f'<p>{description}</p>' if description else '')+'</div></div>'

cv='''<section class="page-intro cv-intro"><div><p class="eyebrow">Curriculum vitae</p><h1>Education & experience</h1></div><a class="button" href="assets/or-goldreich-cv.pdf" download>Download CV PDF <span aria-hidden="true">↓</span></a></section><section class="section"><h2>Education</h2>'''
cv+=timeline('2022–present','University of Chicago','PhD in Statistics','Research in stochastic optimization and statistical theory.')
cv+=timeline('2021–2022','Tel Aviv University','Graduate coursework in Statistics and Data Science','Transferred to the University of Chicago PhD program before completing the degree.')
cv+=timeline('2015–2018','Technion – Israel Institute of Technology','BSc in Mathematics, cum laude','GPA: 91.1. Dean’s List on four occasions.')
cv+='</section><section class="section"><h2>Research & engineering</h2>'
cv+=timeline('2022–present','University of Chicago','PhD Candidate, Statistics','Convergence, stability, and statistical properties of stochastic gradient descent.')
cv+=timeline('Feb–Aug 2022','Tel Aviv University','Research Assistant','Mathematical and quantitative support for empirical legal research in antitrust and regulatory policy.')
cv+=timeline('2020–2021','Nvidia Networking','Formal Verification Software Engineer','Developed verification methodology and Python/C tooling for network protocols and low-level dataplane code.')
cv+=timeline('2012–2015','Israeli Air Force','Computing Systems Instructor','Technical support and user training for logistics information systems; developed a C#/.NET/SQL scheduling application.')
cv+='</section><section class="section" id="teaching"><h2>Teaching</h2>'
cv+=timeline('2023–present','University of Chicago','Teaching Assistant','Statistical Models and Methods; Analysis of Categorical Data; Time Dependent Data; Applied Regression Analysis.')
cv+=timeline('2017–2020','Technion – Israel Institute of Technology','Teaching Assistant','Linear and abstract algebra, set theory, and mathematical foundations. Recognized for teaching excellence in three consecutive semesters.')
cv+='</section><section class="section"><h2>Technical skills & languages</h2><p class="skills-line">Python · R · SQL · MATLAB · C · C++ · C# · Java</p><p class="skills-line">Hebrew (native) · English (fluent)</p></section>'
(DIST/'cv.html').write_text(shell('CV','cv',cv,'Education, research, engineering, and teaching experience of Or Goldreich. Download a two-page academic CV.'))

chart_rows=''
for r in ROWS:
    lo,hi=r['interval_80'];lo95,hi95=r['interval_95'];mean=r['mean_seats'];name=r['name_en']
    label=f'{name}: expected seats {mean:.2f}; 80% interval {lo} to {hi} seats.'
    chart_rows+=f'''<div class="chart-row" data-chart-row data-name="{e(name,quote=True)}" data-mean="{mean:.2f}" data-lo80="{lo}" data-hi80="{hi}" data-lo95="{lo95}" data-hi95="{hi95}" aria-label="{e(label,quote=True)}"><span>{e(name)}</span><span class="track" aria-hidden="true"><span class="interval" style="left:{lo/40*100}%;width:{(hi-lo)/40*100}%"></span><span class="dot" style="left:{mean/40*100}%"></span></span><span class="num">{mean:.1f}</span></div>'''

case=f'''<a class="back-link" href="../../projects.html">← All projects</a><section class="page-intro project-intro"><p class="eyebrow">Independent project · Bayesian forecasting</p><h1>26th Knesset Prediction</h1><p class="lead">From polling measurements to a joint probabilistic forecast of all 120 parliamentary seats.</p><p>I built a Bayesian election model that estimates changing voter support and persistent differences between polling series, propagates uncertainty to election day, and applies the electoral rules to each simulated outcome.</p><div class="button-row">{link(DASHBOARD,'Open prediction dashboard ↗','button')}{link(REPO,'View GitHub repository ↗','button secondary')}</div><p class="snapshot">Frozen information cutoff: 24 October 2026, 17:37:50 Israel time.<br>Election date: 27 October 2026. This page displays the issued snapshot.</p></section>
<div class="metrics" aria-label="Project overview"><div class="metric"><strong>69</strong><span>Usable survey reports</span></div><div class="metric"><strong>6</strong><span>Polling series</span></div><div class="metric"><strong>4,000</strong><span>Joint predictive draws</span></div><div class="metric"><strong>120</strong><span>Seats in every draw</span></div></div>
<div class="project-layout"><aside class="article-nav" aria-label="On this page"><p>On this page</p><a href="#forecast">Forecast</a><a href="#methods">Methods</a><a href="#evaluation">Evaluation</a><a href="#limits">Assumptions & limits</a><a href="#reproduce">Reproducibility</a></aside><div>
<section class="article-section" id="forecast"><h2>A distribution, not a single seat count</h2><p>The model produces joint election outcomes. Each draw contains a complete, internally consistent parliament; marginal averages and intervals summarize the possibilities for each list.</p><div class="chart-box"><div class="chart-top"><h3>Expected seats & uncertainty</h3><div class="segmented" role="group" aria-label="Model uncertainty interval"><button data-interval="80" aria-pressed="true">80%</button><button data-interval="95" aria-pressed="false">95%</button></div></div><div class="legend"><span class="legend-dot">Expected seats</span><span class="legend-line" data-interval-label>80% interval</span></div><div class="chart-labels"><span>Electoral list</span><span>Expected seats</span></div><div class="chart-ticks" aria-hidden="true"><span></span><span class="tick-track"><span>0</span><span>10</span><span>20</span><span>30</span><span>40</span></span><span></span></div><div id="seat-chart-rows">{chart_rows}</div><div class="chart-sort"><label for="chart-sort">Order by</label><select id="chart-sort"><option value="seats">Expected seats</option><option value="name">List name</option></select></div><p class="figure-caption">13 lists with expected seats above 0.01, shown from the frozen 24 October 2026 forecast. Intervals are model-based and marginal; their endpoints do not describe one joint parliament.</p><span id="chart-announcement" class="figure-caption" role="status"></span></div><p class="readout">The full dashboard includes all 37 lists, threshold probabilities, joint majority arithmetic, and an estimated most probable exact parliament. A majority in seats is distinct from forming a government.</p><div class="link-row">{link(DASHBOARD,'Explore the full dashboard ↗')}{link('../../assets/knesset-forecast.csv','Download forecast CSV ↓')}</div></section>
<section class="article-section" id="methods"><h2>From observations to parliaments</h2><ol class="steps"><li><strong>Curate the measurements.</strong> Audit campaign reports and retain eligible national percentage observations. Seat-derived percentages and unsupported subgroup reconstructions are excluded. One partial report contributes only its published ratio.</li><li><strong>Estimate changing support.</strong> Fit a compositional state-space model with daily latent voting intention, partially pooled pollster effects, and measurement covariance in log-ratio coordinates.</li><li><strong>Propagate uncertainty.</strong> Integrate variance parameters over a 448-point grid using sparse Gaussian inference. Project to election day and add a shared election-level discrepancy.</li><li><strong>Allocate seats exactly.</strong> Complete the conditional ballot scenario, then apply the 3.25% threshold, six surplus agreements, and rational Bader–Ofer allocation to every draw.</li></ol><p>The implementation adapts polling components from multiparty election-forecasting research. It uses independent conditional Gaussian draws rather than MCMC, and does not fit a fundamentals model or perform MRP.</p>{link(SNAPSHOT_REPO+'/docs/dynamic.md','Read the model specification ↗')}</section>
<section class="article-section" id="evaluation"><h2>What the checks establish</h2><h3>Electoral mechanics</h3><p>The allocation engine reproduces all five official seat vectors from April 2019 through 2022. This checks the seat-allocation rules; it does not measure election-forecast accuracy.</p><h3>Retrospective prediction of later polls</h3><table class="evaluation"><caption class="figure-caption" style="text-align:left;caption-side:bottom">Log-ratio RMSE; smaller is better. Baseline: equally averaged latest observation per polling series and category.</caption><thead><tr><th scope="col">Training through</th><th scope="col">Model</th><th scope="col">Baseline</th></tr></thead><tbody><tr><td>8 October 2026</td><td>0.223</td><td>0.329</td></tr><tr><td>15 October 2026</td><td>0.234</td><td>0.332</td></tr></tbody></table><p class="note">These are two overlapping checks within one campaign using current archived versions. They predict later polls, not election results, and do not establish calibrated threshold or majority probabilities.</p>{link(SNAPSHOT_REPO+'/docs/poll_holdouts.json','View the recorded diagnostics ↗')}</section>
<section class="article-section" id="limits"><h2>Assumptions & limits</h2><ul class="limitations"><li><strong>Limited historical calibration.</strong> Only one historical national-percentage case, from 2022, updates election-wide discrepancy. The forecast has not demonstrated greater election accuracy than a polling average.</li><li><strong>Source verification.</strong> Most observations are archived secondary transcriptions linked to original reports. Not every primary filing was independently cross-checked.</li><li><strong>Conditional ballot completion.</strong> The reference scenario removes Blue and White proportionally and assigns unmeasured minor lists 0.7% combined support, equally split.</li><li><strong>Dependence and interpretation.</strong> Overlapping polling panels are not separately modeled. Majority probabilities describe seat arithmetic, not government formation.</li><li><strong>Exact-parliament search.</strong> The dashboard’s estimated joint mode is the most probable allocation found in a numerical search, not a certified global optimum.</li></ul></section>
<section class="article-section" id="reproduce"><h2>Reproducible by design</h2><p>The public repository contains a Python model, curated frozen inputs, locked dependencies, tests, technical documentation, and a static dashboard. Its reproduction checker compares all 4,000 issued seat vectors and the recovered terminal mixture with the supplied snapshot.</p><p>A separate integration script verifies the probabilities of candidate exact parliaments; it does not repeat the original broad search. The repository records the retrospective holdout results, while the original holdout runner is not redistributed.</p><div class="link-row">{link(REPO+'#reproduce-the-prediction','Reproduction instructions ↗')}{link(SNAPSHOT_REPO+'/data/README.md','Data & provenance ↗')}{link(SNAPSHOT_REPO+'/docs/joint_mode.md','Joint-mode derivation ↗')}</div><p class="source-note" style="margin-top:25px">Charts and methods on this page use repository snapshot <a href="{REPO+'/tree/'+COMMIT}">{COMMIT[:7]}</a>, forecast <code>{SNAPSHOT['forecast_id']}</code>. Snapshot issued 24 October 2026. The linked project may receive later updates.</p></section>
</div></div>'''
out=DIST/'projects/knesset';out.mkdir(parents=True,exist_ok=True)
(out/'index.html').write_text(shell('26th Knesset Prediction','projects',case,'A Bayesian election-forecasting project by Or Goldreich: polling models, joint seat distributions, reproducible computation, and explicit evaluation limits.','../../'))
print('Built five pages from content.json and the pinned Knesset forecast snapshot.')

# Apply the site's punctuation style without a server-side renderer.
for page in DIST.rglob('*.html'):
    page.write_text(re.sub(r',\s+(and|or)\b', r' \1', page.read_text(), flags=re.I))
