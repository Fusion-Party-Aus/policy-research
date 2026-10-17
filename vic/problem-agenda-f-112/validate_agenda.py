"""Validate the bounded F-112 evidence pack without changing frozen files."""
from pathlib import Path
import csv,json,hashlib,re,subprocess,collections

R=Path(__file__).resolve().parent
checks=[]
def check(name,condition,detail=''):
 checks.append(dict(check=name,passed=bool(condition),detail=detail))
def read(n):return list(csv.DictReader((R/n).open(encoding='utf-8')))
def digest(b):return hashlib.sha256(b).hexdigest()
freeze=json.loads((R/'ranking-frozen.json').read_text())
check('frozen core hashes',all(digest((R/n).read_bytes())==h for n,h in freeze['files'].items()),str(len(freeze['files']))+' files')
register=read('problem-register.csv'); sources=read('sources.csv');ev=read('evidence-matrix.csv');cover=read('coverage-ledger.csv')
pids={r['problem_id'] for r in register};allp=pids|{'VP-012'};sids={s['source_id'] for s in sources}
check('unique ranked problem IDs',len(pids)==len(register)==11)
check('ranking ordering matches freeze',[r['problem_id'] for r in register]==freeze['ordered_ids'])
check('rank numbers',sorted(int(r['rank']) for r in register)==list(range(1,12)))
weights=freeze['weights']
check('ratings 1 to 5',all(1<=int(r[k])<=5 for r in register for k in weights))
check('weighted scores',all(abs(sum(int(r[k])*v for k,v in weights.items())/5-float(r['score']))<1e-8 for r in register))
check('source IDs unique',len(sids)==len(sources)==18)
check('evidence rows unique',len({r['evidence_id'] for r in ev})==len(ev)==20)
check('evidence references',all(r['source_id'] in sids and set(r['problem_ids'].split(';'))<=allp for r in ev))
check('register source references',all(set(r['source_ids'].split(';'))<=sids for r in register))
check('problem coverage denominator',len(cover)==12 and {r['problem_id'] for r in cover}==allp)
check('no response appraisals claimed',all(int(r['response_options_appraised'])==0 and r['response_search_state']=='not started' for r in cover))
check('measurement coverage',{r['problem_id'] for r in read('measurement-plan.csv')}==allp)
check('rating explanations',{r['problem_id'] for r in read('rating-rationales.csv')}==pids)

snap=json.loads((R/'provenance/snapshot-manifest.json').read_text())
check('original snapshot byte hashes',all(digest((R/s['file']).read_bytes())==s['sha256'] for s in snap))
inventory=read('corpus-coverage.csv');cross=read('corpus-crosswalk.csv')
check('corpus denominator',collections.Counter(r['item_type'] for r in inventory)=={'policy':41,'research':25})
check('original IDs preserved uniquely',len({(r['item_type'],r['original_id']) for r in inventory})==66)
check('corpus evidence remains unassessed',all(r['evidence_assessed']=='no' and r['adoption_independently_verified']=='no' for r in inventory))
raw={name:json.loads((R/'provenance'/name).read_text()) for name in ['policies.json','research.json']}
recordchecks=[]
for row in inventory:
 obj=raw[Path(row['source_snapshot']).name]
 for key in row['json_pointer'].strip('/').split('/'):
  obj=obj[int(key)] if isinstance(obj,list) else obj[key]
 recordchecks.append(obj['id']==row['original_id'] and digest(json.dumps(obj,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode())==row['record_sha256_canonical_json'])
check('66 original record pointers and canonical hashes',all(recordchecks))
origpol={r['original_id'] for r in inventory if r['item_type']=='policy'}
origres={r['original_id'] for r in inventory if r['item_type']=='research'}
check('crosswalk denominator',len(cross)==12 and {r['problem_id'] for r in cross}==allp)
check('crosswalk original IDs',all((set(r['policy_ids'].split(';'))-{''})<=origpol and (set(r['research_ids'].split(';'))-{''})<=origres for r in cross))
check('crosswalk recorded after freeze',all(r['mapped_at_utc']>freeze['frozen_at_utc'] for r in cross))
check('corpus mapping reconciles',sum(r['mapping_state']=='associated' for r in inventory)==39 and sum(r['mapping_state']!='associated' for r in inventory)==27)

cfg=json.loads((R/'screening-config.json').read_text())
check('protocol not confirmed',cfg['protocol_status']=='unconfirmed' and cfg['confirmation'] is None)
check('finite proposed limits',cfg['proposed_limits']==dict(hours=12,unique_candidate_records=80,deeply_appraised_documents=30,atomic_assessments=8,pilot_records_max=20))
check('ordered screening codes',[r['code'] for r in cfg['exclusion_codes']]==['E1','E2','E3','E4','E5','E6'])
check('screening seeds not invented',cfg['seeds']==[])
sens=read('sensitivity.csv')
check('sensitivity coverage',len(sens)==8*11 and all(sum(r['scenario']==k for r in sens)==11 for k in {r['scenario'] for r in sens}))
check('discovery query log',len(read('search-log.csv'))==42)
links=read('link-checks.csv')
check('one bounded network check per URL',len(links)==21 and len({r['url'] for r in links})==21)

broken=[]
for p in R.rglob('*.md'):
 for target in re.findall(r'\]\(([^)]+)\)',p.read_text()):
  if target.startswith(('https://','http://','mention://')):continue
  if not (p.parent/target.split('#')[0]).exists():broken.append(str(p.relative_to(R))+': '+target)
check('local Markdown links',not broken,'; '.join(broken))
absrefs=[]
for p in R.rglob('*.md'):
 if '/home/ethan/' in p.read_text() or 'file://' in p.read_text():absrefs.append(str(p.relative_to(R)))
check('no runtime-local deliverable links',not absrefs,','.join(absrefs))
receipt=json.loads((R/'freeze-receipt.json').read_text())
try:
 for name,h in freeze['files'].items():
  b=subprocess.check_output(['git','show',receipt['git_tree_before_corpus_read']+':vic/problem-agenda-f-112/'+name],cwd=R)
  if digest(b)!=h:raise ValueError(name)
 check('independent Git tree matches frozen core',True)
except Exception as e:check('independent Git tree matches frozen core',False,str(e))
result=dict(status='passed' if all(c['passed'] for c in checks) else 'failed',checks=checks,counts=dict(ranked_problems=11,unranked_sentinels=1,retained_source_records=18,evidence_rows=20,corpus_records=66,topic_associated_corpus_records=39,unassociated_corpus_records=27,response_options_appraised=0,discovery_queries=42),limitations=['Structural and arithmetic checks do not validate all substantive claims.','Network errors and challenges are retained access exceptions, not evidence failures by default.','Single-session AI self-review; no independent human review or formal screening.'])
(R/'validation.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(dict(status=result['status'],passed=sum(x['passed'] for x in checks),checks=len(checks),failed=[x for x in checks if not x['passed']]),indent=2))
raise SystemExit(0 if result['status']=='passed' else 1)
