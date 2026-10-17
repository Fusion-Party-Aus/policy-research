"""One bounded reachability check; does not establish evidential validity."""
from pathlib import Path
import csv,datetime,hashlib,concurrent.futures,urllib.request,urllib.error

R=Path(__file__).resolve().parent
sources=list(csv.DictReader((R/'sources.csv').open()))
extra=[
 {'source_id':'S16-XML','url':'https://www.ebi.ac.uk/europepmc/webservices/rest/PMC11865758/fullTextXML'},
 {'source_id':'S16-PubMed','url':'https://pubmed.ncbi.nlm.nih.gov/40010814/'},
 {'source_id':'access-exception-VAHI','url':'https://vahi.vic.gov.au/emergency-care/length-stay'},
]
def check(s):
 row=dict(source_id=s['source_id'],url=s['url'],checked_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),http_status='',final_url='',response_bytes_sampled=0,response_sample_sha256='',state='',note='A response code alone does not establish substantive access or claim support; previous browser reads are recorded in sources.csv.')
 try:
  req=urllib.request.Request(s['url'],headers={'User-Agent':'PolicyResearchLinkCheck/1.0'})
  with urllib.request.urlopen(req,timeout=12) as resp:
   b=resp.read(2_000_000);row.update(http_status=resp.status,final_url=resp.url,response_bytes_sampled=len(b),response_sample_sha256=hashlib.sha256(b).hexdigest(),state='response_received')
   lower=b.lower()
   if any(x in lower[:20000] for x in [b'checking your browser',b'verify you are human',b'just a moment...',b'recaptcha']):row['state']='possible_browser_challenge'
   if b.startswith(b'%PDF'):row['state']='pdf_response_received'
 except urllib.error.HTTPError as e:row.update(http_status=e.code,final_url=e.url,state='http_error',note=str(e))
 except Exception as e:row.update(state='request_error',note=type(e).__name__+': '+str(e))
 return row

with concurrent.futures.ThreadPoolExecutor(max_workers=7) as pool:rows=list(pool.map(check,sources+extra))
with (R/'link-checks.csv').open('w',newline='',encoding='utf-8') as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
for r in rows:print(r['source_id'],r['http_status'],r['state'])
