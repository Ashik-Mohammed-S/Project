"""Development-only selection; one fixed authored test suite, not a public benchmark."""
import hashlib,json,sys
from pathlib import Path
from copilot import Copilot
from retrieval import blocked
ROOT=Path(__file__).parent

def metrics(copilot,cases):
    positive=[c for c in cases if c['relevant']];rows=[]
    for case in cases:
        hits=copilot.retriever.search(case['question'],copilot.config['method'])
        ids=[e['id'] for e in hits]
        ranks=[i+1 for i,key in enumerate(ids) if key in case['relevant']]
        result=copilot.ask(case['question'])
        rows.append(dict(question=case['question'],relevant=case['relevant'],retrieved=ids,
            recall_at_3=len(set(ids)&set(case['relevant']))/len(case['relevant']) if case['relevant'] else None,
            reciprocal_rank=1/min(ranks) if ranks else 0,
            answerable=bool(case['relevant']),abstained=result['abstained'],
            correct_source_answer=bool(set(result['citations'])&set(case['relevant']))))
    answered=[r for r in rows if not r['abstained']]
    unsupported=[r for r in rows if not r['answerable']]
    mean=lambda values:sum(values)/len(values) if values else 0
    return dict(cases=len(rows),answerable_cases=len(positive),unsupported_cases=len(unsupported),
        source_recall_at_3=mean([r['recall_at_3'] for r in rows if r['answerable']]),
        mrr_at_3=mean([r['reciprocal_rank'] for r in rows if r['answerable']]),
        answerability_accuracy=mean([r['answerable']!=r['abstained'] for r in rows]),
        supported_answer_precision=mean([r['correct_source_answer'] for r in answered]),
        unsupported_abstention_rate=mean([r['abstained'] for r in unsupported]),
        correct_source_or_abstain_rate=mean([r['correct_source_answer'] if r['answerable'] else r['abstained'] for r in rows]),rows=rows)

def run(check=False):
    cases=json.loads((ROOT/'data/eval_cases.json').read_text(encoding='utf-8'))
    dev=[c for c in cases if c['split']=='dev'];test=[c for c in cases if c['split']=='test']
    assert not {c['question'] for c in dev}&{c['question'] for c in test}
    candidates=[]
    for method in ['bm25','hybrid']:
        for threshold in [.25,.4,.6,.8]:
            cfg={'method':method,'threshold':threshold}
            m=metrics(Copilot(cfg),dev)
            candidates.append({'config':cfg,'metrics':{k:v for k,v in m.items() if k!='rows'}})
    best=max(candidates,key=lambda r:(r['metrics']['correct_source_or_abstain_rate'],r['metrics']['mrr_at_3']))
    selected=best['config'];copilot=Copilot(selected)
    result={'protocol':'Authored synthetic corpus: 24 development cases select method/threshold; 24 separate test cases are evaluated after selection. No independent or live LLM quality benchmark.',
        'selected_config':selected,'development_candidates':candidates,'test':metrics(copilot,test),
        'bm25_test':metrics(Copilot({'method':'bm25','threshold':selected['threshold']}),test),
        'source_sha256':{f:hashlib.sha256((ROOT/f).read_bytes()).hexdigest() for f in ['data/eval_cases.json','data/knowledge.json','data/synthetic_ledger.csv']},
        'generation_evaluated':False,'limitations':'Source-ID relevance and extractive answers only. Small author-written cases; not independent validation. No claim of semantic faithfulness, production security or employer impact.'}
    path=ROOT/'evaluation/baseline.json'
    if check:
        expected=json.loads(path.read_text(encoding='utf-8'))
        if result!=expected:raise SystemExit('Evaluation differs from the committed baseline; inspect and document the change.')
        if json.loads((ROOT/'config.json').read_text())!=selected:raise SystemExit('Serving configuration differs from selected development configuration')
    else:
        path.parent.mkdir(exist_ok=True);path.write_text(json.dumps(result,indent=2),encoding='utf-8')
        (ROOT/'config.json').write_text(json.dumps(selected,indent=2),encoding='utf-8')
    print(json.dumps({'selected_config':selected,'test':{k:v for k,v in result['test'].items() if k!='rows'}},indent=2))
    return result

if __name__=='__main__':run('--check' in sys.argv)
